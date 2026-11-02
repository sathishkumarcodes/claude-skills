#!/usr/bin/env bash
# Validate skills and package each as dist/<name>.zip for upload to Claude.
# Usage: scripts/package.sh [skill-name ...]   (no args = all skills)
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
mkdir -p dist

if [ "$#" -gt 0 ]; then
  names=("$@")
else
  names=()
  for d in skills/*/; do names+=("$(basename "$d")"); done
fi

fail=0
for name in "${names[@]}"; do
  dir="skills/$name"
  file="$dir/SKILL.md"
  if [ ! -f "$file" ]; then
    echo "✗ $name: $file not found"; fail=1; continue
  fi
  if [ "$(head -n1 "$file")" != "---" ]; then
    echo "✗ $name: SKILL.md must start with a --- frontmatter line"; fail=1; continue
  fi
  front="$(awk 'NR==1{next} /^---$/{exit} {print}' "$file")"
  fm_name="$(printf '%s\n' "$front" | sed -n 's/^name:[[:space:]]*//p' | head -n1 | tr -d '"'"'"'')"
  if [ "$fm_name" != "$name" ]; then
    echo "✗ $name: frontmatter name is '$fm_name' but the folder is '$name'"; fail=1; continue
  fi
  if ! printf '%s' "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
    echo "✗ $name: use lowercase letters, numbers and hyphens only"; fail=1; continue
  fi
  if ! printf '%s\n' "$front" | grep -q '^description:'; then
    echo "✗ $name: frontmatter is missing a description"; fail=1; continue
  fi

  rm -f "dist/$name.zip"
  # Only the skill files go in the ZIP; the folder's README is for people.
  (cd skills && zip -qr "../dist/$name.zip" "$name" -x "$name/README.md")
  echo "✓ $name → dist/$name.zip"
done

exit "$fail"
