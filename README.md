# Gnosis Agent

A library for exploring the landscape of AI Agent frameworks, using the example application of a prediction market betting agent. The various agents interact with markets from [Manifold](https://manifold.markets/), [Presagio](https://presagio.pages.dev/) and [Polymarket](https://polymarket.com/).

These agents build on top of the prediction market APIs from https://github.com/gnosis/prediction-market-agent-tooling.

## Setup

Install the project dependencies with `poetry`, using Python >=3.11:

```bash
python3.11 -m pip install poetry
python3.11 -m poetry install
python3.11 -m poetry shell
```

Create a `.env` file in the root of the repo with the following variables:

```bash
MANIFOLD_API_KEY=...
BET_FROM_PRIVATE_KEY=...
OPENAI_API_KEY=...
```

Depending on the agent you want to run, you may require additional variables. See an exhaustive list in `.env.example`.

## Interactive Streamlit Apps

- An autonomous agent with function calling. Can be 'prodded' by the user to guide its strategy: `streamlit run prediction_market_agent/agents/microchain_agent/app.py` (Deployed [here](https://autonomous-trader-agent.ai.gnosisdev.com))
- Pick a prediction market question, or create your own, and pick one or more agents to perform research and make a prediction: `streamlit run scripts/agent_app.py` (Deployed [here](https://pma-agent.ai.gnosisdev.com))

## Dune Dashboard

The on-chain activity of the deployed agents from this repo can be tracked on a Dune dashboard [here](https://dune.com/gnosischain_team/omen-ai-agents).

## Running

Execute `prediction_market_agent/run_agent.py`, specifying the ID of the runnable agent and the market type:

```bash
% python prediction_market_agent/run_agent.py --help

 Usage: run_agent.py [OPTIONS] AGENT:{prophet_binary}
                     MARKET_TYPE:{polymarket}

╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    agent            AGENT:{prophet_binary}               [default: None] [required]                              │
│ *    market_type      MARKET_TYPE:{polymarket}            [default: None] [required]                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                              │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.       │
│ --help                        Show this message and exit.                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Contributing

See the [Issues](https://github.com/gnosis/prediction-market-agent/issues) for ideas of things that need fixing or implementing. 

A great self-contained first contribution would be to implement an agent using a framework in the ['Other frameworks to try'](https://github.com/gnosis/prediction-market-agent/issues/210) issue.
