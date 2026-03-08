# Pokémon GO PvP Berater

Ein browserbasierter Pokémon GO PvP-Berater mit Attacken-Datenbank, Pokémon-Datenbank, Typ-Übersicht, auswählbaren Meta-Teams und Liga-Ranglisten.

## Features

- **⚡ Attacken-Datenbank** – Alle Schnell- und Ladeattacken mit PvE- und PvP-Werten, durchsuch- und sortierbar
- **🎯 Pokémon-Datenbank** – Pokédex-Einträge mit Typen, besten PvP-Movesets und Generationsfilter (Gen I–IX)
- **🔮 Typ-Übersicht** – Vollständige Typ-Stärken- und Schwächentabelle für alle 18 Typen mit Pokémon GO Multiplikatoren
- **🏆 Meta-Teams** – Auswählbare Top-Teams für Superliga, Hyperliga und Meisterliga mit Synergie-Analyse und Strategie-Tipps
- **📊 Liga-Rangliste** – S/A/B-Tier-Liste der besten Pokémon für alle drei Ligen

## Verwendung

Die App besteht aus einer einzigen HTML-Datei und benötigt keine Installation.

1. [`pokemon-go-berater.html`](pokemon-go-berater.html) herunterladen
2. Datei im Browser öffnen (z. B. per Doppelklick)
3. Fertig – keine Serverinstallation nötig

## Technologie

- Reines HTML, CSS und JavaScript (keine externen Frameworks)
- Sprites werden live von der [PokéAPI](https://pokeapi.co/) geladen
- Schriften: [Bangers](https://fonts.google.com/specimen/Bangers) & [DM Sans](https://fonts.google.com/specimen/DM+Sans) via Google Fonts

---

## 💡 Mögliche Verbesserungen (basierend auf führenden Pokémon GO Seiten)

Die folgenden Funktionen wären wertvolle Ergänzungen, inspiriert von [PVPoke](https://pvpoke.com), [GamePress](https://gamepress.gg/pokemongo), [GO Hub](https://pokemongohub.net), [Silph Road](https://thesilpharena.com) und [PokeGenie](https://pokegenie.net):

### Hohe Priorität

| Feature | Beschreibung | Vorbild |
|---|---|---|
| **IV-Rechner** | Optimale IVs für jede CP-Grenze berechnen (z. B. 0/15/15 für GL) – inkl. Rang-Anzeige | PVPoke, PokeGenie |
| **Battle Simulator** | 1v1 Matchup-Simulation zwischen zwei Pokémon mit Shield-Szenarien (0/0, 1/1, 2/2) | PVPoke |
| **CP-Rechner** | CP-Berechnung bei beliebigem Level und beliebigen IVs | PokeGenie, Calcy IV |
| **Shadow Pokémon Guide** | Vergleich Shadow vs. normal vs. Purified – wann lohnt sich Shadow? | GamePress, GO Hub |
| **Automatische Meta-Updates** | Liga-Ranglisten via PVPoke-API automatisch aktualisieren statt manuell pflegen | PVPoke |

### Mittlere Priorität

| Feature | Beschreibung | Vorbild |
|---|---|---|
| **Raid Counter** | Beste Konter für aktuelle Raid-Bosse mit DPS/TDO-Werten | GamePress, Pokebattler |
| **Mega Evolution Guide** | Welche Mega-Entwicklung lohnt sich für Raids und PvP? | GamePress |
| **Team-Builder** | Eigenes Team aus der Pokémon-Datenbank zusammenstellen und Synergie prüfen | PVPoke |
| **Buddy-Optimierung** | Welche Pokémon als Buddy am meisten Candy bringen (CP-Kosten vs. Nutzen) | GO Hub |
| **Seasons-Tracker** | Tracking von GBL-Saisonänderungen und Meta-Verschiebungen | Silph Road |

### Weitere Ideen

| Feature | Beschreibung |
|---|---|
| **Fangwahrscheinlichkeits-Rechner** | Beste Bälle, Beeren und Medallien für schwierige Fänge |
| **Turnier-Bracket-Generator** | Eigene Turniere erstellen und Ergebnisse verfolgen |
| **Buddy-Herzchen-Tracker** | Tages- und Wochenziele für Buddy-Herzen verfolgen |
| **Move-Vergleich (Elite TM)** | Lohnt sich ein Elite TM für ein bestimmtes Pokémon? |
| **Offline-Modus / PWA** | App als Progressive Web App installierbar machen (kein Browser nötig) |
| **Mehrsprachigkeit** | Englische Übersetzung für internationale Nutzer |
| **Pokémon-Kosten-Rechner** | Wie viel Sternenstaub und Bonbons kostet eine vollständige Entwicklung? |
| **XL-Candy Guide** | Welche Pokémon brauchen XL-Candy und wie viele? Priorisierungsliste |
| **Dunkle/Helle Theme** | Light Mode Option für Nutzer die kein dunkles Theme bevorzugen |
| **Filter nach Liga-Viabilität** | Pokémon-Datenbank nach GL/UL/ML-Tauglichkeit filtern |
