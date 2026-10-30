#!/usr/bin/env bash
# Check format and lint without changing any file (for CI).
set -euo pipefail

cd "$(dirname "$0")/.."

uv run ruff format --check .
uv run ruff check .
