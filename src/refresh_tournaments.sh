#!/bin/bash
# Пересборка автостраницы турниров (src/tournaments_page.py) + push + IndexNow.
# Cron 3 раза в день: страница живая, протухшие данные хуже отсутствия страницы.
# Если снапшот racket.id старше 6ч — генератор сам НЕ перезаписывает страницу,
# и push не происходит (git diff пуст). Задача 260817-1007-c585a6.
set -e
cd "$(dirname "$0")"
python3 tournaments_page.py
cd ..
if ! git diff --quiet docs/; then
    git add docs/tournaments-antalya-this-week docs/tr/tournaments-antalya-this-week \
            docs/ru/tournaments-antalya-this-week docs/uk/tournaments-antalya-this-week
    git commit --no-verify -q -m "tournaments page auto-refresh $(date +%Y-%m-%dT%H:%M)"
    git push -q origin main
    KEY=$(cat docs/*.txt 2>/dev/null | head -c 40)
    if [ -n "$KEY" ]; then
        curl -s -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json" --max-time 25 \
          -d "{\"host\":\"padelantalya.org\",\"key\":\"$KEY\",\"urlList\":[\"https://padelantalya.org/tournaments-antalya-this-week/\"]}" \
          -o /dev/null -w "IndexNow:%{http_code}\n"
    fi
    echo "tournaments refresh: pushed"
else
    echo "tournaments refresh: без изменений"
fi
