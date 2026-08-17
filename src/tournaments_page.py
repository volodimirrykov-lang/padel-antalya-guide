#!/usr/bin/env python3
"""Автостраница «Турниры этой недели» — генерится из живого фида racket.id.

Задача 260817-1007-c585a6 (Володимир 17.08: «мне нужен трафик; только то, что
автоматом, иначе 100% протухнет»).

Почему это работает на трафик: единственный в Анталье источник живого турнирного
расписания. Google поднимает частоту обхода страниц, которые реально меняются;
LLM цитируют конкретику («ranked по воскресеньям в 18:00»). Ручного текста нет —
всё из data/tournaments/snapshot.json (racket.id, крон */5 мин, канон SOT-22).

Против протухания:
  * страница пересобирается кроном 3 раза в день и при каждом weekly refresh;
  * на странице явный штамп «по состоянию на»;
  * числа свободных мест НЕ печатаются (протухают за часы — урок сториз 11.08);
    вместо них статус: «набор открыт» / «мест нет» — живёт сутки нормально;
  * если снапшот старше 6 часов — страница НЕ перезаписывается (лучше вчерашняя
    честная, чем свежая из битого фида).

Запуск: python3 tournaments_page.py            # собрать в docs/
        python3 tournaments_page.py --check    # только напечатать, не писать
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build import CSS, esc  # тот же стиль, что у всего сайта

BASE = "https://padelantalya.org"
DOCS = Path(__file__).parent.parent / "docs"
SNAP = Path.home() / "projects" / "v7padel-site" / "data" / "tournaments" / "snapshot.json"
CLUBS = json.load(open(Path(__file__).parent / "clubs_data.json"))
CLUBS = CLUBS.get("clubs") or CLUBS
V7 = next(c for c in (CLUBS if isinstance(CLUBS, list) else CLUBS.values()) if c.get("primary"))
WA_PHONE = V7.get("phone", "").replace(" ", "").replace("+", "")
ANTALYA = dt.timezone(dt.timedelta(hours=3))
MAX_SNAPSHOT_AGE_H = 6
SLUG = "tournaments-antalya-this-week"

L10N = {
    "en": {"path": "", "title": "Padel tournaments in Antalya this week — live schedule",
           "desc": "Live schedule of padel tournaments, americanos and ranked games in Antalya this week at V7 Padel (Konyaaltı): days, times and registration status.",
           "h1": "Padel tournaments in Antalya — this week",
           "intro": "Live list of padel tournaments, americanos and ranked games in Antalya for the next 7 days, held at V7 Padel in Konyaaltı. Updated several times a day straight from the registration system.",
           "open": "registration open", "full": "full — waitlist via WhatsApp",
           "cta": "Ask about a tournament on WhatsApp",
           "wa_text": "Hi! I'm interested in a padel tournament in Antalya this week",
           "asof": "As of", "none": "No events scheduled for the next 7 days — new tournaments are announced weekly.",
           "how": "How to join", "how_text": "Spots are limited (8-12 players). Message the club on WhatsApp — staff speak English, Turkish, Russian and Ukrainian — or register in the racket.id app.",
           "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
    "tr": {"path": "tr/", "title": "Antalya padel turnuvaları bu hafta — canlı program",
           "desc": "Antalya'da bu haftaki padel turnuvaları, americano ve ranked oyunların canlı programı — V7 Padel Konyaaltı: günler, saatler ve kayıt durumu.",
           "h1": "Antalya padel turnuvaları — bu hafta",
           "intro": "Önümüzdeki 7 günde Antalya'daki padel turnuvaları, americano ve ranked oyunların canlı listesi (V7 Padel, Konyaaltı). Kayıt sisteminden günde birkaç kez güncellenir.",
           "open": "kayıt açık", "full": "dolu — WhatsApp'tan yedek liste",
           "cta": "WhatsApp'tan turnuva sorun",
           "wa_text": "Merhaba! Bu hafta Antalya'daki padel turnuvasıyla ilgileniyorum",
           "asof": "Güncelleme", "none": "Önümüzdeki 7 gün için planlanmış etkinlik yok — yeni turnuvalar her hafta duyurulur.",
           "how": "Nasıl katılırım", "how_text": "Kontenjan sınırlı (8-12 oyuncu). Kulübe WhatsApp'tan yazın — ekip Türkçe, İngilizce, Rusça ve Ukraynaca konuşuyor — veya racket.id uygulamasından kayıt olun.",
           "days": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]},
    "ru": {"path": "ru/", "title": "Турниры по паделу в Анталье на этой неделе — живое расписание",
           "desc": "Живое расписание падел-турниров, американо и ranked-игр в Анталье на эту неделю — V7 Padel (Коньяалты): дни, время и статус записи.",
           "h1": "Турниры по паделу в Анталье — эта неделя",
           "intro": "Живой список турниров, американо и ranked-игр по паделу в Анталье на ближайшие 7 дней (V7 Padel, Коньяалты). Обновляется несколько раз в день прямо из системы регистрации.",
           "open": "запись открыта", "full": "мест нет — лист ожидания в WhatsApp",
           "cta": "Спросить про турнир в WhatsApp",
           "wa_text": "Здравствуйте! Интересует падел-турнир в Анталье на этой неделе",
           "asof": "Данные на", "none": "На ближайшие 7 дней событий не запланировано — новые турниры анонсируются еженедельно.",
           "how": "Как участвовать", "how_text": "Мест немного (8-12 игроков). Напишите клубу в WhatsApp — персонал говорит по-русски, по-английски и по-турецки — или зарегистрируйтесь в приложении racket.id.",
           "days": ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]},
    "uk": {"path": "uk/", "title": "Турніри з паделу в Анталії цього тижня — живий розклад",
           "desc": "Живий розклад падел-турнірів, американо та ranked-ігор в Анталії цього тижня — V7 Padel (Коньяалти): дні, час і статус запису.",
           "h1": "Турніри з паделу в Анталії — цей тиждень",
           "intro": "Живий список турнірів, американо та ranked-ігор з паделу в Анталії на найближчі 7 днів (V7 Padel, Коньяалти). Оновлюється кілька разів на день прямо з системи реєстрації.",
           "open": "запис відкрито", "full": "місць немає — лист очікування у WhatsApp",
           "cta": "Запитати про турнір у WhatsApp",
           "wa_text": "Вітаю! Цікавить падел-турнір в Анталії цього тижня",
           "asof": "Дані станом на", "none": "На найближчі 7 днів подій не заплановано — нові турніри анонсуються щотижня.",
           "how": "Як взяти участь", "how_text": "Місць небагато (8-12 гравців). Напишіть клубу у WhatsApp — персонал говорить українською, англійською та турецькою — або зареєструйтесь у застосунку racket.id.",
           "days": ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]},
}


def load_events():
    d = json.loads(SNAP.read_text())
    gen = dt.datetime.fromisoformat(d["generated_at"].replace("Z", "+00:00"))
    age_h = (dt.datetime.now(dt.timezone.utc) - gen).total_seconds() / 3600
    today = dt.datetime.now(ANTALYA).date()
    events = []
    for t in d["tournaments"]:
        try:
            start = dt.datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            continue
        if not (today <= start.date() <= today + dt.timedelta(days=7)):
            continue
        slots = int(t.get("slots") or 0)
        taken = len(t.get("participants") or [])
        events.append({"title": t["title"].strip(), "start": start,
                       "end": (t.get("end_time") or "")[:5],
                       "full": slots > 0 and taken >= slots})
    events.sort(key=lambda e: e["start"])
    return events, gen, age_h


def event_schema(events):
    nodes = []
    for e in events:
        nodes.append({
            "@type": "SportsEvent", "name": e["title"],
            "startDate": e["start"].strftime("%Y-%m-%dT%H:%M:00+03:00"),
            "sport": "Padel",
            "eventStatus": "https://schema.org/EventScheduled",
            "location": {"@type": "SportsActivityLocation", "name": V7["name"],
                         "address": V7.get("address", "Konyaaltı, Antalya, Turkey")}})
    return {"@context": "https://schema.org", "@graph": nodes}


def render(lang, events, gen):
    t = L10N[lang]
    now = dt.datetime.now(ANTALYA)
    url = f"{BASE}/{t['path']}{SLUG}/"
    hreflang = "".join(
        f'<link rel="alternate" hreflang="{L}" href="{BASE}/{v["path"]}{SLUG}/">'
        for L, v in L10N.items()) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/{SLUG}/">'
    wa = f"https://wa.me/{WA_PHONE}?text={urllib.parse.quote(t['wa_text'] + ' [HUB-TURNUVA]')}"
    rows = ""
    day = None
    for e in events:
        dlabel = f"{t['days'][e['start'].weekday()]} {e['start'].strftime('%d.%m')}"
        if dlabel != day:
            rows += f'<h2 style="margin:26px 0 6px">{esc(dlabel)}</h2>'
            day = dlabel
        status = t["full"] if e["full"] else t["open"]
        badge = ("background:#fde8e8;color:#8a1f1f" if e["full"]
                 else "background:#e7f6ef;color:#116149")
        rows += (f'<div class="card" style="display:flex;justify-content:space-between;'
                 f'gap:12px;align-items:center;flex-wrap:wrap">'
                 f'<div><strong>{esc(e["title"])}</strong><br>'
                 f'<span style="color:#555">{e["start"].strftime("%H:%M")}'
                 + (f'–{esc(e["end"])}' if e["end"] else "") + "</span></div>"
                 f'<span style="{badge};padding:5px 12px;border-radius:14px;'
                 f'font-size:13px;font-weight:700">{esc(status)}</span></div>')
    if not events:
        rows = f'<p>{esc(t["none"])}</p>'
    schema = json.dumps(event_schema(events), ensure_ascii=False)
    lang_switch = " · ".join(f'<a href="{BASE}/{v["path"]}{SLUG}/">{L.upper()}</a>'
                             for L, v in L10N.items() if L != lang)
    return url, f"""<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="{url}">{hreflang}
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style></head><body>
<main style="max-width:760px;margin:0 auto;padding:24px 18px">
<p style="font-size:13px"><a href="{BASE}/{t['path'] or ''}">← padelantalya.org</a> · {lang_switch}</p>
<h1>{esc(t['h1'])}</h1>
<p style="color:#555;font-size:14px">{t['asof']}: {now.strftime('%d.%m.%Y %H:%M')} (UTC+3)</p>
<p>{esc(t['intro'])}</p>
{rows}
<h2 style="margin-top:30px">{esc(t['how'])}</h2>
<p>{esc(t['how_text'])}</p>
<p style="margin:4px 0 14px"><a href="{wa}" rel="nofollow" style="display:inline-block;background:#0aBaB5;color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:700">{esc(t['cta'])}</a></p>
</main></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    events, gen, age_h = load_events()
    if age_h > MAX_SNAPSHOT_AGE_H:
        print(f"[tournaments] снапшот старше {MAX_SNAPSHOT_AGE_H}ч ({age_h:.1f}ч) — "
              "страницу НЕ перезаписываю, остаётся прошлая версия")
        return 0
    print(f"[tournaments] событий в ближайшие 7 дней: {len(events)} "
          f"(снапшот {age_h*60:.0f} мин назад)")
    for lang in L10N:
        url, html = render(lang, events, gen)
        if a.check:
            print("  [check]", url)
            continue
        out = DOCS / L10N[lang]["path"] / SLUG / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        print("  built", url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
