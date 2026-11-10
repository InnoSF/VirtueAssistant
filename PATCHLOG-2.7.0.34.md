# Virtue Assistant 2.7.0.34

Built from 2.7.0.33. A tidy-up release: the four most deeply nested pieces of code are laid out flatter, split
into small named steps, so they are easier to read and to fix. Nothing you see or do changes.

## Changed

- **Action Bar:** the cell menu's choices (back, the categories, travel, typed text, hotkey, low count, target,
  clear, settings, bag slots, Bags links) are handled by one table of small steps instead of one long chain.
- **Social:** the window's queued clicks (tabs, pages, notes, Add, invite answers, Diplomacy, war mode) go
  through the module's action tables, and each tab (Friends, Party, Guild, the minimised bar) gathers its own
  list of players in its own step.
- **Mongotchi:** the pet's drawing is split into steps: where it walks to, the pose of each little animation,
  and what it carries. Quests, the shop and loot are untouched.
- **Ultima Tracker:** reading the save file handles each section (foes, ignore, players, settings, anchors,
  layout, sightings, links, last seen) in its own step.

## The review pass

- Rules check R1-R8: no game action added, changed or removed; no saved setting, file format, journal line or
  key changed.
- Same behaviour: before the change, new item tests recorded what each of the four pieces does today (every
  Action Bar menu choice in every menu state, every Social action and tab, over 60 Mongotchi movement, pose and carry
  cases, and save files with every section, bad lines and the old format), passed on 2.7.0.33, and pass
  unchanged on 2.7.0.34. A side-by-side check also ran the old and new code on tens of thousands of random
  inputs and found no difference. All item tests pass.
- Speed: the call counter (every module, 600 passes, two runs on each version) shows no more calls or hops per
  pass than 2.7.0.33. The Social and Mongotchi steps that run every tick build their tables once, at start.
- The IronPython 3.4 compile; the mock run with every module and with clicks; each module run on its own.
- A fresh review of the change.

## Install

Copy `VirtueAssistantV2-7-0-34.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.33
main script. The `readable` folder on the GitHub page is the same code with comments; don't install it.

Only in game:
- Nothing new to check: the Action Bar cell menu, the Social tabs, the Mongotchi pet and the Ultima Tracker
  windows should work as before.

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
