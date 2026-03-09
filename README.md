# Pokémon GO PvP Advisor

A browser-based Pokémon GO PvP advisor with a move database, Pokémon database, type overview, selectable meta teams, league rankings, battle simulator and calculators.

## Features

- **⚡ Move Database** – All fast and charge moves with PvE and PvP power values, searchable and sortable; incl. **✦ Elite TM Comparison** showing which Pokémon benefit most from exclusive moves
- **🎯 Pokémon Database** – Pokédex entries with types, best PvP movesets and generation filter (Gen I–IX); filter by **GL/UL/ML League suitability**
- **🔮 Type Overview** – Full type strength and weakness table for all 18 types with Pokémon GO multipliers; dual-type matcher
- **🏆 Meta Teams** – Selectable top teams for Great League, Ultra League and Master League with synergy analysis and strategy tips
- **📊 League Rankings** – S/A/B-Tier list of the best Pokémon for all three leagues with type info and counter recommendations
- **⚔️ Battle Simulator** – Choose two Pokémon, analyze type advantages, move effectiveness and base stat comparison
- **🧮 Calculator** – CP calculator and IV rank calculator for all leagues; incl. **Shadow/Purified comparison**, **💰 Pokémon Cost Calculator**, **🎯 Catch Probability Calculator**, **🍬 XL Candy Guide**
- **🌍 Current Events** – Live overview of wild spawns, active raids and bonuses from Pokémon GO; **auto-refreshed weekly** via GitHub Actions (no PR required)
- **⭐ Stardust Rewards** – Overview of Stardust income from all in-game activities
- **🔍 Raid Counter** – Best counters for current raid bosses with type weaknesses and resistance analysis
- **🛠️ Team Builder** – Build your own team and analyse coverage, synergy and weaknesses
- **💎 Mega Guide** – Which Mega Evolutions are worth investing in for raids and PvP
- **🤝 Buddy & Seasons** – Buddy heart tracker, seasonal spawn changes and GBL season overview
- **🏅 Tournament Bracket** – Single-elimination and Round Robin brackets for local tournaments
- **☀️ Dark / Light Theme** – Toggle between dark and light mode; preference saved locally
- **📲 Offline Mode / PWA** – Installable as Progressive Web App, works without internet after first load

## Usage

The app consists of a single HTML file and requires no installation.

1. Download [`pokemon-go-advisor.html`](pokemon-go-advisor.html)
2. Open the file in a browser (e.g. by double-clicking)
3. Done – no server installation required

## Live Event Data (Auto-Update)

Event data (raids, wild spawns, bonuses, upcoming events) is stored in [`events.json`](events.json) and updated **automatically every Monday** via a GitHub Actions workflow (`.github/workflows/update-events.yml`).

The app fetches the latest `events.json` from GitHub on page load and updates the Current Events section in real time — **no pull request or manual update required**.

If the remote data is unavailable (offline, CORS), the app falls back to the hardcoded baseline in `CURRENT_EVENTS`.

## Logo

The app logo is available as [`logo.svg`](logo.svg) and is embedded as the browser favicon.

## Technology

- Pure HTML, CSS and JavaScript (no external frameworks)
- Sprites loaded live from [PokéAPI](https://pokeapi.co/)
- Fonts: [Bangers](https://fonts.google.com/specimen/Bangers) & [DM Sans](https://fonts.google.com/specimen/DM+Sans) via Google Fonts
- Event data auto-updated via GitHub Actions + Python scraper ([`scripts/update_events.py`](scripts/update_events.py))

---

## ✅ Completed Roadmap

All planned features have been implemented. Items below are crossed off as done.

### High Priority

| Feature | Status | Notes |
|---|---|---|
| ~~**IV Calculator**~~ | ✅ Done | IV rank calculator in Calculator tab |
| ~~**Battle Simulator**~~ | ✅ Done | Tab 8 – full move + type analysis |
| ~~**CP Calculator**~~ | ✅ Done | CP calculation in Calculator tab |
| ~~**Shadow Pokémon Guide**~~ | ✅ Done | Shadow/Purified comparison in Calculator |
| ~~**Automatic Meta Updates**~~ | ✅ Done | `events.json` auto-updated weekly via GitHub Actions |

### Medium Priority

| Feature | Status | Notes |
|---|---|---|
| ~~**Raid Counter**~~ | ✅ Done | Tab 10 – counters with type weaknesses |
| ~~**Mega Evolution Guide**~~ | ✅ Done | Tab 12 – PvP and raid viability |
| ~~**Team Builder**~~ | ✅ Done | Tab 11 – synergy and coverage analysis |
| ~~**Buddy Optimization**~~ | ✅ Done | In Buddy & Seasons tab |
| ~~**Seasons Tracker**~~ | ✅ Done | GBL season overview in Buddy tab |

### Further Ideas

| Feature | Status | Notes |
|---|---|---|
| ~~**Catch Probability Calculator**~~ | ✅ Done | In Calculator tab |
| ~~**Tournament Bracket Generator**~~ | ✅ Done | Tab 14 – single elim + round robin |
| ~~**Buddy Heart Tracker**~~ | ✅ Done | Daily/weekly tracker in Buddy tab |
| ~~**Move Comparison (Elite TM)**~~ | ✅ Done | In Moves tab – verdict, PvP advantage vs. best standard |
| ~~**Offline Mode / PWA**~~ | ✅ Done | `manifest.json` + `sw.js` service worker |
| ~~**Pokémon Cost Calculator**~~ | ✅ Done | Evolution + power-up costs in Calculator tab |
| ~~**XL Candy Guide**~~ | ✅ Done | Priority list by league in Calculator tab |
| ~~**Dark/Light Theme**~~ | ✅ Done | Theme toggle in nav bar |
| ~~**League Viability Filter**~~ | ✅ Done | GL/UL/ML filter in Pokédex tab |
| **Multilingual Support** | 🔜 Planned | EN/DE language toggle – planned for next iteration |

