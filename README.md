# Pokémon GO PvP Advisor

A **mobile-first** Progressive Web App (PWA) for Pokémon GO PvP — optimised for smartphones and installable on iOS and Android. Includes a move database, Pokédex, type overview, meta teams, league rankings, battle simulator, calculators and more.

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

## 📱 Mobile & PWA

The app is designed **primarily for mobile** use and is fully optimised for smartphones:

- **Installable** on iOS (Safari → "Add to Home Screen") and Android (Chrome → "Install app")
- Supports iOS notch/home-indicator safe areas (`viewport-fit=cover`)
- Respects the system status bar colour (`apple-mobile-web-app-status-bar-style`)
- Responsive layout adapts to all screen sizes from 320 px upwards
- The horizontal navigation bar is touch-scrollable with hidden scrollbars

### Automatic App Updates (mobile)

When a new version of the app is deployed, your device will automatically download it in the background. A **"🆕 A new version is available!"** banner appears at the bottom of the screen. Tap **Refresh** to instantly switch to the new version — no manual cache-clearing needed.

The service worker uses a **network-first** strategy for the main HTML document, ensuring you always receive the latest version when online. All other static assets (logo, manifest, sprites) are served from cache for fast load times and offline support.

## Usage

The app consists of a single HTML file and requires no installation.

1. Download [`pokemon-go-advisor.html`](pokemon-go-advisor.html)
2. Open the file in a mobile browser (iOS Safari or Android Chrome recommended)
3. Use "Add to Home Screen" for the best full-screen experience
4. Done – no server installation required

## Live Event Data (Auto-Update)

Event data (raids, wild spawns, bonuses, upcoming events) is stored in [`events.json`](events.json) and updated **automatically every Monday** via a GitHub Actions workflow (`.github/workflows/update-events.yml`).

The app fetches the latest `events.json` from GitHub on page load and updates the Current Events section in real time — **no pull request or manual update required**.

If the remote data is unavailable (offline, CORS), the app falls back to the hardcoded baseline in `CURRENT_EVENTS`.

## Logo

The app logo is available as [`logo.svg`](logo.svg) and is embedded as the browser favicon and PWA icon.

## Technology

- Pure HTML, CSS and JavaScript (no external frameworks)
- **PWA**: Service Worker (`sw.js`) + Web App Manifest (`manifest.json`) — installable, works offline
- **Mobile-first**: `viewport-fit=cover`, Apple PWA meta tags, safe-area-inset padding, touch-scroll navigation
- **Auto-update**: network-first HTML fetching + SW update detection with user-facing refresh banner
- Sprites loaded live from [PokéAPI](https://pokeapi.co/)
- Fonts: [Bangers](https://fonts.google.com/specimen/Bangers) & [DM Sans](https://fonts.google.com/specimen/DM+Sans) via Google Fonts
- Event data auto-updated via GitHub Actions + Python scraper ([`scripts/update_events.py`](scripts/update_events.py))

---

## 🗒️ Open Suggestions

Planned and proposed features that are not yet implemented are tracked in **[SUGGESTIONS.md](SUGGESTIONS.md)**.
The file includes a comparison with five leading Pokémon GO community sites and five new feature proposals.

