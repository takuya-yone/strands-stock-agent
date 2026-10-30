#!/usr/bin/env bash
# Lint with ruff (pass --fix to auto-fix).
set -euo pipefail

cd "$(dirname "$0")/.."

uv run ruff check "$@" .
