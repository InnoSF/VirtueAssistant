# =============================================================================
#  Virtue Assistant  -  TazUO Legion Script Manager (Python)
#  Shard: In Mani Ylem
#
#  The mother script: the Virtue Assistant window (Modules and Settings tabs),
#  the shared look (Kit), window snapping, the shared tracker window and the
#  main loop. Every module is its own file in the VirtueAssistantModules
#  folder next to this script, and is loaded from there when this runs. A
#  module file can't run on its own; it needs this script.
#
#     ActionBarModule.py       Action Bar      a bar of cells for items, spells, skills,
#                                              macros and windows, with hotkeys
#     CharacterHudModule.py    Character HUD   frames and bars for you, your target, your
#                                              party and your pets (Frames, Buffs & Timers,
#                                              Swing Bar, Bandages, Pets)
#     InventoryModule.py       Inventory       your bags, paperdoll, every container you
#                                              own and restocking (Bags, Paperdoll,
#                                              Storage, Restock)
#     GrimoireModule.py        Grimoire        spellbook, runebooks and reagents
#     WorldMapModule.py        World Map       guild pings, your corpse, dig spots, dry
#                                              spots and traps, on the map (Map Pings,
#                                              Corpse, Treasure Maps, Ore Tracker,
#                                              Traps & Fields), on TazUO's World Map too
#     UltimaTrackerModule.py   Ultima Tracker  who is around you: friends, foes and
#                                              neutrals, with health bars (Tracker, Lookout)
#     SocialModule.py          Social          friends, party, guild and your profile
#     SkillsModule.py          Skills          your skills, training and the things that
#                                              need you at the keyboard (Skills Window,
#                                              Training Alarm, Skill Bags)
#     PropertyButlerModule.py  Property Butler keeps your house: Detect Hidden sweeps,
#                                              visitors, eject and ban
#     MetersModule.py          Meters          damage, healing, loot and gold-per-hour
#                                              meters, per fight or session
#     MongotchiModule.py       Mongotchi       a pet mongbat to raise, dress up and take
#                                              on journeys
#
#  Five of them are made of PARTS (2.6.5): a part is one feature with its own
#  box under the module's row on the Modules tab (click the arrow to unfold
#  them), and a part that is off costs nothing. The 2.6.06 modules live on as
#  parts (Unit Frames is Character HUD > Frames, Swing Timer is Character HUD
#  > Swing Bar, Unified Bag is Inventory > Bags, Map Pings is World Map > Map
#  Pings, Lookout is Ultima Tracker > Lookout, Skill Bags is Skills > Skill
#  Bags ...); the Modules tab's search box still finds the old names. Every
#  saved setting, window place, list and file keeps its 2.6.06 key, so nothing
#  is lost going to 2.6.5 or back.
#
#  Take a file out of the folder to leave that module out; it simply won't
#  be listed. A new <Name>Module.py dropped in the folder is loaded too,
#  after the ones above (it registers itself with HOST.add at its bottom).
#  Any other folder beside this script whose name starts with
#  VirtueAssistant and ends with Modules is loaded the same way, after
#  VirtueAssistantModules.
#
#  Every window snaps to the others when dragged (corners first) and moves
#  with the window it snapped to; the switch is on the Modules tab.
#
#  Minimizing (2.5.5). Every window has two ways down, side by side at the
#  top right of its title:
#    - Minimize (the boxed down arrow, or double-click the title): the
#      window folds to its own small minimized form and stays on screen,
#      whether or not the Action Bar is up.
#    - Fold into the Action Bar (the gold arrow left of it): the window is
#      hidden completely, minimized form and all; the Action Bar's tray
#      button stands in for it (click it to bring the window back). With no
#      Action Bar on screen the window waits in its minimized form and folds
#      in by itself once the bar is up. The choice is kept per character
#      until you show the window again.
#
#  2.5.6: Mongotchi's gremlin is drawn as the Akalabeth gremlin.
#  2.5.7: swatting it gives a smack and an "oof!" (no more hiss).
#  2.5.8: Ultima Tracker's health bars are smooth, softer-coloured bars
#         (no more stripy line art with a seam), easier on the eyes.
#  2.5.9: Alt+click a Unit Frame to auto-follow that character (Alt+click
#         again to stop), just like Ultima Tracker's bars. Every window that
#         shows another mobile's health or acts on another mobile follows
#         the same rule, through the shared Follow helper below, and they all
#         share one follow: Unit Frames and Ultima Tracker always agree on
#         who you are following.
#  2.5.10: the Swing Timer learns your real swing speed: it keeps the
#         gaps between your last 10 swings with the weapon in hand and aims
#         the bar at their average, updated on every swing.
#  2.5.11: the Swing Timer remembers those swing times between sessions,
#         for every weapon you've used, in _swing_timer_<serial>.txt next
#         to this script (made by the module itself; nothing to install).
#  2.5.12: a swing that takes notably longer than the average (15% or more)
#         isn't counted, so a stall or a lag spike doesn't drag the aim out.
#         Three slow swings in a row mean you really are swinging slower
#         now (low stamina), and the timer relearns from them.
#  2.5.13: Map Pings no longer makes TazUO's Enhanced Map connection drop
#         and reconnect over and over. Its listener on that connection is
#         plain .NET now (a Python one left behind by a stopped run threw on
#         every packet, and TazUO drops the connection when a listener
#         throws), stale listeners are cleared out, the non-standard ping
#         packet is only sent once the map server shows it relays them, and
#         if the connection still keeps dropping Map Pings lets go of it and
#         says so in the journal.
#  2.5.14: the Action Bar's right-click menu always opens wholly on screen:
#         under its cell when there's room, above it when there isn't (a bar
#         at the bottom of the screen), and pushed in from the screen's edges.
#         It stays on screen as it changes size (lists, pages, Back).
#  2.5.15: Unit Frames can size party members' frames separately: tick
#         "Party members" under UNIT FRAME SCALE on its settings page and
#         set their own size with the slider beside it.
#  2.5.16: new module, Meters (MetersModule.py): Details!-style meter
#         windows for damage done / taken, DPS, healing, cures, kills,
#         deaths, spells, mana, consumables, buffs, gold per hour, items
#         gained, skill and stat gains per hour, fame / karma and travel,
#         per fight or for the whole session. "New window" opens more
#         meter windows, each with its own display.
#  2.5.18: a clean-up pass over every file: unused, duplicated and dead
#         code cut out, long-winded code rewritten shorter, and the window
#         plumbing every module repeated (saved positions, the title bar,
#         the minimized bar, the click queue) moved into shared Kit helpers.
#         No change to what anything does.
#  2.5.19: bug fixes. Ultima Tracker: its notes and its "Combat Bars hidden"
#         message point to the Tracker & Pings window.
#  2.5.20: smoothness. Every script call that returns something waits for
#         the client's next frame, and with everything on in a fight the
#         modules spent all their time waiting: a module that should run 20
#         times a second ran about once every 3 seconds, and a click could
#         take seconds to be noticed. Now each pass of the main loop makes
#         one hop to the client and runs the windows and every module there
#         together, with no waits inside; work that has to wait (a server
#         reply, a gump) runs separately and holds nothing up. Picking a
#         target (Ultima Tracker, Unit Frames, Unified Bag ...) no longer
#         freezes the other modules while the cursor is up, and modules no
#         longer clear each other's journal lines.
#  2.5.22: a speed and memory rewrite; nothing changes in what you see or
#         what the modules do. The journal is read once per pass for every
#         module, and only the lines that are new since the last read. The
#         main loop does the least it can on every pass: it keeps a list of
#         the modules that are on (instead of asking every module every
#         time), goes to the client only when something there is due, and the
#         Virtue Assistant and Tracker & Pings windows look at their buttons
#         only after a click. The client's settings are found once and
#         remembered, the profile list is read from disk off the game's
#         thread, the caches that used to grow all session stay small, and a
#         fault in the main loop is reported instead of stopping the script.
#         Fixed: two people saying the same words at the same moment are
#         two journal lines again (one of them used to be dropped).
#  2.5.23: every folder beside this script named VirtueAssistant<Name>Modules
#         is loaded, after VirtueAssistantModules.
#  2.5.24: tidied comments and Ultima Tracker's town-NPC name list.
#  2.5.25: tidied Ultima Tracker's town-NPC name list.
#  2.5.26: windows always stay on screen. Every window of every module and
#         of this script is placed on screen when it opens (Kit.place) and
#         moved back on if it is ever off (the keeper in Snap: a window that
#         grew, was dragged half off and let go, or was left behind by a
#         smaller client window). Every window remembers its place and
#         whether it was minimized (Kit.load_pos / save_pos, load_min /
#         save_min); a place saved on another screen size is moved with
#         the screen anchor it was nearest, so a window in a corner stays
#         in that corner. One anchor convention for every window: the
#         nine screen anchors (Kit.ANCHORS) placed and recognised by
#         Kit.anchor_pos / anchor_at, one snap distance (SNAP_DIST) for
#         windows of every module, and a window's rect is exactly its
#         drawn frame. The rules are written out above Kit.clamp.
#  2.5.27: windows snapped on to the Unified Bag stay anchored to it when its
#         edges move: bags only on or off (no title bar, no side panel, the
#         slots up where the bar was), the side panel coming or going, the
#         slots growing to fit a bag. Each one is put back against the edge
#         it was on, where that edge is now, and keeps following the bag
#         when it is dragged (the rebuild used to drop the link). A window
#         let go against a window that another window places by itself
#         (Kit.attach: the Unified Bag's slots under its title bar, the
#         Action Bar's tray) snaps to it too, and follows the window that
#         leads it.
#  2.5.28: the Skills window is resizable: drag any corner. Its height sets
#         how many rows the skill list shows and its width spreads the
#         columns (the name column and the progress bars grow); both are
#         remembered with its position and shown on its settings page. A
#         saved size larger than the screen is cut down to fit.
#  2.5.29: unit frames stay exactly where they are dropped. A frame is exempt
#         from window snapping (Kit.no_snap: no jump to a screen anchor, an
#         edge or another window on release, no following a dragged window,
#         and no window snaps on to a frame), while the keeper still keeps it
#         on screen; a frame dropped within SNAP_DIST of another frame lines
#         up with it pixel-exact (the module's snap_to_frames). A drag of a
#         frame is saved the moment it settles, a failed position read is
#         never kept, and the Mirror option measures the window in gump
#         pixels and no longer moves the target frame at start-up.
#  2.5.30: a module can ask to be on by default (HOST.add default_on=True):
#         it is on until you untick it.
#  2.5.31: new module, Social (SocialModule.py): TazUO's friends list, your
#         party, your guild (with its Diplomacy page) and your own character
#         profile on four tabs of one window. The Action Bar's window buttons
#         gain a second page, "Module windows": any module's window can sit
#         on a bar button (click turns it on and shows it, click again folds
#         it into the tray).
#  2.5.32: Character module: a Diablo-style paperdoll (your character drawn by
#         the client with twenty equipment slots round it; hover a slot for the
#         item's properties, drag a worn item out, drop an item from a bag or
#         the ground on any slot to wear it, with a stats strip underneath).
#         When Unified Bag runs too the two are ONE window: the paperdoll on
#         the left, every bag's slots on the right under one title bar (Bags,
#         Traps, Settings, fold, Minimize and Close act on the whole); Unified
#         Bag offers bag.attach / bag.grid_size / bag.open_manager /
#         bag.open_traps in HOST.services for it.
#  2.5.33: new module, Property Butler (PropertyButlerModule.py): looks after
#         your house while you stand in it. Sweep uses the Detect Hidden skill
#         on your own spot every time it is off its delay and calls out anyone
#         it reveals; a Visitors list shows every player near you with Friend,
#         Eject and Ban buttons (the house commands are said out loud and the
#         house's cursor is aimed at that player; Ban asks for a second
#         click); Eject... / Ban... / Friend... / Lock down... / Release... pick
#         a player or an item with a target cursor; a short log keeps what was
#         done and what the shard answered. The spoken commands and the skill
#         delay are on its settings page.
#  2.5.34: new module, Skill Bags (SkillBagsModule.py): pair a bag with a
#         skill and an item filter, and it uses the skill on every item in
#         the bag, once each: Item Identification, Arms Lore, Taste
#         Identification, Remove Trap, Lockpicking (with your lockpicks),
#         decoding treasure maps, a plain double-click, or any skill name or
#         tool graphic you type. Auto watches the bag for new items, Run does
#         one pass, Reset forgets what was done; results come from the journal.
#  2.5.35: Mongotchi Journeys: a Journeys button in the pen opens a window with
#         Treasure hunts (eight places, each with its own finds and two relics
#         found nowhere else, farther ones longer, riskier and locked behind a
#         grown pet or a Valor level; a Relics tab collects them, +1% squeaks
#         each), Meditation (send it to one of the eight shrines for 20
#         minutes; virtue levels 0-10 change how it behaves: shop prices,
#         petting, pantry guarding, stolen food won back, bigger hauls, more
#         squeaks, meditation and relic luck, slower hunger, its chatter) and
#         Call home. Trips carry on while the module is off; the Avatar title
#         now needs every virtue at 5; titles the Explorer and the Pilgrim.
#  2.6.0: the major release: it gathers 2.5.26 to 2.5.35 into one version, adds
#         Character's own paperdoll drawing and the stacked Character + Unified
#         Bag window, Social's Guild tab (the server's guild window read into
#         it, roster and all), and a bug-fix pass over every file. In short:
#         - Windows (2.5.26): always wholly on screen, place and minimized
#           state remembered per character and adapted to the screen size,
#           one anchor and snap convention (Kit.place / load_pos / save_pos /
#           load_min / save_min / attach, Kit.ANCHORS, one SNAP_DIST, the
#           screen measured in gump pixels through RenderScale).
#         - Unified Bag (2.5.27): snapped windows follow its edges when the
#           title bar or side panel is hidden or the slots grow; Kit.attach'd
#           windows are snap targets.
#         - Skills (2.5.28): the window is resizable from any corner.
#         - Unit Frames (2.5.29): frames never move on their own (Kit.no_snap)
#           and line up pixel-exact with each other.
#         - HOST.add default_on=True (2.5.30).
#         - Social (2.5.31): new module (Friends / Party / Guild / Profile);
#           the Action Bar's "Module windows" button page.
#         - Character (2.5.32): new module, a Diablo-style paperdoll that
#           joins with Unified Bag into one window.
#         - Property Butler (2.5.33): new module (Detect Hidden sweeps,
#           visitors list, Eject / Ban / Friend / Lock down / Release).
#         - Skill Bags (2.5.34): new module, a skill on every item in a bag.
#         - Mongotchi Journeys (2.5.35): treasure hunts, virtue meditation,
#           relics; new per-character key Mongotchi_quests, main window 448
#           high.
#         - Character: the paperdoll is drawn by the module itself (the
#           client's own paperdoll control stayed blank inside a script
#           window): the body and every worn layer as gump pics in the
#           client's layer order, hover for an item's properties, double-click
#           to use it. The combined window with Unified Bag is stacked: the
#           doll, slots and stats on top, every bag's slots underneath, under
#           one title bar; Unified Bag's gem button (bags only) works there.
#         - Social: the Guild tab shows the server's guild window: the My
#           Guild page (guild name, alliance, faction, charter, website) and
#           the whole Guild Roster (every member with rank, Online / last on
#           and guild title, all its pages), read with the window opened
#           hidden and closed again; Refresh re-reads it, and it is re-read
#           every few minutes while the tab shows (settings). Members in view
#           get a health bar and distance; allies in view that aren't on the
#           roster follow the roster. The tab is 600 wide; new per-character
#           keys Social_guild and Social_roster. Diplomacy falls back to the
#           tab's button id.
#         - Bug fixes everywhere (see "Bugs fixed" in PATCHLOG-2.6.0.md): among
#           them Unified Bag's anchored windows now really follow its edges,
#           a trip of Mongotchi's no longer ends early with the full reward
#           after a login, Grimoire never leaves a pre-target armed, Ultima
#           Tracker's save file survives a damaged line, Social's party Decline
#           works, Skills' Action Bar button brings a hidden window back,
#           modules started before login no longer untick themselves, and
#           Alt+click auto-follow is on every control that shows another
#           character.
#         The full patch log is PATCHLOG-2.6.0.md beside this file. Saved
#         settings and window places from any 2.5.x load unchanged.
#  2.6.01: the improvement pass after 2.6.0 (PATCHLOG-2.6.01.md beside this
#         file has every item). In the mother script: a module file is
#         compiled on the script's thread when its box is ticked (no frame
#         hitch), a settings page is measured once and the measurement kept,
#         modules stop in reverse order so a service lives longer than the
#         modules using it, the window and the hub are not re-read for their
#         place on every save, a target cursor raised from a click handler is
#         still taken down when its module stops, journal lines without a
#         client time are no longer dropped when they repeat, profiles refuse
#         Windows device names and keep the old copy if a save fails half way,
#         a default-on module unticked before the first save stays unticked,
#         windows wider than the screen can be dragged to show either end,
#         the lag line says its figure decays, and the shared Kit gains the
#         gump-layout parser (Kit.gump_parse / gump_cells / cliloc_text) that
#         Grimoire and Social both used to carry, a letter-sum text width
#         (Kit.text_px / Kit.fit) for every module that trims names, a
#         title_bar close tip, Kit.moved_by_code for windows a module places
#         itself, and a cached double-click hook. Every module has its own
#         list of changes in the patch log; nothing saved changes format.
#  2.6.02: trap pings. Trap Highlight puts one Danger! map ping (through
#         Map Pings) on each trap it finds, for you and your guildmates, once
#         per trap; "Ping traps again" on its window pings every trap in range
#         again. On / off on Trap Highlight's settings page (on by default).
#         Map Pings offers HOST.services["pings.send"] for this, paced on its
#         own clock so it never swallows a ping you send yourself.
#  2.6.03: trap ping fixes. A trap ping no longer takes the tracking arrow
#         from a guildmate's ping, and a burst of them no longer pushes
#         guildmates' pings off the screen; a trap that leaves range before
#         its ping is sent is no longer queued twice (the "Sending N" count is
#         right); pausing in the middle of a burst no longer leaves "Sending N"
#         up; a ping that fails outright isn't retried every tick; and Trap
#         Highlight waits out Map Pings' pace instead of asking every tick.
#  2.6.04: Unified Bag without flashes. A bag in a slot no longer shows its
#         own art for a moment when an item moves in or out of it, when it
#         is opened or reopened, or when the client re-shows it; its keeper
#         now runs just before every frame is drawn (also while Character's
#         window is minimized), so it no longer drops into script-driven
#         pinning, and comes back from it by itself.
#  2.6.05: the improvement pass after 2.6.04 (PATCHLOG-2.6.05.md beside this
#         file has every item). In the mother script: one alert service for
#         every module (HOST.alert / HOST.alert_kind: a banner, a client sound
#         and a journal line, rate-limited, with a Settings > Alerts page to
#         pick sounds and mute), guard-zone awareness (HOST.guarded /
#         HOST.guard_area, from the shard's town-guard lines), a Settings >
#         Keys page listing every hotkey with clashes in red (HOST.hotkey_note
#         / hotkey_drop), a What's new window once per version, the Modules
#         tab under headings with a search box (HOST.add category=...), the
#         shared spell tables in Kit (SPELL_WORDS, REAGENTS, MAGERY, mana and
#         cast times, Kit.spell_info), Journal readers that can take only the
#         lines already read (reader.new(False)), and a schedule that keeps
#         going when the computer's clock is set back. Fixed: a settings page
#         a module changes itself is no longer read back over the new values.
#         Every module has its own list of changes in the patch log.
#  2.6.06: nine new modules (PATCHLOG-2.6.06.md beside this file has every
#         item): Lookout (a second client keeps watch and sounds the alarm in
#         this one), Attention (an alarm, and skill loops pause, when staff, a
#         gump or a whisper needs you at the keyboard), Spell Timers, Storage
#         Index (what is in every container you open, on every character of
#         the account, with a search), Corpse Run, Restock, Pets, Harvest
#         Helper and Treasure Hunter. Ultima Tracker offers
#         HOST.services["ultima.classify"], Attention HOST.services
#         ["attention.up"] (Skill Bags pauses while it is up), Spell Timers
#         HOST.services["spelltimers.list"]. Nothing in this script changes
#         but the version, the file list above and the What's new text.
#  2.6.5: the consolidation. 26 shipping modules became 11, grouped by theme,
#         and every one of the 26 is still there as a module or as a PART of
#         one: Character HUD (Unit Frames, Spell Timers, Swing Timer, Bandage
#         Agent, Pets), Inventory (Character, Unified Bag, Storage Index,
#         Restock), World Map (Map Pings, Corpse Run, Treasure Hunter, Harvest
#         Helper, Trap Highlight), Ultima Tracker (+ Lookout) and Skills
#         (+ Skill Bags, Attention). In this script: modules made of parts
#         (HOST.add parts=..., HOST.part_on, the "parts" hook, a PartSet that
#         runs the parts of one file side by side), the Modules tab with a
#         fold arrow per module, parts under it and a search that matches the
#         old names (aliases), a PARTS section at the top of a module's
#         settings page, the record of which parts are on (parts= in the
#         settings, carried over from the 2.6.06 modules= on the first start
#         and written back as the old keys too, so 2.6.06 still starts the
#         same things), old module keys that still answer (HOST.enable,
#         HOST.by_key, HOST.part_running, the Action Bar's mod: cells), a
#         2.6.06 module file left in the folder is skipped with a journal
#         line, HOST.alarm_up(), and the shared helpers Kit.compass /
#         where_text / facet_name / ago / read_int / codec and Kit.arrow (one
#         tracking arrow for every module). Every saved key is unchanged;
#         PATCHLOG-2.6.5.md has every item.
#  2.6.51: window cleanup. In this script: Kit.ART_CIRCLE (a small round
#         button, gump 2117 / 2118) for the windows reduced to simple
#         buttons; HOST.refresh_settings(key) finds the module of a part's
#         key (a part asking for its page to be redrawn by its 2.6.06 key
#         did nothing in 2.6.5); the shared floating window (HubWindow) now
#         only ever holds Ultima Tracker's controls (Map pings has no
#         floating window any more), so it is called Ultima Tracker on the
#         Action Bar; the What's new text. The modules' changes are in
#         PATCHLOG-2.6.51.md.
#  2.6.52: the polish pass. One standard for every window and every piece
#         of text (titles, captions, tooltips, labels, section titles,
#         journal lines), in every module and here: the same title row
#         with the same tooltips (Kit.title_bar / mini_bar), parts named
#         the same everywhere they appear (a part's window title, journal
#         prefix and tray name are its name on the Modules tab: Frames,
#         Buffs & Timers, Swing Bar, Bandages, Pets, Bags, Paperdoll,
#         Storage, Restock, Map Pings, Corpse, Treasure Maps, Ore Tracker,
#         Traps & Fields, Tracker, Lookout, Skills Window, Training Alarm,
#         Skill Bags), shorter and plainer wording throughout, debug boxes
#         in a DEBUG section at the end of each page, sentence-case
#         captions, one tooltip on every control. No feature or saved key
#         changed. The modules' changes are in PATCHLOG-2.6.52.md.
#  2.6.53: no window is ever taller than the screen. A window that grows
#         past the screen's height (a long list, a tall settings page, a
#         small screen) used to hang off the bottom; now Kit.place cuts it
#         to the screen's height and its body scrolls, with the client's
#         own scrollbar down its right side, the title row staying put
#         (Kit.scroll_fit; the window grows Kit.SCROLL_BAND px to the right
#         for the bar). It is done for every window of every module, with
#         no change to the modules: the controls keep their coordinates,
#         and controls a module adds later are swept into the scrolling
#         part by the keeper (Kit.scroll_sweep, with Snap.keep). The
#         Virtue Assistant window passes its own fixed head (title and
#         profile bar) to Kit.place. No saved key changed.
#  2.6.54: the layout: zones round the game area that the module windows sit
#         in (the Layout, ZoneSet, Zone, LayoutEditor and LayoutPage classes;
#         Settings > Layout). A FRAME LAYOUT is the set of zones (Default is
#         generated from the screen: a left band of paperdoll / bags / chat,
#         the frames strip over the game and the bars under it, a right band
#         of map / tracker / meters, spill bands on an ultrawide screen; any
#         other is drawn by the player in the editor, on the screen grid, and
#         reflows by fractions and pins on every screen); a WINDOW LAYOUT
#         says which window sits in which zone (Default, Mirrored, the
#         player's own). A window dragged on to a zone is slotted there and
#         let go anywhere else is free again; windows stack in a zone and a
#         window taller than its slot scrolls (Kit.place max_h=). A window is
#         known by its dock key: Kit.dock_hooks offers its gump, Host.dock_add
#         lists it (Host.layout_add for a window with no tray button: the two
#         frames, the bar, Bags, Grimoire); HOST.layout_holds tells a module
#         its window is placed by the layout. Snap.on_drop tells the layout
#         about a let-go drag. New keys only (VirtueAssistant_layout*,
#         VirtueAssistant_frames*); nothing moves until a window layout is
#         picked or a window is dropped on a zone.
#  2.6.55: every window can be given its zone from the settings, and a window
#         fits the zone it sits in. A WINDOWS section on every module's
#         settings page lists the module's windows with a "Zone: <name>"
#         button that cycles through free and every window zone of the frame
#         layout in use (ConfigWindow._draw_windows, Layout.assign_to); the
#         Layout page lists every window of every module the same way, with
#         a drop-down each. A zone has a FIT (Zone.fit, the editor bar's
#         "Fit:" button): fill width (a window is drawn as wide as the zone,
#         50% to 150% of its size), shrink only (a window wider than the zone
#         is drawn smaller, never bigger) or none. The layout fits a window
#         in one of two ways (Layout._fit_window, 2.6.55): a window whose hooks offer
#         "fit" is told the zone's size and fits itself with its own scale,
#         width or orientation setting (the Action Bar turns upright in a
#         tall zone, Frames, Grimoire and Ultima Tracker set their scale,
#         Bags its columns, Skills its width); a window whose hooks
#         say "scale" (a window its module rebuilds whole and never moves a
#         control of after building) is scaled by the layout itself, with the
#         client's own control scaling (Kit.scale_window, as the Virtue
#         Assistant window has been scaled since 2.5.x), again each time it is
#         rebuilt, and placed at its scaled size; a window with neither is
#         placed and cut to its slot as in 2.6.54. Kit.dock_hooks takes
#         scale=True and offers "redraw"; Host.layout_add takes a hooks dict.
#         A zone's fit is one more field of its saved form (an old form reads
#         as fill width); no other saved key or format changed.
#  2.6.56: a window fills its zone exactly. The windows of a zone share it
#         edge to edge (Layout._slots: each as wide as the zone and a share
#         of its height by its own size, or the other way round across a zone
#         that stacks right; a minimized one keeps its bar's height; no gaps)
#         and every window is made exactly its slot's size (Layout._fit_slot):
#         a module whose hooks say "fit" and "exact" makes it so itself (the
#         tracker's groups and its Combat window, Grimoire); every other window
#         is fitted by the layout (Fill), after its module drew it: the frame,
#         sections and bars stretch, text, buttons and art keep their size and
#         are anchored in their section, a list too tall for its slot scrolls,
#         and nothing is ever outside the window. "fit" modules still get close
#         first (the Action Bar's scale both ways, Frames' scale, Skills' width
#         and rows, Bags' columns and slot size). A module that moves its own
#         controls after drawing does it through Kit.ui_pos / ui_rect / ui_w /
#         ui_h / ui_size (Kit.ui_x / ui_y read back). The client's control
#         scaling ("scale" hooks) is no longer used for this. (2.6.78: wrong
#         for this build: the client draws labels, buttons and checkboxes
#         at a control's scale; Fill scales windows again, see Fill.) The
#         zone's Fit button is gone (every zone
#         fills; the saved field is kept and read as before). Character HUD:
#         Bandages and the Swing Bar are two-row panels of the same width.
#  2.6.57: the zone fixes. A window with windows attached to it (the Action
#         Bar's tray, a meter's side window) is fitted too, to its slot less
#         the room they take, and they keep their place beside its new edges
#         (Fill.beside); the hooks' "pieces_out" keeps a frame on its slot
#         with its pieces riding outside it. TazUO's World Map is the window
#         "worldmap" (ClientWin: a client window the layout places and sizes
#         through ResizeWindow, held while it sits in a zone, given back its
#         own place and size when freed); the client's journal lives in the
#         first reserved zone the same way (the chat line stays where TazUO
#         puts it). Kit.detach / Kit.attached_to undo and read Kit.attach.
#         Buffs & Timers, Bandages and the Swing Bar are no zone occupants any
#         more (LAYOUT_GONE: a saved layout naming them loads without them).
#         Modules: Paperdoll, Meters, Social and the Action Bar draw
#         themselves exactly their slot ("fit" + "exact"); the HUD's pieces
#         ride on the player and target frames.
#  2.6.58: ClientWin reads a client window's rect from its _bounds field (its
#         X / Y / Width / Height are by-reference properties IronPython can't
#         read: in 2.6.57 every read failed, so TazUO's World Map and the
#         journal were never placed). Modules: the Paperdoll stacks its bags
#         under the doll in a zone; Bandages and the Swing Bar are built to
#         the design (161 px wide); Ultima Tracker's own window groups stand
#         down for windows in zones (Combat included); Meters and Social are
#         never wider than their share.
#  2.6.59: Character HUD only. Bandages' "Show who the bandage is on" is off
#         by default (it widened the panel by 90 px, so the panel never came
#         out at the design's width); the repeat arrow is drawn from the ring
#         (gump 236 is a framed stone button); the readout room of both
#         panels is the widest of their words, the same in both (readout_room).
#  2.6.60: the journal in its reserved zone stops above TazUO's chat line
#         when the chat line would sit behind it (Layout._chat_line: the line's
#         top, read from the client's SystemChat every CHAT_LOOK s), so the
#         text you type shows below the journal.
#  2.6.61: Ultima Tracker only. A tracker window in a zone narrower (or
#         shorter) than the tracker's own smallest size is made exactly its
#         slot: it was held at that smallest size (210 px at 100%), so it ran
#         past its zone and over the window beside it. The Combat window is
#         made anew when its slot is narrower than the smallest it was made with.
#  2.6.62: Character HUD only. The player and target frames in zones draw
#         themselves at their slot's size ("fit" + "exact"): the stone frame and
#         a black section behind the art, the art at its circle's side (player
#         left, target right), so frames in zones side by side mirror each
#         other. Bandages and the Swing Bar line up with the end of their
#         frame's bars (the player frame's right, the target frame's left).
#  2.6.63: TazUO's World Map (and the journal in a reserved zone) really held
#         in its zone. ClientWin.fit was a one-shot: it asked for the size once
#         (ResizeWindow, applied on the client's next frame) and never looked
#         again, so a size that didn't take, the player's own resize, the
#         map's double-click fullscreen or its click handler (which turns
#         dragging back on) left it wherever it went. Now every pass checks the
#         window's real place and size against its slot and puts it back
#         (ResizeWindow, else its saved-size field; Location, else its bounds),
#         locks it with the client's own lock (no drag, no border or resize
#         grip sticking out of the zone) and gives the lock back when freed.
#         When it still won't take, one journal line says why.
#  2.6.64: Meters, and two Host helpers for it: Host.layout_slot(key)
#         (the size the layout wants a slotted window to be) and
#         Host.layout_drop(g) (slot a window its module saw let go). A meter
#         window is resizable by its corners when free, and checks its zone
#         slot itself every half second, so it always conforms to its zone.
#  2.6.65: Social only. The Guild tab laid out for a narrow zone: Refresh,
#         Guild window, Diplomacy and Sort no longer run under the page arrows
#         (the arrows go up beside the guild's name and the captions give way,
#         last button first); toolbars that still don't fit wrap onto another
#         line; roster columns that don't fit are left out (their text is in
#         the row's tooltip); every info line is cut to the width it has.
#  2.6.66: the combined Paperdoll and Bags window takes two zones, one over
#         the other: the doll in the top one, the bags in the one under it.
#         Layout.pair_below (HOST.layout_pair) finds the zone flush under the
#         window's own, moves the bags there, or makes one: in the free room
#         under the zone, else by splitting the zone in two; a Default frame
#         layout changed this way is saved as "Default (mine)". Layout.keep
#         never places a window whose "riding" hook says it rides in another
#         window, but counts its zone as taken. Modules: the Paperdoll draws
#         the doll in its slot and the bag grid in the zone under it, and has
#         a small arrow on the edge facing the screen's centre that pops the
#         Storage window out beside it (Storage's "storage.flap" service).
#  2.6.67: Character HUD only. With the player and target frames in zones,
#         Bandages and the Swing Bar sit inside their frame's zone, beside
#         the art past the end of its bars, when there is room there (else
#         outside it as before); the frame leaves a hole in its background
#         behind the piece and keeps the piece in front of it.
#  2.6.68: Inventory only. The combined Paperdoll and Bags window never runs
#         past the zone under the doll (onto the journal): a bag grid with
#         more rows than that zone holds is shown at a smaller container
#         scale until it fits (Bags' "bag.shrink" service); the player's own
#         Bag scale comes back when there is room again, when the bags part
#         from the Paperdoll and when Bags stops.
#  2.6.69: windows in zones are held to their slots. Layout._verify measures
#         every window whose hooks say "verify" on each keeper pass and tells it
#         its slot again (mode "again") while its real size isn't the slot's
#         (Ultima Tracker's groups and Combat, Meters, Social). A window's
#         "inset" hook (TazUO's World Map: 4 px) makes it that much bigger than
#         its slot on every side, so what it draws fills the zone.
#         Layout._client_drops: the free World Map dragged and let go on a zone
#         is slotted there, as a script window is. Host.layout_rect(key): the
#         slot's rect, for a module that makes its window anew in a zone.
#         Modules: Ultima Tracker's groups are made anew at exactly their slot
#         (where the slot is) whenever their real size isn't it, and can't be
#         corner-dragged while in a zone; Meters' side windows no longer take
#         room from its zone ("pieces_out"), and Meters and Social draw
#         themselves again when the layout measures them off their slot.
#  2.6.70: no flicker, firmer zones and one frame. Kit.rect / Kit.note_rect:
#         a window's place as asked until the client applies it (a window just
#         made read 0, 0, 0 x 0 for a frame, and the frames' Bandages and Swing
#         Bar were put against that, at the top-left corner, over and over);
#         Snap.rect / pos and the modules that place a window beside another
#         read through it. A window let go over a window zone no longer snaps
#         to its neighbours first (Layout.takes); one moved from a zone on to a
#         zone holding one window swaps with it; the layout fits them on the
#         next pass. A window the layout measures ("verify") that is still off
#         its slot after MISFIT_FILL passes is stretched to it by the layout
#         (Fill). Kit.render_scale reads Client.Game.RenderScale by reflection
#         (ClassicUO.Client is internal). Surround: Settings > Layout's
#         "Join zone windows in one frame" (off by default) draws one stone
#         surround under the zones, a gold border round the game area,
#         and hides the stone frames of the windows in zones. Settings >
#         Layout's Check fit prints where each window in a zone sits.
#  2.6.71: fixes. Layout.dropped: a reorder inside one zone of two windows
#         no longer swaps one out of it. LayoutEditor: a renamed zone is made
#         again (its move / resize / select callbacks carried the old name),
#         its name is cleaned (Layout.clean_name, never "frames") and its
#         windows go with it on Save. Host.disable from inside a part turns the
#         module off when its last part goes; Host.report switches off only the
#         failing part and clears the count; Host.enable cancels a pending stop.
#         Kit._scroll_undo notes the frame again; Fill.change applies a new size
#         to a fixed-size control. Modules: Inventory > Paperdoll fills its zone
#         (wider panel, stats as a column beside the doll when that draws it
#         bigger) and equips a dropped item again (the layer from the cursor's
#         tile data: a held item isn't in the client's item list); Bags in a
#         zone of its own re-shares its slot at each build; Ultima Tracker,
#         Social, Meters, Character HUD, Action Bar, Property Butler and Skills
#         fixes (see PATCHLOG-2.6.71.md).
#  2.6.72: zones hold their windows, one look, the arched game view.
#         Layout._hold / _release: a window in a zone can't be dragged (CanMove
#         False, checked every pass); Arrange mode (Layout.set_arrange: Settings >
#         Layout's Arrange windows, the Action Bar's Lock button, Esc, or
#         ARRANGE_IDLE s without a drag) shows the zones' outlines and names and
#         lets them move; a drop outside it changes nothing. Host.layout_locked /
#         layout_arrange / layout_arranging / layout_in_use / layout_unified for the
#         modules. The swap guard (Layout._too_small, a "min" hook or a client
#         window's own minimum) and no snap links to or from a held window.
#         ClientWin._lock writes CanMove on every pass (TazUO's World Map turned
#         dragging back on after a click). The one inset: Layout._slot_insets /
#         _grow make every zoned window's panels Kit.ZONE_INSET (4) in from its
#         zone (the border band more on the surround's outer edges), so seams
#         between zones are Kit.GAP; Kit windows keep their hidden MARGIN round
#         that, TazUO's World Map its 4 px, the journal is inset the same way.
#         Surround: gold outside the game area, knots only on the screen's
#         corners, Surround.early hides a rebuilt zoned window's frame before it
#         is drawn, scroll knots are noted as frame (Kit._note_frame_part,
#         Kit.hide_zone_frame), Check look (Layout.look_problems / report_look,
#         Kit.note_title). The editor's Even out (ZoneSet.even_out). The centre
#         band: Zone.hug and Zone.arch (two more saved fields, written only when
#         set; older forms read as off), Layout._arch_on / _apply_hug (a Default-
#         shaped layout gets corner zones and the arch while Settings > Layout's
#         "Arch the game view between your frames" is ticked with one frame on),
#         Surround.arches / build_arch (stone shoulders in 4 px rows with the gold
#         along them, above the game view), Layout._game_view (TazUO's game window
#         is the arched zone; your own place and size kept in Layout_gameview_own
#         and given back). The ping readout (Layout._ping_tick, off by default).
#         Kit.mouse_pos. Modules: see PATCHLOG-2.6.72.md.
#  2.6.73: the zone fixes after 2.6.72. Surround: the stone backdrop is kept
#         the client's very last window (Surround._pin; TazUO's sort turned the
#         "Under" windows round on every click, so a rebuilt bag grid went under
#         the stone and its black vanished), and the gold border and the arch's
#         shoulders are drawn in a window of their own above the game view
#         (Surround.edge_g); the arch's curve is a picture made in memory (Tex,
#         Surround._arch_pixels: stone from the crown's own tiling, the gold
#         anti-aliased along the curve), the 4 px stair only when the client
#         can't make one. Layout._apply_hug: a corner zone also grows down when
#         its window needs the height ("hug" gives (width, height)). Layout.
#         dropped: a zoned window dropped outside every zone goes back to its
#         zone (Settings > Layout's zone buttons free a window); TazUO's World Map
#         shares its zone with no window (Layout._map_zone). Layout._repair (once
#         per character): windows sharing the map's zone, and Ultima Tracker or
#         Meters windows left free by a drop, back in their zones. Modules: see
#         PATCHLOG-2.6.73.md.
#  2.6.74: the fixes after 2.6.73 and the zone editor's features. Kit.pin_size
#         (the client's WantUpdateSize auto size is off for every window placed
#         with Kit.place, so a zoned window whose frame was hidden before its
#         first Update no longer comes out MARGIN short). Snap keeps the key and
#         rect of a dragged window, so a drop survives its window being made anew
#         (Snap.lost, Layout.dropped's key / rect); Kit.just_dragged (a title
#         strip's double-click ignores the click that ended a drag). Layout:
#         the standing repair (_repair every REPAIR_EVERY s; FREED_VAR and
#         HOMES_VAR), debug lines (debug_line, _drop_said), Check zones
#         (report_zones), _client_overflow (a client window bigger than its zone
#         overflows where it covers least), the zone names on plates at the
#         bottom of Arrange mode's outlines, _apply_hug in two passes, the seams
#         in Check look. Surround.build: stone over the whole screen, the border
#         band on the screen's edges and round the game area; _slot_insets per
#         edge. Zone.overlap and Zone.lock (eleventh and twelfth saved fields),
#         ZoneSet.ver ("v=2" in the saved head), Layout._overlap_shape (a keep-
#         clear zone with Overlap on: its own arched or straight top). The
#         editor (LayoutEditor) rewritten: typed values used on Enter, focus
#         loss or Apply; measured rows; gaps and overlaps striped and counted;
#         the zone's windows with a preview (Layout.slots_for / preview_text);
#         undo, keys, edge handles, duplicate, align, lock, presets, Save's notes.
#         Modules: see PATCHLOG-2.6.74.md.
#  2.6.75: Surround.build leaves every keep-clear zone open again (2.6.74 tiled
#         the stone over the whole screen, but TazUO draws the world before every
#         gump, so the stone hid the game view): the stone covers the screen less
#         the keep-clear zones, with any window or reserved zone lying over one
#         still stone (Surround._stone_rects). Modules: see PATCHLOG-2.6.75.md.
#  2.6.76: no change to the mother beyond the version. Modules: see
#         PATCHLOG-2.6.76.md.
#  2.6.77: no change to the mother beyond the version. Modules: see
#         PATCHLOG-2.6.77.md.
#  2.6.78: Fill scales a window that is bigger than its slot instead of
#         squeezing it (Fill.scale_for, FILL_MIN_K; SQUEEZE gone): every control
#         is drawn at k with the client's own scaling, a text field keeps its
#         height as far as its neighbours allow, a window with a list area of
#         its own is never scroll-converted, and a converted window keeps its
#         band. Kit.title_bar fits its row (Kit.title_plan: captions first,
#         then the label after the title, then the title is cut; Kit.caption_tip)
#         and takes extra buttons and a label after the title. Check look also
#         lists controls over one another, outside their section or cut
#         (Overlaps); Check fit says the scale a window is drawn at
#         (Layout.drawn_at, the hook "drawn_at"). Kit.note_scene,
#         Kit.add_textbox(font=). Modules: see PATCHLOG-2.6.78.md.
#  2.6.79: no change to the mother beyond the version. Modules: see
#         PATCHLOG-2.6.79.md.
#  2.6.80: no change to the mother beyond the version. Modules: see
#         PATCHLOG-2.6.80.md.
#  2.6.81: the fixes after 2.6.80. The shared holds of every loop that acts
#         by itself (Host.fight_hold, foe_near, guard_hold; HOLD_TEXT, FOE_*,
#         HURT_SECS): one fight test and one guard-zone rule, an unknown zone
#         holding (the shard's rules, strict reading), and Host.cursor_ok (a
#         module aims only a cursor of the kind its own press raised).
#         Kit.CAST_EXTRA (the shard's +0.5 s on every Magery cast time, in
#         spell_info). Kit._place_raw stores the slot, not the screen, as a
#         scrolled window's cap; Kit.note_rect drops a landed request first.
#         Host.save_prefs / _migrate_parts keep the parts of a module that is
#         off (parts_off=). Profiles.clean renames ".old" / ".saving"; profile
#         export copies on the script thread. Layout: holds / locked need the
#         zone in the frame layout in use (the Layout page lists a missing one),
#         _release redraws a window freed while locked, dropped keeps the stack
#         order, load resets freed / homes, pair_below draws the arch and
#         _free_under sees it, keep disposes the ping readout, the unified box
#         recomputes the zones, the editor's New from Default / Reflow drop the
#         renames; ZoneSet._band_heights gives an empty slot only EMPTY_SLOT.
#         Settings > Alerts heading. Modules: see PATCHLOG-2.6.81.md.
#  2.6.82: the speed pass (DIRECTIONS-speed-after-2.6.81.md). Shared reads
#         per pass for every module (HOST.me, HOST.mobiles, HOST.mobile,
#         HOST.pack_items, cached only inside the client hop: _Memo); thread
#         work opt-in (thread_wanted); PartSet with precomputed owner /
#         interval maps that wakes at the next due part; per-pass memos of
#         Follow.current, Typing.now and fight_hold; settings pages and hub
#         polled fast only after input; Snap / Layout keepers read each window
#         once per look; cached reflection in Kit.client_control. Modules:
#         see PATCHLOG-2.6.82.md.
#  2.6.83: bug pass after the speed pass. The shared mobile scan is sorted
#         nearest first; Typing.release drops the pass's kept answer; a
#         scrolling window's sweep looks again after a failed flush; hub
#         sections get a last read when they close; the layout editor's
#         "Put it here" right after a pick is kept; Fill lets go of its
#         wrappers; a layout refit gets a full on-screen look. Modules: see
#         PATCHLOG-2.6.83.md.
#  2.6.87: the Art looks made again as one work: class Wyrm paints carved stone, one
#         thread of old gold, an arched crown with a keystone and, with the dragons
#         look, two dragons on plinths framing the Action Bar. See PATCHLOG-2.6.87.md.
#  2.6.86: Reclaim space grows only the game area and the gaps beside it, never a
#         frame's zone, and its Undo survives a restart; a layout it stretched is
#         repaired once. The Art looks now show with no gaps between the zones.
#  2.6.85: the update after 2.6.84: a window in a zone is always up (Kit.title_bar,
#         HOST.zone_up_tick), the bar rows and the game view's fit in the layout,
#         Reclaim space, the frame's art, the system stats button, a key on any
#         button (Binds). Modules: see PATCHLOG-2.6.85.md.
#  2.6.84: second bug pass. A part's errors on its settings page or hub
#         section switch off that part only; closing the shared tracker
#         window turns off its Tracker part only (Lookout stays); a part
#         turned on from the script thread starts in one client hop; a
#         cursor claim, the fold-to-bar, Action Bar link and window keeper
#         survive the clock being set back. Modules: see PATCHLOG-2.6.84.md.
#
#  Ultima Tracker's controls sit in the shared floating window (HubWindow;
#  "Tracker & Pings" before 2.6.51, when Guild Pings had a section in it
#  too) that folds into a tray button on the Action Bar.
#
#  Usage:
#    1. Put this file in your TazUO/LegionScripts folder, with the
#       VirtueAssistantModules folder beside it, and run this file from the
#       Legion Script Manager. Run only this one: not the module files, and
#       not an older all-in-one Virtue Assistant at the same time.
#    2. The Virtue Assistant window opens. Tick a module to turn it on, untick
#       it to turn it off. Your choice is remembered per character.
#    3. The small down arrow in its title bar folds the window into a gear.
#       Click the gear to open the window again; drag it anywhere you like.
#       The gold arrow beside it folds the window into the Action Bar
#       instead (no gear; the bar's Virtue Assistant button opens it).
#       Drag any corner of the window to resize it. Its sections (the module
#       list, the options, the module buttons and every section of a module's
#       settings page) run top to bottom, then on into the next column, left
#       to right, to fill the size you dragged to: wide and short gives many
#       short columns, tall and skinny one long one. When you let go the
#       window shrinks to its sections, so no space is left empty. The - and
#       + at the top right scale the whole window (click the percentage for
#       100%). Size and scale are remembered per character.
#    4. A module's own window closes only from its X button (which turns the
#       module off) or by unticking it here; right-clicking a window does
#       nothing. Tick it again in the Virtue Assistant window to bring it back.
#    5. The X on the Virtue Assistant window stops everything.
#    6. The Action Bar's Virtue Assistant, Grimoire and bag buttons open
#       those windows, or fold them into the bar when they are open.
#
#  Hotkeys never fire while you are typing: in the chat line, in a field of
#  any Virtue Assistant window, or in any other text box of the client (a
#  search box, a rename field, the Legion script editor ...). Click the game
#  world, or another window, to leave a field; the hotkeys work again.
#
#  Everything you arrange is remembered per character the moment you do it:
#  where each window sits (saved when you let go of it), whether it is
#  minimized or folded into the Action Bar, which modules are on, and each
#  module's own view choices. Start Virtue Assistant and everything comes
#  back as you left it.
#
#  Every window uses the client's own gump art: the stone frame of the
#  crafting gump, its black sections, the UO font in client hues and the
#  standard gump buttons. The art ids are in the Kit class below if your
#  client shows any of them oddly.
#
#  Each module keeps the saved settings of the script it came from, so your
#  Ultima Tracker foe list, runebook lists and so on carry straight over.
#  Each module's CONFIG section is near the top of its own module file.
#
#  Profiles (the bar under the title, on both tabs): a profile is a copy of
#  one character's whole setup that any other character can load.
#    - Save: stores this character's setup under the name typed in the box
#      (a new profile), or over the profile picked in the list when the box
#      is empty.
#    - Load: puts the picked profile on this character. Every module is
#      stopped, given the profile's settings and started again.
#    - Star: makes the picked profile the favourite (click again to clear
#      it). Every character that hasn't loaded another profile itself gets
#      the favourite when Virtue Assistant starts, new characters included,
#      and gets it again whenever the favourite is saved anew. The favourite
#      is also made TazUO's default profile (default.json / macros.xml), so
#      a brand-new character starts with its client settings even before
#      Virtue Assistant runs.
#    A profile holds: every module's settings and window places, which
#    modules are on, the Bags layout; and TazUO's own settings from
#    the Options window (profile.json, cooldown bars, grid highlights and
#    bands, screen effects, tooltip overrides, name plates, info bar) and
#    the Legion Assistant window (its options, agents' settings, auto loot,
#    organizer, journal filter, buy / sell lists, macros, hotkeys). Things
#    tied to one character's own items stay with that character: runebook
#    and spellbook data, Bags slot assignments, Dress Agent outfits,
#    the grab bag and saved mount / weapon serials. Assistant settings that
#    TazUO already shares across characters (friends, scavenger, graphic,
#    sound and music filters, spell indicators) need no profile.
#    Profiles are folders in LegionScripts/VirtueAssistantProfiles; delete
#    a folder there to delete that profile.
# =============================================================================
import API
import math
import os
import re
import struct
import time

APP_NAME = "Virtue Assistant"
APP_VERSION = "2.6.87"     # the file is named after it: VirtueAssistantV2-6-87.py. A new
#                            version is a NEW folder (the mother script and every module
#                            inside it), beside the old one, never an overwrite.
MODULE_DIR = "VirtueAssistantModules"   # folder of module files, next to this script
SETTINGS_KEY = "VirtueAssistant_settings"
HOST_TICK = 0.02           # seconds between passes of the main loop
UI_TICK = 0.05             # seconds between looks at the script's own windows
LAZY_MODULES = True        # compile a module file only when the module is first turned on
#                            (or its settings page is opened); the others are listed from
#                            their registration line alone, so start-up is the enabled
#                            modules' cost only
GRID_DEFAULT = 32          # pixels between the lines of the screen grid (GRID button)
SNAP_ANCHOR = 40           # pixels within which a let-go window snaps to a screen anchor
#                            (corners, edge midpoints, centre); edges use SNAP_DIST
KEEP_EVERY = 0.5           # seconds between looks for a window that is off the screen
GEAR_ITEM = 0x1053         # item art drawn on the minimized gear ("gears")
HUB_ITEM = 0x1057          # item art on the Action Bar's Ultima Tracker button (sextant)
MAX_MODULE_ERRORS = 25     # a module that keeps failing is switched off
PROFILE_DIR = "VirtueAssistantProfiles"   # saved profiles, next to this script
PROFILE_STATE_KEY = "VirtueAssistant_profile"   # per character: which profile it follows
PROFILE_NAME_MAX = 32      # longest profile name

# ---- alerts (HOST.alert, 2.6.05): see the Alerts class ----
ALERT_RATE = 10.0          # seconds: the same alert (key + who, or key + text) at most this often
ALERT_HOLD = 8.0           # seconds a warn / info banner stays up (an alarm waits for a click)
ALERT_SOUND_GAP = 0.4      # seconds between two alert sounds (a burst plays them in turn)
ALERT_FLASH = 0.5          # seconds between the flashes of an alarm banner
ALERT_SOUNDS = (           # (name, client sound id in Sound.mul) offered on Settings > Alerts
    ("Silent", 0), ("Chime", 0x1EA), ("Harp note", 0x3D0), ("Lever", 0x04A),
    ("Whistle", 0x335), ("Yell", 0x338), ("War drum", 0x2E7), ("Trap snap", 0x1EF),
    ("Boom", 0x307), ("Recall", 0x1FC), ("Heal tone", 0x202), ("Bird", 0x017),
    ("Smack", 0x3B2), ("Harm", 0x1F1), ("Cure", 0x1E0))
# ---- guard zones (HOST.guarded, 2.6.05): see the Guard class ----
GUARD_IN_TEXTS = ("you are now under the protection of the town guards",)     # cliloc 500112 / 500114
GUARD_OUT_TEXTS = ("you have left the protection of the town guards",         # cliloc 500113
                   "beware! you have left the protection of the town guards") # cliloc 500115
#  Used only while the state isn't known yet (no line since the script started
#  and no saved state for the spot you stand on): (facet, x1, y1, x2, y2, name),
#  facet 0 Felucca, 1 Trammel, 2 Ilshenar, 3 Malas. Empty until the town bounds
#  of In Mani Ylem are filled in; add a line per guarded town to use it.
GUARD_AREAS = ()
GUARD_SPOT = 3             # tiles: a saved state counts while you stand this close to where it was seen
# ---- the shared holds of every loop that acts by itself (2.6.81): HOST.fight_hold,
#      HOST.guard_hold, HOST.foe_near (one fight test, one guard-zone rule: R3) ----
FOE_RANGE = 12             # tiles: a hostile this close holds every loop
FOE_EVERY = 1.0            # seconds between two looks at the mobiles around you (shared)
FOE_NOTO = (5, 6)          # enemy, murderer (API.Notoriety): always count
FOE_WAR_NOTO = (3, 4)      # grey (attackable), criminal: count while in war mode
HURT_SECS = 10.0           # seconds a loop stays held after your HP dropped
HURT_FRESH = 2.0           # seconds an HP reading stays fresh enough to compare with
HOLD_TEXT = {              # the wait reason each hold shows (status lines, journal)
    "dead": "you are dead",
    "war": "war mode",
    "hurt": "you took damage",
    "foe": "a hostile is near",
    "item": "you are moving an item",
    "alarm": "an alarm needs you",
    "guard": "guard zone",
    "unknown": "Guard zone not known yet: cross a town's guard line once",
}
# ---- the Modules tab (2.6.05): modules are listed under these headings, in this
#      order (HOST.add category="..."); any other heading comes after them, by name
CATEGORY_ORDER = ("On screen", "Your things", "The world", "Skills and home", "Extras", "Other")
SEARCH_SETTLE = 0.5        # seconds after the last key in the Modules search box before it filters
# ---- "What's new" (2.6.05): shown once per account the first time this version
#      runs; empty = no window. Never mentions anything but shipped modules.
WHATS_NEW_KEY = "VirtueAssistant_seen_version"     # per account: the version last shown
WHATS_NEW = (
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
    "facing the middle of the screen, pops the Storage window out beside it and tucks it away "
    "again.",
    "2.6.65: Social's Guild tab fits its zone: its buttons, the page arrows and the roster "
    "no longer draw over one another or past the edge when the zone is narrow.",
    "2.6.64: Meters fits its zone. A meter window in a zone is drawn at exactly the zone's "
    "size, with as many rows as the height holds, and follows the zone when it changes. Out "
    "of a zone, drag any corner of a meter window to resize it; the Rows setting or Reset "
    "sizes (Meters settings page) gives it back its own size.",
    "2.6.63: TazUO's World Map now fills the zone you put it in, edge to edge, and stays "
    "there: it is locked while it sits in a zone and gets its own place, size and lock back "
    "when you free it.",
    "2.6.62: the player and target frames in zones mirror each other: your frame sits at the "
    "left edge of its zone and the target frame at the right edge of its own, each on the "
    "same stone and black background as the other zone windows. The Swing Bar now sits "
    "under the left end of the target frame's bars, mirroring Bandages under the right end "
    "of yours.",
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
    "Trap Highlight is Traps & Fields, Attention is Training Alarm. The search box still finds "
    "the old names.",
    "Nothing else changed: every setting, window place, list, hotkey and file is kept, and every "
    "button does what it did.",
    "From 2.6.5: 26 modules became 11. The old modules are PARTS of a themed module, each with "
    "its own box (click the arrow on a module's row to see them).",
)


class _Gumps(object):
    """API.Gumps, with right-click closing turned off on every window it adds:
    a module is turned off from the Modules list (or its own X button), never
    by a stray right-click on one of its windows."""
    def __init__(self, inner):
        self._inner = inner

    def __getattr__(self, name):
        # (2.6.82) found once, then a plain attribute: no __getattr__ and no .NET
        # member lookup on every G.Create* (AddGump is the class's own, never here)
        v = getattr(self._inner, name)
        self.__dict__[name] = v
        return v

    def AddGump(self, g):
        try:
            g.CanCloseWithRightClick = False
        except Exception:
            pass
        try:                            # (2.6.74) a window given its size keeps it: the
            p = Kit._pend.get(g)        # client's auto size is off before its first Update
            if (p is not None and p[2] and p[3]) or g in Kit._scrolled:
                Kit.pin_size(g)
        except Exception:
            pass
        try:                            # (2.6.72) made where a zoned window sits, one frame on:
            LAYOUT.surround.early(g)    # its frame hidden from the start (no half-second flash)
        except Exception:
            pass
        r = self._inner.AddGump(g)
        try:
            SNAP.add(g)                 # every window snaps to the others
            LAYOUT.fresh_adds.add(g)    # (2.6.55) a new window: the layout fits it on its
        except Exception:               # next look, not up to KEEP_EVERY later (2.6.82: an
            pass                        # overlay that never snaps takes itself off: skip_gump)
        return r


G = _Gumps(API.Gumps if hasattr(API, "Gumps") else API)   # newer / older TazUO builds


def safe(fn, default=None):
    """fn(), or default if it raises. Every module leans on this one, so it is
    kept as small as Python allows; the mother's own per-pass code uses plain
    try / except instead (no lambda to build on every call)."""
    try:
        return fn()
    except Exception:
        return default


# =============================================================================
#  Client - the few things scripts can't ask TazUO for: the mouse's
#  double-click timer and the Alt / Shift keys. Found by name among the
#  client's loaded assemblies, so it works whatever the assembly is called.
# =============================================================================
class Client(object):
    looked = False
    mouse = None              # (get, set) of Mouse.LastLeftButtonClickTime
    keys = {}                 # "alt" / "shift" -> getter
    NO_CLICK_TIME = 1         # "last click was long ago" (0 / max mean a double-click)

    # Type lookups are remembered: a scan of every loaded assembly (IronPython
    # alone makes dozens of them) was repeated by every caller. The client's own
    # assembly is asked first; a name that isn't found is looked for again at
    # most every TYPE_RETRY seconds (an assembly may load later).
    _types = {}               # full name -> Type, or (None, time of the miss)
    _client_asm = False       # the client's assembly (False: not looked for yet)
    TYPE_RETRY = 30.0

    @staticmethod
    def _type(name):
        hit = Client._types.get(name)
        if hit is not None:
            if type(hit) is not tuple:
                return hit
            if time.time() - hit[1] < Client.TYPE_RETRY:
                return None
        t = None
        try:
            if Client._client_asm is False:
                Client._client_asm = None
                try:
                    Client._client_asm = API.GetType().Assembly
                except Exception:
                    pass
            asm = Client._client_asm
            if asm is not None:
                try:
                    t = asm.GetType(name, False)
                except Exception:
                    t = None
            if t is None:
                import System
                for asm in System.AppDomain.CurrentDomain.GetAssemblies():
                    try:
                        t = asm.GetType(name, False)
                    except Exception:
                        t = None
                    if t is not None:
                        break
        except Exception:
            t = None
        Client._types[name] = t if t is not None else (None, time.time())
        return t

    @staticmethod
    def _member(t, name):
        """(get, set) for a static property or field of a .NET type."""
        import System
        from System.Reflection import BindingFlags
        flags = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
        p = t.GetProperty(name, flags)
        if p is not None:
            return (lambda: p.GetValue(None, None),
                    lambda v: p.SetValue(None, System.Convert.ChangeType(v, p.PropertyType),
                                         None))
        f = t.GetField(name, flags)
        if f is not None:
            return (lambda: f.GetValue(None),
                    lambda v: f.SetValue(None, System.Convert.ChangeType(v, f.FieldType)))
        return None

    @staticmethod
    def find():
        if Client.looked:
            return
        Client.looked = True
        mouse = Client._type("ClassicUO.Input.Mouse")
        if mouse is not None:
            try:
                m = Client._member(mouse, "LastLeftButtonClickTime")
                int(m[0]())
                Client.mouse = m
            except Exception:
                Client.mouse = None
        kb = Client._type("ClassicUO.Input.Keyboard")
        if kb is not None:
            for key, name in (("alt", "Alt"), ("shift", "Shift"), ("ctrl", "Ctrl")):   # (2.6.74) Ctrl
                try:
                    m = Client._member(kb, name)
                    bool(m[0]())
                    Client.keys[key] = m[0]
                except Exception:
                    pass

    @staticmethod
    def second_click_swallowed():
        """The client turns a second click within its double-click time into
        a double-click and never reports it to script click handlers, so a
        double-click arrived as one click (and needed a third). Clear the
        client's last-click time after each of our clicks so the next click
        is reported normally. Returns True if the second click already came
        and went (swallowed) before this click was handled."""
        Client.find()
        if Client.mouse is None:
            return False
        get, put = Client.mouse
        try:
            last = int(get())
            put(Client.NO_CLICK_TIME)
            return last in (0, 0xFFFFFFFF)
        except Exception:
            return False

    @staticmethod
    def typing():
        """True while keys go into a text field (chat line, any text box):
        hotkeys must not act then. See Typing."""
        return bool(safe(Typing.now, False))

    @staticmethod
    def key_held(which):
        if not Client.looked:
            Client.find()
        fn = Client.keys.get(which)
        if fn is None:
            return None
        try:
            return bool(fn())
        except Exception:
            return False

    # ---------- the client thread ----------
    #  Every script call that returns a value (create a control, read a label,
    #  ask about a spell) is handed to the client thread and WAITS for its next
    #  update pass: one round trip each. Inside a function that already runs on
    #  the client thread those calls run in place, so a window of hundreds of
    #  controls is built in one hop. These helpers make that hop.
    MTQ = None                # ClassicUO.Game.Managers.MainThreadQueue
    mtq_looked = False
    main_call = None          # the way to call it that this IronPython build accepts

    @staticmethod
    def _find_mtq():
        if Client.mtq_looked:
            return Client.MTQ
        Client.mtq_looked = True
        try:
            import clr
            clr.AddReference(API.GetType().Assembly)
            from ClassicUO.Game.Managers import MainThreadQueue
            Client.MTQ = MainThreadQueue
        except Exception:
            Client.MTQ = None
        return Client.MTQ

    @staticmethod
    def on_client_thread():
        """True when this code already runs on the client's thread (asked of
        the client every time: other threads may call this too)."""
        MTQ = Client.MTQ if Client.mtq_looked else Client._find_mtq()
        if MTQ is None:
            return False
        try:
            return bool(MTQ.IsMainThread)
        except Exception:
            return False

    @staticmethod
    def _pick_main_call():
        """The way into the client thread this build accepts, tried once. The
        generic method and the delegate type are bound here, once, instead of
        on every hop."""
        from System import Func
        MTQ = Client.MTQ
        F = Func[object]

        def generic_of():
            inv = MTQ.InvokeOnMainThread[object]

            def generic(run):
                inv(F(run))
            return generic

        def inferred_of():
            def inferred(run):
                MTQ.InvokeOnMainThread(F(run))
            return inferred

        def with_event_of():
            from System import Action
            from System.Threading import ManualResetEventSlim

            def with_event(run):
                done = ManualResetEventSlim(False)

                def wrapped():
                    try:
                        run()
                    finally:
                        done.Set()
                MTQ.EnqueueAction(Action(wrapped))
                if not done.Wait(5000):          # a stalled client thread is not "ok"
                    raise _HopTimeout("the client thread didn't answer in 5 s")
            return with_event

        for make in (generic_of, inferred_of, with_event_of):
            probe = {}

            def run_probe():
                probe["ok"] = True
            try:
                candidate = make()
                candidate(run_probe)
            except Exception:
                continue
            if probe.get("ok"):
                return candidate
        return None

    @staticmethod
    def on_main(fn):
        """fn() on the client thread; its result, or None when that can't be
        done or fn raised (the reason is left in Client.error)."""
        how, v = Client.on_main_ex(fn)
        return v if how == "ok" else None

    @staticmethod
    def on_main_ex(fn):
        """("ok", result) when fn ran on the client thread; ("err", message)
        when it ran there and raised; ("no", None) when the hop can't be made."""
        Client.exc = None
        if (Client.MTQ if Client.mtq_looked else Client._find_mtq()) is None:
            return "no", None
        if Client.on_client_thread():
            try:
                return "ok", fn()
            except Exception as ex:
                Client.error = str(getattr(ex, "InnerException", None) or ex)
                Client.exc = ex
                return "err", Client.error
        call = Client.main_call
        if call is None:
            call = Client.main_call = Client._pick_main_call()
            if call is None:
                Client.error = "can't run on the client thread"
                return "no", None
        hop = _Hop(fn)
        try:
            call(hop.run)
        except _HopTimeout as ex:            # queued but not run yet: never run it here as well
            Client.error = str(ex)
            return "err", Client.error
        except Exception as ex:
            Client.error = str(ex)
            return "no", None
        if hop.e is not None:
            Client.error, Client.exc = hop.e, hop.x
            return "err", hop.e
        return "ok", hop.v

    error = ""
    exc = None                # the last exception raised inside on_main_ex


class _HopTimeout(Exception):
    """The client thread took a queued hop but hadn't run it within the wait."""
    pass


class _Hop(object):
    """One call carried to the client thread (Client.on_main_ex): fn, and what
    came back. One small object per hop instead of a closure and a dict."""
    __slots__ = ("fn", "v", "e", "x")

    def __init__(self, fn):
        self.fn, self.v, self.e, self.x = fn, None, None, None

    def run(self):
        try:
            self.v = self.fn()
        except Exception as ex:
            self.e = str(getattr(ex, "InnerException", None) or ex)
            self.x = ex
        except:
            self.e = "unknown error"


# =============================================================================
#  Typing - is a key the player presses text for a field, not a hotkey?
#  The client itself runs its macros only while keyboard focus rests on the
#  chat line and the chat line isn't open for typing. Virtue Assistant's
#  hotkeys follow the same rule, for every field anywhere on screen: the chat
#  line once it's open (Enter), any text box of any window (Virtue Assistant's
#  own settings fields, client search and rename boxes, Legion's editor and
#  other Myra windows), and anything already typed on the chat line. Read
#  live from the client's UIManager by reflection, so it is current at the
#  moment of the key press. Every module asks Client.typing() (or
#  HOST.typing()) before acting on a key.
# =============================================================================
class Typing(object):
    looked = False
    uim = None                # ClassicUO.Game.Managers.UIManager (static)
    prof = None               # ClassicUO.Configuration.ProfileManager (static)
    _members = {}             # (Type, member, static) -> (PropertyInfo / FieldInfo, is a
    #                           property) or None; keyed by the Type itself, so a lookup is
    #                           one dict hit (no FullName read and string per call)
    _flags = None             # BindingFlags for (instance, static) members, made once
    error = ""
    _req = None               # System.Object.ReferenceEquals, bound once (2.6.82)
    _prof_t = None            # the profile object's Type, read once (2.6.82)
    _chat_t = None            # the system chat control's Type, read once (2.6.82)
    _now_pid = -1             # (2.6.82) the pass whose answer _now_val is (client hop only)
    _now_val = False

    @staticmethod
    def _find():
        if Typing.looked:
            return
        Typing.looked = True
        Typing.uim = Client._type("ClassicUO.Game.Managers.UIManager")
        Typing.prof = Client._type("ClassicUO.Configuration.ProfileManager")
        if Typing.uim is None:
            Typing.error = "can't find the client's UIManager"

    @staticmethod
    def _lookup(t, name, static):
        """The member `name` of type t (most derived first), or None."""
        if Typing._flags is None:
            from System.Reflection import BindingFlags
            base = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly
            Typing._flags = (base | BindingFlags.Instance, base | BindingFlags.Static)
        flags = Typing._flags[1 if static else 0]
        m, prop, tt = None, False, t
        while tt is not None and m is None:   # most derived first: no ambiguity
            try:
                m = tt.GetProperty(name, flags)
            except Exception:
                m = None
            if m is not None:
                prop = True
            else:
                m = tt.GetField(name, flags)
            tt = tt.BaseType
        if m is None and not static:          # an interface property (IGui)
            for it in t.GetInterfaces():
                m = it.GetProperty(name)
                if m is not None:
                    prop = True
                    break
        return (m, prop) if m is not None else None

    @staticmethod
    def _get(obj, name, t=None, default=None):
        """A property or field of a .NET object (obj None = static on t)."""
        try:
            static = obj is None
            if t is None:
                t = obj.GetType()
            ck = (t, name, static)
            m = Typing._members.get(ck, False)
            if m is False:
                m = Typing._members[ck] = Typing._lookup(t, name, static)
            if m is None:
                return default
            if m[1]:
                return m[0].GetValue(obj, None)
            return m[0].GetValue(obj)
        except Exception:
            return default

    @staticmethod
    def _same(a, b):
        if a is None or b is None:
            return False
        try:
            req = Typing._req
            if req is None:
                import System
                req = Typing._req = System.Object.ReferenceEquals
            return bool(req(a, b))
        except Exception:
            return a is b

    @staticmethod
    def _ptype(cur):
        """The client profile's Type (the same class all session), read once."""
        t = Typing._prof_t
        if t is None:
            try:
                t = Typing._prof_t = cur.GetType()
            except Exception:
                t = None
        return t

    @staticmethod
    def now():
        """True while a key would go into a text field (see the class note).
        (2.6.82) Inside the client hop the answer is kept for the pass (nothing
        moves during it); a hotkey (script thread) always reads it fresh."""
        try:
            h = HOST
            pid = h.pass_id if h.in_hop else None
        except Exception:
            pid = None
        if pid is not None and Typing._now_pid == pid:
            return Typing._now_val
        v = Typing._now()
        if pid is not None:
            Typing._now_pid = pid
            Typing._now_val = v
        return v

    @staticmethod
    def _now():
        Typing._find()
        uim = Typing.uim
        if uim is None:
            return False
        focus = Typing._get(None, "KeyboardFocusControl", uim)
        chat = Typing._get(None, "SystemChat", uim)
        chat_tb = None
        if chat is not None:
            ct = Typing._chat_t
            if ct is None:
                try:
                    ct = Typing._chat_t = chat.GetType()
                except Exception:
                    ct = None
            chat_tb = Typing._get(chat, "TextBoxControl", ct)
        if focus is not None and not Typing._same(focus, chat_tb):
            # focus on some other text field: typing, unless that field is
            # gone, hidden or read-only (then the client hands focus back)
            if not bool(Typing._get(focus, "IsDisposed", default=False)) \
                    and bool(Typing._get(focus, "IsVisible", default=True)) \
                    and bool(Typing._get(focus, "AcceptKeyboardInput", default=True)):
                return True
        if chat is None:
            return False
        after_enter = True
        if Typing.prof is not None:
            cur = Typing._get(None, "CurrentProfile", Typing.prof)
            if cur is not None:
                v = Typing._get(cur, "ActivateChatAfterEnter", Typing._ptype(cur))
                after_enter = True if v is None else bool(v)
        if after_enter and bool(Typing._get(chat, "IsActive", Typing._chat_t, default=False)):
            return True                       # the chat line is open (Enter)
        text = Typing._get(chat_tb, "Text") if chat_tb is not None else None
        return text is not None and len(str(text)) > 0   # something typed on the chat line

    @staticmethod
    def release():
        """Hand keyboard focus back to the chat line, the way a click on the
        game world does (so hotkeys work again). Runs on the client thread."""
        Typing._now_pid = -1      # (2.6.83) the pass's kept answer is no longer true
        def run():
            Typing._find()
            uim = Typing.uim
            if uim is None:
                return
            try:
                from System.Reflection import BindingFlags
                m = uim.GetMethod("RestoreSystemChatFocus",
                                  BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic)
                if m is not None:
                    m.Invoke(None, None)
                    return
            except Exception:
                pass
            chat = Typing._get(None, "SystemChat", uim)
            tb = Typing._get(chat, "TextBoxControl") if chat is not None else None
            if tb is not None:
                safe(lambda: tb.SetKeyboardFocus())
        if Client.on_client_thread():
            safe(run)
        else:
            Client.on_main(run)


# =============================================================================
#  Follow - Alt+click auto-follow, the same in every module
#  Any health bar, frame or row for another mobile, and any button that acts
#  on one, can be Alt+clicked to auto-follow that mobile with TazUO's own
#  auto-follow; Alt+click the same one again to stop. Every module uses this
#  one helper, so they all agree on who you are following.
#
#    In the click handler (read Alt AT the click, the key may be up by the
#    next tick), only queue it:
#        if Follow.alt_held(): queue(("follow", serial)); return
#    and in tick():
#        Follow.toggle(serial, TITLE)
#
#  Follow.current() is the serial being followed (None if not), read from the
#  client itself, so it is right even after the client stopped following
#  (you walked away, the mobile left view) or you Alt+clicked a mobile in the
#  game world.
# =============================================================================
class Follow(object):
    serial = None             # who we last asked the client to follow
    readers = None            # ways to read the Alt key, best first
    ALT_NAMES = ("ALT", "LALT", "RALT", "LEFTALT", "RIGHTALT", "MENU", "LMENU", "RMENU")
    SDL_ALT = 0x0300          # SDL KMOD_ALT

    @staticmethod
    def _find():
        if Follow.readers is not None:
            return
        r = []
        try:
            import clr
            for asm in ("ClassicUO", "ClassicUO.Client", "TazUO", "FNA", "SDL2-CS", "SDL3-CS"):
                safe(lambda: clr.AddReference(asm))
        except Exception:
            pass
        Client.find()                          # the client's own Keyboard.Alt, by reflection
        if "alt" in Client.keys:
            r.append(lambda: Client.key_held("alt"))
        try:
            from ClassicUO.Input import Keyboard
            bool(Keyboard.Alt)
            r.append(lambda: bool(Keyboard.Alt))
        except Exception:
            pass
        for modname in ("SDL2", "SDL3"):
            try:
                sdl = __import__(modname).SDL
                int(sdl.SDL_GetModState())
                r.append(lambda sdl=sdl: (int(sdl.SDL_GetModState()) & Follow.SDL_ALT) != 0)
            except Exception:
                pass
        Follow.readers = r

    @staticmethod
    def alt_held():
        """True while Alt is down. Safe to call inside a click handler."""
        Follow._find()
        for fn in Follow.readers:
            if safe(fn, False):
                return True
        if Follow.readers:
            # a reader exists and says Alt is up: believe it. The IsKeyPressed
            # loop below is for builds with no reader at all (each call is a
            # frame-wait, inside a click handler)
            return False
        for k in Follow.ALT_NAMES:
            if safe(lambda: API.IsKeyPressed(k), False):
                return True
        return False

    _pid = -1                 # (2.6.82) the pass whose answer _val is (client hop only)
    _val = None

    @staticmethod
    def current():
        """Serial the client is auto-following now, or None. (2.6.82) Kept for
        the rest of the pass inside the client hop; start / stop drop it."""
        try:
            h = HOST
            pid = h.pass_id if h.in_hop else None
        except Exception:
            pid = None
        if pid is not None and Follow._pid == pid:
            return Follow._val
        v = Follow._current()
        if pid is not None:
            Follow._pid = pid
            Follow._val = v
        return v

    @staticmethod
    def _current():
        Typing._find()
        cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
        if cur is not None:
            pt = Typing._ptype(cur)
            mode = Typing._get(cur, "FollowingMode", pt)
            if mode is not None:
                if not bool(mode):
                    Follow.serial = None
                    return None
                t = Typing._get(cur, "FollowingTarget", pt)
                if t is not None:
                    try:
                        Follow.serial = int(t) or None
                    except Exception:
                        pass
                return Follow.serial
        if Follow.serial is not None and safe(lambda: API.FindMobile(Follow.serial)) is None:
            Follow.serial = None               # gone from view; the client stops too
        return Follow.serial

    @staticmethod
    def start(serial, who=APP_NAME):
        serial = int(serial or 0)
        if not serial:
            return False
        Follow._pid = -1                       # (2.6.82) the client's answer changes now
        me = int(safe(lambda: API.Player.Serial, 0) or 0)
        if serial == me:
            API.SysMsg("%s: you can't follow yourself." % who, Kit.HUE_INFO)
            return False
        if safe(lambda: API.FindMobile(serial)) is None:
            API.SysMsg("%s: can't follow them, they are out of sight." % who, Kit.HUE_BAD)
            return False
        try:
            API.AutoFollow(serial)
        except Exception as ex:
            API.SysMsg("%s: couldn't auto-follow (%s)." % (who, ex), Kit.HUE_BAD)
            return False
        Follow.serial = serial
        Follow._pid = -1
        safe(lambda: API.HeadMsg("* following *", serial, 0x44))
        return True

    @staticmethod
    def stop(who=APP_NAME):
        s = Follow.serial
        Follow._pid = -1                       # (2.6.82) the client's answer changes now
        safe(lambda: API.CancelAutoFollow())
        Follow.serial = None
        if s:
            safe(lambda: API.HeadMsg("* stopped following *", s, 0x35))

    @staticmethod
    def toggle(serial, who=APP_NAME):
        """Alt+click: follow this mobile, or stop if we already follow it.
        Call from tick(), not from inside the click handler."""
        serial = int(serial or 0)
        if serial and Follow.current() == serial:
            Follow.stop(who)
            return False
        return Follow.start(serial, who)


# =============================================================================
#  Kit - the shared native look
#  Stone frame of the crafting gump, translucent black sections,
#  the UO font in client hues, client checkboxes and gump-art buttons.
# =============================================================================
class Kit(object):
    WINDOW_BG     = 5054    # stone frame used by the crafting gump
    STONE_TILE    = 5058    # centre piece of that frame (plain stone)
    SECTION_TILE  = 2624    # black tile the crafting gump fills its sections with
    SECTION_ALPHA = 0.8     # how see-through the black sections are
    FIELD_TILE    = 2624    # drawn solid behind text boxes
    CORNER_ART    = 10460   # knot ornament on the frame's corners (0 = off)

    # Gump-art buttons: (normal, pressed, hover)
    ART_PLAY    = (4005, 4007, 4006)   # right arrow
    ART_CLOSE   = (4017, 4019, 4018)   # X / cancel
    ART_OK      = (4023, 4025, 4024)   # check mark
    ART_PAGE    = (4011, 4013, 4012)   # page / scroll
    ART_MIN     = (253, 252, 253)      # small down arrow: Minimize (own minimized form)
    ART_RESTORE = (251, 250, 251)      # small up arrow
    ART_DOCK    = (5602, 5606, 5602)   # gold down triangle (16x16): Fold into the Action Bar
    ART_CIRCLE  = (2117, 2118, 2118)   # small round gem button (15x15): a window's simple buttons (2.6.51)
    #  The fold button sits DOCK_DX px left of the Minimize arrow, DOCK_DY px
    #  lower (the triangle is 16 px tall, the arrow 21). Its tooltip is DOCK_TIP.
    DOCK_DX, DOCK_DY = 20, 2
    DOCK_TIP = "Fold into the Action Bar (its tray button brings the window back)"
    MIN_TIP = "Minimize (double-click the title does too)"
    RESTORE_TIP = "Restore"
    SETTINGS_TIP = "Open the %s settings page"
    CLOSE_TIP = "Close %s (turns it off; the Modules tab turns it back on)"
    DOUBLE_TIP = "Double-click: minimize or restore"

    # Health bar line art (the client's own status bars)
    LINE_RED, LINE_BLUE, LINE_POISON = 0x0805, 0x0806, 0x0808

    HUE_TITLE = 53
    HUE_TEXT  = 1153
    HUE_GOOD  = 68
    HUE_BAD   = 33
    HUE_INFO  = 946

    MARGIN = 12            # stone frame visible around the sections
    GAP    = 8             # stone visible between sections (acts as the border)
    ZONE_INSET = 4         # (2.6.72) one frame on: a zoned window's panels this far in from
    #                        its zone's edge (seams between zones 2 x 4 = GAP)

    _sizes = {}

    # ---------- one hop to the client thread ----------
    @staticmethod
    def on_client(fn, fallback=True):
        """fn() in ONE hop on the client thread, where every script call runs
        in place (see Client): the way to build or redraw a whole window.
        Returns fn's result. When the hop can't be made, or fn fails there, fn
        runs here instead if `fallback` is set (else None comes back). fn must
        not wait (no HOST.idle / API.Pause): on the client thread a wait is a
        freeze, so HOST.idle returns at once there."""
        how, v = Client.on_main_ex(fn)
        if how == "ok":
            return v
        if how == "err":                     # fn ran there and failed: report, don't rerun
            raise Client.exc if isinstance(Client.exc, Exception) else Exception(Client.error)
        return fn() if fallback else None

    # ---------- the screen ----------
    _screen = {"wh": (0, 0), "at": 0.0}

    @staticmethod
    def screen():
        """(width, height) of the client window in the pixels gumps are placed
        in (its pixels over the UI scale, see render_scale; re-read every second)."""
        now = time.time()
        if now - Kit._screen["at"] >= 1.0 or Kit._screen["wh"] == (0, 0):
            Kit._screen["at"] = now
            wh = None
            try:
                b = API.GetClientBounds()
                wh = (int(b.Width), int(b.Height))
            except Exception:
                pass
            if not wh or wh[0] <= 0:
                try:
                    import clr
                    from ClassicUO import Client as CUO
                    cb = CUO.Game.Window.ClientBounds
                    wh = (int(cb.Width), int(cb.Height))
                except Exception:
                    wh = None
            if wh and wh[0] > 0 and wh[1] > 0:
                s = Kit.render_scale()           # gumps are placed in logical pixels
                if abs(s - 1.0) > 0.001:
                    wh = (int(round(wh[0] / s)), int(round(wh[1] / s)))
                Kit._screen["wh"] = wh
        return Kit._screen["wh"]

    _scale = {"fn": None, "looked": False}

    @staticmethod
    def render_scale():
        """The client's UI scale (1.0 when it has none or can't be read): a
        gump's X / Y and size are logical pixels, the client window's pixels
        divided by it, so screen() is given in the same pixels as the gumps."""
        st = Kit._scale
        if not st["looked"]:
            st["looked"] = True
            try:
                import clr
                from ClassicUO import Client as CUO
                float(CUO.Game.RenderScale)
                st["fn"] = lambda: float(CUO.Game.RenderScale)
            except Exception:
                st["fn"] = None
            if st["fn"] is None:
                # (2.6.70) ClassicUO.Client is internal to the client, so the import
                # above fails on TazUO and the scale was taken for 1.0: read it by
                # reflection (Client.Game.RenderScale)
                try:
                    from System.Reflection import BindingFlags
                    t = Client._type("ClassicUO.Client")
                    gp = t.GetProperty("Game", BindingFlags.Static | BindingFlags.Public
                                       | BindingFlags.NonPublic)
                    game = gp.GetValue(None, None)
                    rp = game.GetType().GetProperty("RenderScale", BindingFlags.Instance
                                                    | BindingFlags.Public | BindingFlags.NonPublic)
                    float(rp.GetValue(game, None))
                    st["fn"] = lambda: float(rp.GetValue(gp.GetValue(None, None), None))
                except Exception:
                    st["fn"] = None
        fn = st["fn"]
        if fn is None:
            return 1.0
        try:
            s = fn()
            return s if 0.25 <= s <= 4.0 else 1.0
        except Exception:
            return 1.0

    # ---------- THE WINDOW RULES (every window of every module and of this script) ----------
    #  1. A window is always wholly on screen. Place it with Kit.place(g, x, y,
    #     w, h) (never a bare g.SetRect for the window itself): the place is
    #     clamped to the screen before the window is shown. Whatever still ends
    #     up off screen later (a resize, a rebuild, a resolution change, a
    #     window dragged half off and let go) is moved back by the keeper
    #     (Snap.keep, every KEEP_EVERY seconds, and on the spot when the client
    #     window changes size): every window that went through G.AddGump takes
    #     part, nothing to register. A window that another window places by
    #     itself (a tray beside a bar, a grid under a title bar) is declared
    #     with Kit.attach(follower, leader): it never snaps on its own and the
    #     pair is kept on screen as one. Taller than the screen (2.6.53): it
    #     is never shown hanging off it; Kit.place cuts it to the screen's
    #     height and makes its body scroll, with a scrollbar down its right
    #     side and the title row staying put (Kit.scroll_fit, below). Wider
    #     than the screen: the left edge stays on. A window slotted in a zone
    #     of the layout (2.6.54, see Layout) is cut to its slot the same way
    #     (Kit.place max_h=) and scrolls; it is never shrunk or capped. It
    #     fills its zone (2.6.56): every window in a zone is made exactly the
    #     size of its slot (its module lays it out for it when its hooks say
    #     "fit" and "exact"; else Fill stretches its frame and sections and
    #     anchors the rest), so it never leaves the zone; a module moves its
    #     own controls after drawing through Kit.ui_pos / ui_rect / ui_w.
    #  2. Every window remembers its place and its state, per character.
    #     Position: Kit.load_pos(key, default, size) when it is built and
    #     Kit.save_pos(key, g) the moment it is let go (Kit.on_moved) and in
    #     stop(); minimized: Kit.load_min(key) / Kit.save_min(key, flag) (or the
    #     module's own settings); folded into the Action Bar: the host's dock
    #     wish (HOST.dock_wanted). A place saved on another screen size is
    #     adapted to the screen of today (Kit.adapt): the window keeps its
    #     distance from the screen edge or centre it was nearest, exactly on
    #     the anchor when it sat on one.
    #  3. One anchor convention. The nine screen anchors (Kit.ANCHORS: corners,
    #     edge midpoints, centre) are placed by Kit.anchor_pos and recognised
    #     by Kit.anchor_at, with the same arithmetic for every window (a window
    #     let go near one goes exactly on to it: Snap.snap_screen). Windows snap
    #     to one another flush, edge to edge, within SNAP_DIST, whatever module
    #     drew them; a window's rect (its SetRect) is exactly its drawn frame,
    #     so "flush" is flush on screen too. A module's own grouping (Ultima
    #     Tracker's anchored groups) uses the same distance.
    ANCHORS = ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR")
    SCREEN_KEY = "VirtueAssistant_screen"   # per character: the screen the saved places are for
    _pos_screen = None                      # (W, H) read from it at start (see adapt)

    @staticmethod
    def clamp(x, y, w, h):
        """(x, y) moved the least so a w x h window is wholly on screen. A
        window bigger than the screen keeps whichever edge the place asked for
        shows: its left (top) edge when x (y) is at or past 0, else its right
        (bottom) edge, so a very wide bar can be dragged to reach either end
        and never ends up with both ends off the screen."""
        W, H = Kit.screen()
        x, y, w, h = int(x or 0), int(y or 0), int(w or 0), int(h or 0)
        if W > 0:
            x = max(0, min(x, W - w)) if w <= W else max(W - w, min(x, 0))
        if H > 0:
            y = max(0, min(y, H - h)) if h <= H else max(H - h, min(y, 0))
        return x, y

    # ---------- (2.6.70) a window's place before the client applies it ----------
    #  SetRect / SetPos are queued by the client and land on a later frame, while
    #  GetX / GetWidth answer at once: a window just made reads 0, 0, 0 x 0 and a
    #  window just moved reads its old place. Everything that placed a piece
    #  beside a window just rebuilt (the frames' bandage and swing pieces) put it
    #  at the screen's top-left corner for a frame, then back, over and over (the
    #  flicker). Kit.place and Snap.move note what they asked for here, and
    #  Kit.rect (the snapping, the keeper, the layout and the modules read
    #  through it) answers with that until the client has applied it.
    _frame_parts = {}                       # (2.6.70) window -> its stone frame's controls
    _back_parts = {}                        # (2.6.78) window -> its 9-piece backgrounds' pieces
    _pend = {}                              # window -> (x, y, w or None, h or None, time asked,
    #                                         the client's rect when asked)
    PEND_FOR = 1.0                          # seconds a request is believed before the client

    @staticmethod
    def note_rect(g, x, y, w=None, h=None):
        """Window g was asked to be at (x, y) (and w x h): Kit.rect answers that
        until the client has applied it."""
        if g is None:
            return
        try:
            r = None
            if Kit._pend:
                r = Kit.rect(g)                  # 2.6.81: drop a request that landed or expired
            old = Kit._pend.get(g)
            if w is None and old is not None:
                w, h = old[2], old[3]            # a move after a resize not yet landed
            if old is not None:
                was = old[5]                     # the client's own word from before both
            elif r is not None:
                was = r                          # (2.6.82) the client's word, just read above
            else:
                was = (int(g.GetX()), int(g.GetY()), int(g.GetWidth() or 0),
                       int(g.GetHeight() or 0))
            Kit._pend[g] = (int(x), int(y), None if w is None else int(w),
                            None if h is None else int(h), time.time(), was)
        except Exception:                        # not a window it can keep track of
            pass

    @staticmethod
    def rect(g):
        """(x, y, w, h) of window g: what it was last asked to be while the
        client hasn't applied it yet, else what the client says. None when it
        can't be read."""
        try:
            x, y = int(g.GetX()), int(g.GetY())
            w, h = int(g.GetWidth() or 0), int(g.GetHeight() or 0)
        except Exception:
            return None
        pend = Kit._pend
        if pend:
            p = pend.get(g)
            if p is not None:
                pw = w if p[2] is None else p[2]
                ph = h if p[3] is None else p[3]
                # landed, or the client moved it since (a drag, a fit of its own), or
                # it never will: the client's word from now on
                if (x, y, w, h) == (p[0], p[1], pw, ph) or (x, y, w, h) != p[5] \
                        or time.time() - p[4] > Kit.PEND_FOR:
                    del pend[g]
                else:
                    return p[0], p[1], pw, ph
        return x, y, w, h

    @staticmethod
    def pos(g):
        """(2.6.82) (x, y) of window g as Kit.rect has it, with two client reads
        instead of four when no request for it is waiting to land. None when
        it can't be read."""
        if Kit._pend and g in Kit._pend:
            r = Kit.rect(g)
            return None if r is None else (r[0], r[1])
        try:
            return int(g.GetX()), int(g.GetY())
        except Exception:
            return None

    @staticmethod
    def prune_pending():
        """Drop requests that landed long ago or whose window closed (the keeper)."""
        if len(Kit._pinned) > 400:               # (2.6.74) windows never seen by the snapping
            Kit._pinned = set(g for g in Kit._pinned if Kit.is_open(g))
        if not Kit._pend:
            return
        now = time.time()
        for g in [g for g, p in Kit._pend.items() if now - p[4] > Kit.PEND_FOR]:
            Kit._pend.pop(g, None)

    @staticmethod
    def place(g, x, y, w, h, head=None, max_h=None):
        """SetRect for a window: on screen, always. Returns the (x, y) used.
        A window the layout has fitted to its slot in a zone (2.6.56, Fill)
        stays the slot's size wherever and however big its module places it:
        (w, h) is noted as the window's own size and the slot is kept."""
        rec = Fill.recs.get(g) if Fill.recs else None
        if rec is not None and rec["slot"] is not None:
            rec["nat"], rec["size"] = (int(w or 0), int(h or 0)), None
            sx, sy, sw, sh = rec["slot"]
            if Kit.on_client(lambda: Fill.fit(g, sx, sy, sw, sh, rec["mode"]),
                             fallback=False) is not None:
                return sx, sy
            Fill.recs.pop(g, None)               # couldn't be fitted: placed as it comes
        return Kit._place_raw(g, x, y, w, h, head, max_h)

    @staticmethod
    def _place_raw(g, x, y, w, h, head=None, max_h=None):
        """Kit.place without the zone fit (Fill places with this).
        A window taller than the screen (2.6.53) is not shown half off it:
        it is cut to the screen's height and its body scrolls, with a
        scrollbar down its right side (Kit.scroll_fit; the title row stays
        put). `head`: the height of that fixed top part, in the window's
        pixels (default: the standard title section, MARGIN + 30 + GAP).
        `max_h` (2.6.54): a lower limit than the screen's height, the slot
        of the layout the window sits in; taller than that it scrolls too."""
        w, h = int(w or 0), int(h or 0)
        H = Kit.screen()[1]
        limit = H if not max_h else min(H, int(max_h))
        if limit > 0 and (h > limit or g in Kit._scrolled):
            # 2.6.81: the slot (or None), not the screen height, is what scroll_fit
            # keeps as its cap, so a taller client window lets it grow back
            fit = Kit.scroll_fit(g, w, h, head, int(max_h) if max_h else None)
            if fit is not None:
                w, h = fit
        x, y = Kit.clamp(x, y, w, h)
        g.SetRect(x, y, w, h)
        Kit.note_rect(g, x, y, w, h)             # (2.6.70) read back as asked until it lands
        if g not in Kit._pinned:
            Kit.pin_size(g)                      # (2.6.74) the size set here stays its size
        return x, y

    # (2.6.74) TazUO makes a script window with WantUpdateSize on: on the window's
    # first Update the client sets its Width / Height to the far edge of its VISIBLE
    # children (Control.Update) and turns the flag off. A zoned window whose stone
    # frame the one frame hid before that Update (Surround.early) came out
    # Kit.MARGIN short on the right and bottom, smaller than its slot: every "panels
    # aren't 4 px in" line of 2.6.73's Check look. A window given a size by
    # Kit.place keeps that size now; a window made without a size keeps the
    # client's auto size.
    _pinned = set()                         # windows whose auto size is off (Snap._forget drops them)

    @staticmethod
    def pin_size(g, raw=None):
        """(2.6.74) Turn the client's auto size off for window g (WantUpdateSize
        False on its client gump), so the size this script gives it stays. True
        when it is off now. A plain property set: safe on any thread."""
        try:
            raw = raw if raw is not None else Kit._raw_gump(g)
            if raw is None:
                return False
            if raw.WantUpdateSize:
                raw.WantUpdateSize = False
            Kit._pinned.add(g)
            return True
        except Exception:
            return False

    # ---------- a window taller than the screen scrolls (2.6.53) ----------
    #  Every window placed with Kit.place that is taller than the screen is
    #  turned into a scrolling one, here, with no help from its module: the
    #  window is cut to the screen's height, everything under the title row
    #  is moved into a client scroll area that covers the body, and the
    #  client's own scrollbar (the arrows and rail of its skills window) runs
    #  down the right side, in a band SCROLL_BAND px wide added to the
    #  window. The controls keep their coordinates (the area sits at 0, 0),
    #  so a module that moves or reads its controls later sees no change;
    #  controls it adds later are swept into the area by the keeper
    #  (scroll_sweep, every KEEP_EVERY s). The frame is drawn again for the
    #  new size (add_window_frame notes its pieces for that), a band of
    #  stone that takes the mouse sits behind the title row so scrolled
    #  content never shows or clicks through there, and the title row is
    #  drawn last, on top. A window that can't be converted (no client
    #  access, a control that can't be read) is left as before: clamped,
    #  its top-left corner on screen.
    SCROLL_W = 15                           # the client's scrollbar (gump 256) is 15 px wide
    SCROLL_GAP = 0                          # stone between the sections and the scrollbar
    SCROLL_BAND = SCROLL_GAP + SCROLL_W     # the window grows this much to the right: the
    #                                         bar sits where the right border was, the
    #                                         border moves out past it
    _frames = {}                            # window -> the frame pieces add_window_frame drew
    _scrolled = {}                          # window -> how it was converted (see scroll_fit)
    _rawmode = {}                           # how a raw control's rect is read on this build

    @staticmethod
    def scroll_fit(g, w, h, head=None, limit=None):
        """Make window g (w x h, taller than the screen) a scrolling window
        of the screen's height, or bring one already converted up to date
        with a new size. (width, height) of the window now, or None when it
        couldn't be done (the caller places the window as it is). `limit`
        (2.6.54): the height to cut to instead of the screen's (a slot)."""
        try:
            H = Kit.screen()[1]
            if limit:
                H = min(H, int(limit))
            info = Kit._scrolled.get(g)
            if info is not None and info["w"] == w and info["h"] == h and info["H"] == H:
                return info["w2"], info["hv"]
            if head is None:
                head = info["head"] if info is not None else Kit.MARGIN + 30 + Kit.GAP
            out = Kit.on_client(lambda: Kit._scroll_build(g, w, h, int(head), H),
                                fallback=False)
            if out is not None:
                Kit._scrolled[g]["lim"] = int(limit) if limit else None
            return out
        except Exception:
            return None

    @staticmethod
    def scroll_info(g):
        """How window g was converted ({"w2", "hv", ...}) or None."""
        return Kit._scrolled.get(g)

    @staticmethod
    def _raw_rect(c):
        """(x, y, w, h) of a client control, or None. The client's X / Y /
        Width / Height are ref properties, which not every IronPython reads
        the same way, so the way that works here is found once and kept."""
        mode = Kit._rawmode
        try:
            loc = c.Location
            x, y = int(loc.X), int(loc.Y)
        except Exception:
            return None
        how = mode.get("how")
        if how != "reflect":
            try:
                w, h = int(c.Width), int(c.Height)
                mode["how"] = "direct"
                return x, y, w, h
            except Exception:
                mode["how"] = "reflect"
        try:
            t = c.GetType()
            pw = t.GetProperty("Width")
            ph = t.GetProperty("Height")
            return x, y, int(pw.GetValue(c, None)), int(ph.GetValue(c, None))
        except Exception:
            return None

    @staticmethod
    def _raw_gump(g):
        """The client's own Gump behind a script window (or None)."""
        try:
            raw = g.Gump
            if raw is not None:
                return raw
        except Exception:
            pass
        return Kit.client_control(g)

    @staticmethod
    def _children(raw):
        """The client control's children now, in draw order (a list copy)."""
        kids = raw.Children
        return [kids[i] for i in range(int(kids.Count))]

    @staticmethod
    def _scroll_build(g, w, h, head, H):
        """On the client thread: convert window g, or re-fit a converted one.
        Returns (w2, hv) or None (the window is then as it was)."""
        M = Kit.MARGIN
        if not Kit.flush():                  # every queued Add / SetRect in place first
            return None
        raw = Kit._raw_gump(g)
        if raw is None:
            return None
        hv = min(h, H)
        head = max(0, min(head, hv - M - 40))
        w2 = w + Kit.SCROLL_BAND
        area_w = w - M + Kit.SCROLL_GAP + 14  # the client puts its scrollbar 14 px from the right
        area_h = hv - M
        info = Kit._scrolled.get(g)
        if info is not None:
            return Kit._scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head)
        # a first conversion. Nothing is changed until every control's place has
        # been read; after that a failure puts the frame back (_scroll_undo).
        fr = Kit._frames.get(g)
        corners = fr["corners"] if fr else True
        mouse = fr["mouse"] if fr else True
        old_frame = list(fr["pieces"]) if fr else []
        kids, content, header, fixed = [], [], [], []
        skip = []
        for p in old_frame:
            pr = Kit.client_control(p)
            if pr is not None:
                skip.append(pr)
        same = Kit._same()
        for c in Kit._children(raw):
            try:
                if c.IsDisposed:
                    continue
            except Exception:
                continue
            if any(same(c, s) for s in skip):
                continue
            r = Kit._raw_rect(c)
            if r is None:                    # a control that can't be read: give up
                return None
            kids.append(c)
            cy, ch = r[1], r[3]
            if cy <= 0 and ch >= h - 2:      # a full-height background of the module's own
                fixed.append(c)
            elif cy < head:                  # the title row (and anything across its edge)
                header.append(c)
            else:
                content.append(c)
        Kit._frames.pop(g, None)
        for p in old_frame:
            Kit.dispose(p)
        frame = area = band = None
        try:
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h)
            frame = Kit._scroll_frame(g, w2, hv, corners, mouse)   # under everything
            if not Kit.flush():
                raise Exception("queue")
            for c in fixed:
                c.Parent = raw               # to the end: right after the frame
            g.Add(area)
            if not Kit.flush():
                raise Exception("queue")
            area_raw = Kit.client_control(area)
            if area_raw is None:
                raise Exception("no area")
            for c in content:
                c.Parent = area_raw          # into the scroll area, same coordinates
            band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush():
                raise Exception("queue")
            for c in header:
                c.Parent = raw               # last of all: drawn over the band
        except Exception:
            Kit._scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band)
            return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band,
                         header, fixed, corners, mouse)
        return w2, hv

    @staticmethod
    def _scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head):
        """A converted window placed at another size: the frame and band are
        drawn again for it and the content moves into a scroll area of the
        new size (the client's scrollbar keeps the hit boxes it was made
        with, so it is made anew rather than resized). Returns (w2, hv) or
        None."""
        try:
            for p in info["frame"] + info["band"]:
                Kit.dispose(p)
            old_area, old_raw = info["area"], info["area_raw"]
            header = [c for c in info["header"] if not c.IsDisposed]
            fixed = [c for c in info["fixed"] if not c.IsDisposed]
            corners, mouse = info["corners"], info["mouse"]
            frame = Kit._scroll_frame(g, w2, hv, corners, mouse)
            if not Kit.flush():
                return None
            for c in fixed:
                c.Parent = raw
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h)
            g.Add(area)
            if not Kit.flush():
                return None
            area_raw = Kit.client_control(area)
            if area_raw is None:
                Kit.dispose(area)
                return None
            kids = Kit._children(old_raw)
            for c in kids[1:]:               # [0] is the old scrollbar
                try:
                    if not c.IsDisposed:
                        c.Parent = area_raw
                except Exception:
                    pass
            Kit.dispose(old_area)
            band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush():
                return None
            for c in header:
                c.Parent = raw
        except Exception:
            return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band,
                         header, fixed, corners, mouse)
        return w2, hv

    @staticmethod
    def _scroll_frame(g, w2, hv, corners, mouse):
        """The frame of a scrolling window: the 9-piece stone frame and the
        two knots on the right, which sit under the scrollbar (it covers
        their middle, as the sections cover the left knots' middle, so a
        strip of each shows on the border). Returns the controls drawn."""
        frame = Kit._frame_pieces(g, w2, hv, False, mouse)
        if corners and Kit.CORNER_ART:
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch:
                for cx, cy in ((w2 - cw, 0), (w2 - cw, hv - ch)):
                    p = Kit.add_pic(g, Kit.CORNER_ART, cx, cy, mouse=mouse)
                    if p is not None:
                        frame.append(p)
                        Kit._note_frame_part(g, p)   # (2.6.72) one frame hides it too
        return frame

    @staticmethod
    def _scroll_band(g, w, w2, hv, head, corners, mouse):
        """The band behind the title row of a scrolling window: opaque stone
        (the frame's own tile, from the same origin, so no seam) that takes
        the mouse, so nothing scrolled under the title can be seen or
        clicked; then the two knots on the left, over it as on any window.
        Returns the controls drawn."""
        M = Kit.MARGIN
        band = []
        bl = Kit.pic_size(Kit.WINDOW_BG + 3)[0] or M
        bt = Kit.pic_size(Kit.WINDOW_BG + 1)[1] or M
        t = Kit.add_tiled(g, Kit.STONE_TILE, bl, bt, w - M + Kit.SCROLL_GAP - bl, head - bt)
        if t is not None:
            try:
                t.SetAcceptMouseInput(True)
                t.CanMove = True
            except Exception:
                pass
            band.append(t)
        if corners and Kit.CORNER_ART:
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch:
                for cx, cy in ((0, 0), (0, hv - ch)):
                    p = Kit.add_pic(g, Kit.CORNER_ART, cx, cy, mouse=mouse)
                    if p is not None:
                        band.append(p)
                        Kit._note_frame_part(g, p)   # (2.6.72) one frame hides it too
        return band

    @staticmethod
    def hide_zone_frame(g):
        """(2.6.72) Window g's frame (as noted in Kit._frame_parts) hidden now, as
        the one frame hides it on its next pass: for a module that draws its own
        frame pieces while its window sits in a zone with one frame on."""
        parts = Kit._frame_parts.get(g) if Kit._frame_parts else None
        if not parts:
            return
        Kit.pin_size(g)                          # (2.6.74) hidden frame: the size stays
        for p in parts:
            try:
                p.IsVisible = False
            except Exception:
                pass
        LAYOUT.surround.bare[g] = parts

    @staticmethod
    def _note_frame_part(g, p):
        """(2.6.72) A control that is part of window g's stone frame, drawn after
        the frame itself (a scrolling window's knots): the one frame hides it
        with the rest, and hides it at once when the frame is hidden now."""
        try:
            parts = Kit._frame_parts.get(g)
        except TypeError:
            return
        if parts is None:
            return
        parts.append(p)
        if LAYOUT.surround.bare.get(g) is parts:
            safe(lambda: setattr(p, "IsVisible", False))

    @staticmethod
    def _scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band,
                     header, fixed, corners, mouse):
        Kit._scrolled[g] = {"w": w, "h": h, "H": H, "w2": w2, "hv": hv, "head": head,
                            "raw": raw, "area": area, "area_raw": area_raw, "frame": frame,
                            "band": band, "header": header, "fixed": fixed,
                            "n": Kit._live_count(raw), "corners": corners, "mouse": mouse}
        if len(Kit._scrolled) > 64:          # closed windows never placed again
            for k in [k for k in Kit._scrolled if not Kit.is_open(k)]:
                Kit._scrolled.pop(k, None)

    @staticmethod
    def _scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band):
        """A conversion that failed half way: the window as it was (its frame
        drawn again at its own size, under its controls in their old order)."""
        for p in (frame or []) + (band or []):
            Kit.dispose(p)
        Kit.dispose(area)
        try:
            pieces = Kit._frame_pieces(g, w, h, corners, mouse)
            # (2.6.71) noted again, as add_window_frame does: a later try knows its
            # frame (skipped, drawn again at the size it gets) and its corners / mouse
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}
            Kit.flush()
            for c in kids:
                c.Parent = raw               # after the frame again, in the same order
        except Exception:
            pass

    @staticmethod
    def _live_count(raw):
        """How many children a client control has that aren't disposed (a
        disposed one stays in the list until the control's next update)."""
        n = 0
        try:
            kids = raw.Children
            for i in range(int(kids.Count)):
                if not kids[i].IsDisposed:
                    n += 1
        except Exception:
            return -1
        return n

    _same_fn = None                      # (2.6.82) bound once

    @staticmethod
    def _same():
        """(a, b) -> are these the same client object."""
        fn = Kit._same_fn
        if fn is not None:
            return fn
        try:
            import System
            fn = System.Object.ReferenceEquals
        except Exception:
            fn = lambda a, b: a is b
        Kit._same_fn = fn
        return fn

    @staticmethod
    def scroll_sweep():
        """Every KEEP_EVERY s, on the client thread (Snap.keep): a control a
        module added to a scrolling window after it was converted goes into
        its scroll area too (under the title row it stays where it is)."""
        if not Kit._scrolled:
            return
        gone = []
        H = Kit.screen()[1]
        for g, info in list(Kit._scrolled.items()):
            if not Kit.is_open(g):
                gone.append(g)
                continue
            raw = info["raw"]
            lim = info.get("lim")
            want = min(H, lim) if lim else H
            if H > 0 and info["H"] != want:  # the client window changed height: fit again
                try:
                    fit = Kit._scroll_build(g, info["w"], info["h"], info["head"], want)
                    if fit is not None:
                        info = Kit._scrolled.get(g) or info
                        info["lim"] = lim
                        x, y = Kit.clamp(int(g.GetX()), int(g.GetY()), fit[0], fit[1])
                        g.SetRect(x, y, fit[0], fit[1])
                        Kit.moved_by_code(g)
                except Exception:
                    pass
                continue
            # (2.6.82) one Count read first: a control added or taken out changes
            # it; the child-by-child count runs only then (and every SWEEP_FULL s,
            # for a window that swapped as many controls as it disposed)
            try:
                cnt = int(raw.Children.Count)
            except Exception:
                cnt = -1
            now = time.time()
            if cnt >= 0 and cnt == info.get("cnt") and 0 <= info.get("full_at", 0.0) - now:
                continue
            info["cnt"] = cnt
            info["full_at"] = now + Kit.SWEEP_FULL
            n = Kit._live_count(raw)
            if n < 0 or n == info["n"]:
                continue
            if not Kit.flush():
                info["cnt"] = None                # (2.6.83) looked at again next sweep
                return
            try:
                kids = Kit._children(raw)
            except Exception:
                info["cnt"] = None
                continue
            known = info.get("known")
            if known is None:
                # (2.6.82) one set of the window's own pieces, kept: a set lookup per
                # child instead of a ReferenceEquals call against every piece
                known = set([info["area_raw"]] + info["header"] + info["fixed"])
                for k in info["frame"] + info["band"]:
                    kr = Kit.client_control(k)
                    if kr is not None:
                        known.add(kr)
                info["known"] = known
            for c in kids:
                try:
                    if c.IsDisposed or c in known:
                        continue
                except Exception:
                    continue
                r = Kit._raw_rect(c)
                if r is None:
                    continue
                if r[1] < info["head"]:
                    info["header"].append(c)
                    known.add(c)
                else:
                    try:
                        c.Parent = info["area_raw"]
                    except Exception:
                        pass
            info["n"] = Kit._live_count(raw)
            try:
                info["cnt"] = int(raw.Children.Count)
            except Exception:
                info["cnt"] = -1
        for g in gone:
            Kit._scrolled.pop(g, None)
            Kit._frames.pop(g, None)

    @staticmethod
    def on_screen(g):
        """Move window g (and the windows attached to it) back on screen now,
        if any of it is off. True if it moved."""
        try:
            return SNAP.keep_one(g)
        except Exception:
            return False

    @staticmethod
    def attach(follower, leader):
        """`follower` is placed beside `leader` by the module itself (a tray,
        a grid under a title bar): it never snaps on its own, and the keeper
        keeps the two on screen as one, moving both."""
        SNAP.attach(follower, leader)

    @staticmethod
    def detach(follower):
        """(2.6.57) `follower` no longer follows the window Kit.attach tied it
        to: a free window again, snapping as any other."""
        SNAP.detach(follower)

    @staticmethod
    def attached_to(follower):
        """(2.6.57) The window `follower` is attached to, or None."""
        try:
            return SNAP.attached.get(follower)
        except TypeError:
            return None

    @staticmethod
    def no_snap(g):
        """Window g takes no part in snapping (it stays exactly where it is
        dropped, follows nothing and nothing snaps on to it), but the keeper
        still keeps it on screen and on_moved still tells its module. Unit
        frames: they line up with one another by their own rule."""
        SNAP.exempt(g)

    @staticmethod
    def anchor_pos(name, w, h):
        """(x, y) of a w x h window on screen anchor `name` (one of ANCHORS),
        or (None, None) without a screen or a name. Wider / taller than the
        screen: the left / top edge stays on."""
        W, H = Kit.screen()
        if W <= 0 or H <= 0 or not name:
            return None, None
        col = "L" if "L" in name else "R" if "R" in name else "C"
        row = "T" if "T" in name else "B" if "B" in name else "C"
        x = 0 if col == "L" else max(0, W - w) if col == "R" else max(0, (W - w) // 2)
        y = 0 if row == "T" else max(0, H - h) if row == "B" else max(0, (H - h) // 2)
        return x, y

    @staticmethod
    def anchor_at(x, y, w, h, slack=2):
        """The screen anchor a w x h window at (x, y) sits on ("" = none):
        within `slack` pixels of it on both axes."""
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return ""
        col = "L" if abs(x) <= slack else "R" if abs(x + w - W) <= slack else \
            "C" if abs(x - (W - w) // 2) <= slack else None
        row = "T" if abs(y) <= slack else "B" if abs(y + h - H) <= slack else \
            "C" if abs(y - (H - h) // 2) <= slack else None
        if col is None or row is None:
            return ""
        return (row + col).replace("C", "") or "C"      # "TC" -> "T", "CC" -> "C"

    @staticmethod
    def anchor_targets(w, h):
        """[(x, y)] where a w x h window sits on each anchor, in ANCHORS order
        (top row first, left to right); [] without a screen."""
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return []
        return [Kit.anchor_pos(n, w, h) for n in Kit.ANCHORS]

    @staticmethod
    def remap_axis(p, s, S, S2):
        """Position p of a window s long on a screen S long, on one S2 long:
        it keeps its distance from the edge or the centre it is nearest (the
        third of the screen its middle is in), and sits exactly on the anchor
        when it was exactly on it."""
        p, s, S, S2 = int(p), int(s or 0), int(S), int(S2)
        if S <= 0 or S2 <= 0 or S == S2:
            return p
        if p == 0:
            return 0
        if p == S - s:
            return S2 - s
        if p == (S - s) // 2:
            return (S2 - s) // 2
        c = p + s / 2.0
        if c < S / 3.0:
            return p
        if c > 2 * S / 3.0:
            return S2 - (S - p)
        return p + (S2 - S) // 2

    @staticmethod
    def adapt(x, y, w=0, h=0):
        """A saved window place on the screen of today: moved with the anchor
        it was nearest on the screen it was saved on (the one noted last in
        SCREEN_KEY), then, with the size given, kept wholly on screen."""
        W, H = Kit.screen()
        old = Kit._pos_screen
        x, y = int(x), int(y)
        if old is not None and W > 0 and H > 0 and (W, H) != old:
            x = Kit.remap_axis(x, w, old[0], W)
            y = Kit.remap_axis(y, h, old[1], H)
        if w and h:
            x, y = Kit.clamp(x, y, w, h)
        return x, y

    @staticmethod
    def read_screen():
        """At start: the screen the saved places belong to."""
        try:
            w, h = Kit.get_var(Kit.SCREEN_KEY).split(",")
            Kit._pos_screen = (int(w), int(h))
        except Exception:
            Kit._pos_screen = None

    @staticmethod
    def note_screen(wh=None):
        """From now on the saved places belong to this screen (once the
        windows have been placed on it)."""
        wh = wh or Kit.screen()
        if wh and wh[0] > 0 and wh[1] > 0 and wh != Kit._pos_screen:
            Kit._pos_screen = wh
            Kit.put_var(Kit.SCREEN_KEY, "%d,%d" % wh)

    # ---------- art ----------
    @staticmethod
    def pic_size(graphic):
        """Pixel size of a gump graphic, measured from the client (cached)."""
        wh = Kit._sizes.get(graphic)
        if wh is None:
            w = h = 0
            try:
                p = G.CreateGumpPic(graphic)
                w, h = int(p.GetWidth() or 0), int(p.GetHeight() or 0)
                try:
                    p.Dispose()
                except Exception:
                    pass
            except Exception:
                pass
            wh = Kit._sizes[graphic] = (w, h)
        return wh

    @staticmethod
    def add_pic(g, graphic, x, y, hue=0, mouse=True):
        try:
            p = G.CreateGumpPic(graphic, x, y, hue) if hue else G.CreateGumpPic(graphic, x, y)
            p.SetPos(x, y)
            if not mouse:                    # clicks go through to the window under it
                try:
                    p.SetAcceptMouseInput(False)
                except Exception:
                    pass
            g.Add(p)
            return p
        except Exception:
            return None

    @staticmethod
    def add_tiled(g, graphic, x, y, w, h, alpha=None, fallback="#101010", hue=0):
        if w <= 0 or h <= 0:
            return None
        try:
            t = (G.CreateTiledGumpPic(graphic, w, h, hue) if hue
                 else G.CreateTiledGumpPic(graphic, w, h))
        except Exception:
            t = G.CreateGumpColorBox(alpha if alpha is not None else 1.0, fallback)
        t.SetRect(x, y, w, h)
        if alpha is not None:
            try:
                t.SetAlpha(alpha)
            except Exception:
                pass
        try:
            t.SetAcceptMouseInput(False)
        except Exception:
            pass
        g.Add(t)
        return t

    @staticmethod
    def add_box(g, x, y, w, h, alpha=0.5, color="#FFFFFF"):
        """A flat translucent rectangle (grid lines, markers); never takes the mouse."""
        if w <= 0 or h <= 0:
            return None
        try:
            b = G.CreateGumpColorBox(alpha, color)
        except Exception:
            return None
        b.SetRect(x, y, w, h)
        try:
            b.SetAcceptMouseInput(False)
        except Exception:
            pass
        g.Add(b)
        return b

    @staticmethod
    def add_resizepic(g, base, x, y, w, h, mouse=True):
        """Draw a 9-piece UO background (like a server gump's AddBackground).
        Returns the controls drawn."""
        s = Kit._rp_sizes.get(base)          # (2.6.82) the nine sizes, once per art
        if s is None:
            s = [Kit.pic_size(base + i) for i in range(9)]
            if all(p[0] > 0 and p[1] > 0 for p in s):
                Kit._rp_sizes[base] = s
        tl, t, tr, l, c, r, bl, b, br = s
        if any(p[0] <= 0 or p[1] <= 0 for p in s):
            return [Kit.add_tiled(g, base + 4, x, y, w, h)]   # can't measure: centre only
        out = [
            Kit.add_tiled(g, base + 4, x + l[0], y + t[1], w - l[0] - r[0], h - t[1] - b[1]),
            Kit.add_tiled(g, base + 1, x + tl[0], y, w - tl[0] - tr[0], t[1]),
            Kit.add_tiled(g, base + 7, x + bl[0], y + h - b[1], w - bl[0] - br[0], b[1]),
            Kit.add_tiled(g, base + 3, x, y + tl[1], l[0], h - tl[1] - bl[1]),
            Kit.add_tiled(g, base + 5, x + w - r[0], y + tr[1], r[0], h - tr[1] - br[1]),
            Kit.add_pic(g, base + 0, x, y, mouse=mouse),
            Kit.add_pic(g, base + 2, x + w - tr[0], y, mouse=mouse),
            Kit.add_pic(g, base + 6, x, y + h - bl[1], mouse=mouse),
            Kit.add_pic(g, base + 8, x + w - br[0], y + h - br[1], mouse=mouse)]
        out = [p for p in out if p is not None]
        try:                                 # (2.6.78) a background, not controls (Check look)
            backs = Kit._back_parts
            if len(backs) > 64:
                for k in [k for k in backs if not Kit.is_open(k)]:
                    backs.pop(k, None)
            backs.setdefault(g, []).extend(out)
        except TypeError:
            pass
        return out

    @staticmethod
    def _frame_pieces(g, w, h, corners=True, mouse=True):
        """The stone frame's controls: the 9-piece frame and, with corners,
        the knot on each corner. Returns them."""
        out = Kit.add_resizepic(g, Kit.WINDOW_BG, 0, 0, w, h, mouse)
        if corners and Kit.CORNER_ART:
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch:
                for cx, cy in ((0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)):
                    p = Kit.add_pic(g, Kit.CORNER_ART, cx, cy, mouse=mouse)
                    if p is not None:
                        out.append(p)
        if type(g) is not PageCanvas:        # (2.6.70) the one frame (Surround) hides these
            try:
                parts = Kit._frame_parts
                if len(parts) > 64:          # closed windows: let them go
                    for k in [k for k in parts if not Kit.is_open(k)]:
                        parts.pop(k, None)
                parts[g] = [p for p in out if p is not None]
            except TypeError:
                pass
        return out

    @staticmethod
    def add_window_frame(g, w, h, corners=True, mouse=True):
        """The stone frame. mouse=False lets clicks on it reach the window
        itself (a resizable window is resized by dragging its corners). The
        pieces are noted until the window is placed, so a window taller than
        the screen can have its frame drawn again at the size it gets
        (Kit.place / scroll_fit); the note goes when the window does."""
        pieces = Kit._frame_pieces(g, w, h, corners, mouse)
        if type(g) is not PageCanvas:
            if len(Kit._frames) > 32:        # closed windows: let their notes go
                for k in [k for k in Kit._frames if not Kit.is_open(k)]:
                    Kit._frames.pop(k, None)
                if len(Kit._frames) > 48:
                    Kit._frames.clear()
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}

    @staticmethod
    def add_section(g, x, y, w, h, title=None, alpha=None):
        """A translucent black block, like each part of the crafting gump."""
        if type(g) is PageCanvas:            # a settings page being laid out
            g.sections.append((x, y, w, h))
        t = Kit.add_tiled(g, Kit.SECTION_TILE, x, y, w, h,
                          Kit.SECTION_ALPHA if alpha is None else alpha)
        if title:
            Kit.add_label(g, title, x + 8, y + 6, Kit.HUE_TITLE)
        return t

    # ---------- controls ----------
    @staticmethod
    def add_label(g, text, x, y, hue=None):
        lbl = G.CreateGumpLabel(text, Kit.HUE_TEXT if hue is None else hue)
        lbl.SetPos(x, y)
        g.Add(lbl)
        return lbl

    @staticmethod
    def add_check(g, text, x, y, checked=False, tooltip=None):
        cb = G.CreateGumpCheckbox(text, Kit.HUE_TEXT, checked)   # client checkbox art
        cb.SetPos(x, y)
        if tooltip:
            try:
                cb.SetTooltip(tooltip)
            except Exception:
                pass
        g.Add(cb)
        return cb

    @staticmethod
    def add_textbox(g, text, x, y, w=60, numbers=True, font=16):
        """A text field on its tile. (2.6.78) font: its font size; a window that
        lays itself out at a scale k and then calls Kit.scale_window passes
        round(16 * k), since the client never scales a field's text (the
        field's box itself is scaled with the rest)."""
        Kit.add_tiled(g, Kit.FIELD_TILE, x - 2, y - 1, w + 4, 24)
        tb = G.CreateGumpTextBox(text, w, 22, False, font)
        tb.SetPos(x, y)
        if numbers:
            try:
                tb.NumbersOnly = True
            except Exception:
                pass
        g.Add(tb)
        return tb

    @staticmethod
    def add_slider(g, x, y, w, lo, hi, value):
        s = G.CreateSlider(w, lo, hi, int(value), x, y, True)
        g.Add(s)
        return s

    clicks_seen = False                  # a click handler has run: clicks do arrive

    @staticmethod
    def on_click(ctrl, fn):
        """Click handler that also gets the second click of a double-click.
        Every click pokes the host, so the window's module (and the settings
        window) act on it on the very next pass instead of their next due tick."""
        def handler(*args):
            Kit.clicks_seen = True
            twice = Client.second_click_swallowed()
            fn()
            if twice:                    # replay the click the client kept
                fn()
            HOST.poke()
        G.AddControlOnClick(ctrl, handler)

    _dbl = {}                            # key -> (time, window position)
    pending = []                         # double-clicks the client reported itself

    _fired = {}                          # key -> time it last ran (see once)

    @staticmethod
    def _forget_old(d, now, age=5.0):
        """Keep a key -> time dict (_fired, _dbl) small: a key is often id(window)
        and every rebuilt window brings a new one, while only the last second
        matters (double-click and repeat windows are under one second)."""
        if len(d) > 64:
            for k in [k for k, v in d.items()
                      if now - (v[0] if type(v) is tuple else v) > age]:
                d.pop(k, None)

    @staticmethod
    def once(fn, key):
        """fn, ignoring a repeat within 0.6s (one double-click can be seen
        both by our timing and by the client's own event)."""
        def run():
            now = time.time()
            if now - Kit._fired.get(key, 0.0) < 0.6:
                return
            Kit._fired[key] = now
            Kit._forget_old(Kit._fired, now)
            fn()
        return run

    @staticmethod
    def hook_double(api_ctrl, fn, queue=True):
        """Also listen to the client's own double-click event on the control,
        for when the client keeps the second click to itself. The event fires
        on the client's thread, so by default fn is only queued and the host
        runs it on its next pass. Returns True if the hook is in place."""
        try:
            import clr
            import System
            ctrl = Kit.client_control(api_ctrl)      # None: GetType() below fails
            t0 = ctrl.GetType()
            name = str(t0.FullName)
            # the event and its delegate type, found once per control type: the
            # reflection walk used to run per control (twenty pieces per
            # paperdoll redraw)
            found = Kit._dbl_events.get(name)
            if found is None:
                from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                t, ev = t0, None
                while t is not None and ev is None:
                    ev = t.GetEvent("MouseDoubleClick", flags)
                    t = t.BaseType
                found = (ev, clr.GetPythonType(ev.EventHandlerType), ev.GetAddMethod(True))
                if len(Kit._dbl_events) > 64:
                    Kit._dbl_events.clear()
                Kit._dbl_events[name] = found
            ev, delegate_type, add = found

            def handler(sender, e):
                try:
                    if str(e.Button) == "Left":
                        if queue:
                            Kit.pending.append(fn)
                        else:
                            fn()
                        e.Result = True
                except Exception:
                    pass
            add.Invoke(ctrl, System.Array[object]([delegate_type(handler)]))
            return True
        except Exception:
            return False

    _dbl_events = {}                     # control type name -> (event, delegate type, add method)

    @staticmethod
    def run_pending():
        while Kit.pending:
            lst, Kit.pending = Kit.pending, []   # (2.6.82) no pop(0); late ones in turn after
            for fn in lst:
                try:
                    fn()
                except Exception:
                    pass

    @staticmethod
    def on_moved(g, fn):
        """fn() each time the player has moved window g and let go of it (and
        when g moved because a window it is snapped to was dragged). Use it
        to save the window's position right away, so it is never lost."""
        SNAP.on_moved(g, fn)

    @staticmethod
    def moved_by_code(g):
        """Tell the snapping that window g was just placed by code (SetPos /
        SetRect on an open window: a tray put beside its bar, a grid under a
        title bar, a frame mirrored). Without it, on a client where the mouse
        button can't be read, every such move counts as a drag: after
        SNAP_SETTLE the window is snapped to its neighbours and its module
        told it was moved. Call it right after the move."""
        SNAP.moved_by_code(g)

    @staticmethod
    def typing():
        """True while keys go into a text field (see Typing)."""
        return Client.typing()

    @staticmethod
    def title_catcher(g, x, y, w, h, fn, key=None):
        """Invisible, draggable strip over a title: double-click it to run fn
        (minimize / restore). A drag also ends in a click, so the window must
        not have moved between the two clicks."""
        key = key or id(g)
        fn = Kit.once(fn, key)
        once = fn

        def fn():
            # (2.6.74) a click that ended a drag (or came while one is on) is no half
            # of a double-click: a tracker dragged on to its zone was minimized or
            # folded by the click that let it go, and seemed to vanish
            if Kit.just_dragged(g):
                Kit._dbl.pop(key, None)
                return
            once()

        def clicked():
            now = time.time()
            if Kit.just_dragged(g):              # (2.6.74) see fn above
                Kit._dbl.pop(key, None)
                return
            pos = (safe(lambda: g.GetX(), 0), safe(lambda: g.GetY(), 0))
            last = Kit._dbl.get(key)
            if last and now - last[0] <= 0.7 and abs(pos[0] - last[1][0]) <= 3 \
                    and abs(pos[1] - last[1][1]) <= 3:
                Kit._dbl.pop(key, None)
                fn()
            else:
                Kit._dbl[key] = (now, pos)
                Kit._forget_old(Kit._dbl, now)
        c = Kit.catcher(g, x, y, w, h, clicked, Kit.DOUBLE_TIP,
                        movable=True)
        if Client.mouse is None:
            Kit.hook_double(c, fn)
        return c

    DRAG_QUIET = 0.4                     # (2.6.74) s after a drag ends in which a click is its own

    @staticmethod
    def just_dragged(g):
        """(2.6.74) Window g is being dragged, or was let go DRAG_QUIET s ago or
        less: a click on it now is the end of the drag, not a click."""
        try:
            if g in SNAP.drag or g in SNAP.dragged:
                return True
            t = SNAP.drag_end.get(g)
            return t is not None and time.time() - t < Kit.DRAG_QUIET
        except Exception:
            return False

    @staticmethod
    def catcher(g, x, y, w, h, fn, tooltip=None, movable=False):
        """Invisible click target."""
        c = G.CreateGumpColorBox(0.01, "#000000")
        c.SetRect(x, y, w, h)
        Kit.on_click(c, fn)
        if tooltip:
            try:
                c.SetTooltip(tooltip)
            except Exception:
                pass
        if movable:
            try:
                c.CanMove = True
            except Exception:
                pass
        g.Add(c)
        return c

    @staticmethod
    def _click_handler(store, key, on_click=None):
        cdict = store[1]

        def handler(*args):
            cdict[key] = True
            if on_click is not None:
                on_click()
        return handler

    @staticmethod
    def art_button(g, store, key, art, x, y, label=None, tooltip=None, hue=None,
                   on_click=None):
        """Gump-art button, optionally with a clickable label to its right.
        `store` is the (buttons, clicks) registry of the window it belongs to.
        Clicks are either polled with was_clicked() or handed to on_click."""
        hue = Kit.HUE_TEXT if hue is None else hue
        bdict, cdict = store
        b = G.CreateGumpButton("", Kit.HUE_TEXT, art[0], art[1], art[2])
        b.SetPos(x, y)
        g.Add(b)
        bdict[key] = b
        cdict[key] = False
        # (2.6.85) every button can take a hotkey: see Binds
        bid = Binds.note(store, key, on_click, b, tooltip)
        click = Binds.wrap(bid, Kit._click_handler(store, key, on_click))
        Kit.on_click(b, click)
        combo = Binds.saved.get(bid)
        if combo:
            tooltip = (tooltip + " " if tooltip else "") + "(hotkey: %s)" % combo
        if tooltip:
            try:
                b.SetTooltip(tooltip)
            except Exception:
                pass
        if label:
            bw, bh = Kit.pic_size(art[0])
            lbl = Kit.add_label(g, label, x + (bw or 30) + 5,
                                y + max(((bh or 22) - 16) // 2, 0), hue)
            try:
                lbl.SetAcceptMouseInput(True)
                Kit.on_click(lbl, click)
            except Exception:
                pass
            return lbl
        return b

    _has_hbc = {}                        # control type -> has HasBeenClicked()

    @staticmethod
    def was_clicked(store, key):
        """A click on the button: the click handler's note, plus the client's
        own HasBeenClicked flag (asked only until a click handler has run)."""
        cdict = store[1]
        hit = cdict.get(key, False)
        if hit:
            cdict[key] = False
        if Kit.clicks_seen:                  # the usual case: the handler's note is enough
            return hit
        ctl = store[0].get(key)
        if ctl is not None:                  # until a click handler has run, ask the client
            t = type(ctl)                    # as well
            has = Kit._has_hbc.get(t)
            if has is None:
                has = Kit._has_hbc[t] = hasattr(ctl, "HasBeenClicked")
            if has:
                try:
                    hit = ctl.HasBeenClicked() or hit
                except Exception:
                    pass
        return hit

    #  What each label shows, as last set: label -> [text, hue]. Keyed by the
    #  label itself (identity), not id(label): id() of a client object is a slow
    #  lookup in IronPython and can be reused. Labels of closed windows are let
    #  go of once the dict passes _texts_cap; the cap then grows with the
    #  number still open, so the sweep stays rare however many there are.
    _texts = {}
    _texts_cap = 3000
    _texts_sweep = False                 # a sweep was put off until the next client pass
    _texts_list = None                   # (2.6.82) the labels being swept, and where it is
    _texts_at = 0
    TEXTS_SLICE = 400

    @staticmethod
    def set_text(lbl, text, hue=None):
        """Change a label only when needed. Returns True if the text changed.
        What a label shows is remembered here, so nothing is read back from
        the client after the first look (a read waits for the client, a write
        doesn't)."""
        try:
            e = Kit._texts.get(lbl)
        except TypeError:                    # an unhashable stand-in: not remembered
            e = [None, None]
        if e is None:
            try:
                cur = lbl.Text
            except Exception:
                cur = None
            e = Kit._texts[lbl] = [cur, None]
            if len(Kit._texts) > Kit._texts_cap:
                Kit._prune_texts()
        if e[0] != text:
            e[0] = text
            try:
                lbl.Text = text
            except Exception:
                try:
                    lbl.SetText(text)
                except Exception:
                    pass
            changed = True
        else:
            changed = False
        if hue is not None and e[1] != hue:
            e[1] = hue
            try:
                lbl.Hue = hue
            except Exception:
                pass
        return changed

    @staticmethod
    def _prune_texts():
        if not Client.on_client_thread():
            # every IsDisposed read below is a frame-wait off the client thread
            # (3000 of them: a long stall of the script thread); let the dict
            # grow a little and sweep it on the next client pass instead
            Kit._texts_cap = len(Kit._texts) + 500
            Kit._texts_sweep = True
            return
        # (2.6.82) swept in slices of TEXTS_SLICE labels per client pass (3000+
        # IsDisposed reads in one frame was a hitch); the cap grows meanwhile
        lst = Kit._texts_list
        if lst is None:
            lst = Kit._texts_list = list(Kit._texts)
            Kit._texts_at = 0
            Kit._texts_cap = len(Kit._texts) + 500
        Kit._texts_sweep = True
        i = Kit._texts_at
        end = min(len(lst), i + Kit.TEXTS_SLICE)
        texts = Kit._texts
        while i < end:
            lbl = lst[i]
            i += 1
            try:
                if lbl.IsDisposed:
                    texts.pop(lbl, None)
            except Exception:
                texts.pop(lbl, None)
        Kit._texts_at = i
        if i >= len(lst):
            Kit._texts_list = None
            Kit._texts_sweep = False
            Kit._texts_cap = max(3000, 2 * len(Kit._texts))

    #  Pixel widths of texts, measured once each. Bounded: texts made on the fly
    #  (names, numbers) would otherwise pile up for the whole session; past
    #  WIDTHS_MAX the cache starts over (a width costs one label to measure again).
    _widths = {}
    _ctl_prop = {}                          # (2.6.82) script control type -> its "Control" PropertyInfo
    _rp_sizes = {}                          # (2.6.82) add_resizepic: art base -> its nine sizes
    SWEEP_FULL = 5.0                        # (2.6.82) scroll_sweep's full child count at least this often
    WIDTHS_MAX = 4000

    @staticmethod
    def text_w(text):
        """Pixel width of text in the client's label font (measured once)."""
        px = Kit._widths.get(text)
        if px is None:
            px = 0
            try:
                l = G.CreateGumpLabel(text, Kit.HUE_TEXT)
                px = int(l.GetWidth() or 0)
                try:
                    l.Dispose()
                except Exception:
                    pass
            except Exception:
                pass
            px = px or 8 * len(text)
            if len(Kit._widths) >= Kit.WIDTHS_MAX:
                # (2.6.82) the long, one-off texts go first; the short ones (letters,
                # captions, numbers) are the ones asked for again and again
                wd = Kit._widths
                for k in [k for k in wd if len(k) > 12]:
                    del wd[k]
                if len(wd) >= Kit.WIDTHS_MAX // 2:
                    wd.clear()
            Kit._widths[text] = px
        return px

    @staticmethod
    def wrap(text, width):
        """text split into lines no wider than width. (2.6.82) With letter widths
        that add up (text_px) the line's width is carried along: no label is
        made for any candidate line, and the breaks are the same."""
        lines = []
        words = text.split()
        if words and Kit._px["ok"] is None:
            Kit.text_px("")                       # the one-time font check
        if Kit._px["ok"]:
            pad, cw = Kit._px["pad"], Kit._px_ch
            sp = cw.get(" ")
            if sp is None:
                sp = Kit._ch_w(" ")
            cur = 0
            for word in words:
                ww = Kit.text_px(word) - pad      # its letters
                if lines and cur + sp + ww <= width:
                    lines[-1] += " " + word
                    cur += sp + ww
                else:
                    lines.append(word)
                    cur = pad + ww
            return lines or [""]
        for word in words:
            if lines and Kit.text_w(lines[-1] + " " + word) <= width:
                lines[-1] += " " + word
            else:
                lines.append(word)
        return lines or [""]

    #  Text widths as a sum of letter widths (2.6.01, from the Skills module):
    #  the client's label font has no kerning, so the width of a text is a
    #  constant plus the width of each of its letters. Once a letter is known
    #  (one measurement, see text_w) every text made of known letters costs no
    #  label at all: names, numbers and trimmed texts (Kit.fit) that used to
    #  measure a new label per text (or per letter cut off) are free. Checked
    #  once against a measured reference text; if this client's font doesn't
    #  add up, text_px falls back to text_w (a measured, cached width).
    _px = {"ok": None, "pad": 0}
    _px_ch = {}
    PX_REF = "Total 120.0 / 700.0 (+5.2) Session ~1h 05m: Magery, Str"

    @staticmethod
    def _ch_w(ch):
        w = Kit.text_w("x" + ch + "x") - Kit.text_w("xx")
        Kit._px_ch[ch] = w
        return w

    @staticmethod
    def text_px(text):
        """Pixel width of text in the label font: the sum of its letters'
        widths when the font adds up (no label made for a text of known
        letters), else Kit.text_w."""
        px = Kit._px
        if px["ok"] is None:
            try:
                px["pad"] = 2 * Kit.text_w("x") - Kit.text_w("xx")
                ref = Kit.PX_REF
                px["ok"] = Kit.text_w(ref) == px["pad"] + sum(Kit._ch_w(ch) for ch in ref)
            except Exception:
                px["ok"] = False
        if not px["ok"]:
            return Kit.text_w(text)
        w, cw = px["pad"], Kit._px_ch
        for ch in text:
            x = cw.get(ch)
            w += Kit._ch_w(ch) if x is None else x
        return w

    @staticmethod
    def fit(text, width, tail=".."):
        """text cut short, with `tail` after it, when it is wider than width
        pixels in the label font (letter widths when the font adds up, else
        the longest fitting start found by halving: a few labels, not one per
        letter)."""
        text = str(text or "")
        if len(text) * 9 <= width or Kit.text_px(text) <= width:
            return text
        if Kit._px["ok"]:                         # letters add up: take them off one by one
            w, cw = Kit.text_px(text + tail), Kit._px_ch
            while text and w > width:
                w -= cw.get(text[-1], 0)
                text = text[:-1]
            return text.rstrip() + tail
        lo, hi = 1, len(text) - 1                 # text[:lo] is kept even if it doesn't fit
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if Kit.text_w(text[:mid] + tail) <= width:
                lo = mid
            else:
                hi = mid - 1
        return text[:lo].rstrip() + tail

    # ---------- a server gump's layout (PacketGumpText), 2.6.01 ----------
    #  TazUO keeps a server gump's layout in PacketGumpText: the text lines,
    #  one a line, then the commands, one a line (the last text line and the
    #  first command share a line). Grimoire (runebooks, spellbooks) and
    #  Social (the guild window) each carried a copy of this parser; it lives
    #  here now, so a fix lands once. Basic string operations only: IronPython
    #  disagreed with CPython on fancier versions.
    GUMP_CMDS = ("page", "button", "buttontileart", "checkertrans", "croppedtext", "gumppic",
                 "gumppictiled", "gumppichued", "gumppicphued", "htmlgump", "xmfhtmlgump",
                 "xmfhtmlgumpcolor", "xmfhtmltok", "noclose", "nodispose", "nomove", "noresize",
                 "group", "endgroup", "radio", "checkbox", "resizepic", "text", "textentry",
                 "textentrylimited", "tilepic", "tilepichue", "tooltip", "itemproperty",
                 "mastergump", "picinpic", "picinpichued", "picinpicphued",
                 "togglelimitgumpscale", "maparea")
    _gump_cmds = frozenset(GUMP_CMDS)
    _cliloc_cache = {}

    @staticmethod
    def gump_is_int(a):
        a = str(a)
        if a.startswith("-"):
            a = a[1:]
        return len(a) > 0 and a.isdigit()

    @staticmethod
    def _gump_arg_ok(a):
        """A command argument: an integer, a #cliloc, a name=value option
        (gumppic's hue=N / class=Name) or an @text@ argument."""
        if Kit.gump_is_int(a):
            return True
        if a.startswith("#"):
            return Kit.gump_is_int(a[1:])
        if "=" in a:
            return a.split("=", 1)[0].isalnum()
        return a.startswith("@") or a.endswith("@")

    @staticmethod
    def gump_is_cmd(line):
        """Is this line a gump command? Its first word must be a command AND
        every other token an integer, a #cliloc or part of an @text@ argument:
        a text line that merely starts with such a word ("Page 2 Boss", "Text
        me", "Group leader") is text."""
        words = str(line).strip().split()
        if not words or words[0].lower() not in Kit._gump_cmds:
            return False
        inside = False                            # inside an @...@ argument with spaces
        for a in words[1:]:
            if inside:
                if a.endswith("@"):
                    inside = False
                continue
            if a.startswith("@") and not (len(a) > 1 and a.endswith("@")):
                inside = True
                continue
            if not Kit._gump_arg_ok(a):
                return False
        return True

    @staticmethod
    def _gump_split_merged(merged):
        """The last text line and the first command are glued together; pull
        them apart: (text, command) or (text, None)."""
        merged = str(merged)
        low = merged.lower()
        n = len(merged)
        for p in range(n):
            for kw in Kit.GUMP_CMDS:
                end = p + len(kw)
                if low[p:end] != kw:
                    continue
                if end < n and merged[end] != " ":
                    continue
                if Kit.gump_is_cmd(merged[p:]):
                    return merged[:p], merged[p:]
        return merged, None

    @staticmethod
    def gump_parse(raw):
        """(text_lines, command_token_lists) of a PacketGumpText."""
        raw = str(raw or "").replace("\r", "").replace("\x00", "")
        parts = raw.split("\n")
        while parts and parts[-1].strip() == "":
            parts.pop()
        j = len(parts)
        while j > 0 and Kit.gump_is_cmd(parts[j - 1]):
            j -= 1
        if j == 0:
            lines, cmds = [], parts
        else:
            tail, first = Kit._gump_split_merged(parts[j - 1])
            if first is None:          # last text line was empty
                lines, cmds = parts[:j] + [""], parts[j:]
            else:
                lines, cmds = parts[:j - 1] + [tail], [first] + parts[j:]
        return lines, [c.split() for c in cmds]

    _HTML_RE = re.compile(r"<[^>]*>")       # (2.6.82) compiled once

    @staticmethod
    def strip_html(s):
        return Kit._HTML_RE.sub("", str(s or "")).replace("&nbsp;", " ").strip()

    @staticmethod
    def cliloc_text(n, clilocs=None):
        """The client's text of cliloc number n: the caller's own table first
        (clilocs: {number: text}), then API.GetClilocString when the build has
        it (remembered), else "#n"."""
        if clilocs:
            t = clilocs.get(n)
            if t is not None:
                return t
        t = Kit._cliloc_cache.get(n)
        if t is None:
            t = str(safe(lambda: API.GetClilocString(n), "") or "").strip() or ("#%d" % n)
            if len(Kit._cliloc_cache) > 500:
                Kit._cliloc_cache.clear()
            Kit._cliloc_cache[n] = t
        return t

    @staticmethod
    def gump_cells(raw, clilocs=None):
        """The texts of a gump: [{"x", "y", "w", "h", "text", "raw", "cliloc",
        "bg"}] (text with HTML stripped, raw as sent), and its reply buttons
        [(x, y, id)]. Text controls: htmlgump (text index), xmfhtmlgump /
        xmfhtmlgumpcolor (cliloc), xmfhtmltok (cliloc + arguments), text and
        croppedtext (text index). `clilocs` is an own {number: text} table
        looked at before the client's (see cliloc_text)."""
        lines, cmds = Kit.gump_parse(raw)
        cells, buttons = [], []
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "button" and len(t) >= 8:
                    if int(t[5]) == 1:
                        buttons.append((int(t[1]), int(t[2]), int(t[7])))
                    continue
                cell = None
                if k == "htmlgump" and len(t) >= 8:
                    src = lines[int(t[5])]
                    cell = {"x": int(t[1]), "y": int(t[2]), "w": int(t[3]), "h": int(t[4]),
                            "raw": src, "text": Kit.strip_html(src), "cliloc": 0,
                            "bg": int(t[6]) != 0}
                elif k in ("xmfhtmlgump", "xmfhtmlgumpcolor") and len(t) >= 8:
                    cl = int(str(t[5]).replace("#", ""))
                    cell = {"x": int(t[1]), "y": int(t[2]), "w": int(t[3]), "h": int(t[4]),
                            "raw": "", "text": Kit.cliloc_text(cl, clilocs), "cliloc": cl,
                            "bg": int(t[6]) != 0}
                elif k == "xmfhtmltok" and len(t) >= 9:
                    cl = int(str(t[8]).replace("#", ""))
                    cell = {"x": int(t[1]), "y": int(t[2]), "w": int(t[3]), "h": int(t[4]),
                            "raw": "", "text": Kit.cliloc_text(cl, clilocs), "cliloc": cl,
                            "bg": int(t[5]) != 0}
                elif k == "text" and len(t) >= 5:
                    src = lines[int(t[4])]
                    cell = {"x": int(t[1]), "y": int(t[2]), "w": 0, "h": 0, "raw": src,
                            "text": Kit.strip_html(src), "cliloc": 0, "bg": False}
                elif k == "croppedtext" and len(t) >= 7:
                    src = lines[int(t[6])]
                    cell = {"x": int(t[1]), "y": int(t[2]), "w": int(t[3]), "h": int(t[4]),
                            "raw": src, "text": Kit.strip_html(src), "cliloc": 0, "bg": False}
                if cell is not None:
                    cells.append(cell)
            except (ValueError, IndexError):
                continue
        return cells, buttons

    @staticmethod
    def dispose(ctrl):
        if ctrl is not None:
            try:
                ctrl.Dispose()
            except Exception:
                pass

    @staticmethod
    def is_open(g):
        if g is None:
            return False
        try:
            return not g.IsDisposed
        except Exception:
            return False

    # ---------- per-character saved values, positions, standard window parts ----------
    @staticmethod
    def get_var(key, default=""):
        """A per-character saved string (default when unset or unreadable)."""
        try:
            v = API.GetPersistentVar(key, default, API.PersistentVar.Char)
        except Exception:
            v = default
        return str(v or default)

    @staticmethod
    def put_var(key, value):
        try:
            API.SavePersistentVar(key, value, API.PersistentVar.Char)
        except Exception:
            pass

    @staticmethod
    def load_pos(key, default=(200, 200), size=None):
        """A window position saved with save_pos, as (x, y), adapted to the
        screen of today (Kit.adapt); with size=(w, h) it is also kept wholly
        on screen (Kit.place does that too when the window is built)."""
        try:
            x, y = Kit.get_var(key, "%d,%d" % default).split(",")
            x, y = int(x), int(y)
        except Exception:
            x, y = default
        w, h = size if size else (0, 0)
        return Kit.adapt(x, y, w, h)

    @staticmethod
    def load_min(key):
        """Was the window minimized when last seen? (see save_min)"""
        return Kit.get_var(key, "0") == "1"

    @staticmethod
    def save_min(key, minimized):
        """Remember whether the window is minimized (saved the moment it changes)."""
        Kit.put_var(key, "1" if minimized else "0")

    @staticmethod
    def save_pos(key, g):
        if Kit.is_open(g):
            try:
                API.SavePersistentVar(key, "%d,%d" % (g.GetX(), g.GetY()), API.PersistentVar.Char)
            except Exception:
                pass

    @staticmethod
    def queuer(st):
        """queue(action) -> a click handler that adds action to st["queue"]
        (once) for the module's next tick: clicks never do the work."""
        def queue(action):
            def handler(*args):
                if action not in st["queue"]:
                    st["queue"].append(action)
            return handler
        return queue

    @staticmethod
    def disposer(key, st, win):
        """on_disposed(g) -> handler: window g going away turns module `key`
        off, unless the module replaced it itself (win["g"] moved on) or is
        shutting down (st["shutting"])."""
        def on_disposed(g):
            def handler(*args):
                if win["g"] is g and not st["shutting"]:
                    win["g"] = None
                    HOST.disable(key)
            return handler
        return on_disposed

    TITLE_GAP = 6                        # (2.6.78) px kept between the title and the first button
    CAP_GAP = 10                         # px between two captioned buttons of a title row
    BARE_GAP = 4                         # ...and between two of them drawn without captions

    @staticmethod
    def caption_tip(caption, tip):
        """(2.6.78) A button's tooltip when its caption can't be shown (ui-text 2.3):
        the caption first, then the tooltip (`Settings: open the Bags settings page`)."""
        tip = str(tip or "")
        if not tip:
            return caption
        return "%s: %s%s" % (caption, tip[:1].lower(), tip[1:])

    @staticmethod
    def title_plan(w, title, buttons, after=None):
        """(2.6.78) How a title row fits w px: (captions shown, show `after`, the
        title as drawn, the x of every captioned button right to left, the
        leftmost x). buttons: [(caption, ...)] right to left, left of Settings'
        place (Settings first when the window has a page). The captions go
        first (each button drawn at its art alone, from the right), then the
        grey label after the title, then the title is cut with Kit.fit."""
        M = Kit.MARGIN
        right = w - M - 84 - Kit.DOCK_DX         # Settings' right end (its caption's end)
        t0 = M + 30
        caps_w = [35 + Kit.text_w(b[0]) for b in buttons]

        def xs(with_caps):
            out, x = [], right
            for cw in caps_w:
                x -= cw if with_caps else 30
                out.append(x)
                x -= Kit.CAP_GAP if with_caps else Kit.BARE_GAP
            return out
        tw = Kit.text_w(title.upper())
        aw = (8 + Kit.text_w(after)) if after else 0
        for with_caps in (True, False):
            pos = xs(with_caps)
            left = pos[-1] if pos else right
            if t0 + tw + aw + Kit.TITLE_GAP <= left:
                return with_caps, bool(after), title.upper(), pos, left
        pos = xs(False)
        while pos and pos[-1] < M + 4:           # a row narrower than its buttons: the
            pos.pop()                            # leftmost go (never off the window)
        left = pos[-1] if pos else right
        if t0 + tw + Kit.TITLE_GAP <= left:
            return False, False, title.upper(), pos, left
        room = left - Kit.TITLE_GAP - t0
        if room < Kit.text_w("W.."):             # no room for even a cut title
            return False, False, "", pos, left
        return False, False, Kit.fit(title.upper(), room), pos, left

    @staticmethod
    def title_bar(g, store, w, title, key, on_min, on_dock, on_settings=None, close_tip=None,
                  extra=None, after=None):
        """The title section of a full window: TITLE, a double-click strip,
        then (right to left) Close, Minimize, Fold into the Action Bar and,
        with on_settings, Settings. Returns the x where the buttons start, for
        more buttons to the left of them. close_tip: the Close button's
        tooltip when Kit.CLOSE_TIP isn't right (a window that closes
        without turning its module off: pass "Close").
        (2.6.78) extra: [(key, art, caption, tooltip, on_click)] buttons left of
        Settings, right to left; after: a grey label right after the title (a
        count: "BAGS  8"). The row fits its width (Kit.title_plan): when the
        captions don't all fit with Kit.TITLE_GAP to spare, every captioned
        button is drawn without its caption, its tooltip starting with the
        caption; still too tight, the title is cut (its whole text on the
        title strip's tooltip)."""
        M = Kit.MARGIN
        Kit.add_section(g, M, M, w - 2 * M, 30)
        buttons = []
        if on_settings is not None:
            buttons.append(("Settings", "settings", Kit.ART_PAGE, Kit.SETTINGS_TIP % title,
                            on_settings))
        for b in (extra or ()):
            buttons.append((b[2], b[0], b[1], b[3], b[4]))
        # (2.6.85) a window in a zone is always up: no Minimize, Close or fold arrow and
        # no double-click; its own buttons move right into their room
        zoned = Kit.zone_up(key)
        shift = (84 + Kit.DOCK_DX - 10) if zoned else 0
        caps, show_after, shown, pos, left = Kit.title_plan(w + shift, title, buttons, after)
        lbl = Kit.add_label(g, shown, M + 30, M + 7, Kit.HUE_TITLE)
        if show_after:
            Kit.add_label(g, after, M + 30 + Kit.text_w(shown) + 8, M + 7, Kit.HUE_INFO)
        Kit.note_title(g, M)                 # (2.6.72) for Check look
        if zoned:                            # dragged in Arrange mode; nothing to double-click
            strip = Kit.catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, lambda *a: None,
                                None, movable=True)
        else:
            strip = Kit.title_catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, on_min, key=key)
        if shown != title.upper():           # cut: the whole title on the strip
            try:
                strip.SetTooltip(title if zoned else "%s. %s." % (title, Kit.DOUBLE_TIP))
            except Exception:
                pass
        for (cap, bkey, art, tip, fn), x in zip(buttons, pos):
            if caps:
                Kit.art_button(g, store, bkey, art, x, M + 4, cap, tip, on_click=fn)
            else:
                Kit.art_button(g, store, bkey, art, x, M + 4, None, Kit.caption_tip(cap, tip),
                               on_click=fn)
        if not zoned:
            Kit.dock_button(g, store, w - M - 74, M + 7, on_click=on_dock)
            Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP,
                           on_click=on_min)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None,
                           close_tip or Kit.CLOSE_TIP % title)
        return pos[-1] if pos else w - M - 84 - Kit.DOCK_DX + shift

    @staticmethod
    def zone_up(key):
        """(2.6.85) Window `key` sits in a zone: it is always up, full size."""
        try:
            return bool(HOST.layout_holds(key))
        except Exception:
            return False

    _mouse = [None]                      # (2.6.72) the client's Mouse.Position getter, or False

    @staticmethod
    def mouse_pos():
        """(2.6.72) (x, y) of the mouse in gump pixels, or None when the client
        won't say. Client thread."""
        f = Kit._mouse[0]
        if f is None:
            Kit._mouse[0] = False
            t = Client._type("ClassicUO.Input.Mouse")
            if t is not None:
                try:
                    m = Client._member(t, "Position")
                    p = m[0]()
                    int(p.X)
                    Kit._mouse[0] = m[0]
                except Exception:
                    pass
            f = Kit._mouse[0]
        if not f:
            return None
        try:
            p = f()
            return int(p.X), int(p.Y)        # (the space the client hit-tests gumps in)
        except Exception:
            return None

    _titled = {}                         # (2.6.72) window -> y of its standard title row

    @staticmethod
    def note_title(g, y):
        """(2.6.72) Window g has the standard title row (30 px) at y: Check look
        reads it, to see that title rows in a row of zones line up."""
        try:
            t = Kit._titled
            if len(t) > 64:
                for k in [k for k in t if not Kit.is_open(k)]:
                    t.pop(k, None)
            t[g] = int(y)
        except TypeError:
            pass

    _scenes = {}                         # (2.6.78) window -> [(x, y, w, h)] its scenes
    _scene_parts = {}                    # (2.6.78) window -> the controls its scene animates

    @staticmethod
    def note_scene(g, x, y, w, h, pieces=None):
        """(2.6.78) Window g draws a scene at (x, y), w x h (Mongotchi's pen, the
        bag canvas): pictures in it overlap on purpose, so Check look's overlap
        test leaves them out. Noted again on every build (the last one counts
        for each place). pieces: controls that move with the scene's animation
        (a speech line over the pet): left out of Check look altogether."""
        try:
            t = Kit._scenes
            if len(t) > 64:
                for k in [k for k in t if not Kit.is_open(k)]:
                    t.pop(k, None)
                for k in [k for k in Kit._scene_parts if not Kit.is_open(k)]:
                    Kit._scene_parts.pop(k, None)
            if pieces:
                Kit._scene_parts[g] = [p for p in pieces if p is not None]
            r = (int(x), int(y), int(w), int(h))
            lst = [q for q in t.get(g, []) if (q[0], q[1]) != (r[0], r[1])]
            lst.append(r)
            t[g] = lst[-4:]
        except TypeError:
            pass

    @staticmethod
    def mini_bar(g, store, w, h, title, key, on_restore, text="", hue=None, close_tip=None):
        """A minimized window: small stone bar, one section, a label (returned),
        a double-click strip, Restore and Close."""
        Kit.add_window_frame(g, w, h, corners=False)
        Kit.add_section(g, 8, 8, w - 16, h - 16)
        lbl = Kit.add_label(g, text, 18, 15, Kit.HUE_INFO if hue is None else hue)
        # its own double-click key: the full window's strip and this one used
        # to share `key`, so the debounce after a double-click that minimized
        # swallowed a restore double-click in the next 0.6 s
        Kit.title_catcher(g, 8, 8, w - 70, h - 16, on_restore, key=str(key) + ":mini")
        Kit.art_button(g, store, "restore", Kit.ART_RESTORE, w - 60, 15, None, Kit.RESTORE_TIP,
                       on_click=on_restore)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - 44, 12, None,
                       close_tip or Kit.CLOSE_TIP % title)
        return lbl

    @staticmethod
    def dock_button(g, store, x_min, y_min, on_click=None, key="tobar"):
        """The "Fold into the Action Bar" button, placed beside a Minimize
        arrow drawn at (x_min, y_min): DOCK_DX px to its left. Its click
        should end in HOST.dock_to_bar(<module key>) on the module's tick."""
        return Kit.art_button(g, store, key, Kit.ART_DOCK, x_min - Kit.DOCK_DX,
                              y_min + Kit.DOCK_DY, None, Kit.DOCK_TIP, on_click=on_click)

    @staticmethod
    def dock_hooks(title, icon, st, win, redraw, scale=False, fit=None):
        """Dock-registry hooks (see Host.dock_add) for a module whose window
        is win["g"] and whose "minimized", "docked" and "shutting" flags are
        in st; redraw() rebuilds the window on the module's next pass.
        "minimize" is the window's own minimized form (not folded), used by
        HOST.dock_to_bar while the Action Bar isn't on screen.
        For the layout's zone fill (2.6.56, see Layout._fit_slot):
          fit=fn(w, h, mode) says the module lays the window out for its
            slot in a zone, w x h px, itself (mode is always "w"), and is
            called with (None, None, None) when the window is freed. It runs
            on the client thread in the keeper's pass: record and queue a
            rebuild, never wait. Add hooks["exact"] = True when the window
            then is exactly w x h; without it the layout fits the rest
            (Fill), as it does every window with no "fit". hooks["fill"]:
            "grid" or "frame" (see Fill). scale=True is still taken (2.6.55)
            and means nothing now."""
        def state():
            if win["g"] is None or st["shutting"]:
                return None
            return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")

        def show():
            st["docked"], st["minimized"] = False, False
            redraw()

        def dock():
            st["docked"], st["minimized"] = True, True
            redraw()

        def undock():
            st["docked"] = False
            redraw()

        def minimize():
            st["docked"], st["minimized"] = False, True
            redraw()

        def gump():
            return win["g"]
        hooks = {"title": title, "icon": icon, "state": state, "show": show, "dock": dock,
                 "undock": undock, "minimize": minimize, "gump": gump, "redraw": redraw}
        if scale:
            hooks["scale"] = True
        if fit is not None:
            hooks["fit"] = fit
        return hooks

    # ---------- reading controls back ----------
    @staticmethod
    def flush():
        """Run the client's queued control changes now. SetPos, SetRect and
        Add on a control are queued by the client and run on a later frame,
        while GetX / GetY answer at once: anything that reads a freshly made
        control's place or children must call this first. Only works on the
        client thread (Kit.on_client). True when the queue is empty after."""
        MTQ = Client._find_mtq()
        if MTQ is None or not Client.on_client_thread():
            return False
        try:
            n = 0
            while int(MTQ.Count) > 0 and n < 500:
                MTQ.ProcessQueue()           # 5 ms of queued work per call
                n += 1
            return int(MTQ.Count) == 0
        except Exception:
            return False

    # ---------- scaling a whole window ----------
    @staticmethod
    def client_control(api_ctrl):
        """The client's own control behind a script control (or None).
        (2.6.82) The "Control" property is looked up once per script control
        type (a type's members don't change while the game runs)."""
        try:
            pt = type(api_ctrl)
            cache = Kit._ctl_prop
            prop = cache.get(pt, False)
            if prop is False:
                prop = None
                import clr
                from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                t = clr.GetClrType(pt)
                while t is not None:
                    prop = t.GetProperty("Control", flags)
                    if prop is not None:
                        break
                    t = t.BaseType
                cache[pt] = prop
            if prop is not None:
                return prop.GetValue(api_ctrl, None)
        except Exception:
            pass
        return None

    @staticmethod
    def _scroll_skip(g):
        """(controls to leave alone, the scroll area) of a window the scroll
        conversion (2.6.53) touched: its new frame and band pieces, the scroll
        area and the client's own scrollbar inside it were made at the size
        the window has now and are never scaled; the area's other children
        (the window's body) are."""
        info = Kit._scrolled.get(g)
        if info is None:
            return [], None
        base = info.get("skip_raw")              # (2.6.82) resolved once per conversion
        if base is None:
            base = []
            for p in info["frame"] + info["band"]:
                pr = Kit.client_control(p)
                if pr is not None:
                    base.append(pr)
            info["skip_raw"] = base
        skip = list(base)
        area = info["area_raw"]
        try:
            kids = area.Children
            if int(kids.Count) > 0:
                skip.append(kids[0])             # the client's scrollbar
        except Exception:
            pass
        return skip, area

    @staticmethod
    def scale_window(g, scale):
        """Draw everything in window g at `scale` (1.0 = as built): the
        client's own control scaling (the one its paperdoll and skills
        windows use), applied to every control and what is inside it. The
        window's own size is set by the caller. Call on a freshly built
        window; calling it again scales only the controls added since (a
        control already at that scale is left alone), and the pieces of a
        scroll conversion are never touched. True if it worked."""
        if abs(scale - 1.0) < 0.001:
            return True
        root = Kit.client_control(g)
        if root is None or not Kit.flush():      # the controls are added by the queue
            return False
        skip, area = Kit._scroll_skip(g)
        same = Kit._same()

        def tree(c):
            if skip and any(same(c, k) for k in skip):
                return
            if area is None or not same(c, area):
                if str(c.GetType().Name) == "GumpPicTiled":
                    safe(lambda: setattr(c, "ScaleTiledTexture", True))   # the tile scales too
                c.ApplyScale(scale, True, True, False)
            kids = c.Children
            for i in range(kids.Count):
                tree(kids[i])
        try:
            kids = root.Children
            for i in range(kids.Count):
                tree(kids[i])
            return True
        except Exception:
            return False

    @staticmethod
    def rescale_window(g, old, new):
        """(2.6.55) A window already drawn at scale `old` drawn at `new`
        instead, in place: every control's place and size are multiplied by
        new / old and its mouse scale set to `new` (a label's size is taken
        from its text again). For the layout's zone fit when a window can't
        be rebuilt; a rebuild then Kit.scale_window is the better way (int
        rounding drifts a pixel over many rescales). True if it worked."""
        old, new = float(old or 1.0), float(new or 1.0)
        if abs(new - old) < 0.001:
            return True
        if abs(new - 1.0) < 0.001 and abs(old - 1.0) < 0.001:
            return True
        k = new / old
        root = Kit.client_control(g)
        if root is None or not Kit.flush():
            return False
        skip, area = Kit._scroll_skip(g)
        same = Kit._same()

        def tree(c):
            if skip and any(same(c, s) for s in skip):
                return
            if area is None or not same(c, area):
                if str(c.GetType().Name) == "Label":
                    c.ApplyScale(k, True, False, True)      # the place; the size follows the text
                    c.ApplyScale(new, False, True, True)    # ... at the new mouse scale
                else:
                    if str(c.GetType().Name) == "GumpPicTiled":
                        safe(lambda: setattr(c, "ScaleTiledTexture", True))
                    c.ApplyScale(k, True, True, True)
                    c.SetInternalScale(new)
            kids = c.Children
            for i in range(kids.Count):
                tree(kids[i])
        try:
            kids = root.Children
            for i in range(kids.Count):
                tree(kids[i])
            return True
        except Exception:
            return False

    # ---------- moving a control after drawing it (2.6.56) ----------
    #  A window in a zone is fitted to its slot (Fill): its controls are not
    #  where the module put them. A module that moves or resizes a control of
    #  a window after drawing it does so through these, which pass the change
    #  through the window's fit (and set it as it is when the window isn't
    #  fitted); Kit.ui_x / ui_y / ui_w read back the place the module gave.
    @staticmethod
    def ui_pos(c, x, y):
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, x=x, y=y)):
            c.SetPos(int(x), int(y))

    @staticmethod
    def ui_rect(c, x, y, w, h):
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, x, y, w, h)):
            c.SetRect(int(x), int(y), int(w), int(h))

    @staticmethod
    def ui_w(c, w):
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, w=w)):
            c.SetWidth(int(w))

    @staticmethod
    def ui_h(c, h):
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, h=h)):
            c.SetHeight(int(h))

    @staticmethod
    def ui_size(c, w, h):
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, w=w, h=h)):
            c.SetWidth(int(w))
            c.SetHeight(int(h))

    @staticmethod
    def ui_x(c):
        own = Fill.own(c) if Fill.recs else None
        return own[0] if own is not None else c.GetX()

    @staticmethod
    def ui_y(c):
        own = Fill.own(c) if Fill.recs else None
        return own[1] if own is not None else c.GetY()

    # ---------- spells, shared by every module that knows them (2.6.05) ----------
    #  SPELL_WORDS: your words of power (lower case) -> (spell, kind); kind
    #  "heal" / "cure" / "cure+" marks the spells Meters counts as healing and
    #  cures. Meters, the Frames part's cast bar and the Action Bar read this one copy.
    SPELL_WORDS = {
        "uus jux": ("Clumsy", None), "in mani ylem": ("Create Food", None),
        "rel wis": ("Feeblemind", None), "in mani": ("Heal", "heal"),
        "in por ylem": ("Magic Arrow", None), "in lor": ("Night Sight", None),
        "flam sanct": ("Reactive Armor", None), "des mani": ("Weaken", None),
        "ex uus": ("Agility", None), "uus wis": ("Cunning", None),
        "an nox": ("Cure", "cure"), "an mani": ("Harm", None),
        "in jux": ("Magic Trap", None), "an jux": ("Magic Untrap", None),
        "uus sanct": ("Protection", None), "uus mani": ("Strength", None),
        "rel sanct": ("Bless", None), "vas flam": ("Fireball", None),
        "an por": ("Magic Lock", None), "in nox": ("Poison", None),
        "ort por ylem": ("Telekinesis", None), "rel por": ("Teleport", None),
        "ex por": ("Unlock", None), "in sanct ylem": ("Wall of Stone", None),
        "vas an nox": ("Arch Cure", "cure+"), "vas uus sanct": ("Arch Protection", None),
        "des sanct": ("Curse", None), "in flam grav": ("Fire Field", None),
        "in vas mani": ("Greater Heal", "heal"), "por ort grav": ("Lightning", None),
        "ort rel": ("Mana Drain", None), "kal ort por": ("Recall", None),
        "in jux hur ylem": ("Blade Spirits", None), "an grav": ("Dispel Field", None),
        "kal in ex": ("Incognito", None), "in jux sanct": ("Magic Reflection", None),
        "por corp wis": ("Mind Blast", None), "an ex por": ("Paralyze", None),
        "in nox grav": ("Poison Field", None), "kal xen": ("Summon Creature", None),
        "an ort": ("Dispel", None), "corp por": ("Energy Bolt", None),
        "vas ort flam": ("Explosion", None), "an lor xen": ("Invisibility", None),
        "kal por ylem": ("Mark", None), "vas des sanct": ("Mass Curse", None),
        "in ex grav": ("Paralyze Field", None), "wis quas": ("Reveal", None),
        "vas ort grav": ("Chain Lightning", None), "in sanct grav": ("Energy Field", None),
        "kal vas flam": ("Flamestrike", None), "vas rel por": ("Gate Travel", None),
        "ort sanct": ("Mana Vampire", None), "vas an ort": ("Mass Dispel", None),
        "flam kal des ylem": ("Meteor Swarm", None), "vas ylem rel": ("Polymorph", None),
        "in vas por": ("Earthquake", None), "vas corp por": ("Energy Vortex", None),
        "an corp": ("Resurrection", None), "kal vas xen hur": ("Air Elemental", None),
        "kal vas xen corp": ("Summon Daemon", None), "kal vas xen ylem": ("Earth Elemental", None),
        "kal vas xen flam": ("Fire Elemental", None), "kal vas xen an flam": ("Water Elemental", None),
        # Chivalry
        "expor flamus": ("Cleanse by Fire", "cure"), "obsu vulni": ("Close Wounds", "heal"),
        "consecrus arma": ("Consecrate Weapon", None), "dispiro malas": ("Dispel Evil", None),
        "divinum furis": ("Divine Fury", None), "forul solum": ("Enemy of One", None),
        "augus luminos": ("Holy Light", None), "dium prostra": ("Noble Sacrifice", None),
        "extermo vomica": ("Remove Curse", None), "sanctum viatas": ("Sacred Journey", None),
        # Necromancy
        "uus corp": ("Animate Dead", None), "in jux mani xen": ("Blood Oath", None),
        "in agle corp ylem": ("Corpse Skin", None), "an sanct gra char": ("Curse Weapon", None),
        "pas tym an sanct": ("Evil Omen", None), "rel xen vas bal": ("Horrific Beast", None),
        "rel xen corp ort": ("Lich Form", None), "wis an ben": ("Mind Rot", None),
        "in sar": ("Pain Spike", None), "in vas nox": ("Poison Strike", None),
        "in bal nox": ("Strangle", None), "kal xen bal": ("Summon Familiar", None),
        "rel xen an sanct": ("Vampiric Embrace", None), "kal xen bal beh": ("Vengeful Spirit", None),
        "kal vas an flam": ("Wither", None), "rel xen um": ("Wraith Form", None),
        "ort corp grav": ("Exorcism", None),
    }
    #  Reagents: abbreviation -> (name, item graphic).
    REAGENTS = {"BP": ("Black Pearl", 0x0F7A), "BM": ("Blood Moss", 0x0F7B),
                "GA": ("Garlic", 0x0F84), "GI": ("Ginseng", 0x0F85),
                "MR": ("Mandrake Root", 0x0F86), "NS": ("Nightshade", 0x0F88),
                "SS": ("Spiders' Silk", 0x0F8D), "SA": ("Sulfurous Ash", 0x0F8C)}
    #  Magery: each circle's eight spells with their reagents (classic, the same
    #  as Grimoire's spellbook). Edit here if the shard differs.
    MAGERY = (
        ("Clumsy", "BM NS"), ("Create Food", "GA GI MR"), ("Feeblemind", "GI NS"),
        ("Heal", "GA GI SS"), ("Magic Arrow", "SA"), ("Night Sight", "SS SA"),
        ("Reactive Armor", "GA SS SA"), ("Weaken", "GA NS"),
        ("Agility", "BM MR"), ("Cunning", "MR NS"), ("Cure", "GA GI"), ("Harm", "NS SS"),
        ("Magic Trap", "GA SS SA"), ("Magic Untrap", "BM SA"), ("Protection", "GA GI SA"),
        ("Strength", "MR NS"),
        ("Bless", "GA MR"), ("Fireball", "BP"), ("Magic Lock", "BM GA SA"), ("Poison", "NS"),
        ("Telekinesis", "BM MR"), ("Teleport", "BM MR"), ("Unlock", "BM SA"),
        ("Wall of Stone", "BM GA"),
        ("Arch Cure", "GA GI MR"), ("Arch Protection", "GA GI MR SA"), ("Curse", "GA NS SA"),
        ("Fire Field", "BP SS SA"), ("Greater Heal", "GA GI MR SS"), ("Lightning", "MR SA"),
        ("Mana Drain", "BP MR SS"), ("Recall", "BP BM MR"),
        ("Blade Spirits", "BP MR NS"), ("Dispel Field", "BP GA SS SA"),
        ("Incognito", "BM GA NS"), ("Magic Reflection", "GA MR SS"),
        ("Mind Blast", "BP MR NS SA"), ("Paralyze", "GA MR SS"), ("Poison Field", "BP NS SS"),
        ("Summon Creature", "BM MR SS"),
        ("Dispel", "GA MR SA"), ("Energy Bolt", "BP NS"), ("Explosion", "BM MR"),
        ("Invisibility", "BM NS"), ("Mark", "BP BM MR"), ("Mass Curse", "GA MR NS SA"),
        ("Paralyze Field", "BP GI SS"), ("Reveal", "BM SA"),
        ("Chain Lightning", "BP BM MR SA"), ("Energy Field", "BP MR SS SA"),
        ("Flamestrike", "SS SA"), ("Gate Travel", "BP MR SA"), ("Mana Vampire", "BP BM MR SS"),
        ("Mass Dispel", "BP GA MR SA"), ("Meteor Swarm", "BM MR SS SA"),
        ("Polymorph", "BM MR SS"),
        ("Earthquake", "BM GI MR SA"), ("Energy Vortex", "BP BM MR NS"),
        ("Resurrection", "BM GA GI"), ("Air Elemental", "BM MR SS"),
        ("Summon Daemon", "BM MR SS SA"), ("Earth Elemental", "BM MR SS"),
        ("Fire Elemental", "BM MR SS SA"), ("Water Elemental", "BM MR SS"))
    #  Per circle (first to eighth). UNCHECKED IN GAME: classic (pre-AoS) values.
    SPELL_MANA = (4, 6, 9, 11, 14, 20, 40, 50)
    #  seconds of casting before the target cursor: RunUO's pre-AoS MagerySpell
    #  (0.5 + 0.25 per circle above the first); spell_info adds the shard's
    #  CAST_EXTRA (2.6.81). UNCHECKED IN GAME: Recall, Gate and the 8th-circle
    #  summons are slower still
    CAST_DELAY = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25)
    CAST_EXTRA = 0.5          # In Mani Ylem: every Magery cast time is +0.5 s over RunUO
    #  spells of other schools: name -> seconds of casting (UNCHECKED IN GAME:
    #  RunUO's Chivalry and Necromancy values; edit here if the shard differs)
    CAST_DELAY_OTHER = {"Cleanse by Fire": 1.0, "Close Wounds": 1.5, "Consecrate Weapon": 0.5,
                        "Dispel Evil": 0.25, "Divine Fury": 1.0, "Enemy of One": 0.5,
                        "Holy Light": 1.75, "Noble Sacrifice": 1.5, "Remove Curse": 1.5,
                        "Sacred Journey": 1.5,
                        "Animate Dead": 1.75, "Blood Oath": 1.5, "Corpse Skin": 1.5,
                        "Curse Weapon": 1.0, "Evil Omen": 1.0, "Horrific Beast": 2.0,
                        "Lich Form": 2.0, "Mind Rot": 1.5, "Pain Spike": 1.25,
                        "Poison Strike": 2.0, "Strangle": 2.0, "Summon Familiar": 2.0,
                        "Vampiric Embrace": 2.0, "Vengeful Spirit": 2.0, "Wither": 1.5,
                        "Wraith Form": 2.0, "Exorcism": 2.0}
    _spells = {}              # spell name (lower case) -> spell_info's answer (made once)

    @staticmethod
    def spell_info(name):
        """(circle 1-8, (reagent abbreviations), mana, cast seconds) of a Magery
        spell, (0, (), 0, seconds) of a known spell of another school, or None."""
        if not Kit._spells:
            for n, secs in Kit.CAST_DELAY_OTHER.items():
                Kit._spells[n.lower()] = (0, (), 0, secs)
            for i, (n, regs) in enumerate(Kit.MAGERY):
                c = i // 8 + 1
                Kit._spells[n.lower()] = (c, tuple(regs.split()), Kit.SPELL_MANA[c - 1],
                                          Kit.CAST_DELAY[c - 1] + Kit.CAST_EXTRA)
        return Kit._spells.get(str(name or "").strip().lower())

    @staticmethod
    def spell_of_words(text):
        """(spell, kind) for words of power (as the journal shows them), or None."""
        return Kit.SPELL_WORDS.get(str(text or "").strip().lower())

    # ---------- small shared helpers (2.6.5): one copy instead of one per module ----------
    COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")
    FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")

    @staticmethod
    def compass(dx, dy):
        """The compass point of (dx, dy) in game tiles ("" when both are 0)."""
        if not dx and not dy:
            return ""
        return Kit.COMPASS[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]

    @staticmethod
    def where_text(dx, dy):
        """'312 tiles NE', '1 tile S' or 'under you' for (dx, dy) in tiles."""
        d = max(abs(int(dx)), abs(int(dy)))
        if d == 0:
            return "under you"
        return "%d tile%s %s" % (d, "" if d == 1 else "s", Kit.compass(dx, dy))

    @staticmethod
    def facet_name(m):
        try:
            m = int(m)
        except Exception:
            return "?"
        return Kit.FACETS[m] if 0 <= m < len(Kit.FACETS) else "facet %d" % m

    @staticmethod
    def ago(secs):
        """'45s', '6m', '2h 14m' for a number of seconds (never negative)."""
        secs = max(0, int(secs))
        if secs < 60:
            return "%ds" % secs
        if secs < 3600:
            return "%dm" % (secs // 60)
        return "%dh %dm" % (secs // 3600, (secs % 3600) // 60)

    @staticmethod
    def read_int(ctrl, default, lo=None, hi=None):
        """The integer in a text box (its Text), clamped to [lo, hi]; `default`
        when it is empty or not a number."""
        try:
            v = int(str(ctrl.Text or "").strip())
        except Exception:
            return default
        if lo is not None and v < lo:
            v = lo
        if hi is not None and v > hi:
            v = hi
        return v

    @staticmethod
    def codec_load(text):
        """A 'k=v;k2=v2' settings string as a dict (keys and values stripped)."""
        out = {}
        for part in str(text or "").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                out[k.strip()] = v.strip()
        return out

    @staticmethod
    def codec_save(d):
        """The 'k=v;k2=v2' string of a dict (sorted; ';' and '=' in values become '/')."""
        return ";".join("%s=%s" % (k, str(d[k]).replace(";", "/").replace("=", "/"))
                        for k in sorted(d))

    # ---------- one tracking arrow (2.6.5) ----------
    #  TazUO shows one tracking arrow per id. Every module that pointed one
    #  (pings, the corpse, dig spots, dry spots, the lookout) used its own id,
    #  so five arrows could show at once. Kit.arrow keeps one arrow for all of
    #  them: each owner asks for a spot, and the arrow points at the spot asked
    #  for last (or, with that owner gone, at the most recent one left).
    ARROW_ID = 0x56415252                    # "VARR"
    _arrow = {"owners": [], "shown": None}   # owners: [(owner, x, y)] in the order asked

    @staticmethod
    def arrow(owner, x, y):
        """Point the shared arrow at (x, y) for `owner` (its key); the latest ask wins."""
        a = Kit._arrow
        a["owners"] = [o for o in a["owners"] if o[0] != owner]
        a["owners"].append((owner, int(x), int(y)))
        Kit._arrow_show()

    @staticmethod
    def arrow_clear(owner):
        """`owner` no longer wants the arrow; it goes to the next most recent ask, or down."""
        a = Kit._arrow
        before = len(a["owners"])
        a["owners"] = [o for o in a["owners"] if o[0] != owner]
        if len(a["owners"]) != before:
            Kit._arrow_show()

    @staticmethod
    def arrow_down():
        """Every owner's ask dropped; the arrow comes down (the script stopping)."""
        Kit._arrow["owners"] = []
        Kit._arrow_show()

    @staticmethod
    def arrow_owner():
        """Who the arrow points for now (the owner key), or None."""
        a = Kit._arrow["owners"]
        return a[-1][0] if a else None

    @staticmethod
    def _arrow_show():
        a = Kit._arrow
        want = (a["owners"][-1][1], a["owners"][-1][2]) if a["owners"] else None
        if want == a["shown"]:
            return
        a["shown"] = want
        try:
            if want is None:
                API.TrackingArrow(-1, -1, Kit.ARROW_ID)
            else:
                API.TrackingArrow(want[0], want[1], Kit.ARROW_ID)
        except Exception:
            a["shown"] = None


class Fill(object):
    """(2.6.56) A window made exactly the size of its slot in a zone.

    The layout gives every window in a zone a slot (Layout.keep: the zone's
    whole width, or height, and a share of the other side) and the window is
    made exactly that size, never bigger and never smaller, so a zone is
    filled edge to edge and nothing leaves it. A module that can lay its own
    window out at any size says so in its hooks ("fit" plus "exact": True,
    the tracker's groups, Grimoire, the skills window) and is told the slot;
    every other window is fitted here, after its module drew it at its own
    size, without changing a line of how it draws:

      - the stone frame, the sections and the bars stretch (their edges go
        through a map of each axis that gives the extra room to the sections
        and keeps the margins, the gaps between sections and the title row
        as they are; only sections taller than ROW_H grow in height);
      - text, buttons, art and every other control keep their own size and
        are anchored: inside a section, a control in its left third keeps
        its distance from the section's left edge, one in its right third
        from the right edge, and one in the middle keeps its place in
        proportion; up and down it keeps its place in proportion;
      - nothing is ever placed outside the window.

    (2.6.78) Fill never squeezes. A slot smaller than the window's own size
    on either axis draws the WHOLE window smaller, with the client's own
    control scaling (labels, buttons, checkboxes and tiled art draw at a
    control's InternalScale; pictures at their size), by
    k = min(1, (slot w - band) / own w, max(FILL_MIN_K, slot h / own h)),
    band the scroll bar's when it still scrolls at k: every entry's rect is
    multiplied by k, then the room left on the other axis goes to the
    sections as above. A window still taller than its slot at k scrolls at
    k (Kit.place); one that holds a scroll area of its own never does
    (TazUO doesn't clip a scroll area inside another): its k goes as low as
    it must. A text field keeps its height (its font is fixed when made)
    and only its width scales; its background tile goes with it. A module that moves or
    resizes a control after drawing it does it through Kit.ui_pos /
    ui_rect / ui_w / ui_h / ui_size (Kit.ui_x / ui_y read a control's own
    place back), which pass the change through the same maps; a control
    added later is fitted on the next pass. Hooks "fill": "grid" places
    every control in proportion (a grid of cells, the Action Bar), "frame"
    stretches the frame and sections and centres the rest (pixel art).
    Freed, the window gets back exactly what its module drew. Client thread
    only (the keeper's pass, or Kit.place / Kit.ui_* from a module's tick)."""
    ROW_H = 72              # a section this tall or less is a row: it never grows in height
    MIN_EDGE = 20           # a stretching control this tall or more grows in height; thinner
    #                         (a bar), it keeps its height
    MIN_BG = 40             # a section narrower than this anchors nothing
    FILL_MIN_K = 0.6        # (2.6.78) the least a window is scaled before its body scrolls
    FIELD_T = "TTFTextInputField"   # (2.6.78) the client's text field (Kit.add_textbox)
    recs = {}               # window -> its record (see fit)
    by_raw = {}             # client control -> (record, entry)
    w2r = {}                # script control -> client control (cached)
    _api_t = [None]         # the client's ApiUiBaseControl type (found once)
    broken = False          # a control couldn't be set: no window is fitted from then on

    # ---------- the maps ----------
    @staticmethod
    def _axis(n, N, M, ivals, mode):
        """A monotone map of one axis, [0, n] -> [0, N], as a list of points
        (pairs) to interpolate between: the extra room (or the room short)
        goes to the sections, in proportion to their size; the margins and
        the gaps between sections keep theirs (mode "grid": everything inside
        the margins shares it)."""
        n, N = float(max(1, n)), float(max(1, N))
        E = N - n
        if abs(E) < 0.5:
            return None
        lo, hi = float(M), n - M
        if hi - lo < 8:
            lo, hi = 0.0, n
        merged = []
        for a, b in sorted(ivals):
            a, b = max(lo, float(a)), min(hi, float(b))
            if b - a < 1:
                continue
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        if not merged or mode == "grid":
            merged = [[lo, hi]]
        L = sum(b - a for a, b in merged)
        if E < 0:
            return None                          # (2.6.78) never squeezed: the window is scaled
        pts = [(0.0, 0.0)]
        shift = 0.0
        for a, b in merged:
            pts.append((a, a + shift))
            shift += E * (b - a) / L
            pts.append((b, b + shift))
        pts.append((n, n + shift))
        return pts

    @staticmethod
    def _ev(m, v):
        if m is None:
            return float(v)
        if v <= m[0][0]:
            return float(v)
        for i in range(1, len(m)):
            a0, b0 = m[i - 1]
            a1, b1 = m[i]
            if v <= a1:
                if a1 - a0 < 1e-9:
                    return b1
                return b0 + (v - a0) * (b1 - b0) / (a1 - a0)
        a, b = m[-1]
        return b + (v - a)

    @staticmethod
    def _xform(rec, e):
        """The fitted rect of entry e (see _scan): (2.6.78) its rect at the
        window's scale k first, then the growth maps and the anchors."""
        kind, x, y, w, h, bg = e[:6]
        role = e[8] if len(e) > 8 else None
        if role == "back":                       # a text field's tile: round its field
            pe = rec["ent"].get(e[9])
            if pe is not None:
                fr = Fill._xform(rec, pe)
                return fr[0] - 2, fr[1] - 1, fr[2] + 4, fr[3] + (h - pe[4])
        k = rec.get("k", 1.0)
        h0 = h
        if k != 1.0:
            x, y, w = x * k, y * k, w * k
            if role == "field":                  # its height stays (its font is fixed),
                slack = e[10] if len(e) > 10 else None   # as far as its neighbours allow
                fh = h if slack is None else max(h * k, min(h, (h + 2 * slack) * k))
                y = y + h * k / 2.0 - fh / 2.0
                h = fh
            else:
                h = h * k
            if bg is not None:
                bg = (bg[0] * k, bg[1] * k, bg[2] * k, bg[3] * k)
            w = max(1, int(round(w)))
            h = max(1, int(round(h)))
        fx, fy = rec["fx"], rec["fy"]
        N, Hn = rec["size"]
        ev = Fill._ev
        if kind == "s":
            x0, x1 = ev(fx, x), ev(fx, x + w)    # a bar's fill grows from its left edge
            if h0 >= Fill.MIN_EDGE and (h0 > Fill.ROW_H or rec["rows"]):
                y0, y1 = ev(fy, y), ev(fy, y + h)
            else:
                c = ev(fy, y + h / 2.0)
                y0, y1 = c - h / 2.0, c + h / 2.0
            x0 = max(0, min(N - 1, int(round(x0))))          # never outside the window
            y0 = max(0, min(Hn - 1, int(round(y0))))
            x1, y1 = min(N, int(round(x1))), min(Hn, int(round(y1)))
            return x0, y0, max(1, x1 - x0), max(1, y1 - y0)
        mode = rec["mode"]
        if bg is not None:
            bx, by, bw, bh = bg
            if mode == "frame":                  # the section's art moves as one, centred
                cbx, cby = bx + bw / 2.0, by + bh / 2.0
                nx = x + ev(fx, cbx) - cbx
                ny = y + ev(fy, cby) - cby
            else:
                if mode == "anchor":
                    third = bw / 3.0
                    cx = x + w / 2.0
                    if cx < bx + third:
                        nx = ev(fx, bx) + (x - bx)
                    elif cx > bx + bw - third:
                        nx = ev(fx, bx + bw) - (bx + bw - x)
                    else:
                        nx = ev(fx, cx) - w / 2.0
                else:
                    nx = ev(fx, x + w / 2.0) - w / 2.0
                ny = ev(fy, y + h / 2.0) - h / 2.0
        elif mode == "frame" and not e[7]:       # outside every section: centred in the window
            nx = x + (N - rec["nat"][0] * k) / 2.0
            ny = y + (Hn - rec["nat"][1] * k) / 2.0
        else:
            nx = ev(fx, x + w / 2.0) - w / 2.0
            ny = ev(fy, y + h / 2.0) - h / 2.0
        nx = max(0, min(int(round(nx)), N - w)) if w < N else 0
        ny = max(0, min(int(round(ny)), Hn - h)) if h < Hn else 0
        return nx, ny, w, h

    # ---------- the client side ----------
    @staticmethod
    def raw_of(c):
        r = Fill.w2r.get(c)
        if r is None:
            r = Kit.client_control(c)
            if r is None:
                return None
            if len(Fill.w2r) > 4000:
                Fill.w2r.clear()
            Fill.w2r[c] = r
        return r

    @staticmethod
    def _set(raw, r, pos_only=False):
        """Set a client control's place (and size) through the script's own
        wrapper type (the client's X / Width are ref properties)."""
        t = Fill._api_t[0]
        if t is None:
            return False
        try:
            # (2.6.82) one wrapper per control, kept (a re-fit of a big window made
            # one per control per fit, by reflection); the constructor bound once
            wraps = Fill._wraps
            w = wraps.get(raw)
            if w is None:
                mk = Fill._mk
                if mk is None:
                    import System
                    mk = Fill._mk = System.Activator.CreateInstance
                w = mk(t, raw)
                if len(wraps) >= 6000:
                    wraps.clear()
                wraps[raw] = w
            if pos_only:
                w.SetPos(int(r[0]), int(r[1]))
            else:
                w.SetRect(int(r[0]), int(r[1]), int(r[2]), int(r[3]))
            return True
        except Exception:
            Fill.broken = True                   # this client can't: windows are cut, not fitted
            return False

    _wraps = {}                                  # (2.6.82) client control -> its script wrapper
    _mk = None

    @staticmethod
    def _find_api_type(g):
        if Fill._api_t[0] is not None:
            return True
        try:
            import clr
            t = clr.GetClrType(type(g))
            while t is not None:
                if str(t.Name) == "ApiUiBaseControl":
                    Fill._api_t[0] = t
                    return True
                t = t.BaseType
        except Exception:
            pass
        return False

    # ---------- a window ----------
    @staticmethod
    def _scan(rec, kids, skip, k_now=1.0):
        """Entries for the client controls in `kids` not known yet, read at the
        place their module gave them: [(control, entry)]. An entry is [kind
        ("s" stretches, "p" keeps its size), x, y, w, h, its section's rect
        for the anchors, the rect last set, a piece of the stone frame]."""
        ents = rec["ent"]
        same = Kit._same()
        new = []
        for c in kids:
            try:
                if c.IsDisposed or c in ents:
                    continue
            except Exception:
                continue
            if skip and any(same(c, s) for s in skip):
                continue
            r = Kit._raw_rect(c)
            if r is None:
                continue
            tn = str(c.GetType().Name)
            kind = "s" if tn in Fill.STRETCH else "p"
            if tn == "GumpPic":                  # the client's bar lines stretch like a bar
                try:
                    if int(c.Graphic) in (Kit.LINE_RED, Kit.LINE_BLUE, Kit.LINE_POISON):
                        kind = "s"
                except Exception:
                    pass
            if kind == "s" and tn == "AlphaBlendControl" and r[2] < Fill.MIN_BG:
                try:                             # a small click area: it stays on its control
                    if float(c.Alpha) < 0.05:
                        kind = "p"
                except Exception:
                    pass
            e = [kind, r[0], r[1], r[2], r[3], None, tuple(r), c in rec["frame"], None, None, None]
            ents[c] = e
            Fill.by_raw[c] = (rec, e)
            new.append((c, e))
            if tn == Fill.FIELD_T:
                e[8] = "field"
            if k_now != 1.0:
                Fill._scale_one(rec, c, k_now)
        if new:
            Fill._pair_fields(rec)
        return new

    @staticmethod
    def _pair_fields(rec):
        """(2.6.78) A text field and the background tile Kit.add_textbox drew under
        it (x - 2, y - 1, w + 4, 24) are one control: the tile is never a
        section, and is placed round its field."""
        ents = rec["ent"]
        fields = [(c, e) for c, e in ents.items() if e[8] == "field"]
        if not fields:
            return
        for c, e in ents.items():
            if e[0] != "s" or e[8] is not None or e[7]:
                continue
            for fc, fe in fields:
                if abs(e[1] - (fe[1] - 2)) <= 1 and abs(e[2] - (fe[2] - 1)) <= 1 \
                        and abs(e[3] - (fe[3] + 4)) <= 1 and e[4] <= 26:
                    e[8], e[9] = "back", fc
                    fe[9] = c
                    break
        # the room above and below each field before its neighbours (e[10]): drawn
        # smaller, a field keeps its height only as far as that room goes
        for fc, fe in fields:
            fx, fy, fw, fh = fe[1], fe[2], fe[3], fe[4]
            slack = None
            for c, e in ents.items():
                if c is fc or e[8] == "back" or e[7]:
                    continue
                x, y, w, h = e[1], e[2], e[3], e[4]
                if x >= fx + fw or x + w <= fx:
                    continue
                if x <= fx and y <= fy and x + w >= fx + fw and y + h >= fy + fh:
                    continue                     # its section, or the window's ground
                if y + h <= fy:
                    gap = fy - (y + h)
                elif y >= fy + fh:
                    gap = y - (fy + fh)
                else:
                    continue
                slack = gap if slack is None else min(slack, gap)
            fe[10] = slack

    @staticmethod
    def _desc(c):
        """Every control inside client control c (its children, theirs ...)."""
        out = []
        try:
            stack = list(Kit._children(c))
        except Exception:
            return out
        while stack:
            d = stack.pop()
            out.append(d)
            try:
                stack.extend(Kit._children(d))
            except Exception:
                pass
        return out

    @staticmethod
    def _scale_one(rec, c, k):
        """(2.6.78) Entry c drawn at scale k (its rect is set by _apply): its
        internal scale; tiled art scales its tiles; what is inside it (a list
        area's rows) is scaled from its own rects, kept for unfit."""
        try:
            if abs(k - 1.0) > 0.001 and str(c.GetType().Name) == "GumpPicTiled":
                c.ScaleTiledTexture = True       # (at scale 1 it draws as before)
            c.SetInternalScale(k)
        except Exception:
            pass
        desc = rec["desc"]
        for d in Fill._desc(c):
            try:
                own = desc.get(d)
                if own is None:
                    r = Kit._raw_rect(d)
                    if r is None:
                        continue
                    own = desc[d] = tuple(r)
                if abs(k - 1.0) > 0.001 and str(d.GetType().Name) == "GumpPicTiled":
                    d.ScaleTiledTexture = True
                Fill._set(d, (own[0] * k, own[1] * k, max(1, own[2] * k), max(1, own[3] * k)))
                d.SetInternalScale(k)
            except Exception:
                pass

    STRETCH = ("GumpPicTiled", "AlphaBlendControl", "ScrollArea", "ResizePic",
               "SimpleProgressBar")         # the client types that stretch (backs, bars)

    @staticmethod
    def _bgs(rec):
        """The sections (stretching controls that aren't the whole window or
        its border), as (x, y, w, h)."""
        nw, nh = rec["nat"]
        out = []
        frame = rec["frame"]
        for c, e in rec["ent"].items():
            if e[0] != "s" or c in frame or e[8] == "back":   # the frame's pieces; a field's tile
                continue
            x, y, w, h = e[1], e[2], e[3], e[4]
            if w < Fill.MIN_BG or h < Fill.MIN_EDGE:
                continue
            if w >= nw - 8 and h >= nh - 8:      # the frame's centre, a full-window back
                continue
            if y < 2 or y + h > nh - 2:          # the frame's top and bottom edges
                continue
            out.append((x, y, w, h))
        return out

    @staticmethod
    def _maps(rec):
        nw, nh = rec["nat"]
        N, Hn = rec["size"]
        k = rec.get("k", 1.0)                    # (2.6.78) the maps grow the scaled window
        M = Kit.MARGIN * k
        bgs = Fill._bgs(rec)
        tall = [b for b in bgs if b[3] > Fill.ROW_H]
        rec["rows"] = not tall                   # no tall section: the rows grow in height too
        rec["fx"] = Fill._axis(nw * k, N, M, [(b[0] * k, (b[0] + b[2]) * k) for b in bgs],
                               rec["mode"])
        rec["fy"] = Fill._axis(nh * k, Hn, M, [(b[1] * k, (b[1] + b[3]) * k) for b in (tall or bgs)],
                               rec["mode"])
        rec["bgs"] = bgs
        # each control's section (the smallest that holds its centre), for the anchors
        for e in rec["ent"].values():
            Fill._anchor(e, bgs)

    @staticmethod
    def _anchor(e, bgs):
        if e[0] == "s":
            return
        cx, cy = e[1] + e[3] / 2.0, e[2] + e[4] / 2.0
        best = None
        for x, y, w, h in bgs:
            if x <= cx <= x + w and y <= cy <= y + h and (best is None or w * h < best[2] * best[3]):
                best = (x, y, w, h)
        e[5] = best

    @staticmethod
    def _apply(rec, pairs=None):
        """Set every control (or the (control, entry) pairs given) to its fitted
        rect, where it isn't there already. Disposed controls are let go."""
        for c, e in (list(rec["ent"].items()) if pairs is None else pairs):
            try:
                if c.IsDisposed:
                    rec["ent"].pop(c, None)
                    Fill.by_raw.pop(c, None)
                    Fill._wraps.pop(c, None)     # (2.6.83) its wrapper goes too
                    continue
            except Exception:
                continue
            r = Fill._xform(rec, e)
            if r != e[6]:
                if Fill._set(c, r, e[0] == "p" and rec.get("k", 1.0) == 1.0 and
                             (r[2], r[3]) == (e[3], e[4])):
                    e[6] = r

    @staticmethod
    def fit(g, x, y, W, H, mode="anchor"):
        """Make window g exactly W x H at (x, y) (its slot). True when it was
        changed or placed, False when it was already so, None when it couldn't
        be read (the caller places it as it is)."""
        if Fill.broken or not Fill._find_api_type(g) or not Kit.flush():
            return None
        raw = Kit._raw_gump(g)
        if raw is None:
            return None
        rec = Fill.recs.get(g)
        info = Kit.scroll_info(g)
        if rec is None:
            r = Snap.rect(g)
            if r is None:
                return None
            nat = (info["w"], info["h"]) if info is not None else (r[2], r[3])
            rec = {"g": g, "raw": raw, "nat": nat, "size": None, "slot": None, "mode": mode,
                   "ent": {}, "fx": None, "fy": None, "rows": False, "n": -1, "an": -1,
                   "placed": None, "scroll": False, "bgs": [], "frame": set(),
                   "k": 1.0, "desc": {}, "nested": False,
                   "head0": (info["head"] if info is not None else None) or
                   (Kit.MARGIN + 30 + Kit.GAP)}       # its fixed top part at 100%
            fr = Kit._frames.get(g)              # the frame add_window_frame drew (noted)
            for piece in (fr["pieces"] if fr else ()):
                pr = Kit.client_control(piece)
                if pr is not None:
                    rec["frame"].add(pr)
            Fill.recs[g] = rec
        elif rec["placed"] is not None and info is None:
            r = Snap.rect(g)                     # the module placed it at a new size of its own
            if r is not None and (r[2], r[3]) != rec["placed"][2:]:
                rec["nat"] = (r[2], r[3])
                rec["size"] = None
        rec["mode"] = mode
        skip, area = Kit._scroll_skip(g)
        # (2.6.82) the Children counts first (one read each): the child-by-child
        # live count runs only when one changed, and every Kit.SWEEP_FULL s
        try:
            cnt = (int(raw.Children.Count),
                   int(area.Children.Count) if area is not None else 0)
        except Exception:
            cnt = None
        now = time.time()
        if cnt is not None and cnt == rec.get("cnt") and 0 <= rec.get("full_at", 0.0) - now:
            n, an = rec["n"], rec.get("an")
        else:
            rec["cnt"] = cnt
            rec["full_at"] = now + Kit.SWEEP_FULL
            n = Kit._live_count(raw)
            an = Kit._live_count(area) if area is not None else 0
        new = []
        if n != rec["n"] or an != rec.get("an"):
            kids = Kit._children(raw)
            if area is not None:
                kids = kids + Kit._children(area)
            new = Fill._scan(rec, kids, skip + ([area] if area is not None else []), rec["k"])
            rec["n"], rec["an"] = Kit._live_count(raw), an
            for c, e in new:                     # (2.6.78) a scroll area of its own
                try:
                    if str(c.GetType().Name) == "ScrollArea":
                        rec["nested"] = True
                except Exception:
                    pass
        nw, nh = rec["nat"]
        band = Kit.SCROLL_BAND
        conv = g in Kit._scrolled                # converted once: it keeps its band
        if conv:
            Wb = W - band
            k = 1.0 if (Wb >= nw and H >= nh) else min(1.0, Wb / float(nw),
                                                       max(Fill.FILL_MIN_K, H / float(nh)))
            scroll = nh * k > H + 1
        else:
            k, scroll = Fill.scale_for(nw, nh, W, H, rec["nested"])
        if scroll or conv:
            size = (W - band, int(round(nh * k)) if scroll else H)
        else:
            size = (W, H)
        if abs(k - rec["k"]) > 0.0005:           # (2.6.78) the whole window at its new scale
            rec["k"] = k
            for c in list(rec["ent"]):
                Fill._scale_one(rec, c, k)
            rec["size"] = None
        if size != rec["size"] or mode != rec.get("mode_was"):
            rec["size"], rec["mode_was"], rec["scroll"] = size, mode, scroll
            Fill._maps(rec)
            Fill._apply(rec)
        elif new:
            for c, e in new:
                Fill._anchor(e, rec["bgs"])
            Fill._apply(rec, new)
        r = Snap.rect(g)
        if r is not None and (r[0], r[1], r[2], r[3]) == (x, y, W, H) and not new \
                and rec["placed"] is not None:
            return False                         # as it was: nothing to do
        if scroll or conv:
            head = int(round(rec["head0"] * k))  # the title row, at the window's scale
            Kit._place_raw(g, x, y, size[0], size[1], head, H)
        else:
            Kit._place_raw(g, x, y, W, H, None, None)
        r = Snap.rect(g)
        rec["placed"] = (x, y, r[2], r[3]) if r is not None else (x, y, W, H)
        rec["slot"] = (x, y, W, H)
        return True

    @staticmethod
    def scale_for(nw, nh, W, H, nested=False):
        """(2.6.78) (k, scrolls): the scale window nw x nh is drawn at in a W x H
        slot (1: it fits, or grows) and whether its body then scrolls."""
        nw, nh = float(max(1, nw)), float(max(1, nh))
        if W >= nw and H >= nh:
            return 1.0, False
        if nested:                               # never scrolled: as small as it must be
            return min(1.0, W / nw, H / nh), False
        k = min(1.0, W / nw, max(Fill.FILL_MIN_K, H / nh))
        if nh * k > H + 1:                       # still too tall: it scrolls, beside its bar
            k = min(1.0, (W - Kit.SCROLL_BAND) / nw, max(Fill.FILL_MIN_K, H / nh))
            return k, nh * k > H + 1
        return k, False

    @staticmethod
    def drawn_at(g):
        """(2.6.78) The scale window g is fitted at (1.0: its own size or more)."""
        rec = Fill.recs.get(g)
        return rec.get("k", 1.0) if rec is not None else 1.0

    @staticmethod
    def unfit(g):
        """Window g is no longer fitted: every control back where its module
        put it, the window at its own size. True if it had been fitted.
        (2.6.78) Back at scale 1 too: each control's internal scale, and what
        is inside it put back at its own rect (never scaled back: that drifts)."""
        rec = Fill.recs.pop(g, None)
        if rec is None:
            return False
        for d, own in list(rec.get("desc", {}).items()):
            try:
                if not d.IsDisposed:
                    Fill._set(d, own)
                    d.SetInternalScale(1.0)
            except Exception:
                pass
        for c, e in list(rec["ent"].items()):
            Fill.by_raw.pop(c, None)
            try:
                if not c.IsDisposed:
                    if rec.get("k", 1.0) != 1.0:
                        c.SetInternalScale(1.0)
                    Fill._set(c, (e[1], e[2], e[3], e[4]), e[0] == "p" and rec.get("k", 1.0) == 1.0)
            except Exception:
                pass
            Fill._wraps.pop(c, None)             # (2.6.83) a fit again makes a new one
        if Kit.is_open(g):
            try:
                nw, nh = rec["nat"]
                Kit._place_raw(g, int(g.GetX()), int(g.GetY()), nw, nh, None, None)
                Kit.moved_by_code(g)
            except Exception:
                pass
        return True

    @staticmethod
    def beside(rf, r, nr):
        """(2.6.57) Where a window attached at rf beside window rect r goes when
        that window is now nr: past its right (bottom) edge it keeps its distance
        from the new right (bottom) edge, before its left (top) edge its distance
        from the new left (top) edge, else it moves with the window's corner."""
        def one(f0, f1, a0, a1, b0, b1):
            if f0 >= a1:
                return b1 + (f0 - a1)
            if f1 <= a0:
                return b0 - (a0 - f0)
            return f0 + (b0 - a0)
        return (one(rf[0], rf[0] + rf[2], r[0], r[0] + r[2], nr[0], nr[0] + nr[2]),
                one(rf[1], rf[1] + rf[3], r[1], r[1] + r[3], nr[1], nr[1] + nr[3]))

    @staticmethod
    def fitted(g):
        return g in Fill.recs

    @staticmethod
    def prune():
        """Windows gone: their records go (every keeper pass)."""
        if not Fill.recs:
            return
        for g in [g for g in Fill.recs if not Kit.is_open(g)]:
            rec = Fill.recs.pop(g)
            for c in rec["ent"]:
                Fill.by_raw.pop(c, None)
                Fill._wraps.pop(c, None)         # (2.6.82) its wrappers go with it
        if len(Fill.by_raw) > 20000:             # never: every entry belongs to a record
            Fill.by_raw.clear()
            for rec in Fill.recs.values():
                for c, e in rec["ent"].items():
                    Fill.by_raw[c] = (rec, e)

    # ---------- a module moving its own controls (Kit.ui_*) ----------
    @staticmethod
    def entry(c):
        """(record, entry) of a script control in a fitted window, or None."""
        if not Fill.recs:
            return None
        raw = Fill.raw_of(c)
        if raw is None:
            return None
        return Fill.by_raw.get(raw)

    @staticmethod
    def change(c, x=None, y=None, w=None, h=None):
        """A module sets (part of) its control's own rect: noted, and set
        through the window's maps. False when the control isn't in a fitted
        window (the caller sets it as it is)."""
        hit = Fill.entry(c)
        if hit is None:
            return False
        rec, e = hit
        if x is not None:
            e[1] = int(x)
        if y is not None:
            e[2] = int(y)
        if w is not None:
            e[3] = int(w)
        if h is not None:
            e[4] = int(h)
        if rec["size"] is None:
            return False
        if e[0] == "p" and (x is not None or y is not None):
            Fill._anchor(e, rec["bgs"])          # it may sit in another section now
        r = Fill._xform(rec, e)
        try:
            if e[0] == "p" and w is None and h is None:
                c.SetPos(r[0], r[1])
            else:                                # (2.6.71) a new size is applied too
                c.SetRect(r[0], r[1], r[2], r[3])
            e[6] = r
        except Exception:
            return False
        return True

    @staticmethod
    def own(c):
        """(x, y, w, h) a module gave its control (before fitting), or None
        when the control isn't in a fitted window."""
        hit = Fill.entry(c)
        if hit is None:
            return None
        e = hit[1]
        return e[1], e[2], e[3], e[4]


class Overlaps(object):
    """(2.6.78) Check look's control test for one window (directions 17.3): any
    two leaf controls (labels with text, buttons, checkboxes, text fields,
    sliders, drop-downs, item and gump pictures) whose drawn rects overlap by
    more than 1 px; a leaf outside its section or the window; a leaf on the
    stone (in no section); a leaf cut by its scroll area's edge. A text field
    and its tile are one control; hidden controls, the pictures of a scene a
    module noted (Kit.note_scene), and what a nested scroll area holds past
    its OUTER area (TazUO clips nested areas by the outer one) are left out.
    Sections: tiled art and colour boxes at least MIN_BG x MIN_EDGE, not a
    click area, not the frame, not the whole window, straight in the window
    (or its scroll conversion). Client thread."""
    LEAF = ("Label", "Button", "Checkbox", "TTFTextInputField", "GumpPic", "ResizableStaticPic",
            "HSliderBar", "Combobox", "StbTextBox", "ItemGump")
    SECT = ("GumpPicTiled", "AlphaBlendControl")
    LINES = (0x0805, 0x0806, 0x0808)
    CAP = 1500                           # controls looked at, at most, per window

    @staticmethod
    def _inter(a, b):
        x0, y0 = max(a[0], b[0]), max(a[1], b[1])
        x1, y1 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
        if x1 <= x0 or y1 <= y0:
            return None
        return x0, y0, x1 - x0, y1 - y0

    @staticmethod
    def _inside(a, b, slack=1):
        return (a[0] >= b[0] - slack and a[1] >= b[1] - slack and
                a[0] + a[2] <= b[0] + b[2] + slack and a[1] + a[3] <= b[1] + b[3] + slack)

    @staticmethod
    def _text(c, tn):
        try:
            if tn == "Label":
                return str(c.Text or "")
            if tn == "TTFTextInputField":
                return "a text field"
        except Exception:
            pass
        try:
            t = c.Tooltip
            if t is not None and str(t):
                return str(t)[:32]
        except Exception:
            pass
        return tn

    @staticmethod
    def collect(g):
        """[(control, type name, drawn rect, clip, visible, parent, frame?)]."""
        raw = Kit._raw_gump(g)
        if raw is None:
            return [], None, None
        info = Kit._scrolled.get(g)
        conv = info["area_raw"] if info else None
        frame = set()
        for w in (Kit._frame_parts.get(g) or []):
            c = Kit.client_control(w)
            if c is not None:
                frame.add(c)
        fr = Kit._frames.get(g)
        for w in (fr["pieces"] if fr else []) + (Kit._back_parts.get(g) or []) + \
                (Kit._scene_parts.get(g) or []):
            c = Kit.client_control(w)
            if c is not None:
                frame.add(c)
        if info:
            for w in info["frame"] + info["band"]:
                c = Kit.client_control(w)
                if c is not None:
                    frame.add(c)
        conv_h = info["h"] if info else 0
        out = []

        def walk(c, ox, oy, clip, vis, parent, depth):
            for i, k in enumerate(Kit._children(c)):
                if len(out) >= Overlaps.CAP:
                    return
                try:
                    if k.IsDisposed:
                        continue
                    tn = str(k.GetType().Name)
                    r = Kit._raw_rect(k)
                    if r is None:
                        continue
                    v = vis and bool(k.IsVisible)
                except Exception:
                    continue
                ax, ay = ox + r[0], oy + r[1]
                rr = (ax, ay, r[2], r[3])
                is_bar = tn == "ScrollBar" or (tn != "ScrollArea" and i == 0 and
                                               str(c.GetType().Name) == "ScrollArea")
                out.append((k, tn, rr, clip, v, parent, k in frame or is_bar))
                if tn == "ScrollArea":
                    if k is conv:
                        cl = (ax, ay, r[2] - 14, conv_h)
                    else:
                        cl = (ax, ay, r[2] - 14, r[3])
                    if clip is not None:
                        cl = clip                # (TazUO: the outer area's rect clips it)
                    walk(k, ax, ay, cl, v, k, depth + 1)
                elif depth < 3 and tn not in ("BagCanvas",):
                    walk(k, ax, ay, clip, v, parent, depth + 1)
        walk(raw, 0, 0, None, bool(raw.IsVisible), raw, 0)
        return out, raw, conv

    @staticmethod
    def problems(g, W, H):
        """{"overlap": [(a, b)], "outside": [a], "stone": [a], "cut": [a]} of
        window g (texts of the controls), W x H its content size."""
        ents, raw, conv = Overlaps.collect(g)
        res = {"overlap": [], "outside": [], "stone": [], "cut": []}
        if raw is None:
            return res
        top = (raw, conv) if conv is not None else (raw,)
        scenes = Kit._scenes.get(g, [])
        rec = Fill.recs.get(g)
        secs = []
        backs = set()
        for k, tn, r, clip, v, parent, frame in ents:
            if frame or tn not in Overlaps.SECT or not v:
                continue
            if not any(parent is t for t in top):
                continue
            try:
                if float(k.Alpha) < 0.05:
                    continue
            except Exception:
                pass
            e = rec["ent"].get(k) if rec is not None else None
            if e is not None and len(e) > 8 and e[8] == "back":
                backs.add(k)
                continue
            try:
                ks = min(1.0, float(k.InternalScale or 1.0))   # (a window drawn smaller)
            except Exception:
                ks = 1.0
            if r[2] < Fill.MIN_BG * ks or r[3] < Fill.MIN_EDGE * ks or (r[2] >= W - 8 and r[3] >= H - 8):
                continue
            secs.append(r)
        fields = [r for k, tn, r, c_, v, p_, f_ in ents if tn == "TTFTextInputField" and v]
        leaves = []
        for k, tn, r, clip, v, parent, frame in ents:
            if not v or frame or tn not in Overlaps.LEAF:
                continue
            if tn == "Label":
                try:
                    if not str(k.Text or ""):
                        continue
                except Exception:
                    continue
            if tn == "GumpPic":
                try:
                    if int(k.Graphic) in Overlaps.LINES:
                        continue
                except Exception:
                    pass
            d = r
            if clip is not None:
                d = Overlaps._inter(r, clip)
                if d is None:
                    continue
                if d != r:
                    res["cut"].append(Overlaps._text(k, tn))
            scene = None
            for q in scenes:
                cx, cy = r[0] + r[2] / 2.0, r[1] + r[3] / 2.0
                if q[0] <= cx <= q[0] + q[2] and q[1] <= cy <= q[1] + q[3] and \
                        tn in ("GumpPic", "ResizableStaticPic", "ItemGump"):
                    scene = q
                    break
            leaves.append((k, tn, d, scene, parent))
        for i in range(len(leaves)):
            a = leaves[i]
            for j in range(i + 1, len(leaves)):
                b = leaves[j]
                if a[3] is not None and b[3] is not None:
                    continue                     # two pictures of a scene
                ir = Overlaps._inter(a[2], b[2])
                if ir is not None and ir[2] > 1 and ir[3] > 1:
                    res["overlap"].append((Overlaps._text(a[0], a[1]), Overlaps._text(b[0], b[1])))
        win = (0, 0, W, H)
        for k, tn, d, scene, parent in leaves:
            cx, cy = d[0] + d[2] / 2.0, d[1] + d[3] / 2.0
            best = None
            for q in secs:
                if q[0] <= cx <= q[0] + q[2] and q[1] <= cy <= q[1] + q[3] and \
                        (best is None or q[2] * q[3] < best[2] * best[3]):
                    best = q
            if not Overlaps._inside(d, win):
                res["outside"].append(Overlaps._text(k, tn))
            elif best is None:
                res["stone"].append(Overlaps._text(k, tn))
            elif not Overlaps._inside(d, best):
                res["outside"].append(Overlaps._text(k, tn))
        return res

    @staticmethod
    def lines(res):
        """[problem text] in look_problems' form."""
        out = []
        ov = res["overlap"]
        if len(ov) == 1:
            out.append('1 overlap ("%s" over "%s")' % ov[0])
        elif ov:
            out.append('%d overlaps (first: "%s" over "%s")' % (len(ov), ov[0][0], ov[0][1]))
        for key, one, many in (("outside", "1 control outside its section or the window",
                                "%d controls outside their section or the window"),
                               ("stone", "1 control on the stone between sections",
                                "%d controls on the stone between sections"),
                               ("cut", "1 control cut by its scroll area's edge",
                                "%d controls cut by their scroll area's edge")):
            lst = res[key]
            if lst:
                out.append((one if len(lst) == 1 else many % len(lst)) + ' (first: "%s")' % lst[0])
        return out


class PageCanvas(object):
    """Stands in for the Virtue Assistant window while a module draws its
    settings page: every control the page adds and every section it draws
    (Kit.add_section) is noted, so the window can move each section into its
    columns afterwards. inner None: a measuring pass, nothing is shown."""
    def __init__(self, inner):
        self._inner = inner
        self.ctrls = []
        self.sections = []

    def Add(self, ctrl, *args):
        self.ctrls.append(ctrl)
        if self._inner is not None:
            return self._inner.Add(ctrl, *args)
        return ctrl

    def __getattr__(self, name):
        if self._inner is None:
            raise AttributeError(name)
        return getattr(self._inner, name)


# =============================================================================
#  Alerts - one "tell me loudly" for every module (2.6.05)
#
#    HOST.alert_kind(key, label, default_sound=None)
#        In start(): lists an alert kind on Settings > Alerts, where the player
#        picks its sound or turns it off. The module running is its owner (its
#        title starts the journal line). key: "<module key>.<what>".
#    HOST.alert(key, text, level="warn", sound=None, ping=None, who=None)
#        level "info" / "warn" / "alarm" (an alarm banner flashes until it is
#        clicked); sound: a sound id for this one alert instead of the kind's;
#        ping=(x, y): also a Danger! map ping there through Map Pings, when it
#        runs; who (a serial or a name) keys the rate limit, so two players
#        each get their own alert. True when the alert was raised.
#
#  An alert shows the banner (one small window, top centre at first; drag it
#  anywhere, click it to dismiss), plays its client sound and writes a journal
#  line starting with the module's title. The same alert (key and who, or key
#  and text) is raised at most once every ALERT_RATE seconds; a burst shares the
#  one banner with a count, and its sounds play in turn, never on top of each
#  other. Safe from a client tick and from a thread_tick: the banner itself is
#  drawn on the next client pass (Alerts.tick, from Host.ui_tick), built once
#  and then only shown, hidden and relabelled.
# =============================================================================
class Alerts(object):
    KEY = "VirtueAssistant_alerts"     # per character: mute, banner, each kind's on / sound
    POS_KEY = "VirtueAssistant_alert_pos"
    W, H = 420, 46
    LEVELS = {"info": Kit.HUE_INFO, "warn": Kit.HUE_TITLE, "alarm": Kit.HUE_BAD}
    TEST_KEY = "va.test"

    def __init__(self):
        self.kinds = {}        # key -> {"label", "sound", "owner"} (registered this session)
        self.order = []        # the keys in the order they were registered
        self.choice = {}       # key -> [on, sound] picked on the Alerts page (saved)
        self.mute = False      # no alert sounds at all
        self.banner_on = True  # show the banner (off: sound and journal line only)
        self.loaded = False
        self.last = {}         # (key, who or text) -> time last raised (the rate limit)
        self.pending = []      # (line, hue, alarm) to show on the next client pass
        self.sounds = []       # sound ids waiting their turn
        self.sound_at = 0.0
        self.pings = []        # [x, y, give up at]
        self.busy = False      # tick() has something to do
        self.g = None          # the banner (built once, then reused)
        self.c = {}
        self.shown = False
        self.count = 0         # alerts since the banner was last shown (beyond the one on it)
        self.alarm = False
        self.hue = Kit.HUE_TITLE
        self.line = ""
        self.hide_at = 0.0
        self.flash_at = 0.0
        self.flash_on = False
        self.clicked = False
        self.pos = None        # where the banner was last seen (a drag ends in a click)
        self.moved_at = 0.0
        self.tw = self.W - 36  # room for the text beside the count

    # ---------- saved choices ----------
    def load(self):
        self.loaded = True
        self.choice = {}
        self.mute, self.banner_on = False, True
        for part in Kit.get_var(self.KEY).split(";"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            k, v = k.strip(), v.strip()
            if k == "mute":
                self.mute = v == "1"
            elif k == "banner":
                self.banner_on = v != "0"
            elif k.startswith("kind."):
                bits = v.split(",")
                try:
                    snd = int(bits[1]) if len(bits) > 1 and bits[1] != "" else None
                except ValueError:
                    snd = None
                self.choice[k[5:]] = [bits[0] != "0", snd]

    def save(self):
        parts = ["mute=%d" % (1 if self.mute else 0), "banner=%d" % (1 if self.banner_on else 0)]
        for k in sorted(self.choice):
            on, snd = self.choice[k]
            parts.append("kind.%s=%d,%s" % (k, 1 if on else 0, "" if snd is None else int(snd)))
        Kit.put_var(self.KEY, ";".join(parts))

    def setting(self, key):
        """[on, sound id] for alert kind `key` as the player has it."""
        if not self.loaded:
            self.load()
        k = self.kinds.get(key)
        ch = self.choice.get(key)
        on = ch[0] if ch is not None else True
        snd = ch[1] if ch is not None and ch[1] is not None else (k["sound"] if k else 0)
        return on, int(snd or 0)

    def choose(self, key, on=None, sound=None):
        cur = self.setting(key)
        new = [cur[0] if on is None else bool(on), cur[1] if sound is None else int(sound)]
        if new != list(cur) or key not in self.choice:
            self.choice[key] = new
            self.save()

    # ---------- registering and raising ----------
    def kind(self, key, label, sound=None, owner=None):
        key = str(key)
        k = self.kinds.get(key)
        new = {"label": str(label or key), "sound": int(sound or 0),
               "owner": str(owner or APP_NAME)}
        if k is None:
            self.order.append(key)
        if new != k:
            self.kinds[key] = new
            if key != self.TEST_KEY:
                safe(lambda: HOST.refresh_settings(ALERTS_PAGE))   # the page lists it now
        return key

    def raise_(self, key, text, level="warn", sound=None, ping=None, who=None, owner=None):
        if not self.loaded:
            self.load()
        key = str(key)
        k = self.kinds.get(key)
        if k is None:
            self.kind(key, key, sound, owner)
            k = self.kinds[key]
        on, snd = self.setting(key)
        if not on:
            return False
        now = time.time()
        rk = (key, str(who) if who is not None else str(text))
        t = self.last.get(rk)
        # (here and below: a time ahead of now means the clock was set back; it
        # counts as long past, or the wait would last as long as the clock was ahead)
        if t is not None and 0 <= now - t < ALERT_RATE:
            return False
        if len(self.last) > 200:                 # a cap: forget what the rate limit no longer needs
            cut = now - ALERT_RATE
            for old in [x for x, tt in self.last.items() if tt < cut or tt > now]:
                del self.last[old]
        self.last[rk] = now
        who_t = k["owner"]
        text = str(text)
        line = text if text.startswith(who_t + ":") else "%s: %s" % (who_t, text)
        hue = self.LEVELS.get(level, Kit.HUE_TITLE)
        try:
            API.SysMsg(line, hue)
        except Exception:
            pass
        sid = (int(sound) if sound else snd) if snd else 0   # the player's Silent wins
        if sid and not self.mute and len(self.sounds) < 4:
            if not self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP:
                self._play(sid, now)             # at once when nothing waits (a void call)
            else:
                self.sounds.append(sid)
        if self.banner_on:
            self.pending.append((line, hue, level == "alarm"))
            if len(self.pending) > 50:
                del self.pending[:-50]
        if ping is not None and len(self.pings) < 8:
            try:
                self.pings.append([int(ping[0]), int(ping[1]), now + 10.0])
            except Exception:
                pass
        self.busy = True
        return True

    def _play(self, sid, now):
        self.sound_at = now
        try:
            API.PlaySound(int(sid))
        except Exception:
            pass

    # ---------- every client pass (Host.ui_tick) ----------
    def tick(self, now):
        if not self.busy:
            return
        if self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP:
            self._play(self.sounds.pop(0), now)
        if self.pings:
            x, y, until = self.pings[0]
            fn = HOST.services.get("pings.send")
            done = now > until or fn is None
            if not done:
                try:
                    done = bool(fn(x, y))        # False = not now (paced): try again later
                except Exception:
                    done = True
            if done:
                self.pings.pop(0)
        if self.pending:
            items, self.pending = self.pending, []
            self._show(items, now)
        if self.shown:
            self._watch(now)
        self.busy = bool(self.sounds or self.pings or self.pending or self.shown)

    def _show(self, items, now):
        if not self.banner_on:
            return
        line, hue, alarm = items[-1]
        if self.shown and Kit.is_open(self.g):
            self.count += len(items)
            self.alarm = self.alarm or any(a for _, _, a in items)
        else:
            self.count = len(items) - 1
            self.alarm = any(a for _, _, a in items)
        self.line, self.hue = line, hue
        if not Kit.is_open(self.g):
            self._build()
        if self.g is None:
            return
        self._label()
        if not self.shown:
            safe(lambda: setattr(self.g, "IsVisible", True))
            self.shown = True
            self.clicked = False                     # a click on the last banner isn't for this one
            self.pos = Snap.pos(self.g)
        self.hide_at = now + ALERT_HOLD
        self.flash_at = now + ALERT_FLASH
        self.flash_on = True

    def _label(self):
        c = self.c
        more = ("+%d more" % self.count) if self.count > 0 else ""
        mw = Kit.text_px(more) if more else 0       # letter-sum width: nothing made to measure
        tw = self.W - 36 - ((mw + 8) if more else 0)
        self.tw = tw
        Kit.set_text(c["text"], Kit.fit(self.line, tw), self.hue)
        Kit.set_text(c["more"], more, Kit.HUE_INFO)
        if more:
            safe(lambda: c["more"].SetPos(self.W - 18 - mw, 15))

    def _watch(self, now):
        g = self.g
        if not Kit.is_open(g):
            self.shown, self.g = False, None
            return
        p = Snap.pos(g)
        if p != self.pos:
            if self.pos is not None:
                self.moved_at = now
            self.pos = p
        if self.clicked:
            self.clicked = False
            if not 0 <= now - self.moved_at <= 0.35:     # a drag ends in a click too
                self.dismiss()
                return
        if self.alarm:
            if not 0 < self.flash_at - now <= ALERT_FLASH:
                self.flash_at = now + ALERT_FLASH
                self.flash_on = not self.flash_on
                Kit.set_text(self.c["text"], Kit.fit(self.line, self.tw), Kit.HUE_BAD
                             if self.flash_on else Kit.HUE_TEXT)
        elif not 0 < self.hide_at - now <= ALERT_HOLD:
            self.dismiss()

    def dismiss(self):
        self.shown, self.count, self.alarm = False, 0, False
        g = self.g
        if Kit.is_open(g):
            safe(lambda: setattr(g, "IsVisible", False))

    def _click(self):
        self.clicked = True
        self.busy = True

    def _save_pos(self):
        Kit.save_pos(self.POS_KEY, self.g)

    def _build(self):
        """The banner (client thread). Never takes keyboard focus: no text box."""
        W, H = self.W, self.H
        sw = Kit.screen()[0] or 1024
        x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - W) // 2), 60), (W, H))
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H, corners=False)
        Kit.add_section(g, 8, 8, W - 16, H - 16)
        c = {"text": Kit.add_label(g, "", 18, 15, Kit.HUE_TITLE),
             "more": Kit.add_label(g, "", W - 60, 15, Kit.HUE_INFO)}
        Kit.catcher(g, 0, 0, W, H, self._click, "Click to dismiss; drag to move", movable=True)
        Kit.place(g, x, y, W, H)
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, self._save_pos))
        self.g, self.c = g, c
        self.shown = False

    def close(self):
        g, self.g = self.g, None
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)
        self.shown = False
        self.pending, self.sounds, self.pings = [], [], []
        self.busy = False


# =============================================================================
#  Guard - is the player under the town guards' protection? (2.6.05)
#
#    HOST.guarded()    -> True (in a guarded region), False (outside) or None
#                         (not known yet)
#    HOST.guard_area() -> the name of the GUARD_AREAS entry you stand in, or None
#
#  The shard says it on entering and leaving a guarded region ("You are now
#  under the protection of the town guards." / "You have left the protection
#  of the town guards.", RunUO's GuardedRegion, cliloc 500112-500115); the
#  mother reads those lines from the shared Journal four times a second. Until
#  the first such line the state comes from GUARD_AREAS, when filled in, then
#  from the last state saved for this character, while you stand where it was
#  seen (you log in where you logged out). Otherwise it is None.
# =============================================================================
class Guard(object):
    KEY = "VirtueAssistant_guard"      # per character: "1|0,x,y,facet" - the last state seen
    EVERY = 0.25

    def __init__(self):
        self.state = None
        self.rd = None
        self.next = 0.0
        self.saved = None      # (state, x, y, facet) read once
        self.cache = (0.0, None, None)     # (until, guarded(), guard_area())

    def tick(self, now):
        if now < self.next and self.next - now <= self.EVERY:    # (further: the clock was set back)
            return
        self.next = now + self.EVERY
        if self.rd is None:
            self.rd = Journal.reader()
            self.rd.last = 0                     # the lines already read count too (the last wins)
        for ln in self.rd.new():
            low = ln.low
            if "protection of the town guards" not in low:
                continue
            if ln.name and ln.name.lower() != "system":
                continue                         # a player saying it, not the shard
            new = None
            for t in GUARD_IN_TEXTS:
                if low.startswith(t):
                    new = True
            for t in GUARD_OUT_TEXTS:
                if low.startswith(t):
                    new = False
            if new is not None and new != self.state:
                self.state = new
                self.cache = (0.0, None, None)
                self._save(new)

    @staticmethod
    def _where():
        try:
            p = HOST.me()                        # (2.6.82) the pass's shared player read
            return int(p.X), int(p.Y), int(API.GetMap())
        except Exception:
            return None

    def _save(self, state):
        w = self._where()
        if w is None or not (w[0] or w[1]):      # (0, 0): not in the world
            return
        self.saved = (state, w[0], w[1], w[2])
        Kit.put_var(self.KEY, "%d,%d,%d,%d" % (1 if state else 0, w[0], w[1], w[2]))

    def store(self):
        """When the script stops: the state with the spot you stand on now, the
        one you log in on next time (the line itself comes at a region's edge)."""
        if self.state is not None:
            self._save(self.state)

    def _look(self):
        """(guarded or None, area name or None) from the position: GUARD_AREAS,
        then the saved state of this spot. Cached for a second."""
        now = time.time()
        if now < self.cache[0] <= now + 1.0:     # (further: the clock was set back)
            return self.cache[1], self.cache[2]
        w = self._where()
        state, name = None, None
        if w is not None:
            x, y, m = w
            for a in GUARD_AREAS:
                try:
                    if a[0] == m and a[1] <= x <= a[3] and a[2] <= y <= a[4]:
                        state, name = True, str(a[5])
                        break
                except Exception:
                    continue
            if state is None and self.state is None:
                if self.saved is None:
                    try:
                        b = [int(v) for v in Kit.get_var(self.KEY).split(",")]
                        self.saved = (b[0] == 1, b[1], b[2], b[3])
                    except Exception:
                        self.saved = (None, 0, 0, -1)
                s = self.saved
                if s[0] is not None and s[3] == m and abs(s[1] - x) <= GUARD_SPOT \
                        and abs(s[2] - y) <= GUARD_SPOT:
                    state = s[0]
        self.cache = (now + 1.0, state, name)
        return state, name

    def guarded(self):
        if self.state is not None:
            return self.state
        return self._look()[0]

    def area(self):
        return self._look()[1]


# =============================================================================
#  The Settings tab's own pages (2.6.05): Alerts and Keys. Each is a ModuleSlot
#  with an api like a module's settings page (config_height / build_config /
#  poll_config / config_closed) but no module behind it: listed after the
#  modules' pages, never on the Modules tab, never started or saved as on.
# =============================================================================
class AlertsPage(object):
    def __init__(self):
        self.c = None
        self.store = ({}, {})

    def kinds(self):
        return [k for k in ALERTS.order if k != Alerts.TEST_KEY]

    def height(self, w):
        n = len(self.kinds())
        return 98 + Kit.GAP + 40 + 28 * max(1, n)

    def build(self, g, x, y, w):
        if not ALERTS.loaded:
            ALERTS.load()
        self.store = ({}, {})
        c = {"rows": [], "dd": []}
        Kit.add_section(g, x, y, w, 98, "ALERTS  (every module's warnings)")
        c["mute"] = Kit.add_check(g, "Mute every alert sound", x + 12, y + 32, ALERTS.mute,
                                  "No sound for any alert; the banner and the journal line stay")
        c["banner"] = Kit.add_check(g, "Show the banner", x + 12 + 230, y + 32, ALERTS.banner_on,
                                    "Show alerts in a small banner at the top of the screen "
                                    "(click it to dismiss it, drag it anywhere)")
        Kit.art_button(g, self.store, "test", Kit.ART_PLAY, x + 12, y + 62, "Test alert",
                       "Raise a test alert: banner, sound and journal line")
        Kit.add_label(g, "The same alert repeats at most every %d s." % int(ALERT_RATE),
                      x + 12 + 160, y + 65, Kit.HUE_INFO)
        y2 = y + 98 + Kit.GAP
        kinds = self.kinds()
        h2 = 40 + 28 * max(1, len(kinds))
        # 2.6.81: a kind stays listed after its module stops (its choices still
        # apply when the module comes back), so the hint says when it was added
        Kit.add_section(g, x, y2, w, h2,
                        Kit.fit("ALERT KINDS  (from modules turned on this session)", w - 16))
        if not kinds:
            Kit.add_label(g, "No alert kinds yet: turn a module on that has alerts.",
                          x + 12, y2 + 36, Kit.HUE_INFO)
        dd_w = 150
        x_dd = x + w - 12 - 30 - 8 - dd_w
        later = []
        for i, key in enumerate(kinds):
            k = ALERTS.kinds[key]
            on, snd = ALERTS.setting(key)
            ry = y2 + 34 + 28 * i
            label = Kit.fit(k["label"], 196)
            cb = Kit.add_check(g, label, x + 12, ry, on, "Raise the %s alert" % k["label"])
            Kit.add_label(g, Kit.fit(k["owner"], x_dd - 8 - (x + 236)), x + 236, ry + 2,
                          Kit.HUE_INFO)
            Kit.art_button(g, self.store, "play%d" % i, Kit.ART_PLAY, x + w - 12 - 30, ry - 2,
                           None, "Play the sound picked for this alert")
            ids = [sid for _, sid in ALERT_SOUNDS]
            names = [n for n, _ in ALERT_SOUNDS]
            if snd not in ids:
                ids.append(snd)
                names.append("Sound 0x%X" % snd)
            later.append((key, ids, names, ids.index(snd), x_dd, ry))
            c["rows"].append((key, cb))
        for key, ids, names, idx, dx, dy in later:      # drop-downs last: their lists open on top
            dd = G.CreateDropDown(dd_w, names, idx)
            dd.SetPos(dx, dy)
            g.Add(dd)
            safe(lambda: dd.SetTooltip("The sound for this alert"))
            c["dd"].append((key, dd, ids, idx))
        self.c = c

    def poll(self):
        c = self.c
        if c is None:
            return
        try:
            mute = bool(c["mute"].IsChecked)
            banner = bool(c["banner"].IsChecked)
        except Exception:
            mute, banner = ALERTS.mute, ALERTS.banner_on
        if mute != ALERTS.mute or banner != ALERTS.banner_on:
            ALERTS.mute, ALERTS.banner_on = mute, banner
            if not banner:
                ALERTS.dismiss()
            ALERTS.save()
        for key, cb in c["rows"]:
            try:
                v = bool(cb.IsChecked)
            except Exception:
                continue
            if v != ALERTS.setting(key)[0]:
                ALERTS.choose(key, on=v)
        for n, row in enumerate(c["dd"]):
            key, dd, ids, idx = row
            try:
                i = int(dd.GetSelectedIndex())
            except Exception:
                continue
            if i != idx and 0 <= i < len(ids):
                c["dd"][n] = (key, dd, ids, i)
                ALERTS.choose(key, sound=ids[i])
        if Kit.was_clicked(self.store, "test"):
            ALERTS.kind(Alerts.TEST_KEY, "Test", 0x1EA, APP_NAME)
            ALERTS.last.pop((Alerts.TEST_KEY, "test"), None)
            ALERTS.raise_(Alerts.TEST_KEY, "This is how an alert looks and sounds.", "warn",
                          who="test")
        for n, row in enumerate(c["dd"]):
            if Kit.was_clicked(self.store, "play%d" % n):
                key, dd, ids, idx = row
                if ids[idx]:
                    safe(lambda: API.PlaySound(int(ids[idx])))

    def closed(self):
        self.c = None

    def api(self):
        return {"config_height": self.height, "build_config": self.build,
                "poll_config": self.poll, "config_closed": self.closed}


def _norm_key(k):
    return str(k or "").strip().upper().replace(" ", "")


class Binds(object):
    """(2.6.85) A key on any button. Every Kit.art_button notes an id here ("<owner>|<its
    key>": the module or part drawing it, then the button) with what one click does.
    Settings > Keys' Bind a button arms it: the next button clicked is picked instead
    of pressed, the client's key window asks for the key (on a thread of its own:
    API.RequestHotkey blocks), and the bind is saved per character. A bound key does what
    one click does, once: a key that fires again sooner than REPEAT after its last
    event is being held, so it is ignored until it was let go (R1). It never counts as a
    double-click, so a confirm that wants a real second press (R6) still does. A key
    another module or an Action Bar cell holds is refused."""
    VAR = "VirtueAssistant_binds"            # per character: "id=combo;id=combo"
    REPEAT = 0.6
    ARM_SECS = 20.0                          # bind mode ends by itself after this long
    REG_CAP = 5000
    armed_until = 0.0
    reg = {}                                 # id -> (store, key, on_click)
    saved = {}                               # id -> combo
    last = {}                                # combo -> when its last event came
    hooked = set()                           # combos with a client hook
    armed = False
    picked = None                            # the id waiting for its key
    answer = None                            # the key window's answer
    loaded = False
    OWNER = "Button binds"

    @staticmethod
    def note(store, key, on_click, ctl, tip):
        owner = getattr(HOST, "cur_owner", None)
        if owner is None:
            cur = HOST.current() if hasattr(HOST, "current") else None
            owner = cur.key if cur is not None else "va"
        bid = "%s|%s" % (owner, key)
        if len(Binds.reg) >= Binds.REG_CAP:      # (windows rebuilt note themselves again)
            Binds.reg.clear()
        Binds.reg[bid] = (store, key, on_click)
        return bid

    @staticmethod
    def wrap(bid, handler):
        def click(*args):
            if Binds.armed:                  # bind mode: this click picks the button
                Binds.armed = False
                if time.time() <= Binds.armed_until:
                    Binds.pick(bid)
                    return
            handler(*args)
        return click

    @staticmethod
    def load():
        if Binds.loaded:
            return
        try:
            if not API.Player:                   # the saved binds are this character's
                return
        except Exception:
            return
        Binds.loaded = True
        for part in str(Kit.get_var(Binds.VAR, "") or "").split(";"):
            if "=" in part:
                bid, combo = part.rsplit("=", 1)
                if bid and combo:
                    Binds.saved[bid] = combo
                    Binds.hook(combo)

    @staticmethod
    def save():
        Kit.put_var(Binds.VAR, ";".join("%s=%s" % kv for kv in sorted(Binds.saved.items())))

    @staticmethod
    def hook(combo):
        HOST.hotkey_note(combo, Binds.OWNER, "a button")
        if combo in Binds.hooked:
            return
        Binds.hooked.add(combo)

        def fired(*a):
            Binds.fire(combo)
        try:
            API.OnHotKey(combo, fired)
        except Exception:
            Binds.hooked.discard(combo)

    @staticmethod
    def fire(combo):
        now = time.time()
        was = Binds.last.get(combo)
        Binds.last[combo] = now
        if was is not None and 0 <= now - was < Binds.REPEAT:
            return                           # held: auto-repeat is ignored
        for bid, c in Binds.saved.items():
            if c == combo:
                r = Binds.reg.get(bid)
                if r is None:
                    return                   # its window isn't open
                store, key, on_click = r
                store[1][key] = True
                if on_click is not None:
                    on_click()
                return

    @staticmethod
    def arm(on=True):
        Binds.armed = bool(on)
        if on:
            Binds.armed_until = time.time() + Binds.ARM_SECS
            API.SysMsg("%s: click the button to bind, within %d s (Esc on the key window cancels)."
                       % (APP_NAME, int(Binds.ARM_SECS)), Kit.HUE_INFO)

    @staticmethod
    def pick(bid):
        Binds.armed = False
        Binds.picked = bid
        Binds.answer = None
        import System

        def ask():
            try:
                Binds.answer = str(API.RequestHotkey("Press the key for this button", 30) or "")
            except Exception:
                Binds.answer = ""
        t = System.Threading.Thread(System.Threading.ThreadStart(ask))
        t.IsBackground = True
        t.Start()

    @staticmethod
    def tick():
        """Host pass: the key window's answer."""
        if Binds.answer is None:
            return
        combo, Binds.answer = _norm_key(Binds.answer), None
        bid, Binds.picked = Binds.picked, None
        if bid is None or not combo:
            return
        taken = None
        for row in KeysPage.rows():
            if row[0] == combo and not (row[1] == Binds.OWNER and Binds.saved.get(bid) == combo):
                taken = row[1]
                break
        if taken is not None:
            API.SysMsg("%s: %s is already %s's key; pick another." % (APP_NAME, combo, taken), Kit.HUE_BAD)
            return
        old = Binds.saved.get(bid)
        if old:
            HOST.hotkey_drop(old, Binds.OWNER)
        Binds.saved[bid] = combo
        Binds.hook(combo)
        Binds.save()
        API.SysMsg("%s: %s bound." % (APP_NAME, combo), Kit.HUE_GOOD)
        HOST.refresh_settings(KEYS_PAGE)

    @staticmethod
    def clear():
        for combo in set(Binds.saved.values()):
            HOST.hotkey_drop(combo, Binds.OWNER)
        Binds.saved.clear()
        Binds.save()


class KeysPage(object):
    """Every hotkey Virtue Assistant listens to, with clashes in red:
    HOST.hotkey_note entries, HOST.hotkeys_owned (combo -> module title, kept
    for the modules that fill it), and every HOST.services["<key>.hotkeys"]()
    a module offers (a list of (combo, what): the Action Bar's cells)."""
    ROW = 24

    def __init__(self):
        self.c = None
        self.store = ({}, {})

    @staticmethod
    def rows():
        """[(combo, owner, what, clash)] sorted by combo."""
        out, seen = [], set()
        for combo, owner, what in list(HOST.hotkey_list):
            out.append((_norm_key(combo), owner, what))
            seen.add((_norm_key(combo), owner))
        for combo, owner in list(HOST.hotkeys_owned.items()):
            if (_norm_key(combo), owner) not in seen:
                out.append((_norm_key(combo), str(owner), ""))
        for name, fn in list(HOST.services.items()):
            if not name.endswith(".hotkeys") or not callable(fn):
                continue
            s = HOST.by_key.get(name[:-len(".hotkeys")])
            owner = s.title if s is not None else name[:-len(".hotkeys")]
            try:
                got = fn() or []
            except Exception:
                got = []
            for item in got:
                try:
                    out.append((_norm_key(item[0]), owner, str(item[1])))
                except Exception:
                    continue
        n = {}
        for combo, _, _ in out:
            if combo:
                n[combo] = n.get(combo, 0) + 1
        out = [(combo, owner, what, n.get(combo, 0) > 1) for combo, owner, what in out if combo]
        out.sort(key=lambda r: (r[0], r[1], r[2]))
        return out

    def height(self, w):
        return 64 + self.ROW * max(1, len(self.rows()))

    def build(self, g, x, y, w):
        self.store = ({}, {})
        rows = self.rows()
        h = 64 + self.ROW * max(1, len(rows))
        Kit.add_section(g, x, y, w, h, "HOTKEYS  (every key Virtue Assistant listens to)")
        cap = "Refresh"
        rx = x + w - 12 - 35 - Kit.text_w(cap)
        Kit.art_button(g, self.store, "refresh", Kit.ART_PAGE, rx, y + 4, cap,
                       "Read every module's hotkeys again")
        cap = "Clear binds"                  # (2.6.85) a key on any button
        rx -= 16 + 35 + Kit.text_w(cap)
        Kit.art_button(g, self.store, "bind_clear", Kit.ART_CLOSE, rx, y + 28, cap,
                       "Take the key off every button that has one")
        cap = "Bind a button"
        Kit.art_button(g, self.store, "bind", Kit.ART_PLAY, rx - 16 - 35 - Kit.text_w(cap), y + 28, cap,
                       "Click this, then any button of any window, then press its key")
        clashes = len(set(r[0] for r in rows if r[3]))
        Kit.add_label(g, ("%d key%s bound twice (shown in red)" % (clashes, "" if clashes == 1 else "s"))
                      if clashes else "No key is bound twice.", x + 12, y + 32,
                      Kit.HUE_BAD if clashes else Kit.HUE_INFO)
        if not rows:
            Kit.add_label(g, "No module that is on has a hotkey set.", x + 12, y + 56,
                          Kit.HUE_INFO)
        xo, xw = x + 12 + 160, x + 12 + 160 + 150
        for i, (combo, owner, what, clash) in enumerate(rows):
            ry = y + 56 + self.ROW * i
            hue = Kit.HUE_BAD if clash else Kit.HUE_TEXT
            Kit.add_label(g, Kit.fit(combo, 150), x + 12, ry, hue)
            Kit.add_label(g, Kit.fit(owner, 140), xo, ry, hue if clash else Kit.HUE_TITLE)
            if what:
                Kit.add_label(g, Kit.fit(what, x + w - 16 - xw), xw, ry, Kit.HUE_INFO)
        self.c = True

    def poll(self):
        if self.c is not None and Kit.was_clicked(self.store, "refresh"):
            HOST.refresh_settings(KEYS_PAGE)
        if self.c is not None and Kit.was_clicked(self.store, "bind"):
            Binds.arm(True)
        if self.c is not None and Kit.was_clicked(self.store, "bind_clear"):
            Binds.clear()
            HOST.refresh_settings(KEYS_PAGE)

    def closed(self):
        self.c = None

    def api(self):
        return {"config_height": self.height, "build_config": self.build,
                "poll_config": self.poll, "config_closed": self.closed}


ALERTS_PAGE, KEYS_PAGE = "va.alerts", "va.keys"


# =============================================================================
#  What's new (2.6.05): the first time a new version runs on an account, a
#  small window shows WHATS_NEW; closed, it doesn't come back for that version.
# =============================================================================
class WhatsNew(object):
    W = 520

    def __init__(self):
        self.g = None
        self.store = ({}, {})

    @staticmethod
    def due():
        if not WHATS_NEW:
            return False
        try:
            seen = API.GetPersistentVar(WHATS_NEW_KEY, "", API.PersistentVar.Account)
        except Exception:
            return False
        return str(seen or "") != APP_VERSION

    def open(self):
        if self.due():
            Kit.on_client(self._build)

    def _build(self):
        M, W = Kit.MARGIN, self.W
        lines = []
        for para in WHATS_NEW:
            lines += Kit.wrap(para, W - 2 * M - 24) or [""]
        h_body = 16 + 20 * len(lines)
        H = M + 30 + Kit.GAP + h_body + M
        self.store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, "WHAT'S NEW IN %s %s" % (APP_NAME.upper(), APP_VERSION), M + 30, M + 7,
                      Kit.HUE_TITLE)
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                       "Close (shown once per version)")
        yb = M + 30 + Kit.GAP
        Kit.add_section(g, M, yb, W - 2 * M, h_body)
        for i, line in enumerate(lines):
            Kit.add_label(g, line, M + 12, yb + 8 + 20 * i, Kit.HUE_TEXT)
        sw, sh = Kit.screen()
        Kit.place(g, max(0, ((sw or 1024) - W) // 2), max(0, ((sh or 768) - H) // 3), W, H)
        G.AddGump(g)
        self.g = g

    def poll(self):
        g = self.g
        if g is None:
            return
        if not Kit.is_open(g) or Kit.was_clicked(self.store, "close"):
            self.close(True)

    def close(self, seen=False):
        g, self.g = self.g, None
        Kit.dispose(g)
        if seen:
            try:
                API.SavePersistentVar(WHATS_NEW_KEY, APP_VERSION, API.PersistentVar.Account)
            except Exception:
                pass


# =============================================================================
#  Host - runs the modules side by side
#  Every module gets a tick() on its own interval. Each script call that
#  returns something waits for the client's next frame, so the host makes ONE
#  hop to the client thread per pass and does everything that can't wait
#  there: the windows' polling, snapping, the Action Bar folds and the tick of
#  every module that says "client_tick": True (it must never wait: no
#  HOST.idle, API.Pause, API.RequestTarget). Inside that hop every call runs
#  in place, at no wait. A module that has to wait (a server reply, a gump)
#  does that in its optional thread_tick(), run on the script's own thread
#  right after; HOST.idle(seconds) there keeps the others and the windows
#  running while it waits. Modules without client_tick tick on the script's
#  thread as before. HOST.pick_target() asks the player for a target without
#  holding anything up.
# =============================================================================
class ModuleSlot(object):
    def __init__(self, key, title, desc, factory, interval):
        self.key = key
        self.title = title
        self.desc = desc
        self.factory = factory
        self.interval = interval
        self.api = None           # what the module's factory returned
        self.lazy = None          # path of its file, while not yet compiled (see Host.load)
        self.broken = None        # why the module could not be loaded
        self.enabled = False      # wanted on (saved)
        self.default_on = False   # on until this character unticks it (HOST.add default_on)
        self.category = "Other"   # its heading on the Modules tab (HOST.add category)
        self.running = False
        self.busy = False         # inside its own start / tick / stop
        self.pending_stop = False
        self.next_due = 0.0
        self.errors = set()
        self.error_count = 0
        self.worst_ms = 0.0       # slowest tick in the last little while (decays)
        self.slow_told = False
        self.thread_due = False   # its thread_tick is owed a run (after a client tick)
        self.idle_told = False
        self.on_client = False    # "client_tick", read once when it starts (Host._arm)
        self.iv_fn = None         # its "interval" hook, read once when it starts (2.6.82)
        self.has_thread = False   # it has a "thread_tick" (2.6.82, Host._arm)
        self.thread_want = None   # its "thread_wanted" hook: thread work only when asked
        # ---- a module made of parts (2.6.5, HOST.add parts=...) ----
        self.parts = ()           # (key, title, description, on at first, replaced old keys)
        self.aliases = ()         # old names and feature words the Modules search also matches
        self.parts_on = {}        # part key -> wanted on (saved as parts= in the settings)
        self.parts_running = set()   # the parts running now (kept by the module's PartSet)
        self.folded = True        # its parts hidden under its row on the Modules tab

    @property
    def client(self):
        """The module's tick runs on the client thread, batched with the others."""
        return bool(self.api and self.api.get("client_tick"))

    def part(self, key):
        """The part tuple with that key, or None."""
        for p in self.parts:
            if p[0] == key:
                return p
        return None

    def parts_wanted(self):
        """The keys of the parts ticked on, in the order of the parts list."""
        return [p[0] for p in self.parts if self.parts_on.get(p[0])]

    def part_title(self, key):
        p = self.part(key)
        return "%s > %s" % (self.title, p[1]) if p is not None else self.title


class PartView(object):
    """What HOST.by_key answers for a 2.6.06 module key that is a part now
    ("swing" -> Character HUD's Swing bar), and for "<module>.<part>": the
    few things other modules read of a slot (title, running, enabled, key)."""
    def __init__(self, key, slot, part):
        self.key = key
        self.slot = slot
        self.part = part
        self.title = slot.part_title(part)
        self.category = slot.category

    @property
    def running(self):
        return bool(self.slot.running and self.part in self.slot.parts_running)

    @property
    def enabled(self):
        return bool(self.slot.enabled and self.slot.parts_on.get(self.part))

    @property
    def api(self):
        return self.slot.api

    @property
    def lazy(self):
        return self.slot.lazy

    @property
    def broken(self):
        return self.slot.broken


class _KeyMap(dict):
    """HOST.by_key: the module slots by key, and (2.6.5) a PartView for an old
    module key that became a part, or for "<module>.<part>"."""
    def __init__(self, host):
        dict.__init__(self)
        self.host = host

    def view(self, key):
        slot, part = self.host.resolve(key)
        return PartView(key, slot, part) if part is not None else None

    def __contains__(self, key):
        return dict.__contains__(self, key) or self.view(key) is not None

    def get(self, key, default=None):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        v = self.view(key)
        return v if v is not None else default

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        v = self.view(key)
        if v is None:
            raise KeyError(key)
        return v


def _error_where():
    """'line N' of the innermost frame of the exception being handled, with
    the file's name when it happened in a module file."""
    try:
        import sys
        tb = sys.exc_info()[2]
        while tb is not None and tb.tb_next is not None:
            tb = tb.tb_next
        if tb is None:
            return ""
        where = safe(lambda: os.path.basename(str(tb.tb_frame.f_code.co_filename)), "") or ""
        if where.endswith("Module.py"):
            return " (%s line %d)" % (where, tb.tb_lineno)
        return " (line %d)" % tb.tb_lineno
    except Exception:
        return ""


class JLine(object):
    """One journal line, read once for every module (see Journal)."""
    __slots__ = ("seq", "text", "low", "name", "hue", "ticks", "at", "kind")

    def __init__(self, seq, text, name, hue, ticks, at, kind):
        self.seq, self.text, self.low, self.name = seq, text, text.lower(), name
        self.hue, self.ticks, self.at, self.kind = hue, ticks, at, kind


class Journal(object):
    """The journal, read ONCE per pass for every module.

    API.GetJournalEntries(secs) walks the script's whole journal queue (up to
    the client's "max journal entries") every call and hands back every match
    as a new object; with each module reading 5-30 s back on every tick, the
    same lines were crossed hundreds of times a second. Here the queue is read
    once per pass, only back to the previous read, each line is turned into a
    JLine once (text, lower-case text, speaker name, hue, the client's time in
    ticks, and the time it was first seen here), de-duplicated by (time, text,
    speaker), and kept for KEEP seconds. Only the lines that are new since the
    last read are turned into JLines: the read walks back from the newest line
    and stops at the first one it has already seen. Nothing is ever cleared
    from the client's journal.

      Journal.reader()         -> a reader of your own: reader.new() gives the
                                  lines that came in since your last call
                                  (first call: since the reader was made).
                                  The read itself happens once per pass: in a
                                  thread_tick, call Journal.update(True) first
                                  to see a line that arrived during this pass
      Journal.since(t)         -> lines first seen at or after time.time() t
      Journal.recent(secs)     -> lines first seen in the last secs seconds
      Journal.find(t, texts)   -> the first line since t containing any of
                                  texts (case-insensitive), or None

    Lines from Virtue Assistant's own journal messages are included (filter by
    their "Title:" prefix if a module must skip them)."""
    KEEP = 60.0               # seconds a line is kept here
    MAX_BACK = 30.0           # never read further back than this
    lines = []                # JLine, oldest first
    seen = {}                 # (ticks, text, speaker) -> seq, for the lines still kept
    seq = 0
    read_at = 0.0             # time.time() of the last read
    pass_id = -1              # Host pass the last read belongs to
    direct = True             # (2.6.82) the entries have .Name (read straight, not getattr)
    zero_seen = False         # a line without a client time was met: reads walk the whole
    #                           window (see update), not only back to the last line seen

    class Reader(object):
        __slots__ = ("last",)

        def __init__(self):
            self.last = Journal.seq

        def new(self, read=True):
            """The lines that came in since the last call. read=False: only the
            lines the Journal already holds, without a read of the client's
            journal (one is made every pass a module or the host reads)."""
            if read:
                Journal.update()
            last, self.last = self.last, Journal.seq
            if last >= Journal.seq:
                return []
            out = []
            for ln in reversed(Journal.lines):
                if ln.seq <= last:
                    break
                out.append(ln)
            out.reverse()
            return out

    @staticmethod
    def reader():
        Journal.update()
        return Journal.Reader()

    @staticmethod
    def update(force=False):
        """Read what's new (once per pass; free on later calls in the same pass)."""
        pid = HOST.pass_id
        if pid == Journal.pass_id and not force:
            return
        Journal.pass_id = pid
        now = time.time()
        back = min(Journal.MAX_BACK, max(1.0, now - Journal.read_at + 1.0)) \
            if Journal.read_at else Journal.MAX_BACK
        Journal.read_at = now
        try:
            entries = API.GetJournalEntries(back) or []
        except Exception:
            entries = []
        seen = Journal.seen
        # The client hands the lines back oldest first, and everything before
        # the newest line already taken was taken too: walk back from the end
        # and stop at the first line already seen, so each pass costs the new
        # lines only, not the whole read-back window (crossed again every pass).
        fresh = []
        try:
            i = len(entries) - 1
        except Exception:                    # an enumerable without a length
            entries = list(entries)
            i = len(entries) - 1
        zero = []                            # (key, e) of lines without a client time, newest first
        stopped = False                      # the walk reached a timed line already seen
        while i >= 0:
            e = entries[i]
            i -= 1
            pos = i                          # its place in the window (older = smaller)
            try:
                text = str(e.Text or "")
                if not text:
                    continue
                try:
                    ticks = int(e.Time.Ticks)
                except Exception:
                    ticks = 0
                if Journal.direct:           # (2.6.82) the plain read; getattr only if absent
                    try:
                        name = str(e.Name or "")
                    except AttributeError:
                        Journal.direct = False
                        name = str(getattr(e, "Name", "") or "")
                else:
                    name = str(getattr(e, "Name", "") or "")
                key = (ticks, text, name)        # two speakers, same words, same tick: two lines
                if ticks == 0:
                    # no client time on this build: the key repeats for every
                    # repeat of the line ("You are too far away"), so the walk
                    # can't stop at it. Count copies instead (below): the copies
                    # beyond the ones already kept are new lines, and the newest
                    # of them (de-duplication by position).
                    zero.append((key, e, pos))
                    Journal.zero_seen = True
                    continue
                if stopped or key in seen:
                    # every timed line older than this one was taken already.
                    # Once a line without a time has been met (this read or an
                    # earlier one) the walk goes on to the window's start all
                    # the same: every copy of such a line in the window must be
                    # counted, and one not taken yet may sit below this line
                    # (see `kept`). Timed lines are only skipped from here on.
                    if not Journal.zero_seen:
                        break
                    stopped = True
                    continue
                fresh.append((key, e, pos))
            except Exception:
                continue
        if zero:
            total = {}
            for key, e, pos in zero:
                total[key] = total.get(key, 0) + 1
            # the copies already kept that the client handed back again: those
            # first seen inside this read's window (`back` seconds; a copy seen
            # before it is out of the window, so it must not be counted against
            # the copies in it)
            kept = {}
            ws = now - back
            for ln in reversed(Journal.lines):
                if ln.at < ws:
                    break
                if ln.ticks == 0:
                    k = (0, ln.text, ln.name)
                    kept[k] = kept.get(k, 0) + 1
            rank = {}
            for key, e, pos in zero:         # newest first: rank 0 is the newest copy
                r = rank.get(key, 0)
                rank[key] = r + 1
                if r < total[key] - kept.get(key, 0):
                    fresh.append((key, e, pos))
            fresh.sort(key=lambda t: t[2])   # oldest first, whatever the kind of key
        else:
            fresh.reverse()                  # the walk was newest first
        added = {}
        for key, e, pos in fresh:
            if key[0] != 0:
                if key in added:             # the same (time, text, speaker) twice: once
                    continue
                added[key] = 1
            try:
                Journal.seq += 1
                seen[key] = Journal.seq
                Journal.lines.append(JLine(Journal.seq, key[1], key[2],
                                           int(getattr(e, "Hue", 0) or 0), key[0], now,
                                           str(getattr(e, "TextType", "") or "")))
            except Exception:
                continue
        # forget what's older than KEEP (and its de-duplication key, once the
        # client can no longer hand it back: KEEP > MAX_BACK)
        cut = now - Journal.KEEP
        lines = Journal.lines
        if lines and lines[0].at < cut:
            i = 0
            while i < len(lines) and lines[i].at < cut:
                ln = lines[i]
                seen.pop((ln.ticks, ln.text, ln.name), None)
                i += 1
            del lines[:i]

    @staticmethod
    def since(t):
        Journal.update()
        out = []
        for ln in reversed(Journal.lines):
            if ln.at < t:
                break
            out.append(ln)
        out.reverse()
        return out

    @staticmethod
    def recent(secs):
        return Journal.since(time.time() - secs)

    @staticmethod
    def find(t, texts):
        if isinstance(texts, str):          # one text, not its letters
            texts = (texts,)
        low = [x.lower() for x in texts]
        for ln in Journal.since(t):
            for x in low:
                if x in ln.low:
                    return ln
        return None


class Picker(object):
    """Target cursors that don't stop the other modules. API.RequestTarget
    holds the script until the player clicks (up to its timeout), so every
    module stood still while a cursor was up. Instead the client's own
    callback cursor is put up and watched once per pass; on builds where the
    client can't be reached, API.RequestTarget is used as before."""
    jobs = []                 # {"t", "fn", "until", "d", "got", "block"}
    cuo = None
    neutral = None            # the client's TargetType.Neutral, once _tm() found it
    looked = False
    CURSOR_TARGET = 6983686   # the client's CursorType.Target

    @staticmethod
    def _tm():
        if not Picker.looked:
            Picker.looked = True
            try:
                import clr
                clr.AddReference(API.GetType().Assembly)
                from ClassicUO import Client as CUO
                from ClassicUO.Game.Managers import TargetType
                Picker.cuo, Picker.neutral = CUO, TargetType.Neutral
            except Exception:
                Picker.cuo = None
        if Picker.cuo is None:
            return None
        try:                                  # (2.6.82) no lambda per pass
            return Picker.cuo.Game.UO.World.TargetManager
        except Exception:
            return None

    @staticmethod
    def ask(timeout, fn, owner=None):
        """owner: the key of the module asking (its cursor comes down when it
        stops, see drop); defaults to the module running now, which a cursor
        raised from a click handler or a dock hook has none of."""
        for j in Picker.jobs:                 # one cursor at a time: the new one wins
            j["cancel"] = True
        if owner is None:
            owner = HOST.owner_key()
        Picker.jobs.append({"t": float(timeout), "fn": fn, "until": 0.0, "d": None,
                            "got": None, "block": False, "cancel": False, "owner": owner})
        HOST.poke()

    @staticmethod
    def _done(j, serial):
        if j in Picker.jobs:
            Picker.jobs.remove(j)
        try:
            j["fn"](int(serial or 0))
        except Exception as ex:
            safe(lambda: API.SysMsg("%s: target error: %s%s" % (APP_NAME, ex, _error_where()),
                                    Kit.HUE_BAD))

    @staticmethod
    def tick():
        """On the client thread, every pass."""
        if not Picker.jobs:
            return
        tm = Picker._tm()
        for j in list(Picker.jobs):
            if j["block"]:
                continue
            if j["d"] is None:                # not up yet
                if j["cancel"]:
                    Picker._done(j, 0)
                    continue
                if tm is None:
                    j["block"] = True         # no client access: the old way
                    continue
                try:
                    from System import Action

                    def got(obj, j=j):
                        try:
                            j["got"] = int(getattr(obj, "Serial", 0) or 0) if obj is not None else 0
                        except Exception:
                            j["got"] = 0
                    j["d"] = Action[object](got)
                    tm.SetTargeting(j["d"], Picker.CURSOR_TARGET, Picker.neutral)
                    j["until"] = time.time() + j["t"]
                except Exception:
                    j["d"], j["block"] = None, True
                continue
            if j["got"] is not None:
                Picker._done(j, j["got"])
                continue
            try:
                cur = bool(tm.IsCurrentTargetingAction(j["d"]))
            except Exception:
                cur = False
            if not cur:
                Picker._done(j, 0)            # cancelled, or another cursor took over
            elif j["cancel"] or time.time() >= j["until"]:
                try:
                    tm.CancelTarget()         # ours: clear it (fires got(None))
                except Exception:
                    pass
                Picker._done(j, 0)

    @staticmethod
    def drop(owner=None):
        """A module stopped (owner = its key) or the script is stopping (None):
        its cursors come down, and their on_done gets 0 (so whoever asked
        never waits for an answer that won't come)."""
        mine = [j for j in Picker.jobs if owner is None or j.get("owner") == owner]
        if not mine:
            return
        for j in mine:
            Picker.jobs.remove(j)
        tm = Picker._tm()
        up = [j["d"] for j in mine if j["d"] is not None and j["got"] is None]
        if tm is not None and up:
            def take_down():
                for d in up:
                    if tm.IsCurrentTargetingAction(d):
                        tm.CancelTarget()
            safe(lambda: Kit.on_client(take_down, fallback=False))
        for j in mine:
            Picker._done(j, 0)

    @staticmethod
    def run_blocking():
        """On the script's thread: the old blocking cursor, for builds where the
        client can't be reached."""
        for j in [j for j in Picker.jobs if j["block"]]:
            Picker.jobs.remove(j)
            serial = 0 if j["cancel"] else int(safe(lambda: API.RequestTarget(j["t"]), 0) or 0)
            Picker._done(j, serial)


def _first(e):
    """Sort key: an entry's first item (a mobile's distance)."""
    return e[0]


class _Memo(object):
    """(2.6.82) One game object (the player, a mobile) read lazily for one
    client pass: the first read of a property asks the client, the rest of the
    pass get the same value. .raw is the object itself (hand that to an API
    call, or use it for anything with a side effect). Only HOST.me / mobiles /
    mobile make these; they are thrown away when the pass ends."""

    def __init__(self, raw):
        self.__dict__["raw"] = raw

    def __getattr__(self, name):
        v = getattr(self.__dict__["raw"], name)
        self.__dict__[name] = v
        return v

    def __setattr__(self, name, value):
        setattr(self.__dict__["raw"], name, value)     # a write goes to the object itself
        self.__dict__.pop(name, None)

    def __int__(self):
        return int(self.__dict__["raw"].Serial)


class Host(object):
    def __init__(self):
        self.slots = []
        self.by_key = _KeyMap(self)
        self.old_map = {}         # 2.6.06 module key -> (module key, part key) (HOST.add parts=)
        self.cur_part = None      # the part (its key) whose code is running (set by its PartSet)
        self.cur_owner = None     # that part's owner key: its 2.6.06 key, or "<module>.<part>"
        self.dock_owner = {}      # dock key -> (module key, part key or None)
        self.stack = []           # modules whose code is running right now
        self.quitting = False
        self.shut = False
        self.ui_busy = False
        self.ui_next = 0.0        # next look at the script's own windows
        self.config = None
        self.hub = None           # the shared floating window (Ultima Tracker's controls)
        self.docks = []           # windows that can fold into the Action Bar: [(key, hooks)]
        self.dock_next = 0.0
        self.services = {}        # things one module offers another, by name
        self.hotkeys_owned = {}   # hotkey combo -> module title, for modules that bind keys
        self.debug = False        # extra lines in the journal (Modules tab checkbox)
        self.prefs = {}
        self.poked = False        # a click landed: run every module on the next pass
        self.grid = None          # the screen grid (GRID button on the Action Bar)
        self.profile_req = None   # ("save" / "load" / "fav", profile name) from the window
        self.prefs_frozen = False # a profile is being loaded: don't write the old choices
        self.cursor_claim = (None, 0.0)   # (module key, until): see claim_cursor
        self._claim_len = 0.0             # (2.6.84) how long the claim was made for
        self.foe_seen = (0.0, None)       # (look again at, name of the hostile or None): foe_near
        self.hurt_hp = None               # your HP at the last fight_hold, and the hold it set
        self.hurt_until = 0.0
        self.hurt_at = 0.0                # when hurt_hp was read
        self.client_idles = 0     # HOST.idle calls made on the client thread in this hop
        self.pass_id = 0          # counts passes of the main loop (Journal reads once per pass)
        self.input_at = 0.0       # (2.6.82) the last click / input seen (poll_due)
        # ---- (2.6.82) the shared per-pass reads: HOST.me / mobiles / mobile / pack_items.
        #      Values are kept only inside the client hop (in_hop), where nothing in
        #      the game moves, so a kept value is exactly what a fresh read would give
        self.in_hop = False
        self._me_pid = -1
        self._me = None
        self._mob_pid = -1
        self._mob_list = ()       # ((distance, _Memo), ...) nearest first, for _mob_pid
        self._one_pid = -1
        self._one = {}            # serial -> _Memo or None (FindMobile), for _one_pid
        self._pack = {}           # deep (bool) -> (pass id or -1, time, [items])
        # the scheduler's own lists, rebuilt only when a module starts or stops
        # (never per pass): the running modules in Modules-tab order, and those
        # of them that tick on the client thread
        self.active = []
        self.client_run = []
        self.pass_poked = False   # the pass being run was poked (read by _client_pass)
        self._pass_fn = self._client_pass   # bound once: no new closure on every pass
        self._want_raw = None     # the "dock_want" pref as last parsed, and its set
        self._want_set = frozenset()
        self.told = set()         # the mother's own error lines already shown (once each)
        self.load_jobs = []       # module slots whose file is to be compiled on the script
        #                           thread (see request_load): never inside the client hop
        self.hotkey_list = []     # (combo, owner title, what) noted with hotkey_note (Keys page)
        self.pages = []           # the Settings tab's own pages (Alerts, Keys, Layout), after the modules'
        for key, title, page in ((ALERTS_PAGE, "Alerts", AlertsPage()),
                                 (KEYS_PAGE, "Keys", KeysPage()),
                                 (LAYOUT_PAGE, "Layout", LayoutPage())):
            s = ModuleSlot(key, title, "", None, 1.0)
            s.api = page.api()
            self.pages.append(s)
        self.whats_new = WhatsNew()

    def _tell(self, msg):
        """One journal line for a problem of the mother's own; the same line is
        not repeated (a fault that recurs every pass would flood the journal)."""
        if msg in self.told:
            return
        if len(self.told) > 50:
            self.told.clear()
        self.told.add(msg)
        try:
            API.SysMsg(msg, Kit.HUE_BAD)
        except Exception:
            pass

    def _refresh_active(self):
        """Rebuild the scheduler's lists (a module started or stopped)."""
        act = [s for s in self.slots if s.running]
        self.active = act
        self.client_run = [s for s in act if s.on_client]

    def poke(self):
        """Something happened (a click): every running module and the windows
        get a pass right away instead of waiting for their next due tick."""
        self.poked = True
        self.input_at = time.time()           # (2.6.82) pages poll fast for a while

    # ---- (2.6.82) settings pages and the hub sections: nothing on them changes
    #      without a click or a key, so they are read at full rate (every UI tick)
    #      for INPUT_FAST s after input (a click anywhere, the button held, typing)
    #      and every PAGE_EVERY s otherwise. A page showing live values may ask
    #      for its own pace with "poll_every" in its hooks.
    INPUT_FAST = 1.0
    PAGE_EVERY = 0.25

    def poll_due(self, gate, every=None):
        """True when a page / section is to be read now. gate is a one-item
        list holding when it is due next (the caller's own)."""
        now = time.time()
        if every is not None and every <= UI_TICK:
            return True
        if not Kit.clicks_seen:
            return True                          # clicks don't seem to arrive: as before
        if now - self.input_at <= self.INPUT_FAST or 0 <= gate[0] - now > 2.0:
            fast = True                          # (also: the clock was set back)
        else:
            fast = False
            p = SNAP.pressed()
            if p is not False:                   # held (a slider, a drag) or not known
                if p:
                    self.input_at = now
                fast = True
            elif Kit.typing():
                fast = True
        if fast or now >= gate[0]:
            gate[0] = now + (every if every is not None else self.PAGE_EVERY)
            return True
        return False

    # ---------- shared services: alerts, guard zones, hotkeys (2.6.05) ----------
    def alert_kind(self, key, label, default_sound=None):
        """List an alert kind on Settings > Alerts (see Alerts); call it in start()."""
        s = self.current()
        return ALERTS.kind(key, label, default_sound, s.title if s is not None else APP_NAME)

    def alert(self, key, text, level="warn", sound=None, ping=None, who=None):
        """Banner, sound and journal line, rate-limited (see Alerts). True if raised."""
        s = self.current()
        return ALERTS.raise_(key, text, level, sound, ping, who,
                             s.title if s is not None else APP_NAME)

    def guarded(self):
        """True under the town guards' protection, False outside, None not known (see Guard)."""
        return GUARD.guarded()

    def guard_area(self):
        """The GUARD_AREAS name of where you stand, or None."""
        return GUARD.area()

    def hotkey_note(self, combo, owner, what=""):
        """A module binds `combo` (listed on Settings > Keys; clashes show in red).
        It is held in hotkeys_owned too (unless another module holds it there),
        so the Action Bar keeps off it."""
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list
                            if not (_norm_key(e[0]) == k and e[1] == owner)]
        self.hotkey_list.append((k, str(owner), str(what or "")))
        if k not in self.hotkeys_owned:
            self.hotkeys_owned[k] = str(owner)

    def hotkey_drop(self, combo, owner=None):
        """The module let go of `combo` (owner None: whoever held it)."""
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list
                            if not (_norm_key(e[0]) == k and (owner is None or e[1] == owner))]
        left = [e[1] for e in self.hotkey_list if _norm_key(e[0]) == k]
        cur = self.hotkeys_owned.get(k)
        if cur is not None and (owner is None or cur == str(owner)):
            if left:
                self.hotkeys_owned[k] = left[0]      # another module still binds it
            else:
                del self.hotkeys_owned[k]
        elif cur is None and left:
            self.hotkeys_owned[k] = left[0]          # the leaving module took it out first

    def page_slot(self, key):
        """The settings page `key`: a module's, or one of the Settings tab's own.
        An old module key (or "<module>.<part>") gives its module's page."""
        s, part = self.resolve(key)
        if s is None:
            for p in self.pages:
                if p.key == key:
                    return p
        return s

    # ---------- modules made of parts (2.6.5) ----------
    #  HOST.add(..., parts=((key, title, description, on at first, (old keys it
    #  replaces, ...)), ...), aliases=(...)) lists a module whose features are
    #  parts, each with its own box under the module's row on the Modules tab.
    #  The module's file builds every part like a module of its own and hands
    #  them to a PartSet, which runs the ones that are on (see PartSet). The
    #  parts that are on are saved per character as parts=<module>.<part>,...
    #  (see load_prefs for how a 2.6.06 modules= is carried over).
    def resolve(self, key):
        """(slot, part key or None) for a module key, an old module key that
        is a part now, or "<module>.<part>"; (None, None) when unknown."""
        s = dict.get(self.by_key, key)
        if s is not None:
            return s, None
        m = self.old_map.get(key)
        if m is None and "." in str(key):
            mk, pk = str(key).split(".", 1)
            m = (mk, pk)
        if m is not None:
            s = dict.get(self.by_key, m[0])
            if s is not None and s.part(m[1]) is not None:
                return s, m[1]
        return None, None

    def _note_parts(self, s, parts, aliases):
        s.parts = tuple(tuple(p) for p in (parts or ()))
        s.aliases = tuple(str(a) for a in (aliases or ()))
        for p in s.parts:
            for old in (p[4] if len(p) > 4 else ()):
                self.old_map[str(old)] = (s.key, p[0])
            if p[0] not in s.parts_on:
                s.parts_on[p[0]] = False

    def part_on(self, part, module=None):
        """Is `part` of the calling module (or of `module`) ticked on."""
        if module is None:
            cur = self.current()
            module = cur.key if cur is not None else None
        s = dict.get(self.by_key, module)
        return bool(s is not None and s.parts_on.get(part))

    def part_running(self, key):
        """Is that feature running: a module key, an old module key that is a
        part now, or "<module>.<part>"."""
        s, part = self.resolve(key)
        if s is None:
            return False
        return bool(s.running and (part is None or part in s.parts_running))

    def owner_key(self):
        """The key of the code running now: the part's (its old key when it has
        one) inside a PartSet, else the module's."""
        cur = self.current()
        if cur is None:
            return None
        if self.cur_owner is not None and cur.parts:
            return self.cur_owner
        return cur.key

    def _parts_default(self, s):
        """The parts to turn on when a module made of parts is turned on with
        none of them ticked: those on at first, else its first part."""
        on = [p[0] for p in s.parts if p[3]]
        return on or ([s.parts[0][0]] if s.parts else [])

    def _part_notify(self, s):
        """Tell a running module which of its parts are on now (its "parts" hook)."""
        if not s.running or s.api is None or not s.api.get("parts"):
            return
        self._enter(s)
        try:
            # (2.6.84) a part started from the script thread (an Action Bar press)
            # builds its windows in one hop, as Host.start does (in place there)
            want = set(s.parts_wanted())
            Kit.on_client(lambda: s.api["parts"](want))
        except Exception as ex:
            self.report(s, ex)
        finally:
            self._leave(s)

    def part_set(self, module, part, on):
        """Tick or untick one part. Ticking a part of a module that is off turns
        the module on; unticking its last part turns the module off (the part
        choices are kept for next time)."""
        s = dict.get(self.by_key, module)
        if s is None or s.part(part) is None:
            return
        on = bool(on)
        if s.parts_on.get(part) == on:
            if on and not s.enabled:
                self.enable(module)
            return
        s.parts_on[part] = on
        if on:
            if not s.enabled:
                self.enable(module)
            else:
                self.save_prefs()
                self._part_notify(s)
        else:
            if not s.parts_wanted():
                self.disable(module)
            else:
                self.save_prefs()
                self._part_notify(s)
        self.refresh_settings(module)          # its page shows a section per part that is on

    def alarm_up(self):
        """True while an alarm-level alert banner waits for a click (any module's)."""
        return bool(ALERTS.shown and ALERTS.alarm)

    # ---------- keys ----------
    def typing(self):
        """True while keys go into a text field anywhere on screen (the chat
        line, any text box of any window): a hotkey must do nothing then."""
        return Client.typing()

    def release_typing(self):
        """Take keyboard focus off whatever field has it (back to the chat
        line, as a click on the game world does)."""
        Typing.release()

    # ---------- the screen grid (any window snaps to it while it is shown) ----------
    def grid_size(self):
        return max(8, min(512, self.pref_int("grid", GRID_DEFAULT)))

    def grid_shown(self):
        return self.grid is not None and self.grid.shown

    def grid_toggle(self):
        if self.grid is not None:
            self.grid.toggle()
            self.prefs["grid_on"] = "1" if self.grid_shown() else "0"
            self.save_prefs()                 # shown again at the next start
        return self.grid_shown()

    # ---------- windows that fold into the Action Bar ----------
    #  hooks: "title", "icon" (item graphic for the bar's tray button),
    #  "state"() -> None (off) / "open" / "minimized" / "docked" (hidden, the
    #  bar's button stands in for it), "show"(), "dock"(), "undock"() (back to
    #  the minimized form when the bar goes away), "minimize"() (the minimized
    #  form, not folded; optional), optional "on"() for a click while the
    #  state is None.
    #
    #  Minimizing never folds a window into the bar by itself: Minimize gives
    #  the window's own minimized form. A window folds in only when asked:
    #  its gold "Fold into the Action Bar" button (dock_to_bar), the bar's
    #  tray / window buttons, or a wish kept from last time. The wish (a set
    #  of keys, pref "dock_want", per character) lasts until the window is
    #  shown again; while it stands and the bar is away the window waits in
    #  its minimized form and folds in when the bar comes back. Grimoire,
    #  Bags (Inventory) and this window (keys "grimoire", "bag", "va") talk to the
    #  bar through shared vars, but keep their wish here too.
    def dock_wanted(self, key):
        return key in self._dock_want()

    def _dock_want(self):
        """The keys wished folded (read-only; parsed again only when it changed)."""
        raw = self.prefs.get("dock_want", "") or ""
        if raw != self._want_raw:
            self._want_raw = raw
            self._want_set = frozenset(k for k in str(raw).split(",") if k)
        return self._want_set

    def dock_want_set(self, key, on):
        """Keep (on) or drop the wish that window `key` sits folded in the bar."""
        want = self._dock_want()
        if bool(on) == (key in want):
            return
        want = set(want)
        if on:
            want.add(key)
        else:
            want.discard(key)
        self.prefs["dock_want"] = ",".join(sorted(want))
        self.save_prefs()                     # kept for the next start

    def dock_forget(self, key):
        """The window was minimized or shown by the player: no longer folded."""
        self.dock_want_set(key, False)

    def dock_to_bar(self, key, title=None):
        """The "Fold into the Action Bar" button of window `key` (registered
        with dock_add): folded in now if the bar is on screen, else minimized
        until the bar comes up. Returns True when it folded in now. (2.6.85) A window
        in a zone is always up: nothing happens."""
        if LAYOUT.holds(key):
            return False
        self.dock_want_set(key, True)
        d = dict(self.docks).get(key)
        alive = self.bar_alive()
        if d is not None:
            fn = d.get("dock") if alive else (d.get("minimize") or d.get("dock"))
            if fn:
                safe(fn)
            title = title or d.get("title")
        if not alive:
            self.dock_note(title or key)
        self.dock_next = 0.0
        return alive

    def dock_note(self, title):
        API.SysMsg("%s: the Action Bar isn't open, so the window is minimized for now; it "
                   "folds into the bar once the bar is up." % title, Kit.HUE_INFO)

    def dock_add(self, key, hooks):
        self.dock_remove(key)
        self.docks.append((key, hooks))
        cur = self.current()
        if cur is not None:                   # which module (and part) the window belongs to
            self.dock_owner[key] = (cur.key, self.cur_part if cur.parts else None)
        gump = hooks.get("gump") if hasattr(hooks, "get") else None
        if gump is not None:                  # (2.6.54) the layout can slot it in a zone
            self.layout_add(key, gump, hooks.get("title"), hooks)

    def dock_remove(self, key):
        self.docks = [d for d in self.docks if d[0] != key]
        self.dock_owner.pop(key, None)
        self.layout_remove(key)

    # ---------- windows the layout can slot in a zone (2.6.54, see Layout) ----------
    #  A window registered with dock_add whose hooks offer "gump" (Kit.dock_hooks
    #  does) is listed by itself. A window with no tray button (a frame, the
    #  Action Bar) lists itself with layout_add(key, lambda: <its gump>, title,
    #  hooks), hooks (optional) a dict with "fit" / "exact" / "fill" / "redraw" /
    #  "state" as Kit.dock_hooks explains, for the zone fill. The window is
    #  listed under the module (and part) whose code calls, so its settings
    #  page can offer its zone.
    def layout_add(self, key, get_gump, title=None, hooks=None):
        cur = self.current()
        owner = None
        if cur is not None:
            owner = (cur.key, self.cur_part if cur.parts else None)
        LAYOUT.add(key, get_gump, title, hooks, owner)

    def layout_remove(self, key):
        LAYOUT.remove(key)

    def layout_slot(self, key):
        """(2.6.64) The size (w, h) the layout wants window `key` to be while it
        sits in a zone (the slot, less the room of windows attached to it), or
        None when it is free or not placed yet. For a module that checks its
        own fit (a told fit that went astray is put right on its next look)."""
        key = str(key)
        if not LAYOUT.holds(key):
            return None
        rec = LAYOUT.fitted.get(key)
        if rec is not None and rec.get("told") is not None:
            return rec["told"]
        slot = LAYOUT.placed.get(key)
        return (slot[2], slot[3]) if slot is not None else None

    def layout_rect(self, key):
        """(2.6.69) (x, y, w, h) of the slot window `key` has in its zone, or
        None when it is free or not placed yet: where a module that makes its
        window anew while it sits in a zone makes it."""
        key = str(key)
        if not LAYOUT.holds(key):
            return None
        slot = LAYOUT.placed.get(key)
        return tuple(slot) if slot is not None else None

    def layout_drop(self, g):
        """(2.6.64) Window g was let go where it is: slotted in the window zone
        under it, or freed when it is outside every zone (as a drag does, see
        Layout.dropped; Alt held leaves it where it is)."""
        try:
            LAYOUT.dropped(g)
        except Exception:
            pass

    def layout_holds(self, key):
        """Is window `key` slotted in a zone of the layout: its module then
        leaves its place to the layout (no anchor, mirror or line-up of its own)."""
        return LAYOUT.holds(key)

    def layout_need(self, key, w=None, h=None):
        """(2.6.85) Window `key` needs its zone at least w x h px (either may be None),
        or (both None) nothing beyond the zone as drawn."""
        LAYOUT.need(key, w, h)

    def layout_base(self, key):
        """(2.6.85) The (w, h) of window `key`'s zone as drawn, before any need, or None."""
        return LAYOUT.zone_base(key)

    def layout_locked(self, key):
        """(2.6.72) Window `key` sits in a zone and Arrange mode is off: the layout
        holds it there (CanMove False). A module that writes CanMove (or makes a
        draggable window) asks this first and leaves dragging off while True."""
        return LAYOUT.locked(key)

    def layout_arrange(self, on=None):
        """(2.6.72) Arrange mode: on, off, or (on None) the other way round. The
        Action Bar's Lock button is this while windows sit in zones."""
        LAYOUT.set_arrange((not LAYOUT.arrange) if on is None else on)

    def layout_arranging(self):
        """(2.6.72) True while Arrange mode is on."""
        return LAYOUT.arrange

    def layout_in_use(self):
        """(2.6.72) True while any window sits in a zone (so a layout lock means
        something)."""
        return bool(LAYOUT.assign)

    def layout_unified(self, key=None):
        """(2.6.72) One frame is on (with `key`: and window `key` sits in a zone):
        the window draws panels only, with no stone, opacity or frame of its own."""
        if not LAYOUT.unified:
            return False
        return True if key is None else LAYOUT.holds(key)    # 2.6.81: a zone in use

    def layout_pair(self, top_key, bottom_key):
        """(2.6.66) (top rect, bottom rect): the zone window `top_key` sits in and
        the zone flush under it for window `bottom_key`, made when missing (the
        bottom rect None when it can't be); None when `top_key` is in no zone.
        For a window drawn in two parts, one over the other (see Layout.pair_below)."""
        return LAYOUT.pair_below(top_key, bottom_key)

    def layout_refit(self):
        """(2.6.73) What a window wants of its zone changed (its "hug" answer): the
        zones are worked out again on the keeper's next pass."""
        LAYOUT.dirty = True
        LAYOUT.fresh = True

    def bar_alive(self):
        """The Action Bar is on screen (its heartbeat is fresh)."""
        try:
            alive = float(API.GetSharedVar(ConfigWindow.LINK_ALIVE) or 0)
        except Exception:
            alive = 0.0
        return time.time() - alive <= ConfigWindow.LINK_STALE

    def dock_tick(self):
        """Keeps folded windows and the bar in step (every 0.25 s; the bar's
        heartbeat is read only when something waits on it):
          - a window folded in (by any route) is wished folded;
          - a window shown again drops the wish;
          - the bar went away: folded windows come back minimized, wish kept;
          - the bar is up: minimized windows that are wished folded fold in.
        A window that is simply minimized stays as it is."""
        now = time.time()
        if now < self.dock_next and self.dock_next - now <= 0.25:   # (2.6.84: or the clock went back)
            return
        self.dock_next = now + 0.25
        Binds.load()
        Binds.tick()
        want = self._dock_want()
        fold, unfold = [], []
        self.zone_up_tick()
        for k, d in self.docks:
            if LAYOUT.holds(k):                   # (2.6.85) always up; its wish stays as it was
                continue
            try:
                s = d["state"]()
            except Exception:
                s = None
            if s == "docked":
                if k not in want:
                    self.dock_want_set(k, True)
                unfold.append(d)
            elif s == "open":
                if k in want:
                    self.dock_want_set(k, False)
            elif s == "minimized" and k in want:
                fold.append(d)
        if not fold and not unfold:
            return
        if self.bar_alive():
            for d in fold:
                safe(d.get("dock"))
        else:
            for d in unfold:
                safe(d.get("undock"))

    ZONE_WAS_VAR = "Layout_zone_was"          # per character: "key=m,key=d": how each was left

    def _zone_was(self):
        d = getattr(self, "_zone_was_d", None)
        if d is None:
            d = {}
            for part in str(Kit.get_var(self.ZONE_WAS_VAR, "") or "").split(","):
                if "=" in part:
                    k, v = part.split("=", 1)
                    d[k] = v
            self._zone_was_d = d
        return d

    def _zone_was_save(self):
        Kit.put_var(self.ZONE_WAS_VAR, ",".join("%s=%s" % kv for kv in sorted(self._zone_was_d.items())))

    def zone_up_tick(self):
        """(2.6.85) A window in a zone is shown, open and full size all the time. One
        that is minimized or folded (put there so, started so, or a hotkey did it) comes
        up, and how it was is kept (ZONE_WAS_VAR, so the module's own saved value may
        say up meanwhile); taken out of the zone it goes back to that, and its title row
        is drawn again either way. Every dock_tick (0.25 s): a dict look per window."""
        held = getattr(self, "_zone_held", None)
        if held is None:
            held = self._zone_held = set()
        was = self._zone_was()
        for k, d in self.docks:
            on = LAYOUT.holds(k)
            changed = on != (k in held)
            if changed:
                if on:
                    held.add(k)
                else:
                    held.discard(k)
            try:
                s = d["state"]() if (on or k in was) else None
            except Exception:
                s = None
            if on and s in ("minimized", "docked"):
                if k not in was:
                    was[k] = "d" if (s == "docked" or self.dock_wanted(k)) else "m"
                    self._zone_was_save()
                safe(d.get("show"))
                continue
            if not on and k in was and s is not None:
                v = was.pop(k)
                self._zone_was_save()
                if v == "d":
                    self.dock_to_bar(k, d.get("title"))
                else:
                    safe(d.get("minimize"))
                continue
            if changed and d.get("redraw") is not None and s != "docked":
                safe(d.get("redraw"))

    # ---------- modules ----------
    def add(self, key, title, desc, factory, interval, default_on=False, category=None,
            parts=(), aliases=()):
        s = dict.get(self.by_key, key)
        if s is not None and s.lazy is not None:    # its file is being loaded now
            s.lazy = None
            s.title, s.desc, s.factory, s.interval = title, desc, factory, interval
            s.default_on = bool(default_on)
            s.category = str(category or "Other")
            self._note_parts(s, parts, aliases)
        elif s is not None:                 # two module files with the same key
            API.SysMsg("%s: %s was loaded twice (module key \"%s\"); the second copy "
                       "was skipped." % (APP_NAME, title, key), Kit.HUE_BAD)
            return s
        else:
            s = ModuleSlot(key, title, desc, factory, interval)
            s.default_on = bool(default_on)
            s.category = str(category or "Other")
            self._note_parts(s, parts, aliases)
            self.slots.append(s)
            self.by_key[key] = s
        try:
            s.api = factory()
        except Exception as ex:
            s.broken = str(ex) + _error_where()
            API.SysMsg("%s: %s could not be loaded: %s" % (APP_NAME, title, s.broken),
                       Kit.HUE_BAD)
        self._arm(s)
        return s

    @staticmethod
    def _arm(s):
        """Read once what the scheduler asks of a module on every pass."""
        api = s.api
        s.on_client = bool(api and api.get("client_tick"))
        # (2.6.82) the per-tick dict probes, once here instead of on every tick
        s.iv_fn = api.get("interval") if api else None
        s.has_thread = bool(api) and "thread_tick" in api
        s.thread_want = api.get("thread_wanted") if api else None

    def add_lazy(self, key, title, desc, path, interval, default_on=False, category=None,
                 parts=(), aliases=()):
        """List a module from its registration line; its file is compiled the
        first time it is turned on or its settings page is opened."""
        if dict.__contains__(self.by_key, key):
            return dict.__getitem__(self.by_key, key)
        s = ModuleSlot(key, title, desc, None, interval)
        s.default_on = bool(default_on)
        s.category = str(category or "Other")
        self._note_parts(s, parts, aliases)
        s.lazy = path
        self.slots.append(s)
        self.by_key[key] = s
        return s

    def request_load(self, s):
        """Have a lazily listed module's file compiled on the script's thread,
        outside the client hop (run_due does it on the next pass; a whole
        module file compiled inside the hop was one visible frame hitch when
        a box was ticked or a settings page opened). A module that is enabled
        is started once its file is in. True when the load was put off."""
        if s is None or s.lazy is None:
            return False
        if s not in self.load_jobs:
            self.load_jobs.append(s)
        self.poke()
        return True

    def _run_load_jobs(self):
        """Script thread, between passes: compile one waiting module file and
        start the module if it is wanted on; tell the settings window."""
        if not self.load_jobs or self.stack:
            return
        s = self.load_jobs.pop(0)
        ok = self.load(s)
        if ok and s.enabled and not s.running and not s.pending_stop:
            self.start(s)
        elif not ok and s.enabled:
            # the file couldn't be compiled: not on, as when enable() loads it
            # itself (its box unticks itself, and it isn't saved as on)
            s.enabled = False
            self.save_prefs()
        if self.config is not None:
            self.config.loaded(s.key)

    def load(self, s):
        """Make sure a module's code is loaded. False if it isn't usable."""
        if s is None:
            return False
        if s.lazy is not None:
            path = s.lazy
            t0 = time.time()
            try:
                code = compile(_read_text(path), path, "exec")
                exec(code, globals())          # calls HOST.add, which fills this slot
                if s.lazy is not None:         # the file never registered itself
                    raise Exception("the file's HOST.add line didn't run")
            except Exception as ex:
                s.lazy = None
                line = getattr(ex, "lineno", None)       # a syntax error knows its line
                where = (" (%s line %s)" % (os.path.basename(path), line)) if line \
                    else _error_where()
                s.api, s.broken = None, "%s%s" % (getattr(ex, "msg", None) or ex, where)
                API.SysMsg("%s: %s could not be loaded: %s" % (APP_NAME, s.title, s.broken),
                           Kit.HUE_BAD)
            if self.debug:
                safe(lambda: API.SysMsg("%s: loaded %s in %d ms." % (
                    APP_NAME, os.path.basename(path), (time.time() - t0) * 1000), Kit.HUE_INFO))
        return s.api is not None

    def current(self):
        return self.stack[-1] if self.stack else None

    def stopping(self):
        if self.quitting:
            return True
        try:
            return bool(API.StopRequested)
        except Exception:
            return True

    def aborting(self):
        """True when the module that is running should stop what it's doing."""
        if self.stopping():
            return True
        if self.client_idles > 1 and Client.on_client_thread():
            return True                      # a wait loop on the client thread: let go (see idle)
        s = self.current()
        return s is not None and (s.pending_stop or not s.enabled)

    def idle(self, seconds):
        """Wait while everything else keeps running. Returns False if the
        calling module should give up (it was switched off or the script is
        stopping)."""
        if Client.on_client_thread():         # a wait here would freeze the client
            s = self.current()
            if s is not None and not s.idle_told and self.debug:
                s.idle_told = True
                safe(lambda: API.SysMsg("%s: %s asked to wait on the client thread; the wait "
                                        "was skipped (move it to its thread_tick)."
                                        % (APP_NAME, s.title), Kit.HUE_INFO))
            # Nothing in the game moves while we hold the client thread, so a
            # `while ... HOST.idle(x)` loop here would spin (a frozen game) until
            # its deadline: one skipped wait is let through, a second one in the
            # same hop says "give up".
            self.client_idles += 1
            return self.client_idles <= 1 and not self.aborting()
        end = time.time() + max(0.0, seconds)
        while not API.StopRequested:
            if self.aborting():
                return False
            safe(API.ProcessCallbacks)
            self.run_due()
            if self.aborting():
                return False
            rem = end - time.time()
            if rem <= 0 or rem > seconds + 1.0:      # done (or the clock was set back)
                return True
            API.Pause(min(HOST_TICK, rem))
        return False

    def _enter(self, s):
        s.busy = True
        self.stack.append(s)

    def _leave(self, s):
        stack = self.stack
        if stack and stack[-1] is s:
            stack.pop()
        elif s in stack:
            stack.remove(s)
        s.busy = False

    def report(self, s, ex, what=None, part=None):
        msg = str(ex) + _error_where()
        s.error_count += 1
        if msg not in s.errors:
            s.errors.add(msg)
            safe(lambda: API.SysMsg("%s: %s error (still running): %s"
                                    % (APP_NAME, what or s.title, msg), Kit.HUE_BAD))
        if s.error_count >= MAX_MODULE_ERRORS and s.enabled:
            safe(lambda: API.SysMsg("%s: %s kept failing and was switched off."
                                    % (APP_NAME, what or s.title), Kit.HUE_BAD))
            if part is not None and s.parts and s.parts_on.get(part):
                # (2.6.84) a part's error from outside its tick (its settings page,
                # its hub section): that part, not the whole module
                self.part_set(s.key, part, False)
            else:
                self.disable(s.key)
            # (2.6.71) inside a part only that part goes off: its errors are not
            # held against the module's other parts
            if s.enabled:
                s.error_count = 0

    def start(self, s):
        if s.running or self.stopping() or not self.load(s):
            return
        if self.config is not None:
            self.config.forget_measure(s.key)    # its page may show more while it runs
        s.errors, s.error_count = set(), 0
        s.pending_stop = False
        self._enter(s)
        try:
            s.running = True
            self._arm(s)
            self._refresh_active()
            t0 = time.time()
            # start() builds the module's windows: one hop to the client thread
            # makes that a few milliseconds instead of one round trip per control
            self.client_idles = 0
            Kit.on_client(s.api["start"])
            if self.debug:
                safe(lambda: API.SysMsg("%s: %s started in %d ms." % (
                    APP_NAME, s.title, (time.time() - t0) * 1000), Kit.HUE_INFO))
        except Exception as ex:
            s.running = False
            msg = str(ex) + _error_where()
            safe(lambda: API.SysMsg("%s: %s could not start: %s" % (APP_NAME, s.title, msg),
                                    Kit.HUE_BAD))
            safe(lambda: s.api["stop"]())
            s.enabled = False
            self.save_prefs()
        finally:
            self._leave(s)
            self._refresh_active()
        s.next_due = 0.0

    def _stop(self, s):
        s.pending_stop = False
        if not s.running:
            return
        if self.config is not None:
            self.config.forget_measure(s.key)
        safe(lambda: Picker.drop(s.key))
        if self.cursor_claim[0] == s.key:
            self.cursor_claim = (None, 0.0)
        for p in s.parts:
            safe(lambda: Picker.drop(p[0]))
            for old in p[4]:
                safe(lambda: Picker.drop(old))
                if self.cursor_claim[0] == old:
                    self.cursor_claim = (None, 0.0)
        self._enter(s)
        try:
            s.api["stop"]()
        except Exception:
            pass
        finally:
            s.running = False
            self._leave(s)
            self._refresh_active()

    SLOW_MS = 250             # a tick this long is named in the journal (once per module)

    def tick(self, s, hook="tick"):
        """One tick (or thread_tick) of a module, with its bookkeeping: the
        running stack, error reports, the slowest-tick figure and when it is
        due next. Kept lean: it runs for every module on every pass."""
        s.busy = True
        stack = self.stack
        stack.append(s)
        self.client_idles = 0
        t0 = time.time()
        try:
            s.api[hook]()
        except Exception as ex:
            if not self.stopping():
                self.report(s, ex)
        finally:
            if stack and stack[-1] is s:
                stack.pop()
            elif s in stack:
                stack.remove(s)
            s.busy = False
            t1 = time.time()
            ms = (t1 - t0) * 1000.0
            decayed = s.worst_ms * 0.98
            s.worst_ms = ms if ms > decayed else decayed
            if ms >= self.SLOW_MS and self.debug and not s.slow_told and not self.stopping():
                s.slow_told = True
                safe(lambda: API.SysMsg("%s: a %s tick took %d ms; that is the lag you feel "
                                        "(the Modules tab shows the slowest module)."
                                        % (APP_NAME, s.title, ms), Kit.HUE_INFO))
        if hook == "tick":
            step = s.interval
            nxt = s.iv_fn
            if nxt is not None:
                try:
                    step = nxt() or s.interval
                except Exception:
                    step = s.interval
            s.next_due = t1 + step
            # (2.6.82) a thread pass only when the module has thread work: a
            # "thread_wanted" hook says so; without one, after every tick as before
            if s.has_thread:
                want = s.thread_want
                if want is None:
                    s.thread_due = True
                else:
                    try:
                        s.thread_due = bool(want())
                    except Exception:
                        s.thread_due = True
            else:
                s.thread_due = False
        if s.pending_stop:
            self._stop(s)

    def enable(self, key):
        s, part = self.resolve(key)
        if s is None:
            return
        if part is not None:                  # an old module key, or "<module>.<part>"
            self.part_set(s.key, part, True)
            return
        if s.parts and not s.parts_wanted():  # turned on with no part ticked: its defaults
            for p in self._parts_default(s):
                s.parts_on[p] = True
        if s.lazy is not None and Client.on_client_thread():
            # a box ticked, a bar button: compile the file off this thread and
            # start the module on the pass after (request_load)
            s.enabled = True
            self.save_prefs()
            self.request_load(s)
            return
        if not self.load(s):
            return
        s.enabled = True
        if s.running and s.pending_stop:      # (2.6.71) ticked again before its stop ran
            s.pending_stop = False
        self.save_prefs()
        self.start(s)

    def show_settings(self, key):
        """Open the Virtue Assistant window on this module's settings."""
        if self.config is not None:
            self.config.show_settings(key)

    def refresh_settings(self, key):
        """Redraw a module's settings page if it is showing. key may be a part's
        2.6.06 module key or "<module>.<part>": the page is the module's (2.6.51:
        in 2.6.5 a part's key matched no page, so nothing was redrawn)."""
        if self.config is not None:
            s, _part = self.resolve(key)
            self.config.refresh(s.key if s is not None else key)

    def disable(self, key):
        """Turn a module off (or one part of it, by the part's old module key or
        "<module>.<part>"). Safe to call from the module's own code: the module
        (or the part) is stopped as soon as it returns."""
        s, part = self.resolve(key)
        if s is None:
            return
        if self.shut or self.stopping():
            # the script is stopping and its windows are going away: that
            # must not switch modules off for the next start
            return
        if part is None and s.parts and self.cur_part is not None and self.current() is s \
                and s.parts_on.get(self.cur_part):
            # a part closing its own window turns itself off (2.6.71: only while it
            # is still on; part_set unticking the last part turns the module off
            # from inside that part, and that must reach the module)
            part = self.cur_part
        if part is not None:
            self.part_set(s.key, part, False)
            return
        s.enabled = False
        self.save_prefs()
        if s.running:
            s.pending_stop = True
            if not s.busy:
                self._stop(s)

    def run_due(self):
        """One pass: a hop to the client thread for the windows and every
        client_tick module that is due (skipped when nothing there is due),
        then, on this thread, the modules' thread work."""
        if self.profile_req is not None and not self.stack:
            # only between module passes, never inside one module's wait
            req, self.profile_req = self.profile_req, None
            self.profile_job(req)
            return
        if self.load_jobs and not self.stack:
            self._run_load_jobs()                # a module file to compile: here, not in the hop
        poked, self.poked = self.poked, False
        self.pass_id += 1
        if poked:                                # a click: everything gets a pass now
            self.ui_next = 0.0
        now = time.time()
        # one hop: the windows, target cursors and every client_tick module.
        # A hop costs a frame of waiting, so it is made only when something on
        # the client thread is due (or a click poked us).
        if poked or self._client_due(now):
            self.pass_poked = poked
            try:
                Kit.on_client(self._pass_fn)
            except Exception as ex:
                if not self.stopping():
                    self._tell("%s: pass error: %s" % (APP_NAME, ex))
            now = time.time()
        if Picker.jobs:
            Picker.run_blocking()                # only on builds without client access
        # then, on this thread, the modules that may wait
        for s in self.active:                    # (a list rebuilt, never changed in place)
            if s.pending_stop:
                if s.busy:
                    continue
                self._stop(s)
            elif s.busy or not s.running:
                continue
            elif not s.on_client and (poked or now >= s.next_due
                                      or s.next_due - now > self.CLOCK_BACK):
                self.tick(s)
            elif s.thread_due:
                s.thread_due = False
                self.tick(s, "thread_tick")
            else:
                continue
            if self.stopping():
                return
            try:
                API.ProcessCallbacks()           # hotkeys don't wait for the whole pass
            except Exception:
                pass
        cfg = self.config
        if cfg is not None and cfg.prof_stale and not self.stack:
            cfg.refresh_profiles()               # file reads: here, never on the client thread

    #  A module due before the hop after next could start lands is due now: the
    #  hop lands on the client's next frame, and skipping it would push the
    #  module's tick a whole pass later (its rate would drop). So modules keep
    #  the cadence they had when every pass made a hop; only the windows' own
    #  polling (20 a second, not timing-critical) waits for its due time.
    LOOKAHEAD = HOST_TICK + 0.035
    CLOCK_BACK = 60.0         # a module due further ahead than this: the clock was set back

    def _client_due(self, now):
        """Is anything on the client thread due this pass?"""
        if now >= self.ui_next or Kit.pending or Picker.jobs:
            return True
        if self.ui_next - now > 1.0:             # the clock was set back: due now
            self.ui_next = now
            return True
        soon = now + self.LOOKAHEAD
        for s in self.client_run:
            if soon >= s.next_due:
                return True
            if s.next_due - now > self.CLOCK_BACK:
                s.next_due = now                 # the clock was set back: due now
                return True
        return False

    def _client_pass(self, poked=None):
        """Everything that can't wait, in one hop to the client thread."""
        self.in_hop = True                       # (2.6.82) the per-pass caches may keep values
        try:
            self._client_pass_body(poked)
        finally:
            self.in_hop = False

    def _client_pass_body(self, poked):
        if poked is None:
            poked = self.pass_poked
        self.client_idles = 0
        if Kit._texts_sweep:
            Kit._prune_texts()                   # a sweep put off from the script thread
        self.ui_tick()
        if Picker.jobs:
            try:
                Picker.tick()
            except Exception as ex:              # never let it hold up the modules
                self._tell("%s: target cursor error: %s" % (APP_NAME, ex))
        now = time.time()
        for s in self.client_run:
            # (due further ahead than CLOCK_BACK: the clock was set back, due now;
            # _client_due's own check stops at the first module that is due)
            if s.running and not s.busy and not s.pending_stop and (
                    poked or now >= s.next_due or s.next_due - now > self.CLOCK_BACK):
                self.tick(s)
                if self.stopping():
                    return

    # ---------- sharing the target cursor ----------
    #  One cursor, many modules. A module that is about to raise a cursor it
    #  will answer by itself (a bandage on you, a spell on a friend) claims it
    #  for the few seconds that takes; the others leave the cursor alone (no
    #  aiming, no cancelling) while someone else's claim or pick is running.
    def claim_cursor(self, key, seconds):
        self._claim_len = max(0.0, seconds)            # (set first: read with the claim)
        self.cursor_claim = (key, time.time() + self._claim_len)

    def release_cursor(self, key):
        if self.cursor_claim[0] == key:
            self.cursor_claim = (None, 0.0)

    def cursor_busy(self, key=None):
        """Who else has the target cursor spoken for (a module key, "pick" for
        a HOST.pick_target cursor), or None."""
        if Picker.jobs:
            return "pick"
        owner, until = self.cursor_claim
        # (2.6.84) a claim never lasts longer than it was made for (the clock set back)
        return owner if owner is not None and owner != key and \
            0 < until - time.time() <= self._claim_len + 0.05 else None

    def cursor_ok(self, key, kind="any"):
        """True when a target cursor of `kind` ("any", "beneficial", "harmful",
        "neutral": the kind the module's own action raises) is up and nobody
        else has the cursor spoken for: the one test before a module aims a
        cursor by itself (2.6.81), so a cursor of another kind (the player's
        own harmful spell, another module's) is never aimed. A module may aim
        only a cursor its own press raised; this narrows it to the right kind."""
        if self.cursor_busy(key) is not None:
            return False
        try:
            return bool(API.HasTarget(kind))
        except Exception:
            return False

    # ---------- the shared holds of loops that act by themselves (2.6.81) ----------
    #  Skill Bags, Property Butler's sweep and Bags' Trap / Untrap run all ask
    #  these, so they agree on what a fight is and on an unknown guard zone
    #  (the shard's rules, R3; the strict reading: an unknown zone holds).
    def guard_hold(self):
        """"guard" inside a guard zone, "unknown" while the zone isn't known yet
        (no guard line seen and no saved state for this spot), else None."""
        try:
            g = GUARD.guarded()
        except Exception:
            g = None
        if g is True:
            return "guard"
        if g is None:
            return "unknown"
        return None

    def foe_near(self):
        """The name of a hostile within FOE_RANGE, or None: notoriety enemy or
        murderer, or grey / criminal while that mobile is in war mode; you and your own pets
        and summons (renamable) are skipped, party members are not (a red is a
        red). One look every FOE_EVERY s, shared by every caller."""
        now = time.time()
        at, name = self.foe_seen
        if 0 <= at - now <= FOE_EVERY:
            return name

        def look():
            found = None
            try:
                me = int(self.me().Serial)      # (2.6.82) the shared reads of the pass
            except Exception:
                me = 0
            try:
                for m in self.mobiles(FOE_RANGE):
                    try:
                        if int(m.Serial) == me or m.IsRenamable:
                            continue
                        n = int(m.Notoriety)
                        if n in FOE_NOTO or (n in FOE_WAR_NOTO and m.InWarMode):
                            found = str(m.Name or "") or "?"
                            break
                    except Exception:
                        continue
            except Exception:
                pass
            return found

        try:
            name = look() if Client.on_client_thread() else Kit.on_client(look)
        except Exception:
            name = None
        self.foe_seen = (now + FOE_EVERY, name)
        return name

    def fight_hold(self, now=None):
        """Why a loop that acts by itself must wait right now, or None: "dead",
        "war" (war mode), "hurt" (your HP dropped in the last HURT_SECS),
        "foe" (foe_near), "item" (you hold an item on the cursor) or "alarm"
        (an alarm waits for you: HOST.services["attention.up"]). HOLD_TEXT has
        the words for each. Call it from the client tick (each read is free there)."""
        if now is None:
            now = time.time()
        dead = war = False
        try:
            p = self.me()                        # (2.6.82) read once per pass for every loop
            dead = bool(p.IsDead)
            war = bool(p.InWarMode)
            hits = int(p.Hits)
        except Exception:
            hits = None
        if hits is not None:
            # a drop counts only against a reading from the last HURT_FRESH s: an
            # old one (no loop asked for a while) is no sign of a fight now
            if (self.hurt_hp is not None and hits < self.hurt_hp
                    and 0 <= now - self.hurt_at <= HURT_FRESH):
                self.hurt_until = now + HURT_SECS
            self.hurt_hp = hits
            self.hurt_at = now
        if dead:
            return "dead"
        if war:
            return "war"
        if 0 < self.hurt_until - now <= HURT_SECS:
            return "hurt"
        if self.foe_near():
            return "foe"
        try:
            h = API.GetHeldItem()
            if h is not None:
                try:
                    hs = h.Serial                # (2.6.82) the plain read; getattr only if absent
                except AttributeError:
                    hs = h
                if int(hs or 0):
                    return "item"
        except Exception:
            pass
        up = self.services.get("attention.up")
        if up is not None:
            try:
                if up():
                    return "alarm"
            except Exception:
                pass
        return None

    # ---------- the shared reads of every module (2.6.82) ----------
    #  Each module used to read the same game state on its own: the player (85
    #  places), the mobiles around you (a dozen scans), the same FindMobile
    #  serials and the backpack. These read once per pass and hand every caller
    #  the same answer, inside the client hop only (anywhere else they read live).
    def me(self):
        """The player for this pass: a _Memo of API.Player (each property read
        from the client once per pass; .raw is API.Player itself), or None."""
        if self.in_hop and self._me_pid == self.pass_id:
            return self._me
        try:
            p = API.Player
        except Exception:
            p = None
        m = _Memo(p) if p is not None else None
        if self.in_hop:
            self._me_pid = self.pass_id
            self._me = m
        return m

    def _mob_scan(self):
        """((distance, _Memo), ...) of every mobile the client knows, nearest
        first: one API.GetAllMobiles() per pass (live outside the hop)."""
        if self.in_hop and self._mob_pid == self.pass_id:
            return self._mob_list
        out = []
        byser = None
        if self.in_hop:
            if self._one_pid != self.pass_id:
                self._one = {}
                self._one_pid = self.pass_id
            byser = self._one
        try:
            raw = API.GetAllMobiles() or ()
        except Exception:
            raw = ()
        for r in raw:
            try:
                d = r.Distance
                m = _Memo(r)
                m.__dict__["Distance"] = d
                out.append((d, m))
                if byser is not None:
                    byser[int(r.Serial)] = m
            except Exception:
                continue
        out.sort(key=_first)                 # (2.6.83) nearest first, as promised (stable)
        if self.in_hop:
            self._mob_pid = self.pass_id
            self._mob_list = out
        return out

    def mobiles(self, distance=None):
        """The mobiles within `distance` tiles (all with None), nearest first,
        as _Memo wrappers (.raw: the ApiMobile): what API.GetAllMobiles(distance=d)
        gives, from one scan per pass. A new list on every call."""
        lst = self._mob_scan()
        if distance is None:
            return [e[1] for e in lst]
        out = []
        for d, m in lst:
            if d <= distance:
                out.append(m)
        return out

    def mobile(self, serial):
        """API.FindMobile(serial) for this pass: a _Memo or None."""
        try:
            k = int(serial)
        except Exception:
            return None
        if self.in_hop:
            if self._one_pid != self.pass_id:
                self._one = {}
                self._one_pid = self.pass_id
            one = self._one
            if k in one:
                return one[k]
        try:
            r = API.FindMobile(k)
        except Exception:
            r = None
        m = _Memo(r) if r is not None else None
        if self.in_hop:
            self._one[k] = m
        return m

    def pack_items(self, deep=True, max_age=0.0):
        """list(API.ItemsInContainer(API.Backpack, deep)): the same list for
        every caller in a pass, or one taken within `max_age` seconds. A copy
        on every call; the items' own reads stay live. Raises when the client
        can't list the pack (as API.ItemsInContainer does)."""
        k = bool(deep)
        now = time.time()
        ent = self._pack.get(k)
        if ent is not None and ((self.in_hop and ent[0] == self.pass_id)
                                or (max_age > 0 and 0 <= now - ent[1] <= max_age)):
            return list(ent[2])
        bp = API.Backpack
        # a pack that can't be read raises, as the API itself does (callers keep
        # what they showed before rather than count an empty pack); not kept
        lst = list(API.ItemsInContainer(bp, k) or []) if bp else []
        self._pack[k] = (self.pass_id if self.in_hop else -1, now, lst)
        return list(lst)

    def pack_dirty(self):
        """An item moved in or out of the backpack: the next pack_items reads again."""
        self._pack.clear()

    def pick_target(self, timeout, on_done, owner=None):
        """Put up a target cursor without holding anything up; on_done(serial)
        runs on a later pass once the player targets something (0 if they
        cancel, it times out or another cursor replaces it). Treat on_done like
        a click handler: queue the work, don't wait in it. `owner` is the
        asking module's KEY: pass it when calling from a click handler or a
        dock hook (no module is "running" there), so the cursor comes down
        when that module stops; from a tick it defaults to the module running."""
        Picker.ask(timeout, on_done, owner)

    def ui_tick(self):
        if self.ui_busy or self.config is None:
            return
        self.ui_busy = True
        try:
            Kit.run_pending()                 # the client's queued events: every pass
            now = time.time()
            if now >= self.ui_next:           # the windows' own polling: 20 times a second
                self.ui_next = now + UI_TICK
                self._poll_windows()          # on the client thread: no waits inside
                self.dock_tick()
                SNAP.tick()
                if self.grid is not None:
                    self.grid.tick()
                LAYOUT.poll()                 # the zone editor's controls, while it is up
                self._services_tick(now)
        except Exception as ex:
            msg = "%s: settings window error: %s%s" % (APP_NAME, ex, _error_where())
            if not self.stopping():
                self._tell(msg)
        finally:
            self.ui_busy = False

    def _services_tick(self, now):
        """The alert banner, the guard-zone lines and the What's new window
        (each on its own: a fault in one never holds up the others)."""
        try:
            ALERTS.tick(now)
        except Exception as ex:
            self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
        try:
            GUARD.tick(now)
        except Exception as ex:
            self._tell("%s: guard-zone error: %s%s" % (APP_NAME, ex, _error_where()))
        if self.whats_new.g is not None:
            try:
                self.whats_new.poll()
            except Exception:
                pass

    def _poll_windows(self):
        self.config.poll()
        if self.hub is not None:
            self.hub.poll()

    # ---------- saved choices ----------
    def load_prefs(self):
        prefs = {}
        for part in Kit.get_var(SETTINGS_KEY).split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                prefs[k.strip()] = v.strip()
        self.prefs = prefs
        on = [k for k in prefs.get("modules", "").split(",") if k]
        # a module registered with default_on is on the first time this
        # character meets it; "seen" remembers which, so unticking it sticks
        seen = set(k for k in prefs.get("seen", "").split(",") if k)
        was = prefs.get("seen", "")
        # (2.6.5) which parts are on: carried over from the 2.6.06 module keys in
        # modules= on the first start (and again whenever an older version saved
        # modules= in between: parts_from= is what this version wrote last)
        changed = self._migrate_parts(prefs, on, seen)
        for s in self.slots:
            if s.default_on and s.key not in seen:
                on.append(s.key)
                seen.add(s.key)
                if s.parts and not s.parts_wanted():
                    for p in self._parts_default(s):
                        s.parts_on[p] = True
        prefs["seen"] = ",".join(sorted(seen))
        for s in self.slots:
            s.enabled = s.key in on and (s.api is not None or s.lazy is not None)
            if s.parts and s.enabled and not s.parts_wanted():
                for p in self._parts_default(s):
                    s.parts_on[p] = True
        if prefs["seen"] != was or changed:
            # kept now, not at the next save: a crash before any save would
            # otherwise turn a default-on module the player unticked back on
            self.save_prefs()

    def _migrate_parts(self, prefs, on, seen):
        """Fill every module's parts_on from the saved parts= (and, when that is
        missing or an older version saved modules= since, from the 2.6.06 module
        keys in modules=). `on` gains the key of every module with a part on.
        Returns True when something had to be worked out (save it now)."""
        saved = {}
        for item in prefs.get("parts", "").split(","):
            if "." in item:
                mk, pk = item.split(".", 1)
                saved.setdefault(mk, set()).add(pk)
        # 2.6.81: parts_off= the part choices of modules that are off (older
        # versions ignore the key, so they never turn such a module on)
        saved_off = {}
        for item in prefs.get("parts_off", "").split(","):
            if "." in item:
                mk, pk = item.split(".", 1)
                saved_off.setdefault(mk, set()).add(pk)
        fresh = "parts" not in prefs or prefs.get("parts_from", "") != prefs.get("modules", "")
        on_set = set(on)
        changed = False
        for s in self.slots:
            if not s.parts:
                continue
            mine = saved.get(s.key)
            off = saved_off.get(s.key)
            if mine is None and off is not None and s.key not in on_set \
                    and not any(k in on_set for p in s.parts for k in p[4]):
                for p in s.parts:                # off, with its parts remembered
                    s.parts_on[p[0]] = p[0] in off
                continue
            if mine is not None and not fresh:
                for p in s.parts:
                    s.parts_on[p[0]] = p[0] in mine
                    # (2.6.85) a part marked new (6th field) that this save has never met:
                    # its "on at first" value, once (Inventory > Supplies was part of Frames)
                    if len(p) > 5 and p[5] and p[0] not in mine and p[3]:
                        seen = str(Kit.get_var("VirtueAssistant_new_parts", "") or "").split(",")
                        if p[0] not in seen:
                            Kit.put_var("VirtueAssistant_new_parts", ",".join([x for x in seen if x] + [p[0]]))
                            s.parts_on[p[0]] = True
                            changed = True
            else:
                # from the old keys: a part is on if any module it replaces was on;
                # a part with nothing to replace keeps its saved choice if there is
                # one, else starts at its "on at first" value only on a character
                # that had none of this module's old modules on
                olds = [k for p in s.parts for k in p[4]]
                had_old = any(k in on_set for k in olds) or (s.key in on_set and not olds)
                for p in s.parts:
                    if p[4]:
                        s.parts_on[p[0]] = any(k in on_set for k in p[4])
                    elif mine is not None:
                        s.parts_on[p[0]] = p[0] in mine
                    else:
                        s.parts_on[p[0]] = bool(p[3]) and not had_old and s.key not in on_set
                if s.key in on_set and not s.parts_wanted():
                    for p in self._parts_default(s):   # a 2.6.5 key with no part listed
                        s.parts_on[p] = True
                changed = True
                # a replaced module this character had already met: so has this one
                # (a default-on module they unticked must not come back on)
                if any(k in seen for k in olds) and s.key not in seen:
                    seen.add(s.key)
            if s.parts_wanted():
                if s.key not in on_set:
                    on.append(s.key)
                    on_set.add(s.key)
            elif s.key in on_set:
                on.remove(s.key)
                on_set.discard(s.key)
        return changed

    def pref_int(self, key, default):
        try:
            return int(self.prefs.get(key, default))
        except Exception:
            return default

    def save_prefs(self):
        """Save the window's choices; returns what was saved (None while a
        profile is being loaded, when the old choices must not be written)."""
        if self.config is not None:
            self.config.box_hit = True        # a module may have been switched: tick its box now
        if self.prefs_frozen:
            return None
        # modules=: the keys that are on, and (2.6.5) the 2.6.06 key of every part
        # that is on, so an older version still starts the same things; parts=
        # the parts that are on; parts_from= what modules= was when parts= was
        # written (load_prefs works the parts out again when they differ)
        mods, parts, off = [], [], []
        for s in self.slots:
            if not s.enabled:
                # 2.6.81: an off module's part choices, kept for when it is ticked again
                for p in s.parts:
                    if s.parts_on.get(p[0]):
                        off.append("%s.%s" % (s.key, p[0]))
                continue
            mods.append(s.key)
            for p in s.parts:
                if s.parts_on.get(p[0]):
                    parts.append("%s.%s" % (s.key, p[0]))
                    for old in p[4]:
                        if old not in mods:
                            mods.append(old)
        self.prefs["modules"] = ",".join(mods)
        self.prefs["parts"] = ",".join(parts)
        self.prefs["parts_from"] = self.prefs["modules"]
        if off:
            self.prefs["parts_off"] = ",".join(off)
        else:
            self.prefs.pop("parts_off", None)
        if self.config is not None:
            self.config.store_prefs(self.prefs)
        if self.hub is not None:
            self.hub.store_prefs(self.prefs)
        data = ";".join("%s=%s" % (k, v) for k, v in sorted(self.prefs.items()))
        Kit.put_var(SETTINGS_KEY, data)
        return data

    # ---------- profiles (see Profiles) ----------
    def profile_job(self, req):
        kind, name = req
        try:
            if kind == "save":
                self._profile_save(name)
            elif kind == "load":
                self._profile_load(name)
            elif kind == "fav":
                self._profile_fav(name)
        except Exception as ex:
            safe(lambda: API.SysMsg("%s: profile %s failed: %s%s"
                                    % (APP_NAME, kind, Tz.why(ex), _error_where()),
                                    Kit.HUE_BAD))
        if kind != "load" and self.config is not None and not self.stopping():
            self.config.refresh_profiles()       # what the job changed on disk
            if self.config.mode == "full":
                self.config.prof_redraw = False
                self.config.redraw()             # the list, the star (a load rebuilt it)

    def _profile_save(self, name):
        name = PROFILES.clean(name)
        if not name:
            raise Exception("type a name for the profile in the box")
        API.SysMsg('%s: saving profile "%s"...' % (APP_NAME, name), Kit.HUE_INFO)
        data = self.save_prefs()
        stamp, n, saved, failed = PROFILES.save(name, data)
        fav = PROFILES.favorite()
        PROFILES.set_state("fav" if name == fav else "pick", name, stamp)
        if name == fav:
            try:
                PROFILES.set_client_default(name)
            except Exception as ex:
                failed.append("TazUO default for new characters (%s)" % Tz.why(ex))
        if self.config is not None:
            self.config.prof_sel = name
        PROFILES.report(name, "saved", n, True, saved, failed)

    def _profile_load(self, name):
        if PROFILES.info(name) is None:
            raise Exception('there is no profile "%s"' % name)
        API.SysMsg('%s: loading profile "%s"...' % (APP_NAME, name), Kit.HUE_INFO)
        self.prefs_frozen = True
        try:
            LAYOUT.close()                       # the zone editor, if it is up
            for s in self.slots:                 # each saves its own settings as it stops
                if s.running:
                    self._stop(s)
            if self.config is not None:
                safe(self.config.close)
            if self.hub is not None:
                safe(self.hub.close)
            mode = "fav" if name == PROFILES.favorite() else "pick"
            result = PROFILES.apply(name, mode)
            ALERTS.loaded = False                # the profile's alert choices
            GUARD.saved = None
            Kit.read_screen()                    # the places just applied are for the profile's screen
            LAYOUT.load()                        # the profile's layouts
            for s in self.slots:                 # loaded modules re-read their settings
                if s.api is not None and s.lazy is None and s.factory is not None:
                    try:
                        s.api = s.factory()
                        s.broken = None
                    except Exception as ex:
                        s.api, s.broken = None, str(ex) + _error_where()
                        API.SysMsg("%s: %s could not be loaded: %s"
                                   % (APP_NAME, s.title, s.broken), Kit.HUE_BAD)
            self.load_prefs()
        finally:
            # the windows and modules come back even if the load went wrong
            self.prefs_frozen = False
            self.config = ConfigWindow(self)
            self.config.prof_sel = name
            self.config.open()
            self.hub = HubWindow(self)
            if self.grid is not None:
                safe(self.grid.show if self.pref_int("grid_on", 0) == 1 else self.grid.hide)
            for s in self.slots:
                if s.enabled:
                    self.start(s)
            Kit.note_screen()                    # every window is placed: the places are for this screen
        PROFILES.report(name, "loaded", *result)

    def _profile_fav(self, name):
        if PROFILES.info(name) is None:
            raise Exception("save a profile first, then star it")
        if PROFILES.favorite() == name:
            PROFILES.set_favorite("")
            safe(lambda: PROFILES.set_client_default(None))
            API.SysMsg('%s: "%s" is no longer the favourite profile.' % (APP_NAME, name),
                       Kit.HUE_INFO)
            return
        PROFILES.set_favorite(name)
        note = ""
        try:
            PROFILES.set_client_default(name)
        except Exception as ex:
            note = " (TazUO's default for new characters wasn't set: %s)" % Tz.why(ex)
        API.SysMsg('%s: "%s" is the favourite profile: every character that hasn\'t loaded '
                   'another profile gets it when Virtue Assistant starts.%s'
                   % (APP_NAME, name, note), Kit.HUE_GOOD)

    # ---------- run ----------
    def run(self):
        Client.find()
        if Client.mouse is None:
            safe(lambda: API.SysMsg("%s: couldn't reach the client's mouse timer; "
                                    "double-clicks use the client's own event instead."
                                    % APP_NAME, Kit.HUE_INFO))
        self.load_prefs()
        Kit.read_screen()                     # the screen the saved window places are for
        LAYOUT.load()                         # the frame and window layouts in use
        SNAP.on_drop(LAYOUT.dropped)          # a window let go on a zone is slotted there
        safe(lambda: API.OnStop(self.shutdown))
        self.grid = Grid(self)
        try:
            self.config = ConfigWindow(self)
            self.config.open()
        except Exception as ex:
            # a bad saved pref, a build without the resizable window: say so and
            # keep a handle on screen (the gear) rather than end with no window
            self._tell("%s: the window could not be built: %s%s"
                       % (APP_NAME, ex, _error_where()))
            if self.config is None:          # (it was the window's own making that failed)
                self.config = safe(lambda: ConfigWindow(self))
            if self.config is not None:
                safe(lambda: self.config.build_gear(self.config.gx, self.config.gy))
        try:
            self.hub = HubWindow(self)
        except Exception as ex:
            self._tell("%s: the Ultima Tracker window could not be made: %s%s"
                       % (APP_NAME, ex, _error_where()))
        if self.pref_int("grid_on", 0) == 1:  # the grid was up when you left
            safe(self.grid.show)
        names = [s.title for s in self.slots if s.enabled]
        if self.debug and LOAD_MS:
            safe(lambda: API.SysMsg("%s: load times %s." % (APP_NAME, ", ".join(
                "%s %d ms" % (n.replace("Module.py", ""), ms) for n, ms in LOAD_MS)),
                Kit.HUE_INFO))
        API.SysMsg("%s %s running. %s" % (APP_NAME, APP_VERSION,
                   ("On: " + ", ".join(names)) if names else
                   "Tick a module on the Modules tab to turn it on."), Kit.HUE_GOOD)
        for s in self.slots:
            if s.enabled:
                self.start(s)
        Kit.note_screen()                     # every window is placed: the places are for this screen
        try:
            self.whats_new.open()             # once per account for a new version (WHATS_NEW)
        except Exception as ex:
            self._tell("%s: the What's new window could not be made: %s" % (APP_NAME, ex))
        try:
            while not self.stopping():
                try:
                    API.ProcessCallbacks()
                except Exception:
                    pass
                try:
                    self.run_due()
                except Exception as ex:
                    # a fault of the mother's own must not end the script: say so
                    # (once) and go on with the next pass
                    if self.stopping():
                        break
                    self._tell("%s: main loop error: %s%s" % (APP_NAME, ex, _error_where()))
                API.Pause(HOST_TICK)
        finally:
            self.shutdown()

    def shutdown(self):
        if self.shut:
            return
        self.shut = True
        self.quitting = True
        safe(lambda: Picker.drop(None))       # no cursor of ours left with the client
        safe(LAYOUT.surround.close)           # (2.6.70) the one frame's backdrop goes too
        safe(lambda: Kit.on_client(LAYOUT.game_view_restore))   # (2.6.72) your own game view
        safe(lambda: Kit.dispose(getattr(LAYOUT, "ping_g", None)))   # (2.6.72) the ping readout
        safe(lambda: LAYOUT.set_arrange(False, tell=False))      # (2.6.72) the zone outlines
        # in reverse order of registration, so a module that offers a service
        # (Bags' bag.attach, Ultima Tracker's hub section) is still
        # there while the modules using it (Character, Map Pings) stop; _stop
        # keeps the cursor-claim and stack bookkeeping of the normal path
        for s in reversed(self.slots):
            if s.running:
                try:
                    self._stop(s)
                except Exception:
                    s.running = False
        self._refresh_active()
        if self.config is not None:
            safe(self.save_prefs)
            safe(self.config.close)
        if self.hub is not None:
            safe(self.hub.close)
        safe(ALERTS.close)
        safe(self.whats_new.close)
        safe(LAYOUT.close)                    # the zone editor, if it is up
        safe(Kit.arrow_down)                  # the shared tracking arrow
        safe(GUARD.store)                     # the guard state with the spot you stop on
        safe(Kit.note_screen)                 # the places just saved are for this screen
        if self.grid is not None:
            safe(self.grid.hide)
        safe(lambda: API.SysMsg("%s stopped." % APP_NAME, Kit.HUE_INFO))


# =============================================================================
#  PartSet (2.6.5) - the hooks of a module made of parts
#  A themed module file builds each of its parts like a module of its own (a
#  function returning the usual hooks dict: start, tick, stop, client_tick,
#  thread_tick, interval, config_*) and hands them to a PartSet, which is the
#  module's MODULE dict:
#
#      PARTS = (("frames", _part_frames, 0.1), ("swing", _part_swing, 0.025), ...)
#      MODULE = PartSet(KEY, TITLE, PARTS).hooks()
#
#  The set runs only the parts that are ticked on (HOST.add parts=... lists
#  them with their boxes; HOST.part_on says which): it starts them when the
#  module starts or their box is ticked, stops them when it is unticked or the
#  module stops, ticks each on its own interval inside the module's tick (the
#  module's interval is the smallest of the running parts'), runs their
#  thread_ticks, and draws the settings page as one section per part (a part
#  that is off shows one grey line). A part's old module key still answers
#  (HOST.disable("swing") turns the part off; HOST.by_key["swing"].running).
#  While a part's code runs, HOST.cur_part names it, so cursors and windows
#  it registers are the part's own and come down when the part stops.
# =============================================================================
class PartSet(object):
    OFF_LINE = "%s is off: tick it under PARTS above to turn it on and see its settings."

    def __init__(self, key, title, parts):
        self.key = key
        self.title = title
        self.specs = []            # [part key, builder, interval, old key or None]
        for spec in parts:
            self.specs.append([spec[0], spec[1], float(spec[2]),
                               spec[3] if len(spec) > 3 else None])
        # (2.6.82) one dict get instead of a scan of specs (and a new string) per call
        self._owner = {}           # part key -> the key its own code uses
        self._iv = {}              # part key -> its registered interval
        for sp in self.specs:
            self._owner[sp[0]] = sp[3] or ("%s.%s" % (key, sp[0]))
            self._iv[sp[0]] = sp[2]
        self._fns = {}             # part key -> (interval hook, has thread_tick, thread_wanted)
        self.api = {}              # part key -> its hooks (built at first use)
        self.running = []          # part keys running, in start order
        self.due = {}              # part key -> next tick due
        self.thread_due = {}
        self.want = None           # the set a "parts" hook asked for while busy
        self.busy = 0
        self.stopping = False
        self._slot = None

    # ---------- bookkeeping ----------
    def slot(self):
        if self._slot is None:
            self._slot = dict.get(HOST.by_key, self.key)
        return self._slot

    def owner(self, pk):
        """The key the part's own code uses (its 2.6.06 key when it has one)."""
        return self._owner.get(pk, pk)

    def part_api(self, pk):
        api = self.api.get(pk)
        if api is None:
            for sp in self.specs:
                if sp[0] == pk:
                    HOST.cur_part, HOST.cur_owner = pk, self.owner(pk)
                    try:
                        api = sp[1]()
                    finally:
                        HOST.cur_part = HOST.cur_owner = None
                    self.api[pk] = api
                    self._fns[pk] = ((api.get("interval"), "thread_tick" in api,
                                      api.get("thread_wanted")) if api else (None, False, None))
                    break
        return api

    def interval_of(self, pk):
        return self._iv.get(pk, 0.1)

    def _call(self, pk, hook, *args):
        """One hook of one part, with HOST.cur_part set; an error is reported
        under the part's name and never stops the other parts."""
        api = self.part_api(pk)
        fn = api.get(hook) if api else None
        if not fn:
            return None
        s = self.slot()
        was = (HOST.cur_part, HOST.cur_owner)
        HOST.cur_part, HOST.cur_owner = pk, self.owner(pk)
        self.busy += 1
        try:
            return fn(*args)
        except Exception as ex:
            if s is not None and not HOST.stopping():
                HOST.report(s, ex, s.part_title(pk), pk)
        finally:
            self.busy -= 1
            HOST.cur_part, HOST.cur_owner = was
        return None

    def _sync_slot(self):
        s = self.slot()
        if s is not None:
            s.parts_running = set(self.running)

    # ---------- starting and stopping parts ----------
    def start_part(self, pk):
        if pk in self.running or self.stopping:
            return
        api = self.part_api(pk)
        if api is None:
            return
        self.running.append(pk)
        self._sync_slot()
        if HOST.config is not None:
            HOST.config.forget_measure(self.key)
        self.due[pk] = 0.0
        self.thread_due[pk] = False
        s = self.slot()
        if s is not None:
            s.next_due = 0.0          # (2.6.82) the module wakes at its next part due: now
        self._call(pk, "start")

    def stop_part(self, pk):
        if pk not in self.running:
            return
        self.running.remove(pk)
        self._sync_slot()
        if HOST.config is not None:
            HOST.config.forget_measure(self.key)
        owner = self.owner(pk)
        safe(lambda: Picker.drop(owner))
        HOST.release_cursor(owner)
        self._call(pk, "stop")

    def wanted(self):
        s = self.slot()
        return set(s.parts_wanted()) if s is not None else set()

    def reconcile(self, want=None):
        """Start the parts newly on, stop the ones turned off (in the order of
        the parts list, so a part that offers a service starts first)."""
        if want is None:
            want = self.wanted()
        if self.busy:
            self.want = set(want)         # after the part that is running returns
            return
        self.want = None
        for sp in self.specs:
            pk = sp[0]
            if pk in want and pk not in self.running:
                self.start_part(pk)
        for pk in list(reversed(self.running)):
            if pk not in want:
                self.stop_part(pk)

    # ---------- the module hooks ----------
    def _start(self):
        self.stopping = False
        self.reconcile()

    def _parts(self, on_set):
        self.reconcile(on_set)

    _NOFN = (None, False, None)

    def _tick(self):
        now = time.time()
        poked = HOST.pass_poked
        running = self.running
        due = self.due
        for pk in list(running):
            if pk not in running:
                continue
            d = due.get(pk, 0.0)
            if poked or now >= d or d - now > Host.CLOCK_BACK:
                self._call(pk, "tick")
                nxt, has_thread, want = self._fns.get(pk, self._NOFN)
                step = self._iv.get(pk, 0.1)
                if nxt is not None:
                    try:
                        step = nxt() or step
                    except Exception:
                        pass
                due[pk] = time.time() + step
                if has_thread and want is not None:
                    # (2.6.82) the part says whether it has thread work
                    try:
                        has_thread = bool(want())
                    except Exception:
                        has_thread = True
                self.thread_due[pk] = has_thread
        if self.want is not None and not self.busy:
            self.reconcile(self.want)

    def _thread_wanted(self):
        """(2.6.82) A script-thread pass only when a part has thread work owed."""
        if self.want is not None:
            return True
        td = self.thread_due
        for pk in self.running:
            if td.get(pk):
                return True
        return False

    def _thread_tick(self):
        for pk in list(self.running):
            if self.thread_due.get(pk) and pk in self.running:
                self.thread_due[pk] = False
                self._call(pk, "thread_tick")
        if self.want is not None and not self.busy:
            self.reconcile(self.want)

    def _interval(self):
        """(2.6.82) The time to the next part due (its step was read in _tick),
        not the smallest part interval: no empty ticks between parts out of
        phase, and no part's interval hook asked twice a pass."""
        best = None
        due = self.due
        for pk in self.running:
            d = due.get(pk, 0.0)
            if best is None or d < best:
                best = d
        if best is None:
            return 1.0
        return min(30.0, max(0.002, best - time.time()))

    def _stop(self):
        self.stopping = True
        self.want = None
        for pk in list(reversed(self.running)):
            self.stop_part(pk)

    # ---------- the settings page: one section per part ----------
    HEAD_H = 28

    def _config_height(self, w):
        h = 0
        for sp in self.specs:
            pk = sp[0]
            h += (Kit.GAP if h else 0) + self.HEAD_H
            if pk in self.running:
                api = self.api.get(pk)
                if api and api.get("config_height"):
                    hh = self._call(pk, "config_height", w)
                    h += Kit.GAP + max(0, int(hh or 0))
        return max(40, h)

    def _build_config(self, g, x, y, w):
        s = self.slot()
        for sp in self.specs:
            pk = sp[0]
            title = s.part(pk)[1] if s is not None and s.part(pk) else pk
            on = pk in self.running
            api = self.api.get(pk) if on else None
            if y > 0 and sp is not self.specs[0]:
                y += Kit.GAP
            Kit.add_section(g, x, y, w, self.HEAD_H, title.upper() if on else None)
            if not on:
                Kit.add_label(g, Kit.fit(self.OFF_LINE % title, w - 24), x + 12, y + 7,
                              Kit.HUE_INFO)
            y += self.HEAD_H
            if on and api and api.get("build_config"):
                y += Kit.GAP
                hh = self._call(pk, "config_height", w) if api.get("config_height") else 0
                self._call(pk, "build_config", g, x, y, w)
                y += max(0, int(hh or 0))

    def _poll_config(self):
        for pk in list(self.running):
            self._call(pk, "poll_config")

    def _config_closed(self):
        for pk in self.specs:
            api = self.api.get(pk[0])
            if api and api.get("config_closed"):
                self._call(pk[0], "config_closed")

    def hooks(self):
        return {"start": self._start, "tick": self._tick, "stop": self._stop,
                "client_tick": True, "thread_tick": self._thread_tick,
                "thread_wanted": self._thread_wanted,
                "interval": self._interval, "parts": self._parts,
                "config_height": self._config_height, "build_config": self._build_config,
                "poll_config": self._poll_config, "config_closed": self._config_closed}


# =============================================================================
#  Tz - TazUO's own settings (its Options window and its Legion Assistant
#  window), reached by reflection, the way Client and Typing reach the mouse
#  and the chat line. Anything that touches the client's objects runs on the
#  client thread (Kit.on_client); only Profiles below calls these.
# =============================================================================
class Tz(object):
    _types = {}
    _MISS = object()

    @staticmethod
    def T(name):
        """A client type by full name; raises when this TazUO build has none."""
        if name not in Tz._types:
            Tz._types[name] = Client._type(name)
        t = Tz._types[name]
        if t is None:
            raise Exception("this TazUO build has no %s" % name.split(".")[-1])
        return t

    @staticmethod
    def get(obj, name, t=None):
        """A property or field (obj None: static on t); raises when missing."""
        v = Typing._get(obj, name, t, Tz._MISS)
        if v is Tz._MISS:
            raise Exception("can't read %s" % name)
        return v

    @staticmethod
    def _flags(static):
        from System.Reflection import BindingFlags
        return BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly | \
            (BindingFlags.Static if static else BindingFlags.Instance)

    #  What put / call found, by (type, name, ...): the walk up the type's bases
    #  (and, for call, over every method of each) is done once per member.
    _found = {}

    @staticmethod
    def put(obj, name, value, t=None):
        """Set a property or field, private ones too (obj None: static on t)."""
        t = t if t is not None else obj.GetType()
        ck = ("put", t, name, obj is None)
        hit = Tz._found.get(ck, Tz._MISS)
        if hit is Tz._MISS:
            hit = None
            flags = Tz._flags(obj is None)
            tt = t
            while tt is not None:
                p = tt.GetProperty(name, flags)
                if p is not None and p.CanWrite:
                    hit = (True, p)
                    break
                f = tt.GetField(name, flags)
                if f is not None:
                    hit = (False, f)
                    break
                tt = tt.BaseType
            Tz._found[ck] = hit
        if hit is None:
            raise Exception("can't set %s" % name)
        if hit[0]:
            hit[1].SetValue(obj, value, None)
        else:
            hit[1].SetValue(obj, value)

    @staticmethod
    def call(obj, name, args=(), t=None):
        """Call a method by name and number of arguments, private ones too
        (obj None: static on t). The most derived match wins."""
        import System
        t = t if t is not None else obj.GetType()
        args = list(args)
        ck = ("call", t, name, len(args), obj is None)
        m = Tz._found.get(ck, Tz._MISS)
        if m is Tz._MISS:
            m = None
            flags = Tz._flags(obj is None)
            tt = t
            while tt is not None and m is None:
                for mm in tt.GetMethods(flags):
                    if mm.Name == name and not mm.IsGenericMethodDefinition \
                            and mm.GetParameters().Length == len(args):
                        m = mm
                        break
                tt = tt.BaseType
            Tz._found[ck] = m
        if m is None:
            raise Exception("can't call %s.%s" % (t.Name, name))
        return m.Invoke(obj, System.Array[object](args))

    @staticmethod
    def load_json(path, typeinfo, t):
        """ConfigurationResolver.Load<t>(path, typeinfo): the client's own
        reader for its settings files. None if the file can't be read."""
        import System
        from System.Reflection import BindingFlags
        cr = Tz.T("ClassicUO.Configuration.ConfigurationResolver")
        for m in cr.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static):
            if m.Name == "Load" and m.IsGenericMethodDefinition and m.GetParameters().Length == 2:
                g = m.MakeGenericMethod(System.Array[System.Type]([t]))
                return g.Invoke(None, System.Array[object]([path, typeinfo]))
        raise Exception("can't read TazUO settings files")

    @staticmethod
    def copy_props(src, dst, skip=()):
        """Copy every saved setting (public read/write property that is not
        [JsonIgnore]) of src onto dst. Returns (changed, failed)."""
        import System
        from System.Reflection import BindingFlags
        changed = failed = 0
        for p in dst.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance):
            name = str(p.Name)
            if name in skip or name.endswith("Serial"):
                continue                     # this character's own items
            if not p.CanRead or not p.CanWrite or p.GetIndexParameters().Length \
                    or p.GetSetMethod(False) is None:
                continue
            attrs = safe(lambda: list(p.GetCustomAttributes(True)), []) or []
            if any(a.GetType().Name == "JsonIgnoreAttribute" for a in attrs):
                continue
            try:
                v = p.GetValue(src, None)
                if System.Object.Equals(v, p.GetValue(dst, None)):
                    continue
                try:
                    p.SetValue(dst, v, None)
                except Exception:            # a number that came back as another type
                    pt = p.PropertyType
                    v = System.Enum.ToObject(pt, v) if pt.IsEnum else \
                        System.Convert.ChangeType(v, pt)
                    p.SetValue(dst, v, None)
                changed += 1
            except Exception:
                failed += 1
        return changed, failed

    @staticmethod
    def windows(type_names):
        """The client's open windows whose class is one of type_names."""
        gumps = Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))
        return [g for g in list(gumps) if str(g.GetType().Name) in type_names]

    @staticmethod
    def why(ex):
        """The innermost message of an exception from a reflected call."""
        e = getattr(ex, "clsException", None) or ex
        while getattr(e, "InnerException", None) is not None:
            e = e.InnerException
        return str(getattr(e, "Message", None) or e)


# =============================================================================
#  Profiles - a saved copy of one character's whole setup that any other
#  character can load. Each profile is a folder in LegionScripts/
#  VirtueAssistantProfiles:
#     profile.txt        name, when it was saved, from which character
#     va_vars.txt        every Virtue Assistant setting the character saved
#                        (module settings, window places, which modules are
#                        on), one "key<TAB>value" a line, escaped
#     unified_bag.cfg    the Unified Bag layout (not its slot assignments)
#     tazuo/             TazUO's own files: profile.json (the Options window
#                        and the Assistant's options) and the files listed in
#                        CLIENT_FILES
#  _favorite.txt in the folder names the favorite. Each character remembers
#  which profile it follows in PROFILE_STATE_KEY: "fav|name|stamp" (it
#  follows the favorite) or "pick|name|stamp" (it chose that profile).
# =============================================================================
class Profiles(object):
    # Options settings that belong to one character (its own items, or who it is)
    PROFILE_SKIP = ("Username", "ServerName", "CharacterName", "Serial", "LastLoaded",
                    "FollowingTarget")
    # Bags (Unified Bag file) lines that are this character's own bags and items
    BAG_OWN = ("slot.", "trapsel=", "trapextra=")
    # Virtue Assistant settings keyed by an item serial (a runebook, a spellbook)
    SERIAL_KEY = re.compile(r"_[0-9A-Fa-f]{8}$")
    MISSING = "\x01VA-missing"

    def __init__(self):
        base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
        if base and safe(lambda: os.path.isfile(base), False):
            base = os.path.dirname(base)
        if not base:
            import System
            base = os.path.join(str(System.AppDomain.CurrentDomain.BaseDirectory), "LegionScripts")
        self.base = os.path.join(base, PROFILE_DIR)

    # ---------- files ----------
    @staticmethod
    def _read(path):
        import System
        try:
            if path and System.IO.File.Exists(path):
                return str(System.IO.File.ReadAllText(path))
        except Exception:
            pass
        return None

    @staticmethod
    def _write(path, text):
        import System
        System.IO.File.WriteAllText(path, text, System.Text.UTF8Encoding(False))

    @staticmethod
    def _esc(s):
        return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r") \
            .replace("\n", "\\n")

    @staticmethod
    def _unesc(s):
        un = {"t": "\t", "r": "\r", "n": "\n"}
        return re.sub(r"\\(.)", lambda m: un.get(m.group(1), m.group(1)), s, flags=re.S)

    # names Windows reserves for devices: a folder can't be called these
    RESERVED = frozenset(["CON", "PRN", "AUX", "NUL", "CLOCK$"] + ["COM%d" % i for i in range(1, 10)]
                         + ["LPT%d" % i for i in range(1, 10)])

    @staticmethod
    def clean(name):
        """A profile name that is also a good folder name ('' if none): no
        path characters, and not a Windows device name (CON, NUL, COM1...,
        which fail only at CreateDirectory with an opaque message)."""
        name = re.sub(r'[\\/:*?"<>|\t\r\n]+', "-", str(name or ""))
        name = name.strip(" .-")[:PROFILE_NAME_MAX].strip(" .-")
        low = name.lower()
        if low.endswith(".old") or low.endswith(".saving"):
            # 2.6.81: save's own backup / temporary folder suffixes ("Mage.old" would
            # be hidden from the list and wiped by saving "Mage"): "Mage-old"
            dot = name.rfind(".")
            name = (name[:dot] + "-" + name[dot + 1:])[:PROFILE_NAME_MAX]
        if name.split(".")[0].upper() in Profiles.RESERVED:
            return ""
        return name

    def folder(self, name):
        return os.path.join(self.base, name)

    def names(self):
        """Saved profiles, sorted by name."""
        import System
        out = []
        try:
            if System.IO.Directory.Exists(self.base):
                for d in System.IO.Directory.GetDirectories(self.base):
                    n = str(System.IO.Path.GetFileName(d))
                    if n.endswith(".saving") or n.endswith(".old"):
                        continue
                    if System.IO.File.Exists(os.path.join(str(d), "profile.txt")):
                        out.append(n)
        except Exception:
            pass
        return sorted(out, key=lambda s: s.lower())

    def info(self, name):
        text = self._read(os.path.join(self.folder(name), "profile.txt")) if name else None
        if text is None:
            return None
        info = {}
        for line in text.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                info[k.strip()] = v.strip()
        return info

    def favorite(self):
        name = (self._read(os.path.join(self.base, "_favorite.txt")) or "").strip()
        return name if name and self.info(name) is not None else ""

    def set_favorite(self, name):
        import System
        System.IO.Directory.CreateDirectory(self.base)
        self._write(os.path.join(self.base, "_favorite.txt"), name or "")

    # ---------- which profile this character follows ----------
    def state(self):
        p = Kit.get_var(PROFILE_STATE_KEY).split("|")
        return (p[0], p[1], p[2]) if len(p) >= 3 else ("", "", "")

    def set_state(self, mode, name, stamp):
        Kit.put_var(PROFILE_STATE_KEY, "%s|%s|%s" % (mode, name, stamp))

    # ---------- Virtue Assistant settings ----------
    def keep_var(self, key):
        return key != PROFILE_STATE_KEY and not self.SERIAL_KEY.search(key)

    @staticmethod
    def char_vars():
        """Every setting saved for this character (API.PersistentVar.Char)."""
        import System
        t = Tz.T("ClassicUO.LegionScripting.PersistentVars")
        for m in t.GetMethods():
            if m.Name == "GetAllVars" and m.GetParameters().Length == 1:
                scope = System.Enum.Parse(m.GetParameters()[0].ParameterType, "Char")
                d = m.Invoke(None, System.Array[object]([scope]))
                return dict((str(kv.Key), "" if kv.Value is None else str(kv.Value)) for kv in d)
        raise Exception("can't list this character's saved settings")

    def read_vars(self, name):
        text = self._read(os.path.join(self.folder(name), "va_vars.txt")) or ""
        out = {}
        for line in text.split("\n"):
            if "\t" in line:
                k, v = line.split("\t", 1)
                k = self._unesc(k)
                if k and self.keep_var(k):
                    out[k] = self._unesc(v.rstrip("\r"))
        return out

    def wait_vars(self, wanted, timeout=5.0):
        """Settings are written in the background: wait until every one reads
        back as written. True when they all do."""
        left = dict(wanted)
        end = time.time() + timeout
        while left and not API.StopRequested:
            for k in list(left):
                got = safe(lambda: API.GetPersistentVar(k, self.MISSING, API.PersistentVar.Char))
                if got is not None and str(got) == left[k]:
                    del left[k]
            if not left or time.time() > end:
                break
            API.Pause(0.05)
        return not left

    @staticmethod
    def bag_path():
        """This character's Bags file, _unified_bag_<serial>.cfg (the same name the module uses)."""
        base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
        serial = safe(lambda: int(API.Player.Serial), 0)
        if not serial:
            return None
        name = "_unified_bag_%d.cfg" % serial
        return (base + "/" + name) if base else name

    # ---------- TazUO's own settings ----------
    @staticmethod
    def client_files():
        """(file in the character's TazUO profile folder, what it is, write the
        client's live copy to that file, make the client read it back in).
        Called on the client thread. profile.json is handled on its own."""
        CFG, MGR = "ClassicUO.Configuration.", "ClassicUO.Game.Managers."
        PM = lambda: Tz.T(CFG + "ProfileManager")
        cur = lambda: Tz.get(None, "CurrentProfile", PM())
        path = lambda: str(Tz.get(None, "ProfilePath", PM()))
        world = lambda: Tz.get(None, "Instance", Tz.T("ClassicUO.Game.World"))
        static = lambda tn, name, args=(): Tz.call(None, name, args, Tz.T(tn))
        current = lambda tn: Tz.get(None, "Current", Tz.T(tn))
        inst = lambda tn: Tz.get(None, "Instance", Tz.T(tn))
        SD = CFG + "FeatureConfigs.ScreenDecorations.ScreenDecorations"

        def autoloot_reload():
            a = inst(MGR + "AutoLootManager")
            Tz.put(a, "_loaded", False)       # its loader runs only once otherwise
            Tz.call(a, "Load")

        def infobar_reload():
            Tz.call(Tz.get(world(), "InfoBars"), "Load")
            for gump in Tz.windows(("InfoBarGump",)):
                safe(lambda: Tz.call(gump, "ResetItems"))

        def buysell_flush():
            static(MGR + "BuySellAgent", "Unload")      # writes both lists
            static(MGR + "BuySellAgent", "Load")

        return (
            # ---- the Options window ----
            ("cooldownbars.json", "cooldown bars",
             lambda: Tz.call(current(CFG + "CooldownBarsConfig"), "Save"),
             lambda: static(CFG + "CooldownBarsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_highlights.json", "grid highlights",
             lambda: Tz.call(current(CFG + "GridHighlightsConfig"), "Save"),
             lambda: static(CFG + "GridHighlightsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_container_bands.json", "container bands",
             lambda: Tz.call(current(CFG + "GridContainerBandsConfig"), "Save"),
             lambda: static(CFG + "GridContainerBandsConfig", "LoadForProfile", (path(),))),
            ("screen_decorations.json", "screen effects",
             lambda: Tz.call(current(SD), "Save"),
             lambda: static(SD, "LoadForProfile", (path(),))),
            ("tooltip_overrides.json", "tooltip overrides",
             lambda: Tz.call(Tz.get(current(CFG + "TooltipOverridesConfig"), "Char"), "Save"),
             lambda: static(CFG + "TooltipOverridesConfig", "Load")),
            ("nameoverhead.xml", "name plates",
             lambda: static(MGR + "NameOverHeadManager", "Save"),
             lambda: static(MGR + "NameOverHeadManager", "Load")),
            ("infobar.xml", "info bar",
             lambda: Tz.call(Tz.get(world(), "InfoBars"), "Save"),
             infobar_reload),
            # ---- the Legion Assistant window ----
            ("AutoLoot.json", "auto loot",
             lambda: Tz.call(inst(MGR + "AutoLootManager"), "Save"),
             autoloot_reload),
            ("OrganizerConfig.json", "organizer",
             lambda: Tz.call(inst(MGR + "OrganizerAgent"), "Save"),
             lambda: static(MGR + "OrganizerAgent", "Load")),
            ("journal_filters.json", "journal filter",
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Save", (False,)),
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Load")),
            ("BuyAgentConfig.json", "auto buy", buysell_flush,
             lambda: static(MGR + "BuySellAgent", "Load")),
            ("SellAgentConfig.json", "auto sell", lambda: None,   # flushed with auto buy
             lambda: static(MGR + "BuySellAgent", "Load")),
            ("macros.xml", "macros",
             lambda: Tz.call(Tz.get(world(), "Macros"), "Save", (None,)),
             lambda: Tz.call(Tz.get(world(), "Macros"), "Load")),
            ("hotkeys.json", "hotkeys",
             lambda: static(MGR + "Hotkeys.HotKeys", "Save"),
             lambda: static(MGR + "Hotkeys.HotKeys", "Load")),
        )

    @staticmethod
    def _profile_type():
        PM = Tz.T("ClassicUO.Configuration.ProfileManager")
        return PM, Tz.get(None, "CurrentProfile", PM)

    def _client_export(self, dest):
        """Client thread: have TazUO write every setting to its files. Returns
        (what was saved, what failed, [(file, copy in dest, what)]): (2.6.81)
        the copies are made by save, on the script thread (no disk copies in
        the client's frame beyond TazUO's own saves)."""
        import System
        F = System.IO.File
        PM, cur = self._profile_type()
        src = str(Tz.get(None, "ProfilePath", PM))
        saved, failed, pairs = [], [], []
        try:
            Tz.call(cur, "Save")
            pairs.append((os.path.join(src, "profile.json"), os.path.join(dest, "profile.json"),
                          "options"))
        except Exception as ex:
            failed.append("options (%s)" % Tz.why(ex))
        for fn, what, flush, reload in self.client_files():
            try:
                flush()
                p = os.path.join(src, fn)
                if F.Exists(p):
                    pairs.append((p, os.path.join(dest, fn), what))
            except Exception as ex:
                failed.append("%s (%s)" % (what, Tz.why(ex)))
        return saved, failed, pairs

    def _apply_options(self, path):
        """Client thread: every Options / Assistant option in the profile's
        profile.json onto this character's live settings, then save them."""
        import System
        PM, cur = self._profile_type()
        ctx = Tz.get(None, "DefaultToUse", Tz.T("ClassicUO.Configuration.ProfileJsonContext"))
        src = Tz.load_json(path, Tz.get(ctx, "Profile"), cur.GetType())
        if src is None:
            raise Exception("its profile.json can't be read")
        changed, failed = Tz.copy_props(src, cur, self.PROFILE_SKIP)
        Tz.call(cur, "Save")
        # two settings the client applies only when its Options window sets them
        safe(lambda: Tz.call(Tz.get(None, "Game", Tz.T("ClassicUO.Client")), "SetVSync",
                             (Tz.get(cur, "EnableVSync"),)))
        safe(lambda: Tz.put(None, "ContainerScale",
                            System.Single(int(Tz.get(cur, "ContainersScale")) / 100.0),
                            Tz.T("ClassicUO.Game.Managers.UIManager")))
        return changed, failed

    def _client_import(self, srcdir):
        """Client thread: the profile's TazUO files onto this character. Each
        file goes into the character's folder and the client reads it back in;
        if that fails the character's own file is put back."""
        import System
        F = System.IO.File
        done, failed = [], []
        # its open Options / Assistant windows would show (and save) the old values
        for w in Tz.windows(("OptionsWindow", "AssistantWindow")):
            safe(lambda: Tz.call(w, "Dispose"))
        PM, cur = self._profile_type()
        dest = str(Tz.get(None, "ProfilePath", PM))
        pj = os.path.join(srcdir, "profile.json")
        if F.Exists(pj):
            try:
                changed, bad = self._apply_options(pj)
                done.append("options (%d changed)" % changed)
                if bad:
                    failed.append("%d option%s" % (bad, "" if bad == 1 else "s"))
            except Exception as ex:
                failed.append("options (%s)" % Tz.why(ex))
        for fn, what, flush, reload in self.client_files():
            p = os.path.join(srcdir, fn)
            if not F.Exists(p):
                continue
            target = os.path.join(dest, fn)
            old = F.ReadAllBytes(target) if F.Exists(target) else None
            try:
                F.Copy(p, target, True)
                reload()
                done.append(what)
            except Exception as ex:
                failed.append("%s (%s)" % (what, Tz.why(ex)))
                try:
                    if old is not None:
                        F.WriteAllBytes(target, old)
                    elif F.Exists(target):
                        F.Delete(target)
                    reload()
                except Exception:
                    pass
        return done, failed

    def set_client_default(self, name):
        """Make profile `name` TazUO's default for new characters (its
        default.json and macros.xml); None puts back what was there before."""
        import System
        F = System.IO.File
        root = str(Tz.get(None, "RootPath", Tz.T("ClassicUO.Configuration.ProfileManager")))
        for fn, dflt in (("profile.json", "default.json"), ("macros.xml", "macros.xml")):
            target = os.path.join(root, dflt)
            bak, none = target + ".va-backup", target + ".va-none"
            if name:
                src = os.path.join(self.folder(name), "tazuo", fn)
                if not F.Exists(src):
                    continue
                if not F.Exists(bak) and not F.Exists(none):   # keep the original once
                    if F.Exists(target):
                        F.Copy(target, bak, False)
                    else:
                        self._write(none, "")
                F.Copy(src, target, True)
            elif F.Exists(bak):
                F.Copy(bak, target, True)
                F.Delete(bak)
            elif F.Exists(none):
                if F.Exists(target):
                    F.Delete(target)
                F.Delete(none)

    # ---------- save / load ----------
    @staticmethod
    def _on_client(fn):
        """fn (TazUO's own settings) on the client thread: its (done, failed)."""
        try:
            res = Kit.on_client(fn, fallback=False)
        except Exception as ex:
            res = ([], ["TazUO settings (%s)" % Tz.why(ex)])
        return res or ([], ["TazUO settings (couldn't reach the client)"])

    def save(self, name, prefs_data):
        """This character's setup as profile `name` (written beside the old
        copy, which is replaced only once the new one is complete). Returns
        (stamp, number of Virtue Assistant settings, TazUO saved, failed)."""
        import System
        D = System.IO.Directory
        final = self.folder(name)
        tmp, old = final + ".saving", final + ".old"
        if D.Exists(tmp):
            D.Delete(tmp, True)
        D.CreateDirectory(os.path.join(tmp, "tazuo"))
        stamp = "%d" % int(time.time())
        # Virtue Assistant: everything this character saved, but its own items
        va = dict((k, v) for k, v in self.char_vars().items() if self.keep_var(k))
        va[SETTINGS_KEY] = prefs_data          # the window as it is now
        self._write(os.path.join(tmp, "va_vars.txt"),
                    "".join("%s\t%s\n" % (self._esc(k), self._esc(va[k])) for k in sorted(va)))
        bag = self.bag_path()
        text = self._read(bag) if bag else None
        if text is not None:
            lay = [l for l in text.splitlines() if l.strip() and not l.startswith(self.BAG_OWN)]
            self._write(os.path.join(tmp, "unified_bag.cfg"), "\n".join(lay))
        res = self._on_client(lambda: self._client_export(os.path.join(tmp, "tazuo")))
        saved, failed = list(res[0]), list(res[1])
        F = System.IO.File
        for src, dst, what in (res[2] if len(res) > 2 else ()):
            try:                                 # 2.6.81: copied here, off the client thread
                F.Copy(src, dst, True)
                saved.append(what)
            except Exception as ex:
                failed.append("%s (%s)" % (what, Tz.why(ex)))
        who = safe(lambda: str(API.Player.Name), "") or ""
        self._write(os.path.join(tmp, "profile.txt"),
                    "name=%s\nsaved=%s\nfrom=%s\nversion=%s\n" % (name, stamp, who, APP_VERSION))
        if D.Exists(old):
            D.Delete(old, True)
        if D.Exists(final):
            D.Move(final, old)
        try:
            D.Move(tmp, final)
        except Exception:
            # the new copy couldn't take the old one's place: put the old one
            # back (names() hides "<name>.old", so the profile would look deleted)
            if D.Exists(old) and not D.Exists(final):
                safe(lambda: D.Move(old, final))
            raise
        if D.Exists(old):
            D.Delete(old, True)
        # read it back: the saved copy must hold exactly what was meant to be saved
        if self.read_vars(name) != va or (self.info(name) or {}).get("saved") != stamp:
            raise Exception("the saved copy doesn't read back the same - try again")
        return stamp, len(va), saved, failed

    def apply(self, name, mode):
        """Put profile `name` on this character. The modules must be stopped
        (or not loaded yet). Returns (settings written, all read back,
        TazUO done, TazUO failed)."""
        info = self.info(name)
        if info is None:
            raise Exception('there is no profile "%s"' % name)
        folder = self.folder(name)
        va = self.read_vars(name)
        for k in sorted(va):
            Kit.put_var(k, va[k])
        ok = self.wait_vars(va)
        lay = self._read(os.path.join(folder, "unified_bag.cfg"))
        bag = self.bag_path()
        if lay is not None and bag:
            own = [l for l in (self._read(bag) or "").splitlines() if l.startswith(self.BAG_OWN)]
            self._write(bag, "\n".join([l for l in lay.splitlines() if l.strip()] + own))
        done, failed = self._on_client(lambda: self._client_import(os.path.join(folder, "tazuo")))
        self.set_state(mode, name, info.get("saved", ""))
        return len(va), ok, done, failed

    def report(self, name, verb, n, ok, done, failed):
        API.SysMsg('%s: profile "%s" %s: %d Virtue Assistant settings; TazUO: %s.'
                   % (APP_NAME, name, verb, n, ", ".join(done) or "nothing"), Kit.HUE_GOOD)
        if not ok:
            API.SysMsg("%s: some settings were still being written; restart Virtue "
                       "Assistant if a module looks unchanged." % APP_NAME, Kit.HUE_BAD)
        if failed:
            API.SysMsg("%s: not done: %s." % (APP_NAME, "; ".join(failed)), Kit.HUE_BAD)

    def startup(self):
        """Before the modules load: a character that follows the favorite, or
        has never had a profile, gets the favorite when it is new to it."""
        fav = self.favorite()
        if not fav:
            return
        stamp = (self.info(fav) or {}).get("saved", "")
        mode, name, had = self.state()
        if mode == "pick" and name != fav and self.info(name) is not None:
            return                               # it chose another profile
        if name == fav and had == stamp:
            return                               # already has this copy of it
        n, ok, done, failed = self.apply(fav, "fav")
        self.report(fav, "(the favourite) put on this character", n, ok, done, failed)


# =============================================================================
#  The Virtue Assistant window: a Modules tab with a switch for every module,
#  a Settings tab with every module's settings, and a gear it folds into.
# =============================================================================
class ConfigWindow(object):
    W = 640
    GEAR = 52                 # size of the minimized gear
    TABS = (("modules", "Modules"), ("settings", "Settings"))

    #  Action Bar link (the same kind Grimoire and Bags have). Minimize
    #  folds the window into the gear, which stays on screen. The gold "Fold
    #  into the Action Bar" arrow (or the bar's Virtue Assistant button) folds
    #  it into the bar instead: the gear is hidden ("docked") and the bar's
    #  button stands in for it. The bar sends "show" / "dock"; this window
    #  reports open / gear / docked / off. If the bar stops or is minimized its
    #  heartbeat ends and the gear comes back; it hides again when the bar
    #  returns, until the window is opened (the wish is HOST's "va" key).
    DOCK_KEY = "va"
    LINK_CMD = "VirtueAssistant_cmd"
    LINK_STATE = "VirtueAssistant_state"
    LINK_ALIVE = "ActionBar_alive"     # the bar's heartbeat (time.time())
    LINK_STALE = 10.0                  # seconds without it before the gear returns
    LINK_ENABLE = "VirtueAssistant_enable"   # a module key to turn on, from outside

    def __init__(self, host):
        self.host = host
        self.g = None
        self.mode = None
        self.store = ({}, {})
        self.boxes = {}
        self.seen = {}
        self._pp_key = None       # (2.6.82) the page poll_due's gate is for, and the gate
        self._pp_gate = [0.0]
        self._fld_gate = [0.0]    # (2.6.82) the profile drop-down / search / grid fields
        self.gear_look = 0.0      # (2.6.82) next idle look at the gear's place
        self._fld_due = True
        self.x, self.y = Kit.adapt(host.pref_int("cfg_x", 140), host.pref_int("cfg_y", 80),
                                   self.W, self.MIN_H)
        self.gx, self.gy = Kit.adapt(host.pref_int("gear_x", self.x),
                                     host.pref_int("gear_y", self.y), self.GEAR, self.GEAR)
        self.minimized = host.pref_int("cfg_min", 0) == 1 or host.dock_wanted(self.DOCK_KEY)
        self.tab = host.prefs.get("cfg_tab", "modules")
        if self.tab not in ("modules", "settings"):
            self.tab = "modules"
        self.page = host.prefs.get("cfg_page", "")
        self.shown_page = None    # module whose settings are on screen
        self.request = None       # ("settings", key) asked for by a module
        self.request_tab = None   # a tab asked for from outside ("modules")
        self.snap_cb = None
        self.lag_lbl = None
        self.grid_tb = None
        self.lag_next = 0.0
        SNAP.enabled = host.pref_int("snap", 1) == 1
        host.debug = host.pref_int("debug", 0) == 1
        self.debug_cb = None
        self.dirty = None         # module key whose settings need redrawing
        self.reported = set()
        self.gear_clicked = False
        self.gear_pos = None
        self.gear_moved = 0.0
        self.closing = False
        self.docked = False       # gear hidden: the Action Bar stands in for it
        self.link_state = None    # last state published for the Action Bar
        self.link_next = 0.0
        self.prof_sel = None      # profile picked in the profile list (kept across redraws)
        self.grid_text = None     # the grid field's text as last parsed
        # The saved profiles are read from disk on the script thread (refresh_profiles),
        # never while the window is built on the client thread: a slow disk must not
        # hold up a frame. The window is built from this copy; after each build it is
        # read again and the window redrawn if a profile came or went meanwhile.
        self.prof_cache = None    # ("ok", names, favorite, followed) or ("err", exception)
        self.prof_shown = None    # what the last build showed, to compare with
        self.prof_stale = False   # read the profiles again (on the next pass)
        self.prof_redraw = False  # they changed on disk: draw the window again
        self.page_keys = []       # ("page_<key>", key) for the page buttons drawn
        self.box_list = []        # (slot, checkbox) on the Modules tab, top to bottom
        self.part_boxes = []      # (slot, part key, checkbox): the parts' boxes (2.6.5)
        self.fold_keys = []       # ("fold_<key>", key) for the fold arrows drawn
        self.box_hit = False      # a checkbox of this window was clicked (see _hook_box)
        self.box_next = 0.0       # next safety read of the checkboxes
        self.measured = {}        # (module key, column width) -> (sections, width needed):
        #                           a settings page measured once, kept until it changes
        self.loading = None       # key of the page whose file is being compiled (see _context)
        self.redraw_req = False   # draw the window again on the next poll
        self.stale_page = None    # the page whose module changed its settings (see refresh)
        self.mod_search = ""      # the Modules tab's filter (title or description), lower case
        self.search_tb = None     # its text box, while the Modules tab shows
        self.search_text = None   # the box's text as last read
        self.search_at = 0.0      # when it last changed (it filters SEARCH_SETTLE after)
        self.search_focus = False # give the new box the keyboard after the filter redraw
        self._prof_reset()
        # the room to fill (unscaled pixels): the size the window was dragged to
        sh = Kit.screen()[1]
        self.lim_w = max(self.W, host.pref_int("cfg_w", self.W))
        self.lim_h = max(self.MIN_H, host.pref_int("cfg_h", (sh - 60) if sh > 400 else 1000))
        self.scale = max(50, min(200, host.pref_int("cfg_scale", 100))) / 100.0
        self.size = (0, 0)        # (width, height) on screen the full window was built at
        self.resize_at = 0.0      # time of the last step of a corner drag (0 = none)
        for var in (self.LINK_CMD, self.LINK_ENABLE):          # ignore stale asks
            try:
                API.RemoveSharedVar(var)
            except Exception:
                pass

    # ---------- the profile bar (see Profiles) ----------
    #  A 5-point star drawn as (x, y, w, h) boxes in a 16 x 16 square: there is
    #  no star among the client's gump art.
    STAR_RECTS = ((7, 1, 1, 2), (6, 3, 3, 2), (5, 5, 5, 1), (1, 6, 13, 1), (2, 7, 11, 1),
                  (4, 8, 7, 4), (3, 12, 3, 1), (9, 12, 3, 1), (3, 13, 1, 1), (11, 13, 1, 1))
    STAR_ON, STAR_OFF = "#F0C040", "#6A6A6A"
    PROF_H = 34               # height of the profile bar
    PROF_DD_W = 196           # width of its list

    def _prof_reset(self):
        self.prof_dd = None       # the list of saved profiles (a drop-down)
        self.prof_dd_args = None  # (x, y, w, items, index): added last, so it opens on top
        self.prof_tb = None       # the name box
        self.prof_names = []
        self.prof_fav = ""
        self.prof_stars = {}      # "on" / "off" -> the star's boxes in that colour
        self.prof_seen = None     # list index last seen
        self.prof_star_hit = False

    @staticmethod
    def _cap_w(art, text):
        """Width of an art button with its caption (see Kit.art_button)."""
        return (Kit.pic_size(art[0])[0] or 30) + 5 + Kit.text_w(text)

    def refresh_profiles(self):
        """Read the saved profiles, the favorite and the profile this character
        follows (script thread: file reads). If the window shows other ones,
        it is drawn again on its next poll."""
        self.prof_stale = False
        P = PROFILES
        try:
            data = ("ok", P.names(), P.favorite(), P.state()[1])
        except Exception as ex:
            data = ("err", ex)
        self.prof_cache = data
        if self.prof_shown is not None and self._prof_key(data) != self.prof_shown \
                and self.mode == "full":
            self.prof_redraw = True

    @staticmethod
    def _prof_key(data):
        """What of the profiles the window shows (the list and the star)."""
        return ("ok", data[1], data[2]) if data[0] == "ok" else ("err", str(data[1]))

    def _build_profiles(self, g, x, y, w):
        """The bar: profile list, favorite star, Load, Save and the name box."""
        data = self.prof_cache
        if data is None:                         # not read yet (normally done before)
            self.refresh_profiles()
            data = self.prof_cache
        self.prof_shown = self._prof_key(data)
        self.prof_stale = True                   # look again once the window is up
        if data[0] != "ok":
            raise data[1]
        names, fav, cur = data[1], data[2], data[3]
        sel = self.prof_sel if self.prof_sel in names else None
        if sel is None:
            sel = cur if cur in names else (fav if fav in names else
                                            (names[0] if names else None))
        self.prof_sel, self.prof_names, self.prof_fav = sel, names, fav
        H = self.PROF_H
        Kit.add_section(g, x, y, w, H)
        xs = x + 12 + self.PROF_DD_W + 10
        ys = y + (H - 16) // 2
        self.prof_stars = {"on": [], "off": []}
        for key, color, d in (("shadow", "#000000", 1), ("on", self.STAR_ON, 0),
                              ("off", self.STAR_OFF, 0)):
            for rx, ry, rw, rh in self.STAR_RECTS:
                b = Kit.add_box(g, xs + rx + d, ys + ry + d, rw, rh, 1.0, color)
                if b is not None and key != "shadow":
                    self.prof_stars[key].append(b)
        Kit.catcher(g, xs - 3, ys - 3, 22, 22, self._star_click,
                    "Favourite: every character gets the picked profile unless it loaded "
                    "another (click again to clear it)")
        xb = xs + 28
        Kit.art_button(g, self.store, "p_load", Kit.ART_PLAY, xb, y + 6, "Load",
                       "Load the picked profile on this character")
        xb += self._cap_w(Kit.ART_PLAY, "Load") + 14
        Kit.art_button(g, self.store, "p_save", Kit.ART_OK, xb, y + 6, "Save",
                       "Save this character's setup under the name in the box, or over "
                       "the picked profile when the box is empty")
        xb += self._cap_w(Kit.ART_OK, "Save") + 6
        Kit.add_label(g, "as", xb, y + 9, Kit.HUE_INFO)
        xf = xb + Kit.text_w("as") + 8
        self.prof_tb = Kit.add_textbox(g, "", xf, y + 6, max(60, x + w - 12 - xf),
                                       numbers=False)
        safe(lambda: self.prof_tb.SetTooltip(
            "Name for a new profile (empty: save over the picked one)"))
        items = [n + ("  (favourite)" if n == fav else "") for n in names] or \
            ["(no profiles saved yet)"]
        self.prof_dd_args = (x + 12, y + 7, self.PROF_DD_W, items,
                             names.index(sel) if sel in names else 0)

    def _add_profile_list(self, g):
        """The profile list goes on last, so its open list covers what's below."""
        if self.prof_dd_args is None:
            return
        dx, dy, dw, items, idx = self.prof_dd_args
        dd = G.CreateDropDown(dw, items, idx)
        dd.SetPos(dx, dy)
        g.Add(dd)
        safe(lambda: dd.SetTooltip("The saved profiles; pick one to load or save over"))
        self.prof_dd = dd
        self.prof_seen = idx
        self._show_star()

    def _prof_picked(self):
        return self.prof_sel if self.prof_sel in self.prof_names else None

    def _show_star(self):
        p = self._prof_picked()
        on = bool(p) and p == self.prof_fav
        for key, shown in (("on", on), ("off", not on)):
            for b in self.prof_stars.get(key, []):
                try:
                    b.IsVisible = shown
                except Exception:
                    pass

    def _star_click(self):
        self.prof_star_hit = True

    def _poll_profiles(self):
        """Every pass: the picked profile, the star and the two buttons. The
        work itself is handed to the host (Host.profile_job)."""
        if self.prof_dd is not None and self._fld_due:
            try:
                i = int(self.prof_dd.GetSelectedIndex())
            except Exception:
                i = None
            if i is not None and i != self.prof_seen:
                self.prof_seen = i
                if 0 <= i < len(self.prof_names):
                    self.prof_sel = self.prof_names[i]
                self._show_star()
        star, self.prof_star_hit = self.prof_star_hit, False
        load = Kit.was_clicked(self.store, "p_load")
        save = Kit.was_clicked(self.store, "p_save")
        if not (star or load or save):
            return
        if self.host.profile_req is not None:
            return                               # one at a time
        picked = self._prof_picked()
        if save:
            typed = str(safe(lambda: self.prof_tb.Text, "") or "").strip()
            name = PROFILES.clean(typed) if typed else picked
            if not name:
                API.SysMsg("%s: type a name for the new profile in the box beside Save."
                           % APP_NAME, Kit.HUE_BAD)
                return
            self.host.profile_req = ("save", name)
        elif not picked:
            API.SysMsg("%s: save a profile first (type a name beside Save)." % APP_NAME,
                       Kit.HUE_BAD)
        elif load:
            self.host.profile_req = ("load", picked)
        else:
            self.host.profile_req = ("fav", picked)

    def settings_slots(self):
        """Modules with a settings page (a module not compiled yet is assumed
        to have one; it is compiled when its page is opened)."""
        return [s for s in self.host.slots
                if s.lazy is not None or (s.api is not None and s.api.get("build_config"))] \
            + list(self.host.pages)

    # ---------- building ----------
    def open(self):
        if self.prof_cache is None:
            self.refresh_profiles()              # (script thread: before the hop)
        if self.minimized:
            self.build_gear(self.gx, self.gy)
        else:
            self.build_full(self.x, self.y)

    def build_full(self, x, y):
        """The whole window in one hop on the client thread (see Kit.on_client)."""
        Kit.on_client(lambda: self._build_full(x, y))

    def _replace(self, g, mode, x, y, w, h, head=None):
        old = self.g
        x, y = Kit.place(g, x, y, w, h, head)        # wholly on screen (scrolls if taller)
        if mode == "gear":
            self.gx, self.gy = x, y
        else:
            self.x, self.y = x, y
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        self.g = g
        self.mode = mode
        G.AddGump(g)
        safe(lambda: g.SetInScreen())
        Kit.on_moved(g, self._moved)
        Kit.dispose(old)

    def _note_pos(self):
        """Keep where the window (or the gear) is now. False if unreadable."""
        x, y = self.pos()
        if x is None or y is None:
            return False
        if self.mode == "gear":
            self.gx, self.gy = x, y
        elif self.mode == "full":
            self.x, self.y = x, y
        return True

    def _moved(self):
        """The window (or the gear) was dragged and let go: remember where."""
        if self._note_pos():
            self.host.save_prefs()

    def _settings_error(self, s, what, ex):
        msg = "%s: %s settings %s error: %s%s" % (APP_NAME, s.title, what, ex, _error_where())
        if msg not in self.reported:
            self.reported.add(msg)
            safe(lambda: API.SysMsg(msg, Kit.HUE_BAD))

    def _leave_page(self):
        """Read the settings on screen one last time before they go away."""
        key, self.shown_page = self.shown_page, None
        stale, self.stale_page = self.stale_page == key, None
        s = self.host.page_slot(key)
        if s is None or s.api is None:
            return
        for fn in (("config_closed",) if stale else ("poll_config", "config_closed")):
            if s.api.get(fn):
                try:
                    s.api[fn]()
                except Exception as ex:
                    self._settings_error(s, "save", ex)

    # ---------- size, scale and layout ----------
    #  The window is resizable (drag any corner) and scalable (- and + in the
    #  title bar). Everything below the profile bar is cut into sections -
    #  the module list, the options, the module buttons and each section of
    #  the module's settings page - and they run top to bottom, then on to
    #  the next column, left to right ("newspaper" order). The size you drag
    #  to sets how tall a column may be and how many columns there may be;
    #  the window then shrinks to the sections, so there is never empty space.
    #  If they don't fit in that many columns the columns are made as short as
    #  they can be and the window grows taller. Columns are COL_W wide, the
    #  width every module draws its settings page for.
    COL_W = W - 2 * Kit.MARGIN        # one column (module pages are drawn for this)
    MIN_W = W
    MIN_H = 200
    SETTLE = 0.35             # seconds without a resize step before laying out again
    SCALES = (70, 80, 90, 100, 110, 125, 150)   # percent, the - and + steps
    ART_LESS = (5401, 5401, 5401)     # the client's small minus / plus buttons
    ART_MORE = (5402, 5402, 5402)
    HELP_LINES = ("Tick a module to turn it on; closing a module's own window turns it off.",
                  "Each module's settings are on the Settings tab.",
                  "Drag a corner of this window to resize it; its sections fill the space "
                  "top to bottom, then left to right. The - and + at the top scale it.")
    SNAP_CAP = "Windows snap to each other and move together"
    DEBUG_CAP = "Print debug lines in the journal (slow ticks, connections)"
    BROKEN = "could not be loaded: see the journal"
    LAG_SAMPLE = "Loop: 12 modules on; slowest tick lately Ultima Tracker, 999 ms (decays)"

    def _context(self):
        """What the window shows: (modules, modules with a settings page, the
        page shown on the Settings tab or None for the Modules tab)."""
        host = self.host
        pages = self.settings_slots()
        page = None
        if self.tab == "settings" and pages:
            page = host.page_slot(self.page)
            if page not in pages:
                page = pages[0]
                self.page = page.key
            if page.lazy is not None and Client.on_client_thread():
                # its file isn't compiled yet: that happens on the script thread
                # (Host.request_load), and the page is drawn when it is in
                host.request_load(page)
                self.loading = page
                return host.slots, pages, None
            if not host.load(page) or not page.api.get("build_config"):
                pages = self.settings_slots()      # compiled now: it may have no page
                page = pages[0] if pages and host.load(pages[0]) and \
                    pages[0].api.get("build_config") else None
                if page is not None:
                    self.page = page.key
        self.loading = None
        return host.slots, pages, page

    def _body_y(self):
        return Kit.MARGIN + 34 + Kit.GAP + self.PROF_H + Kit.GAP

    # ---- packing sections into columns ----
    #  A unit is {"h": height} (one section) or {"rows": [heights], "head": h,
    #  "tail": h} (a list that may split between columns, each part a section
    #  of its own with head above its rows and tail below).
    def _pack(self, units, n, limit):
        """Units top to bottom, then on to the next of n columns, none taller
        than limit. [(unit index, column, y, first row, end row, height)], or
        None when they don't fit."""
        GAP = Kit.GAP
        out, col, y = [], 0, 0
        for u, unit in enumerate(units):
            rows = unit.get("rows")
            if rows is None:
                size = unit["h"]
                top = y + GAP if y else 0
                if y and top + size > limit:
                    col, top = col + 1, 0
                if col >= n or size > limit:
                    return None
                out.append((u, col, top, None, None, size))
                y = top + size
                continue
            head, tail = unit["head"], unit["tail"]
            i = 0
            while i < len(rows):
                top = y + GAP if y else 0
                if y and top + head + rows[i] + tail > limit:
                    col, top = col + 1, 0
                if col >= n or head + rows[i] + tail > limit:
                    return None
                j, h = i, head + tail
                while j < len(rows) and top + h + rows[j] <= limit:
                    h += rows[j]
                    j += 1
                out.append((u, col, top, i, j, h))
                i, y = j, top + h
                if i < len(rows):
                    col, y = col + 1, 0
        return out

    def _fit(self, units, n):
        """The packing into n columns whose tallest column is shortest."""
        lo = hi = 0
        for unit in units:
            rows = unit.get("rows")
            if rows is None:
                lo = max(lo, unit["h"])
                hi += unit["h"] + Kit.GAP
            elif rows:
                lo = max(lo, unit["head"] + max(rows) + unit["tail"])
                hi += unit["head"] + sum(rows) + unit["tail"] + Kit.GAP
        hi = max(hi, lo, 1)
        best = self._pack(units, n, hi)
        while lo < hi:
            mid = (lo + hi) // 2
            p = self._pack(units, n, mid)
            if p is not None:
                hi, best = mid, p
            else:
                lo = mid + 1
        return best or []

    def _flow(self, units, CW):
        """Where the units go, in columns CW wide, for the size asked for
        (self.lim_w x self.lim_h)."""
        M, GAP = Kit.MARGIN, Kit.GAP
        lim_w = self.lim_w
        sw = Kit.screen()[0]
        if sw:
            lim_w = min(lim_w, max(self.MIN_W, int(sw / self.scale) - 10))
        n = max(1, (lim_w - 2 * M + GAP) // (CW + GAP))
        if sw:                                   # never wider than the screen
            n = max(1, min(n, (int(sw / self.scale) - 2 * M + GAP) // (CW + GAP)))
        limit = max(40, self.lim_h - self._body_y() - M)
        placed = self._pack(units, n, limit)
        if placed is None:                       # too much for that size: shortest columns
            placed = self._fit(units, n)
        return placed

    # ---- the units of each tab ----
    @staticmethod
    def _matches(s, q):
        """Does the search text match this module: its title, description, an
        alias (an old module's name, a feature word), or one of its parts.
        Returns (module matches, [part keys that match])."""
        if not q:
            return True, []
        hit = q in s.title.lower() or q in (s.desc or "").lower() or \
            any(q in a.lower() for a in s.aliases)
        parts = [p[0] for p in s.parts if q in p[1].lower() or q in (p[2] or "").lower()]
        if not parts:
            for p in s.parts:
                if any(q in str(o).lower() for o in p[4]):
                    parts.append(p[0])
        return hit or bool(parts), parts

    def _mod_rows(self, slots, CW):
        """The Modules tab's rows: a heading per category (CATEGORY_ORDER first,
        then any other by name), the modules under it in their own order, only
        those whose title, description, aliases or parts hold the search text.
        A module made of parts gets a row per part under it when it is
        unfolded (its arrow), or when the search matched one of its parts."""
        q = self.mod_search.strip().lower()
        groups, order, found = {}, [], {}
        for s in slots:
            hit, parts = self._matches(s, q)
            if not hit:
                continue
            found[s.key] = parts
            cat = getattr(s, "category", None) or "Other"
            if cat not in groups:
                groups[cat] = []
                order.append(cat)
            groups[cat].append(s)
        cats = [c for c in CATEGORY_ORDER if c in groups] + \
            sorted(c for c in order if c not in CATEGORY_ORDER)
        rows = []
        for cat in cats:
            rows.append(("head", cat))
            for s in groups[cat]:
                broken = s.api is None and s.lazy is None
                rows.append(("mod", s, broken,
                             Kit.wrap(self.BROKEN if broken else s.desc, CW - 212)))
                if s.parts and not broken and (not s.folded or found.get(s.key)):
                    for p in s.parts:
                        rows.append(("part", s, p, Kit.wrap(p[2] or "", CW - 248),
                                     p[0] in found.get(s.key, ())))
        if not rows:
            rows.append(("none", 'No module matches "%s".' % self.mod_search.strip()))
        return rows

    @staticmethod
    def _row_h(r):
        if r[0] in ("mod", "part"):
            return 26 + 20 * (len(r[3]) - 1)
        return 24

    def _units_modules(self, slots):
        CW = self.COL_W
        rows = self._mod_rows(slots, CW)
        lines = [l for para in self.HELP_LINES for l in Kit.wrap(para, CW - 42)]
        split = CW < 30 + Kit.text_w(self.LAG_SAMPLE) + 12 + Kit.text_w("Grid px") + 8 + 48 + 12
        h_opts = 8 + 22 * len(lines) + 72 + (24 if split else 0)
        units = [{"rows": [self._row_h(r) for r in rows], "head": 34, "tail": 4,
                  "draw": lambda g, x, y, h, i, j: self._draw_mods(g, x, y, CW, h, rows[i:j],
                                                                    i == 0)},
                 {"h": h_opts,
                  "draw": lambda g, x, y, h, i, j: self._draw_opts(g, x, y, CW, h, lines, split)}]
        return units, CW

    PAGE_MAX_W = 1100         # a page that needs more than a column gets up to this

    def _measure_page(self, page, x0, y0, CW):
        """Draw the page into a measuring canvas (nothing is shown): its
        sections and the right edge of its widest control (sections' own
        backgrounds aside). None if the page can't be cut into sections. The
        answer is kept per (module, column width) until the page changes
        (Host.refresh_settings, the module starting or stopping): a page was
        built and thrown away up to twice per show, a tab switch measured it
        all again."""
        ck = (page.key, CW)
        if ck in self.measured:
            return self.measured[ck]
        measure = PageCanvas(None)
        out = None
        try:
            page.api["build_config"](measure, x0, y0, CW)
            if Kit.flush():                      # places are set by the queue
                right = x0 + CW
                for c in measure.ctrls:
                    r = safe(lambda: int(c.GetX()) + int(c.GetWidth()), None)
                    if r is not None and r != x0 + CW:
                        right = max(right, r + 4)
                # (x0, y0) is the same for every build, so the places can be kept
                out = ([tuple(int(v) for v in r) for r in measure.sections], right - x0)
        except Exception:
            out = None
        finally:
            # config_closed first, while the measured controls still hold what
            # they were built with: a page that reads its fields when it closes
            # would read a disposed text box as empty and save that
            if page.api.get("config_closed"):
                safe(page.api["config_closed"])
            for c in measure.ctrls:
                safe(lambda: c.Dispose())
        if len(self.measured) > 64:
            self.measured.clear()
        # None too: a page that can't be cut stays whole. The Settings tab's own
        # pages (Alerts, Keys) list what the modules hold right now, which changes
        # without a refresh_settings: they are measured again on every draw.
        if page not in self.host.pages:
            self.measured[ck] = out
        return out

    def forget_measure(self, key):
        """The page of module `key` may look different now: measure it again."""
        for ck in [ck for ck in self.measured if ck[0] == key]:
            self.measured.pop(ck, None)

    def loaded(self, key):
        """A module's file was compiled (Host._run_load_jobs): if its page was
        waited for, draw the window again."""
        self.forget_measure(key)
        if self.loading is not None and self.loading.key == key:
            self.redraw_req = True

    def _units_loading(self, pages, title):
        """The Settings tab while a page's file is being compiled: the page
        buttons and a note in place of the page."""
        CW = self.COL_W
        slot = 35 + max([Kit.text_w(s.title) for s in pages] or [80]) + 12
        per = max(1, 1 + (CW - 30 - slot) // 196)
        n_rows = (len(pages) + per - 1) // per
        self.page_keys = [("page_" + s.key, s.key) for s in pages]

        def draw_pick(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h)
            for k, s in enumerate(pages):
                r = k // per
                if i <= r < j:
                    Kit.art_button(g, self.store, "page_" + s.key, Kit.ART_PAGE,
                                   x + 30 + (k % per) * 196, y + 6 + (r - i) * 28,
                                   s.title, "Show the %s settings page" % s.title,
                                   Kit.HUE_TITLE if s.title == title else Kit.HUE_TEXT)

        def draw_note(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h)
            Kit.add_label(g, "Loading the %s settings page..." % title, x + 12, y + 12, Kit.HUE_INFO)
        return [{"rows": [28] * n_rows, "head": 6, "tail": 4, "draw": draw_pick},
                {"h": 40, "draw": draw_note}], CW

    def _units_settings(self, pages, page, x0, y0):
        """The module buttons (a list of button rows) and every section of the
        page. The page is drawn into a measuring canvas first to find its
        sections (and how wide it really is: a column widens for a page whose
        controls need more room); it is drawn for real by the last unit's draw."""
        CW = self.COL_W
        rects = None                             # None: drawn in one piece, as it was made
        m = self._measure_page(page, x0, y0, CW)
        if m is not None:
            rects, need = m
            if need > CW:
                CW = min(self.PAGE_MAX_W, need)
                m = self._measure_page(page, x0, y0, CW)
                rects = m[0] if m is not None else None
        slot = 35 + max([Kit.text_w(s.title) for s in pages] or [80]) + 12
        per = max(1, 1 + (CW - 30 - slot) // 196)
        n_rows = (len(pages) + per - 1) // per

        self.page_keys = [("page_" + s.key, s.key) for s in pages]

        def draw_pick(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h)
            for k, s in enumerate(pages):
                r = k // per
                if i <= r < j:
                    Kit.art_button(g, self.store, "page_" + s.key, Kit.ART_PAGE,
                                   x + 30 + (k % per) * 196, y + 6 + (r - i) * 28,
                                   s.title, "Show the %s settings page" % s.title,
                                   Kit.HUE_TITLE if s is page else Kit.HUE_TEXT)
        units = [{"rows": [28] * n_rows, "head": 6, "tail": 4, "draw": draw_pick}]
        if page.parts:                           # PARTS: the same boxes as on the Modules tab
            units.append({"h": 34 + 26 * len(page.parts) + 6,
                          "draw": lambda g, x, y, h, i, j: self._draw_parts(g, x, y, CW, h, page)})
        wins = LAYOUT.windows_of(page.key)       # WINDOWS: the zone each sits in (2.6.55)
        if wins:
            units.append({"h": 34 + 26 * len(wins) + 6,
                          "draw": lambda g, x, y, h, i, j: self._draw_windows(g, x, y, CW, h, wins)})
        try:
            h_page = max(40, int(page.api["config_height"](CW)))
        except Exception as ex:
            self._settings_error(page, "layout", ex)
            h_page = 40
        bands = (self._bands(rects, y0, h_page) if rects else None) or [(0, h_page)]
        state = {"at": {}}                       # band index -> (x, y) it was placed at

        def band_draw(b):
            def draw(g, x, y, h, i, j):
                state["at"][b] = (x, y)
                if b == len(bands) - 1:
                    self._draw_page(g, page, x0, y0, CW, bands, state["at"])
            return draw
        for b, (top, bottom) in enumerate(bands):
            units.append({"h": bottom - top, "draw": band_draw(b)})
        return units, CW

    @staticmethod
    def _bands(rects, y0, h_page):
        """The page's sections as horizontal bands (tops and bottoms relative to
        the page's top): sections inside another one belong to it, sections
        side by side move together."""
        rects = sorted(set(rects), key=lambda r: (r[1], r[0]))
        top_level = [r for r in rects if not any(
            o != r and o[0] <= r[0] and o[1] <= r[1] and r[0] + r[2] <= o[0] + o[2]
            and r[1] + r[3] <= o[1] + o[3] for o in rects)]
        bands = []
        for x, y, w, h in top_level:
            t, b = y - y0, y - y0 + h
            if bands and t < bands[-1][1]:
                bands[-1] = (bands[-1][0], max(bands[-1][1], b))
            else:
                bands.append((t, b))
        return bands

    def _draw_page(self, g, page, x0, y0, CW, bands, at):
        """The module draws its page in one piece at (x0, y0); each control is
        then moved with the band (section) it is in."""
        canvas = PageCanvas(g)
        try:
            page.api["build_config"](canvas, x0, y0, CW)
        except Exception as ex:
            self._settings_error(page, "window", ex)
            Kit.add_section(g, x0, y0, CW, 40)
            Kit.add_label(g, "Settings unavailable: %s" % ex, x0 + 12, y0 + 12, Kit.HUE_BAD)
        self.shown_page = page.key
        moves = []
        for b, (top, bottom) in enumerate(bands):
            px, py = at.get(b, (x0, y0 + top))
            moves.append((top, px - x0, py - (y0 + top)))
        if all(dx == 0 and dy == 0 for t, dx, dy in moves):
            return
        if not Kit.flush():                      # can't read where they are: leave them
            return
        for c in canvas.ctrls:
            try:
                cx, cy = int(c.GetX()), int(c.GetY())
            except Exception:
                continue
            rel = cy - y0
            dx, dy = moves[0][1], moves[0][2]
            for top, mx, my in moves:            # the band it is in (or the one above)
                if rel >= top:
                    dx, dy = mx, my
            if dx or dy:
                safe(lambda: c.SetPos(cx + dx, cy + dy))

    SEARCH_W = 150            # the Modules tab's search box

    def _draw_parts(self, g, x, y, w, h, s):
        """The PARTS section at the top of a module's settings page (2.6.5):
        one box per part, so a part can be turned on where its settings are."""
        Kit.add_section(g, x, y, w, h, "PARTS  (tick a part to turn it on)")
        ry = y + 32
        for p in s.parts:
            cb = Kit.add_check(g, p[1], x + 12, ry, bool(s.parts_on.get(p[0])),
                               "%s: %s" % (s.title, p[2] or p[1]))
            self._hook_box(cb)
            self.part_boxes.append((s, p[0], cb))
            self.seen["%s.%s" % (s.key, p[0])] = bool(s.parts_on.get(p[0]))
            Kit.add_label(g, Kit.fit(p[2] or "", w - 236), x + 224, ry + 2, Kit.HUE_INFO)
            ry += 26

    ZONE_TIP = ("Click for the next zone this window sits in (free: it stays where you put it; "
                "the Layout page has them all)")

    def _draw_windows(self, g, x, y, w, h, wins):
        """The WINDOWS section of a module's settings page (2.6.55): one row per
        window of the module known to the layout, with a Zone button that
        cycles through free and every window zone of the frame layout in use
        (Layout.assign_to). A window of a part that is off isn't listed until
        the part is on."""
        Kit.add_section(g, x, y, w, h, "WINDOWS  (the zone each sits in)")
        zones = LAYOUT.zone_choices()
        ry = y + 32
        for key, title in wins:
            Kit.add_label(g, Kit.fit(title, 200), x + 12, ry + 3)
            zid = LAYOUT.zone_of(key)
            cap = "Zone: " + (zid if zid else "free")
            bkey = "zone_" + key
            Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 224, ry - 2, cap, self.ZONE_TIP)
            self.zone_keys.append((bkey, key, zones))
            ry += 26

    FOLD_TIP = "Show its parts"
    UNFOLD_TIP = "Hide its parts"
    NEW_TAG = "(new)"

    def _draw_mods(self, g, x, y, w, h, rows, first):
        Kit.add_section(g, x, y, w, h, "MODULES  (tick a module to turn it on)" if first
                        else "MODULES  (continued)")
        if first:
            xs = x + w - 12 - self.SEARCH_W
            Kit.add_label(g, "Search", xs - 8 - Kit.text_w("Search"), y + 7, Kit.HUE_INFO)
            tb = Kit.add_textbox(g, self.mod_search, xs, y + 5, self.SEARCH_W, numbers=False)
            safe(lambda: tb.SetTooltip("Type part of a name or a feature to list only those "
                                       "modules (an old module's name works too)"))
            self.search_tb, self.search_text = tb, None
        ry = y + 32
        for row in rows:
            if row[0] == "part":
                s, p, lines, hit = row[1], row[2], row[3], row[4]
                cb = Kit.add_check(g, p[1], x + 36, ry, bool(s.parts_on.get(p[0])),
                                   "%s: %s" % (s.title, p[2] or p[1]))
                self._hook_box(cb)
                self.part_boxes.append((s, p[0], cb))
                self.seen["%s.%s" % (s.key, p[0])] = bool(s.parts_on.get(p[0]))
                xd = x + 236
                for k, line in enumerate(lines):
                    Kit.add_label(g, line, xd, ry + 2 + 20 * k, Kit.HUE_INFO)
                tag = "<- found" if hit else (self.NEW_TAG if not p[4] else "")
                if tag:
                    tw = Kit.text_w(lines[0]) if lines else 0
                    Kit.add_label(g, tag, min(xd + tw + 10, x + w - 12 - Kit.text_w(tag)), ry + 2,
                                  Kit.HUE_TITLE if hit else Kit.HUE_INFO)
                ry += 26 + 20 * (len(lines) - 1)
                continue
            if row[0] != "mod":
                Kit.add_label(g, row[1].upper() if row[0] == "head" else row[1], x + 12, ry + 3,
                              Kit.HUE_TITLE if row[0] == "head" else Kit.HUE_INFO)
                ry += 24
                continue
            s, broken, lines = row[1], row[2], row[3]
            if broken:
                Kit.add_label(g, s.title, x + 36, ry + 2, Kit.HUE_INFO)
            else:
                cb = Kit.add_check(g, s.title, x + 12, ry, s.enabled, s.desc)
                self._hook_box(cb)
                self.boxes[s.key] = cb
                self.box_list.append((s, cb))
                self.seen[s.key] = s.enabled
                if s.parts:                          # the fold arrow, left of the description
                    arrow = ">" if s.folded else "v"
                    Kit.add_label(g, arrow, x + 184, ry + 2, Kit.HUE_TITLE)
                    Kit.catcher(g, x + 178, ry, 18, 22,
                                self._fold_click(s.key),
                                self.FOLD_TIP if s.folded else self.UNFOLD_TIP)
                    self.fold_keys.append(("fold_" + s.key, s.key))
            for k, line in enumerate(lines):
                Kit.add_label(g, line, x + 200, ry + 2 + 20 * k,
                              Kit.HUE_BAD if broken else Kit.HUE_INFO)
            ry += 26 + 20 * (len(lines) - 1)

    def _fold_click(self, key):
        store = self.store

        def hit():
            Kit.clicks_seen = True
            store[1]["fold_" + key] = True
            HOST.poke()
        return hit

    def _draw_opts(self, g, x, y, w, h, lines, split):
        host = self.host
        Kit.add_section(g, x, y, w, h)
        ly = y + 8
        for line in lines:
            Kit.add_label(g, line, x + 30, ly, Kit.HUE_INFO)
            ly += 22
        self.snap_cb = Kit.add_check(g, self.SNAP_CAP, x + 30, ly, SNAP.enabled)
        self.debug_cb = Kit.add_check(g, self.DEBUG_CAP, x + 30, ly + 24, host.debug)
        self._hook_box(self.snap_cb)
        self._hook_box(self.debug_cb)
        ly += 48
        self.lag_lbl = Kit.add_label(g, "", x + 30, ly, Kit.HUE_INFO)
        self.lag_next = 0.0
        if split:                            # too narrow for both on one row
            ly += 24
            Kit.add_label(g, "Grid px", x + 30, ly, Kit.HUE_INFO)
            gx = x + 30 + Kit.text_w("Grid px") + 8
        else:
            gx = x + w - 12 - 50
            Kit.add_label(g, "Grid px", gx - Kit.text_w("Grid px") - 8, ly, Kit.HUE_INFO)
        self.grid_tb = Kit.add_textbox(g, str(host.grid_size()), gx, ly - 2, 44)
        safe(lambda: self.grid_tb.SetTooltip(
            "Spacing of the screen grid in pixels; windows snap to its lines and to the "
            "screen's corners, edges and centre (the Action Bar's Grid button shows it)"))

    # ---- resizing and scaling ----
    def _on_resized(self, *args):
        """A step of a corner drag (from the client, about every 75 ms). The
        window's own panel shows meanwhile, as a preview of the new size."""
        first = not self.resize_at
        self.resize_at = time.time()
        g = self.g
        if first and self.mode == "full" and Kit.is_open(g):
            safe(lambda: g.SetAlpha(0.55))

    def _relayout(self):
        """The corner drag was let go: that size is the new room to fill."""
        g = self.g
        if self.mode != "full" or not Kit.is_open(g):
            return
        try:
            w, h = int(g.GetWidth()), int(g.GetHeight())
            x, y = int(g.GetX()), int(g.GetY())
        except Exception:
            return
        if (w, h) == self.size:
            return
        self.lim_w = max(self.MIN_W, int(round(w / self.scale)))
        self.lim_h = max(self.MIN_H, int(round(h / self.scale)))
        self.x, self.y = x, y
        self.build_full(x, y)
        self.host.save_prefs()

    def _step_scale(self, d):
        pcts = list(self.SCALES)
        cur = int(round(self.scale * 100))
        i = min(range(len(pcts)), key=lambda k: abs(pcts[k] - cur))
        i = max(0, min(len(pcts) - 1, i + d)) if d else pcts.index(100)
        if pcts[i] != cur:
            self.scale = pcts[i] / 100.0
            self.redraw()

    def _reset(self):
        """Forget the controls of the window that is being replaced."""
        self._leave_page()
        self.search_tb, self.search_text, self.search_at = None, None, 0.0
        self.store, self.boxes = ({}, {}), {}
        self.page_keys, self.box_list = [], []
        self.zone_keys = []                      # ("zone_<key>", key, [zone ids]) (2.6.55)
        self.snap_cb = self.lag_lbl = self.debug_cb = None
        self._prof_reset()

    def _build_full(self, x, y):
        self._reset()
        self.seen, self.grid_tb, self.resize_at = {}, None, 0.0
        self.grid_text = None
        self.part_boxes, self.fold_keys = [], []
        M, GAP = Kit.MARGIN, Kit.GAP
        L = M
        slots, pages, page = self._context()
        y_title = M
        y_prof = y_title + 34 + GAP              # the profile bar, on both tabs
        y_body = self._body_y()

        if self.tab == "settings" and page is not None:
            units, CW = self._units_settings(pages, page, L, y_body)
        elif self.tab == "settings" and self.loading is not None and pages:
            units, CW = self._units_loading(pages, self.loading.title)
        else:
            units, CW = self._units_modules(slots)
        placed = self._flow(units, CW)
        n_cols = 1 + max([p[1] for p in placed] or [0])
        W = 2 * M + n_cols * CW + (n_cols - 1) * GAP
        H = y_body + max([p[2] + p[5] for p in placed] or [40]) + M
        IW = W - 2 * M
        S = self.scale
        WS, HS = int(round(W * S)), int(round(H * S))

        try:                                     # resizable by its corners
            g = G.CreateModernGump(x, y, WS, HS, True, int(self.MIN_W * S),
                                   int(self.MIN_H * S), self._on_resized)
            safe(lambda: g.SetAlpha(0))          # its own panel hides under the stone
        except Exception:
            g = G.CreateGump(True, True)         # a build without resizable windows
        Kit.add_window_frame(g, W, H, mouse=False)   # corners free for the drag

        # title bar: name, version, the tabs; scale, minimize and close at the right
        Kit.add_section(g, L, y_title, IW, 34)
        Kit.add_label(g, "VIRTUE ASSISTANT", L + 30, y_title + 9, Kit.HUE_TITLE)
        xv = L + 30 + Kit.text_w("VIRTUE ASSISTANT") + 12
        Kit.add_label(g, "v" + APP_VERSION, xv, y_title + 9, Kit.HUE_INFO)
        xt = xv + Kit.text_w("v" + APP_VERSION) + 16
        Kit.title_catcher(g, L, y_title, xt - 6 - L, 34,
                          lambda: self.store[1].__setitem__("min", True), key="va")
        for key, text in self.TABS:
            on = key == self.tab
            Kit.art_button(g, self.store, "tab_" + key, Kit.ART_PAGE, xt, y_title + 6, text,
                           "Show the %s tab" % text, Kit.HUE_TITLE if on else Kit.HUE_INFO)
            xt += self._cap_w(Kit.ART_PAGE, text) + 16
        pct = "%d%%" % int(round(S * 100))
        xp = W - M - 74 - Kit.DOCK_DX - 8 - 16   # +, the percentage, - (right to left)
        Kit.art_button(g, self.store, "scale_up", self.ART_MORE, xp, y_title + 9, None,
                       "Larger window and text")
        xl = xp - 6 - Kit.text_w(pct)
        Kit.add_label(g, pct, xl, y_title + 9, Kit.HUE_TEXT)
        Kit.catcher(g, xl - 2, y_title + 6, Kit.text_w(pct) + 4, 22,
                    lambda: self.store[1].__setitem__("scale_reset", True),
                    "The window's scale (click for 100%)")
        Kit.art_button(g, self.store, "scale_down", self.ART_LESS, xl - 6 - 16, y_title + 9,
                       None, "Smaller window and text")
        Kit.dock_button(g, self.store, W - M - 74, y_title + 9)
        Kit.art_button(g, self.store, "min", Kit.ART_MIN, W - M - 74, y_title + 9, None,
                       "Minimize to the gear (double-click the title does too)")
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, y_title + 6,
                       None, "Close Virtue Assistant (stops every module)")
        try:
            self._build_profiles(g, L, y_prof, IW)
        except Exception as ex:
            self.prof_dd_args = None
            Kit.add_label(g, "Profiles unavailable: %s" % ex, L + 12, y_prof + 9, Kit.HUE_BAD)

        # the sections, in their columns (the settings page's bands come last
        # and the page is drawn with the last one, so its drop-downs are on top)
        for u, col, top, i, j, h in sorted(placed, key=lambda p: p[0]):
            units[u]["draw"](g, L + col * (CW + GAP), y_body + top, h, i, j)

        safe(lambda: self._add_profile_list(g))  # last of all: its list opens on top
        if not Kit.scale_window(g, S) and S != 1.0:
            self.scale, S, WS, HS = 1.0, 1.0, W, H    # this client can't scale it
            safe(lambda: API.SysMsg("%s: this TazUO build can't scale the window; it stays "
                                    "at 100%%." % APP_NAME, Kit.HUE_BAD))
        self._replace(g, "full", x, y, WS, HS, int(round(y_body * S)))
        fit = Kit.scroll_info(g)                 # taller than the screen: it scrolls now
        self.size = (fit["w2"], fit["hv"]) if fit else (WS, HS)
        self.minimized = False
        self.dirty = None
        if self.search_focus:                    # typing in the search box goes on
            self.search_focus = False
            tb = self.search_tb
            if tb is not None:
                cc = Kit.client_control(tb)
                if cc is not None and Kit.flush():
                    safe(lambda: cc.SetKeyboardFocus())

    def build_gear(self, x, y):
        self._reset()
        S = self.GEAR
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, S, S, corners=False)
        Kit.add_section(g, 7, 7, S - 14, S - 14)
        drawn = False
        try:
            p = G.CreateGumpItemPic(GEAR_ITEM, S - 18, S - 18)
            p.SetPos(9, 9)
            safe(lambda: p.SetAcceptMouseInput(False))
            g.Add(p)
            drawn = True
        except Exception:
            pass
        if not drawn:
            Kit.add_label(g, "VA", S // 2 - 8, S // 2 - 8, Kit.HUE_TITLE)
        Kit.catcher(g, 0, 0, S, S, self._gear_click,
                    "%s: click to open, drag to move" % APP_NAME, movable=True)
        self.gear_clicked = False
        self.gear_pos = None
        self.gear_moved = 0.0
        self._replace(g, "gear", x, y, S, S)
        self.minimized = True
        # docked: the gear is hidden, the bar stands in for it
        self.docked = self.host.dock_wanted(self.DOCK_KEY) and self.host.bar_alive()
        if self.docked:
            self._show_gear(False)

    # ---------- Action Bar link ----------
    def fold_to_bar(self):
        """The gold arrow / the bar's button: fold into the bar (or, with no
        bar up, into the gear until the bar comes)."""
        self.host.dock_want_set(self.DOCK_KEY, True)
        if self.mode == "full":
            self.fold()
        if not self.host.bar_alive():
            self.host.dock_note(APP_NAME)

    def _show_gear(self, shown):
        g = self.g
        if self.mode == "gear" and Kit.is_open(g):
            safe(lambda: setattr(g, "IsVisible", bool(shown)))

    def link_tick(self):
        """Commands from the Action Bar, and this window's state for it
        (shared variables, read every 0.1 s)."""
        now = time.time()
        if now < self.link_next and self.link_next - now <= 0.1:    # (2.6.84: or the clock went back)
            return
        self.link_next = now + 0.1
        key = self._take_shared(self.LINK_ENABLE)
        if key:
            self.host.enable(str(key))
        cmd = self._take_shared(self.LINK_CMD)
        if cmd:
            cmd = str(cmd)
            if cmd == "show" and self.mode != "full":
                self.unfold()
            elif cmd == "dock" and self.mode == "full":
                self.fold_to_bar()
            elif cmd == "modules":
                self.request_tab = "modules"
        want = self.host.dock_wanted(self.DOCK_KEY)
        if self.mode == "gear" and (self.docked or want):
            hide = want and self.host.bar_alive()
            if hide != self.docked:               # bar opened / went away
                self.docked = hide
                self._show_gear(not hide)
        state = ("docked" if self.docked else "gear") if self.mode == "gear" else "open"
        if state != self.link_state:
            self.link_state = state
            safe(lambda: API.SetSharedVar(self.LINK_STATE, state))

    @staticmethod
    def _take_shared(name):
        """A shared variable's value, cleared once read (None if unset)."""
        try:
            v = API.GetSharedVar(name)
        except Exception:
            return None
        if v:
            try:
                API.RemoveSharedVar(name)
            except Exception:
                pass
        return v

    def _gear_click(self):
        self.gear_clicked = True

    def pos(self):
        g = self.g
        try:
            x = int(g.GetX())
        except Exception:
            x = None
        try:
            y = int(g.GetY())
        except Exception:
            y = None
        return x, y

    def store_prefs(self, prefs):
        if Client.on_client_thread():
            self._note_pos()                  # free here; off the client thread the window's
            #                                   place is already known (Kit.on_moved, _replace)
        prefs["cfg_x"], prefs["cfg_y"] = str(self.x), str(self.y)
        prefs["cfg_w"], prefs["cfg_h"] = str(self.lim_w), str(self.lim_h)
        prefs["cfg_scale"] = str(int(round(self.scale * 100)))
        prefs["gear_x"], prefs["gear_y"] = str(self.gx), str(self.gy)
        prefs["cfg_min"] = "1" if self.minimized else "0"
        prefs["cfg_tab"] = self.tab
        prefs["cfg_page"] = self.page or ""
        prefs["snap"] = "1" if SNAP.enabled else "0"
        prefs["debug"] = "1" if self.host.debug else "0"

    def fold(self):
        x, y = self.pos()
        if x is not None:
            self.x, self.y = x, y
        self.gx, self.gy = self.x, self.y
        self.build_gear(self.gx, self.gy)
        self.host.save_prefs()

    def unfold(self):
        x, y = self.pos()
        if x is not None:
            self.gx, self.gy = x, y
        self.docked = False
        self.host.dock_forget(self.DOCK_KEY)      # shown again: no longer folded
        self.build_full(self.gx, self.gy)
        self.host.save_prefs()

    def redraw(self):
        """Rebuild the full window where it stands (tab or page change)."""
        if self.mode != "full":
            self.unfold()
            return
        x, y = self.pos()
        if x is not None:
            self.x, self.y = x, y
        self.build_full(self.x, self.y)
        self.host.save_prefs()

    def show_settings(self, key):
        """Asked for by a module (its Settings button): open its settings page."""
        self.request = key

    def refresh(self, key):
        """A module changed its settings itself: redraw them if they're showing.
        The page's controls still show the old settings, so they are not read
        one last time when it goes (see _leave_page): that read would save the
        old values over the ones the module just set."""
        self.forget_measure(key)
        if self.shown_page == key:
            self.dirty = key
            self.stale_page = key

    def close(self):
        self.closing = True
        self._leave_page()
        g, self.g = self.g, None
        Kit.dispose(g)
        self.docked, self.link_state = False, None
        safe(lambda: API.SetSharedVar(self.LINK_STATE, "off"))

    # ---------- every pass ----------
    #  Polled 20 times a second on the client thread, so it reads as little as
    #  it can: the buttons are looked at only when one of them was clicked (the
    #  click handlers note it; until any handler has run the client is asked
    #  too, see Kit.was_clicked), the boxes are read straight (no lambda per
    #  read), the grid field is parsed only when its text changed.
    def poll(self):
        if self.closing:
            return
        if not Kit.is_open(self.g):
            # closed some other way: keep a handle on screen
            if self.host.stopping():
                return
            self.shown_page = None
            self.build_gear(self.gx, self.gy)
            return
        g = self.g
        self.link_tick()
        if self.g is not g and not Kit.is_open(self.g):
            return
        if self.request is not None:
            key, self.request = self.request, None
            self.tab, self.page = "settings", key
            self.redraw()
            return
        if self.request_tab is not None:
            tab, self.request_tab = self.request_tab, None
            if tab in ("modules", "settings"):
                self.tab = tab
            self.redraw()
            return
        if self.mode == "gear":
            now = time.time()
            # (2.6.82) the gear can only be dragged while the button is held: its
            # place is read then (and on the click), not 20 times a second all session
            if not self.docked and (self.gear_clicked or self.gear_pos is None
                                    or now >= self.gear_look
                                    or SNAP.pressed() is not False):
                self.gear_look = now + 0.5           # (a code move is seen within this)
                p = self.pos()
                if p != self.gear_pos:
                    if self.gear_pos is not None:
                        self.gear_moved = now
                    self.gear_pos = p
            if self.gear_clicked:
                self.gear_clicked = False
                if now - self.gear_moved > 0.35:   # a drag ends in a click too
                    self.unfold()
            return

        if self.prof_redraw:                     # a profile came or went on disk
            self.prof_redraw = False
            self.redraw()
            return
        if self.redraw_req:                      # a page's file came in (see loaded)
            self.redraw_req = False
            if self.tab == "settings":
                self.redraw()
                return
        if self.resize_at and time.time() - self.resize_at >= self.SETTLE \
                and not SNAP.pressed():
            self.resize_at = 0.0                 # a corner drag was let go
            self._relayout()
            return
        if self._poll_buttons():
            return
        # (2.6.82) the profile drop-down, the search box and the grid field are
        # read fast only after input (Host.poll_due), every PAGE_EVERY s otherwise
        self._fld_due = self.host.poll_due(self._fld_gate)
        self._poll_profiles()
        if self.search_tb is not None and self._fld_due and self._poll_search():
            return

        if self.lag_lbl is not None and time.time() >= self.lag_next:
            self.lag_next = time.time() + 1.0
            running = self.host.active
            if running:
                worst = running[0]
                for s in running:
                    if s.worst_ms > worst.worst_ms:
                        worst = s
                text = "Loop: %d modules on; slowest tick lately %s, %d ms (decays)" % (
                    len(running), worst.title, worst.worst_ms)
            else:
                text = "Loop: no modules on"
            Kit.set_text(self.lag_lbl, text)
        if self.grid_tb is not None and self._fld_due:
            try:
                t = self.grid_tb.Text
            except Exception:
                t = None
            if t != self.grid_text:              # parsed only when it changed
                self.grid_text = t
                try:
                    v = int(str(t or "").strip() or 0)
                except Exception:
                    v = 0
                if 8 <= v <= 512 and v != self.host.grid_size():
                    self.host.prefs["grid"] = str(v)
                    self.host.save_prefs()
                    if self.host.grid is not None:
                        self.host.grid.redraw()
        now = time.time()
        if self.box_hit or now >= self.box_next or not Kit.clicks_seen:
            self.box_hit = False
            self.box_next = now + self.BOX_EVERY
            if self._poll_boxes():
                return

        # (2.6.82) no page lookup on the Modules tab (no page shown)
        s = self.host.page_slot(self.shown_page) if self.shown_page is not None else None
        if self.stale_page is not None and self.stale_page == self.shown_page:
            s = None          # changed by its module: drawn again below, not read (refresh)
        if s is not None and s.api is not None and s.api.get("poll_config"):
            if self._pp_key != self.shown_page:  # (2.6.82) a page just shown: read it now
                self._pp_key = self.shown_page
                self._pp_gate[0] = 0.0
            if self.host.poll_due(self._pp_gate, s.api.get("poll_every")):
                try:
                    s.api["poll_config"]()
                except Exception as ex:
                    self._settings_error(s, "update", ex)
        if self.dirty is not None and self.dirty == self.shown_page:
            self.redraw()

    def _poll_search(self):
        """The Modules tab's search box: it filters SEARCH_SETTLE seconds after
        the last key (the tab is drawn again, the box keeps the keyboard).
        True when the window was drawn again."""
        try:
            t = str(self.search_tb.Text or "")
        except Exception:
            return False
        now = time.time()
        if t != self.search_text:
            if self.search_text is not None:
                self.search_at = now
            self.search_text = t
            return False
        if self.search_at and now - self.search_at >= SEARCH_SETTLE:
            self.search_at = 0.0
            if t.strip().lower() != self.mod_search.strip().lower():
                self.mod_search = t.strip()
                self.search_focus = True
                self.redraw()
                return True
        return False

    #  A checkbox changes only when it is clicked, so the checkboxes are read
    #  after a click on one of them (their click hook below notes it and pokes
    #  the host) and, as a safety net, once every BOX_EVERY seconds. Until any
    #  click handler has been seen to run (Kit.clicks_seen) they are read on
    #  every poll, as before. (The grid field is typed into: read every poll.)
    BOX_EVERY = 1.0

    def _hook_box(self, cb):
        """Note clicks on a checkbox (the checkbox toggles itself as always)."""
        if cb is None:
            return

        def hit(*args):
            Kit.clicks_seen = True
            self.box_hit = True
            HOST.poke()
        try:
            G.AddControlOnClick(cb, hit)
        except Exception:
            pass

    def _poll_boxes(self):
        """The Snap and Debug boxes and the module switches. True when the
        window went away or was folded meanwhile."""
        if self.snap_cb is not None:
            try:
                v = bool(self.snap_cb.IsChecked)
            except Exception:
                v = SNAP.enabled
            if v != SNAP.enabled:
                SNAP.enabled = v
                if not v:
                    SNAP.links.clear()
                self.host.save_prefs()
        if self.debug_cb is not None:
            try:
                v = bool(self.debug_cb.IsChecked)
            except Exception:
                v = self.host.debug
            if v != self.host.debug:
                self.host.debug = v
                self.host.save_prefs()
        seen = self.seen
        for s, cb in self.box_list:
            try:
                v = bool(cb.IsChecked)
            except Exception:
                v = s.enabled
            if v != seen.get(s.key):
                seen[s.key] = v
                if v:
                    self.host.enable(s.key)
                else:
                    self.host.disable(s.key)
                if not Kit.is_open(self.g) or self.mode != "full":
                    return True
            elif v != s.enabled:                    # switched off by the module
                try:
                    cb.SetIsChecked(s.enabled)
                except Exception:
                    pass
                seen[s.key] = s.enabled
        for s, pk, cb in self.part_boxes:            # the parts' boxes (2.6.5)
            sk = "%s.%s" % (s.key, pk)
            try:
                v = bool(cb.IsChecked)
            except Exception:
                v = bool(s.parts_on.get(pk))
            if v != seen.get(sk):
                seen[sk] = v
                self.host.part_set(s.key, pk, v)
                if not Kit.is_open(self.g) or self.mode != "full":
                    return True
            elif v != bool(s.parts_on.get(pk)):      # changed by the module or the host
                try:
                    cb.SetIsChecked(bool(s.parts_on.get(pk)))
                except Exception:
                    pass
                seen[sk] = bool(s.parts_on.get(pk))
        return False

    def _poll_buttons(self):
        """The title bar's buttons, the tabs and the page buttons. True when
        one acted (the window may have been rebuilt)."""
        store = self.store
        if Kit.clicks_seen and True not in store[1].values():
            return False                         # nothing was clicked
        if Kit.was_clicked(store, "close"):
            self.host.save_prefs()
            self.host.quitting = True
            return True
        if Kit.was_clicked(store, "min"):
            self.host.dock_forget(self.DOCK_KEY)  # Minimize: the gear, not the bar
            self.fold()
            return True
        if Kit.was_clicked(store, "tobar"):
            self.fold_to_bar()
            return True
        for key, d in (("scale_down", -1), ("scale_up", 1), ("scale_reset", 0)):
            if Kit.was_clicked(store, key):
                self._step_scale(d)
                return True
        for key, _ in self.TABS:
            if Kit.was_clicked(store, "tab_" + key) and key != self.tab:
                self.tab = key
                self.redraw()
                return True
        for bkey, key in self.page_keys:
            if Kit.was_clicked(store, bkey) and key != self.shown_page:
                self.page = key
                self.redraw()
                return True
        for bkey, key in self.fold_keys:          # a module's fold arrow (2.6.5)
            if Kit.was_clicked(store, bkey):
                s = dict.get(self.host.by_key, key)
                if s is not None:
                    s.folded = not s.folded
                self.redraw()
                return True
        for bkey, key, zones in self.zone_keys:   # a window's Zone button (2.6.55)
            if Kit.was_clicked(store, bkey):
                cur = LAYOUT.zone_of(key)
                i = zones.index(cur) if cur in zones else 0
                nxt = zones[(i + 1) % len(zones)] if zones else None
                mz = LAYOUT._map_zone()              # (2.6.73) the map's zone is passed over
                if nxt is not None and key != "worldmap" and nxt == mz and len(zones) > 2:
                    nxt = zones[(i + 2) % len(zones)]
                LAYOUT.assign_to(key, nxt)
                self.redraw()
                return True
        return False


# =============================================================================
#  The shared floating window: one window for the modules that ask for a
#  section in it (Ultima Tracker's controls; until 2.6.51 also Guild Pings,
#  when it was called "Tracker & Pings"). The
#  modules draw their own sections; this adds the title strip, minimize and
#  close. Minimized it is a small strip. Its gold "Fold into the Action Bar"
#  arrow folds it into the bar's tray button instead ("docked"), coming back
#  as the strip when the bar goes away. Closing it turns its modules off.
# =============================================================================
class HubWindow(object):
    W = 372
    MINI_W, MINI_H = 240, 46

    def __init__(self, host):
        self.host = host
        self.g = None
        self.H = 0
        self.sections = []        # [(key, title, hooks)] in the order they were added
        self.stores = {}          # key -> (buttons, clicks) store of that section
        self.store = ({}, {})
        self.x, self.y = Kit.adapt(host.pref_int("hub_x", 100), host.pref_int("hub_y", 100),
                                   self.W, self.MINI_H)
        self.minimized = host.pref_int("hub_min", 0) == 1 or host.dock_wanted("hub")
        self.docked = False
        self.dirty = False
        self.closing = False
        self._gates = {}          # (2.6.82) section key -> [when its poll is due next]
        host.dock_add("hub", {"title": "Ultima Tracker", "icon": HUB_ITEM, "always": True,
                              "state": self.state, "show": self.show, "dock": self.dock,
                              "undock": self.undock, "minimize": self.minimize,
                              "on": self.open_modules})

    # ---------- what modules call ----------
    #  hooks: "height"(w) -> pixels, "build"(g, x, y, w, store) draws the
    #  section(s) there, "poll"(store) every pass while shown, "closed"()
    #  when the controls go away.
    def add(self, key, title, hooks):
        self.remove(key)
        self.sections.append((key, title, hooks))
        self.dirty = True

    def remove(self, key):
        keep = [s for s in self.sections if s[0] != key]
        if len(keep) == len(self.sections):
            return
        self.sections = keep
        self.stores.pop(key, None)
        if not keep:
            self._close_window()
        else:
            self.dirty = True

    def refresh(self):
        self.dirty = True

    def title(self):
        return self.sections[0][1] if len(self.sections) == 1 else "Ultima Tracker"

    def state(self):
        if not self.sections or self.g is None:
            return None
        return "docked" if self.docked else ("minimized" if self.minimized else "open")

    def show(self):
        self.docked = self.minimized = False
        self.dirty = True

    def dock(self):
        if not self.sections:
            return
        self.minimized = self.docked = True
        self.dirty = True

    def undock(self):
        if self.docked:
            self.docked = False
            self._visible(True)

    def minimize(self):
        if not self.sections:
            return
        self.minimized, self.docked = True, False
        self.dirty = True

    def toggle_min(self):
        self.minimized = not self.minimized
        self.docked = False
        self.host.dock_forget("hub")      # Minimize / Restore: its own strip, not the bar
        self.dirty = True

    def open_modules(self):
        """Nothing is on: show the Modules tab so Ultima Tracker or Map Pings
        can be ticked."""
        if self.host.config is not None:
            self.host.config.request_tab = "modules"

    # ---------- building ----------
    def _visible(self, on):
        g = self.g
        if Kit.is_open(g):
            try:
                g.IsVisible = bool(on)
            except Exception:
                pass

    def _pos(self):
        g = self.g
        if Kit.is_open(g):
            try:
                self.x, self.y = int(g.GetX()), int(g.GetY())
            except Exception:
                pass

    def _leave(self):
        for key, title, hooks in self.sections:
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"):
                # (2.6.83) a last read first, as the settings page does: a change
                # made since the last (throttled) poll isn't lost
                try:
                    hooks["poll"](st_)
                except Exception:
                    pass
            if key in self.stores and hooks.get("closed"):
                safe(hooks["closed"])
        self.stores = {}

    def _close_window(self):
        self._pos()
        self._leave()
        g, self.g = self.g, None
        Kit.dispose(g)
        self.docked = False

    def _part_of(self, key):
        """(2.6.84) A section's key is its part's old key ("ultima" is Ultima
        Tracker's Tracker part): (module key, part key), or (key, None)."""
        m = self.host.old_map.get(key)
        if m is not None and dict.get(self.host.by_key, m[0]) is not None:
            return m
        return key, None

    def _off(self, key):
        """Turn a section's own part off (not the module's other parts)."""
        mk, pk = self._part_of(key)
        self.host.disable(("%s.%s" % (mk, pk)) if pk is not None else key)

    def _error(self, key, ex):
        mk, pk = self._part_of(key)
        s = dict.get(self.host.by_key, mk)
        if s is not None:
            self.host.report(s, ex, None, pk)

    def build(self):
        """The window in one hop on the client thread (see Kit.on_client)."""
        Kit.on_client(self._build)

    def _build(self):
        self.dirty = False
        if not self.sections:
            self._close_window()
            return
        self._pos()
        self._leave()
        old = self.g
        M, GAP = Kit.MARGIN, Kit.GAP
        store = ({}, {})
        g = G.CreateGump(True, True)
        title = self.title().upper()
        close_tip = "Close %s (turns %s off; the Modules tab turns %s back on)" % (
            self.title(), "them" if len(self.sections) > 1 else "it",
            "them" if len(self.sections) > 1 else "it")
        if self.minimized:
            w, h = self.MINI_W, self.MINI_H
            Kit.add_window_frame(g, w, h, corners=False)
            Kit.add_section(g, 8, 8, w - 16, h - 16)
            Kit.add_label(g, title, 18, 15, Kit.HUE_TITLE)
            Kit.title_catcher(g, 8, 8, w - 70, h - 16, self.toggle_min, key="hub:mini")
            Kit.art_button(g, store, "min", Kit.ART_RESTORE, w - 60, 15, None, Kit.RESTORE_TIP)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - 44, 12, None, close_tip)
        else:
            w = self.W
            IW = w - 2 * M
            heights = [max(20, int(safe(lambda: hooks["height"](IW), 40) or 40))
                       for key, t, hooks in self.sections]
            h = M + 30 + GAP + sum(heights) + GAP * (len(heights) - 1) + M
            Kit.add_window_frame(g, w, h, corners=False)
            Kit.add_section(g, M, M, IW, 30)
            Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
            Kit.title_catcher(g, M, M, IW - 70 - Kit.DOCK_DX, 30, self.toggle_min, key="hub")
            Kit.dock_button(g, store, w - M - 66, M + 7)
            Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 66, M + 7, None, Kit.MIN_TIP)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 44, M + 4, None, close_tip)
            y = M + 30 + GAP
            for (key, t, hooks), sh in zip(self.sections, heights):
                st_ = ({}, {})
                self.stores[key] = st_
                try:
                    hooks["build"](g, M, y, IW, st_)
                except Exception as ex:
                    Kit.add_section(g, M, y, IW, sh)
                    Kit.add_label(g, "%s: %s" % (t, ex), M + 10, y + 10, Kit.HUE_BAD)
                    self._error(key, ex)
                y += sh + GAP
        self.H = h
        self.x, self.y = Kit.place(g, self.x, self.y, w, h)   # wholly on screen
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        self.g, self.store = g, store
        G.AddControlOnDisposed(g, lambda *a: self._disposed(g))
        G.AddGump(g)
        safe(lambda: g.SetInScreen())
        Kit.on_moved(g, self._moved)
        Kit.dispose(old)
        if self.docked:
            self._visible(False)

    def _moved(self):
        """Dragged and let go: remember where, right away."""
        self._pos()
        self.host.save_prefs()

    def _disposed(self, g):
        """Closed some other way than our buttons: that turns its modules off."""
        if self.g is g and not self.closing:
            self.g = None
            self.stores = {}
            for key, t, hooks in list(self.sections):
                safe(hooks.get("closed", lambda: None))
                self._off(key)

    def store_prefs(self, prefs):
        if Client.on_client_thread():
            self._pos()                       # free here; otherwise known from _moved
        prefs["hub_x"], prefs["hub_y"] = str(self.x), str(self.y)
        prefs["hub_min"] = "1" if self.minimized else "0"

    def close(self):
        self.closing = True
        self._close_window()

    # ---------- every pass ----------
    def poll(self):
        if self.closing:
            return
        if self.dirty:
            self.build()
            if self.sections and self.host.pref_int("hub_min", 0) != int(self.minimized):
                self.host.save_prefs()        # minimized / restored: kept for next start
        g = self.g
        if g is None:
            return
        if not Kit.is_open(g):
            self.g = None
            return
        if Kit.clicks_seen and True not in self.store[1].values():
            pass                          # none of its buttons was clicked
        elif Kit.was_clicked(self.store, "close"):
            self._pos()
            for key, t, hooks in list(self.sections):
                self._off(key)
            return
        elif Kit.was_clicked(self.store, "min"):
            self.toggle_min()
            self.build()
            self.host.save_prefs()
            return
        elif Kit.was_clicked(self.store, "tobar"):
            self.host.dock_to_bar("hub", self.title())
            if self.dirty:
                self.build()
            self.host.save_prefs()
            return
        if self.docked or self.minimized:
            return                        # (dock_tick brings it back when the bar goes)
        for key, t, hooks in list(self.sections):
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"):
                gate = self._gates.get(key)          # (2.6.82) fast only after input
                if gate is None:
                    gate = self._gates[key] = [0.0]
                if not self.host.poll_due(gate, hooks.get("poll_every")):
                    continue
                try:
                    hooks["poll"](st_)
                except Exception as ex:
                    self._error(key, ex)


# =============================================================================
#  Snap - windows dock to one another. While a window is dragged it is
#  watched; when it is let go within SNAP_DIST pixels of another window it
#  jumps so that a corner of it meets a corner of that window (side by side
#  or stacked, edges flush) - corners first - or, failing that, so one edge
#  lines up. A window that snapped on to another follows it when that one is
#  dragged; dragging it away on its own unhooks it. Every gump the script
#  adds takes part (G.AddGump registers them). Nothing can be dragged while
#  the mouse button is up, so when the client says whether it's held the
#  windows are only measured while it is.
#
#  The keeper (Snap.keep, every KEEP_EVERY seconds while nothing is being
#  dragged): every window the script added is wholly on screen, always. One
#  that is off (it opened there, grew, was dragged half off and let go, the
#  client window shrank) is moved back the shortest way, with the windows
#  attached to it (Kit.attach), and its module is told (Kit.on_moved) so the
#  place it saves is the one on screen. When the client window changes size
#  every window first keeps its place relative to the screen anchor it is
#  nearest (Kit.remap_axis), so a window in a corner stays in that corner.
# =============================================================================
SNAP_DIST = 16             # pixels within which a let-go window snaps
SNAP_SETTLE = 0.25         # seconds at rest that count as "let go" if the mouse can't be read
SNAP_EVERY = 0.08          # seconds between looks at where the windows are


SNAP_PRUNE = 2.0           # seconds between sweeps of closed windows while the button is up


class Snap(object):
    """Windows are keyed by the window itself (not id(): in IronPython id() of
    a client object is a slow lookup), membership is a set (not a scan of the
    list on every AddGump), and closed windows are let go of every SNAP_PRUNE
    seconds even while nothing is dragged (they used to wait for the next
    mouse press, holding their on_moved callbacks and controls)."""
    def __init__(self):
        self.gumps = []            # windows the script added, still open (in order added)
        self.members = set()       # the same windows, for a quick "is it in?"
        self.last = None           # gump -> (x, y) last seen; None = measure again
        self.drag = {}             # gump -> time it last moved under the mouse
        self.links = {}            # follower gump -> leader gump
        self.button = None         # getter for Mouse.LButtonPressed, or False
        self.enabled = True
        self.next = 0.0
        self.prune_at = 0.0        # next sweep of closed windows
        self.moved_cb = {}         # gump -> fn: told when it was moved and let go
        self.moved = set()         # gumps moved by the drag going on now
        self.attached = {}         # follower gump -> leader gump (Kit.attach)
        self._fmap = None          # (2.6.82) leader -> [open followers], for one keeper pass
        self._esc_names = ("ESC", "ESCAPE")
        self.no_snap = set()       # windows that never snap, lead or follow (Kit.no_snap)
        self.keep_at = 0.0         # next look for a window off the screen
        self.screen = None         # (W, H) the windows were last kept on
        self.by_code = {}          # gump -> time a module placed it (moved_by_code): the
        #                            SetPos lands on a later frame, so the next change of
        #                            place seen is that move, not a drag
        self.dragged = set()       # gumps moved by the mouse in the drag going on now
        self.droppers = []         # fn(gump) told when a dragged window is let go (on_drop)
        self.drag_end = {}         # (2.6.74) gump -> when a drag of it ended (Kit.just_dragged)
        self.drag_key = {}         # (2.6.74) gump -> its layout key, noted while it is dragged
        self.drag_rect = {}        # (2.6.74) gump -> its rect last seen while dragged
        self.lost = {}             # (2.6.74) dragged gump closed mid-drag -> (its key, its rect)

    def add(self, g):
        if g is not None and g not in self.members:
            self.members.add(g)
            self.gumps.append(g)

    def on_moved(self, g, fn):
        """fn() once the player has moved g and let go (see Kit.on_moved)."""
        if g is None:
            return
        try:
            if g not in self.attached:       # a follower (Kit.attach) never snaps on its own
                self.add(g)
            self.moved_cb[g] = fn
        except TypeError:                    # not a window it can keep track of
            pass

    def on_drop(self, fn):
        """fn(g) after the player dragged window g and let go of it (2.6.54:
        the layout slots or frees it); never for a move made by code."""
        if fn not in self.droppers:
            self.droppers.append(fn)

    def _tell_moved(self):
        """The drag is over: every window it moved saves where it is now;
        the ones the mouse itself moved are offered to the drop listeners."""
        moved, self.moved = self.moved, set()
        dragged, self.dragged = self.dragged, set()
        for g in moved:
            fn = self.moved_cb.get(g)
            if fn is None:
                continue
            if Kit.is_open(g):
                try:
                    fn()
                except Exception:
                    pass
        now = time.time()
        for g in dragged:
            self.drag_end[g] = now               # (2.6.74) Kit.just_dragged
        if len(self.drag_end) > 32:
            for g in [g for g, t in self.drag_end.items() if now - t > 5.0]:
                del self.drag_end[g]
        keys, rects = self.drag_key, self.drag_rect
        self.drag_key, self.drag_rect = {}, {}
        lost, self.lost = self.lost, {}
        for g in dragged:
            if g in moved and Kit.is_open(g):
                for fn in self.droppers:
                    try:
                        fn(g)
                    except Exception as ex:
                        LAYOUT.debug_line("the drop of a window failed: %s%s" % (ex, _error_where()))
                continue
            if keys.get(g) is not None and rects.get(g) is not None:
                lost[g] = (keys[g], rects[g])
        # (2.6.74) a window made anew while it was dragged (its module rebuilt it): the
        # drop goes to the window that stands for it now, at the place the dragged one
        # was let go (2.6.73 lost the drop: nothing was slotted)
        done = set()
        for g, (key, r) in lost.items():
            if key in done:
                continue
            done.add(key)
            LAYOUT.debug_line("%s (%s) was made anew during the drag; its drop goes to the new "
                              "window" % (LAYOUT.title_of(key), key))
            for fn in self.droppers:
                try:
                    fn(None, key=key, rect=r)
                except Exception as ex:
                    LAYOUT.debug_line("the drop of a window failed: %s%s" % (ex, _error_where()))

    def moved_by_code(self, g):
        """Window g was just placed by code (see Kit.moved_by_code): its new
        place is what it was last seen at, so the move is not taken for a drag."""
        if g is None:
            return
        try:
            p = self.pos(g)
            if self.last is not None and p is not None:
                self.last[g] = p
            self.drag.pop(g, None)
            self.moved.discard(g)
            # the client runs SetPos / SetRect on a later frame while GetX answers
            # at once (see Kit.flush), so p may still be the old place: the next
            # change of place tick() sees for g is this move
            self.by_code[g] = time.time()
        except TypeError:
            pass

    def skip_gump(self, g, keep_fresh=False):
        """A window that follows another by itself (the bar's tray) never snaps.
        (2.6.82) An overlay (grid, frame art, marks, the ping readout) also needs
        no fit by the layout: the keeper pass its AddGump asked for is dropped."""
        if not keep_fresh:
            try:
                LAYOUT.fresh_adds.discard(g)
            except Exception:
                pass
        if g in self.members:
            self.members.discard(g)
            try:
                self.gumps.remove(g)
            except ValueError:
                pass

    def exempt(self, g):
        """g never snaps, follows or is snapped on to (see Kit.no_snap); it is
        still kept on screen and its on_moved callback still runs."""
        if g is None:
            return
        try:
            self.add(g)
            self.no_snap.add(g)
            self.links.pop(g, None)
            for f, l in list(self.links.items()):
                if l is g:
                    self.links.pop(f, None)
        except TypeError:                    # not a window it can keep track of
            pass

    def attach(self, follower, leader):
        """`follower` is placed by its module beside `leader` (see Kit.attach):
        it never snaps on its own; the keeper moves the two as one."""
        if follower is None or leader is None or follower is leader:
            return
        try:
            self.skip_gump(follower, keep_fresh=True)   # (a tray is fitted with its leader)
            self.attached[follower] = leader
            self._fmap = None                # (2.6.82) the pass's followers map is stale
            self.add(leader)
        except TypeError:                    # not a window it can keep track of
            pass

    def detach(self, follower):
        """(2.6.57) Undo attach: the follower is a free window that snaps again."""
        try:
            self._fmap = None                # (2.6.82)
            if self.attached.pop(follower, None) is not None and Kit.is_open(follower):
                self.add(follower)
        except TypeError:
            pass

    def followers(self, g):
        """The open windows attached to g (closed ones are let go of)."""
        fm = self._fmap
        if fm is not None:                   # (2.6.82) inside a keeper pass: one scan for all
            lst = fm.get(g)
            return list(lst) if lst else []
        out = []
        for f, l in list(self.attached.items()):
            if not Kit.is_open(f):
                self._forget(f)              # its callbacks and links too, not only the pair
            elif l is g:
                out.append(f)
        return out

    def _forget(self, g):
        if g in self.dragged:                    # (2.6.74) closed mid-drag (made anew): its
            k, r = self.drag_key.get(g), self.drag_rect.get(g)   # drop is kept for the new one
            if k is not None and r is not None:
                self.lost[g] = (k, r)
        self.drag_key.pop(g, None)
        self.drag_rect.pop(g, None)
        self.members.discard(g)
        Kit._pinned.discard(g)                   # (2.6.74)
        self.drag.pop(g, None)
        self.by_code.pop(g, None)
        self.links.pop(g, None)
        self.moved_cb.pop(g, None)
        self.moved.discard(g)
        self.dragged.discard(g)
        self.no_snap.discard(g)
        self._fmap = None                        # (2.6.82)
        self.attached.pop(g, None)
        for f, l in list(self.attached.items()):
            if l is g:
                self.attached.pop(f, None)
        if self.last is not None:
            self.last.pop(g, None)

    def _prune(self):
        """Drop the windows that were closed; returns the open ones."""
        live = []
        for g in self.gumps:
            if Kit.is_open(g):
                live.append(g)
            else:
                self._forget(g)
        self.gumps = live
        return live

    # ---------- the client ----------
    def pressed(self):
        """Left mouse button held? None when the client won't say."""
        if self.button is None:
            self.button = False
            t = Client._type("ClassicUO.Input.Mouse")
            if t is not None:
                for name in ("LButtonPressed", "LeftButtonPressed"):
                    try:
                        m = Client._member(t, name)
                        bool(m[0]())
                        self.button = m[0]
                        break
                    except Exception:
                        pass
        if not self.button:
            return None
        try:
            v = self.button()
        except Exception:
            return None
        return None if v is None else bool(v)

    @staticmethod
    def rect(g):
        r = Kit.rect(g)                           # (2.6.70) as asked, until it lands
        if r is None or r[2] <= 0 or r[3] <= 0:
            return None
        return r

    @staticmethod
    def pos(g):
        return Kit.pos(g)                         # (2.6.70) as asked, until it lands (2.6.82: x, y only)

    @staticmethod
    def visible(g):
        try:
            return bool(g.IsVisible)
        except Exception:
            return True

    @staticmethod
    def move(g, x, y):
        try:
            g.SetPos(int(x), int(y))
        except Exception:
            safe(lambda: setattr(g, "X", int(x)))
            safe(lambda: setattr(g, "Y", int(y)))
        Kit.note_rect(g, x, y)                    # (2.6.70) read back as asked until it lands

    # ---------- every pass ----------
    def tick(self, now=None):
        now = time.time() if now is None else now
        if now < self.next and self.next - now <= SNAP_EVERY:      # (2.6.84: or the clock went back)
            return
        self.next = now + SNAP_EVERY
        if LAYOUT.arrange and not self.drag:         # (2.6.72) Esc ends Arrange mode
            names = self._esc_names               # (2.6.82) only the name the client knows
            for i in range(len(names)):
                try:
                    if API.IsKeyPressed(names[i]):
                        LAYOUT.set_arrange(False)
                        break
                except Exception:
                    if len(names) > 1:           # a name this client refuses: not asked again
                        self._esc_names = names[:i] + names[i + 1:]
                    break
        pressed = self.pressed()
        if pressed is not True:
            if now >= self.keep_at:
                self.keep_at = now + KEEP_EVERY
                self.keep()                   # every window wholly on screen
            elif (LAYOUT.fresh or LAYOUT.fresh_adds) and LAYOUT.assign:
                # (a new window with zones in use: now) (2.6.82) only the layout and
                # the new windows, not the whole screen, until the next full look
                # (2.6.83) a refit (no new window) moves windows out of zones: a
                # full look then, so a freed window is put back on screen at once
                self.keep(light=bool(LAYOUT.fresh_adds) and not LAYOUT.fresh)
        if pressed is False and not self.drag:
            self.last = None                  # button up: look again once it's held
            if now >= self.prune_at:
                self.prune_at = now + SNAP_PRUNE
                self._prune()
            return
        if pressed is not True or now >= self.prune_at:
            self.prune_at = now + SNAP_PRUNE
            live = self._prune()
        else:
            # (2.6.82) held: closed windows are let go of at the same pace as when
            # the button is up (a closed one's place never changes, so it is never
            # taken for a drag); a drop below always prunes first
            live = self.gumps
        last = self.last
        if last is None:                      # first look since the button went down
            last = self.last = {}
            for g in live:
                p = self.pos(g)
                if p is not None:
                    last[g] = p
            return
        drag = self.drag
        by_code = self.by_code
        if by_code:                               # a code move never seen to land: let it go
            for g in [g for g, t in by_code.items() if now - t > 1.0]:
                del by_code[g]
        for g in live:
            p = self.pos(g)
            if p is None:
                continue
            prev = last.get(g)
            if prev is None:
                last[g] = p
                continue
            if p != prev:
                dx, dy = p[0] - prev[0], p[1] - prev[1]
                last[g] = p
                if by_code and g in by_code:      # placed by its module (Kit.moved_by_code)
                    del by_code[g]
                    continue
                if pressed is False:              # moved by code, not the mouse
                    continue
                drag[g] = now
                self.moved.add(g)
                self.dragged.add(g)
                r = None
                if LAYOUT.loaded:                     # (2.6.74) a drop survives a rebuild
                    if g not in self.drag_key:
                        self.drag_key[g] = LAYOUT._key_of(g)
                    r = self.rect(g)
                    if r is not None:
                        self.drag_rect[g] = r
                if LAYOUT.arrange:                    # (2.6.72) light the zone under it
                    LAYOUT.arrange_hover(g, r)        # (2.6.82) the rect just read
                if self.enabled and g not in self.no_snap and g not in LAYOUT.held:
                    self.follow(g, dx, dy, set([g]))  # (a held window tows nothing)
            elif g in drag:
                if pressed is False or (pressed is None and now - drag[g] >= SNAP_SETTLE):
                    del drag[g]
                    # (2.6.70) let go over a window zone: the layout slots it there (on
                    # the drop, below); snapped to a neighbour first, it was pulled
                    # flush with that window (often half out of the zone) and linked to
                    # it, so a later drag of the neighbour dragged it out of its zone
                    if self.enabled and g not in self.no_snap and not LAYOUT.takes(g):
                        self.snap(g, live)
        if (self.moved or self.lost) and not drag:   # let go: save where they are
            self._tell_moved()

    def follow(self, leader, dx, dy, seen):
        """Windows snapped on to `leader` move with it."""
        links = self.links
        if not links:
            return                                # (2.6.82) nothing is snapped on to anything
        held = LAYOUT.held
        for g in self.gumps:
            if g in seen or links.get(g) is not leader:
                continue
            if g in held:                         # (2.6.72) a zoned window is never towed
                links.pop(g, None)
                continue
            p = self.pos(g)
            if p is None:
                continue
            seen.add(g)
            self.move(g, p[0] + dx, p[1] + dy)
            if self.last is not None:
                self.last[g] = (p[0] + dx, p[1] + dy)
            self.moved.add(g)
            self.follow(g, dx, dy, seen)

    def snap(self, g, live):
        if self._fmap is not None:
            return self._snap(g, live)
        self._build_fmap()                       # (2.6.82) one followers scan per drop
        try:
            return self._snap(g, live)
        finally:
            self._fmap = None

    def _snap(self, g, live):
        r = self.rect(g)
        if r is None:
            return
        x, y, w, h = r
        corner = None                 # (distance, x, y, other)
        ex = ey = None                # (distance, value, other)
        links = self.links
        # the windows to snap on to, each with the window that leads it: a
        # window placed by its module beside another (Kit.attach: a grid under
        # a title bar, a tray beside a bar) is a target too, but the link goes
        # to the one that is dragged, since the attached one only moves in tow
        targets = []
        for o in live:
            if o is g or links.get(o) is g or not self.visible(o) or o in self.no_snap:
                continue
            targets.append((o, o))
            for f in self.followers(o):
                if f is not g and self.visible(f):
                    targets.append((f, o))
        for o, lead in targets:
            ro = self.rect(o)
            if ro is None:
                continue
            ox, oy, ow, oh = ro
            # a corner of this window on a corner of that one, outside it
            for tx, ty in ((ox + ow, oy), (ox + ow, oy + oh - h), (ox - w, oy),
                           (ox - w, oy + oh - h), (ox, oy + oh), (ox + ow - w, oy + oh),
                           (ox, oy - h), (ox + ow - w, oy - h)):
                d = max(abs(x - tx), abs(y - ty))
                if d <= SNAP_DIST and (corner is None or d < corner[0]):
                    corner = (d, tx, ty, lead)
            # one edge flush or in line, when the windows are beside each other
            if y < oy + oh + SNAP_DIST and oy < y + h + SNAP_DIST:
                for tx in (ox + ow, ox - w, ox, ox + ow - w):
                    d = abs(x - tx)
                    if d <= SNAP_DIST and (ex is None or d < ex[0]):
                        ex = (d, tx, lead)
            if x < ox + ow + SNAP_DIST and ox < x + w + SNAP_DIST:
                for ty in (oy + oh, oy - h, oy, oy + oh - h):
                    d = abs(y - ty)
                    if d <= SNAP_DIST and (ey is None or d < ey[0]):
                        ey = (d, ty, lead)
        if corner is not None:
            nx, ny, leader = corner[1], corner[2], corner[3]
        else:
            nx = ex[1] if ex else x
            ny = ey[1] if ey else y
            leader = (ex or ey or (None, None, None))[2]
        if leader is None:
            links.pop(g, None)                    # dragged clear of every window
            nx, ny = self.snap_screen(x, y, w, h) # ... but maybe on to the screen itself
        else:
            links[g] = leader
        nx, ny = Kit.clamp(nx, ny, w, h)          # let go half off the screen: back on
        if (nx, ny) != (x, y):
            self.move(g, nx, ny)
            if self.last is not None:
                self.last[g] = (nx, ny)
            self.follow(g, nx - x, ny - y, set([g]))

    # ---------- the screen: every window stays on it ----------
    def keep(self, light=False):
        """Every window wholly on screen (see the window rules above Kit.clamp).
        After a change of the client window's size every window first keeps
        its place relative to the anchor it is nearest; then anything off the
        screen is moved back the shortest way, attached windows along with it,
        and its module is told it moved (so it saves the place on screen)."""
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return
        live = self._prune()
        Kit.prune_pending()                   # (2.6.70) places asked for that landed long ago
        try:
            self._keep_body(W, H, live, light)
        finally:
            self._fmap = None

    def _build_fmap(self):
        """(2.6.82) leader -> [open followers] in one scan of `attached` (one
        is_open per follower, closed ones let go of), instead of a scan of every
        follower for every window the keeper looks at."""
        fm = {}
        for f, l in list(self.attached.items()):
            if not Kit.is_open(f):
                self._forget(f)
            else:
                lst = fm.get(l)
                if lst is None:
                    fm[l] = [f]
                else:
                    lst.append(f)
        self._fmap = fm

    def _keep_body(self, W, H, live, light=False):
        self._build_fmap()
        new = None
        if light:
            new = set(LAYOUT.fresh_adds)
            att = self.attached
            for g in list(new):               # a new tray: its leader is kept with it
                l = att.get(g)
                if l is not None:
                    new.add(l)
        try:
            Kit.scroll_sweep()                # scrolling windows: late controls into the area
        except Exception:
            pass
        old = self.screen
        if old != (W, H):
            new = None                        # the screen changed: every window, as always
            self.screen = (W, H)
            if old is not None:
                for g in live:
                    if g in self.drag:
                        continue
                    r = self.rect(g)
                    if r is None:
                        continue
                    x, y, w, h = r
                    nx = Kit.remap_axis(x, w, old[0], W)
                    ny = Kit.remap_axis(y, h, old[1], H)
                    if (nx, ny) != (x, y):
                        self._shift(g, nx - x, ny - y)
            Kit.note_screen((W, H))           # the saved places are for this screen now
        held = LAYOUT.held
        for g in live:
            # (2.6.72) a window held in a zone is the layout's to place: with one frame
            # on its hidden frame may reach past the screen's edge (its panels don't)
            if new is not None and g not in new:
                continue                      # (2.6.82) a light look: the new windows only
            if g not in self.drag and g not in held:
                self.keep_one(g)
        try:
            LAYOUT.keep(W, H)                 # the slotted windows in their zones (one hop)
        except Exception as ex:
            HOST._tell("%s: layout error: %s%s" % (APP_NAME, ex, _error_where()))
        if (self.moved or self.lost) and not self.drag:
            self._tell_moved()

    def keep_one(self, g):
        """Window g, with the windows attached to it, wholly on screen (the
        top-left corner when the lot is bigger than the screen). True if moved."""
        r = self.rect(g)
        if r is None:
            return False
        x0, y0, x1, y1 = r[0], r[1], r[0] + r[2], r[1] + r[3]
        for f in self.followers(g):
            rf = self.rect(f)
            if rf is not None and self.visible(f):
                x0, y0 = min(x0, rf[0]), min(y0, rf[1])
                x1, y1 = max(x1, rf[0] + rf[2]), max(y1, rf[1] + rf[3])
        nx, ny = Kit.clamp(x0, y0, x1 - x0, y1 - y0)
        if (nx, ny) == (x0, y0):
            return False
        self._shift(g, nx - x0, ny - y0)
        return True

    def _shift(self, g, dx, dy):
        """Move g and its attached windows by (dx, dy), by code."""
        for w in [g] + self.followers(g):
            p = self.pos(w)
            if p is None:
                continue
            self.move(w, p[0] + dx, p[1] + dy)
            if self.last is not None:
                self.last[w] = (p[0] + dx, p[1] + dy)
        self.moved.add(g)

    # ---------- the screen: anchors and the grid ----------
    @staticmethod
    def anchor_targets(w, h):
        """[(x, y)] where a w x h window sits at each screen anchor (corners,
        edge midpoints, centre; top row first, left to right): Kit.anchor_targets."""
        return Kit.anchor_targets(w, h)

    def snap_screen(self, x, y, w, h):
        """A let-go window near a screen anchor goes on to it; near a screen
        edge it goes flush with it; while the grid is shown, each edge of the
        window goes on to the nearest grid line. Returns the new (x, y)."""
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return x, y
        best = None                                   # (distance, x, y)
        for ax, ay in self.anchor_targets(w, h):
            d = max(abs(ax - x), abs(ay - y))
            if d <= SNAP_ANCHOR and (best is None or d < best[0]):
                best = (d, ax, ay)
        if best is not None:
            return best[1], best[2]
        nx, ny = x, y
        for tx in (0, max(0, W - w)):                  # flush with an edge
            if abs(tx - x) <= SNAP_DIST:
                nx = tx
        for ty in (0, max(0, H - h)):
            if abs(ty - y) <= SNAP_DIST:
                ny = ty
        if HOST.grid_shown():                          # the grid's lines
            step = HOST.grid_size()

            def on_line(lo, size, cur):
                """The nearer edge (lo or lo + size) on its grid line, if not moved yet."""
                cands = []
                for edge, back in ((lo, 0), (lo + size, size)):
                    line = int(round(float(edge) / step)) * step
                    if abs(line - edge) <= SNAP_DIST:
                        cands.append((abs(line - edge), line - back))
                return min(cands)[1] if cands and cur == lo else cur
            nx, ny = on_line(x, w, nx), on_line(y, h, ny)
        return nx, ny


class Grid(object):
    """A grid over the whole client window (the Action Bar's GRID button): thin
    lines every grid_size pixels, brighter every fourth, a gold cross through
    the centre and a marker at each of the nine anchors. It never takes the
    mouse. While it is shown, every window of Virtue Assistant snaps to its
    lines when let go (Snap.snap_screen)."""
    MINOR, MAJOR = 0.16, 0.34                 # line alpha
    CROSS, MARK = 0.55, 0.75                  # centre cross, anchor markers
    MARK_W = 10

    def __init__(self, host):
        self.host = host
        self.g = None
        self.shown = False
        self.drawn = None                     # (W, H, step) the overlay was drawn for

    def toggle(self):
        if self.shown:
            self.hide()
        else:
            self.show()

    def show(self):
        self.shown = True
        Kit.on_client(self.build)

    def hide(self):
        self.shown = False
        g, self.g = self.g, None
        Kit.dispose(g)

    def redraw(self):
        if self.shown:
            Kit.on_client(self.build)

    def tick(self):
        """Follows a resized client window."""
        if self.shown and self.drawn is not None:
            W, H = Kit.screen()
            if (W, H, self.host.grid_size()) != self.drawn:
                self.redraw()

    def build(self):
        W, H = Kit.screen()
        step = self.host.grid_size()
        old, self.g = self.g, None
        if W <= 0 or H <= 0:
            Kit.dispose(old)
            return
        g = G.CreateGump(False, False)
        for n, x in enumerate(range(step, W, step), 1):
            Kit.add_box(g, x, 0, 1, H, self.MAJOR if n % 4 == 0 else self.MINOR)
        for n, y in enumerate(range(step, H, step), 1):
            Kit.add_box(g, 0, y, W, 1, self.MAJOR if n % 4 == 0 else self.MINOR)
        Kit.add_box(g, W // 2, 0, 1, H, self.CROSS, "#FFD700")
        Kit.add_box(g, 0, H // 2, W, 1, self.CROSS, "#FFD700")
        m = self.MARK_W
        for ax, ay in Snap.anchor_targets(m, m):
            Kit.add_box(g, ax, ay, m, m, self.MARK, "#FFD700")
        Kit.add_label(g, "GRID %d px: windows snap to its lines, the screen's corners, edges "
                      "and centre  (the Action Bar's Grid button hides it)" % step,
                      m + 8, m + 4, Kit.HUE_TITLE)
        g.SetRect(0, 0, W, H)
        safe(lambda: g.SetAcceptMouseInput(False))
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        try:                                   # under the other windows, if the client lets us
            import System
            g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
        except Exception:
            pass
        self.g = g
        self.drawn = (W, H, step)
        G.AddGump(g)
        SNAP.skip_gump(g)
        Kit.dispose(old)


# =============================================================================
#  The layout (2.6.54): zones round the game area that the module windows sit in
#
#  Two levels, both the player's to change:
#    - a FRAME LAYOUT is the set of zones: where each is, how big, what kind
#      ("window": windows stack in it; "keep clear": no window rests there, the
#      game; "reserved": a client gump lives there, the chat). "Default" is
#      generated from the screen (ZoneSet.default: three bands round the game
#      area, the frames strip over it and the bars under it, spill bands on an
#      ultrawide screen); any other is drawn by the player in the editor
#      (LayoutEditor) and saved as fractions of the screen, so it reflows.
#    - a WINDOW LAYOUT says which window sits in which zone (Layout.assign).
#  A window is named by its dock key (what HOST.dock_add was given; the Frames'
#  two frames are "unitframes.player" / ".target", the bar is "actionbar"), so
#  the dock registry is the only registry: Kit.dock_hooks offers the gump and
#  Host.dock_add lists it (Host.layout_add for a window with no tray button).
#  The engine runs on the keeper's pass (Snap.keep, the client thread, every
#  KEEP_EVERY s): it places only the windows whose place differs from their
#  slot, in one hop, and never waits. A window taller than its slot scrolls
#  (Kit.place max_h=). A window dragged and let go with its centre in a zone is
#  slotted there (Snap.on_drop -> Layout.dropped); let go anywhere else it is
#  free again. Every string here follows the UI and text standard.
# =============================================================================
LAYOUT_VAR = "VirtueAssistant_layout"              # per character: the window layout in use
LAYOUT_ACTIVE = "VirtueAssistant_layout_active"    # its name ("" = none: every window free)
LAYOUT_LIST = "VirtueAssistant_layout_list"        # the player's window layout names
LAYOUT_NAMED = "VirtueAssistant_layout_%s"         # a named window layout
FRAMES_ACTIVE = "VirtueAssistant_frames_active"    # the frame layout in use (Default when unset)
FRAMES_LIST = "VirtueAssistant_frames_list"        # the player's frame layout names
FRAMES_NAMED = "VirtueAssistant_frames_%s"         # a frame layout as drawn (+ "@<class>" variants)
LAYOUT_OPTS = "VirtueAssistant_layout_opts"        # "game=1": an empty band widens the game area
LAYOUT_EDITOR_POS = "VirtueAssistant_layout_editor_pos"
LAYOUT_DEFAULT = "Default"
LAYOUT_MIRRORED = "Mirrored"
LAYOUT_MINE = "Default (mine)"
#  (2.6.57) windows that are no zone occupants any more: Buffs & Timers, Bandages
#  and the Swing Bar ride on the player and target frames. A saved layout that
#  still names them loads without them (and is saved so).
LAYOUT_GONE = frozenset(("spelltimers", "bandage", "swing"))
#  The sketch: which window sits in which zone of the Default frame layout.
WINDOWS_DEFAULT = ("L1=character;L2=bag;C1=unitframes.player;C2=unitframes.target;C4=actionbar;"
                   "R1=worldmap;R2=ultima.friend,ultima.neutral,ultima.foe;R3=meters")
WINDOWS_MIRRORED = ("L1=worldmap;L2=ultima.friend,ultima.neutral,ultima.foe,meters;"
                    "C1=unitframes.player;C2=unitframes.target;C4=actionbar;R1=character;R2=bag")
#  Band sizes of the generated Default (gump pixels; see the layout template)
SIDE_MIN, SIDE_MAX, SIDE_SHARE = 240, 440, 0.22
SPILL_MIN, SPILL_MAX, SPILL_SHARE = 240, 360, 0.12
CENTRE_MIN_SHARE = 0.40
TOP_MIN, TOP_MAX, BOT_MIN, BOT_MAX, STRIP_SHARE = 110, 180, 100, 160, 0.14
LEFT_SLOTS = (("L1", 0.32, 260, "w", 2), ("L2", 0.38, 180, "w", 1), ("L3", 0.30, 160, "r", 0))
RIGHT_SLOTS = (("R1", 0.32, 200, "w", 2), ("R2", 0.40, 240, "w", 3), ("R3", 0.28, 120, "w", 1))
#   (id, share of H, minimum, kind, shrinks: 1 = first to its minimized bars, 0 = never)
EMPTY_SLOT = 46                 # an empty slot keeps this much as a place to drop a window on
MINI_BAR = 46                   # a minimized bar's height
ZONE_MIN_W, ZONE_MIN_H = 96, 64 # the smallest zone the editor lets you draw
ZONE_ALPHA = 0.25               # a zone frame's fill over the game
ZONE_COLORS = {"w": "#3A78C8", "k": "#3AA060", "r": "#C88A3A"}
ZONE_KINDS = (("w", "window"), ("k", "keep clear"), ("r", "reserved"))
ZONE_STACKS = (("d", "down"), ("u", "up"), ("r", "right"), ("l", "left"))
ZONE_FITS = (("w", "fill width"), ("s", "shrink only"), ("n", "none"))   # (2.6.55) Zone.fit
SHRINK_MAX = 6                  # "Shrinks" cycles never, 1st .. 6th
ROOM_MIN = 80                   # a window gets at least this much of a slot (then it scrolls)
FIT_MIN, FIT_MAX = 0.5, 1.5     # (2.6.55) how far a window is scaled to fit its zone
FIT_STEP = 0.02                 # a change of scale smaller than this is not worth a redraw
ARCH_RUN, ARCH_CROWN = 140, 20  # (2.6.72) the arch's S-curve run and crown strip, px at 1080 high


def ratio_class(W, H):
    """The screen's ratio class: narrow (4:3, 5:4), wide (16:10, 16:9) or ultrawide."""
    if W <= 0 or H <= 0:
        return "wide"
    r = float(W) / float(H)
    return "narrow" if r < 1.5 else "wide" if r < 2.0 else "ultrawide"


def _clampv(v, lo, hi):
    return max(lo, min(hi, v))


def _ordinal(n):
    n = int(n)
    if n <= 0:
        return "never"
    if n % 100 in (11, 12, 13):
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


class Zone(object):
    """One zone of a frame layout. `rect` is (left, top, width, height) in
    thousandths of the screen (the saved form); `px` the pixel rect on the
    screen in use (set by ZoneSet.reflow / ZoneSet.default)."""
    __slots__ = ("id", "kind", "rect", "pins", "min", "stack", "prio", "px", "squeezed", "fit",
                 "hug", "arch", "overlap", "lock")

    def __init__(self, id, kind="w", rect=(0, 0, 200, 200), pins="", mins=(0, 0), stack="d",
                 prio=0, fit="w", hug=False, arch=False, overlap=False, lock=False):
        self.id = str(id)
        self.kind = kind if kind in ("w", "k", "r") else "w"
        self.rect = tuple(int(v) for v in rect)
        self.pins = "".join(c for c in str(pins or "").upper() if c in "LTRBXY")
        self.min = (int(mins[0]), int(mins[1]))
        self.stack = stack if stack in ("d", "u", "r", "l") else "d"
        self.prio = max(0, min(SHRINK_MAX, int(prio)))
        self.fit = fit if fit in ("w", "s", "n") else "w"   # (2.6.55) how its windows fit it
        # (2.6.72) a window zone that hugs its window (as wide as the window wants for
        # its height, in its corner of the band), and a keep-clear zone whose top is
        # arched (it runs up to the crown between the hugging zones in its corners)
        self.hug = bool(hug) and self.kind == "w"
        self.arch = bool(arch) and self.kind == "k"
        # (2.6.74) a zone that may lie over other zones (the editor, push_clear, reflow's
        # keep-clear cut and Fill the gaps leave it alone), and a zone locked in the
        # editor (it can't be moved or resized by accident). With Overlap on, a
        # keep-clear zone's arch is its own "Top edge: arched" (arch), not a guess.
        self.overlap = bool(overlap)
        self.lock = bool(lock)
        self.px = None
        self.squeezed = False

    def kind_name(self):
        return dict(ZONE_KINDS)[self.kind]

    def stack_name(self):
        return dict(ZONE_STACKS)[self.stack]

    def fit_name(self):
        return dict(ZONE_FITS)[self.fit]

    def copy(self):
        z = Zone(self.id, self.kind, self.rect, self.pins, self.min, self.stack, self.prio,
                 self.fit, self.hug, self.arch, self.overlap, self.lock)
        z.px = tuple(self.px) if self.px else None
        return z

    def set_px(self, x, y, w, h, W, H):
        """The pixel rect, clamped on screen (never off it), and the fractions from it."""
        w, h = max(1, int(w)), max(1, int(h))
        if W > 0:
            w = min(w, W)
            x = _clampv(int(x), 0, W - w)
        if H > 0:
            h = min(h, H)
            y = _clampv(int(y), 0, H - h)
        self.px = (int(x), int(y), w, h)
        if W > 0 and H > 0:
            self.rect = (int(round(1000.0 * x / W)), int(round(1000.0 * y / H)),
                         int(round(1000.0 * w / W)), int(round(1000.0 * h / H)))

    def note_pins(self, W, H):
        """Which edges sit on a screen edge (within SNAP_DIST), and whether the
        centre is on the screen's centre line; read from px."""
        if not self.px or W <= 0 or H <= 0:
            return
        x, y, w, h = self.px
        p = ""
        if x <= SNAP_DIST:
            p += "L"
        if y <= SNAP_DIST:
            p += "T"
        if W - (x + w) <= SNAP_DIST:
            p += "R"
        if H - (y + h) <= SNAP_DIST:
            p += "B"
        if abs((x + w / 2.0) - W / 2.0) <= SNAP_DIST:
            p += "X"
        if abs((y + h / 2.0) - H / 2.0) <= SNAP_DIST:
            p += "Y"
        self.pins = p

    def save_text(self):
        # (2.6.72) hug and arch are the ninth and tenth fields, only when set (an older
        # version reads the first eight and ignores them)
        extra = (":%d:%d" % (1 if self.hug else 0, 1 if self.arch else 0)) if (self.hug or self.arch) else ""
        # (2.6.74) overlap and lock are the eleventh and twelfth, written only when on
        # (an older version reads ten fields at most and takes them as off)
        if self.overlap or self.lock:
            extra = ":%d:%d:%d:%d" % (1 if self.hug else 0, 1 if self.arch else 0,
                                      1 if self.overlap else 0, 1 if self.lock else 0)
        return "%s:%s:%d,%d,%d,%d:%s:%d,%d:%s:%d:%s%s" % (
            self.id.replace(":", " ").replace(";", " "), self.kind, self.rect[0], self.rect[1],
            self.rect[2], self.rect[3], self.pins, self.min[0], self.min[1], self.stack, self.prio,
            self.fit, extra)

    @staticmethod
    def parse(text):
        """A zone from its saved form, or None when a field is bad. The fit
        (2.6.55) is the eighth field; a form without one is fill width."""
        try:
            f = text.split(":")
            if len(f) < 7 or not f[0].strip():
                return None
            rect = [int(v) for v in f[2].split(",")]
            mn = [int(v) for v in f[4].split(",")]
            if len(rect) != 4 or len(mn) != 2 or rect[2] <= 0 or rect[3] <= 0:
                return None
            fit = f[7].strip() if len(f) > 7 else "w"
            hug = len(f) > 8 and f[8].strip() == "1"           # (2.6.72) older forms: off
            arch = len(f) > 9 and f[9].strip() == "1"
            overlap = len(f) > 10 and f[10].strip() == "1"      # (2.6.74) older forms: off
            lock = len(f) > 11 and f[11].strip() == "1"
            return Zone(f[0].strip(), f[1].strip(), rect, f[3], mn, f[5].strip(), int(f[6]), fit,
                        hug, arch, overlap, lock)
        except Exception:
            return None


class ZoneSet(object):
    """A frame layout: its zones, the grid step and screen it was drawn on."""

    def __init__(self, name, zones=None, grid=GRID_DEFAULT, screen=(0, 0), generated=False):
        self.name = str(name)
        self.zones = list(zones or [])
        self.grid = int(grid or GRID_DEFAULT)
        self.screen = (int(screen[0]), int(screen[1]))
        self.generated = generated          # Default: made again for each screen, never saved
        self.skipped = []                   # zone ids that couldn't be read
        self.ver = 2                        # (2.6.74) 2: its arches are its own (no guess)
        self.needs = {}                     # (2.6.85) zone id -> (w, h) its window asks for

    def by_id(self, zid):
        for z in self.zones:
            if z.id == zid:
                return z
        return None

    def ids(self):
        return [z.id for z in self.zones]

    def copy(self, name=None):
        out = ZoneSet(name or self.name, [z.copy() for z in self.zones], self.grid, self.screen,
                      self.generated)
        out.ver = self.ver
        return out

    def save_text(self):
        # (2.6.74) "v=2": saved by 2.6.74 or later (an older version skips the item)
        return "grid=%d,screen=%dx%d,v=%d;" % (self.grid, self.screen[0], self.screen[1], self.ver) + \
            ";".join(z.save_text() for z in self.zones)

    @staticmethod
    def parse(name, text):
        """A frame layout from its saved form, or None when there is none. A
        zone that can't be read is skipped (listed in .skipped)."""
        text = str(text or "").strip()
        if not text:
            return None
        parts = text.split(";")
        grid, screen, ver = GRID_DEFAULT, (0, 0), 1
        head = parts[0]
        if head.startswith("grid="):
            parts = parts[1:]
            for item in head.split(","):
                try:
                    k, v = item.split("=", 1)
                    if k == "grid":
                        grid = int(v)
                    elif k == "screen":
                        w, h = v.lower().split("x")
                        screen = (int(w), int(h))
                    elif k == "v":
                        ver = int(v)
                except Exception:
                    pass
        zs = ZoneSet(name, [], grid, screen)
        zs.ver = ver                                 # (2.6.74) 1: saved before 2.6.74
        for p in parts:
            if not p.strip():
                continue
            z = Zone.parse(p)
            if z is None:
                zs.skipped.append(p.split(":")[0].strip() or "?")
            elif zs.by_id(z.id) is None:
                zs.zones.append(z)
        return zs

    # ---------- the generated Default ----------
    @staticmethod
    def default(W, H, occupied=(), game_grows=True, arch=False):
        """The sketch, generated for a W x H screen: three bands, the frames
        strip and the bars in the centre, spill bands on an ultrawide screen.
        `occupied`: the zone ids that hold a window (an empty slot gives its
        room to the slots above and below it, keeping EMPTY_SLOT px to drop a
        window on; a whole empty band lets the game area grow over it when
        game_grows)."""
        zs = ZoneSet(LAYOUT_DEFAULT, [], GRID_DEFAULT, (W, H), generated=True)
        if W <= 0 or H <= 0:
            return zs
        occupied = set(occupied)
        cls = ratio_class(W, H)
        if cls == "narrow":
            side, spill = SIDE_MIN, 0
        else:
            side = int(_clampv(SIDE_SHARE * W, SIDE_MIN, SIDE_MAX))
            spill = int(_clampv(SPILL_SHARE * W, SPILL_MIN, SPILL_MAX)) if cls == "ultrawide" else 0
        if W - 2 * side - 2 * spill < CENTRE_MIN_SHARE * W:      # the guard: the game area first
            spill = 0
            if W - 2 * side < CENTRE_MIN_SHARE * W:
                side = max(SIDE_MIN, int((W - CENTRE_MIN_SHARE * W) / 2))
        lx, rx = spill, W - spill - side
        cx, cw = spill + side, W - 2 * (spill + side)
        top_h = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX))
        bot_h = int(_clampv(STRIP_SHARE * H, BOT_MIN, BOT_MAX))

        def band(x, slots):
            heights = ZoneSet._band_heights(H, slots, occupied)
            y = 0
            for (zid, share, mn, kind, prio), (h, squeezed) in zip(slots, heights):
                z = Zone(zid, kind, (0, 0, 1, 1), "", (SIDE_MIN, mn), "d", prio)
                z.set_px(x, y, side, h, W, H)
                z.squeezed = squeezed
                z.note_pins(W, H)
                zs.zones.append(z)
                y += h

        band(lx, LEFT_SLOTS)
        half = cw // 2
        for zid, x, w, p in (("C1", cx, half, 3), ("C2", cx + half, cw - half, 2)):
            # (2.6.72) with the arch, the frames' zones hug their frames in the band's
            # top corners (Layout._apply_hug sizes them)
            z = Zone(zid, "w", (0, 0, 1, 1), "T", (300, TOP_MIN), "d", p, hug=arch)
            z.set_px(x, 0, w, top_h, W, H)
            z.note_pins(W, H)
            zs.zones.append(z)
        gx, gw = cx, cw
        if game_grows:                               # an empty band: the game area grows over it
            if not any(s[0] in occupied for s in LEFT_SLOTS if s[3] == "w"):
                gx, gw = 0, gw + cx
            if not any(s[0] in occupied for s in RIGHT_SLOTS if s[3] == "w"):
                gw = W - gx
        # (2.6.74) arched: it lies over the frames' zones (Overlap on), its top arched
        z = Zone("C3", "k", (0, 0, 1, 1), "XY", (0, 0), "d", 0, arch=arch, overlap=arch)
        if arch:                                     # (2.6.72) up to the crown between the frames
            crown = max(10, int(round(ARCH_CROWN * H / 1080.0)))
            z.set_px(gx, crown, gw, H - crown - bot_h, W, H)
        else:
            z.set_px(gx, top_h, gw, H - top_h - bot_h, W, H)
        z.note_pins(W, H)
        zs.zones.append(z)
        z = Zone("C4", "w", (0, 0, 1, 1), "B", (600, BOT_MIN), "r", 1)
        z.set_px(cx, H - bot_h, cw, bot_h, W, H)
        z.note_pins(W, H)
        zs.zones.append(z)
        band(rx, RIGHT_SLOTS)
        if spill:
            for zid, x in (("L0", 0), ("R0", W - spill)):
                z = Zone(zid, "w", (0, 0, 1, 1), "", (SPILL_MIN, 120), "d", 1)
                z.set_px(x, 0, spill, H, W, H)
                z.note_pins(W, H)
                zs.zones.append(z)
        return zs

    @staticmethod
    def _band_heights(H, slots, occupied):
        """[(height, squeezed)] per slot of a band: the shares of H, every slot
        raised to its minimum (the difference taken from the others in
        proportion to their shares); an empty window slot keeps EMPTY_SLOT px
        and gives the rest to the slots with a window (a band with no window
        at all keeps its shares, so the slots stay wide open to drop on); a
        reserved slot never grows past its share; when the minimums alone
        don't fit, slots shrink to a minimized bar in "shrinks" order."""
        n = len(slots)
        room = H
        any_win = any(zid in occupied for zid, sh, mn, kind, prio in slots if kind == "w")
        share, mins = [], []
        for zid, sh, mn, kind, prio in slots:
            empty = kind == "w" and zid not in occupied and any_win
            share.append(0.0 if empty else float(sh))
            mins.append(EMPTY_SLOT if empty else int(mn))
        squeezed = [False] * n
        # minimums that don't fit: minimize in shrinks order (1st first)
        order = sorted([i for i in range(n) if slots[i][4] > 0 and slots[i][3] == "w"],
                       key=lambda i: slots[i][4])
        while sum(mins) > room and order:
            i = order.pop(0)
            if mins[i] > MINI_BAR:
                mins[i] = MINI_BAR
                squeezed[i] = True
                share[i] = 0.0
        total = sum(share) or 1.0
        h = [room * sh / total for sh in share]
        # raise every slot under its minimum, taking from the others by share
        for _ in range(n):
            short = [(i, mins[i] - h[i]) for i in range(n) if h[i] < mins[i]]
            if not short:
                break
            need = sum(d for i, d in short)
            fixed = set(i for i, d in short)
            for i, d in short:
                h[i] = mins[i]
            donors = [i for i in range(n) if i not in fixed and h[i] > mins[i]]
            pool = sum(h[i] - mins[i] for i in donors)
            if pool <= 0:
                break
            take = min(need, pool)
            for i in donors:
                h[i] -= take * (h[i] - mins[i]) / pool
        # a reserved slot (the chat) keeps to its share; the rest goes to the window slots
        for i in range(n):
            if slots[i][3] == "r" and h[i] > slots[i][1] * room:
                extra, h[i] = h[i] - slots[i][1] * room, slots[i][1] * room
                # 2.6.81: only to slots with a window (an empty one keeps EMPTY_SLOT;
                # a squeezed one has share 0.0); with no window at all, by the shares
                takers = [j for j in range(n) if slots[j][3] == "w" and not squeezed[j]
                          and share[j] > 0]
                if takers:
                    pool = sum(share[j] for j in takers) or 1.0
                    for j in takers:
                        h[j] += extra * share[j] / pool
                else:
                    takers = [j for j in range(n) if slots[j][3] == "w" and not squeezed[j]]
                    pool = sum(slots[j][1] for j in takers) or 1.0
                    for j in takers:
                        h[j] += extra * slots[j][1] / pool
        out = [int(round(v)) for v in h]
        extra = room - sum(out)                      # rounding: the biggest slot takes it
        if out and extra:
            out[out.index(max(out))] += extra
        return [(max(1, out[i]), squeezed[i]) for i in range(n)]

    # ---------- a drawn layout on another screen ----------
    def reflow(self, W, H, step):
        """Every zone's pixel rect for a W x H screen: fractions first (each edge
        on the grid in use), pins win (an edge on a screen edge stays on it, a
        pinned centre on the centre line, flush neighbours stay flush), then
        minimums, then every keep-clear zone shrinks out of the window zones.
        Nothing is ever off screen."""
        if W <= 0 or H <= 0:
            return
        step = max(8, int(step or GRID_DEFAULT))
        if self.needs:                               # (2.6.85) the zones as drawn stay as drawn:
            drawn = [(z, z.rect) for z in self.zones]    # what a need takes is only for now
            self.needs, needs = {}, self.needs
            self.reflow(W, H, step)
            self.needs = needs
            self._apply_needs(W, H)
            self._keep_clear(W, H)
            for z, r in drawn:
                z.rect = r
            return
        oldW, oldH = self.screen if self.screen[0] > 0 and self.screen[1] > 0 else (W, H)
        flush = self._flush_pairs(oldW, oldH)

        def on_grid(v, limit):
            v = int(round(float(v) / step)) * step
            return _clampv(v, 0, limit)
        for z in self.zones:
            l, t, w, h = z.rect
            x0, y0 = on_grid(W * l / 1000.0, W), on_grid(H * t / 1000.0, H)
            x1, y1 = on_grid(W * (l + w) / 1000.0, W), on_grid(H * (t + h) / 1000.0, H)
            if "L" in z.pins:
                x0 = 0
            if "T" in z.pins:
                y0 = 0
            if "R" in z.pins:
                x1 = W
            if "B" in z.pins:
                y1 = H
            if "X" in z.pins and "L" not in z.pins and "R" not in z.pins:
                half = (x1 - x0) // 2
                x0, x1 = W // 2 - half, W // 2 - half + (x1 - x0)
            if "Y" in z.pins and "T" not in z.pins and "B" not in z.pins:
                half = (y1 - y0) // 2
                y0, y1 = H // 2 - half, H // 2 - half + (y1 - y0)
            z.px = (x0, y0, max(1, x1 - x0), max(1, y1 - y0))
        # flush neighbours stay flush: the pinned (or more pinned) one leads
        for a, b, side in flush:
            za, zb = self.by_id(a), self.by_id(b)
            if za is None or zb is None or za.px is None or zb.px is None:
                continue
            ax, ay, aw, ah = za.px
            bx, by, bw, bh = zb.px
            if side == "h":                          # b sits right of a: its left edge follows
                nx = ax + aw
                right = W if "R" in zb.pins else bx + bw
                if right - nx >= ZONE_MIN_W:
                    zb.px = (nx, by, right - nx, bh)
            else:                                    # b sits under a: its top edge follows
                ny = ay + ah
                bottom = H if "B" in zb.pins else by + bh
                if bottom - ny >= ZONE_MIN_H:
                    zb.px = (bx, ny, bw, bottom - ny)
        # minimums: grow into free room beside the zone (else the windows scroll)
        for z in self.zones:
            if z.kind == "k":
                continue
            x, y, w, h = z.px
            if w < z.min[0]:
                w = min(z.min[0], max(w, self._free_right(z, W) - x))
            if h < z.min[1]:
                h = min(z.min[1], max(h, self._free_below(z, H) - y))
            z.set_px(x, y, w, h, W, H)
            z.squeezed = z.prio > 0 and z.px[3] < z.min[1]
        for z in self.zones:                         # none of them over another
            if z.kind != "k" and not z.overlap and self.overlaps(z):
                self.push_clear(z, W, H)
        for z in self.zones:                         # keep clear last: out of every window zone
            if z.kind != "k" or z.overlap:           # (2.6.74) Overlap on: as drawn
                continue
            x, y, w, h = z.px
            for o in self.zones:
                if o is z or o.kind != "w" or o.px is None:
                    continue
                ox, oy, ow, oh = o.px
                if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh:
                    cuts = [(x + w - ox, "R"), ((ox + ow) - x, "L"), (y + h - oy, "B"),
                            ((oy + oh) - y, "T")]
                    cut, side = min(cuts)
                    if side == "R":
                        w -= cut
                    elif side == "L":
                        x, w = x + cut, w - cut
                    elif side == "B":
                        h -= cut
                    else:
                        y, h = y + cut, h - cut
                    if w < ZONE_MIN_W or h < ZONE_MIN_H:
                        x, y, w, h = z.px            # cut to nothing: it keeps its own rect
                        break
            z.set_px(x, y, max(1, w), max(1, h), W, H)
        for z in self.zones:
            z.set_px(z.px[0], z.px[1], z.px[2], z.px[3], W, H)
        self.screen = (W, H)

    def _flush_pairs(self, W, H):
        """[(a, b, "h" | "v")]: zones flush (within SNAP_DIST, in the pixels of
        the screen they were drawn on), b right of / under a."""
        out = []
        px = {}
        for z in self.zones:
            l, t, w, h = z.rect
            px[z.id] = (W * l / 1000.0, H * t / 1000.0, W * w / 1000.0, H * h / 1000.0)
        for a in self.zones:
            ax, ay, aw, ah = px[a.id]
            for b in self.zones:
                if a is b:
                    continue
                bx, by, bw, bh = px[b.id]
                if abs(bx - (ax + aw)) <= SNAP_DIST and by < ay + ah and ay < by + bh:
                    out.append((a.id, b.id, "h"))
                if abs(by - (ay + ah)) <= SNAP_DIST and bx < ax + aw and ax < bx + bw:
                    out.append((a.id, b.id, "v"))
        # the more pinned zone leads: order the pairs so leaders come first
        def rank(zid):
            z = self.by_id(zid)
            return -len(z.pins) if z else 0
        out.sort(key=lambda p: (rank(p[0]), rank(p[1])))
        return out

    def _free_right(self, z, W):
        x, y, w, h = z.px
        lim = W
        for o in self.zones:
            if o is z or o.kind == "k" or o.px is None:
                continue
            ox, oy, ow, oh = o.px
            if ox >= x + w and oy < y + h and y < oy + oh:
                lim = min(lim, ox)
        return lim

    def _free_below(self, z, H):
        x, y, w, h = z.px
        lim = H
        for o in self.zones:
            if o is z or o.kind == "k" or o.px is None:
                continue
            ox, oy, ow, oh = o.px
            if oy >= y + h and ox < x + w and x < ox + ow:
                lim = min(lim, oy)
        return lim

    # ---------- the editor's helpers ----------
    def overlaps(self, z, px=None):
        """The zones z (at px, or its own) may not overlap: a window zone meets
        every kind, a reserved one windows and reserved, a keep-clear one
        windows and keep-clear (the chat may sit over the game)."""
        x, y, w, h = px or z.px
        out = []
        if z.overlap:                                # (2.6.74) it may lie over any zone
            return out
        for o in self.zones:
            if o is z or o.px is None or o.overlap:
                continue
            if z.kind == "r" and o.kind == "k":
                continue
            if z.kind == "k" and o.kind == "r":
                continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh:
                out.append(o)
        return out

    def push_clear(self, z, W, H, step=None):
        """Move z the shortest way out of every zone it may not overlap (a zone
        let go over another is pushed to the nearest free edge of it): of the
        four ways past each zone in the way, the shortest that ends clear of
        them all (on a grid line when that is clear too), else the shortest."""
        for _ in range(12):
            hits = self.overlaps(z)
            if not hits:
                return True
            x, y, w, h = z.px
            cands = []
            for o in hits:
                ox, oy, ow, oh = o.px
                for nx, ny in (((ox - w), y), ((ox + ow), y), (x, (oy - h)), (x, (oy + oh))):
                    if not (0 <= nx <= W - w and 0 <= ny <= H - h):
                        continue
                    clear = not self.overlaps(z, (nx, ny, w, h))
                    if clear and step:
                        gx, gy = int(round(float(nx) / step)) * step, int(round(float(ny) / step)) * step
                        if 0 <= gx <= W - w and 0 <= gy <= H - h and not self.overlaps(z, (gx, gy, w, h)):
                            nx, ny = gx, gy
                    cands.append((0 if clear else 1, abs(nx - x) + abs(ny - y), nx, ny))
            if not cands:
                return False
            cands.sort()
            z.set_px(cands[0][2], cands[0][3], w, h, W, H)
            if cands[0][0] == 0:
                return True
        return not self.overlaps(z)

    def _keep_clear(self, W, H):
        """(2.6.85) After a need: every keep-clear zone out of the grown window zones, on the
        side it lies (its px only)."""
        for z in self.zones:
            if z.kind != "k" or z.overlap or z.px is None:
                continue
            x, y, w, h = z.px
            for o in self.zones:
                if o is z or o.kind != "w" or o.px is None:
                    continue
                ox, oy, ow, oh = o.px
                if ox >= x + w or x >= ox + ow or oy >= y + h or y >= oy + oh:
                    continue
                if oy + oh >= y + h and oy > y:          # it came up from below
                    h = oy - y
                elif oy <= y and oy + oh < y + h:        # down from above
                    h, y = h - (oy + oh - y), oy + oh
                elif ox + ow >= x + w and ox > x:        # in from the right
                    w = ox - x
                elif ox <= x and ox + ow < x + w:        # in from the left
                    w, x = w - (ox + ow - x), ox + ow
            z.px = (x, y, max(1, w), max(1, h))

    def _apply_needs(self, W, H):
        """(2.6.85) A zone whose window needs more room (the Action Bar's extra rows)
        grows that way: away from the screen edge it is pinned to, over any keep-clear
        zone (which shrinks out of it next), and window zones in the way give way down
        to their minimums. Only px changes, never the saved rect: when the need goes
        the zone is back as drawn. Never past the screen."""
        for z in self.zones:
            need = self.needs.get(z.id)
            if need is None or z.px is None or z.kind == "k":
                continue
            x, y, w, h = z.px
            nw, nh = need
            if nh and nh > h:
                grow = min(nh - h, H - h)
                if "B" in z.pins or y + h / 2.0 >= H / 2.0:   # up from the bottom
                    ny = max(0, y - grow)
                    for o in self.zones:
                        if o is z or o.kind != "w" or o.overlap or o.px is None:
                            continue
                        ox, oy, ow, oh = o.px
                        if ox < x + w and x < ox + ow and oy < y and oy + oh > ny:
                            keep = max(o.min[1], 1)
                            cut = max(oy + keep, ny)
                            o.px = (ox, oy, ow, cut - oy)
                            ny = max(ny, cut)
                    h, y = h + (y - ny), ny
                else:                                    # down from the top
                    nb = min(H, y + h + grow)
                    for o in self.zones:
                        if o is z or o.kind != "w" or o.overlap or o.px is None:
                            continue
                        ox, oy, ow, oh = o.px
                        if ox < x + w and x < ox + ow and oy >= y + h and oy < nb:
                            keep = max(o.min[1], 1)
                            top = min(oy + oh - keep, nb)
                            o.px = (ox, top, ow, oy + oh - top)
                            nb = min(nb, top)
                    h = nb - y
            if nw and nw > w:
                grow = min(nw - w, W - w)
                if "R" in z.pins or x + w / 2.0 >= W / 2.0:   # left from the right
                    nx = max(0, x - grow)
                    for o in self.zones:
                        if o is z or o.kind != "w" or o.overlap or o.px is None:
                            continue
                        ox, oy, ow, oh = o.px
                        if oy < y + h and y < oy + oh and ox < x and ox + ow > nx:
                            keep = max(o.min[0], 1)
                            cut = max(ox + keep, nx)
                            o.px = (ox, oy, cut - ox, oh)
                            nx = max(nx, cut)
                    w, x = w + (x - nx), nx
                else:
                    nr = min(W, x + w + grow)
                    for o in self.zones:
                        if o is z or o.kind != "w" or o.overlap or o.px is None:
                            continue
                        ox, oy, ow, oh = o.px
                        if oy < y + h and y < oy + oh and ox >= x + w and ox < nr:
                            keep = max(o.min[0], 1)
                            lft = min(ox + ow - keep, nr)
                            o.px = (lft, oy, ox + ow - lft, oh)
                            nr = min(nr, lft)
                    w = nr - x
            z.px = (x, y, w, h)

    def fill_gaps(self, W, H, step):
        """Every zone grows into the empty room beside it (window zones first,
        then reserved, then keep clear): each edge out to the first zone in the
        way or the screen edge, on the grid, keeping its pins."""
        step = max(8, int(step or GRID_DEFAULT))
        order = sorted(self.zones, key=lambda z: {"w": 0, "r": 1, "k": 2}[z.kind])
        for z in order:
            if z.overlap or z.lock:                  # (2.6.74) left alone
                continue
            x, y, w, h = z.px
            lim = 0
            for o in self.overlaps_side(z, "L"):
                lim = max(lim, o.px[0] + o.px[2])
            nx = 0 if lim == 0 else ((lim + step - 1) // step) * step
            if nx < x:
                w, x = w + (x - nx), nx
            lim = 0
            for o in self.overlaps_side(z, "T"):
                lim = max(lim, o.px[1] + o.px[3])
            ny = 0 if lim == 0 else ((lim + step - 1) // step) * step
            if ny < y:
                h, y = h + (y - ny), ny
            lim = W
            for o in self.overlaps_side(z, "R"):
                lim = min(lim, o.px[0])
            nr = W if lim == W else (lim // step) * step
            if nr > x + w:
                w = nr - x
            lim = H
            for o in self.overlaps_side(z, "B"):
                lim = min(lim, o.px[1])
            nb = H if lim == H else (lim // step) * step
            if nb > y + h:
                h = nb - y
            z.set_px(x, y, w, h, W, H)

    def overlaps_side(self, z, side):
        """The zones z may not overlap that lie beyond its `side`, in its lane."""
        x, y, w, h = z.px
        out = []
        for o in self.zones:
            if o is z or o.px is None:
                continue
            if (z.kind == "r" and o.kind == "k") or (z.kind == "k" and o.kind == "r"):
                continue
            ox, oy, ow, oh = o.px
            if side in ("L", "R"):
                if not (oy < y + h and y < oy + oh):
                    continue
                if side == "L" and ox + ow <= x:
                    out.append(o)
                elif side == "R" and ox >= x + w:
                    out.append(o)
            else:
                if not (ox < x + w and x < ox + ow):
                    continue
                if side == "T" and oy + oh <= y:
                    out.append(o)
                elif side == "B" and oy >= y + h:
                    out.append(o)
        return out

    def even_out(self, z, W, H, step):
        """(2.6.72) The editor's Even out: zone z and the window zones flush
        beside it in its row (same top and bottom), else in its column (same
        left and right), get equal widths (heights) over the span they cover,
        the seams on the grid. Returns how many zones were evened out."""
        step = max(8, int(step or GRID_DEFAULT))
        D = SNAP_DIST

        def run(horizontal):
            same = [o for o in self.zones if o.kind == "w" and o.px is not None and (
                (abs(o.px[1] - z.px[1]) <= D and abs(o.px[3] - z.px[3]) <= D) if horizontal else
                (abs(o.px[0] - z.px[0]) <= D and abs(o.px[2] - z.px[2]) <= D))]
            i = 0 if horizontal else 1
            same.sort(key=lambda o: o.px[i])
            chain = [z]
            for direction in (1, -1):                # grow the flush chain both ways from z
                cur = z
                while True:
                    nxt = None
                    for o in same:
                        if o in chain:
                            continue
                        if direction == 1 and abs(o.px[i] - (cur.px[i] + cur.px[i + 2])) <= D:
                            nxt = o
                        elif direction == -1 and abs(o.px[i] + o.px[i + 2] - cur.px[i]) <= D:
                            nxt = o
                    if nxt is None:
                        break
                    chain.append(nxt)
                    cur = nxt
            chain.sort(key=lambda o: o.px[i])
            return chain, i
        chain, i = run(True)
        if len(chain) < 2:
            chain, i = run(False)
        if len(chain) < 2:
            return len(chain)
        lo = chain[0].px[i]
        hi = chain[-1].px[i] + chain[-1].px[i + 2]
        n = len(chain)
        edges = [lo]
        for k in range(1, n):
            e = lo + (hi - lo) * k / float(n)
            g = int(round(e / step)) * step
            edges.append(g if abs(g - e) <= step / 2.0 and edges[-1] < g < hi else int(round(e)))
        edges.append(hi)
        for k, o in enumerate(chain):
            x, y, w, h = o.px
            if i == 0:
                o.set_px(edges[k], y, edges[k + 1] - edges[k], h, W, H)
            else:
                o.set_px(x, edges[k], w, edges[k + 1] - edges[k], W, H)
        return n

    def new_id(self):
        n = len(self.zones) + 1
        while self.by_id("Zone %d" % n) is not None:
            n += 1
        return "Zone %d" % n


class ClientWin(object):
    """(2.6.57) One of the client's own windows (TazUO's World Map, its
    journal) seen as a window the layout can place: GetX / GetY / GetWidth /
    GetHeight / SetPos / IsVisible / IsDisposed, as a script window has.
    ClientWin.of(kind) finds the open one (looked for at most every LOOK_EVERY
    s while none is open) and hands the same wrapper back while it stays open,
    so the layout and the keeper can keep track of it. fit(w, h) makes it
    exactly that size and keeps it there, locked with the client's own lock
    (2.6.63: checked on every pass, not asked for once); free() gives back the
    place, size and lock it had before. Client thread only (the keeper's pass)."""
    KINDS = {"worldmap": ("WorldMapGump",), "journal": ("ResizableJournal",)}
    TITLES = {"worldmap": "TazUO's World Map", "journal": "TazUO's journal"}
    #  (2.6.69) how far in from the window's edge the client draws it (the World Map:
    #  WorldMapGump.Draw, gX = x + 4 ... gWidth = Width - 8, whether or not its border
    #  shows), so the layout grows the window by that much on every side
    INSET = {"worldmap": 4}
    DROPS = ("worldmap",)    # (2.6.69) the client windows a drag can slot in a zone
    LOOK_EVERY = 1.0
    TRIES = 4                # passes a size or place may take to land before it is reported
    LOCK_VAR = "Layout_client_locked_%s"   # per character: "1" while the layout holds its lock
    found = {}               # kind -> ClientWin (the open one), or None
    looked = {}              # kind -> when it was last looked for
    errors = {}              # kind -> why the client's windows couldn't be listed (or absent)

    _pt = [None]             # the client's Point type (Microsoft.Xna.Framework.Point)
    _bf = [None]             # Control._bounds (FieldInfo)

    @staticmethod
    def point(x, y):
        """A client Point(x, y) (the type of a control's Location, found once)."""
        import System
        t = ClientWin._pt[0]
        if t is None:
            t = ClientWin._pt[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty(
                "Location").PropertyType
        return System.Activator.CreateInstance(t, System.Array[object]([int(x), int(y)]))

    def __init__(self, kind, raw):
        self.kind, self.raw = kind, raw
        self.own = None      # (x, y, w, h, can_move, locked) before the layout took it
        self.tries = 0       # passes in a row it wasn't the size it was told
        self.fail = {}       # "place" / "size" -> why it didn't take (for the journal line)
        self.warned = False
        self.mins = None     # (min w, min h) the client lets it shrink to
        self._rc = None      # (2.6.82) (pass id, rect) read in this client pass

    @staticmethod
    def of(kind):
        cw = ClientWin.found.get(kind)
        if cw is not None and cw.IsDisposed:
            cw = ClientWin.found[kind] = None
        if cw is not None:
            return cw
        now = time.time()
        if now - ClientWin.looked.get(kind, 0.0) < ClientWin.LOOK_EVERY:
            return None
        ClientWin.looked[kind] = now
        try:
            wins = Tz.windows(ClientWin.KINDS[kind])
            ClientWin.errors.pop(kind, None)
        except Exception as ex:
            wins = []
            ClientWin.errors[kind] = Tz.why(ex)
        for raw in wins:
            try:
                if not raw.IsDisposed:
                    cw = ClientWin(kind, raw)
                    break
            except Exception:
                pass
        ClientWin.found[kind] = cw
        return cw

    # ---------- what the layout and the keeper read and set ----------
    @property
    def IsDisposed(self):
        try:
            return bool(self.raw.IsDisposed)
        except Exception:
            return True

    @property
    def IsVisible(self):
        try:
            return bool(self.raw.IsVisible)
        except Exception:
            return False

    # (2.6.58) a client control's X / Y / Width / Height are by-reference
    # properties IronPython can't read: the rect is read from the control's
    # private _bounds field (found once), the place set through Location
    def rect(self):
        # (2.6.82) read once per client pass (the keeper, the layout and the
        # journal's hold each asked several times); a write here drops it
        hop = HOST.in_hop
        if hop:
            c = self._rc
            if c is not None and c[0] == HOST.pass_id:
                return c[1]
        f = ClientWin._bf[0]
        if f is None:
            from System.Reflection import BindingFlags
            f = ClientWin._bf[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetField(
                "_bounds", BindingFlags.Instance | BindingFlags.NonPublic)
        b = f.GetValue(self.raw)
        r = (int(b.X), int(b.Y), int(b.Width), int(b.Height))
        self._rc = (HOST.pass_id, r) if hop else None
        return r

    def GetX(self):
        return self.rect()[0]

    def GetY(self):
        return self.rect()[1]

    def GetWidth(self):
        return self.rect()[2]

    def GetHeight(self):
        return self.rect()[3]

    def _put_bounds(self, x, y, w, h):
        """Write the control's _bounds directly (a place Location didn't set)."""
        import System
        self.rect()                                  # finds the field
        f = ClientWin._bf[0]
        self._rc = None
        f.SetValue(self.raw, System.Activator.CreateInstance(
            f.FieldType, System.Array[object]([int(x), int(y), int(w), int(h)])))

    def SetPos(self, x, y):
        """Put it at (x, y), checked at once (a place is set in place on the
        client thread): Location, else its bounds."""
        x, y = int(x), int(y)
        why = None
        self._rc = None                              # (2.6.82) read it again after the write
        try:
            self.raw.Location = ClientWin.point(x, y)
        except Exception as ex:
            why = Tz.why(ex)
        try:
            r = self.rect()
            if (r[0], r[1]) == (x, y):
                self.fail.pop("place", None)
                return True
            self._put_bounds(x, y, r[2], r[3])
            if self.rect()[:2] == (x, y):
                self.fail.pop("place", None)
                return True
        except Exception as ex:
            why = why or Tz.why(ex)
        self.fail["place"] = "it couldn't be moved (%s)" % (why or "the client put it back")
        return False

    # ---------- the lock ----------
    def _locked(self):
        try:
            return bool(self.raw.IsLocked)
        except Exception:
            return None

    def _lock(self, on):
        """The client's own lock (ResizableGump.SetLockStatus: no drag, no
        border or resize grip, no right-click close); CanMove where it has none."""
        raw = self.raw
        on = bool(on)
        try:
            if bool(raw.IsLocked) != on:
                Tz.call(raw, "SetLockStatus", (on,))
        except Exception:
            pass
        # (2.6.72) CanMove is checked on every pass, whatever IsLocked reads: the
        # client's own lock call can fail (it is protected), and a click on the map
        # turns dragging back on when its lock didn't take (WorldMapGump.OnMouseUp)
        try:
            if on and raw.CanMove:
                raw.CanMove = False
            elif not on and not raw.CanMove and self.own is not None and self.own[4]:
                raw.CanMove = True
        except Exception:
            pass

    def _min_size(self):
        """The smallest the client lets it be (ResizableGump's _minW / _minH)."""
        if self.mins is None:
            mw = Typing._get(self.raw, "_minW", None, 0)
            mh = Typing._get(self.raw, "_minH", None, 0)
            try:
                self.mins = (int(mw or 0), int(mh or 0))
            except Exception:
                self.mins = (0, 0)
        return self.mins

    # ---------- the fit ----------
    def fit(self, w, h, lock=True):
        """Exactly w x h (its place is set by the layout), locked (unlocked
        while Arrange mode is on, so it can be dragged to another zone). Called
        on every pass while it sits in a zone: it is put back whenever it isn't
        that size (the player resized it, the map went fullscreen, the client
        restored its own size)."""
        raw = self.raw
        if self.own is None:
            try:
                lk = self._locked()
                if lk and Kit.get_var(ClientWin.LOCK_VAR % self.kind, "") == "1":
                    lk = False                       # our own lock, kept over a relog
                self.own = self.rect() + (bool(raw.CanMove), lk)
            except Exception:
                self.own = None
            Kit.put_var(ClientWin.LOCK_VAR % self.kind, "1")
        self._lock(lock)
        mw, mh = self._min_size()
        # (2.6.72) a zone smaller than the client lets it be: (2.6.74) said by the layout,
        # which also places the overflow where it covers least (Layout._client_overflow)
        w, h = max(int(w), mw, 1), max(int(h), mh, 1)
        try:
            r = self.rect()
        except Exception as ex:
            self.fail["size"] = "its size couldn't be read (%s)" % Tz.why(ex)
            return
        if (r[2], r[3]) == (w, h):
            self.tries = 0
            self.fail.pop("size", None)
            return
        self.tries += 1
        if self.tries > ClientWin.TRIES:
            self.fail["size"] = "it stays %d x %d, not %d x %d" % (r[2], r[3], w, h)
        try:
            Tz.put(raw, "_isFullscreen", False)     # the World Map's own fullscreen: off
        except Exception:
            pass
        p = ClientWin.point(w, h)
        self._rc = None
        try:
            Tz.call(raw, "ResizeWindow", (p,))      # lands on the client's next frame
        except Exception as ex:
            try:
                Tz.put(raw, "_savedSize", p)         # what ResizeWindow sets
            except Exception:
                self.fail["size"] = "it couldn't be resized (%s)" % Tz.why(ex)

    def free(self):
        """Back to its own place, size and lock, draggable as before."""
        own, self.own, self.tries = self.own, None, 0
        self._rc = None
        Kit.put_var(ClientWin.LOCK_VAR % self.kind, "")
        if own is None or self.IsDisposed:
            return
        try:
            self._lock(bool(own[5]))
            if not own[5]:
                self.raw.CanMove = own[4]
            Tz.call(self.raw, "ResizeWindow", (ClientWin.point(own[2], own[3]),))
            self.SetPos(own[0], own[1])
        except Exception:
            pass
        self.fail = {}

    def report(self):
        """One journal line (per opened window) when the fit didn't take."""
        if self.fail and not self.warned:
            self.warned = True
            API.SysMsg("%s: %s couldn't be held in its zone: %s." % (
                APP_NAME, ClientWin.TITLES.get(self.kind, self.kind),
                "; ".join(self.fail[k] for k in ("place", "size") if k in self.fail)),
                Kit.HUE_BAD)


class Tex(object):
    """(2.6.73) Pictures drawn by the script itself, in memory (no file of any
    kind): RGBA pixels made into a client texture and filed under a name in
    TazUO's named-texture table, the one a LegionTextureControl draws from by
    name (Character HUD's frame art works the same way). Also the client's own
    gump art as pixels, to draw with. Client thread only. ok is False when this
    client can't be reached that way: the callers then draw as before."""
    ok = None
    parts = {}
    names = set()               # textures made here (dropped on stop)

    @staticmethod
    def find():
        if Tex.ok is not None:
            return Tex.ok
        try:
            import clr
            import System
            from System.Reflection import BindingFlags
            static = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
            inst = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
            p = Tex.parts
            lt = Client._type("ClassicUO.Assets.ExternalImageLoader")
            loader = lt.GetProperty("Instance", static).GetValue(None, None)
            p["table"] = lt.GetField("_zipNamedTextures", inst).GetValue(loader)
            p["device"] = lt.GetProperty("GraphicsDevice", inst).GetValue(loader, None)
            p["tex_t"] = Client._type("Microsoft.Xna.Framework.Graphics.Texture2D")
            p["format"] = System.Enum.Parse(
                Client._type("Microsoft.Xna.Framework.Graphics.SurfaceFormat"), "Color")
            p["set_data"] = [m for m in p["tex_t"].GetMethods()
                             if m.Name == "SetData" and m.IsGenericMethodDefinition
                             and len(m.GetParameters()) == 1][0].MakeGenericMethod(
                                 clr.GetClrType(System.UInt32))
            game = Client._type("ClassicUO.Client").GetProperty("Game", static).GetValue(None, None)
            gumps = Tz.get(Tz.get(game, "UO"), "Gumps")
            p["gumps"] = gumps
            p["hued"] = gumps.GetType().GetMethod("GetHuedGumpPixels")
            Tex.ok = all(p.get(k) is not None for k in ("table", "device", "tex_t", "set_data",
                                                         "gumps", "hued"))
        except Exception:
            Tex.ok = False
        return Tex.ok

    @staticmethod
    def gump_pixels(gid):
        """(pixels, w, h) of gump art gid (RGBA, red in the low byte), or None."""
        import System
        args = System.Array[System.Object]([System.UInt32(gid), System.UInt16(0), False, None])
        px = Tex.parts["hued"].Invoke(Tex.parts["gumps"], args)
        b = args[3]
        if px is None or not len(px) or int(b.Width) <= 0 or int(b.Height) <= 0:
            return None
        return list(px), int(b.Width), int(b.Height)

    @staticmethod
    def put(name, w, h, pixels):
        """Make texture `name` from RGBA pixels (premultiplied), replacing and
        freeing an older one of that name."""
        import System
        p = Tex.parts
        tex = System.Activator.CreateInstance(p["tex_t"], System.Array[System.Object](
            [p["device"], int(w), int(h), False, p["format"]]))
        p["set_data"].Invoke(tex, System.Array[System.Object](
            [System.Array[System.UInt32](pixels)]))
        table = p["table"]
        old = table[name] if table.ContainsKey(name) else None
        table[name] = tex
        Tex.names.add(name)
        if old is not None:
            try:
                old.Dispose()
            except Exception:
                pass

    @staticmethod
    def drop(names=None):
        """Remove and free textures made here (all of them when names is None)."""
        if not Tex.ok:
            return
        table = Tex.parts["table"]
        for name in list(Tex.names if names is None else names):
            Tex.names.discard(name)
            try:
                if table.ContainsKey(name):
                    tex = table[name]
                    table.Remove(name)
                    tex.Dispose()
            except Exception:
                pass

    @staticmethod
    def control(g, name, x, y, w, h):
        """A control drawing texture `name` at (x, y), w x h, taking no mouse."""
        t = G.LegionTextureControl(name, int(w), int(h))
        t.SetRect(int(x), int(y), int(w), int(h))
        try:
            t.SetAcceptMouseInput(False)
        except Exception:
            pass
        g.Add(t)
        return t


class Wyrm(object):
    """(2.6.87) The Wyrm Choir: the carved and dragons looks of the one frame (Settings > Layout's
    Art). Dark Gothic choir-stall stone, one thread of old gold round the game view, ending at two
    parcel-gilt dragons either side of the Action Bar. Client gump art and pictures painted in
    memory (Tex), no files. Built once per layout change, on the keeper's pass (client thread):
    nothing here runs per tick, and what is painted is kept by name for the next build.
    Light comes from the top left. Gold is the exception: bright gold only on the heroes.
    g: the backdrop, under every window and under the game view. eg: above the game view but under
    every window (Surround._pin keeps it there). self.tg: over every window, for the small ornaments
    that must lie on a panel's edge (corner blocks, bosses): never over a window's content.
    zones: [(kind, (x, y, w, h))], arches: Surround.arches' tuples."""
    # the ramps (channels in steps of 8: they survive the client's 16-bit colour)
    S = ("#080810", "#101018", "#181820", "#282830", "#403838", "#585048")           # stone
    GILT = ("#201008", "#401808", "#683818", "#905818", "#B08028", "#D0A848", "#F0E098")   # bole to glint
    GARNET = ("#300810", "#601018", "#981820", "#D04030", "#F8B8A0")
    TILE = 9274                 # the ground: dark slate, tiles truly
    FRAME_W = 96                # dragons: room each side of the bar's window (Surround.art_slot)
    FRAME_MIN_H = 100           # ...only in a bar zone at least this tall: the figure must fit
    made = set()                # names of the pictures painted this session

    def __init__(self, sf, look, zones, arches, W, H):
        self.sf, self.look, self.zones, self.arches, self.W, self.H = sf, look, zones, arches, W, H
        self.game = [z for k, z in zones if k == "k" and z[2] > 2 and z[3] > 2]
        self.panels = [z for k, z in zones if k in ("w", "r")]
        self.tg = None
        self.used = set()
        self.can_paint = False
        try:
            self.can_paint = bool(Tex.find()) and Client.on_client_thread()
        except Exception:
            self.can_paint = False

    # ---------- helpers every part uses ----------
    @staticmethod
    def rgb(hexcol):
        h = hexcol.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @staticmethod
    def px(r, g, b, a=255):
        """One texture pixel: RGBA, premultiplied, red in the low byte."""
        if a >= 255:
            return int(r) | (int(g) << 8) | (int(b) << 16) | (255 << 24)
        return (int(r) * a // 255) | ((int(g) * a // 255) << 8) | ((int(b) * a // 255) << 16) | (int(a) << 24)

    @staticmethod
    def box(g, x, y, w, h, col, alpha=1.0):
        """A flat rectangle, one control: for moulding rows (a row of a moulding is one box)."""
        return Kit.add_box(g, int(x), int(y), int(w), int(h), alpha, col)

    def tile(self, g, gid, x, y, w, h, hue=0):
        t = Kit.add_tiled(g, gid, int(x), int(y), int(w), int(h), hue=hue)
        if t is not None:
            safe(lambda: t.SetAcceptMouseInput(False))
        return t

    @staticmethod
    def pic(g, gid, x, y):
        return Kit.add_pic(g, gid, int(x), int(y), mouse=False)

    def paint(self, g, name, x, y, w, h, fn):
        """A picture painted in memory once, then re-used by name: fn() gives its w * h
        Wyrm.px pixels (row by row). False when this client can't (draw a plain form then)."""
        if not self.can_paint:
            return False
        name = "va_wyrm_" + name
        if name not in Wyrm.made or name not in Tex.names:
            Tex.put(name, w, h, fn())
            Wyrm.made.add(name)
        self.used.add(name)
        Tex.control(g, name, int(x), int(y), w, h)
        return True

    def gump(self, gid):
        """(pixels, w, h) of client gump art, RGBA as Wyrm.px, or None."""
        return Tex.gump_pixels(gid) if self.can_paint else None

    # ---------- the build ----------
    def build(self, g, eg, tg):
        """Each part draws on its own; one that fails is told and the rest still draw.
        Then the pictures no part used this time go (an older layout's sizes): sync disposes
        the old windows in this same pass, before anything draws again."""
        self.tg = tg
        for name, fn in (("stone", self.draw_structure), ("arch", self.draw_arch),
                         ("dragons", self.draw_dragons)):
            if name == "dragons" and self.look != "dragons":
                continue
            try:
                fn(g, eg)
            except Exception as ex:
                HOST._tell("%s: the frame's art (%s) couldn't be drawn: %s%s"
                           % (APP_NAME, name, ex, _error_where()))
        stale = [n for n in Wyrm.made if n not in self.used]
        if stale:
            Tex.drop(stale)
            Wyrm.made.difference_update(stale)

    # ---------- the stone: ground, screen frame, seams, game-view border, bosses, corner blocks ----------
    ST_SEAM = (0, 4, 13, 14, 11, 0, 2, 0)        # the 8 px seam, light side first (0-5 stone, 10-16 gilt)
    ST_FRAME = (4, 14, 11, 0)                    # the screen's edge: 4 px show of it, light side first
    ST_TILE = 256                                # a seam's repeat: one rosette, pellets every 64
    ST_PX = 16000                                # new pixels one build may compute (a layout costs about 11000)
    ST_BLOCK = 20                                # the corner block
    ST_GLINTS = (5, 3), (46, 4), (98, 3), (150, 5), (212, 3)     # a seam tile's glints (at, long)

    def _st_col(self, i):
        """A colour by ramp index: 0-5 stone, 10-16 gilt."""
        return Wyrm.GILT[i - 10] if i >= 10 else Wyrm.S[i]

    def _st_px(self, i):
        c = self._st_cols.get(i)
        if c is None:
            r, g_, b = Wyrm.rgb(self._st_col(i))
            c = self._st_cols[i] = Wyrm.px(r, g_, b)
        return c

    def _st_paint(self, g, name, x, y, w, h, fn):
        """self.paint, with a limit on what this build newly computes: a kept picture costs nothing."""
        if not self.can_paint:
            return False
        made = "va_wyrm_" + name
        if made not in Wyrm.made or made not in Tex.names:
            if self._st_new + w * h > Wyrm.ST_PX:
                return False
            self._st_new += w * h
        return self.paint(g, name, x, y, w, h, fn)

    def _st_band(self, g, horiz, x, y, length, idx):
        """A moulding as one control: one line of its rows, stretched along the run."""
        if length <= 0:
            return
        n = len(idx)
        w, h = (length, n) if horiz else (n, length)
        px = [self._st_px(i) for i in idx]
        name = "st_b%s_%s" % ("h" if horiz else "v", "_".join([str(i) for i in idx]))
        made = "va_wyrm_" + name
        tw, th = (1, n) if horiz else (n, 1)
        if self.can_paint:
            if made not in Wyrm.made or made not in Tex.names:
                Tex.put(made, tw, th, px)
                Wyrm.made.add(made)
            self.used.add(made)
            Tex.control(g, made, int(x), int(y), w, h)
            return
        Wyrm.box(g, x, y, w, h, Wyrm.S[0])       # no pictures on this client: dark, and its gold
        top = max(idx)
        if top >= 10:
            at = list(idx).index(top)
            if horiz:
                Wyrm.box(g, x, y + at, length, 1, self._st_col(top))
            else:
                Wyrm.box(g, x + at, y, 1, length, self._st_col(top))

    def _st_foil(self, n, ramp, top):
        """A quatrefoil, n x n, lit from the top left: [row by row] of ramp levels (None: not on it,
        -1: its shadow). The list comes with a 2 px shadow lower right, so it is (n + 2) square.
        Each petal is lit by its own normal; a cut between petals; a dimple in a small button."""
        m = n + 2
        c = (n - 1) / 2.0
        off = n * 0.26
        rad = n * 0.26
        lobes = ((off, 0.0), (-off, 0.0), (0.0, off), (0.0, -off))
        out = [None] * (m * m)
        inside = {}
        for y in range(n):
            dy = y - c
            for x in range(n):
                dx = x - c
                best, ax, ay = 1e9, 0.0, 0.0
                for lx, ly in lobes:
                    bx, by = dx - lx, dy - ly
                    d2 = bx * bx + by * by
                    if d2 < best:
                        best, ax, ay = d2, bx, by
                r = best ** 0.5
                d = r - rad
                if d > 0.5:
                    continue
                inside[x + y * m] = True
                lit = -(ax + ay) / (rad * 1.414)
                near = dx * dx + dy * dy
                adx, ady = abs(dx), abs(dy)
                if near < n * 0.1:
                    i = 0                         # the dimple
                elif near < n * 0.42:
                    i = top if dx + dy < 0 else top - 2
                elif adx - ady < 0.8 and ady - adx < 0.8 and d < -0.5:
                    i = top - 3                   # the cut between petals
                elif d > -0.5:                    # the rim, by its normal
                    i = top + 1 if lit > 0.72 else (top - 1 if lit > -0.25 else top - 4)
                elif lit > 0.2:
                    i = top
                elif lit > -0.3:
                    i = top - 1
                else:
                    i = top - 2
                out[x + y * m] = ramp[max(1, min(i, len(ramp) - 1))] if i else ramp[0]
        for key in list(inside):                  # the shadow it throws
            k2 = key + 2 + 2 * m
            if k2 < m * m and k2 not in inside:
                out[k2] = -1
        return out

    def _st_foil_px(self, n, ramp, top):
        """A foil as Wyrm.px pixels."""
        sh = Wyrm.px(8, 8, 16, 170)
        res = []
        for v in self._st_foil(n, ramp, top):
            if v is None:
                res.append(0)
            elif v == -1:
                res.append(sh)
            else:
                res.append(self._st_px(v))
        return res

    def _st_ramp(self):
        return (0, 10, 11, 12, 13, 14, 15, 16)   # foil levels: 0 the dimple, then bole to glint

    def _st_boss(self, layer, cx, cy):
        """A 16 px quatrefoil at a crossing, over the windows: it reaches 4 px past their edge.
        It always goes in self.tg, whatever layer the caller holds (the arch calls this too)."""
        if not self._st_paint(self.tg, "st_boss16", cx - 8, cy - 8, 18, 18,
                              lambda: self._st_foil_px(16, self._st_ramp(), 5)):
            Wyrm.box(self.tg, cx - 4, cy - 4, 8, 8, Wyrm.GILT[3])

    def _st_piece(self, length, tile, centre, stop_a, stop_b):
        """The columns of a piece of seam, each 8 ints. tile: it is the repeat (rosette in the middle).
        centre: where the run's centre lies on it, or None; pellets are every 64 from there."""
        base = [self._st_px(i) for i in Wyrm.ST_SEAM]
        cols = [base] * length
        px = self._st_px

        def put(u, v, i):
            if 0 <= u < length:
                if cols[u] is base:
                    cols[u] = list(base)
                cols[u][v] = px(i)

        # glints: on the bead, irregular
        if tile:
            for at, n in Wyrm.ST_GLINTS:
                for u in range(at, at + n):
                    put(u, 3, 15)
        elif length > 40:
            at = 11 + (length * 7) % 19
            for u in range(at, at + 3):
                put(u, 3, 15)
        # pellets
        if centre is not None:
            k = centre % 64
            for u in range(k, length, 64):
                far = min(u if stop_a else 99, length - 1 - u if stop_b else 99)
                if far < 12 or (u == centre and (tile or length >= 96)):
                    continue
                put(u - 2, 3, 12), put(u + 2, 3, 12)      # a small collar each side
                put(u - 1, 2, 14), put(u, 2, 15), put(u + 1, 2, 13)
                put(u - 1, 3, 14), put(u, 3, 15), put(u + 1, 3, 13)
                put(u - 1, 4, 12), put(u, 4, 13), put(u + 1, 4, 11)
                put(u - 1, 5, 0), put(u, 5, 11), put(u + 1, 5, 0)
        # the rosette: a small foil cut in the bead
        if centre is not None and 0 <= centre < length and (tile or length >= 96):
            f = self._st_foil(8, self._st_ramp(), 5)
            for vv in range(8):
                for uu in range(8):
                    c = f[uu + vv * 10]
                    if c is not None and c != -1:
                        put(centre - 4 + uu, vv, c)
            for vv in (2, 3, 4):                  # the bead stops a pixel short of it
                put(centre - 5, vv, 0), put(centre + 4, vv, 0)
        # the stops: the bead swells to a leaf, then a shadow where it dies into the next moulding
        for stop, sign, at in ((stop_a, 1, 0), (stop_b, -1, length - 1)):
            if not stop or length < 10:
                continue
            for v in range(8):
                put(at, v, 0), put(at + sign, v, 0)
            for k, h in enumerate((1, 2, 3, 2, 1)):       # from the shadow outwards, half height
                u = at + sign * (2 + k)
                for v in range(3 - h, 4 + h):
                    i = 14 if v < 3 else (13 if v == 3 else 11)
                    if v == 3 - h:
                        i = 15 if k in (1, 2) else 14
                    if v == 3 + h:
                        i = 10
                    put(u, v, i)
                if 4 + h < 8:
                    put(u, 4 + h, 0)
        return cols

    def _st_pack(self, cols, horiz):
        """Columns to the picture's rows (a vertical run is the same moulding transposed: the top-left
        light stays where it was)."""
        out = []
        if horiz:
            for row in zip(*cols):
                out.extend(row)
        else:
            for col in cols:
                out.extend(col)
        return out

    def _st_seam(self, g, horiz, pos, a, b):
        """The 8 px seam at pos, from a to b along its run. Laid out from its centre, so the ends match:
        a piece of ornament, the repeat as often as it fits, the same piece on the far side."""
        L = b - a
        if L <= 0:
            return
        if not self.can_paint:
            if horiz:
                self._st_band(g, True, a, pos - 4, L, Wyrm.ST_SEAM)
            else:
                self._st_band(g, False, pos - 4, a, L, Wyrm.ST_SEAM)
            return
        T = Wyrm.ST_TILE
        n = L // T
        ax =(lambda u, l: (a + u, pos - 4, l, 8)) if horiz else (lambda u, l: (pos - 4, a + u, 8, l))
        d = "h" if horiz else "v"

        def piece(u, l, name, centre, sa, sb, tile=False):
            x, y, w, h = ax(u, l)
            if not self._st_paint(g, "st_s%s_%s_%d" % (d, name, l), x, y, w, h,
                                  lambda: self._st_pack(self._st_piece(l, tile, centre, sa, sb), horiz)):
                self._st_band(g, horiz, x, y, l, Wyrm.ST_SEAM)

        if n == 0:
            piece(0, L, "w", L // 2, True, True)
            return
        ra = (L - n * T) // 2
        rb = L - n * T - ra
        if ra:
            piece(0, ra, "a", ra - T, True, False)
        for i in range(n):
            piece(ra + i * T, T, "t", T // 2, False, False, True)
        if rb:
            piece(L - rb, rb, "b", -T, False, True)

    def _st_glints(self, g, horiz, x, y, length):
        """The frame's glints: a 384 px line of them, mostly clear, over a straight run."""
        at = 40
        S = 384
        step = S + 73
        while at + S < length:
            xx, yy, ww, hh = (x + at, y, S, 1) if horiz else (x, y + at, 1, S)
            if not self._st_paint(g, "st_gl" + ("h" if horiz else "v"), xx, yy, ww, hh,
                                  lambda: self._st_glint_px(S)):
                return
            at += step

    def _st_glint_px(self, S):
        out = [0] * S
        hi = self._st_px(15)
        mid = self._st_px(14)
        at = 17
        i = 0
        gaps = (61, 47, 83, 53, 71, 41, 89, 59)
        while at + 6 < S:
            n = 3 + (i % 3)
            for k in range(n):
                out[at + k] = hi if 0 < k < n - 1 else mid
            at += gaps[i % 8]
            i += 1
        return out

    def _st_corner_px(self, left, top):
        """A chamfered stone block at a screen corner, one small crisp foil in its sunk field, and a
        crocket on each run, where a leaf of stone springs off the frame."""
        S = Wyrm.ST_BLOCK
        T = S + 5
        px = self._st_px
        n = 10
        foil = self._st_foil(n, self._st_ramp(), 5)
        fo = (S - n) // 2
        sh = Wyrm.px(8, 8, 16, 170)
        sx = 1 if left else -1
        sy = 1 if top else -1
        far = S - 1
        ox, oy = 0 if left else T - S, 0 if top else T - S
        out = [0] * (T * T)
        for ty in range(T):
            v = ty if top else T - 1 - ty
            for tx in range(T):
                u = tx if left else T - 1 - tx
                if u >= S or v >= S:
                    continue
                # the nearest edge, and which way it faces on the screen
                d, nx, ny = u, -sx, 0
                if v < d:
                    d, nx, ny = v, 0, -sy
                if far - u < d:
                    d, nx, ny = far - u, sx, 0
                if far - v < d:
                    d, nx, ny = far - v, 0, sy
                e = (2 * far - u - v - 7) * 0.71          # the inner chamfer
                if e < d:
                    d, nx, ny = e, sx, sy
                e = (far - u + v - 3) * 0.71
                if e < d:
                    d, nx, ny = e, sx, -sy
                e = (u + far - v - 3) * 0.71
                if e < d:
                    d, nx, ny = e, -sx, sy
                if d < 0:
                    continue
                lit = -(nx + ny)                          # the light is from the top left
                if d < 1:
                    i = 0
                elif d < 2:
                    i = 5 if lit > 0 else (1 if lit < 0 else 3)
                elif d < 3:
                    i = 4 if lit > 0 else (2 if lit < 0 else 3)
                elif d < 4:
                    i = 0                                 # the field is sunk: its walls light the other way
                elif d < 5:
                    i = 2 if lit > 0 else (4 if lit < 0 else 3)
                else:
                    i = 3
                fu, fv = tx - ox - fo, ty - oy - fo
                if 0 <= fu < n + 2 and 0 <= fv < n + 2:
                    c = foil[fu + fv * (n + 2)]
                    if c == -1:
                        i = 1
                    elif c is not None:
                        i = c
                out[tx + ty * T] = px(i)
        for dx in range(5):
            h = 7 - dx
            for dv in range(3, h):
                for across, u, v in ((top, S + dx, dv), (left, dv, S + dx)):
                    if dv == h - 1:
                        c = sh
                    elif dv == 3 and dx < 2:
                        c = px(13)
                    else:
                        c = px(4 if across else 2)
                    out[(u if left else T - 1 - u) + (v if top else T - 1 - v) * T] = c
        return out

    def _st_corners(self):
        S = Wyrm.ST_BLOCK
        T = S + 5
        W, H = self.W, self.H
        tg = self.tg
        for left, top in ((True, True), (False, True), (True, False), (False, False)):
            cx = 0 if left else W - 1
            cy = 0 if top else H - 1
            if [1 for r in self._st_world if r[0] <= cx < r[0] + r[2] and r[1] <= cy < r[1] + r[3]]:
                continue
            x = 0 if left else W - T
            y = 0 if top else H - T
            name = "st_cn%s%s" % ("l" if left else "r", "t" if top else "b")
            fn = (lambda l, t: lambda: self._st_corner_px(l, t))(left, top)
            if not self._st_paint(tg, name, x, y, T, T, fn):
                bx, by = 0 if left else W - S, 0 if top else H - S
                Wyrm.box(tg, bx, by, S, S, Wyrm.S[3])
                Wyrm.box(tg, bx + S // 2 - 3, by + S // 2 - 3, 6, 6, Wyrm.GILT[4])

    @staticmethod
    def _st_less(a, b, cuts):
        """The spans of a..b less the spans in cuts."""
        out = []
        at = a
        for c0, c1 in sorted(cuts):
            if c1 <= at or c0 >= b:
                continue
            if c0 > at:
                out.append((at, c0))
            at = max(at, c1)
        if at < b:
            out.append((at, b))
        return out

    def _st_frame(self, g):
        """The frame at the screen's edges, except where the world or a dragon's room reaches them."""
        W, H = self.W, self.H
        M = Kit.ZONE_INSET
        F = Wyrm.ST_FRAME
        B = 1                                         # the bead's row
        for side in ("T", "B", "L", "R"):
            horiz = side in "TB"
            size = W if horiz else H
            cuts = []
            for x, y, w, h in self._st_world:
                if horiz and ((side == "T" and y <= 3) or (side == "B" and y + h >= H - 3)):
                    cuts.append((x - M if x > 3 else x, x + w + M if x + w < W - 3 else x + w))
                if not horiz and ((side == "L" and x <= 3) or (side == "R" and x + w >= W - 3)):
                    cuts.append((y - M if y > 3 else y, y + h + M if y + h < H - 3 else y + h))
            if side == "B":
                cuts.extend([(r[0], r[0] + r[2]) for r in self._st_free])
            at = 0 if side in "TL" else (H if horiz else W) - len(F)
            for a, b in Wyrm._st_less(0, size, cuts):
                if horiz:
                    self._st_band(g, True, a, at, b - a, F)
                    self._st_glints(g, True, a, at + B, b - a)
                else:
                    self._st_band(g, False, at, a, b - a, F)
                    self._st_glints(g, False, at + B, a, b - a)

    def _st_border(self, g, eg, side, game, spans):
        """The game view's border on one side, in the stone beside it; on the world when flush with the
        screen: S0, S3, G2, G3 or G2 from outside, then G0 and a shadow on the world."""
        kx, ky, kw, kh = game
        W, H = self.W, self.H
        M = Kit.ZONE_INSET
        near = side in "TL"                           # the light's side: the shadow is deep there
        rows = (0, 3, 13, 14) if near else (13, 13, 3, 0)
        horiz = side in "TB"
        edge = {"L": kx, "T": ky, "R": kx + kw, "B": ky + kh}[side]
        lim = H if horiz else W
        flush = edge < M if near else edge > lim - M
        at = (edge if flush else edge - M) if near else (edge - M if flush else edge)
        layer = eg if flush else g
        sh, alpha = (at + M + 1, 0.5) if near else (at - 3, 0.25)
        gz = at + M if near else at - 1
        dark, shadow = Wyrm.GILT[0], Wyrm.S[0]
        for a, b in spans:
            if b <= a:
                continue
            if horiz:
                self._st_band(layer, True, a, at, b - a, rows)
                Wyrm.box(eg, a, gz, b - a, 1, dark)
                Wyrm.box(eg, a, sh, b - a, 2, shadow, alpha)
            else:
                self._st_band(layer, False, at, a, b - a, rows)
                Wyrm.box(eg, gz, a, 1, b - a, dark)
                Wyrm.box(eg, sh, a, 2, b - a, shadow, alpha)

    def _st_view(self, g, eg):
        """The border round each game view, and a boss where its corner meets a seam."""
        M = Kit.ZONE_INSET
        W, H = self.W, self.H
        G_ = Kit.GAP
        for game in self._st_world:
            kx, ky, kw, kh = game
            arch = None
            for a in self.arches:
                if tuple(a[:4]) == tuple(game):
                    arch = a
            bot = ky + kh
            over = [p for p in self.panels if self._st_overlaps(p, game)]
            free = [r for r in self._st_free if r[1] <= bot + 3 and r[1] + r[3] > bot]
            for side in ("L", "R"):
                # stopped by the frames lying over the view (the arch has what's beside them)
                x = kx if side == "L" else kx + kw
                cuts = []
                for p in over:
                    if p[0] <= x + 3 and p[0] + p[2] >= x - 3:
                        cuts.append((p[1], p[1] + p[3] + (G_ if arch else 0)))
                # it runs on past the corner, to a boss or the end of the view
                end = bot + (M if bot < H - M else 0)
                spans = Wyrm._st_less(ky, end, cuts)
                self._st_border(g, eg, side, game, spans)
                # quiet stone in the margin where the border doesn't run
                if (side == "L" and kx >= M) or (side == "R" and kx + kw <= W - M):
                    at = kx - M if side == "L" else kx + kw
                    for a, b in Wyrm._st_less(ky, bot, spans):
                        self._st_band(g, False, at, a, b - a, (0, 2, 3, 2) if side == "L" else (2, 3, 2, 0))
            if bot < H - M:
                a0, b0 = kx + M, kx + kw - M
                cuts = [(r[0], r[0] + r[2]) for r in free]
                self._st_border(g, eg, "B", game, Wyrm._st_less(a0, b0, cuts))
            if arch is None:
                cuts = [(p[0], p[0] + p[2]) for p in over if p[1] <= ky + 3]
                self._st_border(g, eg, "T", game, Wyrm._st_less(kx, kx + kw, cuts))
            # the corners: a boss where the border turns and a seam goes on
            if bot < H - M:
                for x, at_left in ((kx, True), (kx + kw, False)):
                    if (at_left and x < M) or (not at_left and x > W - M):
                        continue
                    if [r for r in free if r[0] - 3 <= x <= r[0] + r[2] + 3]:
                        continue
                    self._st_boss(self.tg, x, bot + M // 2)

    @staticmethod
    def _st_overlaps(a, b):
        return (a[0] + 3 < b[0] + b[2] and b[0] + 3 < a[0] + a[2] and
                a[1] + 3 < b[1] + b[3] and b[1] + 3 < a[1] + a[3])

    def _st_seams(self, g):
        """Every contact (or a gap under 24 px) of two panels is a seam; contacts on one line join."""
        M = Kit.ZONE_INSET
        runs = {}
        ps = self._st_set
        for i in range(len(ps)):
            for j in range(len(ps)):
                if i == j:
                    continue
                a, b = ps[i], ps[j]
                gx = b[0] - (a[0] + a[2])
                if -3 <= gx < 24:
                    y0, y1 = max(a[1], b[1]), min(a[1] + a[3], b[1] + b[3])
                    if y1 - y0 > 3:
                        runs.setdefault((False, a[0] + a[2] + gx // 2), []).append((y0, y1))
                gy = b[1] - (a[1] + a[3])
                if -3 <= gy < 24:
                    x0, x1 = max(a[0], b[0]), min(a[0] + a[2], b[0] + b[2])
                    if x1 - x0 > 3:
                        runs.setdefault((True, a[1] + a[3] + gy // 2), []).append((x0, x1))
        for (horiz, pos), spans in sorted(runs.items()):
            spans.sort()
            at, end = spans[0]
            joined = []
            for s0, s1 in spans[1:]:
                if s0 <= end + 3:
                    end = max(end, s1)
                else:
                    joined.append((at, end))
                    at, end = s0, s1
            joined.append((at, end))
            for s0, s1 in joined:
                self._st_seam(g, horiz, pos, s0 + M, s1 - M)

    def _st_gaps(self):
        """Rectangles no zone covers, at least 24 px each way."""
        solid = self._st_set + self._st_world + self._st_free
        xs = sorted(set([0, self.W] + [r[0] for r in solid] + [r[0] + r[2] for r in solid]))
        ys = sorted(set([0, self.H] + [r[1] for r in solid] + [r[1] + r[3] for r in solid]))
        xs = [v for v in xs if 0 <= v <= self.W]
        ys = [v for v in ys if 0 <= v <= self.H]
        out, run = [], {}
        for j in range(len(ys) - 1):
            y0, y1 = ys[j], ys[j + 1]
            now, at = {}, None
            for i in range(len(xs) - 1):
                x0 = xs[i]
                if [1 for r in solid if r[0] < xs[i + 1] and r[0] + r[2] > x0 and r[1] < y1 and r[1] + r[3] > y0]:
                    if at is not None:
                        k = (at, x0)
                        now[k] = run.pop(k, y0)
                        at = None
                elif at is None:
                    at = x0
            if at is not None:
                k = (at, xs[-1])
                now[k] = run.pop(k, y0)
            for (a, b), top in run.items():
                out.append((a, top, b - a, y0 - top))
            run = now
        for (a, b), top in run.items():
            out.append((a, top, b - a, ys[-1] - top))
        return [r for r in out if r[2] >= 24 and r[3] >= 24]

    def _st_recess(self, g, r):
        """A gap: a quiet sunk panel, one carved piece in its middle."""
        x, y, w, h = r
        Wyrm.box(g, x, y, w, h, Wyrm.S[0], 0.35)
        Wyrm.box(g, x, y, w, 1, Wyrm.S[0])
        Wyrm.box(g, x, y, 1, h, Wyrm.S[0])
        Wyrm.box(g, x, y + h - 1, w, 1, Wyrm.S[3])
        Wyrm.box(g, x + w - 1, y, 1, h, Wyrm.S[3])
        if min(w, h) >= 40:
            n = 20
            self._st_paint(g, "st_rec20", x + (w - n) // 2, y + (h - n) // 2, n + 2, n + 2,
                           lambda: self._st_foil_px(n, (0, 1, 1, 2, 3, 3, 4, 5), 5))

    def draw_structure(self, g, eg):
        self._st_cols = {}
        self._st_new = 0
        W, H = self.W, self.H
        self._st_world = [tuple(z) for z in self.game]
        # the panels set in the stone; those lying over the game view are the arch's
        self._st_set, self._st_free = [], []
        for p in self.panels:
            p = tuple(p)
            if [1 for k in self._st_world if Wyrm._st_overlaps(p, k)]:
                continue
            r = p
            if self.look == "dragons":
                r = tuple(self.sf.art_slot(p, W, H, self.zones))
            self._st_set.append(r)
            if r != p:                                # the dragons' room, either side of the bar
                self._st_free.append((p[0], p[1], r[0] - p[0], p[3]))
                self._st_free.append((r[0] + r[2], p[1], p[0] + p[2] - r[0] - r[2], p[3]))
        # the ground: dark slate, dimmed so its tile doesn't show
        for x, y, w, h in Surround._stone_rects(self.zones, W, H):
            if self.tile(g, Wyrm.TILE, x, y, w, h) is None:
                Wyrm.box(g, x, y, w, h, Wyrm.S[2])
            else:
                Wyrm.box(g, x, y, w, h, Wyrm.S[0], 0.55)
        for r in self._st_gaps()[:4]:
            self._st_recess(g, r)
        self._st_corners()                            # the small pictures first, if the limit bites
        self._st_view(g, eg)
        self._st_frame(g)
        self._st_seams(g)
        # the margins beside the dragons' room: not over the border above or the bead below
        M = Kit.ZONE_INSET
        for r in self._st_free:
            y0 = r[1] + M
            y1 = min(r[1] + r[3], H - M)
            if r[0] >= M and r[0] < W // 2:
                self._st_band(g, False, r[0] - M, y0, y1 - y0, (0, 2, 3, 2))
            elif r[0] + r[2] <= W - M and r[0] >= W // 2:
                self._st_band(g, False, r[0] + r[2], y0, y1 - y0, (2, 3, 2, 0))

    # ---------- the arch: hood mould, spandrels, crown ----------
    # Outline as Surround.arch_top / _arch_pixels: flat a GAP under each corner frame, a smoothstep
    # S-curve over the run, flat across the crown. The crown line is never above the crown strip
    # (ARCH_CROWN), so the moulding always has room. Bands below are by distance d from the curve,
    # out of the world: bole, bead, bead edge, fillet, hairline; then a hollow and an arris.
    def draw_arch(self, g, eg):
        for a in self.arches:
            self._ar_one(eg, a)

    def _ar_one(self, eg, a):
        kx, ky, kw, kh, left, right, run, flat = a
        crown = max(10, int(round(ARCH_CROWN * self.H / 1080.0)))
        gap = Kit.GAP
        if flat:
            T = max([ky, 6] + [s[2] for s in (left, right) if s is not None])
            y0 = max(0, min(ky, T - crown))
            xl, xr = kx, kx + kw
            sa = left[1] if left is not None else kx     # the stone between the corner frames
            sb = right[0] if right is not None else kx + kw
        else:
            T = max(ky, crown)
            y0 = max(0, T - crown)
            if left is not None and left[2] <= T:
                left = None
            if right is not None and right[2] <= T:
                right = None
            xl = left[1] + gap + run if left is not None else kx
            xr = right[0] - gap - run if right is not None else kx + kw
            if xr <= xl:
                xl = xr = (xl + xr) // 2
            sa, sb = xl, xr
        geo = {"kx": kx, "kw": kw, "T": T, "y0": y0, "run": run, "xl": xl, "xr": xr, "gap": gap,
               "flat": flat, "sa": sa, "sb": sb}
        if not self.can_paint:
            self._ar_plain(eg, geo, left, right)
            return
        self._ar_ramps()
        # the crown's stone first: it starts at the left shoulder's corner, and the rows there share it
        ca = sa
        cb = sb
        if not flat:
            ca = left[1] - Kit.ZONE_INSET if left is not None else sa
            cb = right[0] + Kit.ZONE_INSET if right is not None else sb
        self._ar_y0 = y0
        if cb > ca and T - 1 > y0:
            self.tile(eg, Wyrm.TILE, ca, y0, cb - ca, T - 1 - y0 if not flat else T - 5 - y0)
        for side, sh in (("L", left), ("R", right)):
            if sh is not None and not flat:
                self._ar_shoulder(eg, geo, side, sh, 0)
        if cb > ca and T - 1 > y0:
            self.box(eg, ca, y0, cb - ca, T - 1 - y0 if not flat else T - 5 - y0, Wyrm.S[0], 0.55)
        for side, sh in (("L", left), ("R", right)):
            if sh is not None:
                self._ar_rim(eg, geo, side, sh)
                if not flat:
                    self._ar_shoulder(eg, geo, side, sh, 1)
        self._ar_crown(eg, geo)

    # ---------- colour ----------
    AR_HOLLOW = (16, 16, 24)                     # the hollow beside the moulding, as the dimmed slate falls off

    def _ar_ramps(self):
        self._ar_G = [self.rgb(c) for c in Wyrm.GILT]
        self._ar_S = [self.rgb(c) for c in Wyrm.S]
        self._ar_A = [self.rgb(c) for c in Wyrm.GARNET]

    def _ar_stone(self, eg, x, y, w, h):
        """Slate as a control, dimmed as the ground is."""
        if w > 0 and h > 0:
            if self.tile(eg, Wyrm.TILE, x, y, w, h) is None:
                self.box(eg, x, y, w, h, Wyrm.S[2])
            else:
                self.box(eg, x, y, w, h, Wyrm.S[0], 0.55)

    def _ar_strip(self, eg, horiz, x, y, length, rows):
        """A moulding as one control: one line of its rows stretched along the run.
        rows: [(hex colour, alpha)], light side first."""
        n = len(rows)
        if length <= 0 or not n:
            return
        if not self.can_paint:
            for i in range(n):
                col, al = rows[i]
                if horiz:
                    self.box(eg, x, y + i, length, 1, col, al)
                else:
                    self.box(eg, x + i, y, 1, length, col, al)
            return
        name = "va_wyrm_ar_m%s_%s" % ("h" if horiz else "v",
                                      "_".join(["%s%d" % (c[1:], int(a * 100)) for c, a in rows]))
        if name not in Wyrm.made or name not in Tex.names:
            px = []
            for col, al in rows:
                r_, g_, b_ = self.rgb(col)
                px.append(Wyrm.px(r_, g_, b_, int(al * 255)))
            Tex.put(name, 1 if horiz else n, n if horiz else 1, px)
            Wyrm.made.add(name)
        self.used.add(name)
        Tex.control(eg, name, int(x), int(y), length if horiz else n, n if horiz else length)

    def _ar_gold(self, v):
        """The ramp at a fractional step: v = 4.0 is G4."""
        G = self._ar_G
        v = 0.0 if v < 0 else (6.0 if v > 6 else v)
        i = int(v)
        if i >= 6:
            return G[6]
        t = v - i
        p, q = G[i], G[i + 1]
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, p[2] + (q[2] - p[2]) * t)

    @staticmethod
    def _ar_lit(lit):
        """Bead step from the normal's dot with the light: 0.8 (a level top run) gives G4."""
        if lit >= 0.8:
            return 4.0 + (lit - 0.8) * 6.0
        return 4.0 - (0.8 - lit) * 0.7

    # ---------- one shoulder: slate as a stair of controls, a narrow painted band over its edge ----------
    AR_BAND = 28                                 # px along x of one piece of the band

    def _ar_columns(self, side, xs, x0, x1, b, T, run):
        """Per column, from the hood out to the crown: (x, curve y, cos, normal x, light)."""
        lt = side == "L"
        span = float(b - T)
        ss = Surround._ss
        out = []
        for i in range(x1 - x0):
            x = x0 + i if lt else x1 - 1 - i
            u = (x + 0.5 - xs) / float(run) if lt else (xs - (x + 0.5)) / float(run)
            if u <= 0:
                ye, c, sl = float(b), 1.0, 0.0
            elif u >= 1:
                ye, c, sl = float(T), 1.0, 0.0
            else:
                ye = b - ss(u) * span
                sl = span * 6.0 * u * (1.0 - u) / run
                c = 1.0 / math.sqrt(1.0 + sl * sl)
            nx = (-sl * c) if lt else (sl * c)       # the normal out of the world
            out.append((x, ye, c, nx, -0.6 * nx + 0.8 * c))
        return out

    def _ar_shoulder(self, eg, geo, side, sh, stage):
        """stage 0: the stone. stage 1: all that lies on it."""
        bx0, bx1, b = sh
        T, y0, run, gap = geo["T"], geo["y0"], geo["run"], geo["gap"]
        lt = side == "L"
        if lt:
            xs = bx1 + gap
            x0, x1 = bx1 - Kit.ZONE_INSET, xs + run
        else:
            xs = bx0 - gap
            x0, x1 = xs - run, bx0 + Kit.ZONE_INSET
        if x1 <= x0 or b <= T:
            return
        cols = self._ar_columns(side, xs, x0, x1, b, T, run)
        if stage == 0:
            self._ar_stair(eg, cols, lt, x0, x1, T, b)
            return
        self._ar_band(eg, side, cols, xs, x0, x1, y0, b, T, run)
        self._ar_hood(eg, side, xs, x0, x1, y0, b)
        self._ar_roundel(eg, geo, side, xs, b)

    def _ar_stair(self, eg, cols, lt, x0, x1, T, b):
        """Rows of slate whose stepped edge stays under the band's opaque part (9 px deep). All start from
        the same corner as the crown's stone, so on the left the slate runs on with no seam."""
        ya = T - 1
        i = len(cols) - 1
        rows = []
        while ya < b - 1:
            # the last column (towards the hood) still within reach of this row's top
            while i > 0 and (cols[i - 1][1] - ya) * cols[i - 1][2] <= 9.0:
                i -= 1
            if i <= 0:
                break
            x, ye, c = cols[i][0], cols[i][1], cols[i][2]
            yb = int(ye - 0.5 / c)
            if yb <= ya:
                yb = ya + 1
            rows.append((ya, yb, x + 1 if not lt else x))
            ya = yb
        for ya, yb, ex in rows:
            if lt:
                if ex > x0:
                    self.tile(eg, Wyrm.TILE, x0, self._ar_y0, ex - x0, yb - self._ar_y0)
            elif ex < x1:
                self.tile(eg, Wyrm.TILE, ex, ya, x1 - ex, yb - ya)
        for ya, yb, ex in rows:
            if lt:
                if ex > x0:
                    self.box(eg, x0, ya, ex - x0, yb - ya, Wyrm.S[0], 0.55)
            elif ex < x1:
                self.box(eg, ex, ya, x1 - ex, yb - ya, Wyrm.S[0], 0.55)

    def _ar_band(self, eg, side, cols, xs, x0, x1, y0, b, T, run):
        """The band in pieces, each a small rectangle along the curve, clear where it isn't."""
        lt = side == "L"
        vx = (x0 + 2.0) if lt else (x1 - 2.0)
        R = abs(xs - vx)
        cy = b - 2.5 - R
        first = abs(xs - (x0 if lt else x1)) + Wyrm.AR_BAND // 2
        n = len(cols)
        cusps = self._ar_cusps(xs, lt, run, float(b - T))
        at = 0
        k = 0
        while at < n:
            end = first if k == 0 else at + Wyrm.AR_BAND
            end = n if end + 8 > n else end
            piece = cols[at:end]
            top, bot = 1 << 30, -1
            for q in piece:
                dp = 13.0 if [1 for u_ in cusps if abs(q[0] + 0.5 + 4.0 * q[3] - u_[0]) < u_[1] + 4.0] else 3.0
                top = min(top, int(q[1] - 10.8 / q[2] - 1))
                bot = max(bot, int(q[1] + dp / q[2] + 1))
            if k == 0:
                top = min(top, int(cy) - 1)
            top = max(y0, top)
            xa = min(piece[0][0], piece[-1][0])
            w, h = len(piece), bot - top
            if h > 0:
                name = "ar_b%s%d_%d_%d_%d_%d_%d" % (side, k, w, h, run, b - T, xs % 1024)

                def paint_it(piece=piece, xa=xa, top=top, w=w, h=h, k=k):
                    out = self._ar_band_px(piece, cusps, xa, top, w, h)
                    if k == 0:
                        self._ar_spring_px(out, lt, xs, vx, R, cy, b, xa, top, w, h)
                    return out
                self.paint(eg, name, xa, top, w, h, paint_it)
            at = end
            k += 1

    def _ar_cusps(self, xs, lt, run, span):
        """(x centre, half length along x, height) of the cusps on the world's side."""
        out = []
        scale = min(1.0, run / 140.0)
        for u_, hh in ((0.30, 6.0), (0.52, 8.0), (0.74, 6.0)):
            s_ = span * 6.0 * u_ * (1.0 - u_) / run
            c_ = 1.0 / math.sqrt(1.0 + s_ * s_)
            out.append((xs + (u_ * run if lt else -u_ * run), 20.0 * scale * c_, hh * scale))
        return out

    def _ar_band_px(self, piece, cusps, xa, top, w, h):
        out = [0] * (w * h)
        S, G = self._ar_S, self._ar_G
        s0, s1, s2, s3, s4, s5 = S
        g0, g3 = G[0], G[3]
        hol = Wyrm.AR_HOLLOW
        for q in piece:
            x, ye, c, nx, lit = q
            col = x - xa
            bead = self._ar_gold(self._ar_lit(lit))
            arris = ((s3[0] + s4[0]) // 2, (s3[1] + s4[1]) // 2, (s3[2] + s4[2]) // 2) if lit < 0.45 else (s4 if lit < 0.9 else s5)
            B = (g0, bead, g3, s3, s0, hol, hol, hol, s0, arris)
            sa = 0.25 + 0.25 * max(0.0, lit)
            near_c = None
            for u_ in cusps:
                if abs(x + 0.5 + 4.0 * nx - u_[0]) < u_[1] + 4.0:
                    near_c = u_
            dlow = -11.0 if near_c is not None else -2.5
            first = int(ye - 10.8 / c) - top
            first = 0 if first < 0 else first
            for yi in range(first, h):
                d = (ye - (top + yi + 0.5)) * c
                if d < dlow:
                    break
                p = yi * w + col
                if near_c is not None and d < 0.5:
                    t = (x + 0.5 - d * nx - near_c[0]) / near_c[1]
                    if -1 < t < 1:
                        e = 1.0 - (t if t > 0 else -t)
                        dw = -near_c[2] * e * e      # the cusp's edge, as a distance
                        if d > dw - 0.5:
                            cv = d - dw + 0.5
                            cv = 1.0 if cv > 1 else cv
                            base = s2 if d - dw > 1.2 else (s4 if lit < 0.5 else s1)
                            if d > 0:
                                v = d * 2.0
                                base = (base[0] + (g0[0] - base[0]) * v, base[1] + (g0[1] - base[1]) * v,
                                        base[2] + (g0[2] - base[2]) * v)
                            out[p] = Wyrm.px(base[0], base[1], base[2], int(255 * cv))
                            continue
                        if d > dw - 3.0:
                            al = sa * (1.0 - (dw - 0.5 - d) / 2.5)
                            out[p] = Wyrm.px(8, 8, 16, int(255 * al))
                            continue
                if d >= 0.5:
                    f = d - 0.5
                    i = int(f)
                    t = f - i
                    if i >= 10:
                        continue
                    if i == 9:                       # the arris fades into the slate below
                        out[p] = Wyrm.px(arris[0], arris[1], arris[2], int(255 * (1.0 - t)))
                        continue
                    pa, pb = B[i], B[i + 1]
                    out[p] = (int(pa[0] + (pb[0] - pa[0]) * t) | (int(pa[1] + (pb[1] - pa[1]) * t) << 8) |
                              (int(pa[2] + (pb[2] - pa[2]) * t) << 16) | (255 << 24))
                elif d >= -0.5:
                    cv = d + 0.5
                    rest = (1.0 - cv) * sa
                    out[p] = (int(g0[0] * cv + 8 * rest) | (int(g0[1] * cv + 8 * rest) << 8) |
                              (int(g0[2] * cv + 16 * rest) << 16) | (int((cv + rest) * 255) << 24))
                elif d > -2.5:
                    al = sa * (1.0 + (d + 0.5) / 2.0)
                    out[p] = Wyrm.px(8, 8, 16, int(255 * al * al / sa))
        return out

    def _ar_hood_col(self, o, rx, ry):
        """A pixel of the hood's bead: o across it, (rx, ry) the way out of its curve."""
        s0 = self._ar_S[0]
        col = self._ar_gold(3.1 + (-0.6 * rx - 0.8 * ry) * o * 1.1)
        ao = o if o > 0 else -o
        if ao > 1.0:
            t = ao - 1.0 if ao < 2.0 else 1.0
            col = (col[0] * (1 - t) + s0[0] * t, col[1] * (1 - t) + s0[1] * t, col[2] * (1 - t) + s0[2] * t)
        return col

    def _ar_spring_px(self, out, lt, xs, vx, R, cy, b, xa, top, w, h):
        """The hood springing into the moulding: a quarter circle, on top down to the bead."""
        by = b - 2.5
        for yi in range(max(0, int(cy) - top), min(h, int(by + 2) - top)):
            dy = top + yi + 0.5 - cy
            for cl in range(w):
                x = xa + cl + 0.5
                if (lt and x > xs) or (not lt and x < xs):
                    continue
                dx = x - xs
                r = math.sqrt(dx * dx + dy * dy)
                o = r - R
                if -2.5 < o < 2.5 and r > 0.01:
                    c = self._ar_hood_col(o, dx / r, dy / r)
                    out[yi * w + cl] = int(c[0]) | (int(c[1]) << 8) | (int(c[2]) << 16) | (255 << 24)

    def _ar_hood(self, eg, side, xs, x0, x1, y0, b):
        """The hood's straight run, down beside its window: one stretched line."""
        lt = side == "L"
        vx = (x0 + 2.0) if lt else (x1 - 2.0)
        cy = b - 2.5 - abs(xs - vx)
        n = int(cy) - y0
        if n <= 0:
            return
        xc = x0 if lt else x1 - 5
        rows = []
        for cl in range(5):
            o = (vx - (xc + cl + 0.5)) if lt else (xc + cl + 0.5 - vx)
            c = self._ar_hood_col(o, -1.0 if lt else 1.0, 0.0)
            rows.append(("#%02X%02X%02X" % (int(c[0]), int(c[1]), int(c[2])), 1.0))
        self._ar_strip(eg, False, xc, y0, n, rows)

    # ---------- the corner frame's rim: under, over and beyond its window, in the zone's margin ----------
    def _ar_rim(self, eg, geo, side, sh):
        bx0, bx1, b = sh
        gap = geo["gap"]
        ins = Kit.ZONE_INSET
        flat = geo["flat"]
        S, G = Wyrm.S, Wyrm.GILT
        yz = None
        for z in self.panels:
            if z[0] == bx0 and z[0] + z[2] == bx1 and z[1] + z[3] + gap == b:
                yz = z[1]
        yz = geo["y0"] if yz is None else yz
        lt = side == "L"
        xa = max(geo["kx"], bx0)
        xb = min(geo["kx"] + geo["kw"], bx1)
        if lt:                                       # the shoulder's picture takes over at the near side
            ra, rb = xa, xb - ins
        else:
            ra, rb = xa + ins, xb
        if flat:
            ra, rb = xa, xb
        if rb <= ra:
            return
        bb = b - 5
        self.box(eg, ra, bb - 2 - ins, rb - ra, 2 + ins, S[2])
        if not flat:
            self._ar_strip(eg, True, ra, bb, rb - ra, [(S[0], 1.0), (S[3], 1.0), (G[3], 1.0), (G[4], 1.0),
                                                       (G[0], 1.0), (S[0], 0.5), (S[0], 0.2)])
        # the top: the screen frame's own rows, running on from its neighbours
        ta = ra - ins if lt and ra - ins >= 0 else ra
        tb = rb + ins if not lt and rb + ins <= self.W else rb
        self._ar_strip(eg, True, ta, yz, tb - ta, [(S[4], 1.0), (G[4], 1.0), (G[1], 1.0), (S[0], 1.0)])
        # the far side (and in the flat form the near side too): the left of a bead is lit
        ft = yz + ins
        fh = bb - 2 - ins - ft
        if fh > 0:
            xs_ = [xa, xb - ins] if flat else [xa if lt else xb - ins]
            for fx in xs_:
                self._ar_strip(eg, False, fx, ft, fh, [(S[3], 1.0), (G[3], 1.0), (G[1], 1.0), (S[0], 1.0)])
        self._ar_boss(eg, geo, side, b)

    def _ar_boss(self, eg, geo, side, y):
        """The stone's boss where the moulding meets the game view's side border."""
        kx, kw = geo["kx"], geo["kw"]
        x = kx - 1 if side == "L" else kx + kw
        if (side == "L" and kx >= Kit.ZONE_INSET) or (side == "R" and kx + kw <= self.W - Kit.ZONE_INSET):
            if hasattr(self, "_st_cols"):            # the stone part got that far
                self._st_boss(self.tg if self.tg is not None else eg, x, y - 2)

    # ---------- the spandrel's blind tracery: one picture (it is symmetric, so the light holds) ----------
    def _ar_roundel(self, eg, geo, side, xs, b):
        lt = side == "L"
        T, y0, run, gap = geo["T"], geo["y0"], geo["run"], geo["gap"]
        span = float(b - T)
        s = span * 1.5 / run                         # the curve's slope at its middle
        c = 1.0 / math.sqrt(1.0 + s * s)
        ax = -gap + 7.0                              # the left edge of the room, x from xs
        ay = y0 + 8.0                                # its top
        # a circle touching those two and clear of the crockets on the curve's middle
        rr = ((run * 0.5 - ax) * s * c + (b - span * 0.5 - ay) * c - 21.0) / (1.0 + s * c + c)
        r = min(44, int(rr))
        if r < 12:
            return
        d = 2 * r + 2
        cxr = ax + r
        px_ = xs + cxr - r - 1 if lt else xs - cxr - r - 1

        def paint_it():
            return self._ar_roundel_px(r, d)
        self.paint(eg, "ar_round_%d" % d, px_, ay - 1, d, d, paint_it)

    def _ar_roundel_px(self, r, d):
        """Ribs against dark hollows: a ring and a quatrefoil. A soft mask from one quadrant, then
        an emboss with the top-left light: S0-S3 only."""
        q = d // 2
        rc = r * 0.46
        off = r * 0.44
        rin = r - 3.0
        m = [-1.0] * (d * d)
        for yy in range(q):
            dy = yy + 0.5
            for xx in range(q):
                dx = xx + 0.5
                rad = math.sqrt(dx * dx + dy * dy)
                if rad > r + 0.5:
                    continue
                if rad > rin:
                    v = 1.0 if rad < r - 0.5 else r + 0.5 - rad
                else:
                    e1 = math.sqrt((dx - off) * (dx - off) + dy * dy) - rc
                    e2 = math.sqrt(dx * dx + (dy - off) * (dy - off)) - rc
                    e = e1 if e1 < e2 else e2
                    v = 1.0 - abs(e) / 1.2           # a rib along each foil's edge
                    v = 0.0 if v < 0 else v
                    if rin - rad < 1.0:
                        v = max(v, 1.0 - (rin - rad))
                m[(q - 1 - yy) * d + (q - 1 - xx)] = v
                m[(q - 1 - yy) * d + (q + xx)] = v
                m[(q + yy) * d + (q - 1 - xx)] = v
                m[(q + yy) * d + (q + xx)] = v
        out = [0] * (d * d)
        hi, lo = self._ar_S[3], self._ar_S[0]
        for y in range(1, d - 1):
            row = y * d
            for x in range(1, d - 1):
                p = row + x
                v = m[p]
                if v < 0:
                    continue
                a0, a1 = m[p - d - 1], m[p + d + 1]
                a0 = 0.0 if a0 < 0 else a0
                a1 = 0.0 if a1 < 0 else a1
                e = a1 - a0                          # a rib's lit edge faces up left
                if e > 0.05:
                    out[p] = Wyrm.px(hi[0] + 24, hi[1] + 24, hi[2] + 24, int(255 * min(0.8, e * 0.7)))
                elif e < -0.05:
                    out[p] = Wyrm.px(lo[0], lo[1], lo[2], int(255 * min(0.85, 0.2 - e * 0.7)))
                elif v < 0.5:
                    out[p] = Wyrm.px(lo[0], lo[1], lo[2], 75)
        return out

    # ---------- the crown ----------
    def _ar_crown(self, eg, geo):
        S, G = Wyrm.S, Wyrm.GILT
        T, y0, xl, xr = geo["T"], geo["y0"], geo["xl"], geo["xr"]
        w = xr - xl
        if w <= 0:
            return
        sa, sb = geo["sa"], geo["sb"]
        hs = T - y0
        hol = "#%02X%02X%02X" % Wyrm.AR_HOLLOW
        rows = []
        if hs >= 16 and sb > sa:                     # the outer order, as on the curve
            rows = [(S[4], 1.0), (S[0], 1.0), (hol, 1.0), (hol, 1.0), (hol, 1.0)]
        low = [(S[0], 1.0), (S[3], 1.0), (G[3], 1.0), (G[4], 1.0), (G[0], 1.0), (S[0], 0.5), (S[0], 0.2)]
        if rows:
            self._ar_strip(eg, True, sa, T - 10, sb - sa, rows + low)
        else:
            self._ar_strip(eg, True, xl, T - 5, w, low)
        self._ar_glints(eg, geo)
        if w >= 90:
            self._ar_key(eg, geo)

    def _ar_glints(self, eg, geo):
        """Short highlights on the bead, irregular, mirrored about the crown's centre."""
        xl, xr, T = geo["xl"], geo["xr"], geo["T"]
        cx2 = xl + xr
        at = 150
        for n in (3, 5):
            if cx2 // 2 - at - 60 < xl:
                break
            col = Wyrm.GILT[5]
            self.box(eg, cx2 // 2 - at - n, T - 2, n, 1, col)
            self.box(eg, (cx2 + 1) // 2 + at, T - 2, n, 1, col)
            at += 41 + (n * 13) % 47

    def _ar_key(self, eg, geo):
        T, xl, xr = geo["T"], geo["xl"], geo["xr"]
        y0 = max(geo["y0"], T - 20)                  # the same size at any resolution
        w = xr - xl
        hs = T - y0
        ghalf = 0
        if hs >= 16 and not geo["flat"]:
            ghalf = (min(104, (w // 2 - 30) // 2) // 16) * 16    # the guilloche beside the keystone
        cx2 = xl + xr                                # twice the centre: mirrored to the pixel
        ci = cx2 // 2
        odd = cx2 & 1
        if ghalf:
            for sgn in (-1, 1):
                gw = ghalf + 3
                gx = ci + odd + 18 if sgn > 0 else ci - 18 - gw

                def paint_g(sgn=sgn, gw=gw):
                    return self._ar_guil_px(sgn, gw, hs, ghalf)
                self.paint(eg, "ar_g%d_%d_%d" % (sgn, gw, hs), gx, y0, gw, hs, paint_g)
        half = 26
        W_ = 2 * half + odd
        h = hs + 14

        def paint_it():
            return self._ar_key_px(W_, h, half + odd / 2.0, hs)
        self.paint(eg, "ar_key_%d_%d" % (W_, h), ci - half, y0, W_, h, paint_it)

    def _ar_guil_px(self, sgn, gw, hs, ghalf):
        """One side of the guilloche with its clasp, and the voussoirs' radial joints over it. The
        keystone's side is at column 0 on the right, the last column on the left."""
        out = [0] * (gw * hs)
        T = hs
        G = self._ar_G
        vb = T - 10
        d = 25.0
        for n in range(8):
            if d > gw + 16:
                break
            for yy in range(1, vb):
                off = int(d + (T - yy) * d / 150.0) - 18
                xx = off if sgn > 0 else gw - 1 - off
                if 0 <= xx < gw - 1:
                    out[yy * gw + xx] = Wyrm.px(8, 8, 16, 210)
                    out[yy * gw + xx + 1] = Wyrm.px(88, 80, 72, 90)
            d += 26.0 + (n % 3) * 2.0
        per = self._ar_guil_period()
        gy = T - 9
        for i in range(ghalf):
            xx = i if sgn > 0 else gw - 1 - i
            pc = i % 16
            for r in range(8):
                out[(gy + r) * gw + xx] = per[r * 16 + pc]
        ex = ghalf if sgn > 0 else 0
        for r in range(-1, 8):
            for k, gl in ((0, 4), (1, 3), (2, 1)):
                c = G[gl]
                out[(gy + r) * gw + ex + k] = Wyrm.px(c[0], c[1], c[2])
        return out

    def _ar_key_px(self, W_, h, cx, hs):
        out = [0] * (W_ * h)
        T = hs                                       # rows here: the crown line is row hs
        S = self._ar_S
        # the keystone
        ht, hb = 22.0, 15.0
        ktop = 1 if hs >= 16 else 0
        kbot = T + 10
        kh = float(kbot - ktop)
        cy = (T - 6) + 0.5
        for yy in range(ktop, min(h, kbot + 3)):
            y = yy + 0.5
            hw = ht + (hb - ht) * (y - ktop) / kh
            row = yy * W_
            for xx in range(0, W_):
                px = xx + 0.5 - cx
                ax = -px if px < 0 else px
                bot = kbot - ax / 5.0
                es, eb, et = hw - ax, bot - y, y - ktop
                e = min(es, eb, et)
                if e <= -0.5:                        # its shadow, down and right
                    ax2 = abs(px - 2.0)
                    y2 = y - 2.0
                    hw2 = ht + (hb - ht) * (y2 - ktop) / kh
                    if min(hw2 - ax2, kbot - ax2 / 5.0 - y2, y2 - ktop) > 0:
                        out[row + xx] = Wyrm.px(8, 8, 16, 120)
                    continue
                if e < 0.5:
                    c = S[0]
                    out[row + xx] = Wyrm.px(c[0], c[1], c[2], int(255 * (e + 0.5)))
                    continue
                if e < 3.0:                          # the chamfer, by which face it is
                    if e == et:
                        c = S[5]
                    elif e == eb:
                        c = S[1]
                    else:
                        c = S[4] if px < 0 else S[1]
                    out[row + xx] = Wyrm.px(c[0], c[1], c[2])
                    continue
                out[row + xx] = self._ar_key_face(px, y, cy, kbot)
        return out

    def _ar_key_face(self, px, y, cy, kbot):
        """The keystone's carving: garnet in a gilt collar, a drop below, two leaves."""
        A = self._ar_A
        dy = y - cy
        rr = math.sqrt(px * px + dy * dy)
        if rr < 3.6:                                 # the cabochon
            if rr > 2.9:
                c = A[0]
            else:
                lit = (-px - dy) / 3.0
                c = A[1] if lit < -0.5 else (A[2] if lit < 0.2 else (A[3] if lit < 0.9 else A[4]))
            return Wyrm.px(c[0], c[1], c[2])
        if rr < 6.6:                                 # the collar
            c = self._ar_gold(3.7 + 1.6 * (-0.6 * px - 0.8 * dy) / rr)
            return Wyrm.px(c[0], c[1], c[2])
        if rr < 7.6:
            return Wyrm.px(8, 8, 16)
        ax = -px if px < 0 else px
        ex, ey = ax - 12.0, dy - 1.0
        rl = math.sqrt(ex * ex + ey * ey)
        if abs(rl - 4.5) < 1.0 and ey < 1.5:         # two leaves curling from the collar
            c = self._ar_gold(2.6 + (-0.6 * ex * (1 if px > 0 else -1) - 0.8 * ey) / (rl + 0.01))
            return Wyrm.px(c[0], c[1], c[2])
        yd = y - (kbot - 6.0)
        if ax + abs(yd) < 3.2:                       # the drop
            c = self._ar_gold(3.5 + 1.4 * (-0.6 * px - 0.8 * yd) / 3.0)
            return Wyrm.px(c[0], c[1], c[2])
        return Wyrm.px(24, 24, 32)

    def _ar_guil_period(self):
        """One 16 x 8 period of the two strands, painted once."""
        out = [0] * 128
        for yy in range(8):
            y = yy + 0.5
            for xx in range(16):
                x = xx + 0.5
                sn = math.sin(2.0 * math.pi * x / 16.0)
                cs = abs(math.cos(2.0 * math.pi * x / 16.0))
                nrm = 1.0 / math.sqrt(1.0 + 1.04 * cs * cs)
                da, db = (y - 4.0 - 2.6 * sn) * nrm, (y - 4.0 + 2.6 * sn) * nrm
                top, und = (da, db) if (xx < 4 or xx >= 12) else (db, da)
                if abs(top) < 1.5:
                    d = top
                elif abs(und) < 1.5 and abs(top) > 2.3:
                    d = und
                else:
                    out[yy * 16 + xx] = Wyrm.px(8, 8, 16)
                    continue
                c = self._ar_gold(3.5 - d)
                out[yy * 16 + xx] = Wyrm.px(c[0], c[1], c[2])
        return out

    # ---------- no painting: boxes, the curve in steps ----------
    def _ar_plain(self, eg, geo, left, right):
        S, G = Wyrm.S, Wyrm.GILT
        T, y0, run = geo["T"], geo["y0"], geo["run"]
        xl, xr = geo["xl"], geo["xr"]
        step = 20
        for side, sh in (("L", left), ("R", right)):
            if sh is None:
                continue
            self._ar_rim(eg, geo, side, sh)
            if geo["flat"]:
                continue
            bx0, bx1, b = sh
            lt = side == "L"
            xs = bx1 + geo["gap"] if lt else bx0 - geo["gap"]
            span = float(b - T)
            n = max(1, int(span // step))
            for i in range(n):
                ya = T + i * step
                yb = b if i == n - 1 else ya + step
                um = 1.0 - ((ya + yb) / 2.0 - T) / span
                t = Surround._ss_inv(max(0.0, min(1.0, um)))
                ex = int(xs + t * run) if lt else int(xs - t * run)
                if lt:
                    self.tile(eg, Wyrm.TILE, bx1, ya, max(0, ex - bx1), yb - ya)
                    self.box(eg, ex - 3, ya, 2, yb - ya, G[3])
                else:
                    self.tile(eg, Wyrm.TILE, ex, ya, max(0, bx0 - ex), yb - ya)
                    self.box(eg, ex + 1, ya, 2, yb - ya, G[2])
        sa, sb = geo["sa"], geo["sb"]
        if sb > sa and T - y0 > 5:
            self._ar_stone(eg, sa, y0, sb - sa, T - y0 - 5)
        if xr > xl:
            for i, col in enumerate((S[0], S[3], G[3], G[4], G[0])):
                self.box(eg, xl, T - 5 + i, xr - xl, 1, col)

    # ---------- the dragons: a parcel-gilt pair either side of the bar ----------
    # One figure from the client's right-hand pieces, mirrored for the left, lit from the left on both:
    # head, neck, then the lower piece's S round the pillar and its tail.
    _DR_W, _DR_H = 70, 150
    _DR_PIECES = ((10431, 6, 20, 11, 34), (10432, 0, 6, 48, 144), (10430, 10, 0, 0, 31))   # gump, x, row offset, rows a to b
    _DR_PILLAR = (10, 26)                                      # the pillar's columns
    _DR_CENTRE = 42                                            # pillar's middle to the bar's window
    _DR_PROFILE = (150, 188, 214, 226, 222, 210, 196, 182, 168, 154, 138, 122, 106, 90, 74, 56, 38)   # round, lit left
    _DR_JAW = (0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0)   # the head's lower edge over the pillar
    _DR_FOIL = ("...###...", "..#####..", "..#####..", ".#.###.#.", "#########",
                "####@####", "#########", ".#.###.#.", "..#####..")
    _DR_PAD = 3
    _DR_ROUND = 9                                              # the radius of the head's back
    _DR_PLINTH = 30
    _DR_FB = {-1: ((10421, 9, 20), (10420, 0, 0)), 1: ((10431, 6, 20), (10430, 10, 0))}   # the plain form
    _dr_src = None

    def draw_dragons(self, g, eg):
        for kind, z in self.zones:
            if kind not in ("w", "r"):
                continue
            r = self.sf.art_slot(z, self.W, self.H, self.zones)
            if tuple(r) == tuple(z):
                continue
            self._dr_stall(g, eg, z, r[0], r[0] + r[2], -1)
            self._dr_stall(g, eg, z, r[0], r[0] + r[2], 1)

    def _dr_stall(self, g, eg, z, inner_l, inner_r, side):
        """One bay: niche and plinth in the strip, the figure standing on it."""
        y, floor = int(z[1]), int(z[1] + z[3])
        sx = int(z[0]) if side < 0 else int(inner_r)
        sw = int(inner_l - z[0]) if side < 0 else int(z[0] + z[2] - inner_r)
        n = self._DR_PLINTH
        fw, fh = self._DR_W, self._DR_H
        cx = sx + sw - 1 - self._DR_CENTRE if side < 0 else sx + self._DR_CENTRE     # the pillar's middle
        mid = (self._DR_PILLAR[0] + self._DR_PILLAR[1]) // 2
        fx = cx - (fw - 1 - mid) if side < 0 else cx - mid
        top = floor - n
        fy = top - fh
        if floor - y < n + 40 or fx < sx - 1 or fx + fw > sx + sw + 1 or fy < 0:
            return                                      # no figure fits: nothing here
        for k, p in self.zones:
            if k in ("w", "r") and tuple(p) != tuple(z):
                if fx < p[0] + p[2] and p[0] < fx + fw and fy < p[1] + p[3] and p[1] < fy + fh:
                    return
        self._dr_plinth(g, sx, sw, cx, floor)
        self._dr_niche(g, sx, y, sw, top, cx)
        pad = self._DR_PAD
        pw, ph = fw + 2 * pad, fh + 2 * pad
        name = "dragon_%d_%dx%d" % (side + 1, pw, ph)
        if not self.paint(eg, name, fx - pad, fy - pad, pw, ph, lambda: self._dr_figure(side, pw, ph)):
            ox0 = cx - (51 if side < 0 else 18)
            for gid, ox, oy in self._DR_FB[side]:
                self.pic(eg, gid, ox0 + ox, fy + oy - 4)

    def _dr_ramp(self, stops):
        """Lookup by lum // 8: stops (lum, "#col"), interpolated, in steps of 8."""
        out = []
        i = 0
        rgb = [(s[0], self.rgb(s[1])) for s in stops]
        for n in range(48):
            v = n * 8
            while i < len(rgb) - 2 and v > rgb[i + 1][0]:
                i += 1
            a, ca = rgb[i]
            b, cb = rgb[i + 1]
            t = max(0.0, min(1.0, (v - a) / float(b - a)))
            c = [min(248, (int(ca[k] + (cb[k] - ca[k]) * t) + 4) // 8 * 8) for k in (0, 1, 2)]
            out.append(self.px(c[0], c[1], c[2]))
        return out

    def _dr_source(self):
        """The figure once for both sides: rows of luminance (-1 empty), of source (1 neck, 2 body,
        3 head, 4 eye) and of gold (the masses laid with leaf)."""
        if Wyrm._dr_src is not None:
            return Wyrm._dr_src
        fw, fh = self._DR_W, self._DR_H
        lum = [[-1] * fw for _ in range(fh)]
        src = [[0] * fw for _ in range(fh)]
        gold = [[False] * fw for _ in range(fh)]
        order = 0
        neck = None
        for gid, ox, oy, a, b in self._DR_PIECES:
            order += 1
            d = self.gump(gid)
            if d is None:
                continue
            pix, w, h = d
            if order == 1:
                neck = d
            for yy in range(a, min(b, h)):
                row, srow = lum[yy + oy], src[yy + oy]
                i = yy * w
                for xx in range(w):
                    v = int(pix[i + xx])
                    if v >> 24 and xx + ox < fw:
                        r, gg, bb = v & 255, (v >> 8) & 255, (v >> 16) & 255
                        row[xx + ox] = (r * 3 + gg * 6 + bb) // 10
                        srow[xx + ox] = 4 if gg > r + 24 and gg > bb + 8 else order
        pl, pr = self._DR_PILLAR
        # the jaw lies over the pillar: its flat lower edge cut to a curve, the pillar showing under it
        for x in range(pl, pr + 1):
            for y in range(31 - self._DR_JAW[x - pl], 31):
                lum[y][x] = -1
                src[y][x] = 0
                if neck is not None:
                    v = int(neck[0][(y - 20) * neck[1] + x - 6])
                    if v >> 24:
                        lum[y][x] = v & 255
                        src[y][x] = 1
        # the body over the pillar, where the S crosses it: all else in those columns is pillar
        for y in range(31, self._DR_H):
            if y < 56 or y >= 112:
                a, b = pr + 1, pr
            elif y < 64:
                a, b = pl + 2 * (64 - y), pr
            elif y < 98:
                a, b = pl, pr
            else:
                a, b = pl + (y - 98) * 8 // 7, pr
            for x in range(pl, pr + 1):
                if src[y][x] in (1, 2):
                    src[y][x] = 2 if a <= x <= b else 5
        # the tail curls away behind the pillar's foot
        for y in range(fh - 14, fh):
            for x in range(pr + (fh - y) * (fh - y) // 8 + 1, fw):
                lum[y][x] = -1
                src[y][x] = 0
        # the head's back rounds over on the column, not sawn off
        rnd = self._DR_ROUND
        t = 0
        while t < 31 and src[t][pl + rnd] != 3:
            t += 1
        for y in range(t, min(31, t + rnd)):
            dy = t + rnd - y
            inset = rnd - int((rnd * rnd - dy * dy) ** 0.5)
            for x in range(pl, pl + inset):
                if src[y][x] == 3:
                    lum[y][x] = -1
                    src[y][x] = 0
        # the crest: a band along the head's top, the horn whole
        for x in range(10, fw):
            t = None
            for y in range(31):
                if src[y][x] == 3:
                    if t is None:
                        t = y
                    if y - t < (2 if x < 60 else min(12, 2 + (x - 60) * 2)):
                        gold[y][x] = True
        # the forefeet whole
        for y in range(70, 104):
            for x in range(28, 50):
                if lum[y][x] >= 40 and src[y][x] == 2:
                    gold[y][x] = True
        # the spine: along the back where it is the outline, round the bulge then down the tail
        for y in range(38, fh):
            r = lum[y]
            filled = [x for x in range(fw) if r[x] >= 0]
            if not filled:
                continue
            if 62 <= y < 96:
                gold[y][filled[0]] = True
                if filled[0] + 1 < fw and r[filled[0] + 1] >= 0:
                    gold[y][filled[0] + 1] = True
            elif y >= 102 or y < 58:
                gold[y][filled[-1]] = True
                if r[filled[-1] - 1] >= 0:
                    gold[y][filled[-1] - 1] = True
        result = (lum, src, gold)
        if neck is not None:
            Wyrm._dr_src = result
        return result

    def _dr_figure(self, side, pw, ph):
        """The client's figure regraded: bright carved stone, gold leaf on whole masses, garnet eye."""
        S, G_, A = Wyrm.S, Wyrm.GILT, Wyrm.GARNET
        pad = self._DR_PAD
        px = self.px
        stone = self._dr_ramp(((0, S[0]), (24, S[2]), (48, S[3]), (72, S[5]), (100, "#786858"), (130, "#988870"),
                               (165, "#B8A888"), (205, "#D0C0A0"), (320, "#E8D8B8")))
        pillar = self._dr_ramp(((0, S[0]), (40, S[2]), (72, S[4]), (104, S[5]), (140, "#807060"), (176, "#A09080"),
                                (210, "#C0B098"), (250, "#D0C0A8"), (384, "#E0D0B8")))
        gilt = self._dr_ramp(((0, G_[2]), (40, G_[3]), (80, G_[4]), (140, G_[5]), (384, G_[5])))
        garnet = self._dr_ramp(((0, A[1]), (56, A[2]), (100, A[3]), (150, A[4]), (384, A[4])))
        rr, rg, rb = self.rgb(G_[6])
        glint = px(rr, rg, rb)
        lum0, src0, gold0 = self._dr_source()
        fw, fh = self._DR_W, self._DR_H
        pl, pr = self._DR_PILLAR
        if side < 0:
            lum0 = [r[::-1] for r in lum0]
            src0 = [r[::-1] for r in src0]
            gold0 = [r[::-1] for r in gold0]
            pl, pr = fw - 1 - pr, fw - 1 - pl
        prof = self._DR_PROFILE
        mean = {}
        for x in range(pl, pr + 1):
            vals = [lum0[y][x] for y in range(31, self._DR_H) if src0[y][x] == 5]
            mean[x] = sum(vals) // len(vals) if vals else 100
        masks, ends = [], []
        for row in lum0:
            m = 0
            filled = [x for x in range(fw) if row[x] >= 0]
            for x in filled:
                m |= 1 << x
            masks.append(m)
            ends.append((max(0, filled[0] - 3), min(fw, filled[-1] + 4)) if filled else (fw, fw))
        out = [0] * (pw * ph)
        shadow = px(8, 8, 16, 128)
        s0 = px(8, 8, 16)
        cadj = [int((fw / 2 - x) * 0.4) for x in range(fw)]
        for y in range(fh):
            m = masks[y]
            up = masks[y - 1] if y else 0
            dn = masks[y + 1] if y + 1 < fh else 0
            u2 = masks[y - 2] if y > 1 else 0
            if not (m | up | u2 | dn):
                continue
            row = lum0[y]
            srow = src0[y]
            contour = ((m << 1) | (m >> 1) | up | dn) & ~m
            cast = ((up << 1) | (u2 << 2) | (u2 << 1) | (up << 2)) & ~m & ~contour
            base = (y + pad) * pw + pad
            radj = int((fh * 0.35 - y) * 0.15)
            hsh = (36 - y) * 8 if 28 <= y < 36 else 0   # the head's contact shadow on the pillar
            foot = (y - (self._DR_H - 7)) * 7 if y > self._DR_H - 7 else 0
            gr = gold0[y]
            gu = gold0[y - 1] if y else gr
            lo = min(ends[y][0], ends[y - 1][0] if y else fw, ends[y - 2][0] if y > 1 else fw)
            hi = max(ends[y][1], ends[y - 1][1] if y else 0, ends[y - 2][1] if y > 1 else 0)
            for x in range(lo, hi):
                v = row[x]
                if v < 0:
                    if (contour >> x) & 1:
                        out[base + x] = s0
                    elif (cast >> x) & 1:
                        out[base + x] = shadow
                    continue
                s = srow[x]
                if s == 4:
                    out[base + x] = garnet[v >> 3]
                    continue
                if s == 5:
                    pv = prof[x - pl] + (v - mean[x]) - hsh - foot
                    out[base + x] = pillar[pv >> 3 if pv > 0 else 0]
                    continue
                vv = v + cadj[x] + radj + 8
                if vv < 0:
                    vv = 0
                if gr[x]:
                    if not gu[x] and not gr[x - 1] and vv > 90:   # the top left of a mass catches the light
                        out[base + x] = glint
                    else:
                        out[base + x] = gilt[vv >> 3]
                else:
                    out[base + x] = stone[vv >> 3]
        return out

    def _dr_niche(self, g, x, y, w, top, cx):
        """The shrine behind the statue, centred on its pillar: dark as the screen gets, under a gilt trefoil."""
        h = top - y
        S = Wyrm.S
        half = min(cx - x, x + w - 1 - cx)
        self.box(g, x, y, w, 2, Wyrm.GILT[3])           # the bar's top moulding runs in, at its rows
        self.box(g, x, y + 2, w, 1, S[3])
        self.box(g, x, y + 3, w, 1, S[0])
        self.box(g, x, y + 4, w, h - 4, S[2])
        if h < 24 or half < 20 or not self.paint(g, "niche_%d_%d" % (half, h), cx - half, y + 5, 2 * half + 1, h - 5,
                                                 lambda: self._dr_niche_px(half, h - 5)):
            self.box(g, cx - half + 3, y + 8, 2 * half - 5, h - 8, S[0])

    def _dr_niche_px(self, half, h):
        """Symmetrical and half computed: lit from above, so one picture serves both sides."""
        S, G_ = Wyrm.S, Wyrm.GILT
        c = {}
        for n, v in (("s1", S[1]), ("s2", S[2]), ("g1", G_[1]), ("g3", G_[3]), ("g4", G_[4]), ("g5", G_[5])):
            r, gg, b = self.rgb(v)
            c[n] = self.px(r, gg, b)
        void = self.px(0, 0, 8)
        lob = half * 0.56
        spring = int(lob * 1.55) + 2
        lobes = ((half - 2.5 - lob, spring, lob), (0.0, spring - lob * 0.72, lob))   # from the middle out
        edge = half - 3                                 # the opening's half width
        out = []
        cache = {}
        for y in range(h):
            if y >= spring:
                key = y % 12
                row = cache.get(key)
                if row is None:
                    half_row = []
                    for dx in range(half + 1):
                        d = edge - dx
                        if d < 0:
                            half_row.append(c["s2"] if d < -1 else c["s1"])
                        elif d < 2:
                            half_row.append(c["g4"] if d == 0 else c["g3"])
                        elif d < 3:
                            half_row.append(c["g1"])
                        elif dx > half * 0.5 and d >= 6 and ((dx + y) % 12 == 0 or (dx - y) % 12 == 0):
                            half_row.append(c["s1"])
                        else:
                            half_row.append(void)
                    row = half_row[:0:-1] + half_row
                    cache[key] = row
                out += row
                continue
            half_row = []
            for dx in range(half + 1):
                best = -99.0
                ny = 0.0
                for lx, ly, lr in lobes:
                    ax, ay = dx - lx, y - ly
                    dist = (ax * ax + ay * ay) ** 0.5
                    if lr - dist > best:
                        best = lr - dist
                        ny = ay / (dist + 0.01)
                if best < -1.0:
                    half_row.append(c["s2"])
                elif best < 0.0:
                    half_row.append(c["s1"])
                elif best < 2.0:
                    half_row.append(c["g5"] if ny < -0.75 else c["g4"] if ny < -0.3 else c["g3"])
                elif best < 3.0:
                    half_row.append(c["g1"])
                else:
                    half_row.append(void)
            out += half_row[:0:-1] + half_row
        return out

    def _dr_plinth(self, g, x, w, cx, floor):
        """Stepped base, a narrow die with a large foil, a heavy cap: on the screen's edge, under the pillar."""
        S, G_ = Wyrm.S, Wyrm.GILT
        n = self._DR_PLINTH
        top = floor - n
        self.box(g, x, top, w, n, S[1])                 # what's behind it
        cap, die = 34, 25                               # half widths

        def row(yy, hh, half, col):
            a = max(x, cx - half)
            b = min(x + w, cx + half + 1)
            self.box(g, a, yy, b - a, hh, col)
        # the cap, top down
        row(top, 1, cap, "#A09080")
        row(top + 1, 2, cap, "#786858")
        row(top + 3, 1, cap, G_[4])
        row(top + 4, 1, cap - 1, G_[2])
        row(top + 5, 1, cap - 3, S[0])
        # the die
        dy, dh = top + 6, n - 16
        row(dy, dh, die, S[5])
        self.box(g, cx - die, dy, 2, dh, "#887860")
        self.box(g, cx + die - 1, dy, 2, dh, S[2])
        self.box(g, cx - die, dy, 2 * die + 1, 2, S[0])
        # the base, a torus stepping out, ending in the screen frame's rows
        by = dy + dh
        row(by, 1, die + 4, S[0])
        row(by + 1, 1, die + 6, "#887860")
        row(by + 2, 1, die + 10, "#685848")
        row(by + 3, 2, w, S[5])
        row(by + 5, 1, w, S[0])
        self.box(g, x, floor - 4, w, 1, S[4])
        self.box(g, x, floor - 3, w, 1, G_[4])
        self.box(g, x, floor - 2, w, 1, G_[1])
        self.box(g, x, floor - 1, w, 1, S[0])
        px_, py, pw_, ph_ = cx - die + 5, dy + 3, 2 * die - 9, dh - 5    # the panel sunk in the die
        if ph_ >= 5:
            self.box(g, px_, py, pw_, ph_, S[3])
            self.box(g, px_, py, pw_, 1, S[0])          # shadow under its top edge and left
            self.box(g, px_, py, 1, ph_, S[0])
            self.box(g, px_ + 1, py + ph_ - 1, pw_ - 1, 1, "#887860")   # light on its lower and right edges
            self.box(g, px_ + pw_ - 1, py + 1, 1, ph_ - 1, "#887860")
            if ph_ >= 9:
                q = len(self._DR_FOIL)
                self.paint(g, "dr_foil_%d" % q, cx - q // 2, py + (ph_ - q) // 2, q, q, self._dr_quatrefoil)

    def _dr_quatrefoil(self):
        """A small gilt quatrefoil from its pattern, lit from the upper left, with a dark dimple."""
        G_, S = Wyrm.GILT, Wyrm.S
        cols = []
        for v in (G_[2], G_[3], G_[4], G_[5]):
            r, gg, b = self.rgb(v)
            cols.append(self.px(r, gg, b))
        r, gg, b = self.rgb(S[0])
        dark = self.px(r, gg, b)
        out = []
        n = len(self._DR_FOIL)
        for y in range(n):
            line = self._DR_FOIL[y]
            for x in range(n):
                ch = line[x]
                if ch == ".":
                    out.append(0)
                elif ch == "@":
                    out.append(dark)
                else:
                    out.append(cols[max(0, min(3, 3 - (x + y) * 4 // (2 * n)))])
        return out



class Surround(object):
    """(2.6.70) One frame (Settings > Layout, "Join zone windows in one frame";
    off unless ticked): the old client's look of a UI round a window into the
    game world. With a frame layout in use, a backdrop under every window
    covers each window and reserved zone with stone, as one surround: no
    border where two zones touch, the stone border only on its outer edges
    (the screen's and the game area's); a gold border runs round the edge of
    the game area (every keep-clear zone). The windows sitting in zones drop
    their own stone frames and corner knots, so their sections sit in the one
    surround; a window that leaves its zone (or the box unticked) gets its own
    frame back at once. Nothing else about a window changes, and with the box
    unticked nothing is drawn at all. The backdrop never takes the mouse and
    is drawn under every window (as the GRID is). Client thread (the keeper)."""
    GOLD_DARK = "#8C6A1E"       # the gold border round the game area: outer band
    GOLD_LIGHT = "#E8C15A"      # its inner line
    GOLD_W = 3                  # px of the outer band
    TOUCH = 3                   # zones this close count as touching (no border between)
    # (2.6.85) the art of the surround, client gump art only, drawn once per layout change.
    # (2.6.86) A layout whose windows fill their zones has no gaps, only the seams between
    # panels, so a look is what shows there. "plain": stone. "carved": the surround in dark
    # marble (ART_TILE; the black sections let it through too) with a gold line (ART_LINE,
    # hued) down every seam, and in any gap of ART_MIN_GAP or more a dark panel with gold rods
    # (ART_ROD), a carved piece and knots. "dragons": carved, with the client's dragon columns
    # standing in the game area's bottom corners (they never take the mouse).
    ART_LOOKS = ("plain", "carved", "dragons")   # (2.6.87) carved and dragons: class Wyrm

    def __init__(self):
        self.g = None
        # (2.6.73) the gold border and the arch's shoulders, in a window of their own
        # above the game view (2.6.72's arch_g held the shoulders only)
        self.edge_g = None
        self.sig = None             # what the backdrop was drawn for
        self.bare = {}              # window -> its frame controls hidden now
        self._bands = None          # (top, left, right, bottom) px of the stone border band
        self._raw = None            # (2.6.73) the backdrop's client gump (Surround._pin)
        self._pin_off = False       # ...False for good when the client's list can't be reached
        self._tile = None           # (2.6.73) (pixels, w, h) of the stone tile, for the arch

    def bands(self):
        """(2.6.72) (top, left, right, bottom): how wide the stone border band
        is on each outer edge of the surround (the 9-piece's edge pieces)."""
        if self._bands is None or not all(self._bands):
            base = Kit.WINDOW_BG
            s = [Kit.pic_size(base + i) for i in (1, 3, 5, 7)]
            self._bands = (s[0][1] or 0, s[1][0] or 0, s[2][0] or 0, s[3][1] or 0)
        return self._bands

    def early(self, g):
        """(2.6.72) A window just made (G.AddGump) where a window in a zone sits,
        with one frame on: its stone frame is hidden before it is ever drawn
        (the keeper's pass used to show it for up to KEEP_EVERY s first)."""
        lay = LAYOUT
        if not lay.unified or not lay.assign or self.sig is None:
            return
        parts = Kit._frame_parts.get(g) if Kit._frame_parts else None
        if not parts:
            return
        r = Kit.rect(g)
        if r is None:
            return
        for key, s in lay.placed.items():
            if abs(s[0] - r[0]) <= 24 and abs(s[1] - r[1]) <= 24 and lay.zone_of(key) is not None:
                self._show_frame(g, False)
                self.bare[g] = parts
                return

    # ---------- the window frames ----------
    def _show_frame(self, g, show):
        parts = Kit._frame_parts.get(g) if Kit._frame_parts else None
        if not parts:
            return None
        if not show:
            Kit.pin_size(g)                      # (2.6.74) before anything is hidden
        for p in parts:
            try:
                p.IsVisible = show
            except Exception:
                pass
        return parts

    def frames(self, on, zoned):
        """Hide the stone frame of every window in `zoned` (a set) while `on`;
        give it back to every other one hidden before. Only changes are written."""
        bare = self.bare
        if on:
            for g in zoned:
                parts = Kit._frame_parts.get(g) if Kit._frame_parts else None
                if parts is not None and bare.get(g) is not parts:
                    self._show_frame(g, False)       # (a rebuilt window: its new frame)
                    bare[g] = parts
        for g in [g for g in bare if not on or g not in zoned]:
            parts = bare.pop(g)
            if Kit.is_open(g) and Kit._frame_parts.get(g) is parts:
                self._show_frame(g, True)

    # ---------- the backdrop ----------
    def sync(self, on, zs, W, H, zoned):
        """Every keeper pass: the backdrop for the zones in use (drawn again only
        when they change) and the windows' frames."""
        zones = []
        arches = ()
        if on and zs is not None and W > 0 and H > 0:
            zones = [(z.kind, tuple(z.px)) for z in zs.zones if z.px is not None]
            if not any(k in ("w", "r") for k, _ in zones):
                zones = []
            elif LAYOUT.arch:
                arches = tuple(self.arches(zs, W, H))
        sig = (W, H, tuple(zones), arches, LAYOUT.art) if zones else None
        if sig != self.sig:
            self.sig = sig
            old, self.g = self.g, None
            olde, self.edge_g = self.edge_g, None
            self._raw = None
            if sig is None:                        # (2.6.87) one frame off: the overlay goes too
                oldt, self.top_g = getattr(self, "top_g", None), None
                Kit.dispose(oldt)
            if sig is not None:
                try:
                    self.build(zones, W, H, arches)
                except Exception as ex:
                    HOST._tell("%s: the one frame couldn't be drawn: %s%s"
                               % (APP_NAME, ex, _error_where()))
            Kit.dispose(old)
            Kit.dispose(olde)
        self.frames(sig is not None, zoned)
        if self.g is not None:
            self._pin()

    def close(self):
        self.sig = None
        old, self.g = self.g, None
        olde, self.edge_g = self.edge_g, None
        self._raw = None
        Kit.dispose(old)
        Kit.dispose(olde)
        oldt, self.top_g = getattr(self, "top_g", None), None   # (2.6.87)
        Kit.dispose(oldt)
        Wyrm.made.clear()
        self.frames(False, set())
        try:
            Tex.drop([n for n in Tex.names if n.startswith(self.TEX) or n.startswith("va_wyrm_")])
        except Exception:
            pass

    # ---------- (2.6.73) the backdrop stays under everything ----------
    #  TazUO keeps "Under" windows just above the last window of its list, and its
    #  sort moves the first "Under" window it meets to that place on every pass
    #  after a window is added or brought to the front: two "Under" windows (this
    #  backdrop, the bag grid) swapped places on every click, and whichever was
    #  rebuilt last went under the other (the bags' black vanished under the
    #  stone). The sort never moves the list's very last window, so the backdrop
    #  is kept there: drawn first, under the game view too (the view draws only
    #  inside its own rect; the gold, which must show over the view's border, is
    #  in edge_g). Checked every keeper pass: one read when it is in place.
    def _pin(self):
        if self._pin_off:
            return
        try:
            raw = self._raw
            if raw is None or raw.IsDisposed:
                raw = self._raw = Kit._raw_gump(self.g)
                if raw is None:
                    return
            Typing._find()
            lst = Typing._get(None, "Gumps", Typing.uim) if Typing.uim is not None else None
            if lst is None:
                return
            try:
                self._pin_edge(lst)                # (2.6.87) its failing leaves the backdrop's pin
            except Exception:
                pass
            last = lst.Last
            if last is not None and Typing._same(last.Value, raw):
                return
            node = lst.Find(raw)
            if node is None:                       # not in the list yet (added next frame)
                return
            lst.Remove(node)
            lst.AddLast(node)
        except Exception:
            self._pin_off = True

    def _pin_edge(self, lst):
        """(2.6.87) The art's edge window just in front of the game view and behind every
        other window (the list runs front to back), so it never lies over a window."""
        if LAYOUT.art == "plain" or self.edge_g is None:
            return
        raw = getattr(self, "_edge_raw", None)
        if raw is None or raw.IsDisposed:
            raw = self._edge_raw = Kit._raw_gump(self.edge_g)
            if raw is None:
                return
        t, vp = LAYOUT._viewport()
        vn = lst.Find(vp) if vp is not None else None
        en = lst.Find(raw)
        if vn is None or en is None or vn.Previous is en:
            return
        lst.Remove(en)
        lst.AddBefore(vn, en)

    # ---------- (2.6.72) the arch ----------
    #  An arched keep-clear zone runs up to the crown; the hugging window zones in
    #  its top corners are its shoulders. The edge of the game view (the player's
    #  red line): flat a GAP under each corner block, a smoothstep S-curve rising
    #  over the run, flat across the crown, down the same way on the other side,
    #  mirrored to the pixel. (2.6.73) Each shoulder is one picture made in memory
    #  (Tex; no file): the stone tiled on from the crown strip and the gold
    #  anti-aliased along the curve. 2.6.72 drew stone rows ROW px high, each
    #  tiled from its own left edge, with the gold stepped along them: a jagged,
    #  blurred edge; that is kept only for a client that can't make the picture.
    #  In the edge window, above the game view. When the two curves would meet
    #  (a narrow screen), the top is flat at the lower block's bottom instead.
    ROW = 4

    @staticmethod
    def _ss(t):
        t = 0.0 if t < 0 else (1.0 if t > 1 else t)
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def _ss_inv(u):
        lo, hi = 0.0, 1.0
        for _ in range(14):
            mid = (lo + hi) / 2.0
            if Surround._ss(mid) < u:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2.0

    def arches(self, zs, W, H):
        """[(kx, ky, kw, kh, left, right, run, flat)] for every arched keep-clear
        zone: left = (block x0, x1, bottom + GAP) of the shoulder in its top-left
        (or None), right the same for its top-right; flat True when the top is
        flat (no room for the curves), the top then at the lower shoulder."""
        out = []
        G_ = Kit.GAP
        for z in zs.zones:
            if z.kind != "k" or not z.arch or z.px is None:
                continue
            kx, ky, kw, kh = z.px
            left = right = None
            sh = sorted([o.px for o in zs.zones if o.hug and o.px is not None
                         and not (o.px[0] + o.px[2] <= kx or o.px[0] >= kx + kw or o.px[1] > ky + 2)])
            # the leftmost and rightmost hugging zones over it are its shoulders (one
            # alone: the side of the screen's centre it is on)
            if len(sh) >= 2:
                left, right = sh[0], sh[-1]
            elif sh:
                if sh[0][0] + sh[0][2] / 2.0 < W / 2.0:
                    left = sh[0]
                else:
                    right = sh[0]
            if left is not None:
                left = (left[0], left[0] + left[2], left[1] + left[3] + G_)
            if right is not None:
                right = (right[0], right[0] + right[2], right[1] + right[3] + G_)
            run = max(24, int(round(ARCH_RUN * H / 1080.0)))
            lx = left[1] + G_ if left else kx
            rx = right[0] - G_ if right else kx + kw
            flat = (left is None and right is None) or lx + run + 20 > rx - run
            out.append((kx, ky, kw, kh, left, right, run, flat))
        return out

    def arch_top(self, a):
        """The top of the game view under arch a (its crown, or the flat top)."""
        kx, ky, kw, kh, left, right, run, flat = a
        if not flat:
            return ky
        return max([ky] + [s[2] for s in (left, right) if s is not None])

    TEX = "va_arch_"                     # (2.6.73) names of the arch's pictures
    GOLD_RGB = ((140, 106, 30), (232, 193, 90))   # GOLD_DARK, GOLD_LIGHT

    def _stone_tile(self):
        """(pixels, w, h) of the stone tile (the 9-piece's centre), cached."""
        if self._tile is None:
            got = Tex.gump_pixels(Kit.WINDOW_BG + 4)
            if got is None:
                raise Exception("no stone tile")
            self._tile = got
        return self._tile

    def _arch_pixels(self, a, side, W):
        """(2.6.73) (x0, y0, w, h, pixels) of one shoulder of arch a as a picture:
        stone above and beside the S-curve (tiled from the crown strip's own
        origin, so it runs on from it), the gold along the curve (3 px dark, 1 px
        light on the game's side) anti-aliased by its distance to the curve, and
        nothing where the corner block's window sits or under the curve. Only the
        pixels within 5 px of the curve are worked out one by one; the stone is
        copied a column at a time."""
        kx, ky, kw, kh, left, right, run, flat = a
        sh = left if side == "L" else right
        bx0, bx1, b = sh
        G_ = Kit.GAP
        GT = self.GOLD_W + 1
        tile, tw, th = self._stone_tile()
        if side == "L":
            xs = bx1 + G_                        # the curve starts here (flat before it)
            outer = kx - GT if kx >= GT else kx  # the corner where the side gold meets it
            x0, x1 = outer, xs + run + 2
            edge_x = kx                          # left of it: outside the game area
        else:
            xs = bx0 - G_
            outer = kx + kw + GT if (kx + kw + GT) <= W else kx + kw
            x0, x1 = xs - run - 2, outer
            edge_x = kx + kw
        x0 = max(x0, kx - GT)
        y0, y1 = max(0, ky - GT), b
        w, h = x1 - x0, y1 - y0
        if w <= 0 or h <= 0:
            return None
        out = [0] * (w * h)
        span = float(b - ky)
        dk, lk = self.GOLD_RGB
        cols = {}                                # tile column -> the stone column for these rows

        def stone_col(cx):
            c = cols.get(cx)
            if c is None:
                c = cols[cx] = [tile[cx + (yy % th) * tw] for yy in range(y0, y1)]
            return c

        def cov(d, lo, hi):
            v = min(hi, d + 0.5) - max(lo, d - 0.5)
            return v if v > 0 else 0.0

        def mix(d, sp):
            cl, cd, cs = cov(d, 0.0, 1.0), cov(d, 1.0, 4.0), cov(d, 4.0, 1e9)
            al = cl + cd + cs
            if al <= 0.002:
                return 0
            r = cl * lk[0] + cd * dk[0] + cs * (sp & 0xFF)
            g_ = cl * lk[1] + cd * dk[1] + cs * ((sp >> 8) & 0xFF)
            bb = cl * lk[2] + cd * dk[2] + cs * ((sp >> 16) & 0xFF)
            return (int(r + 0.5) | (int(g_ + 0.5) << 8) | (int(bb + 0.5) << 16) |
                    (int(min(1.0, al) * 255 + 0.5) << 24))

        for x in range(x0, x1):
            col = x - x0
            cx = (x - kx) % tw
            u = (x + 0.5 - xs) / float(run) if side == "L" else (xs - (x + 0.5)) / float(run)
            if u <= 0:
                ye, c = float(b), 1.0
            elif u >= 1:
                ye, c = float(ky), 1.0
            else:
                ye = b - self._ss(u) * span
                slope = span * 6.0 * u * (1.0 - u) / run
                c = 1.0 / math.sqrt(1.0 + slope * slope)
            in_block = (x < bx1) if side == "L" else (x >= bx0)
            outside = (x < edge_x) if side == "L" else (x >= edge_x)
            top = (b - G_) if (in_block or outside) else y0
            if top >= y1:
                continue
            dx = ((edge_x - (x + 0.5)) if side == "L" else ((x + 0.5) - edge_x)) if outside else -1e9
            # the rows of whole stone (the band is 4 px; its edge is worked out below)
            full_end = int(math.ceil(ye - 4.5 / c - 0.5)) if dx < 4.5 else y1
            full_end = max(top, min(y1, full_end))
            if full_end > top:
                sc = stone_col(cx)
                out[(top - y0) * w + col:(full_end - y0) * w + col:w] = sc[top - y0:full_end - y0]
            for y in range(full_end, y1):
                d = (ye - (y + 0.5)) * c
                if dx > d:
                    d = dx
                if d <= -0.5:
                    break
                out[(y - y0) * w + col] = mix(d, tile[cx + (y % th) * tw])
        return x0, y0, w, h, out

    def build_arch(self, a, gold, W, H, g):
        """The shoulders of arch a, drawn into g (the edge window, above the game
        view; the crown strip above them is in the backdrop); gold(...) draws the
        straight gold. (2.6.73) The curve is a picture made in memory (Tex) when
        the client allows it; else the 4 px stone rows with the gold stepped
        along them (2.6.72's look)."""
        kx, ky, kw, kh, left, right, run, flat = a
        base = Kit.WINDOW_BG
        R = self.ROW
        if flat:
            top = self.arch_top(a)
            # stone from the crown down to the flat top, beside / under the blocks
            if top > ky:
                for y0 in range(ky, top, R):
                    y1 = min(top, y0 + R)
                    xa, xb = kx, kx + kw
                    if left is not None and y0 < left[2] - Kit.GAP:
                        xa = left[1]
                    if right is not None and y0 < right[2] - Kit.GAP:
                        xb = right[0]
                    if xb > xa:
                        Kit.add_tiled(g, base + 4, xa, y0, xb - xa, y1 - y0)
            gold(g, kx, top - 4, kw, True)
            return
        smooth = False
        try:
            smooth = bool(Tex.find()) and Client.on_client_thread()
        except Exception:
            smooth = False
        for side in ("L", "R"):
            sh = left if side == "L" else right
            if sh is None or sh[2] <= ky:
                continue
            if smooth:
                try:
                    got = self._arch_pixels(a, side, W)
                    if got is not None:
                        x0, y0, w, h, px = got
                        name = self.TEX + side
                        Tex.put(name, w, h, px)
                        Tex.control(g, name, x0, y0, w, h)
                        continue
                except Exception:
                    smooth = False                   # the stair for this side and the next
            self._arch_stair(g, a, side)
        # the crown's own gold, between the two curves' tops
        xl = (left[1] + Kit.GAP + run) if left else kx
        xr = (right[0] - Kit.GAP - run) if right else kx + kw
        if xr > xl:
            gold(g, xl, ky - 4, xr - xl, True)

    def _arch_stair(self, g, a, side):
        """One shoulder as 4 px stone rows with the gold stepped along them."""
        kx, ky, kw, kh, left, right, run, flat = a
        base = Kit.WINDOW_BG
        R = self.ROW
        sh = left if side == "L" else right
        bx0, bx1, b = sh
        rows = []
        y0 = ky
        while y0 < b:
            y1 = min(b, y0 + R)
            u = float(b - (y0 + y1) / 2.0) / float(max(1, b - ky))
            t = self._ss_inv(max(0.0, min(1.0, u)))
            if side == "L":
                edge = int(round(bx1 + Kit.GAP + t * run))
            else:
                edge = int(round(bx0 - Kit.GAP - t * run))
            under = y0 >= b - Kit.GAP          # the strip under the block
            if side == "L":
                xa = kx if under else bx1
                if edge > xa:
                    Kit.add_tiled(g, base + 4, xa, y0, edge - xa, y1 - y0)
            else:
                xb = kx + kw if under else bx0
                if xb > edge:
                    Kit.add_tiled(g, base + 4, edge, y0, xb - edge, y1 - y0)
            rows.append((y0, y1, edge))
            y0 = y1
        for i, (r0, r1, edge) in enumerate(rows):
            nxt = rows[i + 1][2] if i + 1 < len(rows) else (kx if side == "L" else kx + kw)
            if side == "L":
                Kit.add_box(g, edge - 4, r0, 3, r1 - r0, 1.0, self.GOLD_DARK)
                Kit.add_box(g, edge - 1, r0, 1, r1 - r0, 1.0, self.GOLD_LIGHT)
                if nxt < edge:
                    Kit.add_box(g, nxt, r1 - 4, edge - nxt, 3, 1.0, self.GOLD_DARK)
                    Kit.add_box(g, nxt, r1 - 1, edge - nxt - 1, 1, 1.0, self.GOLD_LIGHT)
            else:
                Kit.add_box(g, edge + 1, r0, 3, r1 - r0, 1.0, self.GOLD_DARK)
                Kit.add_box(g, edge, r0, 1, r1 - r0, 1.0, self.GOLD_LIGHT)
                if nxt > edge:
                    Kit.add_box(g, edge, r1 - 4, nxt - edge, 3, 1.0, self.GOLD_DARK)
                    Kit.add_box(g, edge + 1, r1 - 1, nxt - edge - 1, 1, 1.0, self.GOLD_LIGHT)

    @staticmethod
    def _uncovered(lo, hi, cover):
        """The parts of [lo, hi) not inside any (a, b) of cover."""
        out, at = [], lo
        for a, b in sorted(cover):
            if b <= at or a >= hi:
                continue
            if a > at:
                out.append((at, a))
            at = max(at, b)
        if at < hi:
            out.append((at, hi))
        return out

    @staticmethod
    def _stone_rects(zones, W, H):
        """(2.6.75) [(x, y, w, h)]: the screen less the keep-clear zones (the game
        view: TazUO draws the world under every gump, so stone there hides it),
        where a window or reserved zone lying over a keep-clear zone (an arch's
        shoulders, an overlapping zone) stays stone. Cut in bands at every zone's
        top and bottom; a band the same across as the one above joins it, so the
        stone is a few tiled pieces."""
        holes = [(x, y, x + w, y + h) for k, (x, y, w, h) in zones
                 if k == "k" and w > 2 and h > 2]
        if not holes:
            return [(0, 0, W, H)]
        solid = [(x, y, x + w, y + h) for k, (x, y, w, h) in zones if k in ("w", "r")]
        ys = set([0, H])
        for r in holes + solid:
            for v in (r[1], r[3]):
                if 0 < v < H:
                    ys.add(v)
        ys = sorted(ys)
        out, run = [], {}                          # run: stone span -> top of its piece
        for i in range(len(ys) - 1):
            y0, y1 = ys[i], ys[i + 1]
            open_ = []
            hx = [(a[0], a[2]) for a in holes if a[1] <= y0 and a[3] >= y1]
            if hx:
                sx = [(a[0], a[2]) for a in solid if a[1] <= y0 and a[3] >= y1]
                for a, b in hx:
                    open_.extend(Surround._uncovered(a, b, sx))
            spans = Surround._uncovered(0, W, open_)
            now = {}
            for sp in spans:
                now[sp] = run.pop(sp, y0)          # carried on from the band above, or new
            for (a, b), top in run.items():        # spans that end here
                out.append((a, top, b - a, y0 - top))
            run = now
        for (a, b), top in run.items():
            out.append((a, top, b - a, H - top))
        return [r for r in out if r[2] > 0 and r[3] > 0]

    @staticmethod
    def _minus(rects, cut):
        """rects less the rect cut (x, y, w, h): what is left, as rects."""
        cx, cy, cw, ch = cut
        out = []
        for (x, y, w, h) in rects:
            if cx >= x + w or x >= cx + cw or cy >= y + h or y >= cy + ch:
                out.append((x, y, w, h))
                continue
            if cy > y:
                out.append((x, y, w, cy - y))
            if cy + ch < y + h:
                out.append((x, cy + ch, w, y + h - cy - ch))
            my0, my1 = max(y, cy), min(y + h, cy + ch)
            if cx > x:
                out.append((x, my0, cx - x, my1 - my0))
            if cx + cw < x + w:
                out.append((cx + cw, my0, x + w - cx - cw, my1 - my0))
        return out

    def _finish_gump(self, g, under):
        """A backdrop or edge window: no mouse, no right-click close, never moved or kept."""
        g.SetRect(0, 0, self._size[0], self._size[1])
        safe(lambda: g.SetAcceptMouseInput(False))
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        safe(lambda: setattr(g, "CanMove", False))
        if under:
            try:                                   # under every window (as the GRID)
                import System
                g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
            except Exception:
                pass
        G.AddGump(g)
        SNAP.skip_gump(g)

    def _build_art(self, look, zones, W, H, arches):
        """(2.6.87) The carved and dragons looks."""
        self._size = (W, H)
        g = G.CreateGump(False, False)
        eg = G.CreateGump(False, False)
        tg = G.CreateGump(False, False)
        Wyrm(self, look, zones, arches, W, H).build(g, eg, tg)
        self._finish_gump(g, True)
        self.g = g
        self._raw = None
        self._finish_gump(eg, False)
        self.edge_g = eg
        self._edge_raw = None
        try:                                       # the small ornaments, over every window
            import System
            tg.LayerOrder = System.Enum.Parse(tg.LayerOrder.GetType(), "Over")
        except Exception:
            pass
        self._finish_gump(tg, False)
        self.top_g = tg
        self._pin()

    def art_slot(self, rect, W, H, zones=None):
        """(2.6.87) The room a window has in zone rect (x, y, w, h): with the dragons look,
        the zone under the game area gives Wyrm.FRAME_W each side to its dragons."""
        if LAYOUT.art != "dragons" or not LAYOUT.unified:
            return rect
        x, y, w, h = rect
        if y + h < H - self.TOUCH or w < 5 * Wyrm.FRAME_W or h < Wyrm.FRAME_MIN_H:
            return rect                            # no room for the figure: no dragons, no gap
        if zones is None:
            zs = LAYOUT.frames
            zones = [(z.kind, z.px) for z in zs.zones if z.px is not None] if zs is not None else []
        for k, (gx, gy, gw, gh) in zones:
            if k == "k" and gy + gh <= y + self.TOUCH and gy + gh >= y - 40 and min(x + w, gx + gw) - max(x, gx) >= w * 0.6:
                return (x + Wyrm.FRAME_W, y, w - 2 * Wyrm.FRAME_W, h)
        return rect

    def build(self, zones, W, H, arches=()):
        old_top, self.top_g = getattr(self, "top_g", None), None   # (2.6.87)
        Kit.dispose(old_top)
        if LAYOUT.art != "plain":
            self._build_art(LAYOUT.art, zones, W, H, arches)
            return
        base = Kit.WINDOW_BG
        s = [Kit.pic_size(base + i) for i in range(9)]
        sized = all(p[0] > 0 and p[1] > 0 for p in s)
        tw, lw = (s[1][1], s[3][0]) if sized else (0, 0)       # top band, left band
        rw, bw = (s[5][0], s[7][1]) if sized else (0, 0)       # right band, bottom band
        g = G.CreateGump(False, False)
        T = self.TOUCH
        # (2.6.74) the stone covers everything that isn't game view: every gap
        # between zones, the strip between the game view and the bar, the screen's
        # edges. 2.6.73 drew it per window zone, so a gap showed the game world or
        # black. The border band runs on the screen's edges and round the game area,
        # on the stone's side. (2.6.75) TazUO draws the world BEFORE every gump (a
        # gump at the bottom of the list still draws over it), so 2.6.74's one
        # stone over the whole screen hid the game view: the keep-clear zones are
        # left open (_stone_rects), a window or reserved zone lying over one stone.
        game = [z for k, z in zones if k == "k" and z[2] > 2 and z[3] > 2]
        arched_top = dict((tuple(a[:4]), a) for a in arches)
        for (sx_, sy_, sw_, sh_) in self._stone_rects(zones, W, H):
            Kit.add_tiled(g, base + 4, sx_, sy_, sw_, sh_)
        if sized:
            for a_, b_ in self._uncovered(0, W, [(x, x + w) for (x, y, w, h) in game if y <= T]):
                Kit.add_tiled(g, base + 1, a_, 0, b_ - a_, tw)
            for a_, b_ in self._uncovered(0, W, [(x, x + w) for (x, y, w, h) in game if y + h >= H - T]):
                Kit.add_tiled(g, base + 7, a_, H - bw, b_ - a_, bw)
            for a_, b_ in self._uncovered(0, H, [(y, y + h) for (x, y, w, h) in game if x <= T]):
                Kit.add_tiled(g, base + 3, 0, a_, lw, b_ - a_)
            for a_, b_ in self._uncovered(0, H, [(y, y + h) for (x, y, w, h) in game if x + w >= W - T]):
                Kit.add_tiled(g, base + 5, W - rw, a_, rw, b_ - a_)
            for (x, y, w, h) in game:
                a = arched_top.get((x, y, w, h))
                y0 = y
                if a is not None:                  # its top is the arch's; its sides start
                    y0 = max([y] + [s_[2] for s_ in (a[4], a[5]) if s_ is not None])
                elif y > T:
                    Kit.add_tiled(g, base + 7, x, y - bw, w, bw)
                if y + h < H - T:
                    Kit.add_tiled(g, base + 1, x, y + h, w, tw)
                if x > T and y + h > y0:
                    Kit.add_tiled(g, base + 5, x - rw, y0, rw, y + h - y0)
                if x + w < W - T and y + h > y0:
                    Kit.add_tiled(g, base + 3, x + w, y0, lw, y + h - y0)
        # (2.6.72) the gold round the game area runs in the stone just OUTSIDE it
        # (it was drawn inside, over the world), 1 px light line on the game
        # side; a side on the screen's edge has no stone outside and no gold.
        # No corner knot on the game area any more: knots only on the surround's
        # outer corners (the screen corners the stone covers).
        GW = self.GOLD_W
        GT = GW + 1
        # (2.6.73) the gold is drawn in a window of its own above the game view (the
        # backdrop now sits under the view, whose 5 px border would cover it)
        eg = G.CreateGump(False, False)
        arched = {}                                # (2.6.72) (x, y, w, h) -> its arch
        for a in arches:
            arched[tuple(a[:4])] = a
            # (2.6.74) the crown strip above it is stone already (_stone_rects: it is
            # outside the keep-clear zone)
        for k, (x, y, w, h) in zones:
            if k != "k" or w <= 2 or h <= 2:
                continue
            a = arched.get((x, y, w, h))
            top, bot, lft, rgt = y >= GT, y + h <= H - GT, x >= GT, x + w <= W - GT
            if a is not None:
                # (2.6.72) arched: its top is the arch's (drawn with the shoulders); its
                # sides start under the shoulders
                top = False
                y0 = max([y] + [s_[2] for s_ in (a[4], a[5]) if s_ is not None])
                h, y = h - (y0 - y), y0
            # the outer band (GW px, dark) and the line on the game's edge (1 px, light)
            dx0, dx1 = (x - GT if lft else x), (x + w + GT if rgt else x + w)
            dy0, dy1 = (y - GT if top else y), (y + h + GT if bot else y + h)
            lx0, lx1 = (x - 1 if lft else x), (x + w + 1 if rgt else x + w)
            ly0, ly1 = (y - 1 if top else y), (y + h + 1 if bot else y + h)
            if top:
                Kit.add_box(eg, dx0, y - GT, dx1 - dx0, GW, 1.0, self.GOLD_DARK)
                Kit.add_box(eg, lx0, y - 1, lx1 - lx0, 1, 1.0, self.GOLD_LIGHT)
            if bot:
                Kit.add_box(eg, dx0, y + h + 1, dx1 - dx0, GW, 1.0, self.GOLD_DARK)
                Kit.add_box(eg, lx0, y + h, lx1 - lx0, 1, 1.0, self.GOLD_LIGHT)
            if lft:
                Kit.add_box(eg, x - GT, dy0, GW, dy1 - dy0, 1.0, self.GOLD_DARK)
                Kit.add_box(eg, x - 1, ly0, 1, ly1 - ly0, 1.0, self.GOLD_LIGHT)
            if rgt:
                Kit.add_box(eg, x + w + 1, dy0, GW, dy1 - dy0, 1.0, self.GOLD_DARK)
                Kit.add_box(eg, x + w, ly0, 1, ly1 - ly0, 1.0, self.GOLD_LIGHT)
        cw, ch = Kit.pic_size(Kit.CORNER_ART) if Kit.CORNER_ART else (0, 0)
        if cw and ch:
            for kx, ky in ((0, 0), (W - cw, 0), (0, H - ch), (W - cw, H - ch)):
                # (2.6.74) a screen corner the stone covers: one no game area reaches
                if not any(x < kx + cw and kx < x + w and y < ky + ch and ky < y + h
                           for (x, y, w, h) in game):
                    Kit.add_pic(g, Kit.CORNER_ART, kx, ky, mouse=False)
        g.SetRect(0, 0, W, H)
        safe(lambda: g.SetAcceptMouseInput(False))
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        safe(lambda: setattr(g, "CanMove", False))
        try:                                       # under every window (as the GRID)
            import System
            g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
        except Exception:
            pass
        G.AddGump(g)
        SNAP.skip_gump(g)                          # never snaps, kept or slotted
        self.g = g
        self._raw = None
        if arches:                                 # (2.6.72) the arch's shoulders, on top

            def gold(gg, x, y, w, horiz):
                Kit.add_box(gg, x, y, w, 3, 1.0, self.GOLD_DARK)
                Kit.add_box(gg, x, y + 3, w, 1, 1.0, self.GOLD_LIGHT)
            self.build_arch(arches[0], gold, W, H, eg)
        eg.SetRect(0, 0, W, H)
        safe(lambda: eg.SetAcceptMouseInput(False))
        safe(lambda: setattr(eg, "CanCloseWithRightClick", False))
        safe(lambda: setattr(eg, "CanMove", False))
        G.AddGump(eg)
        SNAP.skip_gump(eg)
        self.edge_g = eg
        self._pin()


class Layout(object):
    """The engine: the frame layout and window layout in use, the registered
    windows, placing, drops, the saved names and the editor (LayoutEditor)."""
    GRID_SAVE = "grid=%d"

    def __init__(self):
        self.wins = {}             # dock key -> (get_gump, title)
        self.assign = {}           # zone id -> [dock keys], top to bottom
        self.frames = None         # the ZoneSet in use (with px for this screen)
        self.frames_name = LAYOUT_DEFAULT
        self.layout_name = ""      # "" = no window layout: every window free
        self.game_grows = True
        self.unified = False       # (2.6.70) Settings > Layout: one frame (Surround)
        self.arch = True           # (2.6.72) Settings > Layout: arch the game view (with one frame)
        self.fit_view = True       # (2.6.85) Settings > Layout: the game view fits the keep-clear zone
        self.art = "carved"        # (2.6.85) Settings > Layout: the frame's art (Surround.ART_LOOKS)
        self.ping = False          # (2.6.72) Settings > Layout: the ping readout (with one frame)
        self.surround = Surround()
        self.screen = None         # (W, H) the zones were computed for
        self.dirty = True          # compute the zones again on the next pass
        self.occ = None            # the zones with a window in them, as last seen
        self.gump_key = {}         # gump -> dock key, as last seen
        self.placed = {}           # dock key -> (x, y, w, h) last placed
        self.squeezed_told = set() # (zone id, key) whose window was minimized for room
        self.editor = None
        self.loaded = False
        self.page_refresh = False  # the Layout page should draw again
        self.last_names = None
        # (2.6.55) the zone fit
        self.hooks = {}            # dock key -> its hooks ("fit", "scale", "redraw", "state")
        self.owner = {}            # dock key -> (module key, part key) whose code listed it
        self.fitted = {}           # dock key -> how it is fitted now (see _fit_slot)
        self.base = {}             # (2.6.56) dock key -> its own size, as first seen slotted
        self.fresh = False         # a window was just added: fit it on the next look
        self.fresh_adds = set()    # (2.6.82) windows added since the last look (G.AddGump)
        self.client_seen = {}      # (2.6.57) client window kind -> the ClientWin last seen
        self.journal_held = None   # (2.6.57) the client's journal, held in a reserved zone
        self.pair_tried = None     # (2.6.66) the zone a bags zone couldn't be made under
        self.client_settle = {}    # (2.6.69) client window key -> (window, rect settled, rect last seen)
        self.misfit = {}           # (2.6.69) dock key -> passes in a row its size wasn't its slot's
        self.fallback = {}         # (2.6.70) dock key -> slot size the layout stretches it to itself
        self.client_told = set()   # (2.6.63) client window kinds whose "can't be found" was said
        self.chat_seen = (0.0, None)   # (2.6.60) (when read, chat line rect or None)
        # (2.6.72) zones hold their windows: a slotted window can't be dragged
        # (CanMove False) unless Arrange mode is on
        self.held = {}             # gump -> (dock key, CanMove it had before it was held)
        self.arrange = False       # Arrange mode: zoned windows may be dragged between zones
        self.arrange_last = 0.0    # when Arrange was turned on or a window was last dragged in it
        self.arrange_g = None      # the zone outlines drawn while Arrange is on
        self.arrange_lit = {}      # zone id -> its "drop here" box in that gump
        self.arrange_hot = None    # zone id lit now
        self.client_target = {}    # client window key -> (x, y) the layout last put it at
        self.min_told = set()      # client window kinds told their zone is under their minimum
        # (2.6.73) the drop rules' notes; (2.6.74) the standing repair (Layout._repair)
        self.repair_at = 0.0       # (2.6.74) next look of the standing repair
        self.repair_told = set()   # (2.6.74) keys told "no zone to go back to" this session
        self.freed = None          # (2.6.74) keys you freed on Settings > Layout (FREED_VAR)
        self.page_preview = ""     # (2.6.74) Settings > Layout: the last zone pick's size line
        self.homes = None          # (2.6.74) key -> the zone it last sat in (HOMES_VAR)
        self.back_told = False     # "stays in a zone" said this session

    # ---------- saved state ----------
    # ---------- (2.6.57) the client's own windows ----------
    #  TazUO's World Map is a window like any other here ("worldmap", the key
    #  the sketch gives it): made exactly its slot's size through the client
    #  (its ResizeWindow), kept there, and given back its own place and size
    #  when freed. The client's journal lives in the first reserved zone of the
    #  frame layout in use (L3 in the sketch), the same way. TazUO's chat line
    #  stays where the client puts it (the bottom of the game area); typing is
    #  untouched.
    def _client_getter(self, kind, key):
        def get():
            cw = ClientWin.of(kind)
            if cw is not self.client_seen.get(kind):
                self.client_seen[kind] = cw      # opened again: fitted afresh
                self.fitted.pop(key, None)
                self.placed.pop(key, None)
            if cw is None and kind not in self.client_told and ClientWin.errors.get(kind) \
                    and self.zone_of(key) is not None:
                self.client_told.add(kind)       # (2.6.63) can't be found: said once
                API.SysMsg("%s: %s can't be found to place it in its zone: %s." % (
                    APP_NAME, ClientWin.TITLES.get(kind, kind), ClientWin.errors[kind]),
                    Kit.HUE_BAD)
            return cw
        return get

    def _client_fit(self, kind):
        # (2.6.63) called on every pass while it sits in a zone ("client" hook):
        # ClientWin.fit puts it back whenever it isn't its slot's size
        def fit(w, h, mode):
            cw = ClientWin.of(kind)
            if cw is None:
                return
            if w is None or h is None:
                cw.free()
            else:
                cw.fit(int(w), int(h), lock=not self.arrange)
                cw.report()
        return fit

    def _client_drops(self):
        """(2.6.69) A client window (TazUO's World Map) is not one of the script's
        own, so the snapping never sees it dragged and let go: it is watched here
        instead, on the keeper's pass, while it is free. A move that has come to
        rest (the same place two looks in a row, the mouse button up) at the same
        size is a drag let go, and goes to Layout.dropped like any other window's
        drop: slotted in the window zone it was let go on (Alt held: left where it
        is). A change of size (its resize grip, its fullscreen) is never a drop."""
        if not self.arrange:                         # (2.6.72) only Arrange mode slots a drop
            self.client_settle.clear()
            return
        for key in ClientWin.DROPS:
            if key not in self.wins:
                self.client_settle.pop(key, None)
                continue
            cw = ClientWin.of(key)
            if cw is None:
                self.client_settle.pop(key, None)
                continue
            try:
                r = cw.rect()
            except Exception:
                continue
            if self.zone_of(key) is not None:
                # (2.6.72) zoned (Arrange mode: unlocked): moved off the place the layout
                # put it, at its size, with the button up (the keeper only runs then): let go
                self.client_settle.pop(key, None)
                at = self.client_target.get(key)
                if at is not None and max(abs(r[0] - at[0]), abs(r[1] - at[1])) > SNAP_DIST \
                        and SNAP.pressed() is not True:
                    self.client_target.pop(key, None)
                    self.dropped(cw)
                continue
            st = self.client_settle.get(key)
            if st is None or st[0] is not cw:
                self.client_settle[key] = (cw, r, r)     # first look: where it rests now
                continue
            settled, last = st[1], st[2]
            if r != last:
                self.client_settle[key] = (cw, settled, r)   # still on the move
                continue
            if r == settled or SNAP.pressed() is True:
                continue                                 # at rest where it was, or still held
            self.client_settle[key] = (cw, r, r)
            if (r[2], r[3]) != (settled[2], settled[3]):
                continue                                 # resized, not dragged
            self.dropped(cw)

    CHAT_LOOK = 0.5          # (2.6.60) seconds between looks at where the chat line is
    CHAT_ROOM = 18           # TazUO's chat line: CHAT_HEIGHT 15 + CHAT_X_OFFSET 3
    JOURNAL_MIN_H = 60       # the journal is never squeezed shorter than this

    def _chat_line(self):
        """(2.6.60) (x, top, w) of TazUO's chat line on screen: the bottom strip
        of the game area (SystemChatControl, its TextBoxControl at Height - 18),
        or None when it can't be read. Read at most every CHAT_LOOK s (it only
        moves when the game area is moved or resized). Client thread."""
        now = time.time()
        at, rect = self.chat_seen
        if now - at < Layout.CHAT_LOOK:
            return rect
        rect = None
        try:
            Typing._find()
            sc = Typing._get(None, "SystemChat", Typing.uim) if Typing.uim is not None else None
            if sc is not None and not bool(Typing._get(sc, "IsDisposed", default=True)):
                f = ClientWin._bf[0]
                if f is None:
                    from System.Reflection import BindingFlags
                    f = ClientWin._bf[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetField(
                        "_bounds", BindingFlags.Instance | BindingFlags.NonPublic)
                b = f.GetValue(sc)
                sx = int(Typing._get(sc, "ParentX", default=0) or 0) + int(b.X)
                sy = int(Typing._get(sc, "ParentY", default=0) or 0) + int(b.Y)
                top = sy + int(b.Height) - Layout.CHAT_ROOM
                tb = Typing._get(sc, "TextBoxControl")
                if tb is not None:               # where the line really is, when readable
                    tby = int(f.GetValue(tb).Y)
                    if 0 <= tby < int(b.Height):
                        top = min(top, sy + tby)
                if int(b.Width) > 0 and int(b.Height) > 0:
                    rect = (sx, top, int(b.Width))
        except Exception:
            rect = None
        self.chat_seen = (now, rect)
        return rect

    def _clear_of_chat(self, x, y, w, h, H):
        """(2.6.60) The journal's height in its zone (x, y, w, h), shortened so
        it ends above TazUO's chat line when the line would be behind it. When
        the line can't be read, a zone at the bottom of the screen keeps
        CHAT_ROOM px free at its foot."""
        line = self._chat_line()
        if line is None:
            cut = Layout.CHAT_ROOM if H and y + h >= H - 2 else 0
            bottom = y + h - cut
        else:
            lx, top, lw = line
            if x >= lx + lw or lx >= x + w or not (y < top < y + h):
                return h                         # the line isn't behind the journal
            bottom = top
        return max(min(h, Layout.JOURNAL_MIN_H), bottom - y)

    def _hold_journal(self, zs, H=0):
        """The client's journal in the first reserved zone (only while a window
        layout is in use); freed when there is none. (2.6.60) It stops above
        TazUO's chat line when that would sit behind it."""
        z = None
        if self.layout_name or self.assign:
            for zz in zs.zones:
                if zz.kind == "r" and zz.px is not None:
                    z = zz
                    break
        cw = ClientWin.of("journal") if z is not None else None
        held = self.journal_held
        if held is not None and held is not cw:
            held.free()
            self.journal_held = None
        if cw is None:
            return
        x, y, w, h = z.px
        if self.unified:                         # (2.6.72) in the stone like every zone
            il, it_, ir, ib = self._slot_insets(z, z.px)
            x, y, w, h = x + il, y + it_, max(1, w - il - ir), max(1, h - it_ - ib)
        h = self._clear_of_chat(x, y, w, h, H)   # (2.6.60) the chat line shows below it
        cw.fit(w, h)
        try:
            if (cw.GetX(), cw.GetY()) != (x, y):
                cw.SetPos(x, y)
        except Exception:
            pass
        cw.report()
        self.journal_held = cw

    def load(self):
        # 2.6.81: a profile load wrote its own freed set and homes: read them again
        self.freed = None
        self.homes = None
        self.repair_told = set()
        self.back_told = False
        self.loaded = True
        if "worldmap" not in self.wins:          # (2.6.57) TazUO's World Map
            # (2.6.69) "inset": TazUO draws the map 4 px in from the window's edge
            # all round (its border, hidden while locked), so the window is made 4 px
            # bigger than its slot on every side and the map itself fills the zone
            self.add("worldmap", self._client_getter("worldmap", "worldmap"), "TazUO's World Map",
                     {"fit": self._client_fit("worldmap"), "exact": True, "client": True,
                      "inset": ClientWin.INSET.get("worldmap", 0)})
        self.frames_name = Kit.get_var(FRAMES_ACTIVE, LAYOUT_DEFAULT) or LAYOUT_DEFAULT
        if self.frames_name != LAYOUT_DEFAULT and self.frames_name not in self.frame_names():
            self.frames_name = LAYOUT_DEFAULT
        self.layout_name = Kit.get_var(LAYOUT_ACTIVE, "")
        opts = Kit.get_var(LAYOUT_OPTS, "game=1")
        self.game_grows = "game=0" not in opts
        self.unified = "frame=1" in opts             # (2.6.70) one frame round the game
        self.arch = "arch=0" not in opts             # (2.6.72) the arched game view (on unless unticked)
        self.fit_view = "fit=0" not in opts          # (2.6.85) on unless unticked
        self.art = "carved"
        for look in Surround.ART_LOOKS:              # (2.6.85) (an older version skips the key)
            if "art=" + look in opts:
                self.art = look
        self.ping = "ping=1" in opts                 # (2.6.72) the ping readout (off unless ticked)
        raw = Kit.get_var(LAYOUT_VAR, "")
        self.assign = self.parse_windows(raw)[1]
        if raw and raw != self.windows_text():       # (2.6.57) obsolete occupants dropped:
            gone = False                             # saved without them
            for part in str(raw).split(";"):
                if "=" in part and part.split("=", 1)[0].strip() != "frames":
                    for k in part.split("=", 1)[1].split(","):
                        if k.strip() in LAYOUT_GONE:
                            gone = True
            if gone:
                self.save_assign()
        self.frames = None
        self.dirty = True

    def save_assign(self):
        Kit.put_var(LAYOUT_VAR, self.windows_text())
        try:
            self._note_homes()                       # (2.6.74) for the standing repair
        except Exception:
            pass

    RECLAIM_VAR = "VirtueAssistant_reclaim_undo"     # per character: "name|default|text"
    RECLAIM_FIXED = "VirtueAssistant_reclaim_fixed"  # "1": a stretched layout was looked for

    def _undo_load(self):
        """The one-step undo, kept over a restart (2.6.85's was gone with the script)."""
        if getattr(self, "reclaim_undo", None) is None and not getattr(self, "_undo_read", False):
            self._undo_read = True
            p = str(Kit.get_var(self.RECLAIM_VAR, "") or "").split("|", 2)
            if len(p) == 3 and p[0]:
                self.reclaim_undo = (p[0], p[2], None, p[1] == "1")
        return getattr(self, "reclaim_undo", None)

    def _undo_set(self, undo):
        self.reclaim_undo = undo
        self._undo_read = True
        Kit.put_var(self.RECLAIM_VAR, "" if undo is None else
                    "%s|%d|%s" % (undo[0], 1 if undo[3] else 0, undo[1]))

    @staticmethod
    def _reclaim_edges(zs, z, blockers, W, H):
        """z's rect grown out to the first blocker in its lane, or the screen's edge."""
        x, y, w, h = z.px
        for side in "LTRB":
            lim = {"L": 0, "T": 0, "R": W, "B": H}[side]
            for o in blockers:
                if o is z or o.px is None:
                    continue
                ox, oy, ow, oh = o.px
                if side in "LR":
                    if not (oy < y + h and y < oy + oh):
                        continue
                    if side == "L" and ox + ow <= x:
                        lim = max(lim, ox + ow)
                    elif side == "R" and ox >= x + w:
                        lim = min(lim, ox)
                else:
                    if not (ox < x + w and x < ox + ow):
                        continue
                    if side == "T" and oy + oh <= y:
                        lim = max(lim, oy + oh)
                    elif side == "B" and oy >= y + h:
                        lim = min(lim, oy)
            if side == "L" and lim < x:
                w, x = w + (x - lim), lim
            elif side == "T" and lim < y:
                h, y = h + (y - lim), lim
            elif side == "R" and lim > x + w:
                w = lim - x
            elif side == "B" and lim > y + h:
                h = lim - y
        return x, y, w, h

    def reclaim_zones(self, zs, W, H):
        """(2.6.86) What Reclaim space changes: the keep-clear zones first, out to the
        first window zone in their way; then the other window zones into any gap still
        beside them. A zone that hugs its window or lies over the game area (the frames in
        an arch's corners) is never grown and never counts as in the way: growing one
        scales its window up over the game view (2.6.85 did, through Fill the gaps). A
        locked zone stays. Returns the ids changed."""
        fixed = [o for o in zs.zones if o.px is not None and not o.hug and
                 (o.kind != "k" and not o.overlap)]
        changed = []
        for z in zs.zones:
            if z.kind != "k" or z.lock or z.px is None:
                continue
            r = self._reclaim_edges(zs, z, fixed, W, H)
            if r != tuple(z.px):
                z.set_px(r[0], r[1], r[2], r[3], W, H)
                changed.append(z.id)
        for z in zs.zones:
            if z.kind != "w" or z.hug or z.overlap or z.lock or z.px is None:
                continue
            others = [o for o in zs.zones if o.px is not None and (o.kind != "r" or z.kind == "r")]
            r = self._reclaim_edges(zs, z, others, W, H)
            if r != tuple(z.px):
                z.set_px(r[0], r[1], r[2], r[3], W, H)
                changed.append(z.id)
        return changed

    def reclaim_space(self):
        """(2.6.85) Settings > Layout's Reclaim space: the gaps beside the zones go, and the
        keep-clear zone takes them. Says what changed; Undo puts the layout before it back,
        once. (2.6.86) See reclaim_zones; a result with less game area is never kept."""
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        if zs is None or not zs.zones:
            API.SysMsg("%s: no frame layout in use: nothing to reclaim." % APP_NAME, Kit.HUE_INFO)
            return

        def game_rect():
            best = (0, 0)
            for z in zs.zones:
                if z.kind == "k" and z.px is not None and z.px[2] * z.px[3] > best[0] * best[1]:
                    best = (z.px[2], z.px[3])
            return best
        was = game_rect()
        default = self.frames_name == LAYOUT_DEFAULT
        undo = (zs.name, zs.save_text(), was, default)
        moved = self.reclaim_zones(zs, W, H)
        now = game_rect()
        if not moved or now[0] * now[1] < was[0] * was[1]:
            self.frames, self.dirty = None, True     # as it was
            API.SysMsg("%s: Reclaim space: every zone is already as tight as it goes." % APP_NAME,
                       Kit.HUE_INFO)
            return
        self._undo_set(undo)
        target = zs.name if not default else "Reclaimed"
        zs.generated = False
        self.save_frames(zs, target, W, H)
        self.use_frames(target, False)
        self.refit_all()
        API.SysMsg("%s: Reclaim space: %d zone%s tightened; game area %d x %d, was %d x %d. "
                   "Undo puts it back." % (APP_NAME, len(moved), "" if len(moved) == 1 else "s",
                                           now[0], now[1], was[0], was[1]), Kit.HUE_GOOD)

    def reclaim_back(self):
        undo = self._undo_load()
        if undo is None:
            return
        self._undo_set(None)
        W, H = Kit.screen()
        if undo[3]:                              # it was Default: Default again
            self.use_frames(LAYOUT_DEFAULT, False)
        else:
            zs = ZoneSet.parse(undo[0], undo[1])
            if zs is None:
                return
            zs.reflow(W, H, HOST.grid_size())
            self.save_frames(zs, undo[0], W, H)
            self.use_frames(undo[0], False)      # read again from what was just saved
        self.refit_all()
        API.SysMsg("%s: Reclaim space undone." % APP_NAME, Kit.HUE_INFO)

    def _repair_stretched(self, zs, W, H):
        """(2.6.86) Once: 2.6.85's Reclaim space could stretch the zones of the frames in an
        arch's corners down over the game view, and saved that. A hugging zone over 45% of
        the screen's height goes back to the height of the band it belongs in. What it was
        is kept for Undo."""
        if Kit.get_var(self.RECLAIM_FIXED, "") == "1":
            return
        Kit.put_var(self.RECLAIM_FIXED, "1")
        tall = [z for z in zs.zones if z.hug and z.px is not None and z.rect[3] >= 450]
        if not tall:
            return
        self._undo_set((zs.name, zs.save_text(), None, False))
        top = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX))
        for z in tall:
            z.set_px(z.px[0], z.px[1], z.px[2], top, W, H)
        self.save_frames(zs, zs.name, W, H)
        API.SysMsg("%s: Reclaim space had stretched %d frame zone%s in layout \"%s\"; put right. "
                   "Undo in Settings > Layout puts it back." % (
                       APP_NAME, len(tall), "" if len(tall) == 1 else "s", zs.name), Kit.HUE_GOOD)

    def refit_all(self):
        try:
            HOST.layout_refit()
        except Exception:
            pass
        self.page_refresh = True

    def save_opts(self):
        Kit.put_var(LAYOUT_OPTS, "game=%d;frame=%d;arch=%d;ping=%d;fit=%d;art=%s" % (
            1 if self.game_grows else 0, 1 if self.unified else 0, 1 if self.arch else 0,
            1 if self.ping else 0, 1 if self.fit_view else 0, self.art))

    @staticmethod
    def parse_windows(text):
        """(frames name, {zone: [keys]}) from a window layout's saved form."""
        frames, out = LAYOUT_DEFAULT, {}
        for part in str(text or "").split(";"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            k = k.strip()
            if k == "frames":
                frames = v.strip() or LAYOUT_DEFAULT
                continue
            keys = [s.strip() for s in v.split(",")
                    if s.strip() and s.strip() not in LAYOUT_GONE]
            if k and keys:
                out[k] = keys
        return frames, out

    def windows_text(self, frames=None):
        items = ["frames=%s" % (frames or self.frames_name)]
        for zid in sorted(self.assign):
            if self.assign[zid]:
                items.append("%s=%s" % (zid, ",".join(self.assign[zid])))
        return ";".join(items)

    @staticmethod
    def _names(var):
        return [n for n in Kit.get_var(var, "").split(",") if n.strip()]

    def frame_names(self):
        return self._names(FRAMES_LIST)

    def layout_names(self):
        return self._names(LAYOUT_LIST)

    @staticmethod
    def clean_name(name, fallback):
        name = re.sub(r"[^A-Za-z0-9 ()'_-]", "", str(name or "")).strip()[:24]
        return name or fallback

    # ---------- the windows ----------
    def add(self, key, getter, title=None, hooks=None, owner=None):
        key = str(key)
        if key in LAYOUT_GONE:                       # (2.6.57) never a zone occupant
            return
        self.wins[key] = (getter, str(title or key))
        self.hooks[key] = hooks if hasattr(hooks, "get") else {}
        if owner is not None:
            self.owner[key] = owner
        self.fitted.pop(key, None)
        self.dirty = True

    def remove(self, key):
        key = str(key)
        self.wins.pop(key, None)
        self.placed.pop(key, None)
        self.hooks.pop(key, None)
        self.owner.pop(key, None)
        self.fitted.pop(key, None)
        self.base.pop(key, None)
        self.dirty = True

    def owner_of(self, key):
        """(module key, part key or None) of window `key`: the module whose code
        listed it, else the module its key names ("<module>.<part>..." or an
        old module key); (None, None) when unknown."""
        o = self.owner.get(key)
        if o is not None:
            return o
        k = str(key)
        while k:
            s, part = HOST.resolve(k)
            if s is not None:
                return s.key, part
            if "." not in k:
                break
            k = k.rsplit(".", 1)[0]
        return None, None

    def windows_of(self, module_key):
        """[(dock key, title)] of the windows listed for module `module_key`
        (its parts' included), by title; for its WINDOWS section."""
        out = []
        for key in self.wins:
            if self.owner_of(key)[0] == module_key:
                out.append((key, self.title_of(key)))
        out.sort(key=lambda kt: kt[1].lower())
        return out

    def all_windows(self):
        """[(dock key, "<Module>: <title>")] of every listed window, by module
        then title; for the Layout page."""
        out = []
        for key in self.wins:
            mk = self.owner_of(key)[0]
            s = dict.get(HOST.by_key, mk) if mk else None
            t = self.title_of(key)
            if s is not None and s.title != t:
                t = "%s: %s" % (s.title, t)
            out.append((key, t))
        out.sort(key=lambda kt: kt[1].lower())
        return out

    def zone_choices(self):
        """[None, zone id, ...]: free, then every window zone of the frame
        layout in use, in its order (what the Zone buttons cycle through)."""
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames
        out = [None]
        if zs is not None:
            out.extend(z.id for z in zs.zones if z.kind == "w")
        return out

    def assign_to(self, key, zid, tell=True):
        """Put window `key` in zone `zid` (at the end of its stack), or free it
        (zid None); from the settings' Zone buttons and drop-downs."""
        key = str(key)
        old = self.zone_of(key)
        if old == zid:
            return
        if tell and zid and ((key != "worldmap" and zid == self._map_zone())
                             or (key == "worldmap" and self.assign.get(zid))):
            # (2.6.73) TazUO's World Map keeps a zone to itself
            API.SysMsg("%s: TazUO's World Map keeps its zone to itself; pick another zone for %s."
                       % (APP_NAME, self.title_of(key) if key != "worldmap" else "it"), Kit.HUE_BAD)
            self.page_refresh = True
            return
        if old is not None:
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if not self.assign[old]:
                del self.assign[old]
        if zid:
            self.assign.setdefault(zid, []).append(key)
            self.unfree(key)                         # (2.6.74) the layout's again
        elif tell:
            self.free_by_you([key])                  # (2.6.74) the repair leaves it free
        self.save_assign()
        if not zid:
            self.free_scrolled()                     # its own size again (before placed forgets it)
        self.placed.pop(key, None)
        self.dirty = True
        self.squeezed_told.discard(key)
        self.page_refresh = True
        if tell:
            if zid:
                API.SysMsg('%s: %s sits in zone "%s" now.' % (APP_NAME, self.title_of(key), zid),
                           Kit.HUE_GOOD)
            else:
                API.SysMsg("%s: %s is free; it stays where you put it." % (APP_NAME, self.title_of(key)),
                           Kit.HUE_GOOD)
        HOST.poke()

    def zone_of(self, key):
        for zid, keys in self.assign.items():
            if key in keys:
                return zid
        return None

    def need(self, key, w, h):
        zid = self.zone_of(str(key))
        zs = self.frames
        if zid is None or zs is None:
            return
        want = (w, h) if (w or h) else None
        if zs.needs.get(zid) != want:
            if want is None:
                zs.needs.pop(zid, None)
            else:
                zs.needs[zid] = want
            self.need_due = True                     # reflowed at the end of this pass

    def zone_base(self, key):
        zid = self.zone_of(str(key))
        zs = self.frames
        z = zs.by_id(zid) if (zid is not None and zs is not None) else None
        if z is None:
            return None
        W, H = zs.screen
        if W <= 0 or H <= 0:
            W, H = Kit.screen()
        keep, z.px = z.px, None
        try:
            return (max(1, int(W * z.rect[2] / 1000.0)), max(1, int(H * z.rect[3] / 1000.0)))
        finally:
            z.px = keep

    def holds(self, key):
        """Is window `key` slotted in a zone of the layout in use (so its
        module leaves its place to the layout). (2.6.81) A zone the frame layout
        in use doesn't have holds nothing: nothing places the window there."""
        zid = self.zone_of(str(key))
        if zid is None:
            return False
        zs = self.frames
        return zs is None or zs.by_id(zid) is not None

    # ---------- (2.6.72) zones hold their windows ----------
    #  A window in a zone is locked there (CanMove False, written only when it
    #  differs), so a drag can't take it out by accident. Rearranging is a mode:
    #  Arrange (Settings > Layout, or the Action Bar's Lock button) shows every
    #  zone's outline and name, lets the zoned windows be dragged, and a drop
    #  slots, reorders, swaps or frees as before. It ends with the same button,
    #  Esc, or ARRANGE_IDLE s without a drag. A module that sets CanMove itself
    #  asks Host.layout_locked(key) first.
    ARRANGE_IDLE = 60.0

    def locked(self, key):
        """Window `key` sits in a zone and Arrange mode is off: it must not move."""
        return not self.arrange and self.holds(key)

    def _hold(self, g, key):
        """Window g (slotted) can't be dragged unless Arrange is on; checked on
        every pass (a module or the client may have turned dragging back on)."""
        if isinstance(g, ClientWin):
            return                                   # its own lock (ClientWin.fit)
        rec = self.held.get(g)
        if rec is None:
            try:
                own = bool(g.CanMove)
            except Exception:
                own = True
            self.held[g] = rec = (key, own)
            for f, l in list(SNAP.links.items()):    # no snap link to or from it
                if f is g or l is g:
                    SNAP.links.pop(f, None)
        want = bool(self.arrange)
        try:
            if bool(g.CanMove) != want:
                g.CanMove = want
        except Exception:
            pass

    def _release(self, keep):
        """Every held window not in `keep` gets its own CanMove back."""
        for g in [g for g in self.held if g not in keep]:
            key, own = self.held.pop(g)
            if g in SNAP.drag or not Kit.is_open(g):
                continue
            if not own and not self.holds(key):
                # 2.6.81: built locked because it sat in a zone, now free: its module
                # builds it again and sets CanMove itself (its own lock included);
                # with no way to rebuild it, it is made draggable
                rd = (self.hooks.get(key) or {}).get("redraw")
                if callable(rd):
                    safe(rd)
                    continue
                own = True
            try:
                if bool(g.CanMove) != own:
                    g.CanMove = own
            except Exception:
                pass

    def set_arrange(self, on, tell=True):
        """Arrange mode on or off (the Settings > Layout button, the Action Bar's
        Lock button, Esc, or ARRANGE_IDLE s without a drag)."""
        on = bool(on)
        if on == self.arrange:
            return
        self.arrange = on
        self.arrange_last = time.time()
        self.arrange_hot = None
        if not on:
            old, self.arrange_g = self.arrange_g, None
            self.arrange_lit = {}
            Kit.dispose(old)
        self.dirty = True
        self.page_refresh = True
        if tell:
            if on:
                API.SysMsg("%s: arrange mode on; drag a window on to a zone, then click Done."
                           % APP_NAME, Kit.HUE_GOOD)
            else:
                API.SysMsg("%s: windows locked in their zones." % APP_NAME, Kit.HUE_GOOD)
        HOST.poke()

    def _arrange_tick(self, zs, W, H):
        """While Arrange is on (the keeper's pass): the zone outlines, and the
        mode ends after ARRANGE_IDLE s with no drag."""
        if not self.arrange:
            return
        now = time.time()
        if SNAP.drag:
            self.arrange_last = now
        elif now - self.arrange_last > self.ARRANGE_IDLE:
            self.set_arrange(False)
            return
        sig = (W, H, tuple((z.id, z.kind, tuple(z.px)) for z in zs.zones if z.px is not None))
        if self.arrange_g is not None and Kit.is_open(self.arrange_g) \
                and getattr(self, "_arrange_sig", None) == sig:
            return
        self._arrange_sig = sig
        old, self.arrange_g = self.arrange_g, None
        self.arrange_lit = {}
        Kit.dispose(old)
        g = G.CreateGump(False, False)
        for z in zs.zones:
            if z.px is None or z.kind != "w":
                continue
            x, y, w, h = z.px
            col = ZONE_COLORS.get(z.kind, "#3A78C8")
            lit = Kit.add_box(g, x, y, w, h, 0.30, col)
            safe(lambda: setattr(lit, "IsVisible", False))
            self.arrange_lit[z.id] = lit
            for bx, by, bw_, bh in ((x, y, w, 2), (x, y + h - 2, w, 2), (x, y, 2, h), (x + w - 2, y, 2, h)):
                Kit.add_box(g, bx, by, bw_, bh, 0.9, col)
            # (2.6.74) the name on a small black plate in the zone's bottom-left corner: at
            # the top it sat on the windows' title text (Social's, Combat's)
            name = Kit.fit(z.id, max(20, w - 28))
            pw = Kit.text_w(name) + 12
            Kit.add_box(g, x + 6, y + h - 6 - 22, pw, 22, 0.85, "#000000")
            Kit.add_label(g, name, x + 12, y + h - 6 - 20, Kit.HUE_TITLE)
        g.SetRect(0, 0, W, H)
        safe(lambda: g.SetAcceptMouseInput(False))
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        safe(lambda: setattr(g, "CanMove", False))
        G.AddGump(g)
        SNAP.skip_gump(g)
        self.arrange_g = g
        self.arrange_hot = None

    def arrange_hover(self, g, r=None):
        """(Snap.tick, while a window is dragged in Arrange mode) light the zone
        it would go into if let go now. Only changes are written. r: its rect,
        when the caller just read it (2.6.82)."""
        if not self.arrange or not self.arrange_lit or self.frames is None:
            return
        if r is None:
            r = Snap.rect(g)
        z = self._drop_zone(r) if r is not None else None
        zid = z.id if z is not None else None
        if zid == self.arrange_hot:
            return
        for k in (self.arrange_hot, zid):
            box = self.arrange_lit.get(k) if k is not None else None
            if box is not None:
                safe(lambda: setattr(box, "IsVisible", k == zid))
        self.arrange_hot = zid

    def _min_of(self, key, g=None):
        """(w, h) window `key` can't be made smaller than (a client window's own
        minimum, a module's "min" hook), or None."""
        hooks = self.hooks.get(key) or {}
        mn = hooks.get("min")
        if callable(mn):
            mn = safe(mn)
        if mn:
            try:
                return int(mn[0]), int(mn[1])
            except Exception:
                pass
        g = g if g is not None else self.gump_of(key)
        if isinstance(g, ClientWin):
            m = g._min_size()
            if m[0] > 0 or m[1] > 0:
                return m
        return None

    def _too_small(self, key, z, g=None):
        """True (and one journal line) when zone z is smaller than window
        `key` can be made."""
        mn = self._min_of(key, g)
        if mn is None or z is None or z.px is None:
            return False
        if z.px[2] >= mn[0] and z.px[3] >= mn[1]:
            return False
        API.SysMsg("%s: %s needs a zone at least %d x %d." % (
            APP_NAME, self.title_of(key), mn[0], mn[1]), Kit.HUE_BAD)
        return True

    def title_of(self, key):
        w = self.wins.get(key)
        if w is not None:
            return w[1]
        s = HOST.page_slot(key)
        return s.title if s is not None else key

    # ---------- (2.6.66) a window over another: two zones, one under the other ----------
    #  A window drawn as two parts (the Paperdoll with its bags under the doll)
    #  takes its own zone for the top part and the zone flush under it for the
    #  bottom part. pair_below finds that zone: the one the bottom window is in
    #  when it is flush under, else any window zone flush under (the bottom
    #  window is moved there), else one made for it: the free room under the
    #  zone (down to the next zone or the screen's edge), or, with no room, the
    #  zone split in two (PAIR_TOP_SHARE of its height on top). A frame layout
    #  changed this way is saved (Default as "Default (mine)", as the editor
    #  does). Nothing is made twice: a zone it can't make is left until the
    #  top window's zone changes.
    PAIR_TOP_SHARE = 0.46       # the top part's share of a zone split in two
    PAIR_MIN_H = 120            # the least height of a zone made under another

    def _flush_below(self, top, z):
        """Zone z sits flush under zone top (within SNAP_DIST), overlapping
        more than half of the narrower one's width."""
        if top is None or z is None or top is z or top.px is None or z.px is None:
            return False
        tx, ty, tw, th = top.px
        zx, zy, zw, zh = z.px
        if abs(zy - (ty + th)) > SNAP_DIST:
            return False
        ov = min(tx + tw, zx + zw) - max(tx, zx)
        return ov * 2 > min(tw, zw)

    def _free_under(self, zs, top, H):
        """The y where the free room under zone top ends: the first zone of any
        kind in its lane below it, or the screen's bottom. (2.6.81) A zone of
        the lane that starts higher and reaches below it (the arched Default's
        keep-clear zone starts at the crown) leaves no room at all."""
        tx, ty, tw, th = top.px
        lim = H
        for o in zs.zones:
            if o is top or o.px is None:
                continue
            ox, oy, ow, oh = o.px
            if oy + oh > ty + th and ox < tx + tw and tx < ox + ow:
                lim = min(lim, max(oy, ty + th))
        return lim

    def pair_below(self, top_key, bottom_key):
        """(top rect, bottom rect) in pixels: the zone holding window top_key and
        the zone flush under it for window bottom_key, made when there is none
        (bottom rect None when it can't be). None when top_key is in no zone.
        Client thread (a module's tick)."""
        if not self.loaded:
            return None
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return None
        zs = self.frames_in_use(W, H)
        top_key, bottom_key = str(top_key), str(bottom_key)
        tzid, bzid = self.zone_of(top_key), self.zone_of(bottom_key)
        tz = zs.by_id(tzid) if tzid else None
        bz = zs.by_id(bzid) if bzid else None
        if tz is None or tz.kind != "w" or tz.px is None:
            if bzid is not None:
                # the top window is free (dragged out of its zone, or freed): the
                # bottom one rides in it, so it is free too (its zone would count
                # as taken with nothing in it)
                self.assign_to(bottom_key, None, tell=False)
            return None
        if bz is not None and self._flush_below(tz, bz):
            return tz.px, bz.px
        moved = bz is not None
        # a window zone already flush under it: the bottom window goes there
        best = None
        for z in zs.zones:
            if z.kind == "w" and self._flush_below(tz, z):
                tx, ty, tw, th = tz.px
                ov = min(tx + tw, z.px[0] + z.px[2]) - max(tx, z.px[0])
                if best is None or ov > best[0]:
                    best = (ov, z)
        if best is not None:
            self.assign_to(bottom_key, best[1].id, tell=False)
            if moved:
                API.SysMsg('%s: %s rides in the %s window, so its zone is the one under it ("%s").'
                           % (APP_NAME, self.title_of(bottom_key), self.title_of(top_key), best[1].id),
                           Kit.HUE_INFO)
            return tz.px, best[1].px
        # none: one is made (once per zone; told in the journal)
        mark = (zs.name, tz.id, tuple(tz.px))
        if getattr(self, "pair_tried", None) == mark:
            return tz.px, None
        self.pair_tried = mark
        name = zs.name
        if zs.generated or name == LAYOUT_DEFAULT:
            # the Default is generated: drawn out as it is (every slot at its full
            # share, as the editor does) and kept as "Default (mine)"
            # 2.6.81: with the arch when it is on (as Layout.edit draws it out)
            zs = ZoneSet.default(W, H, (), False, self.unified and self.arch)
            zs.name, zs.generated = LAYOUT_MINE, False
            name = LAYOUT_MINE
            tz = zs.by_id(tz.id)
            if tz is None or tz.px is None:
                return None
        else:
            zs = zs.copy()                           # the one in use is left as it is
            tz = zs.by_id(tz.id)
        tx, ty, tw, th = tz.px
        room = self._free_under(zs, tz, H) - (ty + th)
        split = False
        if room >= max(ZONE_MIN_H, self.PAIR_MIN_H):
            nx, ny, nw, nh = tx, ty + th, tw, room
        elif th >= 2 * ZONE_MIN_H:
            split = True
            ht = max(ZONE_MIN_H, min(th - ZONE_MIN_H, int(round(th * self.PAIR_TOP_SHARE))))
            nx, ny, nw, nh = tx, ty + ht, tw, th - ht
        else:
            return tz.px, None
        nid = "%s bags" % tz.id
        if zs.by_id(nid) is not None:
            nid = zs.new_id()
        nz = Zone(nid, "w", (0, 0, 1, 1), "", (tz.min[0], self.PAIR_MIN_H), "d", tz.prio, tz.fit)
        if split:
            tz.set_px(tx, ty, tw, ht, W, H)
        nz.set_px(nx, ny, nw, nh, W, H)
        nz.note_pins(W, H)
        tz.note_pins(W, H)
        zs.zones.append(nz)
        self.save_frames(zs, name, W, H)
        if self.frames_name != name:
            self.use_frames(name, tell=False)
        else:
            self.frames, self.dirty = None, True
        self.assign_to(bottom_key, nid, tell=False)
        API.SysMsg('%s: zone "%s" made under "%s" for the bags%s; frame layout "%s" saved.' % (
            APP_NAME, nid, tz.id, " (the zone split in two)" if split else "", name), Kit.HUE_GOOD)
        zs2 = self.frames_in_use(W, H)
        t2, b2 = zs2.by_id(tz.id), zs2.by_id(nid)
        if t2 is None or b2 is None or t2.px is None or b2.px is None:
            return tz.px, nz.px
        return t2.px, b2.px

    def gump_of(self, key):
        w = self.wins.get(key)
        if w is None:
            return None
        try:
            g = w[0]()
        except Exception:
            return None
        return g if Kit.is_open(g) else None

    # ---------- the zones in use ----------
    def occupied(self):
        """The zones with a window on screen in them (a zone whose windows are
        closed is empty: it gives its room away until one opens)."""
        out = set()
        for zid, keys in self.assign.items():
            for key in keys:
                if self.gump_of(key) is not None:
                    out.add(zid)
                    break
        return out

    def frames_in_use(self, W, H):
        """The frame layout in use, with pixel rects for this screen (made
        again when the screen, the occupancy or the choice changed)."""
        if self.frames is not None and not self.dirty and self.screen == (W, H):
            return self.frames
        name = self.frames_name
        arch = self.unified and self.arch            # (2.6.72) the arched game view
        if name == LAYOUT_DEFAULT:
            zs = ZoneSet.default(W, H, self.occupied(), self.game_grows, arch)
        else:
            zs = self.load_frames(name, W, H)
            if zs is not None:
                self._repair_stretched(zs, W, H)     # (2.6.86) once
            if zs is None:
                self.frames_name = name = LAYOUT_DEFAULT
                Kit.put_var(FRAMES_ACTIVE, name)
                zs = ZoneSet.default(W, H, self.occupied(), self.game_grows, arch)
        if arch and getattr(zs, "ver", 1) < 2:
            try:
                self._arch_on(zs, W, H)              # (2.6.72) a layout saved before 2.6.74: guessed
            except Exception:
                pass
        try:
            self._overlap_shape(zs, W, H, arch)      # (2.6.74) Overlap and Top edge, as drawn
        except Exception as ex:
            self.debug_line("the overlapping zones couldn't be worked out: %s%s" % (ex, _error_where()))
        try:
            if arch:
                self._apply_hug(zs, W, H)            # (2.6.72) corner zones as wide as their window
        except Exception:
            pass
        self.frames, self.screen, self.dirty = zs, (W, H), False
        return zs

    def _arch_on(self, zs, W, H):
        """(2.6.72) With the arch ticked, any frame layout shaped like the Default
        (a keep-clear zone with window zones above it on the screen's top edge,
        as a saved "Default (mine)" is) gets it too, for this screen only (nothing
        is saved): the window zones over it hug their windows in its top corners
        and it runs up to the crown between them."""
        crown = max(10, int(round(ARCH_CROWN * H / 1080.0)))
        D = SNAP_DIST
        for k in zs.zones:
            if k.kind != "k" or k.px is None:
                continue
            kx, ky, kw, kh = k.px
            tops = [o for o in zs.zones if o.kind == "w" and o.px is not None
                    and o.px[1] <= D and abs(o.px[1] + o.px[3] - ky) <= D
                    and o.px[0] >= kx - D and o.px[0] + o.px[2] <= kx + kw + D]
            if len(tops) < 2 or ky <= crown:
                continue
            for o in tops:
                o.hug = True
            k.arch = True
            k.overlap = True                         # (2.6.74) it lies over its shoulders
            k.px = (kx, crown, kw, kh + ky - crown)

    def _overlap_shape(self, zs, W, H, arch_ok):
        """(2.6.74) The shape on this screen of every keep-clear zone with Overlap
        on (F1): Top edge arched (and the arch ticked, one frame on): the window
        zones its top overlaps are its shoulders (they hug their windows) and it
        runs up to the crown between them; otherwise it is cut out of the window
        zones it lies over, as a keep-clear zone always was. For this screen only
        (zs is the runtime copy); nothing is saved."""
        D = SNAP_DIST
        crown = max(10, int(round(ARCH_CROWN * H / 1080.0)))
        for k in zs.zones:
            if k.kind != "k" or not k.overlap or k.px is None:
                continue
            kx, ky, kw, kh = k.px
            over = [o for o in zs.zones if o.kind == "w" and o.px is not None and o is not k
                    and o.px[0] < kx + kw and kx < o.px[0] + o.px[2]
                    and o.px[1] < ky + kh and ky < o.px[1] + o.px[3]]
            if k.arch and arch_ok:
                tops = [o for o in over if o.px[1] <= ky + D]
                for o in tops:
                    o.hug = True
                if tops and ky < crown:
                    k.px = (kx, crown, kw, kh - (crown - ky))
                continue
            k.arch = False                           # straight (or the arch unticked)
            x, y, w, h = k.px
            for o in over:
                ox, oy, ow, oh = o.px
                if not (ox < x + w and x < ox + ow and oy < y + h and y < oy + oh):
                    continue
                cut, side = min([(x + w - ox, "R"), ((ox + ow) - x, "L"), (y + h - oy, "B"),
                                 ((oy + oh) - y, "T")])
                if side == "R":
                    w -= cut
                elif side == "L":
                    x, w = x + cut, w - cut
                elif side == "B":
                    h -= cut
                else:
                    y, h = y + cut, h - cut
                if w < ZONE_MIN_W or h < ZONE_MIN_H:
                    x, y, w, h = k.px
                    break
            k.px = (x, y, max(1, w), max(1, h))

    # ---------- (2.6.72) the game view follows the arched zone ----------
    #  With one frame on and the arch ticked, TazUO's game window is made the
    #  arched keep-clear zone's rect (from the crown, or its flat top, down to the
    #  Action Bar's zone): WorldViewportGump.SetGameWindowPosition and
    #  ResizeGameWindow, the place being the camera's less the viewport's border.
    #  Your own place and size are kept (GV_VAR, so a script that stopped without
    #  putting them back puts them back at its next start) and given back when the
    #  arch, one frame or the layout goes, and when Virtue Assistant stops.
    GV_VAR = "Layout_gameview_own"               # per character: "x,y,w,h" of your own game view
    GV_LOCK_VAR = "Layout_gameview_lock"         # (2.6.85) "0" / "1": your own game view's lock
    GV_MIN = (640, 480)                          # the client's smallest game window

    def _viewport(self):
        t = Tz.T("ClassicUO.Game.UI.Gumps.WorldViewportGump")
        return t, Tz.get(None, "Instance", t)

    def _vp_border(self):
        Typing._find()
        cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
        full = bool(Typing._get(cur, "GameWindowFullSize", default=False)) if cur is not None else False
        return 0 if full else 5                   # WorldViewportGump.BORDER_WIDTH

    def _vp_set(self, x, y, w, h):
        """Camera rect (x, y, w, h): the viewport's place is its border further out."""
        t, vp = self._viewport()
        b = self._vp_border()
        Tz.call(vp, "ResizeGameWindow", (ClientWin.point(w, h),), t)
        Tz.call(vp, "SetGameWindowPosition", (ClientWin.point(x - b, y - b),), t)

    def _vp_get(self):
        """Camera rect (x, y, w, h) of the game view now."""
        t, vp = self._viewport()
        f = ClientWin._bf[0]
        if f is None:
            from System.Reflection import BindingFlags
            f = ClientWin._bf[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetField(
                "_bounds", BindingFlags.Instance | BindingFlags.NonPublic)
        r = f.GetValue(vp)
        b = self._vp_border()
        return int(r.X) + b, int(r.Y) + b, int(r.Width) - 2 * b, int(r.Height) - 2 * b

    def _vp_full(self):
        Typing._find()
        cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
        return bool(Typing._get(cur, "GameWindowFullSize", default=False)) if cur is not None else False

    def _vp_chrome(self, on):
        """(2.6.85) The viewport's own border and resize button (private to the client's
        WorldViewportGump, which shows them again whenever it lays itself out: checked on
        every pass while fitted)."""
        t, vp = self._viewport()
        fs = getattr(self, "_vp_fields", None)
        if fs is None:
            from System.Reflection import BindingFlags
            fl = BindingFlags.Instance | BindingFlags.NonPublic
            fs = self._vp_fields = [t.GetField(n, fl) for n in ("_borderControl", "_button")]
        for f in fs:
            ctl = f.GetValue(vp) if f is not None else None
            if ctl is not None and bool(ctl.IsVisible) != bool(on):
                ctl.IsVisible = bool(on)

    def _vp_lock(self, locked):
        """(2.6.85) The client's own game window lock."""
        Typing._find()
        cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
        if cur is not None:
            Tz.put(cur, "GameWindowLock", bool(locked))
        t, vp = self._viewport()
        vp.CanMove = not locked

    def _game_view(self, zs, W, H):
        want = None
        if zs is not None and self.unified and self.arch and self.assign:
            for a in self.surround.arches(zs, W, H):
                top = self.surround.arch_top(a)
                want = (a[0], top, a[2], a[1] + a[3] - top)
                break
        # (2.6.85) Settings > Layout's "Fit the game view": the keep-clear zone is the
        # game view, with one frame or without, unless the client's own view is fullscreen
        if want is None and zs is not None and self.fit_view and self.assign and not self._vp_full():
            best = None
            for z in zs.zones:
                if z.kind == "k" and z.px is not None and z.px[2] > 2 and z.px[3] > 2:
                    if best is None or z.px[2] * z.px[3] > best[2] * best[3]:
                        best = z.px
            if best is not None:
                want = tuple(best)
        if want is not None and (want[2] < self.GV_MIN[0] or want[3] < self.GV_MIN[1]):
            if not getattr(self, "gv_small_told", False):
                self.gv_small_told = True
                API.SysMsg("%s: the game view would be %d x %d, under the client's "
                           "smallest (%d x %d); it is left as you set it." % (
                               APP_NAME, want[2], want[3], self.GV_MIN[0], self.GV_MIN[1]),
                           Kit.HUE_INFO)
            want = None
        if not getattr(self, "gv_checked", False):  # a game view left set by a stop that
            self.gv_checked = True                  # didn't put yours back: back now
            if want is None and Kit.get_var(self.GV_VAR, ""):
                self.game_view_restore()
                return
        if want == getattr(self, "gv_applied", None):
            if want is not None:                 # (2.6.85) the client shows them on any lay-out
                self._vp_chrome(False)
            return
        if want is None:
            self.game_view_restore()
            return
        if not Kit.get_var(self.GV_VAR, ""):
            own = self._vp_get()                 # your own game view, kept before the first change
            Kit.put_var(self.GV_VAR, "%d,%d,%d,%d" % own)
            Typing._find()
            cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
            lk = bool(Typing._get(cur, "GameWindowLock", default=False)) if cur is not None else False
            Kit.put_var(self.GV_LOCK_VAR, "1" if lk else "0")
        self._vp_set(*want)
        self._vp_chrome(False)
        self._vp_lock(True)
        self.gv_applied = want

    # ---------- (2.6.72) the ping readout ----------
    #  Settings > Layout's "Show your ping in the frame" (off by default): with one
    #  frame on, "Ping 54 ms" by the game area's top-right corner, read once a
    #  second from the client (AsyncNetClient.Socket.Statistics, as TazUO's own
    #  network stats read it): green under 100 ms, grey to 200, red above.
    PING_EVERY = 1.0

    def _ping_read(self):
        t = Tz.T("ClassicUO.Network.AsyncNetClient")
        sock = Tz.get(None, "Socket", t)
        stats = Tz.get(sock, "Statistics")
        src = str(Typing._get(stats, "CurrentPingSource", default="") or "")
        if src.endswith("Disabled"):
            return None
        return int(Tz.get(stats, "Ping"))

    def _ping_tick(self, zs, W, H):
        g = getattr(self, "ping_g", None)
        want = None
        if self.ping and self.unified and zs is not None and self.assign:
            for z in zs.zones:
                if z.kind == "k" and z.px is not None:
                    want = z
                    break
        if want is None:
            if g is not None:
                self.ping_g = None
                Kit.dispose(g)
            return
        now = time.time()
        if now < getattr(self, "ping_at", 0.0) and g is not None and Kit.is_open(g):
            return
        self.ping_at = now + self.PING_EVERY
        try:
            ms = self._ping_read()
            text = "Ping %d ms" % ms if ms is not None else "Ping: off"
            hue = Kit.HUE_INFO if ms is None else (
                Kit.HUE_GOOD if ms < 100 else (Kit.HUE_INFO if ms <= 200 else Kit.HUE_BAD))
        except Exception:
            text, hue = "Ping: can't be read", Kit.HUE_INFO
        x, y, w, h = want.px
        if want.arch:
            for a in self.surround.arches(zs, W, H):
                y = self.surround.arch_top(a)
                break
        # (2.6.82) the readout is one window as wide as its widest text, placed
        # once per zone place; a new number moves only the label inside it (no
        # window made again, and no label made to measure, every second)
        tw = Kit.text_px(text) + 8
        TW = getattr(self, "ping_tw", None)
        if TW is None:
            TW = self.ping_tw = Kit.text_px("Ping 9999 ms") + 8
        TW = max(TW, tw)
        px, py = max(0, x + w - TW - 2), max(0, y - Surround.GOLD_W - 1 - 18)
        lx = 4 + TW - tw                         # right-aligned as before
        if g is None or not Kit.is_open(g) or getattr(self, "ping_at_xy", None) != (px, py, TW):
            Kit.dispose(g)
            g = G.CreateGump(False, False)
            self.ping_lbl = Kit.add_label(g, text, lx, 1, hue)
            g.SetRect(px, py, TW + 40, 18)
            safe(lambda: g.SetAcceptMouseInput(False))
            safe(lambda: setattr(g, "CanCloseWithRightClick", False))
            safe(lambda: setattr(g, "CanMove", False))
            G.AddGump(g)
            SNAP.skip_gump(g)
            self.ping_g, self.ping_at_xy, self.ping_lx = g, (px, py, TW), lx
        else:
            Kit.set_text(self.ping_lbl, text, hue)
            if lx != getattr(self, "ping_lx", None):
                self.ping_lx = lx
                try:
                    self.ping_lbl.SetPos(lx, 1)
                except Exception:
                    pass

    def game_view_restore(self):
        """Your own game view back (when the layout set it); client thread."""
        self.gv_applied = None
        raw = Kit.get_var(self.GV_VAR, "")
        if not raw:
            return
        try:
            x, y, w, h = [int(v) for v in raw.split(",")]
            self._vp_set(x, y, w, h)
            if not self._vp_full():              # (2.6.85) its border and lock, as they were
                self._vp_chrome(True)
            lk = Kit.get_var(self.GV_LOCK_VAR, "")
            if lk:
                self._vp_lock(lk == "1")
        except Exception:
            return                               # tried again on the next pass
        Kit.put_var(self.GV_VAR, "")
        Kit.put_var(self.GV_LOCK_VAR, "")

    def _apply_hug(self, zs, W, H):
        """(2.6.72) Every hugging window zone holding a window whose hooks offer
        "hug" is made as wide as the window wants, in its corner: a zone in the
        screen's left half keeps its left edge, one in the right half its right
        edge. The room it gives up goes to the arched keep-clear zone beside it
        (the game view). (2.6.73) "hug" is fn(window height) -> the window's
        (width, height) (or a width alone): it is given the height the window has
        in the zone, and a height above it makes the zone that much taller, down
        over the game view (never past the screen's bottom), so a frame with
        Bandages or the Swing Bar under its bars holds them inside its box."""
        # (2.6.74) two passes: the insets a hugging zone's window grows by depend on
        # what its edges touch, and the hug itself changes that (an edge that touched
        # its neighbour faces the game view once the zone is narrower), so the sizes
        # are worked out again on the zones as hugged (2.6.73 used the first guess)
        orig = dict((z.id, z.px) for z in zs.zones if z.hug and z.px is not None)
        for _pass in (0, 1):
            for z in zs.zones:
                if not z.hug or z.px is None:
                    continue
                want = None
                for key in self.assign.get(z.id, []):
                    hooks = self.hooks.get(key) or {}
                    fn = hooks.get("hug")
                    g = self.gump_of(key) if fn is not None else None
                    if g is None:
                        continue
                    try:
                        gl, gt, gr, gb = self._grow(key, g, hooks, z, z.px, False, zs)
                        got = fn(orig[z.id][3] + gt + gb)
                        if isinstance(got, tuple):
                            ww, wh = int(got[0]), int(got[1] or 0)
                        else:
                            ww, wh = int(got), 0
                        want = (ww - gl - gr, (wh - gt - gb) if wh > 0 else 0)
                    except Exception:
                        want = None
                    if want and want[0] > 0:
                        break
                if not want or want[0] <= 0:
                    continue
                x, y, w, h = orig[z.id]
                nw = max(ZONE_MIN_W, min(w, want[0]))
                nh = max(h, min(want[1], H - y)) if want[1] > h else h
                if x + w / 2.0 < W / 2.0:
                    z.px = (x, y, nw, nh)
                else:
                    z.px = (x + w - nw, y, nw, nh)
        # (2.6.73) the corner zones of one band keep one height (the tallest), so the
        # arch between them stays mirrored when only one frame has a piece under it
        hz = [z for z in zs.zones if z.hug and z.px is not None]
        if len(hz) > 1:
            top = max(z.px[1] + z.px[3] for z in hz)
            for z in hz:
                x, y, w, h = z.px
                if y + h < top:
                    z.px = (x, y, w, top - y)

    def load_frames(self, name, W, H):
        """A saved frame layout for this screen: its variant for the ratio
        class, else the one drawn, reflowed (and the variant then saved)."""
        cls = ratio_class(W, H)
        var = FRAMES_NAMED % name
        zs = ZoneSet.parse(name, Kit.get_var(var + "@" + cls, ""))
        fresh = False
        if zs is None:
            zs = ZoneSet.parse(name, Kit.get_var(var, ""))
            fresh = True
        if zs is None:
            return None
        for zid in zs.skipped:
            HOST._tell('%s: zone "%s" in frame layout "%s" couldn\'t be read; skipped.'
                       % (APP_NAME, zid, name))
        zs.reflow(W, H, HOST.grid_size())
        if fresh and zs.zones:
            Kit.put_var(var + "@" + cls, zs.save_text())
        return zs

    def save_frames(self, zs, name, W, H):
        """Keep a drawn frame layout under `name`: as drawn (for other screens)
        and as this screen's variant; the name joins the list."""
        zs.name = name
        zs.screen = (W, H)
        zs.grid = HOST.grid_size()
        for z in zs.zones:
            z.note_pins(W, H)
        text = zs.save_text()
        Kit.put_var(FRAMES_NAMED % name, text)
        cls = ratio_class(W, H)
        for k in ("narrow", "wide", "ultrawide"):    # the other screens reflow it anew
            Kit.put_var((FRAMES_NAMED % name) + "@" + k, text if k == cls else "")
        names = self.frame_names()
        if name not in names:
            names.append(name)
            Kit.put_var(FRAMES_LIST, ",".join(names))
        self.page_refresh = True

    def use_frames(self, name, tell=True):
        """Pick the frame layout to use; zone ids the window layout names that
        it doesn't have are kept (they come back with their layout)."""
        if name != LAYOUT_DEFAULT and name not in self.frame_names():
            name = LAYOUT_DEFAULT
        self.frames_name = name
        Kit.put_var(FRAMES_ACTIVE, name)
        self.frames, self.dirty = None, True
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 else None
        if tell:
            free = 0
            if zs is not None:
                ids = set(zs.ids())
                free = sum(len(k) for zid, k in self.assign.items() if zid not in ids)
            API.SysMsg('%s: frame layout "%s" in use%s.' % (
                APP_NAME, name, ("; %d window%s had no zone and are free" % (free, "" if free == 1 else "s"))
                if free else ""), Kit.HUE_GOOD)
        self.page_refresh = True

    def remove_frames(self, name):
        if name == LAYOUT_DEFAULT:
            return False
        names = [n for n in self.frame_names() if n != name]
        Kit.put_var(FRAMES_LIST, ",".join(names))
        for cls in ("", "@narrow", "@wide", "@ultrawide"):
            Kit.put_var((FRAMES_NAMED % name) + cls, "")
        if self.frames_name == name:
            self.use_frames(LAYOUT_DEFAULT, tell=False)
        API.SysMsg('%s: frame layout "%s" deleted.' % (APP_NAME, name), Kit.HUE_GOOD)
        self.page_refresh = True
        return True

    # ---------- window layouts ----------
    def window_layout_text(self, name):
        if name == LAYOUT_DEFAULT:
            return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_DEFAULT)
        if name == LAYOUT_MIRRORED:
            return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_MIRRORED)
        return Kit.get_var(LAYOUT_NAMED % name, "")

    def use_windows(self, name, tell=True):
        """Put window layout `name` to use: every window in its zone ("" frees
        them all). The frame layout it was made for is put to use as well."""
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and name not in self.layout_names():
            name = ""
        frames, assign = self.parse_windows(self.window_layout_text(name)) if name else (self.frames_name, {})
        if name:                                     # (2.6.74) the layout places every window
            self.unfree(None)
        else:                                        # every window freed by you
            self.free_by_you(list(self.wins) + [k for ks in self.assign.values() for k in ks])
        self.layout_name = name
        Kit.put_var(LAYOUT_ACTIVE, name)
        self.assign = assign
        self.save_assign()
        self.free_scrolled()                         # windows no longer slotted: their own size
        self.placed = {}
        self.squeezed_told = set()
        # a saved window layout brings the frame layout it was made for; the
        # built-in two fit the frame layout in use (a zone it lacks is skipped)
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and frames != self.frames_name:
            self.use_frames(frames, tell=False)
        else:
            self.dirty = True
        if tell:
            if name:
                API.SysMsg('%s: window layout "%s" in use.' % (APP_NAME, name), Kit.HUE_GOOD)
            else:
                API.SysMsg("%s: every window is free; drop one on a zone to slot it."
                           % APP_NAME, Kit.HUE_GOOD)
        self.page_refresh = True

    def save_windows(self, name=None):
        """Save where every window sits now as window layout `name` (the one in
        use; a built-in one is saved as "<name> (mine)")."""
        name = name or self.layout_name or LAYOUT_MINE
        if name in (LAYOUT_DEFAULT, LAYOUT_MIRRORED):
            name = name + " (mine)"
        name = self.clean_name(name, LAYOUT_MINE)
        Kit.put_var(LAYOUT_NAMED % name, self.windows_text())
        names = self.layout_names()
        if name not in names:
            names.append(name)
            Kit.put_var(LAYOUT_LIST, ",".join(names))
        self.layout_name = name
        Kit.put_var(LAYOUT_ACTIVE, name)
        API.SysMsg('%s: window layout "%s" saved.' % (APP_NAME, name), Kit.HUE_GOOD)
        self.page_refresh = True

    def free_all(self):
        self.use_windows("", tell=True)

    def reset(self):
        self.use_windows(LAYOUT_DEFAULT, tell=True)

    def free_scrolled(self):
        """A window no longer slotted keeps no slot height: placed again at its
        own size (the scrollbar hides when it fits); a fitted one (2.6.56) gets
        back exactly what its module drew."""
        for key in [k for k in self.fitted if self.zone_of(k) is None]:
            self._unfit(key)
        for key, rect in list(self.placed.items()):
            if self.zone_of(key) is None:
                g = self.gump_of(key)
                info = Kit.scroll_info(g) if g is not None else None
                if info is not None:
                    try:
                        Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"])
                        Kit.moved_by_code(g)
                    except Exception:
                        pass
                self.placed.pop(key, None)

    # ---------- the pass (Snap.keep, the client thread) ----------
    def keep(self, W, H):
        """Place every slotted window whose place differs from its slot."""
        if not self.loaded or W <= 0 or H <= 0:
            return
        occ = self.occupied()
        if occ != self.occ:                          # a window opened or closed: the Default
            self.occ = occ                           # gives an empty slot's room away
            if self.frames_name == LAYOUT_DEFAULT:
                self.dirty = True
        zs = self.frames_in_use(W, H)
        if self.editor is not None:
            self.editor.keep(W, H)
        self.fresh = False
        self.fresh_adds.clear()
        Fill.prune()
        if self.fitted:                              # a window no longer in a zone: its own size
            for key in [k for k in self.fitted if self.zone_of(k) is None]:
                self._unfit(key)
        try:
            self._hold_journal(zs, H)                # (2.6.57) the client's journal: a reserved zone
        except Exception:
            pass
        try:
            self._client_drops()                     # (2.6.69) the World Map dragged on to a zone
        except Exception:
            pass
        try:
            self._arrange_tick(zs, W, H)             # (2.6.72) Arrange mode: outlines, idle end
        except Exception:
            pass
        now = time.time()
        if now >= self.repair_at and not SNAP.drag:
            self.repair_at = now + self.REPAIR_EVERY
            try:
                self._repair(zs)                     # (2.6.74) a standing rule now
            except Exception as ex:
                self.debug_line("the zone repair failed: %s%s" % (ex, _error_where()))
        if not self.assign:
            self.surround.sync(False, zs, W, H, set())   # (2.6.70) no windows in zones: none
            self._release(())
            try:
                self._game_view(None, W, H)          # (2.6.72) your own game view back
            except Exception:
                pass
            try:
                self._ping_tick(zs, W, H)            # 2.6.81: no windows in zones: the readout goes
            except Exception:
                pass
            return
        drag = SNAP.drag
        told = []
        seen = set()
        self.gump_key = {}
        for z in zs.zones:
            keys = self.assign.get(z.id)
            if not keys or z.kind != "w" or z.px is None:
                continue
            items = []
            for key in keys:
                g = self.gump_of(key)
                if g is None:
                    continue
                self.gump_key[g] = key
                if g in seen or g in SNAP.attached or not Snap.visible(g):
                    continue
                riding = (self.hooks.get(key) or {}).get("riding")
                if riding is not None:
                    try:                             # (2.6.66) rides in another window: its
                        if riding():                 # zone counts as taken, it is never placed
                            continue
                    except Exception:
                        pass
                seen.add(g)
                self._hold(g, key)                   # (2.6.72) locked in its zone
                if z.squeezed and key not in self.squeezed_told:
                    self.squeezed_told.add(key)
                    self._minimize(key)
                r = Snap.rect(g)
                if r is None:
                    if isinstance(g, ClientWin):     # (2.6.63) said once, not passed over silently
                        try:
                            g.rect()
                            why = "it has no size"
                        except Exception as ex:
                            why = Tz.why(ex)
                        g.fail["size"] = "its place and size couldn't be read (%s)" % why
                        g.report()
                    continue
                hooks = self.hooks.get(key) or {}
                # the window's extent: its rect with the windows attached to it (a tray
                # beside a bar, a grid under a title bar); they move along with it
                fol = [f for f in SNAP.followers(g) if Snap.visible(f)]
                ext = r
                for f in fol:
                    rf = Snap.rect(f)
                    if rf is not None:
                        x0, y0 = min(ext[0], rf[0]), min(ext[1], rf[1])
                        x1 = max(ext[0] + ext[2], rf[0] + rf[2])
                        y1 = max(ext[1] + ext[3], rf[1] + rf[3])
                        ext = (x0, y0, x1 - x0, y1 - y0)
                mini = False
                state = hooks.get("state")
                if state is not None:
                    try:
                        mini = state() == "minimized"
                    except Exception:
                        pass
                items.append((key, g, r, ext, fol, hooks, mini, self._base(key, g, ext, mini)))
            if not items:
                continue
            for it, slot in zip(items, self._art_slots(z, self._slots(z, items))):
                if it[1] in drag:
                    continue
                try:
                    if self._fit_slot(it, slot, z):  # (sets placed: the grown slot)
                        told.append(it[1])
                except Exception:
                    self.placed[it[0]] = slot
        self._release(seen)                          # (2.6.72) left its zone: its own CanMove
        try:                                         # (2.6.70) the one frame, when ticked
            self.surround.sync(self.unified, zs, W, H, seen)
        except Exception:
            pass
        try:
            self._game_view(zs, W, H)                # (2.6.72) the arched zone is the game view
        except Exception:
            pass
        if getattr(self, "need_due", False):         # (2.6.85) a window asked for more room
            self.need_due = False
            try:
                zs.reflow(W, H, HOST.grid_size())
                self._apply_hug(zs, W, H)
            except Exception:
                pass
        try:
            self._ping_tick(zs, W, H)                # (2.6.72) the ping readout, when ticked
        except Exception:
            pass
        if told:
            Kit.flush()                              # the places land before their modules look
            for g in told:
                fn = SNAP.moved_cb.get(g)
                if fn is not None:
                    try:
                        fn()                         # the module saves the slot as its place
                    except Exception:
                        pass

    # ---------- the slots (2.6.56) ----------
    #  Every window in a zone gets a slot, and the slots fill the zone edge to
    #  edge: down a zone that stacks down (or up) each window is as wide as
    #  the zone and has a share of its height; across one that stacks right
    #  (or left) each is as tall as the zone and has a share of its width. A
    #  minimized window keeps its bar's height (width) and the others share
    #  the rest by their own sizes, as first seen in the zone (so a window
    #  that refits never moves the others). The windows touch (no gap: a
    #  zone is filled, not dotted). Then each window is made exactly its
    #  slot's size (_fit_slot): its module fits it when its hooks offer
    #  "fit" (and "exact": True says the module makes it exactly that size),
    #  and the layout fits every other one (Fill), so a window never leaves
    #  its zone and never leaves part of it empty.
    def _base(self, key, g, ext, mini):
        """The window's own size for the shares: as first seen slotted (kept
        while it stays in a zone), a minimized one's bar as it is."""
        if mini:
            return ext[2], ext[3]
        b = self.base.get(key)
        if b is None:
            rec = Fill.recs.get(g)
            b = rec["nat"] if rec is not None else (ext[2], ext[3])
            self.base[key] = b
        return b

    def _art_slots(self, z, slots):
        """(2.6.87) The zone's windows share the room its dragons leave them."""
        if self.art != "dragons" or z.px is None:
            return slots
        W_, H_ = Kit.screen()
        zx, zy, zw, zh = z.px
        nx, ny, nw, nh = self.surround.art_slot(tuple(z.px), W_, H_)
        if nw == zw:
            return slots
        k = nw / float(zw)
        return [(nx + int((x - zx) * k), y, int(w * k), h) for (x, y, w, h) in slots]

    def _slots(self, z, items):
        """[(x, y, w, h)] for the windows of zone z, in the order given."""
        zx, zy, zw, zh = z.px
        down = z.stack in ("d", "u")
        along = zh if down else zw
        n = len(items)
        all_mini = all(it[6] for it in items)
        fixed = []
        weights = []
        for it in items:
            size = it[7][1] if down else it[7][0]
            if it[6] and not all_mini:
                fixed.append(max(1, min(int(size), along)))
                weights.append(0)
            else:
                fixed.append(None)
                weights.append(max(1, int(size)))
        free = along - sum(f for f in fixed if f is not None)
        total = sum(weights)
        if free < n or total <= 0:                   # bars alone overfill it: everyone shares
            fixed = [None] * n
            weights = [max(1, int(it[7][1] if down else it[7][0])) for it in items]
            free, total = along, sum(weights)
        lens = []
        left, left_w = free, total
        for f, wt in zip(fixed, weights):
            if f is not None:
                lens.append(f)
            else:
                share = int(round(left * float(wt) / left_w)) if left_w > 0 else left
                lens.append(max(1, share))
                left -= share
                left_w -= wt
        out = []
        pos = zy if z.stack == "d" else zy + zh if z.stack == "u" else zx if z.stack == "r" else zx + zw
        for ln in lens:
            if z.stack == "d":
                out.append((zx, pos, zw, ln))
                pos += ln
            elif z.stack == "u":
                pos -= ln
                out.append((zx, pos, zw, ln))
            elif z.stack == "r":
                out.append((pos, zy, ln, zh))
                pos += ln
            else:
                pos -= ln
                out.append((pos, zy, ln, zh))
        return out

    # (2.6.72) One inset. With one frame on, every zoned window's panels start
    # Kit.ZONE_INSET px in from its slot's edge (so the stone seam between two
    # zones, or two windows in a zone, is 2 x ZONE_INSET = Kit.GAP, the gap between
    # two sections in a window), and the stone border band's width more on an
    # outer edge of the surround (the screen's, the game area's). A Kit window
    # keeps Kit.MARGIN of (hidden) frame round its panels, so it is made that much
    # bigger than the panels' rect on each side; TazUO's World Map draws its map
    # its "inset" in from its edge. With one frame off nothing changes (the World
    # Map grows by its inset, 2.6.69).
    def _slot_insets(self, z, slot, zs=None):
        """(l, t, r, b): how far in from slot's edges the panels start (zs: the
        zones to measure against, the ones in use when None)."""
        ZI = Kit.ZONE_INSET
        zs = zs if zs is not None else self.frames
        if z is None or z.px is None or zs is None:
            return (ZI, ZI, ZI, ZI)
        zx, zy, zw, zh = z.px
        sx, sy, sw, sh = slot
        bt, bl, br, bb = self.surround.bands()
        W, H = self.screen if self.screen else Kit.screen()
        # (2.6.74) with one frame on the stone covers everything that isn't game view
        # (gaps between zones too: Surround.build), so an edge gets the border band
        # only where it faces the game view or lies on the screen's edge; against a
        # zone or a gap it is a plain seam. Each edge is looked at along its length:
        # the band when any real part of it (more than EDGE_SLACK px) faces the game.
        game = [o.px for o in zs.zones if o is not z and o.px is not None and o.kind == "k"]
        out = []
        for side, on_edge, lo, hi, at, horiz, band in (
                ("l", abs(sx - zx) <= 1, sy, sy + sh, sx - 1, False, bl),
                ("t", abs(sy - zy) <= 1, sx, sx + sw, sy - 1, True, bt),
                ("r", abs(sx + sw - zx - zw) <= 1, sy, sy + sh, sx + sw, False, br),
                ("b", abs(sy + sh - zy - zh) <= 1, sx, sx + sw, sy + sh, True, bb)):
            if not on_edge:                  # between two windows of one zone
                out.append(ZI)
                continue
            if at < 0 or (horiz and H > 0 and at >= H) or (not horiz and W > 0 and at >= W):
                out.append(band + ZI)        # the screen's edge
                continue
            n = 0
            for (ox, oy, ow, oh) in game:
                if horiz:
                    if oy <= at < oy + oh:
                        n += max(0, min(hi, ox + ow) - max(lo, ox))
                elif ox <= at < ox + ow:
                    n += max(0, min(hi, oy + oh) - max(lo, oy))
            out.append(band + ZI if n > self.EDGE_SLACK else ZI)
        return tuple(out)

    EDGE_SLACK = 8           # (2.6.74) px of an edge that may face the game and still be a seam

    def _grow(self, key, g, hooks, z, slot, mini=False, zs=None):
        """(l, t, r, b) px window g is made bigger than its slot on each side."""
        ins = int(hooks.get("inset") or 0)           # (2.6.69) drawn this far in from its edge
        if not self.unified:
            return (ins, ins, ins, ins)
        if isinstance(g, ClientWin):
            margin = ins
        elif Kit._frame_parts.get(g):
            margin = 8 if mini else Kit.MARGIN       # (a minimized bar's section is 8 px in)
        else:
            margin = int(hooks.get("margin") or 0)   # a window with a frame of its own making
        return tuple(margin - i for i in self._slot_insets(z, slot, zs))

    def _fit_slot(self, it, slot, z=None):
        """Make window it (as built in keep) exactly slot (x, y, w, h). True
        when it was placed or changed. (2.6.72) The slot is first grown by
        _grow (one frame on: the panels ZONE_INSET in from the zone's edges)."""
        key, g, r, ext, fol, hooks, mini, base = it
        gl, gt, gr, gb = self._grow(key, g, hooks, z, slot, mini)
        slot = (slot[0] - gl, slot[1] - gt, slot[2] + gl + gr, slot[3] + gt + gb)
        self.placed[key] = slot                      # what the window is made (layout_rect)
        sx, sy, sw, sh = slot
        fit_fn = hooks.get("fit")
        rec = self.fitted.get(key)
        ins = 0                                      # (2.6.72) in the grown slot already
        if fit_fn is not None:
            tw, th = sw + 2 * ins, sh + 2 * ins
            if fol and not hooks.get("pieces_out"):
                # (2.6.57) the room its attached windows leave it (the bar's tray)
                tw, th = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            told = rec.get("told") if rec is not None else None
            # a change of a few pixels from a follower's own size is no new slot
            # (else the bar and its tray could see-saw a pixel at a time); a client
            # window (2.6.63) is told every pass: it checks its own size and is put
            # back when the player, or the client, changed it
            if told is None or abs(told[0] - tw) > 4 or abs(told[1] - th) > 4 \
                    or (told != (tw, th) and (tw, th) == (sw, sh)) or hooks.get("client"):
                self.fitted[key] = rec = {"kind": "fit", "told": (tw, th)}
                try:
                    fit_fn(tw, th, "w")              # the module fits it (a rebuild, later)
                except Exception:
                    pass
        elif rec is None:
            self.fitted[key] = {"kind": "fill"}
        if hooks.get("exact"):
            # the module makes it the slot's size itself: it is moved to its slot (with
            # what is attached to it), its size left to it
            gx, gy = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
            if hooks.get("pieces_out"):
                # (2.6.57) the window itself fills its slot; what is attached to it
                # (the frames' bandage, swing and buff pieces) rides along outside it,
                # on the side its module put them (toward the game area)
                gx, gy = sx, sy
            gx, gy = gx - ins, gy - ins
            if isinstance(g, ClientWin):
                # (2.6.74) a zone smaller than the client lets the window be: its overflow
                # goes where it covers least (no window zone; then not the game view;
                # off the screen's edge before either), and the journal says once by how
                # much the zone is too small. 2.6.73 let the map hang over its neighbours.
                gx, gy = self._client_overflow(key, g, z, gx, gy, sw, sh, (gl, gt, gr, gb))
                self.client_target[key] = (gx, gy)   # (2.6.72) where a drag in Arrange starts from
            # (2.6.70) a window measured by the layout ("verify") that still isn't its
            # slot's size after MISFIT_FILL passes is stretched to it by the layout
            if fit_fn is not None and hooks.get("verify"):
                self._verify(key, g, r, rec, fit_fn, mini)
                fb = self.fallback.get(key)
                if fb is not None and not mini and not fol:
                    if fb != (sw, sh):
                        self.fallback.pop(key, None)     # a new slot: its module's turn again
                    else:
                        done = Fill.fit(g, sx, sy, sw, sh, hooks.get("fill") or "anchor")
                        if done is not None:
                            if done:
                                Kit.moved_by_code(g)
                            return bool(done)
            if (r[0], r[1]) == (gx, gy):
                return False
            Snap.move(g, gx, gy)
            Kit.moved_by_code(g)
            for f in fol:                            # in tow, as the keeper moves them
                pf = Snap.pos(f)
                if pf is not None:
                    Snap.move(f, pf[0] + gx - r[0], pf[1] + gy - r[1])
                    Kit.moved_by_code(f)
            return True
        if fol:
            # (2.6.57) windows are attached to it (the Action Bar's tray, a meter's
            # side window, the frames' pieces): the window itself is fitted to the
            # slot less the room they take beside it (pieces_out: the whole slot,
            # they ride outside it), then each is moved to keep its place beside
            # the window's new edges. 2.6.56 only moved such a window, so it never
            # filled its zone.
            if hooks.get("pieces_out"):
                lx, ly, lw, lh = sx, sy, sw, sh
            else:
                lx, ly = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
                lw, lh = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            if lw < 40 or lh < 20:                   # no room left for it: moved only (2.6.56)
                gx, gy = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
                if (r[0], r[1]) == (gx, gy):
                    return False
                Snap.move(g, gx, gy)
                Kit.moved_by_code(g)
                for f in fol:
                    pf = Snap.pos(f)
                    if pf is not None:
                        Snap.move(f, pf[0] + gx - r[0], pf[1] + gy - r[1])
                        Kit.moved_by_code(f)
                return True
            done = Fill.fit(g, lx, ly, lw, lh, hooks.get("fill") or "anchor")
            if done is None:                         # couldn't be fitted: moved to its place
                if (r[0], r[1]) == (lx, ly):
                    return False
                Snap.move(g, lx, ly)
                Kit.moved_by_code(g)
                for f in fol:
                    pf = Snap.pos(f)
                    if pf is not None:
                        Snap.move(f, pf[0] + lx - r[0], pf[1] + ly - r[1])
                        Kit.moved_by_code(f)
                return True
            nr = Snap.rect(g) or (lx, ly, lw, lh)
            for f in fol:
                rf = Snap.rect(f)
                if rf is None:
                    continue
                fx, fy = Fill.beside(rf, r, nr)
                if (rf[0], rf[1]) != (fx, fy):
                    Snap.move(f, fx, fy)
                    Kit.moved_by_code(f)
                    done = True
            if done:
                Kit.moved_by_code(g)
            return bool(done)
        done = Fill.fit(g, sx, sy, sw, sh, hooks.get("fill") or "anchor")
        if done is None:                             # couldn't be fitted: cut to its slot (2.6.54)
            Fill.unfit(g)
            info = Kit.scroll_info(g)
            fw, fh = (info["w"], info["h"]) if info is not None else (r[2], r[3])
            if (r[0], r[1]) == (sx, sy) and r[3] == min(fh, sh):
                return False
            Kit._place_raw(g, sx, sy, fw, fh, None, sh if fh > sh else None)
            done = True
        if done:
            Kit.moved_by_code(g)
        return bool(done)

    def _client_overflow(self, key, g, z, gx, gy, sw, sh, grow):
        """(2.6.74) (x, y) for client window g in slot (gx, gy, sw, sh) when its
        smallest size is bigger than the slot: of the places where it still covers
        its whole slot, the one whose overflow covers the least, by window zones
        first, then keep-clear zones, then the screen's outside."""
        try:
            mw, mh = g._min_size()
        except Exception:
            return gx, gy
        rw, rh = max(sw, mw), max(sh, mh)
        if rw <= sw and rh <= sh:
            return gx, gy
        zs = self.frames
        W, H = Kit.screen()
        if z is not None and z.px is not None and (key, z.id, z.px) != getattr(self, "small_said", None):
            self.small_said = (key, z.id, z.px)       # said once per zone and size
            API.SysMsg('%s: %s needs zone "%s" to be at least %d x %d; it is %d x %d.' % (
                APP_NAME, self.title_of(key), z.id, max(z.px[2], mw - grow[0] - grow[2]),
                max(z.px[3], mh - grow[1] - grow[3]), z.px[2], z.px[3]), Kit.HUE_BAD)
        ox, oy = rw - sw, rh - sh

        def cost(x, y):
            c = 0
            for o in (zs.zones if zs is not None else []):
                if o is z or o.px is None or o.kind == "r":
                    continue
                a = max(0, min(x + rw, o.px[0] + o.px[2]) - max(x, o.px[0])) * \
                    max(0, min(y + rh, o.px[1] + o.px[3]) - max(y, o.px[1]))
                c += a * (100 if o.kind == "w" else 10)
            on = max(0, min(x + rw, W) - max(x, 0)) * max(0, min(y + rh, H) - max(y, 0))
            return c + (rw * rh - on)
        best = None
        for fx in sorted(set((0, ox // 2, ox))):
            for fy in sorted(set((0, oy // 2, oy))):
                c = cost(gx - fx, gy - fy)
                if best is None or c < best[0]:
                    best = (c, gx - fx, gy - fy)
        return best[1], best[2]

    # (2.6.69) A window that lays itself out for its slot ("fit" + "exact") was
    # told its slot once, when the slot changed, and nothing ever looked at the
    # size it really came out: a rebuild that didn't land, a corner drag, or a
    # module that saw the same size twice and drew nothing left it at another
    # size for good (Ultima Tracker's groups, Meters). A window whose hooks say
    # "verify" is now measured on every keeper pass; when its size is not its
    # slot's for MISFIT_AGAIN passes in a row it is told again, with mode
    # "again" (draw yourself at this size even if it is the size you were told
    # before), and again after 4, 8, 16 ... passes. With Debug on, one journal line says
    # so if it still isn't right after MISFIT_TELL passes.
    MISFIT_SLACK = 2         # px a window may be off its slot's size (a frame's rounding)
    MISFIT_AGAIN = 2         # passes (of KEEP_EVERY s) before it is told again (then 4, 8 ...)
    MISFIT_TELL = 12         # passes before the journal line (Debug on)
    MISFIT_FILL = 8          # (2.6.70) passes before the layout stretches it to its slot itself

    def _verify(self, key, g, r, rec, fit_fn, it_mini=False):
        told = rec.get("told") if rec is not None else None
        if told is None:
            return
        if SNAP.drag:                                # (2.6.74) never told again mid-drag: a
            return                                   # window made anew loses the drop
        if it_mini:                                  # its minimized bar: its own size
            self.misfit.pop(key, None)
            return
        bad = abs(r[2] - told[0]) > self.MISFIT_SLACK or abs(r[3] - told[1]) > self.MISFIT_SLACK
        if not bad:
            self.misfit.pop(key, None)
            return
        n = self.misfit.get(key, 0) + 1
        self.misfit[key] = n
        if n == self.MISFIT_FILL and key not in self.fallback:
            self.fallback[key] = (int(told[0]), int(told[1]))   # (2.6.70) see _fit_slot
        if n >= self.MISFIT_AGAIN and n & (n - 1) == 0:     # 2, 4, 8, 16 ... passes: a window
            #                                              that can't be that size is never
            #                                              drawn again every second
            try:
                fit_fn(told[0], told[1], "again")
            except Exception:
                pass
        if n == self.MISFIT_TELL and HOST.debug:
            API.SysMsg('%s: %s stays %d x %d in zone "%s", not %d x %d.' % (
                APP_NAME, self.title_of(key), r[2], r[3], self.zone_of(key) or "?",
                told[0], told[1]), Kit.HUE_INFO)

    def _unfit(self, key):
        """Window `key` is no longer in a zone: a module that fitted it is told
        (None, None, None), and the layout's own fit is undone (every control
        back where its module put it, the window at its own size)."""
        rec = self.fitted.pop(key, None)
        self.base.pop(key, None)
        self.misfit.pop(key, None)
        self.fallback.pop(key, None)
        self.client_settle.pop(key, None)
        if rec is None:
            return
        hooks = self.hooks.get(key) or {}
        if rec.get("kind") == "fit":
            fn = hooks.get("fit")
            if fn is not None and rec.get("told") is not None:
                try:
                    fn(None, None, None)
                except Exception:
                    pass
        g = self.gump_of(key)
        if g is not None:
            Fill.unfit(g)

    def _minimize(self, key):
        """A squeezed zone: its windows go to their minimized bars (once)."""
        d = dict(HOST.docks).get(key)
        if d is None:
            return
        fn = d.get("minimize")
        if fn is not None:
            safe(fn)

    def report_fit(self):
        """(2.6.70) Settings > Layout's Check fit: one journal line per window in
        a zone, its place and size against its slot's."""
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        n = bad = 0
        ridden = []                                  # zones whose windows ride in another (bags)
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, [])
            rides = [safe((self.hooks.get(k) or {}).get("riding") or (lambda: False), False)
                     for k in keys]
            if keys and all(rides) and z.px is not None:
                ridden.append(z.px)
        for z in (zs.zones if zs is not None else []):
            for key in self.assign.get(z.id, []):
                g = self.gump_of(key)
                slot = self.placed.get(key)
                if g is None or slot is None:
                    continue
                r = Snap.rect(g)
                if r is None:
                    continue
                n += 1
                want = tuple(slot)                   # (2.6.72) placed is the grown slot
                ok = all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, want))
                for p in ridden:                     # it holds the windows of the zone by it
                    x0, y0 = min(want[0], p[0]), min(want[1], p[1])
                    u = (x0, y0, max(want[0] + want[2], p[0] + p[2]) - x0,
                         max(want[1] + want[3], p[1] + p[3]) - y0)
                    if all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, u)):
                        ok = True
                if not ok:
                    bad += 1
                API.SysMsg('%s: %s in "%s": %d x %d at %d, %d%s.' % (
                    APP_NAME, self.title_of(key), z.id, r[2], r[3], r[0], r[1],
                    "; fills it" if ok else "; its zone is %d x %d at %d, %d" % (
                        want[2], want[3], want[0], want[1])),
                    Kit.HUE_GOOD if ok else Kit.HUE_BAD)
                k, full = self.drawn_at(key, g)      # (2.6.78) a window drawn smaller
                if k < 0.995 and full is not None:
                    API.SysMsg('%s: %s is drawn at %d%% in zone "%s"; %d x %d shows it at 100%%.'
                               % (APP_NAME, self.title_of(key), int(round(k * 100)), z.id,
                                  full[0], full[1]), Kit.HUE_INFO)
        if not n:
            API.SysMsg("%s: no window sits in a zone." % APP_NAME, Kit.HUE_INFO)
        else:
            API.SysMsg("%s: %d of %d windows fill their zone; screen %d x %d (UI scale %.2f)." % (
                APP_NAME, n - bad, n, W, H, Kit.render_scale()), Kit.HUE_INFO)

    def drawn_at(self, key, g):
        """(2.6.78) (scale, (w, h) at 100%) of a zoned window: the module's own
        ("drawn_at" hook: fn() -> (k, (w, h))), else Fill's."""
        hooks = self.hooks.get(key) or {}
        fn = hooks.get("drawn_at")
        if fn is not None:
            got = safe(fn, None)
            if got:
                return got
        rec = Fill.recs.get(g)
        if rec is None or rec.get("k", 1.0) >= 0.995:
            return 1.0, None
        nw, nh = rec["nat"]
        return rec["k"], (int(nw), int(nh))

    def report_zones(self):
        """(2.6.74) Settings > Layout's Check zones: one journal line per listed
        window (its key, zone or free, open and visible, its state, being dragged,
        attached, held, CanMove, its rect against the slot it was given)."""
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        freed = self._freed()
        n = 0
        for key, title in self.all_windows():
            n += 1
            zid = self.zone_of(key)
            g = self.gump_of(key)
            bits = ['zone "%s"' % zid if zid else ("free (freed by you)" if key in freed else "free")]
            if zid and zs is not None and zs.by_id(zid) is None:
                bits.append("its zone isn't in this frame layout")
            if g is None:
                bits.append("closed")
            else:
                hooks = self.hooks.get(key) or {}
                vis = Snap.visible(g)
                st = safe(hooks["state"]) if hooks.get("state") else None
                bits.append(("visible" if vis else "hidden") + (", " + str(st) if st else ""))
                if g in SNAP.drag:
                    bits.append("being dragged")
                if g in SNAP.attached:
                    bits.append("attached to another window")
                if g in self.held:
                    bits.append("held")
                cm = safe(lambda: bool(g.CanMove), None) if not isinstance(g, ClientWin) else None
                if cm is not None:
                    bits.append("can move" if cm else "can't move")
                r = Snap.rect(g)
                slot = self.placed.get(key)
                bits.append(("at %d, %d, %d x %d" % tuple(r)) if r else "no rect")
                if slot is not None:
                    bits.append("slot %d, %d, %d x %d" % tuple(slot))
                if isinstance(g, ClientWin):
                    mw, mh = g._min_size()
                    bits.append("smallest %d x %d" % (mw, mh))
            API.SysMsg("%s: %s (%s): %s." % (APP_NAME, title, key, "; ".join(bits)), Kit.HUE_INFO)
        if not n:
            API.SysMsg("%s: no window is listed for the layout yet." % APP_NAME, Kit.HUE_INFO)
        else:
            API.SysMsg("%s: %d windows; frame layout \"%s\", window layout \"%s\"; Arrange %s." % (
                APP_NAME, n, self.frames_name, self.layout_name or "(none)",
                "on" if self.arrange else "off"), Kit.HUE_INFO)

    def look_problems(self):
        """(2.6.72) [(title, problem)] for every zoned window that breaks the
        one-frame look: a frame the one frame can't hide, a title row not drawn
        by Kit.title_bar, panels not ZONE_INSET in from the zone, title rows in a
        row of zones not on one y. For Check look (and the tests)."""
        out = []
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        if zs is None:
            return out
        rows = []                                    # (zone top, zone bottom, title y, title)
        for z in zs.zones:
            for key in self.assign.get(z.id, []):
                g = self.gump_of(key)
                slot = self.placed.get(key)
                if g is None or slot is None or isinstance(g, ClientWin):
                    continue
                t = self.title_of(key)
                hooks = self.hooks.get(key) or {}
                if hooks.get("riding") and safe(hooks["riding"], False):
                    continue
                if not Kit._frame_parts.get(g) and not hooks.get("margin"):
                    out.append((t, "its frame isn't one the one frame can hide"))
                r = Snap.rect(g)
                if r is not None and not all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, slot)):
                    out.append((t, "its panels aren't %d px in from its zone" % Kit.ZONE_INSET))
                ty = Kit._titled.get(g)
                st = (hooks.get("state") and safe(hooks["state"])) or "open"
                if ty is None:
                    if st == "open" and not hooks.get("untitled"):
                        out.append((t, "its title row isn't the standard one"))
                elif r is not None:
                    rows.append((slot[1], slot[1] + slot[3], r[1] + ty, t))   # (its slot's row)
                if st == "open" and r is not None:   # (2.6.78) its controls (Overlaps)
                    try:
                        info = Kit.scroll_info(g)
                        cw, ch = (info["w"], info["h"]) if info is not None else (r[2], r[3])
                        for why in Overlaps.lines(Overlaps.problems(g, cw, ch)):
                            out.append((t, why))
                    except Exception:
                        pass
        # (2.6.74) the seams: two windows side by side (or one over the other) in
        # zones that touch have Kit.GAP of stone between their panels
        panels = []
        T = Surround.TOUCH
        for z in zs.zones:
            for key in self.assign.get(z.id, []):
                g = self.gump_of(key)
                slot = self.placed.get(key)
                if g is None or slot is None or isinstance(g, ClientWin) or not Kit._frame_parts.get(g):
                    continue
                hooks = self.hooks.get(key) or {}
                if hooks.get("riding") and safe(hooks["riding"], False):
                    continue
                r = Snap.rect(g)
                if r is None:
                    continue
                m = Kit.MARGIN
                panels.append((self.title_of(key), (r[0] + m, r[1] + m, r[2] - 2 * m, r[3] - 2 * m),
                               slot))
        G_ = Kit.GAP
        for i, (ta, pa, sa) in enumerate(panels):
            for tb, pb, sb in panels[i + 1:]:
                for (t1, p1, s1), (t2, p2, s2) in (((ta, pa, sa), (tb, pb, sb)), ((tb, pb, sb), (ta, pa, sa))):
                    ov_y = min(p1[1] + p1[3], p2[1] + p2[3]) - max(p1[1], p2[1])
                    ov_x = min(p1[0] + p1[2], p2[0] + p2[2]) - max(p1[0], p2[0])
                    if ov_y > 0 and abs((s1[0] + s1[2]) - s2[0]) <= 2 * Kit.MARGIN + T:
                        seam = p2[0] - (p1[0] + p1[2])
                        if abs(seam - G_) > 1 and -40 < seam < 40:
                            out.append((t1, "its seam with %s is %d px, not %d" % (t2, seam, G_)))
                    if ov_x > 0 and abs((s1[1] + s1[3]) - s2[1]) <= 2 * Kit.MARGIN + T:
                        seam = p2[1] - (p1[1] + p1[3])
                        if abs(seam - G_) > 1 and -40 < seam < 40:
                            out.append((t1, "its seam with %s is %d px, not %d" % (t2, seam, G_)))
        for i, a in enumerate(rows):                 # zones side by side: one title y
            for b in rows[i + 1:]:
                if abs(a[0] - b[0]) <= SNAP_DIST and abs(a[1] - b[1]) <= SNAP_DIST \
                        and abs(a[2] - b[2]) > 1:
                    out.append((b[3], "its title row is %d px off %s's" % (b[2] - a[2], a[3])))
        return out

    def report_look(self):
        """(2.6.72) Settings > Layout's Check look: one journal line per zoned
        window that breaks the one-frame look, or one line saying none does."""
        if not self.unified:
            # (2.6.78) its controls are looked at all the same (overlaps, outside, cut)
            bad = self.control_problems()
            for t, why in bad:
                API.SysMsg("%s: %s: %s." % (APP_NAME, t, why), Kit.HUE_BAD)
            API.SysMsg("%s: one frame is off; tick Join zone windows in one frame first%s."
                       % (APP_NAME, "" if bad else " (no window in a zone has controls "
                          "over one another)"), Kit.HUE_INFO)
            return
        bad = self.look_problems()
        for t, why in bad:
            API.SysMsg("%s: %s: %s." % (APP_NAME, t, why), Kit.HUE_BAD)
        if not bad:
            API.SysMsg("%s: every window in a zone has the one-frame look." % APP_NAME,
                       Kit.HUE_GOOD)

    def control_problems(self):
        """(2.6.78) [(title, problem)]: Check look's control test (Overlaps) alone,
        for every open window in a zone."""
        out = []
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        for z in (zs.zones if zs is not None else []):
            for key in self.assign.get(z.id, []):
                g = self.gump_of(key)
                if g is None or isinstance(g, ClientWin):
                    continue
                hooks = self.hooks.get(key) or {}
                if hooks.get("riding") and safe(hooks["riding"], False):
                    continue
                st = (hooks.get("state") and safe(hooks["state"])) or "open"
                r = Snap.rect(g)
                if st != "open" or r is None:
                    continue
                try:
                    info = Kit.scroll_info(g)
                    cw, ch = (info["w"], info["h"]) if info is not None else (r[2], r[3])
                    for why in Overlaps.lines(Overlaps.problems(g, cw, ch)):
                        out.append((self.title_of(key), why))
                except Exception:
                    pass
        return out

    # ---------- a drop ----------
    def _map_zone(self):
        """(2.6.73) The zone id TazUO's World Map sits in, or None."""
        return self.zone_of("worldmap")

    # ---------- (2.6.74) the standing repair ----------
    #  2.6.72 freed a zoned window let go outside every zone in Arrange mode, and let
    #  a window join the World Map's zone; 2.6.73 put them back once, for its first
    #  20 s, and gave up silently on any error. Now it is a standing rule, looked at
    #  every REPAIR_EVERY s while a window layout is in use: a window that shares the
    #  map's zone, and an Ultima Tracker or Meters window, or TazUO's World Map, that
    #  is free while it has a zone it belongs to, goes back there, unless you freed it
    #  yourself (Settings > Layout's zone drop-down, Free all, or the window layout
    #  "(none)"; kept per character in FREED_VAR until you put it in a zone again).
    #  The zone it belongs to: the one it last sat in (HOMES_VAR) when that holds
    #  nothing but its own module's windows, else as _home_for finds. One journal
    #  line per window moved; a window with nowhere to go is told once a session.
    REPAIR_EVERY = 2.0
    REPAIR_KEYS = ("ultima.friend", "ultima.neutral", "ultima.foe", "ultima.combat", "meters",
                   "worldmap")
    FREED_VAR = "VirtueAssistant_layout_freed"   # per character: "key,key": freed by you
    HOMES_VAR = "VirtueAssistant_layout_homes"   # per character: "key=zone;...": last zones

    def _freed(self):
        if self.freed is None:
            self.freed = set(k for k in Kit.get_var(self.FREED_VAR, "").split(",") if k.strip())
        return self.freed

    def free_by_you(self, keys):
        """(2.6.74) Windows `keys` were freed by the player: the repair leaves them."""
        f = self._freed()
        n = len(f)
        f.update(str(k) for k in keys)
        if len(f) != n:
            Kit.put_var(self.FREED_VAR, ",".join(sorted(f)))

    def unfree(self, key=None):
        """(2.6.74) Window `key` (every window, key None) is the layout's again."""
        f = self._freed()
        if not f:
            return
        if key is None:
            f.clear()
        elif key in f:
            f.discard(key)
        else:
            return
        Kit.put_var(self.FREED_VAR, ",".join(sorted(f)))

    def _homes(self):
        if self.homes is None:
            self.homes = {}
            raw = Kit.get_var(self.HOMES_VAR, "")
            # the first run after 2.6.73: no homes known yet, so a free tracker or Meters
            # window is taken to belong in a zone (as 2.6.73's one-time repair did)
            self.migrating = not raw
            for part in raw.split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    if k.strip() and v.strip():
                        self.homes[k.strip()] = v.strip()
        return self.homes

    def _note_homes(self):
        """(2.6.74) Every window in a zone: that zone is its home (saved on change)."""
        h = self._homes()
        changed = False
        for zid, keys in self.assign.items():
            for k in keys:
                if h.get(k) != zid:
                    h[k] = zid
                    changed = True
        if changed:
            if len(h) > 64:
                for k in [k for k in h if self.zone_of(k) is None][:len(h) - 64]:
                    del h[k]
            Kit.put_var(self.HOMES_VAR, ";".join("%s=%s" % kv for kv in sorted(h.items())))

    def _repair(self, zs):
        if not self.assign:
            return                                   # no window layout in use: nothing belongs
        homes = self._homes()
        if not homes:
            self._note_homes()
        mz = self._map_zone()
        squat = [k for k in (self.assign.get(mz, []) if mz else []) if k != "worldmap"]
        freed = self._freed()
        todo = list(squat)
        listed = None
        for key in self.REPAIR_KEYS:
            if key not in self.wins or key in freed or key in squat or self.zone_of(key) is not None:
                continue
            # it belongs in a zone: it sat in one, the window layout in use lists it, its
            # module's other windows sit in zones, or (the first run) it is a tracker or Meters
            if listed is None:
                listed = set()
                if self.layout_name:
                    for ks in self.parse_windows(self.window_layout_text(self.layout_name))[1].values():
                        listed.update(ks)
            mod = key.split(".")[0]
            kin = any(k.split(".")[0] == mod for ks in self.assign.values() for k in ks)
            if key in homes or key in listed or (kin and key != "worldmap") \
                    or (getattr(self, "migrating", False) and key != "worldmap"):
                todo.append(key)
        changed = []
        for key in todo:
            if self.gump_of(key) is None:
                continue                             # closed: looked at again when it opens
            cur = self.zone_of(key)
            home = self._home_for(key, zs, mz)
            if home is None:
                if key not in self.repair_told and key != "worldmap":
                    self.repair_told.add(key)
                    API.SysMsg("%s: %s has no zone to go back to; drop it on one in Arrange mode."
                               % (APP_NAME, self.title_of(key)), Kit.HUE_INFO)
                if cur is None:
                    continue
            if cur is not None:
                self.assign[cur] = [k for k in self.assign[cur] if k != key]
                if not self.assign[cur]:
                    del self.assign[cur]
            if home is not None:
                self.assign.setdefault(home, []).append(key)
            self.placed.pop(key, None)
            rec = self.fitted.get(key)
            if rec is not None and rec.get("kind") == "fit":
                rec.pop("told", None)
            changed.append((key, home))
        if changed:
            self.save_assign()
            self.dirty = self.fresh = True
            self.page_refresh = True
            for key, home in changed:
                if home is not None:
                    API.SysMsg('%s: %s put back in zone "%s".' % (APP_NAME, self.title_of(key), home),
                               Kit.HUE_GOOD)
            self.free_scrolled()
            HOST.poke()

    def _home_for(self, key, zs, mz):
        """The zone window `key` goes back to (see _repair), or None."""
        wz = [z for z in zs.zones if z.kind == "w" and z.px is not None and z.id != mz]
        if key == "worldmap":                        # (2.6.74) the map: an empty zone only
            wz = [z for z in zs.zones if z.kind == "w" and z.px is not None
                  and not self.assign.get(z.id)]
        ids = set(z.id for z in wz)
        mod = key.split(".")[0]

        def kin_only(zid):
            return all(k.split(".")[0] == mod for k in self.assign.get(zid, []) if k != key)
        last = self._homes().get(key)                # (2.6.74) where it last sat
        if last in ids and kin_only(last):
            return last
        if key == "worldmap":
            return None                              # never a zone it didn't have
        sketch = {}
        for zid, keys in self.parse_windows(WINDOWS_DEFAULT)[1].items():
            for k in keys:
                sketch[k] = zid
        zid = sketch.get(key)
        if zid in ids and kin_only(zid):
            return zid
        empty = [z for z in wz if not self.assign.get(z.id)]
        kin = [z for z in wz if z.id in self.assign
               and any(k != key and k.split(".")[0] == mod for k in self.assign[z.id])]
        if kin:
            for kz in kin:                           # an empty zone in its row, touching
                kx, ky, kw, kh = kz.px
                for z in empty:
                    x, y, w, h = z.px
                    ov = min(y + h, ky + kh) - max(y, ky)
                    side = abs(x - (kx + kw)) <= SNAP_DIST or abs((x + w) - kx) <= SNAP_DIST
                    if side and ov * 2 > min(h, kh):
                        return z.id
            return kin[0].id
        if empty:
            r = Snap.rect(self.gump_of(key)) if self.gump_of(key) is not None else None
            cx, cy = (r[0] + r[2] / 2.0, r[1] + r[3] / 2.0) if r else (0.0, 0.0)
            empty.sort(key=lambda z: (z.px[0] + z.px[2] / 2.0 - cx) ** 2
                       + (z.px[1] + z.px[3] / 2.0 - cy) ** 2)
            return empty[0].id
        return None

    def _key_of(self, g):
        key = self.gump_key.get(g)
        if key is None:
            for k in self.wins:
                if self.gump_of(k) is g:
                    return k
        return key

    def _drop_zone(self, r):
        """The window zone a window let go at rect r goes into: the one under its
        centre, or one it covers more than half of; None: none (it is free)."""
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2
        hit = None                                   # the zone the window's centre is in
        covered = None                               # (area, zone): a zone it covers most of
        for z in self.frames.zones:
            if z.kind != "w" or z.px is None:
                continue
            x, y, w, h = z.px
            if hit is None and x <= cx < x + w and y <= cy < y + h:
                hit = z
            ow = min(x + w, r[0] + r[2]) - max(x, r[0])
            oh = min(y + h, r[1] + r[3]) - max(y, r[1])
            if ow > 0 and oh > 0 and ow * oh * 2 > w * h and (covered is None or ow * oh > covered[0]):
                covered = (ow * oh, z)
        if covered is not None:                      # an empty slot is a thin strip: a window
            hit = covered[1]                         # dropped over it is meant for it
        return hit

    def takes(self, g):
        """(2.6.70) Will window g, let go where it is now, be slotted in a zone
        (so it must not snap to its neighbours first)? Alt held: no."""
        try:
            if not self.loaded or self.frames is None or not self.arrange:
                return False                         # (2.6.72) only Arrange mode slots a drop
            if self._key_of(g) is None or safe(Follow.alt_held, False):
                return False
            r = Snap.rect(g)
            return r is not None and self._drop_zone(r) is not None
        except Exception:
            return False

    def debug_line(self, text, hue=None):
        """(2.6.74) One journal line, only with Debug on (the Modules tab)."""
        try:
            if HOST.debug:
                API.SysMsg("%s: %s." % (APP_NAME, text), Kit.HUE_INFO if hue is None else hue)
        except Exception:
            pass

    def _drop_said(self, key, r, hit, what):
        """(2.6.74) Debug: one line per drop (window, key, rect, zone, outcome)."""
        if not HOST.debug:
            return
        self.debug_line('drop: %s (%s) at %s on %s: %s' % (
            self.title_of(key) if key else "a window", key or "no key",
            ("%d, %d, %d x %d" % tuple(r[:4])) if r else "?",
            ('"%s"' % hit.id) if hit is not None else "no zone", what))

    def dropped(self, g, key=None, rect=None):
        """The player let go of window g after a drag (Snap.on_drop): with its
        centre inside a window zone it is slotted there; anywhere else it is
        free. Alt held: left where it is. (2.6.70) A window moved from one zone
        on to a zone holding one window swaps places with it (it used to squeeze
        in beside it, both at half size); the windows are fitted on the very
        next pass, not up to KEEP_EVERY later. (2.6.74) key / rect: a window
        made anew while it was dragged (Snap._tell_moved): the drop is of
        window `key` (its window now), let go at rect."""
        if not self.loaded or self.frames is None:
            return
        if key is None:
            key = self._key_of(g)
        else:
            g = self.gump_of(key)
            if g is None:
                self._drop_said(key, rect, None, "ignored (its window is closed)")
                return
        if key is None:
            self._drop_said(None, rect or Snap.rect(g), None, "ignored (not a window the layout knows)")
            return
        if not self.arrange:
            # (2.6.72) outside Arrange mode a drop changes nothing: a zoned window
            # (that the client let move anyway) goes back to its slot on the next pass
            if self.zone_of(key) is not None:
                self.fresh = self.dirty = True
                HOST.poke()
                self._drop_said(key, rect or Snap.rect(g), None, "back to its zone (Arrange is off)")
            return
        self.arrange_last = time.time()
        if safe(Follow.alt_held, False):
            self._drop_said(key, rect, None, "left where it is (Alt held)")
            return
        r = rect if rect is not None else Snap.rect(g)
        if r is None:
            self._drop_said(key, None, None, "ignored (its place can't be read)")
            return
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2
        hit = self._drop_zone(r)
        self.fresh = True                            # (2.6.70) fitted on the next pass
        if self.arrange_hot is not None:
            box = self.arrange_lit.get(self.arrange_hot)
            if box is not None:
                safe(lambda: setattr(box, "IsVisible", False))
            self.arrange_hot = None
        for f, l in list(SNAP.links.items()):        # (2.6.70) no snap link to or from it
            if f is g or l is g:
                SNAP.links.pop(f, None)
        old = self.zone_of(key)
        if hit is None:
            if old is None:
                self._drop_said(key, r, None, "stays free")
                return
            # (2.6.73) a window in a zone is never freed by a drop: let go outside
            # every zone it goes back to its own (2.6.72 freed it, and a tracker
            # dragged a little too far was left floating for good). Settings >
            # Layout's zone buttons free a window.
            self.dirty = True
            HOST.poke()
            self._drop_said(key, r, None, 'back to "%s"' % old)
            if not self.back_told:
                self.back_told = True
                API.SysMsg("%s: %s stays in its zone; drop it on another zone to move it "
                           "(Settings > Layout's zone buttons free a window)."
                           % (APP_NAME, self.title_of(key)), Kit.HUE_INFO)
            return
        if old == hit.id and len(self.assign.get(old, [])) <= 1:   # its own zone: put back
            self.dirty = True
            HOST.poke()
            self._drop_said(key, r, hit, "back to its own zone")
            return
        # (2.6.73) TazUO's World Map keeps a zone to itself: no window joins it there,
        # and the map goes only into an empty zone or swaps with a zone's one window
        mz = self._map_zone()
        others_there = [k for k in self.assign.get(hit.id, []) if k != key]
        lone = len(others_there) == 1 and self.gump_of(others_there[0]) is not None   # a swap
        if (key != "worldmap" and hit.id == mz and hit.id != old and (old is None or not lone)) \
                or (key == "worldmap" and others_there and (old is None or not lone)):
            self.dirty = True
            HOST.poke()
            self._drop_said(key, r, hit, "refused (the World Map's zone)")
            API.SysMsg("%s: TazUO's World Map keeps its zone to itself; drop %s on another zone."
                       % (APP_NAME, self.title_of(key) if key != "worldmap" else "it"),
                       Kit.HUE_BAD)
            return
        # (2.6.72) never into a zone smaller than the window can be made (TazUO's
        # World Map has a minimum): refused, with one journal line; nothing moves
        if old != hit.id and self._too_small(key, hit, g):
            self.dirty = True
            HOST.poke()
            self._drop_said(key, r, hit, "refused (the zone is too small)")
            return
        swap = None
        # 2.6.81: the slots of the zone dropped on, read before they are cleared
        # below, so the stack place is still found (a drag up within a zone)
        slots_was = dict((k, self.placed.get(k)) for k in self.assign.get(hit.id, []))
        if old is not None:
            # (2.6.70) from a zone on to a zone holding one open window: they swap
            # (2.6.71) never within one zone: a reorder there must keep both
            others = [k for k in self.assign.get(hit.id, []) if k != key] if old != hit.id else []
            if len(others) == 1 and self.gump_of(others[0]) is not None:
                swap = others[0]
                if self._too_small(swap, self.frames.by_id(old)):   # (2.6.72) swap guard
                    self.dirty = True
                    HOST.poke()
                    self._drop_said(key, r, hit, "refused (no room for %s in its zone)"
                                    % self.title_of(swap))
                    return
            # (2.6.72) the windows of both zones are fitted afresh on the next pass
            for k in list(self.assign.get(old, [])) + list(self.assign.get(hit.id, [])):
                rec = self.fitted.get(k)
                if rec is not None and rec.get("kind") == "fit":
                    rec.pop("told", None)            # told its new slot, even at the old size
                self.placed.pop(k, None)
            at = self.assign[old].index(key) if key in self.assign[old] else 0
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if swap is not None:
                self.assign[old].insert(min(at, len(self.assign[old])), swap)
                self.assign[hit.id] = [k for k in self.assign[hit.id] if k != swap]
                self.placed.pop(swap, None)
                self.squeezed_told.discard(swap)
            if not self.assign[old]:
                del self.assign[old]
        keys = self.assign.setdefault(hit.id, [])
        # where in the stack: by the centre's place along the zone's axis
        pos = len(keys)
        for i, k in enumerate(keys):
            p = slots_was.get(k) or self.placed.get(k)
            if p is None:
                continue
            if hit.stack in ("d", "u"):
                mid = p[1] + p[3] // 2
                before = cy < mid if hit.stack == "d" else cy > mid
            else:
                mid = p[0] + p[2] // 2
                before = cx < mid if hit.stack == "r" else cx > mid
            if before:
                pos = i
                break
        keys.insert(pos, key)
        self.unfree(key)                             # (2.6.74) in a zone: no longer freed by you
        self.save_assign()
        self.dirty = True
        self.squeezed_told.discard(key)
        self._drop_said(key, r, hit, "slotted" + ((" (%s went to \"%s\")" % (self.title_of(swap), old))
                                                  if swap is not None else ""))
        HOST.poke()

    def slots_for(self, z, keys):
        """(2.6.74) [(key, (x, y, w, h))] the slots windows `keys` would get in zone
        z (their own sizes as the layout knows them, else equal shares)."""
        items = []
        for k in keys:
            base = self.base.get(k)
            if base is None:
                g = self.gump_of(k)
                r = Snap.rect(g) if g is not None and not isinstance(g, ClientWin) else None
                base = (r[2], r[3]) if r else (100, 100)
            items.append((k, None, None, None, None, None, False, base))
        if not items or z is None or z.px is None:
            return []
        return list(zip(keys, self._slots(z, items)))

    def preview_text(self, key, z, keys=None, slots_fn=None):
        """(2.6.74) One line for the editor's Windows list and Settings > Layout:
        the size window `key` gets in zone z ("Meters: 304 x 412 here (shown at
        96%)"), or what it needs ("!" in front: it can't go there)."""
        if key is None or z is None or z.px is None:
            return ""
        t = self.title_of(key)
        if z.kind != "w":
            return "!%s can only go in a window zone." % t
        mz = self._map_zone()
        if (key != "worldmap" and z.id == mz and z.id != self.zone_of(key)) or \
                (key == "worldmap" and [k for k in self.assign.get(z.id, []) if k != key]):
            return "!TazUO's World Map keeps its zone to itself."
        mn = self._min_of(key)
        if mn and (z.px[2] < mn[0] or z.px[3] < mn[1]):
            return "!%s needs %d x %d at least; this zone is %d x %d." % (t, mn[0], mn[1], z.px[2], z.px[3])
        keys = [k for k in (keys if keys is not None else self.assign.get(z.id, [])) if k != key] + [key]
        slot = None
        if slots_fn is not None:
            for k, sl in slots_fn(z, keys):
                if k == key:
                    slot = sl
        if slot is None:
            for k, sl in self.slots_for(z, keys):
                if k == key:
                    slot = sl
        if slot is None:
            slot = z.px
        ZI = Kit.ZONE_INSET if self.unified else 0
        w, h = max(1, slot[2] - 2 * ZI), max(1, slot[3] - 2 * ZI)
        base = self.base.get(key)
        if base is None:
            g = self.gump_of(key)
            r = Snap.rect(g) if g is not None and not isinstance(g, ClientWin) else None
            base = (r[2], r[3]) if r else None
        shown = ""
        if base and base[0] > 0 and base[1] > 0:
            sc = min(1.0, float(w) / base[0], float(h) / base[1])
            if sc < 0.995:
                shown = " (shown at %d%%)" % int(round(sc * 100))
        return "%s: %d x %d here%s." % (t, w, h, shown)

    # ---------- the editor ----------
    def edit(self, fresh=False):
        """Open the zone editor on the frame layout in use (fresh: on a new one
        with a single zone in the middle of the screen)."""
        if self.editor is not None:
            return
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return
        if fresh:
            names = self.frame_names()
            n, name = 2, "Mine"
            while name in names or name == LAYOUT_DEFAULT:
                name = "Mine %d" % n
                n += 1
            zs = ZoneSet(name, [], HOST.grid_size(), (W, H))
            z = Zone("Zone 1", "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
            z.set_px((W - 320) // 2, (H - 240) // 2, 320, 240, W, H)
            zs.zones.append(z)
        elif self.frames_name == LAYOUT_DEFAULT:
            # as drawn: the bands as they are; (2.6.74) with the arch when it is on, so a
            # Default edited and saved keeps it (as its own Overlap and Top edge)
            zs = ZoneSet.default(W, H, self.occupied(), False, self.unified and self.arch)
            zs.generated = False
        else:
            # (2.6.74) the layout as drawn, not the copy in use (its corner zones narrowed
            # to their windows were saved that way); one saved before 2.6.74 gets its
            # guessed arch made its own
            zs = self.load_frames(self.frames_name, W, H) or self.frames_in_use(W, H).copy()
            if getattr(zs, "ver", 1) < 2 and self.unified and self.arch:
                try:
                    self._arch_on(zs, W, H)
                except Exception:
                    pass
        self.editor = LayoutEditor(self, zs, fresh)
        self.editor.open()

    def poll(self):
        """Every UI tick (the client thread): the editor's controls."""
        if self.editor is not None:
            self.editor.poll()

    def status_text(self):
        W, H = Kit.screen()
        step = HOST.grid_size()
        if W <= 0 or H <= 0:
            return "Screen: not known yet"
        return "Screen: %d x %d, %s; grid %d px, %d x %d squares" % (
            W, H, ratio_class(W, H), step, (W + step - 1) // step, (H + step - 1) // step)

    def close(self):
        if self.editor is not None:
            self.editor.close(keep=False, quiet=True)


class LayoutEditor(object):
    """Edit mode: every zone of the frame layout as a translucent Kit window on
    the real screen (stone frame, a colour fill, the zone's name and windows),
    dragged and resized with the machinery every window has (and, 2.6.74, by
    its edges); an editor window with the selected zone's settings and windows
    and the frame layout's own buttons.
    (2.6.74) A typed value is used only when you are done with it: Enter, the
    box losing focus, or Apply (Esc puts the boxes back); 2.6.73 applied every
    key, so typing 44 applied 4 first and said "no room" on the way. The ZONE
    rows are laid out by measuring and wrap; gaps and overlaps between zones are
    striped red and counted; Overlap, Top edge and Lock per zone; the zone's
    windows with a preview of their slots; values in squares or pixels; Undo /
    Redo (Ctrl+Z / Ctrl+Y); arrow keys nudge (Shift+arrows resize); Delete
    removes (press twice); Duplicate, Align and Same size (Shift+click picks
    more zones); New from Default, Mirror, Copy to; Save warns."""
    BAR_W = 720
    SETTLE = 0.3                 # seconds after the last resize step
    FIELD_W = 52
    ROW = 28
    UNDO_MAX = 50
    DEL_ARM = 3.0                # s within which a second Delete removes the zone
    HANDLE = 10                  # px: the edge handles' thickness
    KEYS = {"up": ("UP",), "down": ("DOWN",), "left": ("LEFT",), "right": ("RIGHT",),
            "delete": ("DELETE",), "z": ("Z",), "y": ("Y",),
            "enter": ("RETURN", "ENTER", "KP_ENTER"), "esc": ("ESCAPE", "ESC")}
    FIELDS = ("col", "row", "w", "h")

    def __init__(self, layout, zs, fresh):
        self.layout = layout
        self.zs = zs
        self.fresh = fresh
        self.frames = {}         # zone id -> {"g", "lbl", "sum", "resize_at", "size"}
        self.bar = None
        self.store = ({}, {})
        self.c = {}
        self.renames = {}          # (2.6.71) zone id when opened -> its id now
        self.sel = zs.zones[0].id if zs.zones else None
        self.multi = set()         # (2.6.74) zone ids picked with Shift+click (sel among them)
        self.grid_was = None
        self.fields = None       # (col, row, w, h) texts the zone has now (committed)
        self.name_text = None
        self.saveas_text = ""
        self.bar_pos = None
        self.rebuild = False
        self.closed = False
        self.W, self.H = Kit.screen()
        # (2.6.74)
        self.px_mode = False       # the boxes hold pixels (else grid squares)
        self.undo, self.redo = [], []
        self.keys_was = {}         # key name -> held at the last poll (edges only)
        self.focus_was = None      # which of the editor's boxes had focus at the last poll
        self.raws = {}             # box name -> its client control (focus)
        self.said = None           # the last refusal said (never twice in a row)
        self.del_armed = None      # (zone id, when) a first Delete
        self.marks = None          # the gaps / overlaps overlay
        self.marks_sig = None
        self.counts = (0, 0)       # (gaps, overlaps)
        self.handles = []          # [(gump, side, rect)] of the selected zone's edges
        self.handles_sig = None
        self.edge = None           # (zone id, side, mouse at start, px at start) while dragged
        self.edge_g = None         # the outline shown while an edge is dragged
        self.edge_at = 0.0
        self.pressed_was = False
        self.pick = 0              # the Windows drop-down's choice (0: none)
        self.pick_keys = []        # its keys, by index
        self.preview = ""          # the preview line under WINDOWS
        self.raws_ok = False       # the client's keyboard focus can be read

    # ---------- open / close ----------
    def open(self):
        self.grid_was = HOST.grid_shown()
        if not self.grid_was:
            safe(HOST.grid_toggle)
        for z in self.zs.zones:
            self.build_zone(z)
        self.build_bar()
        self.draw_marks()

    def close(self, keep, quiet=False):
        if self.closed:
            return
        self.closed = True
        for zid, fr in list(self.frames.items()):
            Kit.dispose(fr.get("g"))
        self.frames = {}
        Kit.dispose(self.bar)
        self.bar = None
        Kit.dispose(self.marks)
        self.marks = None
        self._drop_handles()
        Kit.dispose(self.edge_g)
        self.edge_g = None
        if self.grid_was is not None and HOST.grid_shown() != self.grid_was:
            safe(HOST.grid_toggle)
        self.layout.editor = None
        self.layout.dirty = True
        self.layout.page_refresh = True
        if not keep and not quiet:
            API.SysMsg("%s: the saved zones are back." % APP_NAME, Kit.HUE_INFO)

    # ---------- undo / redo ----------
    def _snap(self):
        return ([z.copy() for z in self.zs.zones], self.sel, dict(self.renames))

    def push(self):
        """Keep the zones as they are now, before a change (Undo brings them back)."""
        self.undo.append(self._snap())
        if len(self.undo) > self.UNDO_MAX:
            del self.undo[0]
        self.redo = []

    def _restore(self, snap):
        zones, sel, renames = snap
        for zid in list(self.frames):
            Kit.dispose(self.frames[zid].get("g"))
        self.frames = {}
        self.zs.zones = [z.copy() for z in zones]
        self.renames = dict(renames)
        self.sel = sel if self.zs.by_id(sel) is not None else (self.zs.zones[0].id if self.zs.zones else None)
        self.multi = set()
        for z in self.zs.zones:
            self.build_zone(z)
        self.rebuild = True

    def do_undo(self):
        if not self.undo:
            self.say("nothing to undo.", Kit.HUE_INFO)
            return
        self.redo.append(self._snap())
        self._restore(self.undo.pop())

    def do_redo(self):
        if not self.redo:
            self.say("nothing to redo.", Kit.HUE_INFO)
            return
        self.undo.append(self._snap())
        self._restore(self.redo.pop())

    def say(self, text, hue=None):
        """One journal line, never the same one twice in a row."""
        if text == self.said:
            return
        self.said = text
        API.SysMsg("%s: %s" % (APP_NAME, text), Kit.HUE_BAD if hue is None else hue)

    # ---------- zone frames ----------
    def _windows_in(self, z):
        """Titles of the windows the layout has in zone z (by its saved id)."""
        L = self.layout
        zid = self.orig_id(z.id)
        return [L.title_of(k) for k in L.assign.get(zid, [])]

    def orig_id(self, zid):
        """The id zone `zid` has in the saved layout (before a rename here)."""
        for was, now in self.renames.items():
            if now == zid:
                return was
        return zid

    def build_zone(self, z):
        old = self.frames.get(z.id, {}).get("g")
        x, y, w, h = z.px
        M = Kit.MARGIN
        fr = {"g": None, "resize_at": 0.0, "size": (w, h)}
        try:
            g = G.CreateModernGump(x, y, w, h, not z.lock, ZONE_MIN_W, ZONE_MIN_H, self._resized(z.id))
            safe(lambda: g.SetAlpha(0))
        except Exception:
            g = G.CreateGump(True, True)
        if z.lock:
            safe(lambda: setattr(g, "CanMove", False))
        Kit.add_window_frame(g, w, h, corners=False, mouse=False)
        Kit.add_box(g, M, M, w - 2 * M, h - 2 * M, ZONE_ALPHA, ZONE_COLORS.get(z.kind, "#FFFFFF"))
        self._draw_overlaps(g, z)
        if z.kind == "k":
            self._draw_game(g, z)
        if z.id == self.sel and self.pick:
            self._draw_preview(g, z)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        sel = z.id == self.sel or z.id in self.multi
        fr["lbl"] = Kit.add_label(g, Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * M - 24),
                                  M + 12, M + 7, Kit.HUE_TITLE if sel else Kit.HUE_TEXT)
        wins = self._windows_in(z) if z.kind == "w" else []
        fr["wins"] = Kit.add_label(g, Kit.fit(", ".join(wins), w - 2 * M - 24) if wins else "",
                                   M + 12, M + 30 + 6, Kit.HUE_TEXT)
        fr["sum"] = Kit.add_label(g, "", M + 12, M + 30 + 6 + (20 if wins else 0), Kit.HUE_INFO)
        Kit.catcher(g, M, M, w - 2 * M, 30, self._select(z.id),
                    "Click to select the zone (Shift+click: pick more); drag to move it "
                    "(it lands on the grid)" if not z.lock else
                    "Click to select the zone (Shift+click: pick more); it is locked", movable=not z.lock)
        Kit.place(g, x, y, w, h)
        G.AddGump(g)
        Kit.no_snap(g)                               # it snaps by the editor's own rule (snapped)
        safe(lambda: Kit.on_moved(g, self._moved(z.id)))
        fr["g"] = g
        self.frames[z.id] = fr
        self.update_zone(z)
        Kit.dispose(old)

    def _draw_overlaps(self, g, z):
        """(2.6.74) A hatched band where z lies over another zone (Overlap on)."""
        x, y, w, h = z.px
        for o in self.zs.zones:
            if o is z or o.px is None or not (z.overlap or o.overlap):
                continue
            ox, oy, ow, oh = o.px
            ax, ay = max(x, ox), max(y, oy)
            bx, by = min(x + w, ox + ow), min(y + h, oy + oh)
            if bx - ax < 4 or by - ay < 4:
                continue
            for sx in range(ax, bx, 12):             # stripes every 12 px
                Kit.add_box(g, sx - x, ay - y, min(4, bx - sx), by - ay, 0.45, "#E8C15A")

    def _draw_game(self, g, z):
        """(2.6.74) A keep-clear zone shows the game view as it will be: the gold
        line round it, and the arch's curve when its top edge is arched."""
        x, y, w, h = z.px
        gold = "#E8C15A"
        zs = self.zs.copy()
        try:
            self.layout._overlap_shape(zs, self.W, self.H, True)
        except Exception:
            pass
        k = zs.by_id(z.id)
        kx, ky, kw, kh = k.px if k is not None else z.px
        arch = None
        if k is not None and k.arch:
            for a in self.layout.surround.arches(zs, self.W, self.H):
                if tuple(a[:4]) == tuple(k.px):
                    arch = a
        dy = ky - y
        Kit.add_box(g, kx - x, ky - y + kh - 2, kw, 2, 0.9, gold)
        Kit.add_box(g, kx - x, dy, 2, kh, 0.9, gold)
        Kit.add_box(g, kx - x + kw - 2, dy, 2, kh, 0.9, gold)
        if arch is None or arch[7]:
            Kit.add_box(g, kx - x, dy, kw, 2, 0.9, gold)
            return
        run = arch[6]
        for side, sh in (("L", arch[4]), ("R", arch[5])):
            if sh is None:
                continue
            b = sh[2]
            xs = sh[1] + Kit.GAP if side == "L" else sh[0] - Kit.GAP
            for i in range(0, run + 1, 4):           # the S-curve, a dot every 4 px
                u = i / float(run)
                yy = int(round(b - Surround._ss(u) * (b - ky)))
                xx = xs + i if side == "L" else xs - i
                Kit.add_box(g, xx - x - 1, yy - y - 1, 3, 3, 0.9, gold)
        xl = (arch[4][1] + Kit.GAP + run) if arch[4] else kx
        xr = (arch[5][0] - Kit.GAP - run) if arch[5] else kx + kw
        if xr > xl:
            Kit.add_box(g, xl - x, ky - y, xr - xl, 2, 0.9, gold)

    def _slots_preview(self, z, keys):
        return self.layout.slots_for(z, keys)

    def _draw_preview(self, g, z):
        """(2.6.74) The picked window's slot (and those of the zone's windows) as
        filled boxes with their titles, as the layout will make them."""
        key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
        if key is None or z.kind != "w":
            return
        L = self.layout
        keys = [k for k in L.assign.get(self.orig_id(z.id), []) if k != key] + [key]
        x, y = z.px[0], z.px[1]
        ZI = Kit.ZONE_INSET if L.unified else 0
        for k, (sx, sy, sw, sh) in self._slots_preview(z, keys):
            col = "#E8C15A" if k == key else "#202020"
            Kit.add_box(g, sx - x + ZI, sy - y + ZI, max(1, sw - 2 * ZI), max(1, sh - 2 * ZI), 0.55, col)
            Kit.add_label(g, Kit.fit(L.title_of(k), max(20, sw - 16)), sx - x + 8, sy - y + sh - 26,
                          Kit.HUE_TEXT)

    def update_zone(self, z):
        fr = self.frames.get(z.id)
        if fr is None:
            return
        step = HOST.grid_size()
        x, y, w, h = z.px
        text = "%s, %d x %d squares" % (z.kind_name(), max(1, int(round(float(w) / step))),
                                        max(1, int(round(float(h) / step))))
        if z.overlap:
            text += ", overlaps"
        Kit.set_text(fr["sum"], Kit.fit(text, w - 2 * Kit.MARGIN - 24))
        Kit.set_text(fr["lbl"], Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * Kit.MARGIN - 24),
                     Kit.HUE_TITLE if (z.id == self.sel or z.id in self.multi) else Kit.HUE_TEXT)

    def _select(self, zid):
        def hit():
            shift = bool(safe(lambda: Client.key_held("shift"), False))
            if shift and self.sel is not None and zid != self.sel:
                if zid in self.multi:                # Shift+click again: un-picked
                    self.multi.discard(zid)
                else:
                    self.multi.add(zid)
                    self.multi.add(self.sel)
                self.rebuild = True
                HOST.poke()
                return
            if zid != self.sel or self.multi:
                self.multi = set()
                self.sel = zid
                self.pick = 0
                self.rebuild = True
                HOST.poke()
        return hit

    def _resized(self, zid):
        def hit(*args):
            fr = self.frames.get(zid)
            if fr is not None:
                fr["resize_at"] = time.time()
        return hit

    def _moved(self, zid):
        def hit():
            z = self.zs.by_id(zid)
            fr = self.frames.get(zid)
            if z is None or fr is None or not Kit.is_open(fr["g"]):
                return
            r = Snap.rect(fr["g"])
            if r is None:
                return
            if (r[0], r[1]) == (z.px[0], z.px[1]):
                return
            if z.lock:                               # locked: back where it was
                self.place_zone(z)
                self.say('zone "%s" is locked; click Lock to move it.' % z.id, Kit.HUE_INFO)
                return
            self.landed(z, r[0], r[1], z.px[2], z.px[3], resized=False)
        return hit

    def _blocker(self, z):
        """The first zone z may not overlap, or None."""
        hits = self.zs.overlaps(z)
        return hits[0] if hits else None

    def landed(self, z, x, y, w, h, resized=True):
        """A zone frame let go (or resized): on a screen anchor when near one,
        else each edge flush with the screen or a neighbour when near, else on
        its nearest grid line whatever the distance; a resize lands the size
        on whole squares; then clear of every zone it may not overlap, and
        placed."""
        W, H = self.W, self.H
        step = HOST.grid_size()
        if resized:
            w = max(ZONE_MIN_W, int(round(float(w) / step)) * step)
            h = max(ZONE_MIN_H, int(round(float(h) / step)) * step)
        w, h = min(w, W), min(h, H)
        best = None                                  # a screen anchor, within SNAP_ANCHOR
        for ax, ay in Kit.anchor_targets(w, h):
            d = max(abs(ax - x), abs(ay - y))
            if d <= SNAP_ANCHOR and (best is None or d < best[0]):
                best = (d, ax, ay)
        if best is not None:
            nx, ny = best[1], best[2]
        else:
            nx = ny = None
            for tx in (0, max(0, W - w)):            # flush with a screen edge
                if abs(tx - x) <= SNAP_DIST:
                    nx = tx
            for ty in (0, max(0, H - h)):
                if abs(ty - y) <= SNAP_DIST:
                    ny = ty
            for o in self.zs.zones:                  # flush with another zone frame
                if o is z or o.px is None:
                    continue
                ox, oy, ow, oh = o.px
                if nx is None and oy < y + h + SNAP_DIST and y < oy + oh + SNAP_DIST:
                    for tx in (ox + ow, ox - w, ox, ox + ow - w):
                        if abs(tx - x) <= SNAP_DIST:
                            nx = tx
                if ny is None and ox < x + w + SNAP_DIST and x < ox + ow + SNAP_DIST:
                    for ty in (oy + oh, oy - h, oy, oy + oh - h):
                        if abs(ty - y) <= SNAP_DIST:
                            ny = ty
            if nx is None:                           # hard to the grid, whatever the distance
                nx = int(round(float(x) / step)) * step
            if ny is None:
                ny = int(round(float(y) / step)) * step
        was = z.px
        self.push()
        z.set_px(nx, ny, w, h, W, H)
        if not self.zs.push_clear(z, W, H, step):
            z.set_px(was[0], was[1], was[2], was[3], W, H)   # no room there: as it was
            self.undo.pop()
            o = self._blocker(z)
            self.say('no room for zone "%s" there%s; it stays where it was.' % (
                z.id, (' (it would cover "%s")' % o.id) if o is not None else ""))
        z.note_pins(W, H)
        self.place_zone(z)
        self.changed()

    def changed(self):
        """After a change of the zones: the boxes, the marks and the counts."""
        self.fields = None                           # the boxes show the zone again
        self.show_fields()
        self.draw_marks()

    def place_zone(self, z):
        fr = self.frames.get(z.id)
        if fr is None:
            return
        x, y, w, h = z.px
        if (w, h) != fr["size"] or z.overlap or z.kind == "k" or any(o.overlap for o in self.zs.zones):
            self.build_zone(z)                       # the frame is drawn for its size (and bands)
            return
        try:
            Kit.place(fr["g"], x, y, w, h)
            Kit.moved_by_code(fr["g"])
        except Exception:
            pass
        self.update_zone(z)

    def keep(self, W, H):
        if (W, H) != (self.W, self.H):
            self.W, self.H = W, H
            self.zs.reflow(W, H, HOST.grid_size())
            for z in self.zs.zones:
                self.place_zone(z)
            self.draw_marks()

    # ---------- (2.6.74) gaps and overlaps ----------
    def gaps(self):
        """[rect] of the screen no zone covers (merged), and how many separate gaps."""
        W, H = self.W, self.H
        zs = [z.px for z in self.zs.zones if z.px is not None]
        xs = sorted(set([0, W] + [p[0] for p in zs] + [p[0] + p[2] for p in zs]))
        ys = sorted(set([0, H] + [p[1] for p in zs] + [p[1] + p[3] for p in zs]))
        xs = [v for v in xs if 0 <= v <= W]
        ys = [v for v in ys if 0 <= v <= H]
        nx, ny = len(xs) - 1, len(ys) - 1
        free = {}
        for j in range(ny):
            cy = (ys[j] + ys[j + 1]) / 2.0
            for i in range(nx):
                cx = (xs[i] + xs[i + 1]) / 2.0
                if not any(p[0] <= cx < p[0] + p[2] and p[1] <= cy < p[1] + p[3] for p in zs):
                    free[(i, j)] = True
        # separate gaps: groups of free cells that touch
        seen, n = set(), 0
        for cell in free:
            if cell in seen:
                continue
            n += 1
            stack = [cell]
            seen.add(cell)
            while stack:
                i, j = stack.pop()
                for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if nb in free and nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
        rects = []
        for j in range(ny):                          # runs along each row, merged down
            i = 0
            while i < nx:
                if (i, j) in free:
                    i0 = i
                    while i < nx and (i, j) in free:
                        i += 1
                    rects.append((xs[i0], ys[j], xs[i] - xs[i0], ys[j + 1] - ys[j]))
                else:
                    i += 1
        merged = []
        for r in rects:
            for k, m in enumerate(merged):
                if m[0] == r[0] and m[2] == r[2] and m[1] + m[3] == r[1]:
                    merged[k] = (m[0], m[1], m[2], m[3] + r[3])
                    break
            else:
                merged.append(r)
        return merged, n

    def bad_overlaps(self):
        """[(a, b, rect)]: zones over each other that may not be (no Overlap)."""
        out = []
        zones = self.zs.zones
        for i, a in enumerate(zones):
            for b in zones[i + 1:]:
                if a.px is None or b.px is None or b not in self.zs.overlaps(a):
                    continue
                if a in self.zs.overlaps(b) or not b.overlap:
                    x0, y0 = max(a.px[0], b.px[0]), max(a.px[1], b.px[1])
                    x1 = min(a.px[0] + a.px[2], b.px[0] + b.px[2])
                    y1 = min(a.px[1] + a.px[3], b.px[1] + b.px[3])
                    if x1 > x0 and y1 > y0:
                        out.append((a, b, (x0, y0, x1 - x0, y1 - y0)))
        return out

    def draw_marks(self):
        """A red stripe on every gap and every overlap that isn't allowed; the
        counts for the FRAME LAYOUT line. Drawn again only when the zones change."""
        sig = (self.W, self.H, tuple((z.id, z.kind, z.overlap, tuple(z.px or ())) for z in self.zs.zones))
        if sig == self.marks_sig and Kit.is_open(self.marks):
            return
        self.marks_sig = sig
        gaps, n = self.gaps()
        bad = self.bad_overlaps()
        counts = (n, len(bad))
        old, self.marks = self.marks, None
        Kit.dispose(old)
        if gaps or bad:
            g = G.CreateGump(False, False)
            for (x, y, w, h) in gaps:
                Kit.add_box(g, x, y, w, h, 0.45, "#C83030")
            for a, b, (x, y, w, h) in bad:
                Kit.add_box(g, x, y, w, h, 0.55, "#C83030")
            g.SetRect(0, 0, self.W, self.H)
            safe(lambda: g.SetAcceptMouseInput(False))
            safe(lambda: setattr(g, "CanMove", False))
            safe(lambda: setattr(g, "CanCloseWithRightClick", False))
            G.AddGump(g)
            SNAP.skip_gump(g)
            self.marks = g
        if counts != self.counts:
            self.counts = counts
            self.rebuild = True                      # the FRAME LAYOUT line

    # ---------- (2.6.74) the edge handles ----------
    def _drop_handles(self):
        for g, side, r in self.handles:
            Kit.dispose(g)
        self.handles = []
        self.handles_sig = None

    def _sync_handles(self):
        z = self.zs.by_id(self.sel) if self.sel else None
        fr = self.frames.get(z.id) if z is not None else None
        sig = (z.id, tuple(z.px), z.lock, fr.get("g") if fr else None) \
            if z is not None and z.px is not None else None
        if sig == self.handles_sig:
            return
        self._drop_handles()
        self.handles_sig = sig
        if z is None or z.lock:
            return
        x, y, w, h = z.px
        T = self.HANDLE
        L_ = max(24, min(80, w // 3))
        V_ = max(24, min(80, h // 3))
        for side, r in (("l", (x, y + (h - V_) // 2, T, V_)), ("r", (x + w - T, y + (h - V_) // 2, T, V_)),
                        ("t", (x + (w - L_) // 2, y + Kit.MARGIN + 30, L_, T)),
                        ("b", (x + (w - L_) // 2, y + h - T, L_, T))):
            g = G.CreateGump(True, False)
            Kit.add_box(g, 0, 0, r[2], r[3], 0.9, "#E8C15A")
            Kit.catcher(g, 0, 0, r[2], r[3], lambda: None,
                        "Drag to move this edge of the zone (it lands on the grid)")
            g.SetRect(r[0], r[1], r[2], r[3])
            safe(lambda: setattr(g, "CanCloseWithRightClick", False))
            G.AddGump(g)
            SNAP.skip_gump(g)
            self.handles.append((g, side, r))

    def _edge_tick(self, pressed):
        """While the button is held after it went down on an edge handle: an
        outline of the zone as it will be, with its size; let go: it lands."""
        now = time.time()
        if self.edge is None:
            if pressed and not self.pressed_was and self.handles:
                m = Kit.mouse_pos()
                if m is not None:
                    for g, side, r in self.handles:
                        if r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]:
                            z = self.zs.by_id(self.sel)
                            if z is not None:
                                self.edge = (z.id, side, m, tuple(z.px))
                            break
            return
        zid, side, m0, p0 = self.edge
        z = self.zs.by_id(zid)
        m = Kit.mouse_pos()
        if z is None or m is None:
            self.edge = None
            Kit.dispose(self.edge_g)
            self.edge_g = None
            return
        x, y, w, h = p0
        dx, dy = m[0] - m0[0], m[1] - m0[1]
        if side == "l":
            nx = min(x + w - ZONE_MIN_W, max(0, x + dx))
            x, w = nx, w + (x - nx)
        elif side == "r":
            w = max(ZONE_MIN_W, min(self.W - x, w + dx))
        elif side == "t":
            ny = min(y + h - ZONE_MIN_H, max(0, y + dy))
            y, h = ny, h + (y - ny)
        else:
            h = max(ZONE_MIN_H, min(self.H - y, h + dy))
        if pressed:
            if now - self.edge_at >= 0.05:
                self.edge_at = now
                step = HOST.grid_size()
                old, self.edge_g = self.edge_g, None
                Kit.dispose(old)
                g = G.CreateGump(False, False)
                for bx, by, bw_, bh in ((0, 0, w, 2), (0, h - 2, w, 2), (0, 0, 2, h), (w - 2, 0, 2, h)):
                    Kit.add_box(g, bx, by, bw_, bh, 0.95, "#E8C15A")
                t = "%d x %d squares (%d x %d)" % (max(1, int(round(float(w) / step))),
                                                    max(1, int(round(float(h) / step))), w, h)
                Kit.add_box(g, 6, 6, Kit.text_w(t) + 12, 22, 0.85, "#000000")
                Kit.add_label(g, t, 12, 8, Kit.HUE_TITLE)
                g.SetRect(x, y, w, h)
                safe(lambda: g.SetAcceptMouseInput(False))
                G.AddGump(g)
                SNAP.skip_gump(g)
                self.edge_g = g
            return
        self.edge = None                             # let go
        Kit.dispose(self.edge_g)
        self.edge_g = None
        if (x, y, w, h) != p0:
            self.landed_rect(z, x, y, w, h)

    def landed_rect(self, z, x, y, w, h):
        """(2.6.74) An edge let go: the edges on the grid, kept clear of the zones
        it may not cover (refused, with the zone in the way, when it would)."""
        step = HOST.grid_size()
        x0 = int(round(float(x) / step)) * step
        y0 = int(round(float(y) / step)) * step
        x1 = int(round(float(x + w) / step)) * step
        y1 = int(round(float(y + h) / step)) * step
        x1, y1 = min(x1, self.W), min(y1, self.H)
        if x + w >= self.W - SNAP_DIST:
            x1 = self.W
        if y + h >= self.H - SNAP_DIST:
            y1 = self.H
        self.apply_rect(z, x0, y0, max(ZONE_MIN_W, x1 - x0), max(ZONE_MIN_H, y1 - y0))

    def apply_rect(self, z, x, y, w, h, typed=None):
        """Put zone z at (x, y, w, h) when it covers no zone it may not: True;
        else one line naming the zone in the way, nothing moved: False."""
        W, H = self.W, self.H
        if w > W or h > H or x < 0 or y < 0 or x + w > W or y + h > H:
            self.say('zone "%s" can\'t be %s there: it would run off the screen; make it '
                     'smaller or move it.' % (z.id, typed or "that size"))
            return False
        was = z.px
        z.set_px(x, y, w, h, W, H)
        o = self._blocker(z)
        if o is not None:
            z.set_px(was[0], was[1], was[2], was[3], W, H)
            self.say('zone "%s" can\'t be %s there: it would cover "%s"; make it %s or move it.' % (
                z.id, typed or "that size", o.id,
                "shorter" if (h > was[3] and w <= was[2]) else "narrower" if w > was[2] else "smaller"))
            return False
        nw = z.px
        z.set_px(was[0], was[1], was[2], was[3], W, H)
        self.push()
        z.set_px(nw[0], nw[1], nw[2], nw[3], W, H)
        z.note_pins(W, H)
        self.said = None
        self.place_zone(z)
        self.changed()
        return True

    # ---------- the editor window ----------
    @staticmethod
    def _cap_w(cap):
        return 35 + Kit.text_w(cap)

    def _flow(self, g, store, items, x0, y, x_max):
        """(2.6.74) Captioned buttons laid out by measuring, left to right, 16 px
        apart, wrapping to a new row when the next one would pass x_max. items:
        (key, art, caption, tooltip). Returns the y of the last row."""
        x = x0
        for key, art, cap, tip in items:
            cw = self._cap_w(cap)
            if x > x0 and x + cw > x_max:
                x = x0
                y += self.ROW
            Kit.art_button(g, store, key, art, x, y - 2, cap, tip)
            x += cw + 16
        return y

    def build_bar(self):
        old = self.bar
        W = self.BAR_W
        M, GAP = Kit.MARGIN, Kit.GAP
        store = ({}, {})
        c = {}
        g = G.CreateGump(True, True)
        IW = W - 2 * M
        x_max = M + IW - 12
        z = self.zs.by_id(self.sel) if self.sel else None
        L = self.layout
        step = HOST.grid_size()
        # the ZONE section's rows, laid out first so its height is the rows drawn
        ops = []
        y1 = M + 30 + GAP
        ry = y1 + 32
        body = []                                    # (kind, ...) drawn once the height is known
        if z is None:
            body.append(("label", "No zone yet. Click Add zone, then drag it where you want it.",
                         M + 12, ry + 3, Kit.HUE_INFO))
            ry += self.ROW
        else:
            nx = M + 12 + Kit.text_w("Name:") + 8
            body.append(("label", "Name:", M + 12, ry + 3, None))
            body.append(("box", "name", z.id, nx, ry, 130, False,
                         "The zone's name (1 to 3 words, unique in this frame layout); Enter uses it"))
            items = [("kind", Kit.ART_PAGE, "Kind: " + z.kind_name(),
                      "Click for the next kind: window, keep clear, reserved"),
                     ("stack", Kit.ART_PAGE, "Stack: " + z.stack_name(),
                      "Click for the next direction windows stack in this zone"),
                     ("prio", Kit.ART_PAGE, "Shrinks: " + _ordinal(z.prio),
                      "Click to change when this zone shrinks to minimized bars on a small screen"),
                     ("overlap", Kit.ART_PAGE, "Overlap: " + ("on" if z.overlap else "off"),
                      "Click to let this zone lie over other zones (on) or keep it clear of them (off)")]
            if z.kind == "k" and z.overlap:
                items.append(("top", Kit.ART_PAGE, "Top edge: " + ("arched" if z.arch else "straight"),
                              "Click for the game view's top edge: arched round the zones it lies "
                              "over, or straight"))
            items += [("lock", Kit.ART_PAGE, "Lock: " + ("on" if z.lock else "off"),
                       "Click to lock the zone (it can't be moved or resized) or unlock it"),
                      ("dup", Kit.ART_OK, "Duplicate", "Add a copy of this zone beside it"),
                      ("remove", Kit.ART_CLOSE, "Remove", "Remove this zone (Delete twice does too); "
                       "its windows become free")]
            ops.append(("flow", items, nx + 130 + 16, ry))
            # the place and size: the boxes, in squares or pixels
            ry = self._flow_end(items, nx + 130 + 16, ry, x_max) + self.ROW
            fx = M + 12
            unit = "px" if self.px_mode else "squares"
            for key, label, tip in (("col", "Col:" if not self.px_mode else "X:",
                                     "The zone's left edge, in %s from the screen's left (0-%d)"),
                                    ("row", "Row:" if not self.px_mode else "Y:",
                                     "The zone's top edge, in %s from the screen's top (0-%d)"),
                                    ("w", "W:", "The zone's width in %s (1-%d)"),
                                    ("h", "H:", "The zone's height in %s (1-%d)")):
                hi = (self.W if key in ("col", "w") else self.H)
                if not self.px_mode:
                    hi = (hi + step - 1) // step
                body.append(("label", label, fx, ry + 3, None))
                fx += Kit.text_w(label) + 6
                body.append(("box", key, "", fx, ry, self.FIELD_W, True,
                             (tip % (unit, hi)) + "; Enter or Apply uses it, Esc puts it back"))
                fx += self.FIELD_W + 14
            ops.append(("flow", [("apply", Kit.ART_OK, "Apply",
                                  "Use the values typed in the boxes (Enter does too)"),
                                 ("units", Kit.ART_PAGE, "Units: " + unit,
                                  "Click to type the place and size in grid squares or in pixels")],
                        fx + 4, ry))
            ry = self._flow_end([("apply", None, "Apply", ""), ("units", None, "Units: " + unit, "")],
                                fx + 4, ry, x_max) + self.ROW
            c["px_y"] = ry + 3
            body.append(("px", M + 12, ry + 3))
            ry += 20
            pins = ", ".join(n for p, n in (("L", "left"), ("T", "top"), ("R", "right"), ("B", "bottom"),
                                            ("X", "centre"), ("Y", "middle")) if p in z.pins)
            body.append(("pins", "Pinned: " + (pins or "none"), M + 12, ry + 3))
            ry += 20
            ry += 8
            items = [("even", Kit.ART_PLAY, "Even out", "Give this zone and the zones flush beside it in "
                      "its row (or column) equal sizes, on the grid")]
            if len(self.multi) >= 2:
                items += [("al_l", Kit.ART_PLAY, "Align left", "Line the picked zones' left edges up with this zone's"),
                          ("al_t", Kit.ART_PLAY, "Align top", "Line the picked zones' top edges up with this zone's"),
                          ("al_r", Kit.ART_PLAY, "Align right", "Line the picked zones' right edges up with this zone's"),
                          ("al_b", Kit.ART_PLAY, "Align bottom", "Line the picked zones' bottom edges up with this zone's"),
                          ("same", Kit.ART_PLAY, "Same size", "Make the picked zones this zone's size")]
            ops.append(("flow", items, M + 12, ry))
            ry = self._flow_end(items, M + 12, ry, x_max) + self.ROW
            if len(self.multi) >= 2:
                body.append(("label", Kit.fit("%d zones picked (Shift+click picks more or fewer)."
                                              % len(self.multi), IW - 24), M + 12, ry + 3, Kit.HUE_INFO))
                ry += 20
        ZH = ry - y1 + 6
        # WINDOWS: the selected window zone's windows (F2)
        y2 = y1 + ZH + GAP
        wins_rows = []
        WH = 0
        if z is not None and z.kind == "w":
            wins_rows = list(L.assign.get(self.orig_id(z.id), []))
            WH = 30 + 28 + 26 * len(wins_rows) + (20 if self.preview else 0) + 14
            if not wins_rows:
                WH += 20
        y3 = y2 + (WH + GAP if WH else 0)
        cls = ratio_class(self.W, self.H)
        others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
        presets = [("undo", Kit.ART_PAGE, "Undo", "Undo the last change (Ctrl+Z)"),
                   ("redo", Kit.ART_PAGE, "Redo", "Redo the change undone (Ctrl+Y)"),
                   ("from_default", Kit.ART_PLAY, "New from Default", "Start these zones again from the Default layout"),
                   ("mirror", Kit.ART_PLAY, "Mirror", "Swap the zones left and right"),
                   ("copyto", Kit.ART_OK, "Copy to others",
                    "Use these zones on %s and %s screens too (save them first)" % tuple(others))]
        saved_other = [k for k in others if Kit.get_var((FRAMES_NAMED % self.zs.name) + "@" + k, "")]
        if saved_other:
            presets.append(("reflow", Kit.ART_PLAY, "Reflow from: " + saved_other[0],
                            "Rebuild these zones from the layout's %s-screen variant" % saved_other[0]))
            c["reflow_from"] = saved_other[0]
        prow = self._flow_end(presets, M + 12, 0, x_max)    # rows past the first, x ROW
        FH = 30 + 28 * 2 + prow + 20 * 3 + 10
        H = y3 + FH + M
        # ---- draw ----
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, IW, 30)
        Kit.add_label(g, "ZONES", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.add_label(g, Kit.fit('frame layout "%s"' % self.zs.name, IW - 250),
                      M + 30 + Kit.text_w("ZONES") + 12, M + 7, Kit.HUE_INFO)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                       "Close the editor and bring back the saved zones")
        Kit.add_section(g, M, y1, IW, ZH, "ZONE  (the selected one)")
        boxes = []
        for item in body:
            if item[0] == "label":
                Kit.add_label(g, item[1], item[2], item[3], item[4])
            elif item[0] == "box":
                key, text, bx, by, bw_, num, tip = item[1:]
                tb = Kit.add_textbox(g, text, bx, by, bw_, numbers=num)
                safe(lambda t=tip, b=tb: b.SetTooltip(t))
                c[key] = tb
                boxes.append(key)
            elif item[0] == "px":
                c["px"] = Kit.add_label(g, "", item[1], item[2], Kit.HUE_INFO)
                c["px_x"] = item[1]
            elif item[0] == "pins":
                lbl = Kit.add_label(g, item[1], item[2], item[3], Kit.HUE_INFO)
                safe(lambda: lbl.SetTooltip("Edges that stay on the screen's edge (or its centre "
                                            "line) when this layout is used on another screen size"))
        for op in ops:
            self._flow(g, store, op[1], op[2], op[3], x_max)
        if z is not None:
            self.name_text = z.id
        if WH:
            Kit.add_section(g, M, y2, IW, WH, "WINDOWS  (in this zone, top to bottom)")
            ry = y2 + 32
            Kit.add_label(g, "Window:", M + 12, ry + 3)
            dd_x = M + 12 + Kit.text_w("Window:") + 8
            dd_w = 300
            bx = dd_x + dd_w + 16
            Kit.art_button(g, store, "w_add", Kit.ART_OK, bx, ry - 2, "Put it here",
                           "Put the picked window in this zone now (no Arrange mode needed)")
            ry += 28
            if not wins_rows:
                Kit.add_label(g, "No window here yet. Pick one above, then click Put it here.",
                              M + 12, ry + 3, Kit.HUE_INFO)
                ry += 20
            for i, k in enumerate(wins_rows):
                Kit.add_label(g, Kit.fit(L.title_of(k), 300), M + 12, ry + 3)
                bx = M + 12 + 310
                Kit.art_button(g, store, "w_up_%d" % i, Kit.ART_PAGE, bx, ry - 2, "Up",
                               "Move %s up the zone's stack" % L.title_of(k))
                bx += self._cap_w("Up") + 16
                Kit.art_button(g, store, "w_down_%d" % i, Kit.ART_PAGE, bx, ry - 2, "Down",
                               "Move %s down the zone's stack" % L.title_of(k))
                bx += self._cap_w("Down") + 16
                Kit.art_button(g, store, "w_out_%d" % i, Kit.ART_CLOSE, bx, ry - 2, "Take out",
                               "Take %s out of the zone (it stays where it is, free)" % L.title_of(k))
                ry += 26
            c["wins_rows"] = wins_rows
            if self.preview:
                bad = self.preview.startswith("!")
                Kit.add_label(g, Kit.fit(self.preview.lstrip("!"), IW - 24), M + 12, ry + 3,
                              Kit.HUE_BAD if bad else Kit.HUE_INFO)
        # FRAME LAYOUT: the whole
        Kit.add_section(g, M, y3, IW, FH, "FRAME LAYOUT")
        ry = y3 + 32
        x = M + 12
        for key, art, cap, tip in (("add", Kit.ART_OK, "Add zone", "Add a zone in the middle of the screen; drag it where you want it"),
                                   ("fill", Kit.ART_PLAY, "Fill the gaps", "Grow every zone into the empty room beside it"),
                                   ("save", Kit.ART_OK, "Save", "Save these zones as the frame layout in use (Default is saved as Default (mine))"),
                                   ("saveas", Kit.ART_OK, "Save as", "Save these zones under the name in the box")):
            Kit.art_button(g, store, key, art, x, ry - 2, cap, tip)
            x += self._cap_w(cap) + 16
        c["saveas"] = Kit.add_textbox(g, self.saveas_text, x, ry,
                                      max(60, W - M - 12 - self._cap_w("Discard") - 16 - x), numbers=False)
        safe(lambda: c["saveas"].SetTooltip("A name for Save as (letters, digits, spaces)"))
        cap = "Discard"
        Kit.art_button(g, store, "discard", Kit.ART_CLOSE, W - M - 12 - self._cap_w(cap), ry - 2,
                       cap, "Close the editor and bring back the saved zones")
        ry += 28
        ry = self._flow(g, store, presets, M + 12, ry, x_max) + 28
        n = len(self.zs.zones)
        nk = sum(1 for zz in self.zs.zones if zz.kind == "k")
        nr = sum(1 for zz in self.zs.zones if zz.kind == "r")
        gaps, over = self.counts
        status = "%d zone%s, %d keep clear, %d reserved; %d gap%s, %d overlap%s; %d x %d, %s" % (
            n, "" if n == 1 else "s", nk, nr, gaps, "" if gaps == 1 else "s", over,
            "" if over == 1 else "s", self.W, self.H, cls)
        Kit.add_label(g, Kit.fit(status, IW - 24), M + 12, ry + 3,
                      Kit.HUE_BAD if (gaps or over) else Kit.HUE_INFO)
        ry += 20
        lx = M + 12                                  # the legend
        for col, name in ((ZONE_COLORS["w"], "window"), (ZONE_COLORS["k"], "keep clear"),
                          (ZONE_COLORS["r"], "reserved"), ("#C83030", "gap or overlap"),
                          ("#E8C15A", "overlap allowed")):
            Kit.add_box(g, lx, ry + 6, 12, 12, 0.9, col)
            Kit.add_label(g, name, lx + 16, ry + 3, Kit.HUE_INFO)
            lx += 16 + Kit.text_w(name) + 14
        ry += 20
        Kit.add_label(g, Kit.fit("Arrows nudge the zone a square; Shift+arrows resize it; Delete twice "
                                 "removes it.", IW - 24), M + 12, ry + 3, Kit.HUE_INFO)
        # the drop-down last: its list opens on top
        if WH:
            wl = L.all_windows()
            names = ["(pick a window)"]
            self.pick_keys = [None]
            for k, t in wl:
                zid = L.zone_of(k)
                names.append(Kit.fit(t + (' (in "%s")' % zid if zid else ""), 290))
                self.pick_keys.append(k)
            if self.pick >= len(names):
                self.pick = 0
            dd = G.CreateDropDown(dd_w, names, self.pick)
            dd.SetPos(dd_x, y2 + 32)
            g.Add(dd)
            safe(lambda: dd.SetTooltip("A window to put in this zone; the zone shows where it would sit"))
            c["w_pick"] = dd
        ax, ay = Kit.anchor_pos("B", W, H)
        x, y = self.bar_pos or Kit.load_pos(LAYOUT_EDITOR_POS, (ax or 200, ay or 200), (W, H))
        if Kit.is_open(old):
            x, y = old.GetX(), old.GetY()
        Kit.place(g, x, y, W, H)
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, self._bar_moved))
        self.bar, self.store, self.c = g, store, c
        self.raws = {}
        for key in boxes + ["saveas"]:
            raw = Kit.client_control(c[key]) if key in c else None
            if raw is not None:
                self.raws[key] = raw
        self.fields = None
        self.focus_was = None
        self.show_fields()
        Kit.dispose(old)

    def _flow_end(self, items, x0, y, x_max):
        """The y of the last row _flow would draw for items."""
        x = x0
        for it in items:
            cw = self._cap_w(it[2])
            if x > x0 and x + cw > x_max:
                x = x0
                y += self.ROW
            x += cw + 16
        return y

    @staticmethod
    def set_box(tb, text):
        try:
            tb.SetText(str(text))
        except Exception:
            safe(lambda: setattr(tb, "Text", str(text)))

    def _bar_moved(self):
        Kit.save_pos(LAYOUT_EDITOR_POS, self.bar)
        self.bar_pos = Snap.pos(self.bar)

    def _values(self, z):
        """The texts the boxes show for zone z (squares, or pixels)."""
        x, y, w, h = z.px
        if self.px_mode:
            return tuple(str(v) for v in (x, y, w, h))
        step = HOST.grid_size()
        return tuple(str(v) for v in (int(round(float(x) / step)), int(round(float(y) / step)),
                                      max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step)))))

    def show_fields(self):
        """The selected zone's place and size in the boxes, and the other unit."""
        c = self.c
        z = self.zs.by_id(self.sel) if self.sel else None
        if z is None or "col" not in c:
            return
        texts = self._values(z)
        if texts != self.fields:
            self.fields = texts
            for key, t in zip(self.FIELDS, texts):
                self.set_box(c[key], t)
        x, y, w, h = z.px
        if self.px_mode:
            step = HOST.grid_size()
            text = "%d x %d squares at square %d, %d" % (
                max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step))),
                int(round(float(x) / step)), int(round(float(y) / step)))
        else:
            text = "%d x %d px at %d, %d" % (w, h, x, y)
        Kit.set_text(c["px"], Kit.fit(text, self.BAR_W - Kit.MARGIN - 12 - c["px_x"]))

    # ---------- every UI tick ----------
    def _key(self, name):
        """True on the poll a key goes down (held keys don't repeat)."""
        down = False
        for k in self.KEYS[name]:
            try:
                if API.IsKeyPressed(k):
                    down = True
                    break
            except Exception:
                pass
        was = self.keys_was.get(name, False)
        self.keys_was[name] = down
        return down and not was

    def _focus(self):
        """Which of the editor's boxes holds the keyboard focus (or None)."""
        if not self.raws:
            return None
        try:
            Typing._find()
            f = Typing._get(None, "KeyboardFocusControl", Typing.uim) if Typing.uim is not None else None
        except Exception:
            f = None
        self.raws_ok = Typing.uim is not None
        n = 0
        while f is not None and n < 4:
            for key, raw in self.raws.items():
                if Typing._same(f, raw):
                    return key
            f = Typing._get(f, "Parent")
            n += 1
        return None

    def _box_texts(self):
        c = self.c
        try:
            return tuple(str(c[k].Text or "").strip() for k in self.FIELDS)
        except Exception:
            return None

    def poll(self):
        if self.closed:
            return
        if not Kit.is_open(self.bar):               # closed some other way: that is Discard
            self.close(keep=False)
            return
        now = time.time()
        for zid, fr in list(self.frames.items()):
            z = self.zs.by_id(zid)
            g = fr.get("g")
            if z is None or not Kit.is_open(g):
                continue
            if fr["resize_at"]:
                r = Snap.rect(g)
                if r is not None and (r[2], r[3]) != fr["size"]:
                    step = HOST.grid_size()           # (2.6.74) the size while it is dragged
                    Kit.set_text(fr["sum"], Kit.fit("%d x %d squares" % (
                        max(1, int(round(float(r[2]) / step))), max(1, int(round(float(r[3]) / step)))),
                        max(40, r[2] - 2 * Kit.MARGIN - 24)), Kit.HUE_TITLE)
                if now - fr["resize_at"] >= self.SETTLE:
                    fr["resize_at"] = 0.0
                    if r is not None and (r[2], r[3]) != fr["size"]:
                        if z.lock:
                            self.build_zone(z)
                        else:
                            self.landed(z, r[0], r[1], r[2], r[3], resized=True)
        pressed = SNAP.pressed() is True
        self._sync_handles()
        self._edge_tick(pressed)
        self.pressed_was = pressed
        store, c = self.store, self.c
        z = self.zs.by_id(self.sel) if self.sel else None
        if Kit.was_clicked(store, "close") or Kit.was_clicked(store, "discard"):
            self.close(keep=False)
            return
        focus = self._focus()
        typing = bool(safe(Typing.now, False))
        # keys: Enter / Esc for the boxes; the rest only while nothing is typed into
        enter = self._key("enter")
        esc = self._key("esc")
        if not typing and not self.edge:
            ctrl = bool(safe(lambda: Client.key_held("ctrl"), False))
            shift = bool(safe(lambda: Client.key_held("shift"), False))
            if self._key("z") and ctrl:
                self.do_undo()
            elif self._key("y") and ctrl:
                self.do_redo()
            elif z is not None:
                for name, d in (("left", (-1, 0)), ("right", (1, 0)), ("up", (0, -1)), ("down", (0, 1))):
                    if self._key(name):
                        self.nudge(z, d, shift)
                if self._key("delete"):
                    self.delete_pressed(z)
        if Kit.was_clicked(store, "add"):
            self.push()
            zid = self.zs.new_id()
            nz = Zone(zid, "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
            nz.set_px((self.W - 320) // 2, (self.H - 240) // 2, 320, 240, self.W, self.H)
            self.zs.zones.append(nz)
            if not self.zs.push_clear(nz, self.W, self.H, HOST.grid_size()):
                self.zs.zones.remove(nz)
                self.undo.pop()
                self.say("no room for another zone; remove one or make one smaller.")
                return
            nz.note_pins(self.W, self.H)
            self.sel, self.multi = zid, set()
            self.build_zone(nz)
            self.changed()
            self.rebuild = True
        elif Kit.was_clicked(store, "undo"):
            self.do_undo()
        elif Kit.was_clicked(store, "redo"):
            self.do_redo()
        elif Kit.was_clicked(store, "even") and z is not None:
            self.push()
            n = self.zs.even_out(z, self.W, self.H, HOST.grid_size())
            if n < 2:
                self.undo.pop()
                self.say("no zone sits flush beside this one in its row or column.")
            else:
                self._all_moved()
        elif Kit.was_clicked(store, "fill"):
            self.push()
            self.zs.fill_gaps(self.W, self.H, HOST.grid_size())
            self._all_moved()
        elif Kit.was_clicked(store, "save"):
            self.save(self.zs.name if self.zs.name != LAYOUT_DEFAULT else LAYOUT_MINE)
            return
        elif Kit.was_clicked(store, "saveas"):
            name = Layout.clean_name(safe(lambda: c["saveas"].Text, ""), "")
            if not name:
                self.say("type a name in the box, then click Save as.")
            else:
                self.save(name if name != LAYOUT_DEFAULT else LAYOUT_MINE)
                return
        elif Kit.was_clicked(store, "reflow") and c.get("reflow_from"):
            other = ZoneSet.parse(self.zs.name, Kit.get_var((FRAMES_NAMED % self.zs.name) + "@" + c["reflow_from"], ""))
            if other is not None:
                other.reflow(self.W, self.H, HOST.grid_size())
                self.push()
                # 2.6.81: fresh zones carry the saved ids again: no renames to carry over
                self._restore(([zz.copy() for zz in other.zones], self.sel, {}))
                self.changed()
        elif Kit.was_clicked(store, "from_default"):
            self.push()
            d = ZoneSet.default(self.W, self.H, (), False, self.layout.unified and self.layout.arch)
            self._restore(([zz.copy() for zz in d.zones], self.sel, {}))   # 2.6.81: ids anew
            self.changed()
        elif Kit.was_clicked(store, "mirror"):
            self.push()
            for zz in self.zs.zones:
                x, y, w, h = zz.px
                zz.set_px(self.W - x - w, y, w, h, self.W, self.H)
                zz.note_pins(self.W, self.H)
            self._all_moved()
        elif Kit.was_clicked(store, "copyto"):
            self.copy_to()
        elif Kit.was_clicked(store, "units"):
            self.commit_rect(z, quiet=True) if z is not None else None
            self.px_mode = not self.px_mode
            self.rebuild = True
        if z is not None and not self.rebuild:
            self.poll_zone(z, store)
        if z is not None and z.kind == "w" and not self.rebuild:
            self.poll_windows(z, store, c)
        if not self.rebuild:
            self.poll_fields(z, focus, enter, esc, Kit.was_clicked(store, "apply"))
        self.focus_was = focus
        self.draw_marks()
        if self.rebuild:
            self.rebuild = False
            self.saveas_text = str(safe(lambda: c["saveas"].Text, self.saveas_text) or "")
            for zz in self.zs.zones:
                self.update_zone(zz)
            self.build_bar()

    def _all_moved(self):
        for zz in self.zs.zones:
            zz.note_pins(self.W, self.H)
            self.place_zone(zz)
        self.changed()

    def poll_zone(self, z, store):
        """The ZONE section's buttons."""
        if Kit.was_clicked(store, "kind"):
            self.push()
            kinds = [k for k, n in ZONE_KINDS]
            z.kind = kinds[(kinds.index(z.kind) + 1) % len(kinds)]
            z.hug = z.hug and z.kind == "w"
            z.arch = z.arch and z.kind == "k"
            self.build_zone(z)
            self.changed()
            self.rebuild = True
        elif Kit.was_clicked(store, "stack"):
            self.push()
            stacks = [k for k, n in ZONE_STACKS]
            z.stack = stacks[(stacks.index(z.stack) + 1) % len(stacks)]
            self.rebuild = True
        elif Kit.was_clicked(store, "prio"):
            self.push()
            z.prio = (z.prio + 1) % (SHRINK_MAX + 1)
            self.rebuild = True
        elif Kit.was_clicked(store, "overlap"):
            self.push()
            z.overlap = not z.overlap
            if not z.overlap:
                z.arch = False
                if not self.zs.push_clear(z, self.W, self.H, HOST.grid_size()):
                    o = self._blocker(z)
                    self.say('zone "%s" still lies over "%s"; move it or make it smaller.'
                             % (z.id, o.id if o is not None else "a zone"), Kit.HUE_INFO)
                z.note_pins(self.W, self.H)
            for zz in self.zs.zones:
                self.build_zone(zz)
            self.changed()
            self.rebuild = True
        elif Kit.was_clicked(store, "top"):
            self.push()
            z.arch = not z.arch
            self.build_zone(z)
            self.rebuild = True
        elif Kit.was_clicked(store, "lock"):
            self.push()
            z.lock = not z.lock
            self.build_zone(z)
            self.rebuild = True
        elif Kit.was_clicked(store, "dup"):
            self.duplicate(z)
        elif Kit.was_clicked(store, "remove"):
            self.remove(z)
        else:
            for key, edge in (("al_l", "l"), ("al_t", "t"), ("al_r", "r"), ("al_b", "b"), ("same", "s")):
                if Kit.was_clicked(store, key):
                    self.align(z, edge)
                    break

    def poll_windows(self, z, store, c):
        """(2.6.74) The WINDOWS section: the pick, its preview, Put it here, and
        the zone's windows moved up, down or out."""
        L = self.layout
        dd = c.get("w_pick")
        now = time.time()
        add = Kit.was_clicked(store, "w_add")    # (2.6.83) first: a pick just changed keeps it
        if dd is not None and (now >= getattr(self, "_pick_next", 0.0)
                               or now - HOST.input_at <= HOST.INPUT_FAST):
            self._pick_next = now + 0.2          # (2.6.82) not every tick: 5 a second
            try:
                i = int(dd.GetSelectedIndex())
            except Exception:
                i = self.pick
            if i != self.pick:
                self.pick = i
                key = self.pick_keys[i] if 0 < i < len(self.pick_keys) else None
                self.preview = self.preview_text(key, z) if key else ""
                self.build_zone(z)
                self.rebuild = True
                if not add:
                    return
        zid = self.orig_id(z.id)
        if add:
            key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
            if key is None:
                self.say("pick a window in the list first, then click Put it here.", Kit.HUE_INFO)
                return
            if L.frames is None or L.frames.by_id(zid) is None:
                self.say('zone "%s" isn\'t saved yet; click Save, then put the window in it.' % z.id)
                return
            if L.zone_of(key) == zid:
                self.say("%s already sits in this zone." % L.title_of(key), Kit.HUE_INFO)
                return
            mz = L._map_zone()
            if (key != "worldmap" and zid == mz) or (key == "worldmap" and L.assign.get(zid)):
                self.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."
                         % (L.title_of(key) if key != "worldmap" else "it"))
                return
            if L._too_small(key, L.frames.by_id(zid)):
                return
            L.assign_to(key, zid)
            self.pick, self.preview = 0, ""
            self.build_zone(z)
            self.rebuild = True
            return
        rows = c.get("wins_rows") or []
        for i, k in enumerate(rows):
            for what in ("up", "down", "out"):
                if not Kit.was_clicked(store, "w_%s_%d" % (what, i)):
                    continue
                keys = L.assign.get(zid, [])
                if k not in keys:
                    break
                if what == "out":
                    L.assign_to(k, None)
                else:
                    j = keys.index(k)
                    t = j - 1 if what == "up" else j + 1
                    if 0 <= t < len(keys):
                        keys[j], keys[t] = keys[t], keys[j]
                        for kk in keys:
                            L.placed.pop(kk, None)
                            rec = L.fitted.get(kk)
                            if rec is not None and rec.get("kind") == "fit":
                                rec.pop("told", None)
                        L.save_assign()
                        L.dirty = L.fresh = True
                        HOST.poke()
                self.build_zone(z)
                self.rebuild = True
                return

    def preview_text(self, key, z):
        """(2.6.74) One line: the size window `key` would have in zone z, or what
        it needs; "!" in front when it can't go there."""
        return self.layout.preview_text(key, z, [k for k in self.layout.assign.get(self.orig_id(z.id), [])],
                                        self._slots_preview)

    # ---------- the boxes (2.6.74: used when you are done with them) ----------
    def poll_fields(self, z, focus, enter, esc, apply):
        c = self.c
        if z is None or "name" not in c:
            return
        left = self.focus_was if (self.focus_was is not None and focus != self.focus_was) else None
        if esc and (focus is not None or self._edited(z)):
            self.fields = None                       # the boxes back to the zone's values
            self.show_fields()
            self.set_box(c["name"], z.id)
            return
        if "name" in (focus, left) or apply:
            name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
            if (enter and focus == "name") or left == "name" or apply:
                if name != z.id:
                    self.rename(z, name)
                    return
        if focus is None and left is None and enter and not self.raws_ok:
            # the client's focus can't be read here: Enter uses whatever was typed
            name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
            if name != z.id:
                self.rename(z, name)
                return
            self.commit_rect(z)
            return
        if (enter and focus in self.FIELDS) or (left in self.FIELDS and focus not in self.FIELDS) or apply:
            self.commit_rect(z)

    def _edited(self, z):
        texts = self._box_texts()
        name = str(safe(lambda: self.c["name"].Text, z.id) or "").strip()
        return (texts is not None and texts != self._values(z)) or name != z.id

    def commit_rect(self, z, quiet=False):
        """The four boxes' values, used: the zone moved and sized, or refused with
        one line (the boxes then go back)."""
        texts = self._box_texts()
        if texts is None or texts == self._values(z):
            return
        try:
            col, row, w, h = [int(t) for t in texts]
        except Exception:
            if not quiet:
                self.say("type whole numbers in Col, Row, W and H.")
            self.fields = None
            self.show_fields()
            return
        step = 1 if self.px_mode else HOST.grid_size()
        x, y = max(0, col) * step, max(0, row) * step
        w, h = max(1, w) * step, max(1, h) * step
        typed = "%d x %d %s" % (max(1, int(texts[2])), max(1, int(texts[3])),
                                "px" if self.px_mode else "squares")
        if w < ZONE_MIN_W or h < ZONE_MIN_H:
            if not quiet:
                self.say('zone "%s" can\'t be %s: the smallest zone is %d x %d px.' % (
                    z.id, typed, ZONE_MIN_W, ZONE_MIN_H))
            self.fields = None
            self.show_fields()
            return
        if z.lock:
            self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO)
            self.fields = None
            self.show_fields()
            return
        if not self.apply_rect(z, x, y, w, h, typed):
            self.fields = None
            self.show_fields()

    def rename(self, z, name):
        name = Layout.clean_name(name, "")
        if not name or name.lower() == "frames" or self.zs.by_id(name) is not None:
            self.say('zone "%s" can\'t be called "%s": %s.' % (
                z.id, name, "a name needs letters or digits" if not name else
                "the name is taken" if self.zs.by_id(name) is not None else "that name is kept"))
            self.set_box(self.c["name"], z.id)
            return
        self.push()
        old = z.id
        z.id = name
        for k, v in self.renames.items():
            if v == old:
                self.renames[k] = name
                break
        else:
            self.renames[old] = name
        fr = self.frames.pop(old, None)
        if fr is not None:
            self.frames[name] = fr
        self.sel = name
        self.multi = set(name if m == old else m for m in self.multi)
        self.said = None
        self.build_zone(z)
        self.rebuild = True

    # ---------- (2.6.74) more ways to change zones ----------
    def nudge(self, z, d, resize):
        if z.lock:
            self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO)
            return
        step = HOST.grid_size()
        x, y, w, h = z.px
        if resize:
            self.apply_rect(z, x, y, max(ZONE_MIN_W, w + d[0] * step), max(ZONE_MIN_H, h + d[1] * step))
        else:
            self.apply_rect(z, x + d[0] * step, y + d[1] * step, w, h)

    def delete_pressed(self, z):
        now = time.time()
        if self.del_armed is not None and self.del_armed[0] == z.id and now - self.del_armed[1] <= self.DEL_ARM:
            self.del_armed = None
            self.remove(z)
            return
        self.del_armed = (z.id, now)
        API.SysMsg('%s: press Delete again to remove zone "%s".' % (APP_NAME, z.id), Kit.HUE_INFO)

    def remove(self, z):
        if z.lock:
            self.say('zone "%s" is locked; click Lock to remove it.' % z.id, Kit.HUE_INFO)
            return
        self.push()
        self.zs.zones = [zz for zz in self.zs.zones if zz is not z]
        fr = self.frames.pop(z.id, None)
        if fr is not None:
            Kit.dispose(fr.get("g"))
        self.multi.discard(z.id)
        self.sel = self.zs.zones[0].id if self.zs.zones else None
        self.changed()
        self.rebuild = True

    def duplicate(self, z):
        self.push()
        nz = z.copy()
        nz.id = self.zs.new_id()
        nz.lock = False
        step = HOST.grid_size()
        x, y, w, h = z.px
        nz.set_px(x + step, y + step, w, h, self.W, self.H)
        self.zs.zones.append(nz)
        if not nz.overlap and not self.zs.push_clear(nz, self.W, self.H, step):
            self.zs.zones.remove(nz)
            self.undo.pop()
            self.say("no room for a copy of zone \"%s\"; make room first." % z.id)
            return
        nz.note_pins(self.W, self.H)
        self.sel, self.multi = nz.id, set()
        self.build_zone(nz)
        self.changed()
        self.rebuild = True

    def align(self, z, edge):
        picked = [self.zs.by_id(i) for i in self.multi if i != z.id]
        picked = [p for p in picked if p is not None and not p.lock]
        if not picked:
            return
        self.push()
        x, y, w, h = z.px
        refused = []
        for p in picked:
            px, py, pw, ph = p.px
            if edge == "l":
                r = (x, py, pw, ph)
            elif edge == "t":
                r = (px, y, pw, ph)
            elif edge == "r":
                r = (x + w - pw, py, pw, ph)
            elif edge == "b":
                r = (px, y + h - ph, pw, ph)
            else:
                r = (px, py, w, h)
            was = p.px
            p.set_px(r[0], r[1], r[2], r[3], self.W, self.H)
            if self._blocker(p) is not None:
                p.set_px(was[0], was[1], was[2], was[3], self.W, self.H)
                refused.append(p.id)
            p.note_pins(self.W, self.H)
        if refused:
            self.say("%s would cover another zone, so %s stayed where %s %s." % (
                ", ".join('"%s"' % r for r in refused), "it" if len(refused) == 1 else "they",
                "it" if len(refused) == 1 else "they", "was" if len(refused) == 1 else "were"),
                Kit.HUE_INFO)
        self._all_moved()

    def copy_to(self):
        name = self.zs.name
        if self.zs.generated or name == LAYOUT_DEFAULT or name not in self.layout.frame_names():
            self.say("save these zones first (Save or Save as), then click Copy to.", Kit.HUE_INFO)
            return
        cls = ratio_class(self.W, self.H)
        zs = self.zs.copy(name)
        zs.screen = (self.W, self.H)
        zs.grid = HOST.grid_size()
        for zz in zs.zones:
            zz.note_pins(self.W, self.H)
        text = zs.save_text()
        others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
        for k in others:
            Kit.put_var((FRAMES_NAMED % name) + "@" + k, text)
        API.SysMsg('%s: frame layout "%s" copied to %s screens.' % (APP_NAME, name, " and ".join(others)),
                   Kit.HUE_GOOD)

    def warnings(self):
        """(2.6.74) The lines Save gives about these zones (it saves anyway)."""
        out = []
        L = self.layout
        for z in self.zs.zones:
            if z.kind != "w" or z.px is None:
                continue
            for k in L.assign.get(self.orig_id(z.id), []):
                mn = L._min_of(k)
                if mn and (z.px[2] < mn[0] or z.px[3] < mn[1]):
                    out.append('zone "%s" is %d x %d, smaller than %s can be (%d x %d)' % (
                        z.id, z.px[2], z.px[3], L.title_of(k), mn[0], mn[1]))
        gaps, over = self.counts
        if gaps:
            out.append("the zones leave %d gap%s (Fill the gaps closes them)" % (gaps, "" if gaps == 1 else "s"))
        if over:
            out.append("%d overlap%s of zones without Overlap on" % (over, "" if over == 1 else "s"))
        if not any(z.kind == "k" for z in self.zs.zones):
            out.append("no keep-clear zone: nothing marks the game view")
        return out

    def save(self, name):
        for w in self.warnings():
            API.SysMsg("%s: note: %s." % (APP_NAME, w), Kit.HUE_INFO)
        zs = self.zs.copy(name)
        zs.generated = False
        zs.ver = 2
        self.layout.save_frames(zs, name, self.W, self.H)
        # (2.6.71) the windows of a renamed zone go with it
        L, moved = self.layout, False
        for was, now in self.renames.items():
            if was != now and was in L.assign and now not in L.assign:
                L.assign[now] = L.assign.pop(was)
                moved = True
        if moved:
            L.save_assign()
        API.SysMsg('%s: frame layout "%s" saved.' % (APP_NAME, name), Kit.HUE_GOOD)
        self.close(keep=True)
        self.layout.use_frames(name, tell=False)


class LayoutPage(object):
    """The Settings tab's Layout page: the LAYOUT section (which frame layout
    and window layout are in use, the editor, save, reset, free all)."""
    H = 30 + 28 + 28 + 26 + 26 + 26 + 26 + 26 + 26 + 28 + 24 + 10   # (2.6.85) fit, art / reclaim rows

    def __init__(self):
        self.c = None
        self.store = ({}, {})
        self.frame_names = []
        self.layout_names = []
        self.wins = []             # [(dock key, title)] listed in WINDOWS (2.6.55)
        self.zones = []            # the Zone drop-downs' choices: "free", then the zone ids

    def height(self, w):
        wins = LAYOUT.all_windows()
        return self.H + (Kit.GAP + 34 + 26 * len(wins) + 6 + (20 if LAYOUT.page_preview else 0)
                         if wins else 0)

    def build(self, g, x, y, w):
        L = LAYOUT
        self.store = ({}, {})
        c = {}
        Kit.add_section(g, x, y, w, self.H, "LAYOUT  (where each window sits)")
        dd_w = 170
        ry = y + 32
        Kit.add_label(g, "Zones:", x + 12, ry + 3)
        bx = x + 12 + 80 + dd_w + 16
        cap = "Edit zones"
        Kit.art_button(g, self.store, "edit", Kit.ART_PAGE, bx, ry - 2, cap,
                       "Show every zone as a frame on the screen grid to drag, resize, add or remove")
        bx += 35 + Kit.text_w(cap) + 16
        cap = "New zones"
        Kit.art_button(g, self.store, "new", Kit.ART_OK, bx, ry - 2, cap,
                       "Start a new frame layout with one zone in the middle of the screen")
        bx += 35 + Kit.text_w(cap) + 16
        cap = "Remove zones"
        Kit.art_button(g, self.store, "remove", Kit.ART_CLOSE, bx, ry - 2, cap,
                       "Delete the frame layout in use (Default can't be deleted)")
        ry += 28
        Kit.add_label(g, "Windows:", x + 12, ry + 3)
        bx = x + 12 + 80 + dd_w + 16
        cap = "Save windows"
        Kit.art_button(g, self.store, "save", Kit.ART_OK, bx, ry - 2, cap,
                       "Save where every window sits now as the window layout in use")
        bx += 35 + Kit.text_w(cap) + 16
        cap = "Reset"
        Kit.art_button(g, self.store, "reset", Kit.ART_CLOSE, bx, ry - 2, cap,
                       "Put the window layout back to Default and place every window again")
        bx += 35 + Kit.text_w(cap) + 16
        cap = "Free all"
        Kit.art_button(g, self.store, "free", Kit.ART_CLOSE, bx, ry - 2, cap,
                       "Take every window out of its zone and leave it where it is")
        ry += 28
        c["game"] = Kit.add_check(g, "Give an empty zone's room to the game area", x + 12, ry,
                                  L.game_grows, "Widens the game area when a zone beside it is empty")
        ry += 26
        # (2.6.70) the one frame round the game area (Surround), and the fit check
        c["unified"] = Kit.add_check(g, "Join zone windows in one frame", x + 12, ry, L.unified,
                                     "Windows in zones share one stone surround, with a gold border "
                                     "round the game area (unticked: every window keeps its own look)")
        cap = "Check fit"
        Kit.art_button(g, self.store, "check", Kit.ART_PLAY, x + w - 12 - 35 - Kit.text_w(cap),
                       ry - 2, cap, "Print in the journal where each window in a zone sits and "
                       "whether it fills its zone")
        ry += 26
        # (2.6.72) zones hold their windows: Arrange mode moves them; Check look
        cap = "Done" if L.arrange else "Arrange windows"
        Kit.art_button(g, self.store, "arrange", Kit.ART_OK if L.arrange else Kit.ART_PLAY,
                       x + 12, ry - 2, cap,
                       "Lock every window in its zone" if L.arrange else
                       "Unlock the layout so windows can be moved between zones (Esc or Done locks it)")
        cap = "Check look"
        lx = x + w - 12 - 35 - Kit.text_w(cap)
        Kit.art_button(g, self.store, "look", Kit.ART_PLAY, lx,
                       ry - 2, cap, "Print in the journal each window in a zone that doesn't "
                       "follow the one-frame look")
        cap = "Check zones"                          # (2.6.74)
        Kit.art_button(g, self.store, "zones_check", Kit.ART_PLAY, lx - 16 - 35 - Kit.text_w(cap),
                       ry - 2, cap, "Print in the journal every window the layout knows: its zone, "
                       "whether it is open, held or dragged, and its place")
        ry += 26
        c["arch"] = Kit.add_check(g, "Arch the game view between your frames", x + 12, ry, L.arch,
                                  "With one frame on and the frames in the top corners, the game "
                                  "view runs up between them under an arched stone edge")
        ry += 26
        c["ping"] = Kit.add_check(g, "Show your ping in the frame", x + 12, ry, L.ping,
                                  "With one frame on, your connection's ping shows by the game "
                                  "area's top-right corner")
        ry += 26
        c["fit_view"] = Kit.add_check(g, "Fit the game view to the keep-clear zone", x + 12, ry,
                                      L.fit_view,
                                      "No border, exactly that zone's size and locked there; "
                                      "unticked or stopped, your own view comes back")
        ry += 26
        cap = "Art: " + L.art
        Kit.art_button(g, self.store, "art", Kit.ART_PAGE, x + 12, ry - 2, cap,
                       "The art between the zones with one frame on: plain stone, carved panels, or "
                       "carved with dragons; click for the next")
        bx = x + 12 + 35 + Kit.text_w("Art: dragons") + 24
        cap = "Reclaim space"
        Kit.art_button(g, self.store, "reclaim", Kit.ART_PLAY, bx, ry - 2, cap,
                       "Give the game area every gap beside it; the frames and other windows keep their size")
        bx += 35 + Kit.text_w(cap) + 16
        if L._undo_load() is not None:
            cap = "Undo"
            Kit.art_button(g, self.store, "reclaim_undo", Kit.ART_CLOSE, bx, ry - 2, cap,
                           "Put the zones back as they were before Reclaim space")
        ry += 28
        Kit.add_label(g, Kit.fit(L.status_text(), w - 24), x + 12, ry, Kit.HUE_INFO)
        # the drop-downs last: their lists open on top
        self.frame_names = [LAYOUT_DEFAULT] + L.frame_names()
        fi = self.frame_names.index(L.frames_name) if L.frames_name in self.frame_names else 0
        dd = G.CreateDropDown(dd_w, self.frame_names, fi)
        dd.SetPos(x + 12 + 80, y + 32)
        g.Add(dd)
        safe(lambda: dd.SetTooltip("The frame layout in use: the zones the windows sit in"))
        c["zones"] = (dd, fi)
        self.layout_names = ["(none)", LAYOUT_DEFAULT, LAYOUT_MIRRORED] + L.layout_names()
        cur = L.layout_name or "(none)"
        li = self.layout_names.index(cur) if cur in self.layout_names else 0
        dd2 = G.CreateDropDown(dd_w, self.layout_names, li)
        dd2.SetPos(x + 12 + 80, y + 32 + 28)
        g.Add(dd2)
        safe(lambda: dd2.SetTooltip("The window layout in use; pick one to place every window in its zone"))
        c["windows"] = (dd2, li)
        # WINDOWS (2.6.55): every listed window with the zone it sits in; the
        # drop-downs after everything else, so an open list draws on top
        self.wins = L.all_windows()
        c["zone_dd"] = []
        if self.wins:
            self.zones = ["free"] + [z for z in L.zone_choices() if z]
            wy = y + self.H + Kit.GAP
            wh = 34 + 26 * len(self.wins) + 6 + (20 if L.page_preview else 0)
            Kit.add_section(g, x, wy, w, wh, "WINDOWS  (the zone each sits in)")
            ry = wy + 32
            for key, title in self.wins:
                Kit.add_label(g, Kit.fit(title, 270), x + 12, ry + 3)
                ry += 26
            if L.page_preview:                       # (2.6.74) the last window put in a zone
                bad = L.page_preview.startswith("!")
                Kit.add_label(g, Kit.fit(L.page_preview.lstrip("!"), w - 24), x + 12, ry + 3,
                              Kit.HUE_BAD if bad else Kit.HUE_INFO)
            ry = wy + 32
            for key, title in self.wins:
                zid = L.zone_of(key)
                ids, labels = self.zones, self.zones
                if zid is not None and zid not in self.zones:
                    # 2.6.81: a zone this frame layout lacks is shown as it is, so
                    # picking "free" frees the window
                    ids = self.zones + [zid]
                    labels = self.zones + [Kit.fit("%s (missing)" % zid, dd_w - 30)]
                zi = ids.index(zid) if zid in ids else 0
                dd3 = G.CreateDropDown(dd_w, labels, zi)
                dd3.SetPos(x + 12 + 290, ry)
                g.Add(dd3)
                safe(lambda d=dd3, t=title: d.SetTooltip(
                    "The zone %s sits in (free: it stays where you put it)" % t))
                c["zone_dd"].append((key, dd3, zi, ids))
                ry += 26
        self.c = c

    def poll(self):
        c = self.c
        if c is None:
            return
        L = LAYOUT
        if L.page_refresh:
            L.page_refresh = False
            HOST.refresh_settings(LAYOUT_PAGE)
            return
        for n, (key, dd3, zi, ids) in enumerate(c["zone_dd"]):
            try:
                i = int(dd3.GetSelectedIndex())
            except Exception:
                i = zi
            if i != zi and 0 <= i < len(ids):
                c["zone_dd"][n] = (key, dd3, i, ids)
                zid = None if i == 0 else ids[i]
                L.page_preview = ""
                if zid:                              # (2.6.74) what it gets there, or why not
                    W, H = Kit.screen()
                    zs = L.frames_in_use(W, H) if W > 0 and H > 0 else None
                    z = zs.by_id(zid) if zs is not None else None
                    L.page_preview = L.preview_text(key, z)
                L.assign_to(key, zid)
                L.page_refresh = True
                return
        dd, fi = c["zones"]
        try:
            i = int(dd.GetSelectedIndex())
        except Exception:
            i = fi
        if i != fi and 0 <= i < len(self.frame_names):
            c["zones"] = (dd, i)
            L.use_frames(self.frame_names[i])
            return
        dd2, li = c["windows"]
        try:
            i = int(dd2.GetSelectedIndex())
        except Exception:
            i = li
        if i != li and 0 <= i < len(self.layout_names):
            c["windows"] = (dd2, i)
            L.use_windows("" if i == 0 else self.layout_names[i])
            return
        try:
            game = bool(c["game"].IsChecked)
        except Exception:
            game = L.game_grows
        if game != L.game_grows:
            L.game_grows = game
            L.save_opts()
            L.dirty = True
        try:
            uni = bool(c["unified"].IsChecked)
        except Exception:
            uni = L.unified
        if uni != L.unified:                         # (2.6.70) drawn or taken away on the next pass
            L.unified = uni
            L.save_opts()
            L.dirty = L.fresh = True                 # 2.6.81: the arch and hug follow it
        if Kit.was_clicked(self.store, "reclaim"):   # (2.6.85)
            L.reclaim_space()
            return
        if Kit.was_clicked(self.store, "reclaim_undo"):
            L.reclaim_back()
            return
        if Kit.was_clicked(self.store, "art"):
            looks = Surround.ART_LOOKS
            L.art = looks[(looks.index(L.art) + 1) % len(looks)]
            L.save_opts()
            L.page_refresh = True
            return
        for k, attr in (("arch", "arch"), ("ping", "ping"), ("fit_view", "fit_view")):     # (2.6.72)
            try:
                v = bool(c[k].IsChecked)
            except Exception:
                v = getattr(L, attr)
            if v != getattr(L, attr):
                setattr(L, attr, v)
                L.save_opts()
                L.dirty = L.fresh = True
        if Kit.was_clicked(self.store, "check"):
            L.report_fit()
        if Kit.was_clicked(self.store, "look"):
            L.report_look()
        if Kit.was_clicked(self.store, "zones_check"):
            L.report_zones()                         # (2.6.74)
        if Kit.was_clicked(self.store, "arrange"):
            L.set_arrange(not L.arrange)
            return
        if Kit.was_clicked(self.store, "edit"):
            L.edit(fresh=False)
        elif Kit.was_clicked(self.store, "new"):
            L.edit(fresh=True)
        elif Kit.was_clicked(self.store, "remove"):
            if not L.remove_frames(L.frames_name):
                API.SysMsg("%s: Default can't be deleted; pick another frame layout first."
                           % APP_NAME, Kit.HUE_BAD)
        elif Kit.was_clicked(self.store, "save"):
            L.save_windows()
        elif Kit.was_clicked(self.store, "reset"):
            L.reset()
        elif Kit.was_clicked(self.store, "free"):
            L.free_all()

    def closed(self):
        self.c = None

    def api(self):
        return {"config_height": self.height, "build_config": self.build,
                "poll_config": self.poll, "config_closed": self.closed}


LAYOUT_PAGE = "va.layout"


SNAP = Snap()
ALERTS = Alerts()                          # HOST.alert (see Alerts)
GUARD = Guard()                            # HOST.guarded (see Guard)
LAYOUT = Layout()                          # the zones and the windows in them (see Layout)

HOST = Host()


# =============================================================================
#  Loading the modules
#  Each module is its own file, in the VirtueAssistantModules folder next to
#  this script (or in another folder beside it named VirtueAssistant...Modules).
#  A file is run inside this script, so it sees everything above (API, G,
#  safe, Client, Kit, HOST ...), and its last lines register it with
#  HOST.add(...). The files below load in this order (the Modules tab order);
#  any other *Module.py loads after them, by name: VirtueAssistantModules
#  first, then the other folders, by folder name.
# =============================================================================
MODULE_FILES = (
    ("actionbar", "Action Bar", "ActionBarModule.py"),
    ("hud", "Character HUD", "CharacterHudModule.py"),
    ("inventory", "Inventory", "InventoryModule.py"),
    ("grimoire", "Grimoire", "GrimoireModule.py"),
    ("worldmap", "World Map", "WorldMapModule.py"),
    ("ultima", "Ultima Tracker", "UltimaTrackerModule.py"),
    ("social", "Social", "SocialModule.py"),
    ("skills", "Skills", "SkillsModule.py"),
    ("butler", "Property Butler", "PropertyButlerModule.py"),
    ("meters", "Meters", "MetersModule.py"),
    ("mongotchi", "Mongotchi", "MongotchiModule.py"),
)
#  Module keys of files no longer shipped: a file registering one of them (left
#  in the folder by an older install) is skipped, with a journal line.
RETIRED_KEYS = ("autodoors",)


def module_folders():
    """The module folders: VirtueAssistantModules first, then every other
    folder named VirtueAssistant...Modules, by name. Each is looked for
    beside this script, else in the client's LegionScripts folder."""
    places = []
    base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
    if base:
        if safe(lambda: os.path.isfile(base), False):
            base = os.path.dirname(base)
        places += [base, os.path.dirname(base)]
    try:
        import System
        root = str(System.AppDomain.CurrentDomain.BaseDirectory).rstrip("/\\")
        places += [os.path.join(root, "LegionScripts"), root]
    except Exception:
        pass
    found = {}                             # folder name -> its path (first place found)
    for p in places:
        if not p:
            continue
        for n in (safe(lambda: os.listdir(p), []) or []):
            if n in found or not (n.startswith("VirtueAssistant") and n.endswith("Modules")):
                continue
            d = os.path.join(p, n)
            if safe(lambda: os.path.isdir(d), False):
                found[n] = d
    names = ([MODULE_DIR] if MODULE_DIR in found else []) + \
        sorted(n for n in found if n != MODULE_DIR)
    return [found[n] for n in names]


def _read_text(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        import System                      # IronPython builds without file io
        return str(System.IO.File.ReadAllText(path))


class _Reg(object):
    """What a module file's HOST.add(...) line says, read without compiling the
    file: the key, title, description, interval, default_on, category, parts
    and aliases (see read_registration)."""
    def __init__(self):
        self.ok = False
        self.key = self.title = self.desc = None
        self.interval = None
        self.default_on = False
        self.category = None
        self.parts = ()
        self.aliases = ()

    def take(self, key, title, desc, factory=None, interval=None, default_on=False,
             category=None, parts=(), aliases=()):
        self.key, self.title, self.desc = str(key), str(title), str(desc)
        self.interval = interval if isinstance(interval, (int, float)) else None
        self.default_on = bool(default_on)
        self.category = category
        self.parts = tuple(tuple(p) for p in (parts or ()))
        self.aliases = tuple(aliases or ())
        self.ok = True


def _balanced(text, start):
    """The text inside the parentheses that open at `start` (text[start] is
    "("), minding strings; None when they never close."""
    depth, i, n = 0, start, len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
        i += 1
    return None


def read_registration(text):
    """The last HOST.add(...) call in a module file, read as data (every name in
    it that isn't a number of this script is taken as None): a _Reg, or None
    when the call can't be read that way (the file is then compiled at once)."""
    at = text.rfind("HOST.add(")
    if at < 0:
        return None
    args = _balanced(text, at + len("HOST.add"))
    if args is None:
        return None
    ns = {}
    for name in set(re.findall(r"[A-Za-z_]\w*", args)):
        v = globals().get(name)
        ns[name] = v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    for word in ("True", "False", "None"):
        ns.pop(word, None)
    reg = _Reg()
    ns["_reg"] = reg.take
    try:
        eval("_reg(" + args + ")", {"__builtins__": {}}, ns)
    except Exception:
        return None
    return reg if reg.ok else None


def load_modules():
    folders = module_folders()
    if not folders:
        API.SysMsg("%s: no %s folder found next to this script, so no modules were "
                   "loaded. Put the folder of module files beside it." % (APP_NAME, MODULE_DIR),
                   Kit.HUE_BAD)
        return
    known = [f for _, _, f in MODULE_FILES]
    # (folder, file name) for every module file: the built-in order first,
    # then the rest of each folder, folder by folder, by name. A file name
    # found in two folders loads from the first one only.
    listings = []
    for d in folders:
        names = safe(lambda: os.listdir(d), []) or []
        listings.append((d, sorted(n for n in names if n.endswith("Module.py"))))
    entries = []
    for n in known:
        for d, names in listings:
            if n in names:
                entries.append((d, n))
                break
    taken = set(n for _, n in entries)
    for d, names in listings:
        for n in names:
            if n not in taken:
                entries.append((d, n))
                taken.add(n)
    titles = dict((f, (k, t)) for k, t, f in MODULE_FILES)
    # which modules are switched on (saved): those are compiled now, the rest
    # when first needed (LAZY_MODULES)
    on, debug = set(), False
    for part in Kit.get_var(SETTINGS_KEY).split(";"):
        part = part.strip()
        if part.startswith("modules="):
            on = set(k for k in part.split("=", 1)[1].split(",") if k)
        elif part.startswith("debug="):
            debug = part.split("=", 1)[1].strip() == "1"
    t_all = time.time()
    for where, name in entries:
        path = os.path.join(where, name)
        if not safe(lambda: os.path.isfile(path), False):
            continue                       # left out on purpose: not listed
        m = None
        try:
            text = _read_text(path)
            # the registration line at the bottom: HOST.add("key", "Title", "description",
            # _module_x, interval [, default_on=True] [, category="Heading"] [, parts=(...)]
            # [, aliases=(...)]), read as data (read_registration)
            m = read_registration(text)
            if m is not None and m.key in RETIRED_KEYS:
                # a module no longer shipped, left in the folder by an older install
                API.SysMsg("%s: %s is no longer part of %s and was skipped; that file "
                           "can be deleted." % (APP_NAME, name, APP_NAME), Kit.HUE_INFO)
                continue
            if m is not None and m.key in HOST.old_map and HOST.old_map[m.key][0] != m.key:
                # a 2.6.06 module file whose module is a part of a themed module now
                mk, pk = HOST.old_map[m.key]
                home = dict.get(HOST.by_key, mk)
                API.SysMsg("%s: %s is now part of %s and was skipped; that file can be "
                           "deleted." % (APP_NAME, name, home.title if home else mk),
                           Kit.HUE_INFO)
                continue
            if m is not None and dict.__contains__(HOST.by_key, m.key):
                # a second file with a key already listed (lazily or not): skip it
                # here, or its HOST.add would be taken for the first file's own
                API.SysMsg("%s: %s was loaded twice (module key \"%s\"); the second copy "
                           "was skipped." % (APP_NAME, m.title, m.key), Kit.HUE_BAD)
                continue
            if m is not None and m.interval is None and debug:
                API.SysMsg("%s: %s: the interval in its HOST.add line isn't a number "
                           "or a name of this script, so the file is compiled at start "
                           "(not lazily)." % (APP_NAME, name), Kit.HUE_INFO)
            if LAZY_MODULES and m is None and debug:
                API.SysMsg("%s: %s has no HOST.add line this script can read (quoted key / "
                           "title / description, a numeric interval), so the file is "
                           "compiled at start (not lazily)." % (APP_NAME, name), Kit.HUE_INFO)
            wanted = m is not None and (m.key in on or any(
                old in on for p in m.parts for old in (p[4] if len(p) > 4 else ())))
            if LAZY_MODULES and m is not None and m.interval is not None and not wanted:
                HOST.add_lazy(m.key, m.title, m.desc, path, m.interval, m.default_on,
                              m.category, m.parts, m.aliases)
                continue                   # listed; compiled when turned on
            t0 = time.time()
            code = compile(text, path, "exec")
            exec(code, globals())          # defines the module and calls HOST.add
            LOAD_MS.append((name, int((time.time() - t0) * 1000)))
        except Exception as ex:
            line = getattr(ex, "lineno", None)       # a syntax error knows its line
            if line:
                msg = "%s (%s line %s)" % (getattr(ex, "msg", None) or ex, name, line)
            else:
                msg = "%s%s" % (ex, _error_where())
            API.SysMsg("%s: %s could not be loaded: %s" % (APP_NAME, name, msg),
                       Kit.HUE_BAD)
            # listed on the Modules tab as broken: by the key and title of its
            # own registration line when one was read, else by the built-in table
            kt = (m.key, m.title) if m is not None else titles.get(name)
            if kt is not None and not dict.__contains__(HOST.by_key, kt[0]):
                key, title = kt
                s = HOST.add(key, title, "", lambda: None, 0.1)
                s.api, s.broken = None, msg
    LOAD_MS.append(("all", int((time.time() - t_all) * 1000)))


LOAD_MS = []                               # (module file, ms to compile and load) - debug
PROFILES = Profiles()
try:
    PROFILES.startup()                     # the favorite profile, before anything reads settings
except Exception as _ex:
    API.SysMsg("%s: the favourite profile could not be put on this character: %s%s"
               % (APP_NAME, Tz.why(_ex), _error_where()), Kit.HUE_BAD)


def _module_sysstats():
    """(2.6.85) A small button: hover for ping, FPS and memory; click for a window of them."""
    KEY = "sysstats"
    TITLE = "System Stats"
    POS_KEY, MIN_KEY, BTN_KEY, OPEN_KEY = ("SystemStats_pos", "SystemStats_min", "SystemStats_btn",
                                           "SystemStats_open")
    W, H = 240, 170
    MINI_W, MINI_H = 240, 46
    EVERY = 0.3                 # seconds between reads: a few a second at most
    TRAY_ICON = 0x1F2D
    ROWS = ("Ping", "FPS", "Frame", "Memory", "In", "Out", "Packets")
    st = {"shutting": False, "minimized": False, "docked": False, "open": False, "queue": [],
          "next": 0.0, "vals": {}, "tip": None}
    win = {"g": None, "c": {}, "store": ({}, {})}
    btn = {"g": None, "b": None, "store": ({}, {})}
    queue = Kit.queuer(st)
    on_disposed = Kit.disposer(KEY, st, win)
    srcs = {"env": None, "gc": None}

    def read():
        """Everything from fields the client keeps anyway: no waits, cached between reads."""
        v = {}
        try:
            if srcs["env"] is None:
                srcs["env"] = Tz.T("ClassicUO.CUOEnviroment")
            fps = int(Tz.get(None, "CurrentRefreshRate", srcs["env"]))
            v["FPS"] = str(fps)
            v["Frame"] = "%.1f ms" % (1000.0 / fps) if fps > 0 else "-"
        except Exception:
            pass
        try:
            sock = Tz.get(None, "Socket", Tz.T("ClassicUO.Network.AsyncNetClient"))
            stats = Tz.get(sock, "Statistics")
            src = str(Typing._get(stats, "CurrentPingSource", default="") or "")
            v["Ping"] = "off" if src.endswith("Disabled") else "%d ms" % int(Tz.get(stats, "Ping"))
            v["In"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesReceived")) / 1024.0)
            v["Out"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesSent")) / 1024.0)
            v["Packets"] = "%d in, %d out" % (int(Tz.get(stats, "TotalPacketsReceived")),
                                              int(Tz.get(stats, "TotalPacketsSent")))
        except Exception:
            pass
        try:
            import System
            v["Memory"] = "%d MB" % (int(System.GC.GetTotalMemory(False)) // (1024 * 1024))
        except Exception:
            pass
        return v

    def build_button():
        x, y = Kit.load_pos(BTN_KEY, (8, 200), (46, 46))
        store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, 46, 46, corners=False)
        b = Kit.art_button(g, store, "stats", Kit.ART_CIRCLE, 12, 12, None, "System stats",
                           on_click=queue("toggle"))
        Kit.place(g, x, y, 46, 46)
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, lambda: Kit.save_pos(BTN_KEY, g)))
        btn.update({"g": g, "b": b, "store": store})

    def build_window():
        x, y = Kit.load_pos(POS_KEY, (70, 200), (W, H))
        if Kit.is_open(win["g"]):
            x, y = win["g"].GetX(), win["g"].GetY()
        old, win["g"] = win["g"], None
        M = Kit.MARGIN
        store = ({}, {})
        c = {}
        g = G.CreateGump(True, True)
        if st["minimized"]:
            w, h = MINI_W, MINI_H
            c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"), close_tip="Close")
        else:
            w, h = W, M + 30 + Kit.GAP + 8 + len(ROWS) * 20 + M - 8 - 12
            Kit.add_window_frame(g, w, h)
            Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"), close_tip="Close")
            yb = M + 30 + Kit.GAP
            Kit.add_section(g, M, yb, w - 2 * M, h - yb - M)
            for i, name in enumerate(ROWS):
                Kit.add_label(g, name + ":", M + 10, yb + 6 + i * 20, Kit.HUE_INFO)
                c[name] = Kit.add_label(g, "", M + 90, yb + 6 + i * 20, Kit.HUE_TEXT)
        Kit.place(g, x, y, w, h)
        if safe(lambda: HOST.layout_locked(KEY), False):
            safe(lambda: setattr(g, "CanMove", False))
        win.update({"g": g, "c": c, "store": store})
        G.AddControlOnDisposed(g, on_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, lambda: Kit.save_pos(POS_KEY, win["g"])))
        if st["minimized"] and st["docked"]:
            safe(lambda: setattr(g, "IsVisible", False))
        refresh()
        Kit.dispose(old)

    def refresh():
        v = st["vals"]
        c = win["c"]
        if st["minimized"]:
            lbl = c.get("status")
            if lbl is not None:
                Kit.set_text(lbl, "%s: %s, %s FPS" % (TITLE, v.get("Ping", "-"), v.get("FPS", "-")))
            return
        for name in ROWS:
            lbl = c.get(name)
            if lbl is not None:
                Kit.set_text(lbl, v.get(name, "-"))

    def close_window():
        g, win["g"] = win["g"], None
        st["open"] = False
        HOST.dock_remove(KEY)
        Kit.save_pos(POS_KEY, g)
        Kit.put_var(OPEN_KEY, "0")
        Kit.dispose(g)

    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "next": 0.0,
                   "minimized": Kit.load_min(MIN_KEY) or bool(safe(lambda: HOST.dock_wanted(KEY), False)),
                   "open": Kit.get_var(OPEN_KEY, "0") == "1"})
        build_button()
        if st["open"] or safe(lambda: HOST.layout_holds(KEY), False):
            st["open"] = True
            build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))

    def _tick():
        now = time.time()
        while st["queue"]:
            action = st["queue"].pop(0)
            if action == "toggle":
                if st["open"] and not safe(lambda: HOST.layout_holds(KEY), False):
                    close_window()
                elif not st["open"]:
                    st["open"] = True
                    Kit.put_var(OPEN_KEY, "1")
                    st["minimized"] = st["docked"] = False
                    build_window()
                    HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            elif action == "toggle_min":
                st["minimized"] = not st["minimized"]
                st["docked"] = False
                HOST.dock_forget(KEY)
                Kit.save_min(MIN_KEY, st["minimized"])
                build_window()
            elif action == "to_bar":
                HOST.dock_to_bar(KEY, TITLE)
            elif action == "redraw":
                if st["open"]:
                    build_window()
        if st["open"] and Kit.was_clicked(win["store"], "close"):
            close_window()
        if not 0 <= st["next"] - now <= EVERY:
            st["next"] = now + EVERY
            st["vals"] = read()
            v = st["vals"]
            tip = "Ping %s, %s FPS, memory %s. Click: open or close the window" % (
                v.get("Ping", "-"), v.get("FPS", "-"), v.get("Memory", "-"))
            if tip != st["tip"] and btn["b"] is not None:
                st["tip"] = tip
                try:
                    btn["b"].SetTooltip(tip)
                except Exception:
                    pass
            if st["open"] and win["g"] is not None and not (st["minimized"] and st["docked"]):
                refresh()

    def _stop():
        st["shutting"] = True
        HOST.dock_remove(KEY)
        if win["g"] is not None:
            Kit.save_pos(POS_KEY, win["g"])
        Kit.save_min(MIN_KEY, st["minimized"])
        Kit.put_var(OPEN_KEY, "1" if st["open"] else "0")
        g, win["g"] = win["g"], None
        Kit.dispose(g)
        b, btn["g"] = btn["g"], None
        if b is not None:
            Kit.save_pos(BTN_KEY, b)
        Kit.dispose(b)

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True}


load_modules()
HOST.add("sysstats", "System Stats", "A small button with your ping, FPS and memory", _module_sysstats,
         0.1, category="On screen")
HOST.run()
