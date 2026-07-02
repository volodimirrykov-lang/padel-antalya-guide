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
hours = club.get("sales", {}).get("hours") or "08:00-23:00"
# формат сателлита: "08:00–23:00 daily"
if "08:00" in str(hours):
    set_field("hours", "08:00–23:00 daily")

# цена из pricing_TRY
p = club["pricing_TRY"]
price = (f"{p['court_60min']['per_court']} TL / 60 min "
         f"(≈{p['court_60min']['per_person']} TL pp for four), "
         f"{p['court_90min']['per_court']} TL / 90 min, "
         f"{p['court_120min']['per_court']} TL / 2h")
set_field("price", price)

# instagram
ig = club["contacts"].get("instagram_main", "").lstrip("@")
if ig:
    set_field("instagram", ig)

# валидация художественного описания кортов против registry
cc = club["facility"]["courts_count"]
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
