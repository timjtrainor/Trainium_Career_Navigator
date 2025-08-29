from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.services import evaluation as evaluation_service
from backend.app.models.evaluation import PersonaEvaluation


class FakeCursor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple]] = []

    def execute(self, query: str, params: tuple) -> None:
        self.calls.append((query, params))

    def close(self) -> None:  # pragma: no cover - no action
        pass


class FakeConn:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursor()

    def cursor(self) -> FakeCursor:
        return self.cursor_obj

    def commit(self) -> None:  # pragma: no cover - no action
        pass

    def close(self) -> None:  # pragma: no cover - no action
        pass


def test_evaluate_job_crewai(monkeypatch) -> None:
    monkeypatch.setattr(evaluation_service, "_get_conn", lambda: FakeConn())
    results = evaluation_service.evaluate_job("job1")
    assert len(results) == 5
    assert all(isinstance(r, PersonaEvaluation) for r in results)
    personas = {r.persona for r in results}
    assert personas == set(evaluation_service.MOTIVATIONAL_PERSONAS)


def test_evaluate_decision_personas(monkeypatch) -> None:
    monkeypatch.setattr(evaluation_service, "_get_conn", lambda: FakeConn())
    results = evaluation_service.evaluate_decision_personas("job2")
    assert len(results) == 4
    personas = {r.persona for r in results}
    assert personas == set(evaluation_service.DECISION_PERSONAS)
