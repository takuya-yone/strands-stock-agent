#!/usr/bin/env bash
# Format all files with ruff.
set -euo pipefail

cd "$(dirname "$0")/.."

uv run ruff format .
