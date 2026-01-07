#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

rm -f konmari.skill
(
  cd konmari
  zip -r ../konmari.skill .
)

echo "Built konmari.skill"
