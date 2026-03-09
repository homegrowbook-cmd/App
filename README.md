# Pokémon GO PvP Advisor

A browser-based Pokémon GO PvP advisor with a move database, Pokémon database, type overview, selectable meta teams, league rankings, battle simulator and calculators.

## Features

- **⚡ Move Database** – All fast and charge moves with PvE and PvP power values, searchable and sortable
- **🎯 Pokémon Database** – Pokédex entries with types, best PvP movesets and generation filter (Gen I–IX)
- **🔮 Type Overview** – Full type strength and weakness table for all 18 types with Pokémon GO multipliers; dual-type matcher
- **🏆 Meta Teams** – Selectable top teams for Great League, Ultra League and Master League with synergy analysis and strategy tips
- **📊 League Rankings** – S/A/B-Tier list of the best Pokémon for all three leagues with type info and counter recommendations
- **⚔️ Battle Simulator** – Choose two Pokémon, analyze type advantages, move effectiveness and base stat comparison
- **🧮 Calculator** – CP calculator and IV rank calculator for all leagues; incl. **Shadow/Purified comparison**
- **🌍 Current Events** – Live overview of wild spawns, active raids and bonuses from Pokémon GO
- **⭐ Stardust Rewards** – Overview of Stardust income from all in-game activities

## Usage

The app consists of a single HTML file and requires no installation.

1. Download [`pokemon-go-advisor.html`](pokemon-go-advisor.html)
2. Open the file in a browser (e.g. by double-clicking)
3. Done – no server installation required

## Logo

The app logo is available as [`logo.svg`](logo.svg) and is embedded as the browser favicon.

## Technology

- Pure HTML, CSS and JavaScript (no external frameworks)
- Sprites loaded live from [PokéAPI](https://pokeapi.co/)
- Fonts: [Bangers](https://fonts.google.com/specimen/Bangers) & [DM Sans](https://fonts.google.com/specimen/DM+Sans) via Google Fonts

---

## 💡 Possible Improvements (based on leading Pokémon GO sites)

The following features would be valuable additions, inspired by [PVPoke](https://pvpoke.com), [GamePress](https://gamepress.gg/pokemongo), [GO Hub](https://pokemongohub.net), [Silph Road](https://thesilpharena.com) and [PokeGenie](https://pokegenie.net):

### High Priority

| Feature | Description | Reference |
|---|---|---|
| **IV Calculator** | Calculate optimal IVs for each CP cap (e.g. 0/15/15 for GL) – incl. rank display | PVPoke, PokeGenie |
| **Battle Simulator** | 1v1 matchup simulation between two Pokémon with shield scenarios (0/0, 1/1, 2/2) | PVPoke |
| **CP Calculator** | CP calculation at any level and IVs | PokeGenie, Calcy IV |
| **Shadow Pokémon Guide** | Comparison: Shadow vs. normal vs. Purified – when is Shadow worth it? | GamePress, GO Hub |
| **Automatic Meta Updates** | League rankings automatically updated via PVPoke API instead of manual maintenance | PVPoke |

### Medium Priority

| Feature | Description | Reference |
|---|---|---|
| **Raid Counter** | Best counters for current raid bosses with DPS/TDO values | GamePress, Pokebattler |
| **Mega Evolution Guide** | Which Mega Evolution is worth it for raids and PvP? | GamePress |
| **Team Builder** | Build your own team from the Pokémon database and check synergy | PVPoke |
| **Buddy Optimization** | Which Pokémon bring the most Candy as Buddy (CP cost vs. benefit) | GO Hub |
| **Seasons Tracker** | Tracking GBL season changes and meta shifts | Silph Road |

### Further Ideas

| Feature | Description |
|---|---|
| **Catch Probability Calculator** | Best balls, berries and medals for difficult catches |
| **Tournament Bracket Generator** | Create your own tournaments and track results |
| **Buddy Heart Tracker** | Daily and weekly goals for Buddy hearts |
| **Move Comparison (Elite TM)** | Is an Elite TM worth it for a specific Pokémon? |
| **Offline Mode / PWA** | App installable as Progressive Web App (no browser required) |
| **Multilingual Support** | Translations for international users |
| **Pokémon Cost Calculator** | How much Stardust and Candy does a full evolution cost? |
| **XL Candy Guide** | Which Pokémon need XL Candy and how many? Priority list |
| **Dark/Light Theme** | Light mode option for users who prefer it |
| **League Viability Filter** | Filter Pokémon database by GL/UL/ML suitability |
