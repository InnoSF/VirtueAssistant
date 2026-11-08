# Virtue Assistant 2.6.103

Built from 2.6.102. Fixes from a third bug pass (shard rules, saved data, window and text rules,
start and stop).

## Shard rules (In Mani Ylem)

- **Action Bar (R6):** a Stealing (or Snooping, Discordance, Provocation) cell aimed at the last
  target now also asks for the confirming second press in a guard zone when that last target is
  an item, not a mobile (stealing from a pack).
- **Action Bar (R6):** a harmful cell now aims at the target that was checked when you pressed it.
  Before, clicking a blue's frame or bar during the cast changed the last target and the cursor
  landed on the blue with no confirm.
- **Property Butler (R8):** Ban's confirming second click no longer accepts a double-click; the
  second click must come at least 0.3 s after the first.

## Fixed

### Windows in a zone stay up
- **Grimoire:** in a zone, double-clicking its title and the Action Bar's Grimoire cell can no
  longer minimise or fold it.
- **Ultima Tracker:** category windows and Combat Bars in a zone no longer minimise on a title
  double-click.

### Character HUD
- **Frames:** a frame snapped beside another near the screen edge is kept wholly on screen.

### Inventory
- **Paperdoll:** stopping while it waits for the player, or while it is folded into the tray, no
  longer saves the wrong minimised state.

### World Map
- **Map Pings:** the wheel-drag guide uses Virtue Assistant's window rules and colours.

### Virtue Assistant
- Loading a profile, or running a module alone, loads button hotkeys before the windows are
  built, so their tooltips show the key at once.
- System Stats shows its full tooltip again after being turned off and on.
- Tooltips no longer end with a full stop (title strips, Character HUD follow hints, Skills,
  Mongotchi, Bags); Corpse's settings say "minimized" like everything else.

## The review pass

- **Rules check:** the only changes to actions are the confirms above (R6, R8). Nothing new is
  automated.
- **Checked:** each finding checked against the code before it was fixed; a fresh review of every
  changed line (it found that the Action Bar zone fix and a Grimoire start-up fix had side effects;
  both were taken out and left for a fuller fix); every file compiles in real IronPython 3.4 with no errors and is plain ASCII;
  names checked; no saved key or format changed.
- **Tests run (on a mock client, not in game):** full suite: no errors; about 1,900 random
  clicks: no errors; every module alone: no errors; item tests: 79, all pass.
- **Left for the owner:** see `DIRECTIONS-owner-decisions.md`.

## Install

Copy `VirtueAssistantV2-6-103.py` and the `VirtueAssistantModules` folder (with `_WhatsNew.py` and
`_Alone.py` in it) into `TazUO/LegionScripts/`, replacing the whole modules folder, then run the
main script. Your settings and saved files carry over. You can delete the 2.6.102 main script.

Only in game:
- Grimoire and Ultima Tracker windows in a zone: double-clicking the title does nothing.
- An Action Bar harmful cell: press it on a red, click a blue's frame before the cursor comes:
  the cursor still goes to the red.
- Property Butler Ban with confirm on: a quick double-click doesn't ban; a second click a moment
  later does.
- Everything listed under "Only in game" for 2.6.92 to 2.6.102.
