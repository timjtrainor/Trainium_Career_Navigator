from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.services.evaluation import _parse_output


def test_parse_output_valid() -> None:
    vote, rationale = _parse_output("Vote: Yes\nRationale: strong match")
    assert vote is True
    assert rationale == "strong match"


@pytest.mark.parametrize(
    "raw",
    [
        "Approval: Yes\nRationale: good",
        "Vote: Maybe\nRationale: unsure",
        "Random text",
    ],
)
def test_parse_output_invalid(raw: str) -> None:
    with pytest.raises(ValueError):
        _parse_output(raw)


def test_parse_output_missing_rationale() -> None:
    vote, rationale = _parse_output("Vote: No")
    assert vote is False
    assert rationale == ""
