# Virtue Assistant

An all-in-one helper for the TazUO client's Legion scripting (Python), made for the In Mani Ylem shard.

The main script (`VirtueAssistantV<x-y-z>.py`) holds the Virtue Assistant window (Modules and Settings tabs), window snapping, zones, profiles and the main loop. Each module is a file in the VirtueAssistantModules folder beside it and can't run on its own.

```
   ActionBarModule.py       Action Bar       cells for items, spells, skills and
                                             windows, with hotkeys
   CharacterHudModule.py    Character HUD    frames, timers and bars for you and pets
                                             (Frames, Buffs & Timers, Swing Bar,
                                             Bandages, Pets)
   InventoryModule.py       Inventory        bags, paperdoll, storage, restock and
                                             supplies (Bags, Paperdoll, Storage,
                                             Restock, Supplies, Bag Sections)
   GrimoireModule.py        Grimoire         spellbook, runebooks and reagents
   WorldMapModule.py        World Map        pings, corpse, dig and dry spots, traps,
                                             on TazUO's World Map too (Map Pings,
                                             Corpse, Treasure Maps, Ore Tracker,
                                             Traps & Fields)
   UltimaTrackerModule.py   Ultima Tracker   friends, foes and neutrals near you
                                             (Tracker, Lookout, Overview)
   SocialModule.py          Social           friends, party, guild and profile
   SkillsModule.py          Skills           skills, training and AFK alarms
                                             (Skills Window, Training Alarm,
                                             Skill Bags)
   PropertyButlerModule.py  Property Butler  house sweeps, visitors, eject and ban
   MetersModule.py          Meters           damage, healing, loot and gold meters
   MongotchiModule.py       Mongotchi        a pet mongbat to raise and dress up
```

Parts: five modules are split into parts, each with its own box under the module's row on the Modules tab (click the arrow to unfold). A part that is off costs nothing. The Modules tab's search also finds older module names.

Remove a file from the folder to leave that module out. A new `<Name>Module.py` in the folder loads too, as does any folder beside the main script named `VirtueAssistant...Modules`.

Saved files (lists, layouts, exports, profiles) go in the VirtueAssistantSettings folder beside the main script, made on the first start.

## Install and use

1. Put the main script and the VirtueAssistantModules folder in TazUO/LegionScripts and run the main script from the Legion Script Manager. Run only that file, and no other copy of Virtue Assistant at the same time. Its window shows first; the modules you had on then start one at a time.
2. In the Virtue Assistant window, tick a module to turn it on, untick it to turn it off.
3. The down arrow in its title folds the window into a gear (click the gear to reopen it); the gold arrow folds it into the Action Bar instead.
4. Drag a corner to resize: its sections flow into columns to fill the size, then the window shrinks to fit them. The scale buttons (- and +) scale it; click the percentage for 100%.
5. A module's window closes only from its X (which turns the module off); right-click does nothing.
6. The X on the Virtue Assistant window stops everything.
7. At start it checks the TazUO parts it reads. If a TazUO update renamed one, a red journal line names it and the module or part that needs it stays off until the next Virtue Assistant (only for that session: your choice is kept).
8. If Virtue Assistant didn't finish starting last time (the client closed or froze while modules were starting), it asks first: Start normally, or Start safely with every module off for that session. Then tick modules back on one at a time on the Modules tab to find the one that stops it.

## Two copies of the code

The files at the top of the GitHub page (and in the zip on the Releases page) are the ones to install. They are packed small to download: tabs for indents, few spaces and short names for values used inside one function. The `readable` folder holds the same code laid out normally, with a note on every function and comments where the code isn't obvious, for anyone who wants to read how it works. Both run the same, but install only the packed files. When the journal shows an error with a file and line, it names a line of the packed files.

## A module on its own

Any module also runs alone: pick its file (in the VirtueAssistantModules group) in the Legion Script Manager. The main script must be in LegionScripts, but isn't started. Alone, a module has its own window, its settings (the window's Settings button) and its hotkeys, and the shard-rule pauses still apply. It has no main window, profiles, zones, tray or other modules, and it doesn't change which modules the full suite turns on. A themed module's parts are ticked under PARTS in its settings. Closing its window stops it. It won't start while the full suite runs, and stops if the suite starts.

## Windows

- **Minimize** (boxed down arrow, or double-click the title): the window shrinks to a small form on screen.
- **Fold into the Action Bar** (gold arrow): the window hides; its tray button on the Action Bar brings it back. With no Action Bar up, it stays minimised until the bar opens.
- **Snapping:** windows snap to each other and to the screen grid when dragged, and move with the window they snapped to (switch in Settings > Interface).
- Every window uses the client's gump art.
- **Look** (Settings > Interface, LOOK): the Look button cycles Classic, Dark (charcoal frames), Parchment (brown frames and sections) and High contrast. Open windows redraw at once and keep their place. Saved per character; Classic by default.
- **Text size** (the same section): 100, 115, 130 or 150% for text in lists and bars; TazUO's own UI scale still sizes every window.
- **Compact rows:** tighter rows in lists and settings, and smaller frames.
- **Fade windows when idle:** a window fades (Faded: 20-90%, default 40) once the mouse has been off it and nothing in it changed for a while (After: 2-30 s, default 6), and comes back when the mouse is over it or it changes. The Action Bar and unit frames stay solid unless "Fade the Action Bar and unit frames too" is ticked; the Virtue Assistant window and alerts never fade.
- **Colour-blind marks** (ACCESSIBILITY): a colour-blind palette for notoriety and HP colours, plus letters: R murderer, C criminal or grey, O enemy, A ally, I invulnerable before a name, and P poisoned, Z paralysed, M mortal wound after it.
- **Streamer mode:** other players show as "Player <id>", you as "You", and guild names, places and coordinates as "(hidden)", so a stream or screenshot gives nothing away. Journal lines keep the real names.
- Window places, minimised or folded state, which modules are on and each module's view are remembered per character as soon as you change them.

## Zones

Settings > Interface (the Interface module) splits the screen into zones. A window in a zone fills it and stays there; Arrange mode (or Lock on the Action Bar) unlocks windows to move them between zones, and Esc or Done locks them again. The page also edits zones, saves layouts and has Reclaim space, which gives empty room to the game area.

- **Set up:** a three-step window (it opens by itself the first time, when no layout is chosen yet): pick one of five ready-made screens (Sides, Mirrored, Bottom bar, Right column, Compact; the screen shows each as you click it), check which zone each window goes in, then pick the look. Nothing changes until Done.
- **One panel:** with "Join windows in zones into one panel" on, one stone frame covers every window zone and reserved zone (the journal and bag grid too), with no corners or lines between windows and a gold border round the game view. Windows lose their own frames and title rows; hover a window's top edge to show its title row. A zone set to "Apart" in the zone editor keeps its own edge.
- **Zone editor:** Split cuts a zone in two, Join merges it with a matching neighbour; gold lines mark zones that join. Stack: tabs shows one window of the zone at a time, with a strip of tabs above it; click a tab to show that window, and drop a window on the zone to add it.
- **Share code** (LAYOUTS): puts a code for the frame and window layouts in use in the Code field (Ctrl+A then Ctrl+C copies it; it is also written to layout-code.txt in VirtueAssistantSettings). Paste someone's share code there and press Load code to add it as a layout, with " (shared)" after its name; it fits itself to your screen.
- **Layouts by situation:** with "Switch layouts by situation" on, pick a window layout for war mode, the bank (for 5 minutes after you open it, while near), dungeons and towns (guard zones); war mode comes first, then bank, dungeon, town. Leaving them all puts back the windows as they were.
- **Interface off:** every window is free again and your own game view comes back.

## Settings

- **Search:** the box at the top of the Settings tab finds any setting by its caption, section or tooltip, across every page (pages not opened yet are read one at a time). Click a hit to open its page, with "<- found" beside the row.
- **New:** a setting added in this version shows a "new" tag until you have seen its page; a page or part with one is marked in the lists.
- **Alerts:** History opens the ALERT HISTORY window, the last 50 alerts with their time (also from the alert banner). Quiet 30 min turns alert sounds and banners off for 30 minutes (Resume ends it early); alerts still go to the history and the journal, and alarms still pause skill loops.
- **Backups** (this character): Back up now saves every Virtue Assistant setting of this character; Restore puts the picked backup back (press twice within 3 s; the settings of now are backed up first). One is also made by itself the first time a new version starts. The 10 newest are kept, in VirtueAssistantSettings/Backups.

## Quick Launcher

The Find button on the Virtue Assistant window (also a hotkey in Settings > Hotkeys, and an Action Bar Launcher cell) opens the QUICK LAUNCHER: type a few words to find a Grimoire rune, an Action Bar cell, a window, a layout (with Interface on), a setting or a command such as alert history and quiet. Every word must match. With the field empty it lists Recent, the last 5 runs of this session.

- **Enter** runs the top row, a click runs that row; the launcher then closes. A run is one action: a rune is one trip through Grimoire, a cell is one use of that cell with its own checks.
- Enter never counts as the second press of the harmful-cursor confirm (see Hotkeys): it can only arm it; a click on the row 0.6 to 3 s later confirms.
- A cell that changed since it was listed is refused rather than run.

## Hotkeys

Set on each module's settings page and on the Action Bar; Settings > Hotkeys lists them all and binds a key to any button. They never fire while you type in the chat line or any text box; click the game world to leave a field.

- **One owner per key:** a second module or button that claims a held key gets a red journal line naming the holder, and takes the key when the holder lets it go.
- **Harmful cursor in town:** aiming a harmful target cursor at a blue or green in a guard zone (or a zone not yet known) only arms on the first click; a second click within 3 s aims. A double-click doesn't count.

## Profiles

The bar under the title, on both tabs. A profile is one character's whole setup, which any character can load.

- **Save:** under the typed name, or over the picked profile when the box is empty.
- **Load:** puts the picked profile on this character (every module restarts with its settings).
- **Star:** makes the picked profile the favourite (click again to clear). Characters that haven't loaded another profile get it at start, new ones included. It also becomes TazUO's default profile, so a new character starts with its client settings.

A profile holds every module's settings and window places, which modules are on, the Bags layout, TazUO's Options settings (profile.json, cooldown bars, grid highlights, name plates, info bar and more) and Legion Assistant settings (agents, auto loot, organizer, journal filter, buy / sell lists, macros, hotkeys). Data tied to one character's items stays with it: runebook and spellbook data, Bags slots, Dress Agent outfits, the grab bag, mount and weapon serials. Settings TazUO already shares across characters need no profile.

Profiles are folders in VirtueAssistantSettings/VirtueAssistantProfiles; delete a folder to delete that profile.
