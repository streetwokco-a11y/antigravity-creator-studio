#!/usr/bin/env bash
set -eo pipefail

echo -e "\033[1;34m[Step 1/3]\033[0m Testing /db-migration-guard skill manifest..."
if [ -f ".agents/skills/db-migration-guard/SKILL.md" ]; then
  echo -e "Manifest Path: \033[1;32m.agents/skills/db-migration-guard/SKILL.md\033[0m"
  echo -e "Symlink Path : \033[1;32m.agent/skills/db-migration-guard/SKILL.md\033[0m"
else
  echo -e "\033[1;31m[FAIL]\033[0m Missing db-migration-guard skill."
  exit 1
fi

echo -e "\033[1;34m[Step 2/3]\033[0m Testing /api-contract-sync skill manifest..."
if [ -f ".agents/skills/api-contract-sync/SKILL.md" ]; then
  echo -e "Manifest Path: \033[1;32m.agents/skills/api-contract-sync/SKILL.md\033[0m"
else
  echo -e "\033[1;31m[FAIL]\033[0m Missing api-contract-sync skill."
  exit 1
fi

echo -e "\033[1;34m[Step 3/3]\033[0m Testing /pr-readiness-audit skill manifest..."
if [ -f ".agents/skills/pr-readiness-audit/SKILL.md" ]; then
  echo -e "Manifest Path: \033[1;32m.agents/skills/pr-readiness-audit/SKILL.md\033[0m"
else
  echo -e "\033[1;31m[FAIL]\033[0m Missing pr-readiness-audit skill."
  exit 1
fi

echo "--------------------------------------------------------"
echo -e "\033[1;32m[SUCCESS]\033[0m All 3 Video #3 custom lead magnet skills verified & ready."
