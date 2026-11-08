# The modules

What each module and part does. A part has its own box under its module's row on the Modules tab and runs only while ticked.

## Action Bar (ActionBarModule.py)

Key "actionbar", On screen. Cells for items, spells, skills and windows.

- A cell holds an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, outfit, text to say, window or runebook destination, each with a hotkey and target. Right-click a cell to set it.
- The 12 bottom-left cells have 12 pages; up to 4 extra rows go above the top row.
- Drop the bar near a corner, edge middle or the centre to anchor it; on the left or right edge it stands upright.
- Keys starts keybind mode; Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap grid.
- Bag slots, Grimoire, Virtue Assistant and Module windows buttons show their window, or fold it into the bar's tray.
- Travel cells go to a runebook destination through Grimoire.

## Character HUD (CharacterHudModule.py)

Key "hud", On screen. Frames, timers and bars for you and pets.

```
   Frames           Health frames: you, target, party (with a cast bar)
   Buffs & Timers   Timed buffs, debuffs and your spells
   Swing Bar        When your next melee swing lands
   Bandages         One-press bandage, timer and alerts
   Pets             Pets' health, distance and commands
```

Bandages never bandages by itself: one press, one bandage (shard rules).

## Grimoire (GrimoireModule.py)

Key "grimoire", Your things. Spellbook, runebooks and reagents: cast from your spellbook, travel to any rune by Recall, Gate Travel, charge or scroll, star favourite destinations and search every runebook.

## Inventory (InventoryModule.py)

Key "inventory", Your things. Bags, paperdoll, storage, restock, supplies.

```
   Bags             All your bags in one grid
   Paperdoll        What you wear, and your stats
   Storage          What the containers you opened hold
   Restock          Refills from a chest or bank, on a press
   Supplies         Pack supplies, low counts marked
```

Paperdoll joins the Bags window.

## Meters (MetersModule.py)

Key "meters", Extras. Damage, healing, loot and gold meters, per fight or session.

- **Displays:**
  - COMBAT: Damage done, Damage taken, All damage nearby, Biggest hits, Kills, Deaths.
  - HEALING: Healing done, Healing received, Healing by method, Cures, Poisonings.
  - MAGIC & ITEMS: Spells cast, Mana spent, Consumables, Buffs & debuffs.
  - ECONOMY & PROGRESS: Gold, Gold by place, Items gained, Skill gains, Stat gains, Fame & karma, Travel, Session summary.
- **Segments:** Current (this or the last fight), Overall (since start or reset) and earlier fights. A fight starts with the first damage dealt or taken and ends after a set quiet time.
- **Windows:** open more meter windows, each with its own display and segment. Drag a corner to resize; in a zone a window takes the zone's size. The first window's X turns Meters off.
- Click a row for details; Alt+click a mobile's row to auto-follow it (again to stop).
- **Report** posts the top rows to party chat (if set and in a party), else your journal.
- **Gold by place:** gold per hour by guarded town, a spot you named ("Name this spot"), or Elsewhere.
- **Last-hour graph:** one bar per minute under the rows.
- **Export** writes a segment to `Meters_<serial>.txt` in VirtueAssistantSettings.
- **Death recap:** the last seconds of damage taken when you die.

How it counts:
- Damage numbers are the client's own (the numbers over heads).
- Your damage: damage on a mobile you attacked or recently targeted, so your pets' damage on your target counts as yours.
- Damage taken, healing, cures and deaths are watched for you, your party, your pets and your TazUO friends. Pets' and strangers' HP comes as a percentage, so their healing shows as a "(%)" row.
- Your healing: an HP rise right after your bandage, heal spell or heal potion; rises below the regeneration limit are ignored.
- Items gained and reagents used come from your backpack (open it once after login).

## Mongotchi (MongotchiModule.py)

Key "mongotchi", Extras. A pet mongbat to raise and dress up.

- **Care:** feed it, play, brush, clean the pen, put it to bed (Lights), cure it, send it foraging; click it to pet it. Its mood is a UO loyalty level. It grows from pup to mongotchi to Greater Mongotchi when well cared for; neglected, it goes wild.
- **Gremlins** steal half your food; click one before it reaches the pantry to swat it.
- **Squeaks** come from care and trickle in at 30 an hour, even while off (up to a day's worth). Spend them in the Shop on treats, clothes, dyes, auras, toys, decor, titles, voices and upgrades.
- **Playpen:** Share posts your mongotchi as a 64-character code in chat (channel: Settings). Players running Mongotchi pick it up from their journal; up to six visit at once. Codes can be pasted by hand. Sharing happens only on a press; the re-share reminder only prints a journal line.
- **Journeys:** treasure hunts to eight places, each with its own finds and two relics; far places take longer and are riskier. Each distinct relic adds 1% to squeaks. Meditating at the eight shrines levels each virtue (0-10), each with its own bonus; all eight at 5 unlock the Avatar title. Trips continue while the module is off.
- **Seasons** (your computer's calendar): Halloween, Winter and New Year items, in the Shop's Seasonal tab only in season.
- **Achievements:** sixteen milestones, each paying squeaks once.
- **Companion** (2500 squeaks): your mongotchi flies behind you in the world (only you see it), reacts to what you do and obeys spoken pet commands ("<name> follow / come / stay / speak / dance / kill / good / sleep / fetch / go home", "all ..." too).

Time passes for the pet only while the module is on, unless "Keep living while the module is off" is ticked.

## Property Butler (PropertyButlerModule.py)

Key "butler", Skills and home. House sweeps, visitors, eject and ban: Detect Hidden on your spot (once, or whenever ready), eject, ban, befriend, lock down and release on a press, and a log of actions and visits.

## Skills (SkillsModule.py)

Key "skills", Skills and home. Skills, training and AFK alarms.

```
   Skills Window    Skills with locks, groups and gains
   Training Alarm   Alarm when staff or a gump needs you
   Skill Bags       A skill on each item in a bag, once
```

Skill Bags pauses while the Training Alarm is raised.

## Social (SocialModule.py)

Key "social", The world. Friends, party, guild and profile, on four tabs: TazUO's friends list, your party, your guild (info, roster, diplomacy) and your character.

## Ultima Tracker (UltimaTrackerModule.py)

Key "ultima", The world. Friends, foes and neutrals near you.

```
   Tracker          Trackers and combat bars
   Lookout          A second client keeps watch
```

## World Map (WorldMapModule.py)

Key "worldmap", The world. Pings, corpse, dig and dry spots, traps, also shown on TazUO's World Map.

```
   Map Pings        Guild pings on your Enhanced Map
   Corpse           Arrow, decay time and Get my things
   Treasure Maps    Dig spots of your decoded maps
   Ore Tracker      Your weight and spots that ran dry
   Traps & Fields   Traps and magic fields recoloured
```

The other parts send their pings through Map Pings.
