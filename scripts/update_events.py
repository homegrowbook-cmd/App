#!/usr/bin/env python3
"""
update_events.py – Auto-updates events.json from Pokémon GO Hub and Pokémon GO Live.

Fetches:
  - Current raid bosses from https://pokemongohub.net/post/guide/current-go-raids/
  - Upcoming events from https://pokemongohub.net/post/event/

Run this script in CI (GitHub Actions) on a weekly schedule.
It reads events.json, updates what it can from live sources,
and writes the result back. Falls back gracefully if fetching fails.

Primary source: Pokémon GO Hub (pokemongohub.net) – community-verified, updated with
every event rotation and widely regarded as the most reliable third-party tracker.
Fallback source: Leek Duck (leekduck.com) – used only if the primary source fails.

Usage:
    python scripts/update_events.py
"""

import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

EVENTS_JSON = Path(__file__).parent.parent / "events.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; PokemonGO-Events-Updater/1.0; "
        "+https://github.com/homegrowbook-cmd/App)"
    )
}

# Primary source: Pokémon GO Hub – community-verified tracker, updated with every rotation
POGOHUB_RAIDS_URL  = "https://pokemongohub.net/post/guide/current-go-raids/"
POGOHUB_EVENTS_URL = "https://pokemongohub.net/post/event/"

# Fallback source: Leek Duck – used only when the primary source is unavailable
LEEKDUCK_BOSS_URL   = "https://leekduck.com/raid-bosses/"
LEEKDUCK_EVENTS_URL = "https://leekduck.com/events/"


def fetch(url: str, timeout: int = 15) -> str | None:
    """Fetch a URL and return the HTML as a string, or None on error."""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError, OSError) as exc:
        print(f"[warn] Could not fetch {url}: {exc}", file=sys.stderr)
        return None


# ── Pokémon GO Hub raid-boss parser ──────────────────────────────────────────

class PoGoHubRaidParser(HTMLParser):
    """Minimal HTML parser to extract raid boss names and tiers from pokemongohub.net."""

    # Maps heading text → normalised tier label
    TIER_KEYWORDS = {
        "tier 1": "1★",
        "1-star": "1★",
        "1 star": "1★",
        "tier 3": "3★",
        "3-star": "3★",
        "3 star": "3★",
        "tier 5": "5★",
        "5-star": "5★",
        "5 star": "5★",
        "mega": "Mega",
        "shadow": "Shadow",
    }

    def __init__(self):
        super().__init__()
        self.bosses: dict[str, list[dict]] = {}
        self._current_tier: str | None = None
        self._in_heading = False
        self._heading_buf = ""
        self._in_boss = False
        self._boss_buf = ""
        self._heading_tags = {"h2", "h3", "h4"}

    def _detect_tier(self, text: str) -> str | None:
        lower = text.lower()
        for keyword, label in self.TIER_KEYWORDS.items():
            if keyword in lower:
                return label
        return None

    def handle_starttag(self, tag: str, attrs_list):
        attrs = dict(attrs_list)
        classes = attrs.get("class", "")

        if tag in self._heading_tags:
            self._in_heading = True
            self._heading_buf = ""
            return

        # Boss name: look for common entry/card class patterns
        if tag in ("li", "span", "div", "p"):
            if any(kw in classes for kw in ("entry", "boss", "pokemon", "raid-boss", "name")):
                self._in_boss = True
                self._boss_buf = ""

    def handle_endtag(self, tag: str):
        if tag in self._heading_tags and self._in_heading:
            self._in_heading = False
            tier = self._detect_tier(self._heading_buf)
            if tier:
                self._current_tier = tier
                if tier not in self.bosses:
                    self.bosses[tier] = []
            return

        if self._in_boss and tag in ("li", "span", "div", "p"):
            self._in_boss = False
            name = self._boss_buf.strip()
            if name and len(name) > 2 and self._current_tier:
                # Avoid duplicates
                existing = {b["name"].lower() for b in self.bosses[self._current_tier]}
                if name.lower() not in existing:
                    self.bosses[self._current_tier].append({
                        "name": name,
                        "types": [],
                        "num": 0,
                        "source": POGOHUB_RAIDS_URL,
                    })

    def handle_data(self, data: str):
        if self._in_heading:
            self._heading_buf += data
        elif self._in_boss:
            self._boss_buf += data


# ── Leek Duck raid-boss parser (fallback) ────────────────────────────────────

class RaidBossParser(HTMLParser):
    """Minimal HTML parser to extract raid boss names and tiers from leekduck.com/raid-bosses/."""

    # Maps Leek Duck CSS class → normalised tier label
    TIER_MAP = {
        "raid-boss-tier-1":  "1★",
        "raid-boss-tier-3":  "3★",
        "raid-boss-tier-5":  "5★",
        "raid-boss-mega":    "Mega",
        "raid-boss-tier-ex": "EX",
    }

    def __init__(self):
        super().__init__()
        self.bosses: dict[str, list[dict]] = {}
        self._current_tier: str | None = None
        self._in_boss_name = False
        self._boss_name_buf = ""
        self._boss_queue: list[dict] = []   # bosses found before their tier header

    def handle_starttag(self, tag: str, attrs_list):
        attrs = dict(attrs_list)
        classes = attrs.get("class", "")

        # Tier header
        for css, label in self.TIER_MAP.items():
            if css in classes:
                self._current_tier = label
                if label not in self.bosses:
                    self.bosses[label] = []
                return

        # Boss name span
        if tag == "span" and "boss-name" in classes:
            self._in_boss_name = True
            self._boss_name_buf = ""

    def handle_endtag(self, tag: str):
        if tag == "span" and self._in_boss_name:
            self._in_boss_name = False
            name = self._boss_name_buf.strip()
            if name and self._current_tier:
                self.bosses[self._current_tier].append({
                    "name": name,
                    "types": [],          # types not reliably available in HTML
                    "num": 0,             # Pokédex number added in post-processing
                    "source": LEEKDUCK_BOSS_URL,
                })

    def handle_data(self, data: str):
        if self._in_boss_name:
            self._boss_name_buf += data


def parse_raid_bosses(html: str) -> dict[str, list[dict]]:
    """Parse Leek Duck raid boss HTML and return a tier→boss dict."""
    parser = RaidBossParser()
    parser.feed(html)
    # Remove empty tiers and tiers we don't recognise
    known = {"1★", "3★", "5★", "Mega"}
    return {t: v for t, v in parser.bosses.items() if t in known and v}


# ── Leek Duck events parser ───────────────────────────────────────────────────

class EventsPageParser(HTMLParser):
    """Extract upcoming events from leekduck.com/events/."""

    def __init__(self):
        super().__init__()
        self.events: list[dict] = []
        self._in_event = False
        self._in_title = False
        self._in_date  = False
        self._title_buf = ""
        self._date_buf  = ""
        self._depth = 0
        self._event_depth = 0

    def handle_starttag(self, tag, attrs_list):
        attrs = dict(attrs_list)
        classes = attrs.get("class", "")
        self._depth += 1

        if "event-item" in classes or "upcoming-event" in classes:
            self._in_event = True
            self._event_depth = self._depth
            self._title_buf = ""
            self._date_buf = ""

        if self._in_event:
            if "event-name" in classes or "event-title" in classes:
                self._in_title = True
            if "event-date" in classes or "event-time" in classes:
                self._in_date = True

    def handle_endtag(self, tag):
        if self._in_event and self._depth == self._event_depth:
            title = self._title_buf.strip()
            ev_date = self._date_buf.strip()
            if title:
                self.events.append({
                    "icon": "📅",
                    "name": title,
                    "date": ev_date or "TBA",
                    "desc": "",
                    "source": LEEKDUCK_EVENTS_URL,
                })
            self._in_event = False
            self._in_title = False
            self._in_date  = False
        if self._in_title and tag in ("span", "h3", "h4", "div"):
            self._in_title = False
        if self._in_date and tag in ("span", "div", "time"):
            self._in_date = False
        self._depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self._title_buf += data
        elif self._in_date:
            self._date_buf += data


# ── Pokémon GO Hub events parser ──────────────────────────────────────────────

class PoGoHubEventsParser(HTMLParser):
    """Extract upcoming events from pokemongohub.net/post/event/."""

    def __init__(self):
        super().__init__()
        self.events: list[dict] = []
        self._in_article = False
        self._in_title = False
        self._in_date = False
        self._title_buf = ""
        self._date_buf = ""
        self._depth = 0
        self._article_depth = 0

    def handle_starttag(self, tag, attrs_list):
        attrs = dict(attrs_list)
        classes = attrs.get("class", "")
        self._depth += 1

        if tag == "article" or "post-item" in classes or "entry-summary" in classes:
            self._in_article = True
            self._article_depth = self._depth
            self._title_buf = ""
            self._date_buf = ""

        if self._in_article:
            if tag in ("h2", "h3") or "entry-title" in classes or "post-title" in classes:
                self._in_title = True
            if tag in ("time",) or "entry-date" in classes or "post-date" in classes:
                self._in_date = True
                dt = attrs.get("datetime", "")
                if dt:
                    self._date_buf = dt[:10]

    def handle_endtag(self, tag):
        if self._in_article and self._depth == self._article_depth:
            title = self._title_buf.strip()
            ev_date = self._date_buf.strip()
            if title and len(title) > 5:
                self.events.append({
                    "icon": "📅",
                    "name": title,
                    "date": ev_date or "TBA",
                    "desc": "",
                    "source": POGOHUB_EVENTS_URL,
                })
            self._in_article = False
            self._in_title = False
            self._in_date = False
        if self._in_title and tag in ("h2", "h3", "a", "span"):
            self._in_title = False
        if self._in_date and tag in ("time", "span"):
            self._in_date = False
        self._depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self._title_buf += data
        elif self._in_date and not self._date_buf:
            self._date_buf += data


def parse_raid_bosses_pogohub(html: str) -> dict[str, list[dict]]:
    """Parse Pokémon GO Hub raid boss HTML and return a tier→boss dict."""
    parser = PoGoHubRaidParser()
    parser.feed(html)
    known = {"1★", "3★", "5★", "Mega", "Shadow"}
    return {t: v for t, v in parser.bosses.items() if t in known and v}


def parse_raid_bosses_leekduck(html: str) -> dict[str, list[dict]]:
    """Parse Leek Duck raid boss HTML and return a tier→boss dict (fallback)."""
    parser = RaidBossParser()
    parser.feed(html)
    # Remove empty tiers and tiers we don't recognise
    known = {"1★", "3★", "5★", "Mega"}
    return {t: v for t, v in parser.bosses.items() if t in known and v}


def parse_upcoming_events_pogohub(html: str) -> list[dict]:
    """Parse Pokémon GO Hub events page and return a list of future events."""
    parser = PoGoHubEventsParser()
    parser.feed(html)
    seen: set[str] = set()
    result: list[dict] = []
    for ev in parser.events:
        key = ev["name"].lower()
        if key not in seen and len(key) > 3:
            seen.add(key)
            result.append(ev)
        if len(result) >= 8:
            break
    return result


def parse_upcoming_events_leekduck(html: str) -> list[dict]:
    """Parse Leek Duck events page and return a list of future events (fallback)."""
    parser = EventsPageParser()
    parser.feed(html)
    # Keep at most 8 entries and deduplicate
    seen: set[str] = set()
    result: list[dict] = []
    for ev in parser.events:
        key = ev["name"].lower()
        if key not in seen and len(key) > 3:
            seen.add(key)
            result.append(ev)
        if len(result) >= 8:
            break
    return result


# ── Pokédex number lookup ────────────────────────────────────────────────────

# Lightweight name→dex mapping for the most common raid bosses.
# Extend this list as needed; for unknown Pokémon num stays 0.
_POKEDEX: dict[str, int] = {
    "bulbasaur": 1, "ivysaur": 2, "venusaur": 3, "charmander": 4, "charmeleon": 5,
    "charizard": 6, "squirtle": 7, "wartortle": 8, "blastoise": 9, "caterpie": 10,
    "metapod": 11, "butterfree": 12, "weedle": 13, "kakuna": 14, "beedrill": 15,
    "pidgey": 16, "pidgeotto": 17, "pidgeot": 18, "rattata": 19, "raticate": 20,
    "spearow": 21, "fearow": 22, "ekans": 23, "arbok": 24, "pikachu": 25,
    "raichu": 26, "sandshrew": 27, "sandslash": 28, "nidoran♀": 29, "nidorina": 30,
    "nidoqueen": 31, "nidoran♂": 32, "nidorino": 33, "nidoking": 34,
    "clefairy": 35, "clefable": 36, "vulpix": 37, "ninetales": 38, "jigglypuff": 39,
    "wigglytuff": 40, "zubat": 41, "golbat": 42, "oddish": 43, "gloom": 44,
    "vileplume": 45, "paras": 46, "parasect": 47, "venonat": 48, "venomoth": 49,
    "diglett": 50, "dugtrio": 51, "meowth": 52, "persian": 53, "psyduck": 54,
    "golduck": 55, "mankey": 56, "primeape": 57, "growlithe": 58, "arcanine": 59,
    "poliwag": 60, "poliwhirl": 61, "poliwrath": 62, "abra": 63, "kadabra": 64,
    "alakazam": 65, "machop": 66, "machoke": 67, "machamp": 68, "bellsprout": 69,
    "weepinbell": 70, "victreebel": 71, "tentacool": 72, "tentacruel": 73,
    "geodude": 74, "graveler": 75, "golem": 76, "ponyta": 77, "rapidash": 78,
    "slowpoke": 79, "slowbro": 80, "magnemite": 81, "magneton": 82, "farfetch'd": 83,
    "doduo": 84, "dodrio": 85, "seel": 86, "dewgong": 87, "grimer": 88,
    "muk": 89, "shellder": 90, "cloyster": 91, "gastly": 92, "haunter": 93,
    "gengar": 94, "onix": 95, "drowzee": 96, "hypno": 97, "krabby": 98,
    "kingler": 99, "voltorb": 100, "electrode": 101, "exeggcute": 102,
    "exeggutor": 103, "cubone": 104, "marowak": 105, "hitmonlee": 106,
    "hitmonchan": 107, "lickitung": 108, "koffing": 109, "weezing": 110,
    "rhyhorn": 111, "rhydon": 112, "chansey": 113, "tangela": 114, "kangaskhan": 115,
    "horsea": 116, "seadra": 117, "goldeen": 118, "seaking": 119, "staryu": 120,
    "starmie": 121, "mr. mime": 122, "scyther": 123, "jynx": 124, "electabuzz": 125,
    "magmar": 126, "pinsir": 127, "tauros": 128, "magikarp": 129, "gyarados": 130,
    "lapras": 131, "ditto": 132, "eevee": 133, "vaporeon": 134, "jolteon": 135,
    "flareon": 136, "porygon": 137, "omanyte": 138, "omastar": 139, "kabuto": 140,
    "kabutops": 141, "aerodactyl": 142, "snorlax": 143, "articuno": 144,
    "zapdos": 145, "moltres": 146, "dratini": 147, "dragonair": 148, "dragonite": 149,
    "mewtwo": 150, "mew": 151,
    # Gen II
    "chikorita": 152, "bayleef": 153, "meganium": 154, "cyndaquil": 155,
    "quilava": 156, "typhlosion": 157, "totodile": 158, "croconaw": 159,
    "feraligatr": 160, "sentret": 161, "furret": 162, "hoothoot": 163,
    "noctowl": 164, "ledyba": 165, "ledian": 166, "spinarak": 167, "ariados": 168,
    "crobat": 169, "chinchou": 170, "lanturn": 171, "pichu": 172, "cleffa": 173,
    "igglybuff": 174, "togepi": 175, "togetic": 176, "natu": 177, "xatu": 178,
    "mareep": 179, "flaaffy": 180, "ampharos": 181, "bellossom": 182, "marill": 183,
    "azumarill": 184, "sudowoodo": 185, "politoed": 186, "hoppip": 187,
    "skiploom": 188, "jumpluff": 189, "aipom": 190, "sunkern": 191, "sunflora": 192,
    "yanma": 193, "wooper": 194, "quagsire": 195, "espeon": 196, "umbreon": 197,
    "murkrow": 198, "slowking": 199, "misdreavus": 200, "unown": 201, "wobbuffet": 202,
    "girafarig": 203, "pineco": 204, "forretress": 205, "dunsparce": 206,
    "gligar": 207, "steelix": 208, "snubbull": 209, "granbull": 210, "qwilfish": 211,
    "scizor": 212, "shuckle": 213, "heracross": 214, "sneasel": 215, "teddiursa": 216,
    "ursaring": 217, "slugma": 218, "magcargo": 219, "swinub": 220, "piloswine": 221,
    "corsola": 222, "remoraid": 223, "octillery": 224, "delibird": 225,
    "mantine": 226, "skarmory": 227, "houndour": 228, "houndoom": 229,
    "kingdra": 230, "phanpy": 231, "donphan": 232, "porygon2": 233, "stantler": 234,
    "smeargle": 235, "tyrogue": 236, "hitmontop": 237, "smoochum": 238,
    "elekid": 239, "magby": 240, "miltank": 241, "blissey": 242, "raikou": 243,
    "entei": 244, "suicune": 245, "larvitar": 246, "pupitar": 247, "tyranitar": 248,
    "lugia": 249, "ho-oh": 250, "celebi": 251,
    # Gen III
    "treecko": 252, "grovyle": 253, "sceptile": 254, "torchic": 255, "combusken": 256,
    "blaziken": 257, "mudkip": 258, "marshtomp": 259, "swampert": 260,
    "salamence": 373, "metagross": 376, "regirock": 377, "regice": 378,
    "registeel": 379, "latias": 380, "latios": 381, "kyogre": 382, "groudon": 383,
    "rayquaza": 384, "jirachi": 385, "deoxys": 386,
    # Gen IV
    "turtwig": 387, "grotle": 388, "torterra": 389, "chimchar": 390, "monferno": 391,
    "infernape": 392, "piplup": 393, "prinplup": 394, "empoleon": 395,
    "starly": 396, "staravia": 397, "staraptor": 398,
    "shieldon": 410, "bastiodon": 411,
    "dialga": 483, "palkia": 484, "heatran": 485, "regigigas": 486, "giratina": 487,
    "cresselia": 488, "manaphy": 490, "darkrai": 491, "shaymin": 492, "arceus": 493,
    # Gen V
    "snivy": 495, "servine": 496, "serperior": 497,
    "whismur": 293, "loudred": 294, "exploud": 295,
    "tornadus": 641, "thundurus": 642, "reshiram": 643, "zekrom": 644,
    "landorus": 645, "kyurem": 646, "keldeo": 647, "meloetta": 648, "genesect": 649,
    # Gen VI
    "chespin": 650, "quilladin": 651, "chesnaught": 652,
    "xerneas": 716, "yveltal": 717, "zygarde": 718, "diancie": 719,
    "hoopa": 720, "volcanion": 721,
    # Gen VII
    "rowlet": 722, "litten": 725, "popplio": 728,
    "cosmog": 789, "cosmoem": 790, "solgaleo": 791, "lunala": 792,
    "nihilego": 793, "necrozma": 800, "magearna": 801, "marshadow": 802,
    "zeraora": 807,
    # Gen VIII
    "grookey": 810, "thwackey": 811, "rillaboom": 812,
    "scorbunny": 813, "raboot": 814, "cinderace": 815,
    "sobble": 816, "drizzile": 817, "inteleon": 818,
    "zacian": 888, "zamazenta": 889, "eternatus": 890,
    "kubfu": 891, "urshifu": 892, "zarude": 893, "regieleki": 894, "regidrago": 895,
    "glastrier": 896, "spectrier": 897, "calyrex": 898,
    # Megas (resolve from base)
    "mega venusaur": 3, "mega charizard x": 6, "mega charizard y": 6,
    "mega blastoise": 9, "mega beedrill": 15, "mega pidgeot": 18,
    "mega steelix": 208, "mega slowbro": 80, "mega gengar": 94, "mega kangaskhan": 115,
    "mega pinsir": 127, "mega gyarados": 130, "mega aerodactyl": 142,
    "mega ampharos": 181, "mega scizor": 212, "mega heracross": 214,
    "mega houndoom": 229, "mega tyranitar": 248, "mega sceptile": 254,
    "mega blaziken": 257, "mega swampert": 260, "mega gardevoir": 282,
    "mega aggron": 306, "mega medicham": 308, "mega manectric": 310,
    "mega altaria": 334, "mega salamence": 373, "mega metagross": 376,
    "mega latias": 380, "mega latios": 381, "mega rayquaza": 384,
    "mega lopunny": 428, "mega garchomp": 445, "mega lucario": 448,
    "mega abomasnow": 460, "mega gallade": 475,
    "mega audino": 531, "mega diancie": 719,
}


def dex_num(name: str) -> int:
    """Return the Pokédex number for a Pokémon name, or 0 if unknown."""
    return _POKEDEX.get(name.lower(), 0)


# ── Main update logic ────────────────────────────────────────────────────────

def load_events() -> dict:
    with open(EVENTS_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def save_events(data: dict) -> None:
    with open(EVENTS_JSON, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print(f"[ok] events.json updated → lastUpdated: {data['lastUpdated']}")


def update_raids(events: dict) -> bool:
    """Fetch current raid bosses from Pokémon GO Hub (primary) or Leek Duck (fallback)."""
    # Try primary source: Pokémon GO Hub
    html = fetch(POGOHUB_RAIDS_URL)
    if html:
        bosses = parse_raid_bosses_pogohub(html)
        if bosses:
            for tier_bosses in bosses.values():
                for boss in tier_bosses:
                    boss["num"] = dex_num(boss["name"])
            events["raids"] = bosses
            events["sources"]["raids"] = POGOHUB_RAIDS_URL
            print(f"[ok] Raids updated from GO Hub: {sum(len(v) for v in bosses.values())} bosses across {len(bosses)} tiers.")
            return True
        print("[warn] No raid bosses parsed from GO Hub – trying Leek Duck fallback.", file=sys.stderr)

    # Fallback: Leek Duck
    html = fetch(LEEKDUCK_BOSS_URL)
    if not html:
        return False
    bosses = parse_raid_bosses_leekduck(html)
    if not bosses:
        print("[warn] No raid bosses parsed from Leek Duck fallback – skipping raid update.", file=sys.stderr)
        return False
    for tier_bosses in bosses.values():
        for boss in tier_bosses:
            boss["num"] = dex_num(boss["name"])
    events["raids"] = bosses
    events["sources"]["raids"] = LEEKDUCK_BOSS_URL
    print(f"[ok] Raids updated from Leek Duck (fallback): {sum(len(v) for v in bosses.values())} bosses across {len(bosses)} tiers.")
    return True


def update_future_events(events: dict) -> bool:
    """Fetch upcoming events from Pokémon GO Hub (primary) or Leek Duck (fallback)."""
    # Try primary source: Pokémon GO Hub
    html = fetch(POGOHUB_EVENTS_URL)
    if html:
        upcoming = parse_upcoming_events_pogohub(html)
        if upcoming:
            events["futureEvents"] = upcoming
            events["sources"]["futureEvents"] = POGOHUB_EVENTS_URL
            print(f"[ok] Future events updated from GO Hub: {len(upcoming)} events found.")
            return True
        print("[warn] No upcoming events parsed from GO Hub – trying Leek Duck fallback.", file=sys.stderr)

    # Fallback: Leek Duck
    html = fetch(LEEKDUCK_EVENTS_URL)
    if not html:
        return False
    upcoming = parse_upcoming_events_leekduck(html)
    if not upcoming:
        print("[warn] No upcoming events parsed from Leek Duck fallback – skipping future-events update.", file=sys.stderr)
        return False
    events["futureEvents"] = upcoming
    events["sources"]["futureEvents"] = LEEKDUCK_EVENTS_URL
    print(f"[ok] Future events updated from Leek Duck (fallback): {len(upcoming)} events found.")
    return True


def main() -> int:
    print(f"[info] Loading {EVENTS_JSON}")
    events = load_events()

    today = date.today().isoformat()
    changed = False

    if update_raids(events):
        changed = True
    if update_future_events(events):
        changed = True

    # Always update lastUpdated and mark as auto-updated
    events["lastUpdated"] = today
    events["autoUpdated"] = True
    changed = True

    save_events(events)
    return 0


if __name__ == "__main__":
    sys.exit(main())
