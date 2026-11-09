# Virtue Assistant 2.7.0.24

Built from 2.7.0.23. A code review of 2.7.0.23 found eight small problems. This version fixes them: two you can
see, and the rest small speed and tidiness fixes. If anything misbehaves, go back to 2.7.0.23.

## Shard rules (In Mani Ylem)

- No game action was added or changed. The same presses do the same single things, so R1-R8 are untouched.

## Fixed

- **Inventory > Restock:** a target typed on the settings page just before the page closed (within a quarter of a
  second) was lost. It is now kept.

## Changed

- **Character HUD:** the loop that refreshes the HUD in small slices now also stops when the script stops. It
  does the same work as before.
- **Inventory:** the loop that works out how small bag items must be drawn now has a fixed number of steps. The
  result is the same. Bags, search highlighting and sorting use the lighter error guards again in the work they
  do every pass.
- **Meters, Mongotchi, Skills, Ultima Tracker:** the same lighter error guards are back in the work they do every
  pass (pets nearby, effects and the gremlin animation, skill rows and staff names, the attacker check).
- **Ultima Tracker:** the scan for players nearby makes its working lists only when it finds something, as it
  did before 2.7.0.19. It runs several times a second, so this saves a little work each time.
- **Main script:**
  - Settings tab: after you click another page, the profile list is still drawn on top of the page. Its open
    list no longer sits under the new page's controls. A profile you picked but haven't loaded yet stays picked.
  - Settings tab: if a quick page switch fails, the error now shows in the journal and the whole window is
    redrawn, where before the error was hidden.
  - Settings tab: flipping pages many times no longer leaves the old pages' controls in two internal caches.
    A window the zones have stretched always redraws whole on a page switch.
  - Copying TazUO settings for profiles works out a setting's default values once, not on every use.
  - The loop that evens out a row of zones now has a fixed number of steps. The result is the same.

## The review pass

- Rules check R1-R8: no new game action calls.
- A fresh review of the diff checked each of the eight fixes against the code. It confirmed seven. On the eighth
  it noted that a stretched settings window could keep old controls in a third cache. The settings window is
  never stretched by the zones today, but a page switch on such a window now redraws whole, so that can't
  happen.
- Speed: the mock run's call counter, with every module on and 600 passes, shows no rise in calls or client hops
  per pass.
- All 536 item tests pass, 7 of them new: Restock keeps a late edit; the profile list is last after a page
  switch and keeps its pick; a failed page switch is reported and the window redrawn; 30 page flips leave nothing
  behind in the caches; a stretched window redraws whole; the default values are worked out once; no loop of the
  old form is left. All 7 fail on 2.7.0.23. Also run:
  - the mock run, with and without every module;
  - each module run on its own;
  - the IronPython 3.4 compile;
  - the layout check.

## Install

Copy `VirtueAssistantV2-7-0-24.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`. Replace
the whole modules folder, then run the main script. You can delete the 2.7.0.23 main script.

Only in game:
- That after clicking another Settings page, the profile list's open list shows on top of the page.
- That a Restock target typed and closed quickly is kept.
- That bags, search highlighting, sorting, Meters, Mongotchi, Skills and Ultima Tracker behave as before.
