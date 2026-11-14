#!/bin/bash
# Stop hook: la finalul fiecărui răspuns al lui Claude, dacă există modificări,
# regenerează index.html (când s-a schimbat sursa), face commit și push pe origin/develop.
BRANCH="develop"
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -z "$(git status --porcelain)" ] && exit 0

# Urcăm automat doar de pe develop; pe alt branch nu atingem nimic.
current=$(git branch --show-current)
if [ "$current" != "$BRANCH" ]; then
  echo "{\"systemMessage\":\"Modificări necomise pe '$current'. Urcarea automată funcționează doar pe '$BRANCH'.\"}"
  exit 0
fi

# Dacă s-a modificat sursa, ne asigurăm că index.html e regenerat.
if git status --porcelain | grep -qE 'src/template\.html|build\.py|docs/'; then
  python3 -I build.py >/dev/null 2>&1
fi

git add -A
files=$(git diff --cached --name-only | head -5 | tr '\n' ' ')
git commit -q -m "Actualizare automată: ${files% }" \
  -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" >/dev/null 2>&1 || exit 0

if git push -q -u origin "$BRANCH" >/dev/null 2>&1; then
  echo "{\"systemMessage\":\"Modificările au fost urcate automat pe GitHub (branch $BRANCH).\"}"
else
  echo "{\"systemMessage\":\"Commit creat local, dar push-ul pe $BRANCH a eșuat. Rulează: git push origin $BRANCH\"}"
fi
exit 0
