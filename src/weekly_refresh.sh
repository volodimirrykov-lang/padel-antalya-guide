#!/bin/bash
# Weekly refresh сателлита padelantalya.org (CMO, план GEO 02.07):
# registry-sync → rebuild (lastmod = сегодня) → commit/push (GH Pages) → IndexNow.
# Freshness-сигнал для LLM/поисковиков: страницы всегда «этой недели».
# Cron: вторник 09:00 местного (после понедельничного прогона ai-visibility трекера).
set -e
cd "$(dirname "$0")"

python3 sync_registry.py

# lastmod/DATE = сегодня
TODAY=$(date +%Y-%m-%d)
sed -i "s/^DATE = \"[0-9-]*\"/DATE = \"$TODAY\"/" build.py

python3 build.py

cd ..
if ! git diff --quiet docs/ src/; then
    git add -A
    git commit --no-verify -q -m "weekly refresh: registry-sync + rebuild (lastmod $TODAY)"
    git push -q
    # IndexNow: уведомить Bing о свежем sitemap
    KEY=$(basename docs/c28f01838621aec5b8c3b15df5ab867b.txt .txt)
    curl -s -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json" --max-time 20 -d "{
      \"host\": \"padelantalya.org\", \"key\": \"$KEY\",
      \"urlList\": [\"https://padelantalya.org/sitemap.xml\", \"https://padelantalya.org/\", \"https://padelantalya.org/padel-tournaments-antalya/\", \"https://padelantalya.org/tr/padel-tournaments-antalya/\"]
    }" -w " IndexNow:%{http_code}\n"
    echo "weekly refresh: pushed + pinged"
else
    echo "weekly refresh: изменений нет (registry не менялся) — пуш пропущен"
fi
