# Virtue Assistant 2.6.87

The frame's art, made again from the ground up, built from 2.6.86 with everything in it kept. Its
Carved look had visible errors, and its Dragons stood in the game view. Art direction came from
research into Gothic stonework, illuminated manuscripts and classic game frames. The art is drawn from
the client's own art and pictures painted in memory: there are no files to install.

## Changed

### Settings > Layout, the Art button
- **Carved:**
  - Dark slate stone all round the windows, with no grey stone or grey strips left.
  - One thread of old gold runs along the seams and round the game view, with small carved bosses
    where seams meet and corner blocks at the screen's corners.
  - The arch over the game view is new: dark stone shoulders, a gold line that follows the curve,
    carved quatrefoils in the spandrels, and a crown with a garnet keystone and a plaited gold band.
- **Dragons:** Carved, plus two carved dragons coiled round pillars, one each side of the Action Bar.
  - Each stands in a lit shrine on a stone plinth, with gold-leaf crest, claws and spine and garnet eyes.
  - The Action Bar is 192 px narrower to make room for them, and may draw a little smaller.
  - Their heads and necks rise about 60 px above the bar, over the game view. Clicks go through them.
  - They only appear when the bar's zone is at least 100 px tall and wide enough. A shorter bar keeps
    its full width with no dragons, which is the case with the default zones at 1366 x 768.
- **Plain:** the stone look, as before.

### Character HUD
- **Frames:** the dotted gold trim on frames in a zone is gone, in every look. It looked wrong against
  the new art.

## Fixed
- **Stuck art layers:** the frame's art is now kept in front of the game view and behind your windows,
  so it never covers a window or changes when you click one. The small corner blocks and bosses lie
  over the panels' edges and take no clicks.

## The review pass

- **Rules check:** no new actions in game. This is art and window placement only.
- **Checked:**
  - Every file parses, uses nothing newer than IronPython 3.4, and is plain ASCII.
  - Names checked. Old saved keys and formats are unchanged, with no new keys.
- **Tests run (on a mock client, not in game):**
  - An independent review of the art and code, twice, which found real bugs that were fixed. Among
    them: art that could cover window content, pictures left in memory after stopping, corner ornaments
    left on screen with one frame turned off, and art refused after several layout changes.
  - 77 checks, all passing.
  - Both looks painted from the real code and the client's art over a real screenshot, and looked at.
  - Other screen sizes (1366 x 768, 1920 x 1080, 3840 x 2160) and layouts ran without errors.
- **Cost:**
  - The first drawing takes about 0.7 s at 2560 x 1080 in a test with no real drawing, measured in real
    IronPython, and is a one-time hitch while the pictures are painted.
  - A later redraw takes about 0.1 s. A layout change that alters the sizes repaints those pictures.
  - This is over the budget we set: about 72,000 painted pixels and 220 controls. Nothing runs per tick.
- **Left as they are:** the window bars' grey edges in our test pictures come from the screenshot used;
  in game they should show the new stone through, and that hasn't been seen yet.

## Install

Copy `VirtueAssistantV2-6-87.py` and the `VirtueAssistantModules` folder into
`TazUO/LegionScripts/` and run the new mother script. Then pick your look with Art in Settings > Layout.

Only in game:
- All of the art, with your own windows over it, at your screen size.
- The Action Bar's fit between the dragons.
- The small first-draw hitch.
- Unticking "Join zone windows in one frame", and switching looks, leaving nothing behind.
