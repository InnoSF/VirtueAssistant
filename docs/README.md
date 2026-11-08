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
                                             Restock, Supplies)
   GrimoireModule.py        Grimoire         spellbook, runebooks and reagents
   WorldMapModule.py        World Map        pings, corpse, dig and dry spots, traps,
                                             on TazUO's World Map too (Map Pings,
                                             Corpse, Treasure Maps, Ore Tracker,
                                             Traps & Fields)
   UltimaTrackerModule.py   Ultima Tracker   friends, foes and neutrals near you
                                             (Tracker, Lookout)
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

1. Put the main script and the VirtueAssistantModules folder in TazUO/LegionScripts and run the main script from the Legion Script Manager. Run only that file, and no other copy of Virtue Assistant at the same time.
2. In the Virtue Assistant window, tick a module to turn it on, untick it to turn it off.
3. The down arrow in its title folds the window into a gear (click the gear to reopen it); the gold arrow folds it into the Action Bar instead.
4. Drag a corner to resize: its sections flow into columns to fill the size, then the window shrinks to fit them. The scale buttons (- and +) scale it; click the percentage for 100%.
5. A module's window closes only from its X (which turns the module off); right-click does nothing.
6. The X on the Virtue Assistant window stops everything.

## A module on its own

Any module also runs alone: pick its file (in the VirtueAssistantModules group) in the Legion Script Manager. The main script must be in LegionScripts, but isn't started. Alone, a module has its own window, its settings (the window's Settings button) and its hotkeys, and the shard-rule pauses still apply. It has no main window, profiles, zones, tray or other modules, and it doesn't change which modules the full suite turns on. A themed module's parts are ticked under PARTS in its settings. Closing its window stops it. It won't start while the full suite runs, and stops if the suite starts.

## Windows

- **Minimize** (boxed down arrow, or double-click the title): the window shrinks to a small form on screen.
- **Fold into the Action Bar** (gold arrow): the window hides; its tray button on the Action Bar brings it back. With no Action Bar up, it stays minimised until the bar opens.
- **Snapping:** windows snap to each other and to the screen grid when dragged, and move with the window they snapped to (switch on the Modules tab).
- Every window uses the client's gump art.
- Window places, minimised or folded state, which modules are on and each module's view are remembered per character as soon as you change them.

## Zones

Settings > Layout splits the screen into zones. A window in a zone fills it and stays there; Arrange mode (or Lock on the Action Bar) unlocks windows to move them between zones, and Esc or Done locks them again. The page also edits zones, saves layouts and has Reclaim space, which gives empty room to the game area.

## Hotkeys

Set on each module's settings page and on the Action Bar; Settings > Hotkeys lists them all and binds a key to any button. They never fire while you type in the chat line or any text box; click the game world to leave a field.

## Profiles

The bar under the title, on both tabs. A profile is one character's whole setup, which any character can load.

- **Save:** under the typed name, or over the picked profile when the box is empty.
- **Load:** puts the picked profile on this character (every module restarts with its settings).
- **Star:** makes the picked profile the favourite (click again to clear). Characters that haven't loaded another profile get it at start, new ones included. It also becomes TazUO's default profile, so a new character starts with its client settings.

A profile holds every module's settings and window places, which modules are on, the Bags layout, TazUO's Options settings (profile.json, cooldown bars, grid highlights, name plates, info bar and more) and Legion Assistant settings (agents, auto loot, organizer, journal filter, buy / sell lists, macros, hotkeys). Data tied to one character's items stays with it: runebook and spellbook data, Bags slots, Dress Agent outfits, the grab bag, mount and weapon serials. Settings TazUO already shares across characters need no profile.

Profiles are folders in VirtueAssistantSettings/VirtueAssistantProfiles; delete a folder to delete that profile.
