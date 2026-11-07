# Virtue Assistant 2.6.94

A fix for 2.6.93, built from it: 2.6.93 stopped at launch with "name 'ApiGameObject' is not
defined" (File: API.py, Line: 9). Nothing else changes: same windows, settings, texts, saves and
timings.

## Fixed

### Virtue Assistant
- **Starts again.** TazUO takes out a script's `import API` line before running it, but only when
  that line holds nothing else. 2.6.93's line packing put it on one line with the other imports,
  so the client left it in, Python loaded the `API.py` help file in LegionScripts instead of the
  real API, and that file stopped the script. The line is on its own again.

## The review pass

- **Rules check:** no new actions in game. Besides the version number and the What's new text, only the
  first line of the mother script changed.
- **Checked:**
  - Every module's own `import API` line was already on its own line; only the mother's was
    packed.
  - The packing tool now leaves `import API` on its own line. The file layout check and a new
    item test both catch a packed one (both flag 2.6.93).
  - Every file compiles in real IronPython 3.4 with no errors and is plain ASCII. Names checked.
  - Saved settings, keys and file formats are unchanged.
- **Tests run (on a mock client, not in game):** every module on: no errors. The item tests pass, the new one included.
- **Why the tests missed it:** the mock client supplies its own `API`, so a packed `import API`
  worked there. The new item test reads the files as text, the way TazUO does.

## Install

Copy `VirtueAssistantV2-6-94.py` and the `VirtueAssistantModules` folder (with `_WhatsNew.py` in
it) into `TazUO/LegionScripts/` and run the new mother script. Your settings and saved files carry
over as they are. You can delete the 2.6.93 mother script.

Only in game:
- The script starts without the API.py error, and every module loads.
- Everything listed under "Only in game" for 2.6.93 still needs checking: it was never seen in
  game, because 2.6.93 couldn't start.
