#!/usr/bin/env python3
"""Sync фактов V7 из canonical registry → clubs_data.json сателлита.

Правило SSoT: цена/телефон/часы/адрес меняются в registry — сателлит не должен врать старое.
Синкаются только машинные поля; художественные описания (courts wording EN) остаются ручными,
но валидируются против registry (courts_count). Расхождение художественного текста ≠ падение:
пишем WARN в stdout (weekly_refresh перешлёт в лог).

Запуск: перед build.py в weekly_refresh.sh
"""
import json, sys
from pathlib import Path

REG = Path("/home/user/projects/v7padel-site/data/clubs/registry.json")
CD = Path(__file__).parent / "clubs_data.json"

reg = json.load(open(REG))
club = next(c for c in reg["clubs"] if c["club_id"] == "v7-antalya-1")
data = json.load(open(CD))
v7 = next(c for c in data["clubs"] if "V7" in c["name"])

changed = []

def set_field(key, value):
    if v7.get(key) != value:
        changed.append(f"{key}: {v7.get(key)!r} -> {value!r}")
        v7[key] = value

# телефон / адрес / часы
set_field("phone", club["contacts"]["phone"])
set_field("address", club["identity"]["address"])
# 12.07: канон часов = facility.hours (Olya 07.07: 07:00-00:00), НЕ sales.hours —
# старый код с fallback "08:00" молча держал сателлит на протухших часах
# 05.09: часы берём НА ДАТУ из working_hours.periods, а не строкой facility.hours.
# Повод: владелец сменил режим на 08:00-00:00 с 07.09, строку в реестре обновили 05.09 —
# и сателлит на ближайшем прогоне опубликовал бы «с 08:00», пока клуб ещё открыт с 07:00.
# Строка facility.hours осталась запасным путём, если периодов нет.
import datetime as _dt
_fac = club.get("facility", {})
_today = _dt.date.today()
_cur = None
for _per in (_fac.get("working_hours") or {}).get("periods") or []:
    try:
        _frm = _dt.date.fromisoformat(_per["from"])
    except Exception:
        continue
    _to = _per.get("to")
    if _frm <= _today and (not _to or _today <= _dt.date.fromisoformat(_to)):
        _cur = _per
hours = (f"{_cur['open']}-{_cur['close']}" if _cur
         else (_fac.get("hours") or club.get("sales", {}).get("hours") or ""))
m = __import__("re").match(r"(\d{2}:\d{2})-(\d{2}:\d{2})", str(hours))
if m:
    set_field("hours", f"{m.group(1)}–{m.group(2)} daily")
else:
    print(f"WARN: facility.hours нераспознан ({hours!r}) — hours не синкнут", file=sys.stderr)

# цена из pricing_TRY
p = club["pricing_TRY"]
price = (f"{p['court_60min']['per_court']} TL / 60 min "
         f"(≈{p['court_60min']['per_person']} TL pp for four), "
         f"{p['court_90min']['per_court']} TL / 90 min, "
         f"{p['court_120min']['per_court']} TL / 2h")
set_field("price", price)

# структурные цены для авто-таблицы на странице цен (build.py, price-топик).
# Отдельными полями, а не строкой: таблица рендерится из чисел, при смене прайса
# в registry обновится сама следующим build'ом.
set_field("pricing", {
    "court_60": p["court_60min"]["per_court"], "court_60_pp": p["court_60min"]["per_person"],
    "court_90": p["court_90min"]["per_court"], "court_90_pp": p["court_90min"]["per_person"],
    "court_120": p["court_120min"]["per_court"], "court_120_pp": p["court_120min"]["per_person"],
})

# instagram
ig = club["contacts"].get("instagram_main", "").lstrip("@")
if ig:
    set_field("instagram", ig)

# валидация художественного описания кортов против registry
# 05.09: courts_count в реестре НЕТ — есть список courts_ids (тот же дефект, что ловил
# story_free_slots 30.08). Из-за KeyError синк падал ЦЕЛИКОМ, и сателлит переставал
# обновляться молча — данные в src/data стояли с последнего удачного прогона.
_f = club["facility"]
cc = _f.get("courts_count") or len(_f.get("courts_ids") or [])
if not cc:
    sys.exit("в реестре нет ни courts_count, ни courts_ids — не выдумываю число кортов")
if str(cc) not in v7.get("courts", ""):
    print(f"WARN: courts wording не содержит courts_count={cc} из registry — проверь руками: {v7.get('courts')}", file=sys.stderr)
# запрещённые формулировки не должны просочиться
for bad in ("climate-controlled", "air-conditioned courts", "indoor courts"):
    if bad in json.dumps(data):
        print(f"WARN: запрещённая формулировка '{bad}' в clubs_data!", file=sys.stderr)

if changed:
    json.dump(data, open(CD, "w"), ensure_ascii=False, indent=1)
    print("synced from registry:")
    for c in changed:
        print("  " + c)
else:
    print("registry sync: расхождений нет")
