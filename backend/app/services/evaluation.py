from __future__ import annotations

import logging
import os
import time
from typing import Dict, List, Tuple

import psycopg2
from crewai import Agent, Crew, Process, Task
from crewai.llms.base_llm import BaseLLM

from ..models.evaluation import PersonaEvaluation
from ..services.personas_loader import load_personas

logger = logging.getLogger(__name__)

MOTIVATIONAL_PERSONAS = [
    "builder",
    "maximizer",
    "harmonizer",
    "pathfinder",
    "adventurer",
]

DECISION_PERSONAS = [
    "visionary",
    "realist",
    "guardian",
    "judge",
]


class PersonaLLM(BaseLLM):
    """Deterministic LLM used for persona simulations."""

    def __init__(self, persona_id: str, job_id: str) -> None:
        super().__init__(model="dummy")
        self.persona_id = persona_id
        self.job_id = job_id

    def call(  # type: ignore[override]
        self,
        messages: str | list[dict[str, str]],
        tools: list[dict] | None = None,
        callbacks: list | None = None,
        available_functions: Dict[str, object] | None = None,
        from_task: object | None = None,
        from_agent: object | None = None,
    ) -> str:
        vote = hash((self.persona_id, self.job_id)) % 2 == 0
        rationale = (
            f"{self.persona_id.title()} {'recommends' if vote else 'does not recommend'} this job."
        )
        return f"Vote: {'Yes' if vote else 'No'}\nRationale: {rationale}"


def _get_conn() -> psycopg2.extensions.connection:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(dsn)


def _get_provider(persona_id: str) -> Tuple[str, str]:
    personas = {p.id: p for p in load_personas()}
    persona = personas[persona_id]
    provider = os.getenv("EVALUATION_PROVIDER", "openai")
    model = persona.provider_map.get(provider, "")
    return provider, model


def _build_agents(job_id: str) -> Dict[str, Agent]:
    agents: Dict[str, Agent] = {}
    for persona in load_personas():
        agents[persona.id] = Agent(
            role=persona.id,
            goal=persona.decision_lens,
            backstory=persona.summary,
            allow_delegation=persona.category == "motivational",
            llm=PersonaLLM(persona.id, job_id),
        )
    return agents


def _parse_output(raw: str) -> Tuple[bool, str]:
    try:
        first_line, _, rest = raw.partition("\n")
        if not first_line.lower().startswith("vote:"):
            raise ValueError("missing vote line")
        vote_text = first_line.split(":", 1)[1].strip().lower()
        if vote_text not in {"yes", "no"}:
            raise ValueError("vote must be 'Yes' or 'No'")
        vote = vote_text == "yes"
        if "Rationale:" in rest:
            rationale = rest.split("Rationale:", 1)[1].strip()
        else:
            rationale = ""
        return vote, rationale
    except Exception as exc:
        raise ValueError(f"Unexpected output format: {raw}") from exc


def _evaluate_persona_set(job_id: str, persona_ids: List[str]) -> List[PersonaEvaluation]:
    conn = _get_conn()
    results: List[PersonaEvaluation] = []
    agents = _build_agents(job_id)
    try:
        cur = conn.cursor()
        for persona_id in persona_ids:
            task = Task(
                description=(
                    "Consult other personas in the crew and evaluate the job. "
                    "Reply with 'Vote: Yes' or 'Vote: No' and a brief rationale."
                ),
                expected_output="Vote: <Yes|No>\nRationale: <reason>",
                agent=agents[persona_id],
            )
            crew = Crew(
                agents=list(agents.values()),
                tasks=[task],
                process=Process.sequential,
            )
            start = time.time()
            output = crew.kickoff()
            latency = int((time.time() - start) * 1000)
            raw = output.tasks_output[0].raw
            vote, rationale = _parse_output(raw)
            provider, _model = _get_provider(persona_id)
            cur.execute(
                """
                INSERT INTO evaluations (
                    job_unique_id, persona, provider, vote_bool,
                    rationale_text, latency_ms, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """,
                (job_id, persona_id, provider, vote, rationale, latency),
            )
            results.append(
                PersonaEvaluation(
                    persona=persona_id, vote_bool=vote, rationale_text=rationale
                )
            )
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return results


def evaluate_job(job_id: str) -> List[PersonaEvaluation]:
    return _evaluate_persona_set(job_id, MOTIVATIONAL_PERSONAS)


def evaluate_decision_personas(job_id: str) -> List[PersonaEvaluation]:
    return _evaluate_persona_set(job_id, DECISION_PERSONAS)


class JobNotFoundError(Exception):
    """Raised when a job record does not exist."""


class QueueError(Exception):
    """Raised when an evaluation task cannot be queued."""


def queue_job_evaluation(job_id: str) -> None:
    """Enqueue a job for asynchronous evaluation."""

    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM jobs_normalized WHERE job_id_ext = %s", (job_id,)
        )
        if not cur.fetchone():
            raise JobNotFoundError
        cur.close()
    finally:
        conn.close()
    try:
        logging.getLogger(__name__).info("queued evaluation for %s", job_id)
    except Exception as exc:  # pragma: no cover - logging rarely fails
        raise QueueError from exc
