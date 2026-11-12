# Virtue Assistant 2.7.0.38

Built from 2.7.0.37. Reagent Prices now keeps every vendor by name instead of one price list per shop, starts a
long price history, and its window can be resized, with text that scales with it. Nothing else changes.

## Shard rules (In Mani Ylem)

Nothing new acts in game. Prices are still read only from a buy list you opened; the Buy list button stays one
press, one menu, as in 2.7.0.37. The gone check and the name fill only read the client's own list of mobiles near
you. Nothing buys, hands over gold (R7), travels or repeats by itself (R1-R3). Follow stays the shared Alt+click
toggle (R5).

## Changed

- **Reagent Prices:**
  - Every vendor is kept on its own, by name, as `Kara, Vesper` wherever it is named (the window, best elsewhere,
    the last-read line and the journal). A vendor it hasn't read since this release, or whose name it can't see
    yet, shows as `Vesper vendor 2` until it does; two vendors of one shop with the same name show as `Kara 2`.
    A name also fills in when you open another buy list in that vendor's shop while it is near you.
  - The grid has one row per vendor: Shop (on a shop's first row), Vendor, then the 8 reagents, each with its own
    up and down arrows.
  - Best stops buy each reagent from a shop's vendors cheapest first, so "short" means all its vendors together
    lack the stock.
  - A vendor missed on 2 visits at least 1 hour apart (you within 12 tiles of its spot, the vendor not there)
    counts as gone: it leaves the window, best stops and book. Its history stays, and it comes back the next time
    you read it.
  - A new file, `ReagentPrices_history.txt` in the settings folder, keeps every read (the last 10,000, at most 400
    per vendor), shared by your characters. It loads after start-up has settled. The reads you already have are
    filled in from your saved prices.
  - The price log `ReagentPrices_log.csv` gains two columns at the end: `vendor,serial`.
  - The book keeps its pages; each shop's read line is now `Read 12 Nov 14:05`, with `2 vendors` on the line
    below when more than one vendor was read.
  - The window resizes: drag its corner. The text, rows and columns scale with it (60% to 150%), in every view, in
    and out of a zone. The size is kept per character; with no saved size it opens at the size it had before. The
    title row, buttons, the drop-down and the name field keep their size. The window's text uses the client's
    smooth font so it can scale and follows Settings > Interface text size; below about 90% its rows sit closer
    than other windows' rows.
  - Saved prices carry over both ways: 2.7.0.37 loads what this release saves, and the other way round.

## The review pass

- Rules check R1-R8: no new action call; the only new client reads are the vendor's name and whether it is still
  in the client's mobile list.
- Built in three steps (saved data and history, the per-vendor views, the scaled window). Each step had a fresh
  review of its own change, and its findings were fixed, each with a test that fails on the code before the fix:
  a history write landing in the middle of a read counted that read twice; the history fill now copies the old
  lines before going through them; a text width the client reports as 0 is no longer kept; the scale is picked
  again until the width fits; a saved size bigger than the screen is held to the screen.
- Tests added: 20, 20 and 16 (one file per step). Older checks that tested the one-row-per-shop grid or the old
  line format on purpose now run only on the old code, each with a new check in its place.
- Release checks: the IronPython 3.4 compile under TazUO's own IronPython, the mock run with every module and
  with a saved character, every module run on its own, the start-up counter in four modes, the call counter
  (calls per pass level with 2.7.0.37), the item tests (1342, 0 failed), and the checks of the installed and
  readable copies and the release zip.

## Install

Copy `VirtueAssistantV2-7-0-38.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.37
main script. The `readable` folder on the GitHub page is the same code with comments; don't install it.

Only in game:
- the vendors' names as the client gives them (a plain name, or with a title), the names filled in at other buy
  lists, and how far away the client still sees a vendor;
- whether the gone check's 12 tiles fit the shops, and that it never marks a vendor gone wrongly;
- the grid's width with real names, and any flicker when a list opens in grid view;
- how the smooth text, its colours and its centring look in each look at 60% and 150%, also with Settings >
  Interface text size at 150%;
- how the resize corner feels, that a drag settles once, and how long a rebuild at a new size takes;
- two characters sharing the history file, and how long writing a full history takes.

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
- **2.7.0.36:** start-up builds every window once, in place, and settles sooner; the 22 start-up fixes; the
  System Stats ping button and resizable window; compiled modules kept between Plays.
- **2.7.0.37:** a faster start-up, most of all on a second Play; health frames shown at once; the "Splits:" line;
  the new Reagent Prices module.
- **2.7.0.38:** Reagent Prices keeps every vendor by name, keeps a price history and has a resizable, scaled
  window.
