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
    first_line, _, rest = raw.partition("\n")
    vote = "yes" in first_line.lower()
    rationale = rest.split("Rationale:", 1)[-1].strip() if rest else ""
    return vote, rationale


def evaluate_job(job_id: str) -> List[PersonaEvaluation]:
    conn = _get_conn()
    results: List[PersonaEvaluation] = []
    agents = _build_agents(job_id)
    try:
        cur = conn.cursor()
        for persona_id in MOTIVATIONAL_PERSONAS:
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
