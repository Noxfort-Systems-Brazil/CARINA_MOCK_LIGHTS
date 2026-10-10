#!/usr/bin/env bash
# ==============================================================================
# CARINA MOCK LIGHTS - Automated Sync and Push Script
# Usage:
#   ./sync.sh "commit message"
#   ./sync.sh                     (uses automatic message with date/time)
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
COMMIT_MSG="$1"

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="chore: update CARINA MOCK LIGHTS modules ($(date '+%Y-%m-%d %H:%M:%S'))"
fi

echo -e "${BLUE}=== [CARINA MOCK LIGHTS] Sincronizando com GitHub ===${NC}"
echo -e "${BLUE}Branch atual:${NC} ${BRANCH}"

echo -e "${BLUE}1/3 Adicionando arquivos...${NC}"
git add -A

if git diff --cached --quiet; then
    echo -e "${YELLOW}Nenhuma alteração nova para comitar.${NC}"
else
    echo -e "${BLUE}2/3 Comitando: \"${COMMIT_MSG}\"...${NC}"
    git commit -m "$COMMIT_MSG"
fi

if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${BLUE}3/3 Enviando para o GitHub (origin ${BRANCH})...${NC}"
    git push origin "$BRANCH"
    echo -e "${GREEN}✔ CARINA MOCK LIGHTS atualizada com sucesso no GitHub!${NC}"
else
    echo -e "${YELLOW}Aviso: Repositório remoto 'origin' não configurado. Commit local salvo.${NC}"
fi
