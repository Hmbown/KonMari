#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
default_dest_dir="${HOME}/.claude/skills"

if [[ -n "${CODEX_HOME:-}" ]]; then
  default_dest_dir="${CODEX_HOME%/}/skills"
fi

dest_arg="${1:-$default_dest_dir}"

if [[ "$dest_arg" == *.skill ]]; then
  dest_dir="$(dirname "$dest_arg")"
  dest_file="$dest_arg"
else
  dest_dir="$dest_arg"
  dest_file="${dest_dir}/konmari.skill"
fi

mkdir -p "$dest_dir"

"$root_dir/scripts/build_skill.sh"

cp "$root_dir/konmari.skill" "$dest_file"

echo "Installed konmari.skill to $dest_file"
