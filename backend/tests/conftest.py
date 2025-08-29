import sys
import types

# Minimal numpy stub so tests avoid heavy dependency
numpy_stub = types.ModuleType("numpy")
numpy_stub.array = lambda seq: list(seq)
numpy_stub.dot = lambda a, b: sum(x * y for x, y in zip(a, b))
numpy_stub.ndarray = list  # type: ignore[attr-defined]
sys.modules.setdefault("numpy", numpy_stub)

# Minimal CrewAI stubs for deterministic tests
class _DummyBaseLLM:
    def __init__(self, model: str) -> None:  # pragma: no cover - trivial
        self.model = model

    def call(self, *args, **kwargs) -> str:  # pragma: no cover - deterministic
        return "Vote: Yes\nRationale: stub"

class _DummyAgent:  # pragma: no cover - behaviour not tested
    def __init__(self, *args, **kwargs) -> None:
        pass

class _DummyTask:  # pragma: no cover - behaviour not tested
    def __init__(self, *args, **kwargs) -> None:
        pass

class _DummyProcess:  # pragma: no cover - behaviour not tested
    sequential = "sequential"

class _DummyCrew:
    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover
        pass

    def kickoff(self):  # pragma: no cover - deterministic
        output = types.SimpleNamespace(raw="Vote: Yes\nRationale: stub")
        return types.SimpleNamespace(tasks_output=[output])

crewai = types.ModuleType("crewai")
crewai.Agent = _DummyAgent
crewai.Crew = _DummyCrew
crewai.Process = _DummyProcess
crewai.Task = _DummyTask

llm_mod = types.ModuleType("crewai.llms.base_llm")
llm_mod.BaseLLM = _DummyBaseLLM

sys.modules.setdefault("crewai", crewai)
sys.modules.setdefault("crewai.llms", types.ModuleType("crewai.llms"))
sys.modules.setdefault("crewai.llms.base_llm", llm_mod)
