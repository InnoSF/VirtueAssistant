WHATS_NEW = ("2.6.94: Virtue Assistant starts again. 2.6.93 stopped at launch with an error from API.py.",
    "2.6.93: the scripts are shorter again, now under half their size of two versions ago. Nearly "
    "every settings page is drawn by one shared builder, the modules share more of Virtue Assistant's helpers, and "
    "short lines of code are packed together. Nothing changes in game.",
    "2.6.92: the scripts are about 40% shorter: the same features in far fewer lines, and the notes "
    "that were inside the code are now in the docs folder. Two things are gone: Mongotchi's developer panel, and "
    "the carved and dragons looks of the one frame (Settings > Layout's Art button); a frame that used one of "
    "them now shows the plain stone. Also fixed: Property Butler's log window no longer redraws on every new line.",
    "2.6.91: the modules use Virtue Assistant's own shared helpers instead of keeping "
    "copies, and drop code that was kept for older versions. Nothing else changes in game.",
    "2.6.90: inside each module file the code comes in the same order (saved settings, the "
    "window, the settings page, then starting and stopping). Nothing changes in game.",
    "2.6.89: the script files are laid out in one consistent form, so they are easier to "
    "read and change. Nothing changes in game.",
    "2.6.88: everything Virtue Assistant saves now sits in one folder, VirtueAssistantSettings, "
    "beside the script. Files an earlier version saved beside it are moved there when it starts.",
    "2.6.87: the frame's art is new. Settings > Layout's Art button has carved stone with one "
    "thread of old gold round the game view and an arched crown with a keystone, and dragons, "
    "which adds two carved dragons on plinths framing the Action Bar.",
    "2.6.86: Reclaim space no longer stretches the frames over the game view; a layout it "
    "stretched is put right once. The Art button in Settings > Layout now changes the look "
    "of the frame round your windows even when no gaps lie between them.",
    "2.6.85: the bandage bar fills however a bandage was started, and a window in a zone "
    "is always up, with no Minimize, Close or fold arrow. Supplies moved to Inventory, "
    "with new buttons on the bag sidebar and easy sort filters. The Swing Bar shows where "
    "to turn back when kiting. The game view fits its zone, Settings > Layout can reclaim "
    "space, and any button can have a hotkey (Settings > Keys).",
    "2.6.82: a speed pass over everything. Virtue Assistant reads the game far less "
    "often for the same result: one look at you, the mobiles around you and your "
    "backpack per pass, shared by every module, and windows, bars and settings pages "
    "that read only when something can have changed. Nothing it does in game changed.",
    "2.6.81: over a hundred fixes. Every loop that acts by itself (Skill Bags, Property "
    "Butler's sweep, Bags' Trap / Untrap run) now waits the same way: in a fight, near "
    "a hostile, while you move an item, and until the guard zone is known. A harmful "
    "press on a blue in town asks for a second press, a module answers only the target "
    "cursor its own press raised, and Ultima Tracker's B is one bandage per press.",
    "2.6.80: on the bag canvas each bag's items keep their places relative to one another, "
    "as in the bag itself, whatever size its region takes, and every item stays wholly "
    "inside its own bag's region, below its label.",
    "2.6.79: the bag canvas works in game: 2.6.78 stopped Bags with an error as soon as "
    "your bags were shown in a zone.",
    "2.6.78: in a zone your open bags fill the whole bag area as one picture: each bag "
    "gets a region shaped to its contents, an item you let go stays where you put it, and "
    "each region is labelled with its bag. Windows smaller than their zone are drawn "
    "smaller instead of squeezed, so nothing lies over anything else; Skills, Property "
    "Butler and Mongotchi lay themselves out for their zone at any size. Title rows fit "
    "their width, and Settings > Layout's Check look and Check fit say more.",
    "2.6.77: the Paperdoll's figure is drawn behind the equipment slots, and a worn item "
    "can be pressed and dragged off the figure to take it off (2.6.76 meant to do both, "
    "but the figure still showed in front and couldn't be lifted).",
    "2.6.76: drag a worn item off the Paperdoll's figure to take it off, as in the client's "
    "own paperdoll, and items in the equipment slots can be dragged out from anywhere on "
    "their picture. The Paperdoll keeps its layout whatever you wear: your character fills "
    "the panel's height and a wide figure shows behind the slots.",
    "2.6.75: the game view shows through its zone again (2.6.74 covered it with stone). "
    "In a zone the Paperdoll fills the whole zone, its slots spread top to bottom, and "
    "your character fills the middle of the doll panel at any size. The Action Bar's "
    "Keys, Lock and Grid buttons are always short text buttons again, never icons.",
    "2.6.74: windows fill their zones to the edge, and a window dragged on to a zone in "
    "Arrange mode is slotted there even when it redraws itself on the way. Meters and "
    "Ultima Tracker's windows go back to their zone unless you freed them on Settings > "
    "Layout, and TazUO's World Map never hangs over its neighbours. The stone now covers "
    "every gap between zones. The Action Bar fills its zone's width. In the zone editor a "
    "typed size is used when you press Enter, a zone can overlap others (the game view's "
    "top can be arched round your frames), you can put windows in a zone with a preview, "
    "and there are Undo, arrow keys, edge handles, Lock, Duplicate, Mirror and more.",
    "2.6.73: Bandages and the Swing Bar sit inside your frame's and your target's box, "
    "with the frames a little higher, and the arch beside them is a smooth curve. The bags' "
    "black stays when you hide their side panel, and in a zone the bags are packed to fit "
    "it: drop an item anywhere in the bag area and it lands in the bag under it, right "
    "there. A window dropped outside every zone goes back to its zone, TazUO's World Map "
    "keeps its zone to itself, and Meters and Ultima Tracker's windows are put back in "
    "their zones once. The Action Bar's bottom row sits on a black bar like the others.",
    "2.6.72: windows in zones stay in them: click Arrange windows on Settings > Layout "
    "(or the Action Bar's Lock button) to move them between zones, then Done (or Esc). "
    "With Join zone windows in one frame ticked, every zone has the same look: black "
    "panels, the same narrow seams, no knots or gold on the game, and Ultima Tracker's "
    "windows in the standard style. Your frame and your target's sit in the top corners "
    "with Bandages and the Swing Bar under their bars, and the game view arches up "
    "between them (untick Arch the game view between your frames to keep it as it was). "
    "Bags never flip between two sizes, and many smaller fixes.",
    "2.6.71: the Paperdoll fills its zone: the doll and its slots are drawn bigger, with "
    "your stats in a column beside them when that leaves more room, and no empty stone at "
    "the sides. Dropping an item on an equipment slot wears it again. Skill Bags always "
    "pauses in war mode, and its town pause can only be turned off while Training Alarm is "
    "on. Many smaller fixes to zones and windows.",
    "2.6.70: Bandages and the Swing Bar no longer flicker beside your frames. A window you "
    "drag on to a zone now drops straight into it and fills it; drag it on to a zone that "
    "holds another window and the two swap places. New on Settings > Layout: tick Join zone "
    "windows in one frame for one stone surround round the game area, with a gold border on "
    "its edge (unticked, every window keeps its own look), and Check fit prints in the "
    "journal where each window in a zone sits.",
    "2.6.69: windows in zones stay locked to them. TazUO's World Map now fills its zone to "
    "the edges (no strip of the game round it) and can be dragged on to a zone to put it "
    "there. Ultima Tracker's Combat, Friends, Foes and Neutral windows each fill their own "
    "zone and no longer overlap the window beside them. Meters fills its zone, even with "
    "its display list or segment list open.",
    "2.6.68: the Paperdoll and its bags stay inside their two zones. When the bags need more "
    "rows than the zone under the doll holds, they are shown smaller until they fit, so the "
    "journal or any window under them never covers them. Your own Bag scale comes back as "
    "soon as there is room for it.",
    "2.6.67: with your frame and your target's frame in zones, Bandages and the Swing Bar "
    "now sit inside those zones, beside the bars of their frame, instead of under them.",
    "2.6.66: the Paperdoll and its bags take two zones: the doll in the window's own zone, "
    "the bags in the zone under it (made for them when there is none: in the free room under "
    "the zone, or by splitting it in two). The small arrow on the window's edge, on the side "
    "facing the middle of the screen, pops the Storage window out beside it and tucks it away again.",
    "2.6.65: Social's Guild tab fits its zone: its buttons, the page arrows and the roster "
    "no longer draw over one another or past the edge when the zone is narrow.",
    "2.6.64: Meters fits its zone. A meter window in a zone is drawn at exactly the zone's "
    "size, with as many rows as the height holds, and follows the zone when it changes. Out "
    "of a zone, drag any corner of a meter window to resize it; the Rows setting or Reset "
    "sizes (Meters settings page) gives it back its own size.",
    "2.6.63: TazUO's World Map now fills the zone you put it in, edge to edge, and stays "
    "there: it is locked while it sits in a zone and gets its own place, size and lock back when you free it.",
    "2.6.62: the player and target frames in zones mirror each other: your frame sits at the "
    "left edge of its zone and the target frame at the right edge of its own, each on the "
    "same stone and black background as the other zone windows. The Swing Bar now sits "
    "under the left end of the target frame's bars, mirroring Bandages under the right end of yours.",
    "2.6.61: Ultima Tracker's windows fit their zones exactly, however narrow the zone: "
    "side by side, they no longer run over one another.",
    "2.6.60: the journal in a zone at the bottom of the screen now stops above the chat "
    "line, so what you type shows below it instead of behind it.",
    "2.6.59: Bandages and the Swing Bar as designed: both 182 px wide and flush when stacked. "
    "\"Show who the bandage is on\" is off unless you tick it (it widens the panel). The repeat "
    "arrow is a gold ring with an arrowhead, like the target reticle beside it.",
    "2.6.58: fixes to 2.6.57. TazUO's World Map and the journal now really go into their "
    "zones. The Paperdoll in a zone puts its bags under the doll, on a solid black "
    "background. Bandages and the Swing Bar are both 161 px wide, with the time left as "
    "seconds (\"7.2s\"). The tracker's Combat window no longer jumps about in its zone. "
    "Meters and Social keep to their share of a zone: in a narrow one their columns share "
    "the width and buttons lose their captions (the tooltips still name them).",
    "2.6.57: the zones, fixed. TazUO's World Map and the client's journal now sit in their "
    "zones at the zone's size. The Paperdoll fills its zone with the doll and its slots scaled "
    "as one, and items drag on and off the doll again; the bags under it fill the rest in the "
    "same look. Meters, Social and the Action Bar draw themselves at their zone's size, and "
    "the tracker's windows keep theirs. The player and target frames have no X any more. "
    "Your buffs are icons in a row on your frame with their time under each; Bandages ride on "
    "your frame and the Swing Bar on your target's, below a frame in the top half of the "
    "screen and above it in the bottom half. Bandages has a gold target reticle and a curved "
    "repeat arrow, and the Swing Bar's food shows in grey until you eat or set it.",
    "2.6.56: every window fills its zone exactly. The windows in a zone now share it edge to "
    "edge, each as wide as the zone with a share of its height, and each is made exactly that "
    "size: the tracker's windows, Combat and Grimoire lay themselves out for it, the Action "
    "Bar and Frames scale as big as fits, Skills takes the width and as many rows as fit, Bags "
    "grows its slots, and every other window stretches its frame and sections to the slot with "
    "its text and buttons kept in place. Nothing leaves its zone. Bandages and the Swing Bar "
    "are now two-row panels of the same width: the bar and its seconds, then the bandage, the "
    "count, the target ring and the spiral, or the hit chance and the satiety. Neither has a "
    "smaller form or a tray button any more; turn the part off to hide it. A bandage on "
    "someone else now starts at 7.5 s.",
    "2.6.55: a zone for every window, from the settings. Each module's settings page has a "
    "WINDOWS section with a Zone button per window (click it for the next zone, or free), and "
    "the Layout page lists every window with a drop-down. A window now fits the zone it sits "
    "in: each zone has a Fit (the Fit button on the editor bar): fill width draws its windows "
    "as wide as the zone, shrink only makes a window wider than the zone smaller, none leaves "
    "them as they are. The Action Bar stands upright in a tall zone; Frames, Grimoire and "
    "Ultima Tracker fit by their scale, Bags by its columns, Skills by its width; a window "
    "that is drawn whole (Meters, Corpse, Treasure Maps, Traps & Fields, Ping History, "
    "Restock, Training Alarm, Skill Bags, Sightings, Lookout) is scaled whole; the rest keep "
    "their size and are placed and cut to their slot as before.",
    "2.6.54: the layout. Settings > Layout places the module windows in zones round the game "
    "area: paperdoll and bags on the left, the frames over the game and the Action Bar under "
    "it, the map, the tracker and the meters on the right. Pick the Default window layout to "
    "try it; drag any window on to a zone to slot it there (it stacks under what is there), "
    "drag it out to free it. Edit zones shows every zone on the screen grid to drag, resize, "
    "add or remove, and saves your own frame layouts; they reflow for any screen. Nothing "
    "moves until you pick a layout or drop a window on a zone.",
    "2.6.53: no window is ever taller than the screen. A window that grows past the screen's "
    "height (a long list, a tall settings page, a small screen) now fits the screen and its "
    "body scrolls, with a scrollbar down its right side; the title row stays put. Every window "
    "of every module does this, and nothing else about them changed.",
    "2.6.52 is a polish pass: every window and every piece of text, in every module, now follows "
    "one standard. Windows share the same title row and tooltips; captions, labels and section "
    "titles are shorter and plainer; every button, box and field has a tooltip that says what it "
    "does; the debug boxes of each settings page sit in a DEBUG section at its end.",
    "A part is now called the same thing everywhere: its name on the Modules tab is its window "
    "title, its journal prefix and its name on the Action Bar. So Unit Frames is Frames, Spell "
    "Timers is Buffs & Timers, Swing Timer is Swing Bar, Unified Bag is Bags, Character is "
    "Paperdoll, Storage Index is Storage, Corpse Run is Corpse, Treasure Hunter is Treasure Maps, "
    "Trap Highlight is Traps & Fields, Attention is Training Alarm. The search box still finds the old names.",
    "Nothing else changed: every setting, window place, list, hotkey and file is kept, and every "
    "button does what it did.",
    "From 2.6.5: 26 modules became 11. The old modules are PARTS of a themed module, each with "
    "its own box (click the arrow on a module's row to see them).",)
