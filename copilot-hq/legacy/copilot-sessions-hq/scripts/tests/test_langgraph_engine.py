from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from langgraph.graph.state import CompiledStateGraph

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrator.runtime_graph.engine import LangGraphDeps, _build_tick_graph, run_tick


@dataclass
class _Agent:
    agent_id: str


class _Provider:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def run_one(self, agent_id: str) -> tuple[int, str]:
        self.calls.append(agent_id)
        return 0, f"ran {agent_id}"


def test_build_tick_graph_returns_compiled_langgraph() -> None:
    compiled = _build_tick_graph(
        [
            ("alpha", lambda state: state),
            ("omega", lambda state: state),
        ]
    )

    assert isinstance(compiled, CompiledStateGraph)


def test_run_tick_executes_langgraph_pipeline_in_order() -> None:
    provider = _Provider()
    calls: list[str] = []

    def run_cmd(cmd: list[str], *, timeout: int = 0) -> tuple[int, str]:
        calls.append(f"run_cmd:{cmd[-1]}")
        return 0, "ok"

    def dispatch_commands_step(log: list[dict]) -> None:
        calls.append("dispatch_commands")
        log.append({"step": "dispatch_commands", "rc": 0})

    def release_cycle_step(log: list[dict]) -> None:
        calls.append("release_cycle")
        log.append({"step": "release_cycle", "rc": 0})

    def coordinated_push_step(log: list[dict]) -> None:
        calls.append("coordinated_push")
        log.append({"step": "coordinated_push", "rc": 0})

    def prioritized_agents() -> list[_Agent]:
        calls.append("prioritized_agents")
        return [_Agent("ceo-copilot"), _Agent("dev-forseti"), _Agent("qa-forseti")]

    def health_check_step(_provider: _Provider, log: list[dict]) -> None:
        calls.append("health_check")
        log.append({"step": "health_check", "rc": 0})

    deps = LangGraphDeps(
        run_cmd=run_cmd,
        dispatch_commands_step=dispatch_commands_step,
        release_cycle_step=release_cycle_step,
        coordinated_push_step=coordinated_push_step,
        prioritized_agents=prioritized_agents,
        health_check_step=health_check_step,
        now_ts=lambda: 1000,
        kpi_monitor_cmd=["python3", "scripts/release-kpi-monitor.py", "--auto-remediate"],
    )

    result, kpi_last_run, release_cycle_last_run = run_tick(
        provider,
        agent_cap=2,
        publish_enabled=False,
        kpi_interval=100,
        kpi_last_run=1000,
        release_cycle_interval=100,
        release_cycle_last_run=1000,
        deps=deps,
    )

    assert result["engine_mode"] == "langgraph"
    assert result["selected_agents"] == ["ceo-copilot", "dev-forseti"]
    assert [entry["step"] for entry in result["log"]] == [
        "consume_replies",
        "dispatch_commands",
        "coordinated_push",
        "pick_agents",
        "exec_agents",
        "health_check",
        "publish",
    ]
    assert provider.calls == ["ceo-copilot", "dev-forseti"]
    assert calls == [
        "run_cmd:scripts/consume-forseti-replies.sh",
        "dispatch_commands",
        "coordinated_push",
        "prioritized_agents",
        "health_check",
    ]
    assert kpi_last_run == 1000
    assert release_cycle_last_run == 1000
