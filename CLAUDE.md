# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python >=3.14, managed with `uv`. There is no test suite.

- `uv sync` — install dependencies
- `uv run python -m strands_stock_agent.main` — run the demo entrypoint (`src/strands_stock_agent/main.py`; it sets `BYPASS_TOOL_CONSENT=true` and invokes an agent directly. Switch which agent runs by editing the commented calls there)
- `uv run ruff check .` / `uv run ruff format .` — lint / format (ruff is the only dev tool)

Running agents needs AWS credentials with Bedrock access in `ap-northeast-1`. The exchange tools also need DynamoDB tables `fx-balance-table` and `order-record-table` (see `db/balance_db.py`).

## Architecture

A [Strands Agents](https://strandsagents.com) app with three module-level `Agent` singletons in `agents/`, re-exported from `agents/__init__.py`. They are instantiated at import time and called like functions (`search_agent("...")`).

- `search_agent` — stock/market info via yfinance tools. Its system prompt tells it to write a Markdown report with `file_write`, but `file_write` is **not** in its tool list.
- `exchange_exec_agent` — FX rates, balance lookup, and placing orders. Its system prompt hardcodes `UserId is 'test_user'`.
- `report_agent` — takes text and writes a Markdown report to `reports/` using `strands_tools.file_write`.

Layering for the exchange flow: `agents/` → `tools/` (`@tool`-decorated functions; the docstring `Args:` sections are the schema the LLM sees) → `serrvices/` (business logic) → `db/` (PynamoDB models). `schemas.py` holds all enums and pydantic models, including `StrandsLlmModelEnum`, which wraps pre-built `BedrockModel` instances; agents select models through it.

`tools/__init__.py` uses `import *` from each tools module, so a new tool is exposed to agents once it is defined there. It must also be added to the agent's tools list.

## Gotchas

- The directory is spelled `serrvices` (typo). Imports must use that spelling.
- `exec_order` in `serrvices/exchange_service.py` adds and subtracts the same `quantity` of both currencies, with no rate conversion and no balance check. It also never writes to `OrderRecordModel`.
- `get_last_price` and `calc_jpy_value` call yfinance on every order.
- Logging uses AWS Lambda Powertools `Logger` (`logger.py`). Agent prompts and responses are in Japanese.
