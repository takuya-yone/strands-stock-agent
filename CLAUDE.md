# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python >=3.14, managed with `uv`. There is no test suite.

- `uv sync` — install dependencies
- `uv run python -m strands_stock_agent.main` — run the demo entrypoint (`src/strands_stock_agent/main.py`; it sets `BYPASS_TOOL_CONSENT=true`, runs `exchange_exec_agent`, then passes its result to `exchange_report_agent`. Switch which agents run by editing the commented calls there)
- `scripts/lint.sh [--fix]` / `scripts/format.sh` / `scripts/check.sh` — ruff lint / format / non-mutating check for CI (wrappers around `uv run ruff ...`; ruff is the only dev tool, line length 120, import sorting enabled)
- `scripts/data-cleanup.sh [--yes]` — **destructive**: deletes every record in `FxBalanceHistoryTable` and `FxOrderHistoryTable` and empties the S3 bucket `fx-order-summary-bucket` (needs aws cli v2 and jq). `FxBalanceTable` is not touched

Running agents needs AWS credentials with Bedrock access in `ap-northeast-1`. The exchange tools also need these DynamoDB tables (models in `db/balance_db.py`):

| Table | Model | Keys |
| --- | --- | --- |
| `FxBalanceTable` | `UserBalanceModel` | hash `ActorId` |
| `FxBalanceHistoryTable` | `UserBalanceHistoryModel` | hash `ActorId`, range `Timestamp` |
| `FxOrderHistoryTable` | `OrderHistoryModel` | hash `TransactionId`; GSI `actor-id-index` (`ActorId` / `Timestamp`) |

## Architecture

A [Strands Agents](https://strandsagents.com) app with five module-level `Agent` singletons in `agents/`, re-exported from `agents/__init__.py`. They are instantiated at import time and called like functions (`search_agent("...")`).

- `search_agent` — stock/market info via yfinance tools. Its system prompt tells it to write a Markdown report with `file_write`, but `file_write` is **not** in its tool list.
- `report_agent` — takes text and writes a Markdown report to `reports/` using `strands_tools.file_write`.
- `exchange_exec_agent` — FX rates, balance lookup, order history, and placing orders. Tools: `get_exchange_info`, `get_fx_balance`, `order`, `generate_transaction_id`, `get_order_histories`. Its system prompt hardcodes `ActorId is 'test_user'` and requires a transaction ID for every order, JPY on one side of every trade, and a single execution per request.
- `exchange_report_agent` — takes the exec agent's output, writes `reports/<transaction_id>.md` with `file_write`, then stores the summary on the order record via `put_exchange_report_to_dynamodb`.

Layering for the exchange flow: `agents/` → `tools/` (`@tool`-decorated functions; the docstring `Args:` sections are the schema the LLM sees) → `services/` (business logic) → `db/` (PynamoDB models). `schemas.py` holds all enums and pydantic models, including `StrandsLlmModelEnum`, which wraps pre-built `BedrockModel` instances; agents select models through it (all agents currently use `KIMI_K3_GLOBAL` except `report_agent`, which uses `NOVA_2_LITE_GLOBAL`).

`tools/__init__.py` uses `import *` from each tools module, so a new tool is exposed to agents once it is defined there. It must also be added to the agent's tools list.

## Gotchas

- The directory is spelled `services` (typo). Imports must use that spelling.
- The user identifier is `actor_id` / `ActorId` everywhere (tool args, pydantic models, DynamoDB keys). Some docstrings still say "user ID".
- `exec_order` in `services/exchange_service.py`: `buy_quantity` is in the buy currency and is converted to the sell currency via JPY (`_convert_quantity`). It raises `ValueError` if neither side is JPY or if any balance would go negative. On success it writes the balance, a `UserBalanceHistoryModel` snapshot, and an `OrderHistoryModel` record (ticker `"<sell>/<buy>"`, price = JPY rate of the buy currency). Balances are integers end to end: the converted sell amount is rounded up (`math.ceil` after `round(..., 6)`), `FxBalance` fields are `int`, and `_save_balance` / `_save_user_balance_history` cast to `int`. Legacy fractional values in DynamoDB are truncated on read via `to_fx_balance`.
- `get_order_histories` returns at most the 10 most recent orders for an actor (GSI query, newest first).
- `exchange_report_tools.py` also defines `put_exchange_report_to_s3` (bucket `fx-order-summary-bucket`), but no agent has it in its tools list.
- `_get_jpy_rate`, `_get_last_price` and `_calc_jpy_value` call yfinance on every order (several times per order).
- `exchange_exec_agent` has its `callback_handler=None` line commented out (streaming output is on); the other agents silence it.
- Logging uses AWS Lambda Powertools `Logger` (`logger.py`). Agent prompts and responses are in Japanese.
