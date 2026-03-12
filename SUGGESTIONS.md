# 🗒️ Open Feature Suggestions

This file lists features that have been **researched and proposed** but are **not yet implemented**.
Completed features are tracked in the [README](README.md).

---

## Research Basis

The following five Pokémon GO community sites were reviewed and compared against the current app to identify gaps and opportunities for improvement:

| # | Site | URL | Key Strengths |
|---|------|-----|---------------|
| 1 | **PvPoke** | https://pvpoke.com | Custom cups, CMP chart, multi-battle matrix |
| 2 | **GamePress Pokémon GO Wiki** | https://pogoold.gamepress.gg | Attacker tier lists, role-based analysis (lead / safe-switch / closer) |
| 3 | **GO Battle Log** | https://gobattlelog.com | Battle history logging, personal win/loss statistics, ELO tracking |
| 4 | **BattleFlow** | https://battleflow.app | Pokémon box importer, match-up threat matrix, IV stat product |
| 5 | **Pokémon GO Hub** | https://pokemongohub.net | Meta-shift news, season previews, move-update coverage |

---

## Planned / Open Items

### From previous README roadmap

| Feature | Priority | Notes |
|---|---|---|
| **Multilingual Support** | 🔜 Medium | EN/DE language toggle – all UI strings, tab labels and help texts |

---

### New Suggestions (based on site comparison)

| # | Feature | Priority | Inspiration | Description |
|---|---------|----------|-------------|-------------|
| 1 | **GBL Season Battle Log** ✅ *Implemented* | 🔥 High | GO Battle Log | Log daily GBL sets, win/loss tracking per season, rating history, CSV export. All data in `localStorage`. |
| 2 | **Custom Cup / Format Builder** | 🔥 High | PvPoke – Custom Rankings | Allow users to define a custom cup: choose CP cap, restrict or exclude Pokémon families or types, then re-rank the Pokédex entries accordingly. Useful for community tournaments and remote events. |
| 3 | **CMP (Charge Move Priority) Table** | 🟡 Medium | PvPoke – CMP Chart | Add a reference table in the Battle tab showing which Pokémon win CMP ties at common breakpoints. Critical for competitive play where simultaneous charge moves decide the outcome. |
| 4 | **PvP IV Rank Checker** ✅ *Implemented* | 🟡 Medium | BattleFlow / pvpivs.com | Stat-product rank lookup for GL / UL / ML given any Pokémon's IVs. Shows rank #N/4096, stat product, best level, CP, and percentile. Covers 600+ Pokémon including regional forms. |
| 5 | **Role-Based Team Analyzer** | 🟢 Low | GamePress / BattleFlow | In the Team Builder tab, automatically classify each Pokémon as *Lead*, *Safe Switch*, or *Closer* based on bulk, fast charge energy, and type coverage. Flag if the team has two leads or no safe switch. |
| 6 | **Community Spawn Map** ✅ *Implemented* | 🔥 High | Silph Road Atlas / community reports | A Leaflet.js map where players manually mark Pokémon spawn points they've personally observed. Points are stored in `localStorage`. Each marker holds Pokémon name, spawn category (Normal / Nest / Biome / Event), optional note, and GPS coordinates. Users can export/import their data as JSON to share with others. No game API access required – fully community-driven and ToS-compliant. |

---

## What Data Can Be Read From Pokémon GO Legitimately?

Niantic's Terms of Service forbid automated reading of the game client or its API. The table below summarises **what is and is not permitted**:

| Data Type | Legitimate? | Method |
|-----------|-------------|--------|
| Pokémon species stats (base ATK/DEF/HP) | ✅ Yes | Published in official Game Master files leaked/datamined and re-published by the community; also on fan wikis |
| Move data (power, energy, duration) | ✅ Yes | Same as above – static data freely available from GAME_MASTER |
| Type effectiveness chart | ✅ Yes | Fixed chart from Niantic's help pages and fan wikis |
| CP formula, IV mechanics | ✅ Yes | Reverse-engineered and officially acknowledged in Niantic blog posts |
| Current wild spawns (your local area) | ✅ Yes | **Self-observed** and manually entered; crowd-sourced community reports |
| PokéStop / Gym locations | ✅ Yes | OpenStreetMap / Wayfarer contributions made public by the community |
| Event schedules & bonuses | ✅ Yes | Officially announced on pokemongolive.com and Niantic Newsroom |
| Raid boss rotations | ✅ Yes | Officially announced + community confirmed (no scraping needed) |
| Weather boost types | ✅ Yes | Static type→weather map, published by Niantic |
| GBL season schedule & rewards | ✅ Yes | Officially published on pokemongolive.com |
| Buddy candy distances | ✅ Yes | Published by Niantic and well-known fan wikis |
| Real-time Pokémon positions via game API | ❌ No | Violates ToS – requires reverse-engineering the live API |
| Automated location spoofing / bot scanning | ❌ No | Explicitly banned; risks permanent account ban |
| Injecting / modifying the game client | ❌ No | Violates ToS and potentially local laws |

### Summary for This App
All data currently used in this app (Pokémon stats, move data, type chart, event information) comes from **static, publicly-available community sources** and is **not** obtained by querying the live Niantic API. The new Spawn Map feature uses **only user-entered coordinates** – no automated game scanning of any kind.

---

*Last updated: 2026-03-11*
