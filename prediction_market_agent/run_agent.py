"""
Entrypoint for running the agent in GKE.
If the agent adheres to PMAT standard (subclasses deployable agent),
simply add the agent to the `RunnableAgent` enum and then `RUNNABLE_AGENTS` dict.

Can also be executed locally, simply by running `python prediction_market_agent/run_agent.py <agent> <market_type>`.
"""

from enum import Enum

import nest_asyncio
import typer
from prediction_market_agent_tooling.deploy.agent import DeployableAgent
from prediction_market_agent_tooling.loggers import patch_logger
from prediction_market_agent_tooling.markets.markets import MarketType

from prediction_market_agent.utils import patch_polymarket_clob_side_enum

# Apply CLOB side enum fix before any agents import Polymarket modules
patch_polymarket_clob_side_enum()

from prediction_market_agent.agents.advanced_agent.deploy import AdvancedAgent
from prediction_market_agent.agents.alert_agent.alert_on_slack import (
    PerformanceAlertAgent,
)
from prediction_market_agent.agents.arbitrage_agent.deploy import (
    DeployableArbitrageAgent,
)
from prediction_market_agent.agents.berlin1_agent.polysent_agent import (
    Berlin1PolySentAgent,
)
from prediction_market_agent.agents.berlin2_agent.openai_search_agent_high import (
    Berlin2OpenaiSearchAgentHigh,
)
from prediction_market_agent.agents.berlin2_agent.openai_search_agent_variable import (
    Berlin2OpenaiSearchAgentVariable,
)
from prediction_market_agent.agents.coinflip_agent.deploy import (
    DeployableCoinFlipAgent,
    DeployableCoinFlipAgentByHighestLiquidity,
)
from prediction_market_agent.agents.gptr_agent.deploy import (
    GPTRAgent,
    GPTRHighestLiquidityAgent,
)
from prediction_market_agent.agents.invalid_agent.deploy import InvalidAgent
from prediction_market_agent.agents.known_outcome_agent.deploy import (
    DeployableKnownOutcomeAgent,
)
from prediction_market_agent.agents.logprobs_agent.deploy import DeployableLogProbsAgent
from prediction_market_agent.agents.metaculus_agent.deploy import (
    DeployableMetaculusBotTournamentAgent,
)
from prediction_market_agent.agents.microchain_agent.deploy import (
    DeployableMicrochainAgent,
    DeployableMicrochainModifiableSystemPromptAgent0,
    DeployableMicrochainModifiableSystemPromptAgent1,
    DeployableMicrochainModifiableSystemPromptAgent2,
    DeployableMicrochainModifiableSystemPromptAgent3,
    DeployableMicrochainWithGoalManagerAgent0,
)
from prediction_market_agent.agents.microchain_agent.nft_treasury_game.deploy_nft_treasury_game import (
    DeployableAgentNFTGame1,
    DeployableAgentNFTGame2,
    DeployableAgentNFTGame3,
    DeployableAgentNFTGame4,
    DeployableAgentNFTGame5,
    DeployableAgentNFTGame6,
    DeployableAgentNFTGame7,
)
from prediction_market_agent.agents.ofvchallenger_agent.deploy import OFVChallengerAgent
from prediction_market_agent.agents.omen_cleaner_agent.deploy import OmenCleanerAgent
from prediction_market_agent.agents.prophet_agent.deploy import (
    DeployableOlasEmbeddingOAAgent,
    DeployableProphetBinary,
    DeployableProphetCategorical,
)
from prediction_market_agent.agents.replicate_to_omen_agent.deploy import (
    DeployableReplicateToOmenAgent,
)
from prediction_market_agent.agents.skew_agent.deploy import SkewAgent
from prediction_market_agent.agents.social_media_agent.deploy import (
    DeployableSocialMediaAgent,
)
from prediction_market_agent.agents.specialized_agent.deploy import (
    MarketCreatorsStalkerAgent1,
    MarketCreatorsStalkerAgent2,
)
from prediction_market_agent.agents.think_thoroughly_agent.deploy import (
    DeployableThinkThoroughlyAgent,
    DeployableThinkThoroughlyProphetResearchAgent,
)


class RunnableAgent(str, Enum):
    coinflip = "coinflip"
    coinflip_highest_liquidity = "coinflip_highest_liquidity"
    replicate_to_omen = "replicate_to_omen"
    think_thoroughly = "think_thoroughly"
    think_thoroughly_prophet = "think_thoroughly_prophet"
    knownoutcome = "knownoutcome"
    microchain = "microchain"
    microchain_modifiable_system_prompt_0 = "microchain_modifiable_system_prompt_0"
    microchain_modifiable_system_prompt_1 = "microchain_modifiable_system_prompt_1"
    microchain_modifiable_system_prompt_2 = "microchain_modifiable_system_prompt_2"
    microchain_modifiable_system_prompt_3 = "microchain_modifiable_system_prompt_3"
    microchain_with_goal_manager_agent_0 = "microchain_with_goal_manager_agent_0"
    metaculus_bot_tournament_agent = "metaculus_bot_tournament_agent"
    prophet_binary = "prophet_binary"
    prophet_categorical = "prophet_categorical"
    # prophet_scalar = "prophet_scalar"  # removed
    olas_embedding_oa = "olas_embedding_oa"
    # Social media (Farcaster + Twitter)
    social_media = "social_media"
    omen_cleaner = "omen_cleaner"
    ofv_challenger = "ofv_challenger"
    arbitrage = "arbitrage"
    market_creators_stalker1 = "market_creators_stalker1"
    market_creators_stalker2 = "market_creators_stalker2"
    invalid = "invalid"
    nft_treasury_game_agent_1 = "nft_treasury_game_agent_1"
    nft_treasury_game_agent_2 = "nft_treasury_game_agent_2"
    nft_treasury_game_agent_3 = "nft_treasury_game_agent_3"
    nft_treasury_game_agent_4 = "nft_treasury_game_agent_4"
    nft_treasury_game_agent_5 = "nft_treasury_game_agent_5"
    nft_treasury_game_agent_6 = "nft_treasury_game_agent_6"
    nft_treasury_game_agent_7 = "nft_treasury_game_agent_7"
    advanced_agent = "advanced_agent"
    gptr_agent = "gptr_agent"
    gptr_agent_highest_liquidity = "gptr_agent_highest_liquidity"
    logprobs_agent = "logprobs_agent"
    berlin1_polysent_agent = "berlin1_polysent_agent"
    berlin2_search_high = "berlin2_search_high"
    berlin2_search_var = "berlin2_search_var"
    skew_agent = "skew_agent"
    performance_alert = "performance_alert"


RUNNABLE_AGENTS: dict[RunnableAgent, type[DeployableAgent]] = {
    RunnableAgent.logprobs_agent: DeployableLogProbsAgent,
    RunnableAgent.coinflip: DeployableCoinFlipAgent,
    RunnableAgent.coinflip_highest_liquidity: DeployableCoinFlipAgentByHighestLiquidity,
    RunnableAgent.replicate_to_omen: DeployableReplicateToOmenAgent,
    RunnableAgent.think_thoroughly: DeployableThinkThoroughlyAgent,
    RunnableAgent.think_thoroughly_prophet: DeployableThinkThoroughlyProphetResearchAgent,
    RunnableAgent.knownoutcome: DeployableKnownOutcomeAgent,
    RunnableAgent.microchain: DeployableMicrochainAgent,
    RunnableAgent.microchain_modifiable_system_prompt_0: DeployableMicrochainModifiableSystemPromptAgent0,
    RunnableAgent.microchain_modifiable_system_prompt_1: DeployableMicrochainModifiableSystemPromptAgent1,
    RunnableAgent.microchain_modifiable_system_prompt_2: DeployableMicrochainModifiableSystemPromptAgent2,
    RunnableAgent.microchain_modifiable_system_prompt_3: DeployableMicrochainModifiableSystemPromptAgent3,
    RunnableAgent.microchain_with_goal_manager_agent_0: DeployableMicrochainWithGoalManagerAgent0,
    RunnableAgent.social_media: DeployableSocialMediaAgent,
    RunnableAgent.metaculus_bot_tournament_agent: DeployableMetaculusBotTournamentAgent,
    RunnableAgent.prophet_binary: DeployableProphetBinary,
    RunnableAgent.prophet_categorical: DeployableProphetCategorical,
    # RunnableAgent.prophet_scalar: DeployableProphetScalar,
    RunnableAgent.olas_embedding_oa: DeployableOlasEmbeddingOAAgent,
    RunnableAgent.omen_cleaner: OmenCleanerAgent,
    RunnableAgent.ofv_challenger: OFVChallengerAgent,
    RunnableAgent.arbitrage: DeployableArbitrageAgent,
    RunnableAgent.market_creators_stalker1: MarketCreatorsStalkerAgent1,
    RunnableAgent.market_creators_stalker2: MarketCreatorsStalkerAgent2,
    RunnableAgent.invalid: InvalidAgent,
    RunnableAgent.nft_treasury_game_agent_1: DeployableAgentNFTGame1,
    RunnableAgent.nft_treasury_game_agent_2: DeployableAgentNFTGame2,
    RunnableAgent.nft_treasury_game_agent_3: DeployableAgentNFTGame3,
    RunnableAgent.nft_treasury_game_agent_4: DeployableAgentNFTGame4,
    RunnableAgent.nft_treasury_game_agent_5: DeployableAgentNFTGame5,
    RunnableAgent.nft_treasury_game_agent_6: DeployableAgentNFTGame6,
    RunnableAgent.nft_treasury_game_agent_7: DeployableAgentNFTGame7,
    # Removed legacy prophet variants (Claude/DeepSeek/Gemini/GPT4o_*), consolidated to GPT-5
    RunnableAgent.advanced_agent: AdvancedAgent,
    RunnableAgent.gptr_agent: GPTRAgent,
    RunnableAgent.gptr_agent_highest_liquidity: GPTRHighestLiquidityAgent,
    RunnableAgent.berlin1_polysent_agent: Berlin1PolySentAgent,
    RunnableAgent.berlin2_search_high: Berlin2OpenaiSearchAgentHigh,
    RunnableAgent.berlin2_search_var: Berlin2OpenaiSearchAgentVariable,
    RunnableAgent.skew_agent: SkewAgent,
    RunnableAgent.performance_alert: PerformanceAlertAgent,
}

APP = typer.Typer(pretty_exceptions_enable=False)


@APP.command()
def main(
    agent: RunnableAgent,
    market_type: MarketType,
) -> None:
    nest_asyncio.apply()  # See https://github.com/pydantic/pydantic-ai/issues/889, we had issue with Think Thoroughly that is using multiprocessing heavily.
    patch_logger(force_patch=True)
    RUNNABLE_AGENTS[agent]().run(market_type=market_type)


if __name__ == "__main__":
    APP()
