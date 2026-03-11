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
| 1 | **GBL Season Battle Log** | 🔥 High | GO Battle Log | Let users log their daily GBL sets (team used, win/loss, opponent lead). Display a season summary: win rate, rating progress graph, most-faced Pokémon. All data stored in `localStorage` – no account needed. |
| 2 | **Custom Cup / Format Builder** | 🔥 High | PvPoke – Custom Rankings | Allow users to define a custom cup: choose CP cap, restrict or exclude Pokémon families or types, then re-rank the Pokédex entries accordingly. Useful for community tournaments and remote events. |
| 3 | **CMP (Charge Move Priority) Table** | 🟡 Medium | PvPoke – CMP Chart | Add a reference table in the Battle tab showing which Pokémon win CMP ties at common breakpoints. Critical for competitive play where simultaneous charge moves decide the outcome. |
| 4 | **PvP IV Rank Checker** | 🟡 Medium | BattleFlow / pvpivs.com | Extend the Calculator tab with a stat-product rank lookup: given a Pokémon's IV and level, display its rank (#1 = best) and stat product for GL (1500 CP), UL (2500 CP) and ML. Highlight whether the spread is top-100. |
| 5 | **Role-Based Team Analyzer** | 🟢 Low | GamePress / BattleFlow | In the Team Builder tab, automatically classify each Pokémon as *Lead*, *Safe Switch*, or *Closer* based on bulk, fast charge energy, and type coverage. Flag if the team has two leads or no safe switch. |

---

*Last updated: 2026-03-11*
