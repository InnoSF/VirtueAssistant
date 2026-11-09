# Virtue Assistant 2.7.0.16

Built from 2.7.0.15. One fix and one look change: with the one-panel look on, Social and Pets no longer keep
jumping between two looks, and the gold edges round the Action Bar and Paperdoll slots are thinner. If anything
misbehaves, go back to 2.7.0.15.

## Shard rules (In Mani Ylem)

- These changes only alter how windows are drawn and placed. Nothing is sent to the game and no actions are
  added, so R1-R8 are untouched.

## Fixed

- **Mother script:**
  - With "Join windows in zones into one panel" on, Social in the bottom right corner (and Pets on the right edge)
    kept switching many times a second between its title row showing and its title hidden with the window moved
    up. Each time the window redrew itself, the layout looked at it before the game had finished adding its
    pieces, decided it had no title row, and fitted it the plain way; the next look found the title row and
    fitted it the one-panel way, which made the window redraw again, and round it went. The layout now waits for
    the window's pieces to be in place before it decides, so the window settles after one pass and stays put.
  - A layout pass that can't reach the game's own thread now leaves a joined window as it is instead of undoing
    it for a moment.

## Changed

- **Action Bar:**
  - The gold edges round the slot frames are thin 3 px gold lines instead of the wide bevel, and the gold trim
    between cells is 3 px too (it was up to 5). Cells, buttons and bag slots keep their exact size and place; the
    freed space is the dark fill. They stay gold in Dark mode and never catch a click.
- **Paperdoll:**
  - The item slots have the same thin 3 px gold edge. Each slot keeps its size, place, drop area, click and
    tooltip.

## The review pass

- Rules check R1-R8: no new game action calls. The changes are only about how windows are drawn and placed.
- A fresh review of the diff.
- 467 item tests pass (15 new), with:
  - the mock run, with and without every module;
  - each module run alone;
  - the IronPython 3.4 compile;
  - the undefined-names check and the layout check.
- The new tests rebuild your saved zones on a 2560 x 1080 screen with Social in the bottom right zone, let the
  game add a window's pieces a moment later as it really does, and check that:
  - Social keeps one look over many passes: still, with the mouse going on and off its top edge, redrawn every
    second, and with a pass that can't reach the game's thread (it flipped on 2.7.0.15);
  - every zoned window (Paperdoll, Bags, Pets, Meters, Social, Action Bar) keeps one look, one-panel look on and
    off, Dark mode on and off, still and redrawn every second (Pets flipped too on 2.7.0.15);
  - the Action Bar frames are 3 px gold lines round a dark fill, never tinted and never catching a click, flat and
    upright, light and dark;
  - every frame, cell, button and click area of the Action Bar has the exact place and size it had in 2.7.0.15,
    and the trim between cells is 3 px (or the gap, if smaller) and stays centred;
  - the Paperdoll slots have 3 px gold frames on the same 48 x 48 drop areas.
- A picture drawn from the client's own art (old bevel, 3 px and 2 px; light and dark; three bar sizes, upright,
  and Paperdoll slots) was compared: 3 px is clearly thinner and still clearly gold; 2 px looked faint.

## Install

Copy `VirtueAssistantV2-7-0-16.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, replacing
the whole modules folder, then run the main script. You can delete the 2.7.0.15 main script.

Only in game:
- Social, Pets and the other zoned windows stay still with the one-panel look on, also while the mouse rests on
  them and while Social reads the guild window.
- The 3 px gold lines read well at your Action Bar size, in normal and Dark mode, and on the Paperdoll slots.
- At the smallest bar size the 3 px edge still shows as gold.
- Dragging items onto cells and slots, clicking and right-clicking them work as before.
