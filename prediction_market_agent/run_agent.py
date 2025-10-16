"""
Entrypoint for running the agent in GKE.
Can also be executed locally by running
`python prediction_market_agent/run_agent.py <agent> <market_type>`.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import nest_asyncio
import typer
from prediction_market_agent_tooling.loggers import patch_logger

from prediction_market_agent.utils import patch_polymarket_clob_side_enum

# Apply CLOB side enum fix before any agents import Polymarket modules
patch_polymarket_clob_side_enum()

from prediction_market_agent.agents.registry import RUNNABLE_AGENTS, RunnableAgent

if TYPE_CHECKING:
    from prediction_market_agent_tooling.markets.market_type import MarketType as _MarketType

APP = typer.Typer(pretty_exceptions_enable=False)


def _parse_market_type(raw_market_type: str) -> "_MarketType":
    from prediction_market_agent_tooling.markets.market_type import MarketType

    value = raw_market_type.strip()
    try:
        return MarketType(value)
    except ValueError:
        try:
            return MarketType[value.upper()]
        except KeyError as exc:
            raise typer.BadParameter(
                f"Unsupported market type '{raw_market_type}'."
            ) from exc


@APP.command()
def main(
    agent: RunnableAgent,
    market_type: str,
) -> None:
    resolved_market_type = _parse_market_type(market_type)
    nest_asyncio.apply()  # See https://github.com/pydantic/pydantic-ai/issues/889, we had issue with Think Thoroughly that is using multiprocessing heavily.
    patch_logger(force_patch=True)
    if resolved_market_type != _parse_market_type("polymarket"):
        raise ValueError("Only MarketType.POLYMARKET is supported in this configuration.")
    RUNNABLE_AGENTS[agent]().run(market_type=resolved_market_type)


if __name__ == "__main__":
    APP()
