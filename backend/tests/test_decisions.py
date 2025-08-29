from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.services import decisions as decisions_service
from backend.app.models.decision import Decision



class FakeCursor:
    def __init__(self, judge_row, other_rows):
        self.judge_row = judge_row
        self.other_rows = other_rows
        self.calls = []
        self.last_query = ""

    def execute(self, query: str, params: tuple | list | None = None) -> None:
        self.calls.append((query, params))
        self.last_query = query

    def fetchone(self):
        if "persona = %s" in self.last_query:
            return self.judge_row
        return None

    def fetchall(self):
        if "persona IN" in self.last_query:
            return self.other_rows
        return []

    def close(self) -> None:
        pass


class FakeConn:
    def __init__(self, judge_row, other_rows):
        self.cursor_obj = FakeCursor(judge_row, other_rows)

    def cursor(self):
        return self.cursor_obj

    def commit(self) -> None:
        pass

    def close(self) -> None:
        pass


def test_aggregate_decision(monkeypatch) -> None:
    judge_row = (True, "judge yes")
    other_rows = [(True,), (False,), (True,)]
    fake = FakeConn(judge_row, other_rows)
    monkeypatch.setattr(decisions_service, "_get_conn", lambda: fake)
    monkeypatch.setattr(
        decisions_service, "evaluate_decision_personas", lambda job_id: []
    )
    result = decisions_service.aggregate_decision("job1")
    assert isinstance(result, Decision)
    assert result.final_decision_bool is True
    assert abs(result.confidence - 2 / 3) < 1e-6
    insert_calls = [c for c in fake.cursor_obj.calls if "INSERT INTO decisions" in c[0]]
    assert insert_calls
    judge_calls = [c for c in fake.cursor_obj.calls if "persona = %s" in c[0]]
    assert judge_calls
