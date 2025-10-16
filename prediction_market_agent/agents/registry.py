from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from importlib import import_module
from typing import Iterable, Type

from prediction_market_agent_tooling.deploy.agent import DeployableAgent


@dataclass(frozen=True)
class AgentDefinition:
    name: str
    import_path: str

    @property
    def agent_cls(self) -> Type[DeployableAgent]:
        return _load_agent_class(self.import_path)


@lru_cache(maxsize=None)
def _load_agent_class(import_path: str) -> Type[DeployableAgent]:
    module_name, class_name = import_path.rsplit(".", 1)
    module = import_module(module_name)
    agent_cls = getattr(module, class_name)
    if not issubclass(agent_cls, DeployableAgent):
        raise TypeError(
            f"{import_path} does not resolve to a DeployableAgent subclass."
        )
    return agent_cls


def _iter_agent_definitions() -> Iterable[AgentDefinition]:
    yield AgentDefinition(
        "prophet_binary",
        "prediction_market_agent.agents.prophet_agent.deploy.DeployableProphetBinary",
    )


AGENT_DEFINITIONS: tuple[AgentDefinition, ...] = tuple(_iter_agent_definitions())

RunnableAgent = Enum(  # type: ignore[misc]
    "RunnableAgent",
    {definition.name: definition.name for definition in AGENT_DEFINITIONS},
    type=str,
)

RUNNABLE_AGENTS: dict[RunnableAgent, Type[DeployableAgent]] = {
    RunnableAgent[definition.name]: definition.agent_cls
    for definition in AGENT_DEFINITIONS
}

__all__ = ["AgentDefinition", "AGENT_DEFINITIONS", "RunnableAgent", "RUNNABLE_AGENTS"]
