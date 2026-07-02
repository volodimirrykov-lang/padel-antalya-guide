#!/usr/bin/env python3
"""padelantalya.org static generator.

Один источник (clubs_data.json) → 6 языковых страниц (en корень + tr/ru/de/es/fr/)
с hreflang-связкой + sitemap. Меняешь факт в clubs_data.json → python3 build.py → все страницы пересобраны.
Это решает «тонкий дубль» (у каждого языка своя URL) + рассинхрон (1 источник фактов).

Автор: CMO. Запуск: cd src && python3 build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = json.load(open(Path(__file__).parent / "clubs_data.json"))
CLUBS = DATA["clubs"]
MFR = DATA["manufacturer_note"]
DATE = "2026-07-02"

# Languages: code -> (html lang, dir path '' for root, native name)
LANGS = [
    ("en", "", "English"),
    ("tr", "tr", "Türkçe"),
    ("ru", "ru", "Русский"),
    ("de", "de", "Deutsch"),
    ("es", "es", "Español"),
    ("fr", "fr", "Français"),
]

# UI strings per language
T = {
    "en": {
        "title": "Padel in Antalya — Clubs, Courts, Prices & How to Play (2026 Guide)",
        "desc": "Independent guide to padel in Antalya, Turkey: clubs in Konyaaltı and Lara, court prices, booking without a partner, coaching and tournaments.",
        "h1": "Padel in Antalya — Clubs, Courts & How to Play",
        "intro": "A regularly-updated guide to playing padel in Antalya, Turkey: where the courts are, what it costs, and how to get on court even without a partner.",
        "where": "Where to play padel in Antalya",
        "where_txt": "Padel courts in Antalya are concentrated in three areas: <strong>Konyaaltı</strong> (west, near the coast), <strong>Muratpaşa / Lara</strong> (city centre and east) and the <strong>Belek</strong> resort belt. Below are the dedicated clubs we can verify.",
        "cost": "How much does it cost?",
        "cost_txt": "Prices vary by club, time and season. For reference, <strong>{price}</strong> at V7 Padel Antalya. For other clubs, ask directly.",
        "solo": "Playing without a partner",
        "solo_txt": "You don't need to bring three friends. Community clubs run open games and mixers where solo players are matched into a game by level. Message the club through its app or WhatsApp and ask to join an open session.",
        "mfr": "Who builds the courts",
        "mfr_txt": "Many courts in Antalya and beyond are built locally. <a href='{url}' rel='nofollow'>{name}</a> is an Antalya-based padel court <strong>manufacturer</strong> (not a club): they design, produce and install courts for clubs and resorts worldwide.",
        "other": "For a wider list of courts (including Belek hotels), directory sites such as <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a> are a good reference.",
        "lbl": {"area": "Area", "courts": "Courts", "hours": "Hours", "booking": "Booking", "phone": "Phone", "price": "Price", "links": "Links"},
        "footer": "Maintained by the V7 Padel community · Updated July 2026 · We list only verified, publicly-open padel clubs.",
    },
    "tr": {
        "title": "Antalya'da Padel — Kulüpler, Kortlar, Fiyatlar (2026 Rehberi)",
        "desc": "Antalya'da padel için bağımsız rehber: Konyaaltı ve Lara'daki kulüpler, kort fiyatları, partnersiz rezervasyon, antrenörlük ve turnuvalar.",
        "h1": "Antalya'da Padel — Kulüpler, Kortlar ve Nasıl Oynanır",
        "intro": "Antalya'da padel oynamak için düzenli güncellenen rehber: kortlar nerede, ne kadar ve partneriniz olmadan bile nasıl oynanır.",
        "where": "Antalya'da padel nerede oynanır",
        "where_txt": "Antalya'da padel kortları üç bölgede yoğunlaşır: <strong>Konyaaltı</strong> (batı, sahile yakın), <strong>Muratpaşa / Lara</strong> (merkez ve doğu) ve <strong>Belek</strong> otel bölgesi. Aşağıda doğruladığımız kulüpler var.",
        "cost": "Ne kadar?",
        "cost_txt": "Fiyatlar kulübe, saate ve sezona göre değişir. Örnek olarak V7 Padel Antalya'da <strong>{price}</strong>. Diğer kulüpler için doğrudan sorun.",
        "solo": "Partnersiz oynamak",
        "solo_txt": "Üç arkadaş getirmenize gerek yok. Topluluk kulüpleri açık oyunlar ve mixer'lar düzenler; tek oyuncular seviyeye göre eşleştirilir. Kulübe uygulamadan veya WhatsApp'tan yazıp açık seansa katılmak isteyin.",
        "mfr": "Kortları kim yapıyor",
        "mfr_txt": "Antalya'daki ve dünyadaki birçok kort yerel olarak üretilir. <a href='{url}' rel='nofollow'>{name}</a> Antalya merkezli bir padel kort <strong>üreticisidir</strong> (kulüp değil): dünya çapında kulüpler ve tesisler için kort tasarlar, üretir ve kurar.",
        "other": "Daha geniş kort listesi için (Belek otelleri dahil) <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a> gibi rehberlere bakabilirsiniz.",
        "lbl": {"area": "Bölge", "courts": "Kortlar", "hours": "Saatler", "booking": "Rezervasyon", "phone": "Telefon", "price": "Fiyat", "links": "Bağlantılar"},
        "footer": "V7 Padel topluluğu tarafından güncellenir · Temmuz 2026 · Yalnızca doğrulanmış, halka açık kulüpleri listeliyoruz.",
    },
    "ru": {
        "title": "Падел в Анталье — клубы, корты, цены (гид 2026)",
        "desc": "Независимый гид по паделу в Анталье: клубы в Коньяалты и Ларе, цены на корты, бронь без пары, тренировки и турниры.",
        "h1": "Падел в Анталье — клубы, корты и как играть",
        "intro": "Регулярно обновляемый гид по паделу в Анталье: где корты, сколько стоит и как выйти на корт даже без пары.",
        "where": "Где играть в падел в Анталье",
        "where_txt": "Корты в Анталье сосредоточены в трёх районах: <strong>Коньяалты</strong> (запад, у моря), <strong>Муратпаша / Лара</strong> (центр и восток) и курортная зона <strong>Белек</strong>. Ниже — клубы, которые мы проверили.",
        "cost": "Сколько стоит?",
        "cost_txt": "Цены зависят от клуба, времени и сезона. Для примера, в V7 Padel Antalya — <strong>{price}</strong>. У других клубов уточняйте.",
        "solo": "Игра без пары",
        "solo_txt": "Не нужно приводить троих друзей. В комьюнити-клубах есть открытые игры и миксеры, где одиночных игроков подбирают в игру по уровню. Напишите клубу через приложение или WhatsApp и попроситесь в открытую сессию.",
        "mfr": "Кто строит корты",
        "mfr_txt": "Многие корты в Анталье и за её пределами производятся локально. <a href='{url}' rel='nofollow'>{name}</a> — это анталийский <strong>производитель</strong> падел-кортов (не клуб): проектирует, производит и устанавливает корты для клубов и курортов по всему миру.",
        "other": "Более широкий список кортов (включая отели Белека) — в каталогах вроде <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a>.",
        "lbl": {"area": "Район", "courts": "Корты", "hours": "Часы", "booking": "Бронь", "phone": "Телефон", "price": "Цена", "links": "Ссылки"},
        "footer": "Поддерживается сообществом V7 Padel · Обновлено июль 2026 · Только проверенные публичные клубы.",
    },
    "de": {
        "title": "Padel in Antalya — Clubs, Plätze, Preise (Guide 2026)",
        "desc": "Unabhängiger Guide für Padel in Antalya: Clubs in Konyaaltı und Lara, Platzpreise, Buchung ohne Partner, Training und Turniere.",
        "h1": "Padel in Antalya — Clubs, Plätze & wie man spielt",
        "intro": "Ein regelmäßig aktualisierter Guide für Padel in Antalya: wo die Plätze sind, was es kostet und wie man auch ohne Partner spielt.",
        "where": "Wo man in Antalya Padel spielt",
        "where_txt": "Padelplätze in Antalya konzentrieren sich auf drei Gebiete: <strong>Konyaaltı</strong> (Westen, küstennah), <strong>Muratpaşa / Lara</strong> (Zentrum und Osten) und die Hotelregion <strong>Belek</strong>. Unten die von uns verifizierten Clubs.",
        "cost": "Was kostet es?",
        "cost_txt": "Die Preise variieren je nach Club, Zeit und Saison. Beispiel V7 Padel Antalya: <strong>{price}</strong>. Bei anderen Clubs bitte direkt erfragen.",
        "solo": "Spielen ohne Partner",
        "solo_txt": "Sie müssen keine drei Freunde mitbringen. Community-Clubs bieten offene Spiele und Mixer, bei denen Einzelspieler nach Niveau zusammengebracht werden. Schreiben Sie dem Club über App oder WhatsApp.",
        "mfr": "Wer die Plätze baut",
        "mfr_txt": "Viele Plätze in Antalya und weltweit werden lokal gebaut. <a href='{url}' rel='nofollow'>{name}</a> ist ein in Antalya ansässiger Padelplatz-<strong>Hersteller</strong> (kein Club): entwirft, produziert und installiert Plätze für Clubs und Resorts weltweit.",
        "other": "Eine größere Platzliste (inkl. Belek-Hotels) bieten Verzeichnisse wie <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a>.",
        "lbl": {"area": "Gebiet", "courts": "Plätze", "hours": "Zeiten", "booking": "Buchung", "phone": "Telefon", "price": "Preis", "links": "Links"},
        "footer": "Gepflegt von der V7 Padel Community · Aktualisiert Juli 2026 · Nur verifizierte, öffentliche Clubs.",
    },
    "es": {
        "title": "Pádel en Antalya — clubes, pistas, precios (guía 2026)",
        "desc": "Guía independiente del pádel en Antalya: clubes en Konyaaltı y Lara, precios de pista, reserva sin pareja, clases y torneos.",
        "h1": "Pádel en Antalya — clubes, pistas y cómo jugar",
        "intro": "Una guía actualizada del pádel en Antalya: dónde están las pistas, cuánto cuesta y cómo jugar incluso sin pareja.",
        "where": "Dónde jugar al pádel en Antalya",
        "where_txt": "Las pistas en Antalya se concentran en tres zonas: <strong>Konyaaltı</strong> (oeste, junto a la costa), <strong>Muratpaşa / Lara</strong> (centro y este) y la franja hotelera de <strong>Belek</strong>. Abajo, los clubes que hemos verificado.",
        "cost": "¿Cuánto cuesta?",
        "cost_txt": "Los precios varían según el club, la hora y la temporada. Por ejemplo, en V7 Padel Antalya: <strong>{price}</strong>. Para otros clubes, consulta directamente.",
        "solo": "Jugar sin pareja",
        "solo_txt": "No hace falta traer a tres amigos. Los clubes de comunidad organizan partidos abiertos y mixers donde los jugadores solos se emparejan por nivel. Escribe al club por su app o WhatsApp.",
        "mfr": "Quién construye las pistas",
        "mfr_txt": "Muchas pistas en Antalya y el mundo se fabrican localmente. <a href='{url}' rel='nofollow'>{name}</a> es un <strong>fabricante</strong> de pistas de pádel con sede en Antalya (no un club): diseña, produce e instala pistas para clubes y resorts en todo el mundo.",
        "other": "Para una lista más amplia de pistas (incluidos hoteles de Belek), directorios como <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a> son una buena referencia.",
        "lbl": {"area": "Zona", "courts": "Pistas", "hours": "Horario", "booking": "Reserva", "phone": "Teléfono", "price": "Precio", "links": "Enlaces"},
        "footer": "Mantenida por la comunidad V7 Padel · Actualizado julio 2026 · Solo clubes verificados y abiertos al público.",
    },
    "fr": {
        "title": "Padel à Antalya — clubs, terrains, prix (guide 2026)",
        "desc": "Guide indépendant du padel à Antalya : clubs à Konyaaltı et Lara, prix des terrains, réservation sans partenaire, cours et tournois.",
        "h1": "Padel à Antalya — clubs, terrains et comment jouer",
        "intro": "Un guide régulièrement mis à jour du padel à Antalya : où sont les terrains, combien ça coûte et comment jouer même sans partenaire.",
        "where": "Où jouer au padel à Antalya",
        "where_txt": "Les terrains à Antalya se concentrent dans trois zones : <strong>Konyaaltı</strong> (ouest, près de la côte), <strong>Muratpaşa / Lara</strong> (centre et est) et la zone hôtelière de <strong>Belek</strong>. Ci-dessous, les clubs que nous avons vérifiés.",
        "cost": "Combien ça coûte ?",
        "cost_txt": "Les prix varient selon le club, l'heure et la saison. Par exemple, chez V7 Padel Antalya : <strong>{price}</strong>. Pour les autres clubs, renseignez-vous directement.",
        "solo": "Jouer sans partenaire",
        "solo_txt": "Pas besoin d'amener trois amis. Les clubs communautaires organisent des parties ouvertes et des mixers où les joueurs seuls sont regroupés par niveau. Écrivez au club via son app ou WhatsApp.",
        "mfr": "Qui construit les terrains",
        "mfr_txt": "Beaucoup de terrains à Antalya et ailleurs sont fabriqués localement. <a href='{url}' rel='nofollow'>{name}</a> est un <strong>fabricant</strong> de terrains de padel basé à Antalya (pas un club) : il conçoit, produit et installe des terrains pour des clubs et resorts dans le monde entier.",
        "other": "Pour une liste plus large de terrains (y compris les hôtels de Belek), des annuaires comme <a href='https://padelkoy.com/en' rel='nofollow'>PadelKöy</a> sont une bonne référence.",
        "lbl": {"area": "Zone", "courts": "Terrains", "hours": "Horaires", "booking": "Réservation", "phone": "Téléphone", "price": "Prix", "links": "Liens"},
        "footer": "Maintenu par la communauté V7 Padel · Mise à jour juillet 2026 · Uniquement des clubs vérifiés et ouverts au public.",
    },
}

BASE = "https://padelantalya.org"


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hreflang_block(cur_code):
    out = []
    for code, path, _ in LANGS:
        href = BASE + "/" + (path + "/" if path else "")
        out.append(f'<link rel="alternate" hreflang="{code}" href="{href}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{BASE}/">')
    return "\n".join(out)


def lang_switcher(cur_code):
    links = []
    for code, path, native in LANGS:
        href = BASE + "/" + (path + "/" if path else "")
        if code == cur_code:
            links.append(f'<strong>{native}</strong>')
        else:
            links.append(f'<a href="{href}">{native}</a>')
    return " · ".join(links)



# Pre-filled WhatsApp (конверсия из гида + операторы видят источник лида)
WA_PHONE = "905467800877"
WA_TEXTS = {
    "en": "Hi! I found you via the PadelAntalya guide — I'd like to book a court / join a game.",
    "tr": "Merhaba! PadelAntalya rehberinden ulaştım — kort rezervasyonu / oyuna katılım hakkında bilgi almak istiyorum.",
    "ru": "Здравствуйте! Нашёл вас через гид PadelAntalya — хочу забронировать корт / присоединиться к игре.",
    "de": "Hallo! Ich habe Sie über den PadelAntalya-Guide gefunden — ich möchte einen Platz buchen.",
    "es": "¡Hola! Los encontré por la guía PadelAntalya — quiero reservar una pista.",
    "fr": "Bonjour ! Je vous ai trouvés via le guide PadelAntalya — je voudrais réserver un terrain.",
}
def wa_link(lang):
    import urllib.parse
    txt = WA_TEXTS.get(lang, WA_TEXTS["en"])
    return f"https://wa.me/{WA_PHONE}?text={urllib.parse.quote(txt)}"


def club_card(club, t, lang="en"):
    L = t["lbl"]
    rows = [(L["area"], club["area"]), (L["courts"], club["courts"])]
    if club.get("hours"):
        rows.append((L["hours"], club["hours"]))
    phone_html = f' · <a href="{wa_link(lang)}" rel="nofollow">WhatsApp {club["phone"]}</a>' if club.get("phone") else ""
    rows.append((L["booking"], esc(club["booking"]) + phone_html))
    if club.get("price"):
        rows.append((L["price"], esc(club["price"])))
    links = []
    if club.get("website"):
        links.append(f'<a href="{club["website"]}" rel="nofollow">{club["website"].replace("https://","")}</a>')
    if club.get("instagram"):
        links.append(f'IG <a href="https://www.instagram.com/{club["instagram"]}" rel="nofollow">@{club["instagram"]}</a>')
    if links:
        rows.append((L["links"], " · ".join(links)))
    tr = "".join(f"<tr><th>{esc(k)}</th><td>{v}</td></tr>" for k, v in rows)
    cls = "card top" if club.get("primary") else "card"
    tag = f'<span class="tag">{esc(club["area"])}</span> <span class="tag">{esc(club["type"])}</span>'
    return f'<div class="{cls}"><h3>{esc(club["name"])} {tag}</h3><table>{tr}</table></div>'


def schema_jsonld(t):
    items = []
    for i, c in enumerate(CLUBS, 1):
        node = {"@type": "SportsActivityLocation", "name": c["name"],
                "address": {"@type": "PostalAddress", "streetAddress": c["address"],
                            "addressLocality": c["area"].split(" /")[0], "addressRegion": "Antalya", "addressCountry": "TR"}}
        if c.get("phone"): node["telephone"] = c["phone"]
        if c.get("website"): node["url"] = c["website"]
        if c.get("instagram"): node["sameAs"] = [f"https://www.instagram.com/{c['instagram']}"]
        if c.get("lat"): node["geo"] = {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lng"]}
        if c.get("hours"): node["openingHours"] = "Mo-Su 08:00-23:00"
        items.append({"@type": "ListItem", "position": i, "item": node})
    article = {"@context": "https://schema.org", "@type": "Article", "headline": t["h1"],
               "about": "Padel in Antalya, Turkey", "inLanguage": [c for c, _, _ in LANGS],
               "dateModified": DATE, "publisher": {"@type": "Organization", "name": "Padel Antalya Guide"}}
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": "Padel clubs in Antalya", "itemListElement": items}
    return (f'<script type="application/ld+json">{json.dumps(article, ensure_ascii=False)}</script>\n'
            f'<script type="application/ld+json">{json.dumps(itemlist, ensure_ascii=False)}</script>')


CSS = """*{box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,sans-serif;color:#13202b;background:#f7f9fb;margin:0;line-height:1.65}
header{background:linear-gradient(135deg,#0d2438,#14507a);color:#fff;padding:50px 20px 36px}.wrap{max-width:860px;margin:0 auto;padding:0 20px}
header h1{font-size:29px;margin:0 0 10px;line-height:1.25}header p{font-size:16px;opacity:.92;margin:0;max-width:62ch}
.langs{margin-top:16px;font-size:13px;opacity:.9}.langs a{color:#bfe0ff;text-decoration:none}.langs strong{color:#fff}
main{padding:32px 0 56px}h2{font-size:21px;margin:32px 0 12px;border-bottom:2px solid #e3e9ef;padding-bottom:6px}h3{font-size:17px;margin:18px 0 8px}
.card{background:#fff;border:1px solid #e3e9ef;border-radius:12px;padding:16px 20px;margin:14px 0}.top{border-color:#1f6feb;box-shadow:0 2px 14px rgba(31,111,235,.12)}
.tag{display:inline-block;background:#eaf2ff;color:#1f6feb;font-size:12px;font-weight:600;padding:2px 9px;border-radius:20px;margin:2px 4px 2px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:6px}th,td{text-align:left;padding:7px 10px;border-bottom:1px solid #e3e9ef;vertical-align:top}th{color:#5b6b78;font-weight:600;white-space:nowrap}
a{color:#1f6feb}footer{border-top:1px solid #e3e9ef;color:#5b6b78;font-size:13px;padding:22px 0;text-align:center}"""


def render(code, path, native):
    t = T[code]
    price = CLUBS[0].get("price", "")
    cards = "\n".join(club_card(c, t, code) for c in CLUBS)
    canonical = BASE + "/" + (path + "/" if path else "")
    html = f"""<!DOCTYPE html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="{canonical}">
{hreflang_block(code)}
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta name="robots" content="index,follow">
{schema_jsonld(t)}
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap">
  <h1>{esc(t['h1'])}</h1>
  <p>{esc(t['intro'])}</p>
  <div class="langs">{lang_switcher(code)}</div>
</div></header>
<main class="wrap">
<h2>{esc(t['where'])}</h2>
<p>{t['where_txt']}</p>
{cards}
<p style="color:#5b6b78;font-size:13px">{t['other']}</p>
<h2>{esc(t['cost'])}</h2>
<p>{t['cost_txt'].replace('{price}', esc(price))}</p>
<h2>{esc(t['solo'])}</h2>
<p>{t['solo_txt']}</p>
<h2>{esc(t['mfr'])}</h2>
<p>{t['mfr_txt'].replace('{url}', MFR['url']).replace('{name}', esc(MFR['name']))}</p>
</main>
<footer class="wrap">Padel Antalya Guide — {t['footer']}</footer>
</body>
</html>
"""
    if path:
        d = DOCS / path
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)
    else:
        (DOCS / "index.html").write_text(html)
    return canonical


TOPIC_LANGS = ["tr", "ru"]  # варианты помимо en; контент — ключи topic["tr"], topic["ru"]
TOPIC_UI = {
    "en": {"back": "← Antalya padel guide", "back_url": "/", "see": 'See the full <a href="{home}">Antalya padel guide</a> for all clubs, prices and how to book.',
           "footer": "Padel Antalya Guide — maintained by the V7 Padel community · Updated July 2026", "wa": "WhatsApp — book a court / ask a question"},
    "tr": {"back": "← Antalya padel rehberi", "back_url": "/tr/", "see": 'Tüm kulüpler, fiyatlar ve rezervasyon için <a href="{home}">Antalya padel rehberine</a> bakın.',
           "footer": "Padel Antalya Rehberi — V7 Padel topluluğu tarafından güncellenir · Temmuz 2026", "wa": "WhatsApp — kort ayırt / soru sor"},
    "ru": {"back": "← Гид по паделу в Анталье", "back_url": "/ru/", "see": 'Все клубы, цены и бронирование — в <a href="{home}">гиде по паделу в Анталье</a>.',
           "footer": "Padel Antalya Guide — поддерживается сообществом V7 Padel · Обновлено июль 2026", "wa": "WhatsApp — забронировать корт / задать вопрос"},
}

def render_topic(topic, lang="en"):
    """Topic-страница (FAQPage schema). lang="en" — корень /slug/, иначе /<lang>/<slug>/ c hreflang-связкой всех вариантов."""
    slug = topic["slug"]
    t = topic if lang == "en" else topic[lang]
    ui = TOPIC_UI[lang]
    canonical = f"{BASE}/{slug}/" if lang == "en" else f"{BASE}/{lang}/{slug}/"
    variants = [("en", f"{BASE}/{slug}/")] + [(L, f"{BASE}/{L}/{slug}/") for L in TOPIC_LANGS if L in topic]
    hreflang = "".join(f'<link rel="alternate" hreflang="{L}" href="{u}">' for L, u in variants)
    hreflang += f'<link rel="alternate" hreflang="x-default" href="{BASE}/{slug}/">'
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in t["faqs"]]}
    faq_html = "".join(
        f'<details class="card"><summary><strong>{esc(q)}</strong></summary>'
        f'<p style="margin-top:8px">{esc(a)}</p></details>'
        for q, a in t["faqs"])
    lang_switch = " · ".join(f'<a href="{u}">{L.upper()}</a>' for L, u in variants if L != lang)
    see_full = ui["see"].format(home=f"{BASE}{ui['back_url']}")
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="{canonical}">
{hreflang}
<meta name="robots" content="index,follow">
<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
<style>{CSS}
details summary{{cursor:pointer;font-size:15px}}details{{padding:14px 18px}}</style>
</head>
<body>
<header><div class="wrap">
  <h1>{esc(t['h1'])}</h1>
  <p>{esc(t['intro'])}</p>
  <div class="langs"><a href="{BASE}{ui['back_url']}">{ui['back']}</a> · {lang_switch}</div>
</div></header>
<main class="wrap">
<p style="margin:4px 0 14px"><a href="{wa_link(lang)}" rel="nofollow" style="display:inline-block;background:#0aBaB5;color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:700">{ui['wa']}</a></p>
{faq_html}
<p style="color:#5b6b78;font-size:13px;margin-top:20px">{see_full}</p>
</main>
<footer class="wrap">{ui['footer']}</footer>
</body>
</html>
"""
    d = (DOCS / slug) if lang == "en" else (DOCS / lang / slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html)
    return canonical


def main():
    urls = []
    for code, path, native in LANGS:
        urls.append(render(code, path, native))
    # topic-страницы под discovery-запросы (ChatGPT/Bing gap)
    try:
        topics = json.load(open(Path(__file__).parent / "topics.json"))["topics"]
        for tp in topics:
            urls.append(render_topic(tp))
            for L in TOPIC_LANGS:
                if L in tp:
                    urls.append(render_topic(tp, lang=L))
    except FileNotFoundError:
        pass
    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f'<url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>')
    sm.append('</urlset>')
    (DOCS / "sitemap.xml").write_text("\n".join(sm) + "\n")
    print(f"Built {len(urls)} pages + sitemap:")
    for u in urls:
        print("  " + u)


if __name__ == "__main__":
    main()
