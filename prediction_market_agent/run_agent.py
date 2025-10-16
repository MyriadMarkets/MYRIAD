"""
Entrypoint for running the agent in GKE.
Can also be executed locally by running
`python prediction_market_agent/run_agent.py <agent> <market_type>`.
"""
import nest_asyncio
import typer
from prediction_market_agent_tooling.loggers import patch_logger
from prediction_market_agent_tooling.markets.markets import MarketType

from prediction_market_agent.utils import patch_polymarket_clob_side_enum

# Apply CLOB side enum fix before any agents import Polymarket modules
patch_polymarket_clob_side_enum()

from prediction_market_agent.agents.registry import RUNNABLE_AGENTS, RunnableAgent

APP = typer.Typer(pretty_exceptions_enable=False)


@APP.command()
def main(
    agent: RunnableAgent,
    market_type: MarketType,
) -> None:
    nest_asyncio.apply()  # See https://github.com/pydantic/pydantic-ai/issues/889, we had issue with Think Thoroughly that is using multiprocessing heavily.
    patch_logger(force_patch=True)
    if market_type != MarketType.POLYMARKET:
        raise ValueError("Only MarketType.POLYMARKET is supported in this configuration.")
    RUNNABLE_AGENTS[agent]().run(market_type=market_type)


if __name__ == "__main__":
    APP()
