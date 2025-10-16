import typing as t

from prediction_market_agent_tooling.deploy.agent import DeployableTraderAgent
from prediction_market_agent_tooling.deploy.betting_strategy import (
    BettingStrategy,
    FullBinaryKellyBettingStrategy,
    FullCategoricalKellyBettingStrategy,
)
from prediction_market_agent_tooling.gtypes import USD
from prediction_market_agent_tooling.loggers import logger
from prediction_market_agent_tooling.markets.agent_market import AgentMarket
from prediction_market_agent_tooling.markets.data_models import (
    CategoricalProbabilisticAnswer,
    ProbabilisticAnswer,
)
from prediction_market_agent_tooling.markets.markets import MarketType
from prediction_market_agent_tooling.markets.omen.omen import OmenAgentMarket
from prediction_market_agent_tooling.tools.openai_utils import get_openai_provider
from prediction_prophet.benchmark.agents import (
    EmbeddingModel,
    OlasAgent,
    PredictionProphetAgent,
)
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.settings import ModelSettings

from prediction_market_agent.agents.utils import get_maximum_possible_bet_amount
from prediction_market_agent.utils import DEFAULT_OPENAI_MODEL, APIKeys


class DeployableTraderAgentER(DeployableTraderAgent):
    """Base class for PredictionProphet agents operating on binary markets."""

    agent: PredictionProphetAgent | OlasAgent
    bet_on_n_markets_per_run = 2

    def answer_binary_market(self, market: AgentMarket) -> ProbabilisticAnswer | None:
        prediction = self.agent.predict(market.question)
        logger.info(
            f"Answering '{market.question}' with '{prediction.outcome_prediction}'."
        )
        outcome_prediction = prediction.outcome_prediction
        return (
            outcome_prediction.to_probabilistic_answer()
            if outcome_prediction is not None
            else None
        )


class DeployableTraderAgentERCategorical(DeployableTraderAgent):
    """Base class for PredictionProphet agents operating on categorical markets."""

    agent: PredictionProphetAgent
    bet_on_n_markets_per_run = 2

    def answer_categorical_market(
        self, market: AgentMarket
    ) -> CategoricalProbabilisticAnswer | None:
        prediction = self.agent.predict_categorical(market.question, market.outcomes)
        logger.info(
            f"Answering '{market.question}' with '{prediction.outcome_prediction}'."
        )
        return prediction.outcome_prediction


class _BaseGPT5ProphetAgent(DeployableTraderAgentER):
    """Common loader for GPT-5 binary PredictionProphet agents."""

    model_name: str = DEFAULT_OPENAI_MODEL

    def load(self) -> None:
        super().load()
        api_keys = APIKeys()
        self.agent = PredictionProphetAgent(
            research_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
                model_settings=ModelSettings(temperature=0.7),
            ),
            prediction_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
                model_settings=ModelSettings(temperature=0.0),
            ),
            include_reasoning=True,
            logger=logger,
        )


class _BaseGPT5ProphetCategoricalAgent(DeployableTraderAgentERCategorical):
    """Common loader for GPT-5 categorical PredictionProphet agents."""

    model_name: str = DEFAULT_OPENAI_MODEL

    def load(self) -> None:
        super().load()
        api_keys = APIKeys()
        self.agent = PredictionProphetAgent(
            research_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
                model_settings=ModelSettings(temperature=0.7),
            ),
            prediction_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
                model_settings=ModelSettings(temperature=0.0),
            ),
            include_reasoning=True,
            logger=logger,
        )


class DeployableProphetBinary(_BaseGPT5ProphetAgent):
    """Unified binary PredictionProphet agent (GPT-5)."""

    def get_betting_strategy(self, market: AgentMarket) -> BettingStrategy:
        return (
            FullBinaryKellyBettingStrategy(
                max_position_amount=get_maximum_possible_bet_amount(
                    min_=USD(1),
                    max_=USD(5),
                    trading_balance=market.get_trade_balance(APIKeys()),
                ),
                max_price_impact=0.7,
            )
            if isinstance(market, OmenAgentMarket)
            else super().get_betting_strategy(market)
        )

    def get_markets(
        self,
        market_type: MarketType,
    ) -> t.Sequence[AgentMarket]:
        markets = super().get_markets(market_type)
        return [m for m in markets if getattr(m, "is_binary", False)]


class DeployableProphetCategorical(_BaseGPT5ProphetCategoricalAgent):
    """Unified categorical PredictionProphet agent (GPT-5)."""

    def get_betting_strategy(self, market: AgentMarket) -> BettingStrategy:
        return (
            FullCategoricalKellyBettingStrategy(
                max_position_amount=get_maximum_possible_bet_amount(
                    min_=USD(0.01),
                    max_=USD(0.75),
                    trading_balance=market.get_trade_balance(APIKeys()),
                ),
                max_price_impact=0.068,
                allow_multiple_bets=False,
                allow_shorting=False,
                multicategorical=False,
            )
            if isinstance(market, OmenAgentMarket)
            else super().get_betting_strategy(market)
        )

    def get_markets(
        self,
        market_type: MarketType,
    ) -> t.Sequence[AgentMarket]:
        markets = super().get_markets(market_type)
        return [
            m
            for m in markets
            if not getattr(m, "is_binary", False) and not getattr(m, "is_scalar", False)
        ]


class DeployableOlasEmbeddingOAAgent(_BaseGPT5ProphetCategoricalAgent):
    """PredictionProphet agent using OLAS embeddings with GPT-5."""

    agent: OlasAgent

    def get_betting_strategy(self, market: AgentMarket) -> BettingStrategy:
        return (
            FullCategoricalKellyBettingStrategy(
                max_position_amount=get_maximum_possible_bet_amount(
                    min_=USD(0.1),
                    max_=USD(6),
                    trading_balance=market.get_trade_balance(APIKeys()),
                ),
                max_price_impact=0.7333271417580082,
                allow_multiple_bets=False,
                allow_shorting=False,
                multicategorical=False,
            )
            if isinstance(market, OmenAgentMarket)
            else super().get_betting_strategy(market)
        )

    def load(self) -> None:
        super().load()
        api_keys = APIKeys()
        self.agent = OlasAgent(
            research_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
            ),
            prediction_agent=Agent(
                OpenAIModel(
                    self.model_name,
                    provider=get_openai_provider(api_key=api_keys.openai_api_key),
                ),
            ),
            embedding_model=EmbeddingModel.openai,
            logger=logger,
        )
