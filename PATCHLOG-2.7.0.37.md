# Virtue Assistant 2.7.0.37

Built from 2.7.0.36. A speed release: start-up does less work, above all on a second Play in the same client
session, and the health frames show at once instead of waiting for their art. It also brings a new module,
Reagent Prices (The world), and "Show start-up times" gains a "Splits:" line that says where the start-up time
went.

## Shard rules (In Mani Ylem)

The speed work adds no way to act: it only changes how Virtue Assistant starts and what it keeps in memory
between Plays. Reagent Prices acts in game in one way by itself: it writes the book you picked, while you have
it open. The vendor's buy list opens only on a press of its button or hotkey, one menu per press. Nothing buys,
hands over gold (R7), travels or repeats by itself (R1-R3). Follow is the shared Alt+click toggle (R5).

## Start-up readings of 2.7.0.36 in game

With "Show start-up times" on:

| Play | start-up | code | data setup | profiles | module files | main window | modules | first build | settled |
|---|---|---|---|---|---|---|---|---|---|
| cold (first after starting the client) | 2.2 s | 13 ms | 74 ms | 42 ms | 63 ms | 315 ms | ~392 ms | 1336 ms | 5.2 s |
| warm (second Play) | 0.9 s | 7 ms | 4 ms | 7 ms | 85 ms | 162 ms | ~53 ms | 600 ms | 3.3 s |

Both said "Settling: 13 window builds." (nothing built twice, the main window not built). These are what this
release works on: the time before the first window, the long first build, and the wait until settled.

## Measured start-up

Counted in the test run (a mock client, not the game) with the boot counter: 2.7.0.36 before, 2.7.0.37 after,
one Play and then a second Play in the same session. "Settled" is when start-up as a whole is done (every window
built and quiet); the times are mock times, not game times. 2.7.0.37 also starts Reagent Prices, one module more.

- **Every module on**, first Play: settled at pass 74, 2.05 s before; pass 51, **1.80 s** after. 18 window
  builds both. Controls created until settled 2693 / 2710 (Reagent Prices' window).
- **Every module on**, second Play: settled at pass 70, 1.14 s before; pass 48, **0.68 s** after. Width and
  picture probes 47 / 1 instead of 317 / 25 on the first Play (only windows the first Play never built still
  measure their text).
- **A saved character** (that character's own modules and layout), first Play: settled at pass 56, 2.55 s
  before; pass 33, **1.51 s** after. Window builds 12 / 11 (Buffs & Timers finds its frame at once).
- **A saved character**, second Play: settled at pass 55, 1.78 s before; pass 33, **0.54 s** after. Text and
  picture probes 254 / 56 on the first Play, **0 / 0** on the second; controls created 1984 / 1699.

The mock can't show the real cold-start gain from compiling and building at the same time, the client calls no
longer made, or the frame timing: your own "Show start-up times" readings are the real measure.

## New: Reagent Prices (The world)

- Open a reagent vendor's buy list and the module reads its prices and stock. It remembers them per shop (16
  shops listed, plus "New shop") and knows the shop again from the vendor or where you stand. It asks "Which
  shop?" once when it can't tell; while that question is open it still reads the buy lists of shops it knows.
- The window shows the cheapest shop for each reagent. With a list open, it shows this vendor's prices against
  the best elsewhere. A grid view shows every shop at once. Prices older than 7 days show grey. The window is
  built once, with your saved prices already in it.
- Shopping list: set how many of each you want to keep. It counts your backpack when a buy list opens, shows what
  to buy and the cost here against the cheapest shops, and ranks the best three stops.
- A price book: pick a book once in the settings. While you have it open, in your backpack, within 1 tile or in
  your open bank box, the module writes the prices into it (page 1 cheapest, page 2 best stops, then one page per
  shop). It writes freely only into a blank book, one titled "Reagent Prices" or one it wrote before. Any other
  book needs an "Overwrite" press. The book holds 16 shops; when you know more, the journal says how many are
  left out.
- "Buy list" button and hotkey: opens the buy list of the nearest reagent vendor within 8 tiles. Alt+click it to
  auto-follow that vendor (again to stop).
- A price log `ReagentPrices_log.csv` (last 5000 lines) in the settings folder, for a spreadsheet.

## Changed

- **Character HUD:** the health frames show at once. A frame starts with the portrait and art kept from the Play
  before (or a plain stone frame and portrait when there is none, as on the first Play after starting the client)
  and the real art is swapped into the same place when it is ready: no rebuild, no move, no flash. The frame, ring
  and portrait pictures are kept in the client between Plays, so a second Play draws nothing again; when you turn
  on Legion's "Disable module cache", nothing is kept and leftover pictures are cleared at the next start.
  Pictures are drawn in larger slices while starting, so they are ready sooner.
- **Mongotchi, World Map (Map Pings), Ultima Tracker:** they no longer load Python's slow `random`, `socket` and
  `threading` libraries while starting (about half a second in a fresh client); they use the small built-in parts
  of them instead. Nothing you see changes.
- **Main script:**
  - On a second Play the main script runs the compiled copy of itself it kept from the Play before, instead of the
    copy the Script Manager just compiled. Any change to the file compiles it again; the Script Manager's "Disable
    module cache" turns this off.
  - Text widths, picture sizes and the client's own parts it looks up are measured once per client session and
    kept, so a second Play measures nothing again. A failed measurement is not kept and is tried again.
  - Module files are read faster (in one piece), once per Play.
  - The main window, the Ultima Tracker window, the zone plan, the "running" line and What's new are set up in one
    step on the client instead of about twenty.
  - On the first Play after starting the client, the first modules start while the rest are still compiling,
    instead of after all of them. If anything goes wrong with that, it falls back to the 2.7.0.36 order by itself.
  - Start-up counts as settled after a quarter second without a window change (half a second while a window still
    waits for something, such as frame art).
  - A Stop pressed while a module is starting no longer switches that module off for the next Play.
  - "Show start-up times" adds a third line, `Splits: read N ms, compiled N ms (N cached), set up N ms; started
    in N steps (longest N ms, N controls); Character HUD ready at N s.`:
    - **read:** reading the module files from disk;
    - **compiled:** turning them into code, and how many came from the compile cache instead (on a second Play
      every module should be cached and this should be near 0);
    - **set up:** running each module file so its parts exist;
    - **started in N steps:** the steps on the client that build the windows; the longest one is the hitch you
      may feel, with how many window controls it made;
    - **... ready at:** when a module's own picture work was done (Character HUD: the frames with their art),
      counted from the press of Play.

## The review pass

- Rules check R1-R8: the speed work adds no action. Reagent Prices' only new action calls are the buy-list menu
  on your press and the book pages, written only into the book you picked while it is open (see above). Saved
  data gains the Reagent Prices keys and drops none, so settings carry over both ways between 2.7.0.36 and
  2.7.0.37.
- Each build step had a fresh review of its own change, its findings fixed, each with a test that fails on the
  code before the fix (where the mock can show it). Two ideas were measured and dropped: fewer controls in the
  Action Bar and Skills (it would not have looked the same) and a few small client passes that saved nothing.
- Reagent Prices had its own review for each of its four build steps; 20 findings fixed, each with a test that
  failed first, among them a player titled "Mage" picked as the vendor, Follow running on after the module
  stopped, a held hotkey counted more than once and an "Overwrite" press that never expired.
- A bug sweep before release: five reviewers read the changed code from different angles (the start path and
  threads, the main script, the frames, the tools, Reagent Prices). Fixed, each with a failing test first: a Stop
  during start-up switching a module off; the kept self-copy dropped on a Stop; a failed client lookup kept for
  good; frame pictures left behind in the client with "Disable module cache" on or after an upgrade; Reagent
  Prices building its window twice, a "Which shop?" question holding up other buy lists, a book in the bank called
  "too far away" and shops past the book's 16 left out without a word. The "Splits:" line was put in plain words.
  Five other points were ruled out by reading the code path; Reagent Prices' 3-second wait for the vendor's
  menu was left as it is (it runs on the script's own thread, as the Action Bar's does).
- **A start-up shortcut taken back:** one step replaced Python's `os` library on the start path with the small
  Windows-only part it is built on, to save about 0.2 s on a cold Play. The sweep found that TazUO on Linux and
  macOS names that part differently, so Virtue Assistant would not start there at all. The main script loads the
  real `os` again; the other library changes above work on every system and stay.
- Item tests: 1297, 0 failed. The IronPython 3.4 compile under TazUO's own IronPython; the mock run with every
  module, with a saved character and with clicks; each changed module run on its own; the call counter shows
  calls and hops per pass level with 2.7.0.36; the boot counter for one and two Plays.

## Install

Copy `VirtueAssistantV2-7-0-37.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.36
main script. The `readable` folder on the GitHub page is the same code with comments; don't install it.

Worth knowing:
- The first Play after starting the client keeps nothing from before; the second Play in the same client session
  is where most of the gain shows.
- The Script Manager's "Disable module cache" toggle turns every kept copy off (compiled code, measurements and
  frame pictures): every Play then starts afresh.

Only in game:
- the real start-up times on a cold and a warm Play: turn on "Show start-up times" (Settings > System Stats) and
  compare its lines, the "Splits:" line among them, with the readings above;
- the health frames showing at once, the plain stone frame on the first Play and the art swapping in without a
  move or flash; the frame pictures still right after a Stop and Play;
- the first windows appearing while the rest still compile, on the first Play;
- a Stop pressed in the middle of start-up, and the modules still on at the next Play;
- frame pictures cleared from the client with "Disable module cache" on;
- Reagent Prices: the shard's buy lists and their prices, the "Buy" menu text and its range, vendor titles, the
  book pages and header as the server takes them and how they look, the window's and grid's column widths, and
  whether prices change at each restock.

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
