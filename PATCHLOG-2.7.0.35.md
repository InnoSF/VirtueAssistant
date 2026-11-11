# Virtue Assistant 2.7.0.35

Built from 2.7.0.34. A front-end release: four looks, text size, compact rows, colour-blind marks and a streamer
mode for every window; a search box for Settings, an alert history and a quiet switch, settings backups; layouts
you can share as a code, switch by situation, show as tabs and fade when idle; and four new windows (Ultima Tracker
Overview, Inventory Bag Sections, an Action Bar radial ring and the Quick Launcher). New settings show a "new" tag
until you have seen them.

## Shard rules (In Mani Ylem)

Nothing here acts by itself. Each new way to act is one press for one action, through the same checks as before:

- **Action Bar radial ring:** press and hold the ring key, let go over a cell: that cell runs once, exactly as a
  click on it would (R1: no repeat, no chain; held-key repeats are ignored). A harmful cell aimed at a blue in a
  guard zone still asks for a second press (R6).
- **Quick Launcher:** Enter (or a click on a row) runs that one row once. A rune is one trip through Grimoire's own
  travel queue and is refused while a trip is still pending. A cell is one Action Bar cell run, checked again first
  so a cell changed since the list was made is refused. Enter is never the R6 confirming press; a click on the row
  can be.
- **Inventory Bag Sections:** a double-click on a cell uses that item once; a doubled click still uses it once.
  The part never moves items.
- Situations, tabs, fade, looks, search, history, quiet and backups only change what Virtue Assistant shows or
  saves. While alerts are quiet, an alarm-level alert still counts as an alarm, so skill loops still pause (R3).

## Changed

- **Ultima Tracker:** a new **Overview** part: one window with Players, Monsters, Pets and Corpses tabs (name,
  HP, distance), its own sort, range and row count; Alt+click a row to auto-follow. The Tracker list gains a
  **Sort** button (name, distance, HP). Looks, compact rows, colour-blind marks and streamer names apply
  throughout, including Sightings, Lookout and the killer list.
- **Character HUD:** frames, Pets, Buffs & Timers, the Swing Bar and Bandages take colour-blind ring colours and
  marks (P poisoned, Z paralysed, M mortal wound) and streamer names ("You" for your own frame); compact rows and
  text size shrink frames and timer rows.
- **Inventory:** a new **Bag Sections** part shows what you carry grouped by kind (14 ready-made sections, up to
  12 of your own from a target, and Other), with item pictures and amounts. Storage hides your characters' names
  and chest places in streamer mode. Saved Bags category filters now also work with the filter window closed.
- **Action Bar:** the **radial ring** (Settings > Action Bar, RADIAL RING: pick a key and a page) and a
  **Launcher** cell that opens the Quick Launcher. Compact and text size scale the bar.
- **Grimoire:** runes can be found and travelled to from the Quick Launcher; labels follow the text size.
- **Social, Property Butler, Meters, World Map, Skills, Mongotchi:** streamer mode hides other players, guilds,
  places and coordinates; Social and Property Butler rows take colour-blind marks; compact rows where lists have
  them.
- **Interface:** LOOK section (Look, Text size, Compact, Fade windows when idle with Faded and After, Fade the
  Action Bar and unit frames too), ACCESSIBILITY (Colour-blind marks, Streamer mode). The zone editor's Stack
  button gains **tabs**: the windows of that zone share it, one at a time, with a tab strip on top. LAYOUTS gains
  **Share code** and **Load code**; the new LAYOUTS BY SITUATION section picks a window layout for war mode,
  the bank, dungeons and towns.
- **Main script:** a search box on the Settings and Modules tabs ("<- found" marks the row); "new" tags on new
  settings; Alerts gains **History** (the last 50 alerts, also from the banner) and **Quiet 30 min** / Resume;
  a **Backups** page (Back up now, Restore with two presses; one backup is made by itself the first time a new
  version starts); the **Find** button and hotkey open the **Quick Launcher** (runes, Action Bar cells, windows,
  layouts, settings and commands; Recent lists your last five runs). Alerts are veiled in streamer mode when they
  show. What's new and the docs describe all of the above.

Values to check in game (named constants, easy to change):
- Parchment: frame hue 2960, corner 1260, sections 1845 at 90%. High contrast: frame and corner 1175, sections
  solid.
- Colour-blind hues: innocent 1266, ally 1060, grey and criminal 2958, enemy 1174, murderer 1100, invulnerable
  1568.
- `DUNGEON_AREAS`: Felucca x 5120-6143, y 0-2303 counts as a dungeon. Fire, Ice and perhaps Hythloth and
  Terathan Keep lie past y 2303 and may not switch to the dungeon layout.
- The Launcher cell's picture (0x0E2E, a crystal ball) is a guess.

## The review pass

- Rules check R1-R8: the three new ways to act (radial release, launcher run, Bag Sections double-click) are one
  press for one action through the existing checks (`run_cell` with its R6 confirm, Grimoire's travel queue,
  a 0.6 s once-guard); nothing else acts in game. Saved data only gained new keys and fields at the end:
  2.7.0.34 settings load here, and 2.7.0.35 settings load in 2.7.0.34 (upgrade test passed).
- Every one of the 13 build steps had a fresh review of its own change, its findings fixed before the next
  step, and its own item tests, each first run on the code before the step (where the mock can show it, they
  failed there).
- A bug sweep before release: eight reviewers read every changed function (481) from different angles (settings
  and alerts, zones and layouts, the switches in each module, the new windows, speed, tools). Of 43 points, 33
  were real and fixed, each with a test that fails on the code before the fix, and 10 were ruled out by reading
  the code path. Main fixes: streamer mode also veils alert texts, one "Player" id per player across modules,
  quiet kept per character, the automatic backup taken before settings load, restore clears settings the backup
  lacks, a size cap on loading share codes, tab strips fade with their windows.
- Item tests: 965, 0 failed. The IronPython 3.4 compile, and the mock run under TazUO's own IronPython; the mock
  run with every module, with clicks, with every switch on in many combinations; each module run on its own.
- Speed: the call counter (600 passes, two runs on each version) shows calls and hops per pass level with
  2.7.0.34 when the new features are off.
- Worth knowing, left as is or changed on purpose:
  - the minimised Overview bar reads "Overview: <tab>", without a count that could go stale;
  - streamer mode veils players, not pets or monsters, and journal lines keep real names;
  - alerts raised before streamer mode went on keep their names in the history;
  - an older bug, not fixed in this release: a frame layout saved under the name "list" or "active" overwrites
    the saved list of frame layouts or the one in use.

## Install

Copy `VirtueAssistantV2-7-0-35.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.34
main script. The `readable` folder on the GitHub page is the same code with comments; don't install it.

Only in game:
- the four looks and their hues, text size and compact rows on every window;
- tab strips and fading on screen;
- how the radial ring feels (opening, the highlight, letting go over a cell);
- Enter in the Quick Launcher, and the Find button's fit on the Virtue Assistant window;
- layouts by situation at real town edges, bank visits and dungeon entrances;
- Bag Sections item pictures and amounts.

## Since 2.7.0.25

Everything that changed from 2.7.0.26 to this release, in one place.

- **2.7.0.26:** fixes for features that never worked on today's TazUO, because the game events they listened for
  were asked for under the wrong names. The Swing Bar now times your swings from the swing sounds; Meters counts
  the potions you drink; the Training Alarm's whisper alarm works; Treasure Maps marks a dug-up map done; Property
  Butler checks a mobile that comes into view sooner; the Party buttons of the Action Bar and Social open the
  client's party window.
- **2.7.0.27:** System Stats shows the five busiest Virtue Assistant parts, and a new setting (Show start-up
  times) lists in the journal how long each start-up step took.
- **2.7.0.28:** two start-up safety nets. If a TazUO update breaks something a module reads, the journal says
  which and only that module or part stays off for the session. If Virtue Assistant didn't finish starting last
  time, a SAFE START window offers to start with every module off.
- **2.7.0.29:** the journal warns once when one of TazUO's own helpers is on in a way this shard's rules don't
  allow (auto loot, looting human corpses, scavenger, automatic doors) and says where to switch it off. A System
  Stats setting turns the warnings off.
- **2.7.0.30:** the death recap and your corpse's arrow start the moment you die; Traps & Fields scans as you
  move and less often while you stand still; the corpse search asks the client once instead of ten times.
- **2.7.0.31:** guard zone lines, cast failures, poison, paralysis and bandage results are read by the client's
  message number as well as by their words, so they keep working if the wording changes.
- **2.7.0.32:** Buffs & Timers can also show your Polymorph timer as one of TazUO's own cooldown bars (a setting,
  off by default).
- **2.7.0.33:** tidy-up: a few small pieces of code copied into several modules now live once in the main script.
  Nothing you see changes.
- **2.7.0.34:** tidy-up: the four most deeply nested pieces of code (Action Bar menu, Social, Mongotchi, Ultima
  Tracker save file) are laid out flatter. Nothing you see changes.
- **2.7.0.35:** looks, text size, compact rows, colour-blind marks and streamer mode; Settings search, alert
  history and quiet, backups; share codes, layouts by situation, tabs and fade; Overview, Bag Sections, the
  radial ring and the Quick Launcher.
