# The modules

What each module and part does. A part has its own box under its module's row on the Modules tab and runs only while ticked.

## Action Bar (ActionBarModule.py)

Key "actionbar", On screen. Items, spells, skills and windows.

- A cell holds an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, outfit, text to say, window or runebook destination, each with a hotkey and target. Right-click a cell to set it.
- The 12 bottom-left cells have 12 pages; up to 4 extra rows go above the top row.
- Drop the bar near a corner, edge middle or the centre to anchor it; on the left or right edge it stands upright.
- Keys starts keybind mode; Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap grid.
- Bag slots, Grimoire, Virtue Assistant and Module windows buttons show their window, or fold it into the bar's tray.
- Travel cells go to a runebook destination through Grimoire.
- Thin gold lines (3 px) edge the slot frames and separate the cells, bag slots and window buttons; they stay gold in Dark mode.
- **Radial ring** (RADIAL RING): set a key with Ring key (Backspace clears it). Hold the key and the cells of one page (Ring page: shown, or a page 1-12) open in a radial ring round the mouse; move onto a cell and let go to use it once, as a click would (a harmful cell on a blue in town still asks for a second press). Letting go in the middle, far outside or before moving uses nothing; the ring closes after 10 s.
- A Launcher window cell opens the Quick Launcher, which also finds and runs this bar's cells.

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

Frames: since 2.7.0.37 the frames are built at once when the part starts. When no pictures are kept (the first Play in a client, or after a new version or frame size) a frame starts as a plain stone frame with a plain stone portrait, the same size and place; the frame, ring and portrait pictures are swapped into the same frame as each is drawn (no rebuild, nothing moves). If the frame pictures can't be drawn, it becomes the stone frame. A frame that already has its pictures keeps them while a new frame size is drawn. The frame, ring and portrait pictures are kept in the client between Plays (Python's `sys._VA_ART` remembers which ones, at most 64, plus the last 4 portraits' pixels, keyed by serial, the worn items' pictures and hues, the size and the portrait sliders), so a second Play draws nothing; a portrait that changed is redrawn and swapped into the same frame. A portrait with a picture that couldn't be read is never kept. Pictures for a frame size or ring colour no longer used are dropped when Frames next starts; turning Frames off drops them all (pictures kept at Stop wait in the client, at most 64, until Frames next starts with drawn pictures). While start-up is settling the pictures get 40 ms of the script thread per tick instead of 8 ms.

Buffs & Timers: since 2.7.0.32 its settings page has **Also show Polymorph as a TazUO cooldown bar** (off by default, saved with the part's settings). Ticked, each Polymorph cast on you that Buffs & Timers times also makes one of TazUO's own cooldown bars with the same time left (at TazUO's cooldown bar spot). The bar goes when the row goes: the timer runs out, your body changes back early, the cast failed, you die, you untick the setting, or the part or script stops (a timer still running comes back as a new bar at the next start). The window's own row stays as it is.

## Grimoire (GrimoireModule.py)

Key "grimoire", Your things. Spellbook, runebooks and reagents: cast from your spellbook, travel to any rune by Recall, Gate Travel, Sacred Journey, charge or scroll, star favourite destinations and search every runebook. The Quick Launcher finds its runes too; running one is one trip, refused while another is on its way.

## Interface (InterfaceModule.py)

Key "interface", On screen. Zones, layouts and the one-panel look. On by default.

- Its settings page (Settings > Interface) holds everything about zones, layouts and snapping: Set up, Arrange windows, Edit zones, the look, saved frame and window layouts, the zone of each window, snapping and the grid.
- **Set up** opens a three-step window: a ready-made screen, the zone of each window, the look. It opens by itself once, when no layout has been chosen yet.
- **One panel** (Join windows in zones into one panel): one frame over every zone, no corners or dividing lines, a gold border round the game view; windows drop their frames and title rows (hover a window's top edge for it).
- **LOOK:** Look (Classic, Dark, Parchment, High contrast), Text size, Compact rows and Fade windows when idle (Faded:, After:, and whether the Action Bar and Character HUD > Frames fade too); they stay on with Interface off. ACCESSIBILITY: Colour-blind marks and Streamer mode (see the README).
- The zone editor (Edit zones) adds Split, Join and Apart to the zone tools. Its Stack button also cycles to tabs: the zone shows one window at a time under a strip of tabs (the window's title on each), and the others wait behind it, still running.
- **Share code** and **Load code** (LAYOUTS) pass the layouts in use as a text code; **LAYOUTS BY SITUATION** switches window layouts in war mode, at the bank, in dungeons and in town.
- Windows in zones (2.7.0.12): every window that holds a list or rows draws at its zone's size and shows as many rows as fit; a window too small for its zone keeps its own size and says so once. A window assigned to a zone opens there even if it was closed, and its own buttons don't close it. Windows that can sit in a zone include the Ultima Tracker panel, Supplies (and Supplies Rows), the killer window, Mongotchi's Shop, Playpen, Journeys and Achievements, the Property Butler Log and Skill Bags Results.
- The Paperdoll pairs with a "<zone> bags" zone below it for the bags; an empty bags zone left behind when the Paperdoll moves is removed.
- **Check fit** (Settings > Interface > LAYOUTS) lists every zoned window and whether it fills its zone, plus empty zones and windows assigned but not open. Windows assigned but not open stay in the window lists, marked "(not open)".
- Off: zones stop; every window is free and your own game view comes back. The settings page stays for snapping. Running alone it does nothing (zones need the full Virtue Assistant).

## Inventory (InventoryModule.py)

Key "inventory", Your things. Bags, paperdoll, storage, restock, supplies.

```
   Bags             All your bags in one grid
   Paperdoll        What you wear, and your stats
   Storage          What the containers you opened hold
   Restock          Refills from a chest or bank, on a press
   Supplies         Pack supplies, low counts marked
   Bag Sections     What you carry, grouped by kind
```

Bag Sections shows your backpack's items grouped into sections (REAGENTS, POTIONS and so on), one picture per kind of item with its total. Its settings pick up to 12 sections in all: ready-made ones (14, six ticked at first) and your own, made with "Add from target..." (the item's kind, checked first); Show Other adds a last section for the rest. Double-click a picture to use one of that item, once.

Paperdoll joins the Bags window. Storage re-reads an open container soon after its items change (and every 15 s while it is open); a Name or Forget shows a moment later.

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
- **Playpen:** Share posts your mongotchi as a 64-character code in chat (channel: Settings). Players running Mongotchi pick it up from their journal; up to five visit at once (six with yours). Codes can be pasted by hand. Sharing happens only on a press; the re-share reminder only prints a journal line.
- **Journeys:** treasure hunts to eight places, each with its own finds and two relics; far places take longer and are riskier. Each distinct relic adds 1% to squeaks. Meditating at the eight shrines levels each virtue (0-10), each with its own bonus; all eight at 5 unlock the Avatar title. Trips continue while the module is off.
- **Seasons** (your computer's calendar): Halloween, Winter and New Year items, in the Shop's Seasonal tab only in season.
- **Achievements:** sixteen milestones, each paying squeaks once.
- **Companion** (2500 squeaks): your mongotchi flies behind you in the world (only you see it), reacts to what you do and obeys spoken pet commands ("<name> follow / come / stay / speak / dance / kill / good / sleep / fetch / go home", "all ..." too).

Time passes for the pet only while the module is on, unless "Keep living while the module is off" is ticked.

## Property Butler (PropertyButlerModule.py)

Key "butler", Skills and home. House sweeps, visitors, eject and ban: Detect Hidden on your spot (once, or whenever ready), eject, ban, befriend, lock down and release on a press, and a log of actions and visits.

Visits and the foe alarm count only in your own house: a house is noted as yours when you Release or Friend there (until one is noted, any house counts). Visitor rows keep their place: a row that empties stays blank for 1.5 s, and a press within 1 s of a row changing is refused, so a press never lands on someone else. The Ban... target pick is the confirmation; it needs no second click.

## Reagent Prices (ReagentPricesModule.py)

Key "prices", The world. Reagent prices and a price book: it reads the price and stock of the eight reagents from every buy list you open (it never opens one by itself or buys anything), keeps them per vendor and shop and writes them into a book you pick.

Shops: it starts with 16 shops (Castle British to Yew Abbey). A vendor belongs to the shop it was linked to, else to the nearest known shop within Shop distance (settings NUMBERS), else the window asks "Which shop?" with the first shop not read yet picked; "New shop" in that list adds one. Change links the last vendor read to another shop. A vendor is named as Kara, Vesper (its name, then its shop); until its name is known (it is taken at a read, or when you open another buy list in its shop while it is in your client's world) it shows as Vesper vendor 2 (its place in the order the shop's vendors were first read; a shop's only vendor shows as just the shop name), and a second vendor of the same name in one shop as Kara 2. A vendor that isn't there on two visits at least 1 hour apart (you within 12 tiles of its place, opening another buy list in its shop) is gone: it leaves the window, the best stops and the book, and comes back when it is read again; its history stays. The settings section SHOPS renames (type over a name; it applies when the page closes), removes (with its prices) and adds shops.

View: cheapest shows each reagent's lowest price, its shop and how old it is; a shop with more than one vendor names the vendor. While a buy list is open, each row shows this vendor's price (green when it is cheapest or tied) beside the best of every other vendor, the same shop's others included. View: grid shows a row per vendor (by shop, then the order they were first read; up to 60 rows): the shop on its first row, the vendor, then its price and stock for each reagent: the cheapest of each column green, "-" sold out, "^" or "v" when the price rose or fell since that vendor's read before; the vendor of the open buy list is marked "(here)". A price older than Old after (7 days) shows grey; "Skip old prices for the cheapest" leaves old prices out of the cheapest and the best stops. With a shopping list (settings SHOPPING LIST: how many of each to keep, bags included) each row shows how many to buy, and BEST STOPS shows the three best shops for the list: shops that have every reagent in full come first, cheapest first (buying from the shop's vendors cheapest first); a shop that lacks a reagent says "no ..." and one whose vendors together have too little stock says "short ...", and these rank after complete shops. The journal line after a read and the last-read line name the vendor.

Size: drag a corner to resize the window; its body (text, rows, columns, reagent pictures and sections) scales with it from 60% to 150%, the largest that fits both its width and height, with spare room shared out between the columns and rows; the title row stays as it is. The smallest size is the view at 60%, so every vendor row always shows; a window taller than the screen scrolls. Body text uses the client's smooth font so it can scale, and follows Settings > Interface text size. The size is kept per character (ReagentPrices_size) and applies to both views: a switch keeps it and rescales, growing to the other view's smallest size when needed. In a zone the zone's size is the size.

Buy list (the title-row button, or a key set in the HOTKEYS section) opens the buy list of the nearest reagent vendor within 8 tiles, one per press. Alt+click it to auto-follow that vendor (again to stop).

The book: "Pick book..." in the settings. Page 1 is the cheapest shop for each reagent, page 2 the best stops, pages 3-18 one shop each (the lowest price of its vendors; under the date of the newest read, "2 vendors" when more than one was read); "*" marks an old price. It writes while you have the book open, from your backpack, your open bank box or within 1 tile, and only a book that is blank, titled Reagent Prices or already in its layout; any other book shows Overwrite in the window first. The book holds 16 shops (pages 3-18); with more shops, the extra ones are left out and the journal says how many.

Files, in the VirtueAssistantSettings folder and shared by your characters: ReagentPrices_data.txt (shops, vendors, the newest reads, the last 10 prices of each shop and reagent), ReagentPrices_history.txt (every read of every vendor: the newest 10000, at most 400 per vendor) and ReagentPrices_log.csv (time, shop, reagent, price, stock, vendor, serial: one line per reagent per read, the last 5000 lines), which opens in a spreadsheet.

## Skills (SkillsModule.py)

Key "skills", Skills and home. Skills, training and AFK alarms.

```
   Skills Window    Skills with locks, groups and gains
   Training Alarm   Alarm when staff or a gump needs you
   Skill Bags       A skill on each item in a bag, once
```

Skill Bags pauses while the Training Alarm is raised. It uses only bags in your backpack, and opens a closed bag only on Run (Auto shows it as closed). A custom tool rule runs only on Run and stops at its count. The Training Alarm ignores a gump another module said it was opening, once that module knows the gump's id.

## Social (SocialModule.py)

Key "social", The world. Friends, party, guild and profile, on four tabs: TazUO's friends list, your party, your guild (info, roster, diplomacy) and your character.

## Ultima Tracker (UltimaTrackerModule.py)

Key "ultima", The world. Friends, foes and neutrals near you.

```
   Tracker          Trackers and combat bars
   Lookout          A second client keeps watch
   Overview         Players, monsters, pets, corpses
```

Overview is a window with four tabs (Players, Monsters, Pets, Corpses): one row each with name, health, a bar and distance, up to a set number of rows within a set range (settings LIST). Its Sort: button orders each tab by distance, HP or name (Corpses: distance or name), kept per tab. The Tracker's settings have their own Sort: button (name, distance or HP) for the tracker list. Alt+click a row (not on Corpses) to auto-follow it (again to stop).

## World Map (WorldMapModule.py)

Key "worldmap", The world. Pings, corpse, dig and dry spots, traps, also shown on TazUO's World Map.

```
   Map Pings        Guild pings on your Enhanced Map
   Corpse           Arrow, decay time and Get my things
   Treasure Maps    Dig spots of your decoded maps
   Ore Tracker      Your weight and spots that ran dry
   Traps & Fields   Traps and magic fields recoloured
```

The other parts send their pings through Map Pings. Corpse uses only a corpse named "corpse of <your name>" (or "remains of"); a nameless one waits until you click it once, and Get my things refuses a corpse that isn't yours.

## Alerts (in the main script)

Settings > Alerts. Alert banners and sounds from every module. History (also on the banner) opens the Alert History window: the last 50 alerts with their time, kept across restarts. Quiet 30 min stops banners and sounds for 30 minutes (Resume ends it); alerts still reach the history and journal, and an alarm still pauses skill loops.

## Backups, Hotkeys and What's new (in the main script)

Settings > Backups and Settings > Hotkeys are described in the README. What's new lists what changed in each recent version.

## System Stats (in the main script)

Key "sysstats", On screen. A small button that shows your ping (since 2.7.0.36, as text) and opens a window of ping, FPS, frame time, memory and network traffic. Since 2.7.0.36 the window is 300 px wide, has a Settings button and can be resized like Meters (its size is saved in `SystemStats_size`); the busiest list shows as many rows as fit (5-12). With the window closed it reads the numbers every 2 s instead of every 0.3 s. Since 2.7.0.27 the window also lists the busiest Virtue Assistant parts (a module without parts counts as one): the share of time each spent working over about the last 10 s, and its slowest recent tick in ms. The list is worked out once a second, only while the window is open and not minimised. Its settings page has **Show start-up times** (off by default, saved in the main settings): after start-up, one journal line lists how long each step took (code, data setup, profiles, module files, main window, each module's load, first build). Since 2.7.0.36 it waits until the windows stop changing and prints two lines: that list with the time start-up settled, then a "Settling:" line with the number of window builds and the windows built more than once. Since 2.7.0.37 a third line, "Splits:", says where the time went: reading, compiling (and how many modules came from the compile cache) and running the module files, the number of start-up hops with the longest one and the controls it made, and when the Character HUD frames got their pictures. On the first Play after starting the client, the next module compiles while the one before it starts, so the first windows appear sooner; each module's load time in the first line then leaves out the compile that ran during a start, and "compile" in the Splits line still counts it. It also settles after 0.25 s of quiet instead of 0.5 s, unless a window said it is still waiting (then 0.5 s). Since 2.7.0.29 it also has **Don't warn me about TazUO settings** (off by default, saved in the main settings). Unticked, Virtue Assistant reads TazUO's own settings at start, after a profile load and once a minute, and prints one journal line per setting per session when one would break the shard's rules: Enable Auto Loot (R2), Auto Loot Human Corpses while auto loot is on (R6), Enable Scavenger with items in its list (R2). Since 2.7.0.36 it no longer warns about Automatically open doors: the shard turns doors off itself. It never changes a TazUO setting.

TazUO has its own profiler (the top bar: More + > Developer > Profiler) and an equipment durability tracker (the modern paperdoll's menu: Durability Tracker); System Stats doesn't copy them.
