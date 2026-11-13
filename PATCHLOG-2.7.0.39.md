# Virtue Assistant 2.7.0.39

Built from 2.7.0.38. A full bug sweep: every module and the main script were read line by line, every fix was
reviewed again, and the code was checked with new test tools (saved data that is damaged or hand-edited, every
click and hotkey path, every window size, text encodings, the two client threads, writes to the client's own
controls). Every bug found was fixed with a test that fails on the old code. No new features.

## Shard rules (In Mani Ylem)

Nothing new acts in game. Several fixes tighten the rules where a path could slip past them:
- Action Bar cells that aim a harmful spell, field or wand at your last target, and cells that target an item in
  a blue or green player's backpack, now ask for the second press in a guard zone (R6), and one press starts only
  one Legion script (R1).
- Three quick clicks no longer count as the confirming second press (R6).
- Ultima Tracker never lets a bandage press and a spell press aim each other's cursor (R1).
- Property Butler's Ban... pick is itself the confirmation, and visitor rows keep their place so a press never
  lands on someone else (R8).
- Skill loops stay paused while an alarm's hold runs, also after the banner is switched off (R3).

## Fixed

### Action Bar

- Action Bar: the Party window button now opens TazUO's party window itself, so a TazUO macro you have running keeps running.
- Action Bar: a macro, script or item cell set to target your last target now asks for a second press when that target is an item in a blue or green player's backpack in a guard zone.
- Action Bar: when the Grimoire module can't start, the Grimoire button opens your spellbook at once instead of after 4 seconds.
- Action Bar: a cell name that doesn't fit under the hotkey on a very small cell sits on the cell's bottom edge, or is left out, instead of spilling past the cell.
- Action Bar: the status line under EDIT A CELL is cut to fit the settings page.
- Action Bar: a Legion script cell starts only one script, even when TazUO's script list can't be read.
- Action Bar: a shorter description on the Modules tab.
- Action Bar: a cell that casts Fire Field, Poison Field, Energy Field, Blade Spirits or Energy Vortex at your last target, or uses a wand on it, now asks for a second press when that target is blue or green in a guard zone.
- Action Bar: a short spell name typed on a cell (such as "field") is now judged by the spell it really casts.
- Action Bar: an item, macro, script or spell cell set to target your last target now leaves a neutral cursor for you to aim by hand when that target is blue or green in a guard zone.
- Action Bar: the radial ring key stops at once when another module takes that key, and works again when it is freed.
- Action Bar: the Grimoire and Bags buttons no longer open the spellbook or bag as well when the module is slow to start.
- Action Bar: Legion script cells start the exact script you picked, and one press starts only one script.
- Action Bar: the script list no longer shows a "LegionScripts/" prefix or files from Virtue Assistant's module folders.
- Action Bar: a cell filled or cleared from its menu gets the right background at once.
- Action Bar: names on small cells use a smaller text size so they stay inside the cell.
- Action Bar: a hotkey given to a top-row cell, a button or a bag slot comes off the bottom cells of the other pages.
- Action Bar: the settings page fits the narrower settings window of an Action Bar run alone.
- Action Bar: the Hotkey and Red at menus are wide enough for their hint and status lines.
- Action Bar: with the Action Bar off, Pick item, Prev, Next, Keybind mode and the ring buttons say to turn it on first.
- Action Bar: "Then target" is offered only on cells that raise a target cursor.
- Action Bar: Back from "Type a name" returns to the list you came from.
- Action Bar: a start that fails before the bar has loaded no longer saves an empty bar over yours.
- Action Bar: a right-click on a cell wakes Virtue Assistant at once, so its menu opens without a pause.
- Action Bar: a zone too small for the bar's shape says so.

### Character HUD

- Character HUD: mirrored frames follow a drag all the way, even when you let go while still moving.
- Character HUD: the cast bar names your spell when it runs out of mana at the end of its cast.
- Character HUD: Buffs & Timers drops a spell the shard refuses as too far away or unseen when an Action Bar cell aimed it.
- Character HUD: a buff cast with an Action Bar "target yourself" cell shows on you when you have no last target or turn hidden, and a spell that spent no mana shows no row.
- Character HUD: Pick on the Frames settings page leaves a spell or bandage cursor alone.
- Character HUD: a buff waiting for your stats to move stays on the right person when you pick a new target meanwhile.
- Character HUD: times past an hour read as hours and minutes (1:02 h).
- Character HUD: damaged saved settings, learned swings, frames, timers or bandage times read as defaults instead of stopping a part.
- Character HUD: Bandages no longer ends a running bandage when the shard refuses another click with "you must wait".
- Character HUD: the Swing Bar no longer learns its first swing from a chase.
- Character HUD: the Frames OPTIONS columns line up with compact rows on.
- Character HUD: with Prefer the attack target ticked, the target frame goes back to your last target once the mobile you attacked is gone.
- Character HUD: a portrait is taken again when someone changes clothes, armour, hair or body during play.
- Character HUD: pieces of a frame behind a tab stay hidden with it instead of showing at the screen's edge.
- Character HUD: a saved frame for someone out of sight shows their saved name, and a party member's real name is saved once known.
- Character HUD: Buffs & Timers no longer drops a buff on a far or unseen line from something else, and a fizzle, no mana or no reagents now stops a timer for the failed spell.
- Character HUD: Remove frame only aims its own cursor, and Add frame or Remove frame leaves a spell or bandage cursor alone.
- Character HUD: an Invisibility timer brought back after a restart ends when you are revealed.
- Character HUD: the cast bar says "No mana" without naming your previous spell.
- Character HUD: mirrored frames follow a drag all the way to where it was let go.
- Character HUD: a buff you cast on yourself shows on you, not on your last target.
- Character HUD: the Swing Bar follows your current stamina, keeps counting while paused, notices your swing while you step, and follows the mobile you attacked by double-click.
- Character HUD: unticking the shard's buff icons clears the rows they made.
- Character HUD: times show a space before the unit (12 s), and tooltips lose their final full stop.
- Character HUD: the Pets "Heal with" drop-down lines up with its row when compact rows are on.
- Character HUD: Bandages stops waiting at once when the shard says you must wait, and answers only a cursor that comes within 1.5 s.
- Character HUD: Pets ends a heal when the shard refuses the spell before any cursor.
- Character HUD: a bandage time typed just before the settings page closes is kept.
- Character HUD: the Bandages settings can now be found with the settings search.
- Character HUD: Pets no longer scans every mobile four times a second when a pet uses two or more slots.
- Character HUD: Pets notes and help start with a capital and give tiles as a unit.

### Interface

- Interface: renaming a zone in the zone editor keeps its windows in every saved window layout made on those frames, in a situation layout's way back, and in the zone's picked tab.
- Interface: a new, split or copied zone no longer takes the name of a zone renamed or removed earlier, so it never picks up that zone's windows.
- Interface: Put it here in a New zones session says the zone isn't saved yet, and goes by the zone's size as you edited it.
- Interface: the window picked in the zone editor stays picked when windows open or close.
- Interface: the Col and Row hints in the zone editor give the last square a zone can start on.
- Interface: the save notes about a window too big for its zone use that window's minimum for the zone's shape, and count a tabs zone's tab strip.
- Interface: the Modules tab describes Interface as "Zones, layouts and the one-panel look", and the fade option names Character HUD > Frames.
- Interface: typing a new Col, Row, W or H for a zone in the zone editor keeps the other sides exactly where they were, and a zone that reaches the screen edge stays on it instead of being refused.
- Interface: saving zones after swapping names, or after giving a zone the name of a removed one, keeps each zone's windows with it.
- Interface: Delete in the zone editor removes a zone only with the mouse on that zone or on the editor.
- Interface: picking another zone in the zone editor clears the window preview of the last one.
- Interface: Put it here also updates the zone the window came from.
- Interface: Even out no longer resizes a locked zone; it names the locked zone instead.
- Interface: the zone editor says a refusal again when you try the same thing a few seconds later.
- Interface: resizing the game window while the zone editor is open no longer leaves undo steps for the old screen size.
- Interface: the zone editor no longer works out its gap marks on every pass when there is nothing to mark.
- Interface: the zones-picked line in the zone editor loses its stray full stop.
- Interface: Done in Interface Setup now sticks while a situation layout (war mode, bank, dungeon or town) is in use.
- Interface: the Interface Setup window stays above its zone preview when you pick a layout or a zone.
- Interface: Set up brings a minimised Interface Setup window back.
- Interface: if the Interface Setup window is closed some other way, its zone preview goes with it.
- Interface: Check says "1 of 1 window fills its zone" for a single window.
- Interface: window zones no longer land on each other or slide into the game area when a frame layout fits a new screen size.
- Interface: a frame layout loaded again keeps every zone where it was.
- Interface: Reclaim space no longer stretches a window zone over the journal's zone, and says every zone is already tight when the game area would not grow.
- Interface: a window asking for more room never ends up with less, never covers the journal's zone, and keeps that room when the frames are rebuilt.
- Interface: Fill gaps no longer grows a zone into its neighbours.
- Interface: on an ultrawide screen the game area no longer grows under a window in the outer zones.
- Interface: TazUO's World Map or journal says again when it can't be held after coming back to its zone.
- Interface: switching layouts by situation and back keeps the windows you freed and each window's home.
- Interface: a window with a minimum size sharing a zone keeps its own size when its share is too small, stays on screen, and is named once.
- Interface: picking a frame layout moves the windows at once.
- Interface: an empty bags zone another saved window layout uses is no longer deleted.
- Interface: the bags pairing builds "Default (mine)" from the zones you use.
- Interface: Ultima Tracker windows don't hold a zone at log-in while the Tracker part is off.
- Interface: "1 window had no zone and is free".
- Interface: a layout code with over 64 zones or a repeated zone name is refused; its zone names are cleaned like the editor's.
- Interface: Reset and the Default or Mirrored window layout switch to the Default frames when yours have none of their zones.
- Interface: layout names keep accented letters, and one of the settings' own names gets " 2".
- Interface: the dungeon layout also covers Terathan Keep's southern area.
- Interface: a shared or saved frame layout with an empty side keeps a whole game area when it fits a new screen size.
- Interface: a zone no longer stays enlarged after the window that asked for the room leaves it.
- Interface: Share now puts the layout code in its Code field (it stayed empty in the client).

### Inventory

- Inventory: Trap and Untrap read only the server's lines and your own, so speech nearby or a bandage out of reach no longer marks a bag as failed.
- Inventory: Trap and Untrap say why a bag was skipped (out of reach or refused).
- Inventory: an item dropped on a Sort filter's buttons or tick box, or on Add by target or a preset, adds a filter instead.
- Inventory: Bags in a zone falls back to basic pinning when it can't reach the client's window controls, instead of failing.
- Inventory: the Sort filters window opens again next time if it was open.
- Inventory: Paperdoll no longer draws its window twice when it starts after a redraw was left waiting.
- Inventory: Storage skips damaged times or serials in its index file, so the index keeps saving.
- Inventory: Sort filter and Bag Sections names cut to length never end in half an emoji.
- Inventory: Bags, Sort filters, Restock and Bag Sections leave out damaged or out-of-range saved values.
- Inventory: Bags and Bag Sections now tell weapons, armour and jewellery apart by how each item is worn, so shirts, robes, rings, shields and candles no longer count as weapons and plate, chainmail and leather armour count as armour.
- Inventory: Food, tools and the other kinds match whole words, so black pearls, spears, war hammers and leggings no longer land under Food or Keys and tools.
- Inventory: Bag Sections fills its kinds even when Bags runs with basic pinning.
- Inventory: Bags in a zone no longer saves the zone's place as its own.
- Inventory: items that leave a bag together all leave the zoned bags display.
- Inventory: Trap and Untrap count a bag the server refuses as failed, not done.
- Inventory: Bags draws no more columns than it has slots.
- Inventory: a refused "Scale items with the bags" unticks its box again.
- Inventory: a minimised or folded Bags no longer redraws every second after an Inventory part is switched.
- Inventory: switching Bags off closes the Sort filters window and drops a pending bag pick.
- Inventory: Sort and new filters use an item's own colour while Find lights it.
- Inventory: a doubled click on a filter's remove or move button acts once.
- Inventory: Sort rules ticked just before Sort or Clear are saved.
- Inventory: the Sort filters window remembers its place and whether it is minimised.
- Inventory: an item dropped on a filled Sort filters list is added.
- Inventory: a look change redraws the Bags side windows too.
- Inventory: showing or hiding the combined Paperdoll and Bags window counts for start-up settling.
- Inventory: Paperdoll redraws a slot when the worn item changes its look, such as a lantern you light or a robe that is dyed.
- Inventory: Paperdoll without client access shows slot pictures in the item's colour, and a double-click on them or on the body uses the item again.
- Inventory: Paperdoll waits for the drop before it redraws when the Bags grid changes size under an item you are dragging.
- Inventory: Paperdoll's weight alert can sound again only after the load drops under 92%.
- Inventory: Storage notes chests and containers on the ground (in houses too) again.
- Inventory: Storage's Name button in streamer mode leaves the Find box empty instead of showing the real bank box or chest label.
- Inventory: Storage keeps the newest place name, or a cleared one, when two clients share the index.
- Inventory: Storage saves when a place reopened unchanged was last seen, and waits a few seconds before it tries a failed index save again.
- Inventory: Storage cuts a long name without breaking an emoji, and its status lines end without a full stop.
- Inventory: Restock hides a chest's place in streamer mode and tells potions and scrolls apart (Heal potion, Heal scroll).
- Inventory: Supplies settings keep Choose rows and the side drop-down in place with Compact rows on.
- Inventory: the Supplies table can be dragged when there is no player frame to stick to.
- Inventory: the Supplies Rows window shows its own name.
- Inventory: Bag Sections' minimised bar counts item kinds, and a cell's tooltip says a double-click uses one.

### Grimoire

- Grimoire: A trip button or rune pressed again while a trip is on its way never starts a second trip after it ends.
- Grimoire: Making the window too small from a left or top corner no longer pushes it off screen; the opposite edge stays where it was.
- Grimoire: Scale is held to what fits the screen, so the title-row buttons stay on screen.
- Grimoire: When the save file couldn't be read at start, stars set meanwhile never overwrite the Favourites saved in it; they are merged once it reads again.
- Grimoire: Favourites that load a little late now light their stars on runebook pages already shown.
- Grimoire: A runebook that closes before its button is pressed makes no trip, and the journal says so.
- Grimoire: Reagent names no longer run into each other at small scales.
- Grimoire: The Favourites and search lines name the way each row travels (a charge, for example).
- Grimoire: A trip made while Favourites are still loading stays as Last.
- Grimoire: Runebook reads and trips wait for Social's guild read, so neither window shows on screen.
- Grimoire: Stopping the script or switching Grimoire off in the middle of a read or trip ends it at once.
- Grimoire: Summon Creature can be cast from the Fifth Circle again.
- Grimoire: Polymorph no longer holds the target cursor for 5 s.
- Grimoire: the window can't be dragged smaller than its frame, so its title-row buttons stay clickable.
- Grimoire: moving Scale on its settings page while Grimoire is off is saved, with no error.
- Grimoire: a double-clicked trip button, or a second rune pressed while a trip is on its way, no longer makes a second trip.
- Grimoire: a runebook read cut short by a cast no longer leaves the runebook window on screen.
- Grimoire: a scroll trip stops, and keeps the scroll, when the runebook doesn't take the rune.
- Grimoire: a trip is refused when another feature's target cursor stays in use.
- Grimoire: Favourites are no longer lost when the save file can't be read at start.
- Grimoire: Last in Favourites shows only trips really made.
- Grimoire: a window in a zone fits its zone again after a Scale change.
- Grimoire: a spell pressed while another waits for the cursor says it wasn't cast.
- Grimoire: British spelling in spell descriptions, "1 spell known", charge-only runebooks say so, reagent names no longer overlap at small scales, journal lines name the VirtueAssistantSettings folder.

### World Map

- World Map: markers on TazUO's World Map are no longer taken over by a second client after a few minutes while Map Pings is off.
- World Map: a character that comes back after its markers were cleared keeps its new markers, and marker names now carry the character, so two clients never share one.
- World Map: a clock set back no longer makes a running client look gone.
- Map Pings: status lines have no full stop, and the TazUO login line reads plainly in streamer mode.
- Map Pings: connection news from the background is never lost.
- Corpse: Get my things keeps the corpse when it didn't open, instead of forgetting it as empty.
- Corpse: a Need help ping while Map Pings isn't connected writes one journal line, not two.
- Corpse, Treasure Maps, Ore Tracker and Traps & Fields: damaged saved spots, times and hues are skipped or set right instead of breaking the part.
- Treasure Maps: Forget lost maps keeps the spots of maps you keep in the bank.
- Ore Tracker: a block found dry again after it may have come back gets a fresh full window.
- Traps & Fields: keeps scanning after the clock is set back, and closing its settings page always lets go of it.
- World Map: clearing old ping markers while TazUO's World Map is closed no longer removes your corpse, dig spot, dry spot and trap markers from it.
- World Map: two clients on one TazUO install no longer remove each other's markers from TazUO's World Map, and each character's corpse marker has its own name.
- World Map: markers are saved without holding up the game, the corpse marker is kept first when the map is full, and markers left by a logout or crash are cleared at the next start.
- World Map: ping markers that couldn't be removed are tried again a little later.
- Map Pings: the settings page status line is updated safely while connecting.
- Map Pings: a ping on an item in a bag goes to where the bag is, not to a spot in the sea.
- Map Pings: streamer mode now hides guildmates' names over your head, on TazUO's World Map and in the login status.
- Map Pings: the Connection drop-down lines up with its row when compact rows are on.
- Corpse: Get my things no longer forgets a full corpse when the server says to wait.
- Corpse: the Need help ping says when only you can see it.
- Treasure Maps: dig tiles left marked by a logout are cleared at the next start.
- Treasure Maps: a map of unknown level reads "treasure map", every map gets its own marker, and the page number no longer runs into the arrows.
- Treasure Maps and Ore Tracker: closing the tracking arrow is noticed even while another arrow is up.
- Ore Tracker: trying a dry spot again keeps its first estimate, times read "45 s" and "6-16 min", and a damaged saved time no longer switches the part off.
- Traps & Fields: trap graphics typed just before closing the settings page are saved.
- Corpse and Treasure Maps: reading bags and the bank box is lighter on the game.

### Ultima Tracker

- Ultima Tracker: the title-row buttons line up with every other window's.
- Ultima Tracker: B is refused while an H, C, P or Z cast waits for its cursor, and a spell button pressed while a bandage cursor is pending casts once the bandage is aimed, so one press never aims the other's cursor.
- Ultima Tracker: a grey who turns red within 10 s of the first alert is alerted as red once the 10 s pass, while still in range.
- Ultima Tracker: in streamer mode the bandage, health bar, NPC and Foe link journal lines and Lookout's "spotted" line hide player names.
- Ultima Tracker: a combat bar removed for being idle comes back when that mobile, still your last target, loses HP.
- Ultima Tracker: another player saying "X is attacking you" in red no longer puts X on the combat bars or in the attacker list.
- Ultima Tracker: a player who says their own name with "the" while mounted, running or in war mode is no longer taken for a titled NPC.
- Ultima Tracker: typing "heal" or "cure" in chat during a cast no longer counts as the spell's words.
- Ultima Tracker: Target... no longer puts a vendor or other yellow NPC on the Foe list.
- Lookout: without the Tracker part, a blue player with a common first name is counted again once their name shows no title; titled NPCs still aren't.
- Lookout: a long row keeps its "(lookout)" or "(here)" tag; row tooltips leave out the coordinates.
- Ultima Tracker: names with any letters now save and load; the save file stays plain text that older versions read.
- Ultima Tracker: a save line with a broken time no longer stops every later save.
- Ultima Tracker: B only uses bandages from your own backpack.
- Ultima Tracker: a player whose name holds "the" is no longer hidden as an NPC.
- Ultima Tracker: with two clients, the last save at Stop is kept, and Ignore, links, learned players, foe sightings and the sightings log from both clients survive.
- Ultima Tracker: a save that fails or has to wait is tried again, and the journal says so once.
- Ultima Tracker: a save file that is busy at start is read again before saving is turned off.
- Ultima Tracker: a grey who turns red or orange in range is alerted again.
- Ultima Tracker: a player only saying "X is attacking you" no longer puts X on the combat bars or in the killer window.
- Ultima Tracker: ordinary speech no longer teaches a titled NPC, so a red who says their own name with "the" still shows and alerts.
- Ultima Tracker: Sightings dates read day first.
- Ultima Tracker: a P, Z, H or C press aims only the cursor its own spell raises; a fizzle, a failed cast, another spell or any other cursor leaves the next cursor to you.
- Ultima Tracker: a doubled click on a combat bar or a spell button acts once.
- Ultima Tracker: the attacker list stays up while you are dead and closes when you are resurrected.
- Ultima Tracker: in streamer mode a clicked foe and the Foe list journal lines show the hidden name.
- Ultima Tracker: Target... no longer puts you, a pet or an animal on the Foe list.
- Ultima Tracker: Reset to defaults leaves a combat window in a zone where it is.
- Lookout: without the Tracker part, titled NPCs no longer raise alarms.
- Lookout: rows read "12 tiles NE"; shorter tooltips.
- Overview: the count shows every mobile in range and stays inside its box.

### Social

- Social: A chat draft now stays on its own tab when you switch tabs or fold the window, so a party message can never end up in the guild chat field.
- Social: The guild read waits a few seconds while Grimoire reads a runebook, so neither window pops up on screen.
- Social: The guild window ids are remembered between Plays, so the first read after start-up stays hidden too.
- Social: A timed guild read leaves a guild window you have open alone; Refresh still reads it.
- Social: The guild read finds its page even when another gump opens at the same moment.
- Social: A timed read no longer wipes your saved roster when a "not in a guild" window is open.
- Social: Colour-blind marks on the Friends and Party tabs now follow each player's current notoriety.
- Social: Saved friend names keep your current friends first.
- Social: A damaged saved guild read time no longer stops the guild from saving.
- Social: A pending party invite no longer rewrites the party line twice on every refresh.
- Social: Party window opens the client's party window directly, so a TazUO macro you have running keeps running.
- Social: Decline also closes TazUO's own invite window.
- Social: Guild lines that are blanked later lose their old tooltip.
- Social: Rows show no health bar while a player's health isn't known yet (it looked like a dead player's).
- Social: A friend you remove in TazUO's own friends list is no longer announced as leaving view.

### Reagent Prices

- Reagent Prices: the SHOPS Add field now really empties after a shop is added.
- Reagent Prices: with two clients open, history rows the other client moved to another shop no longer come back to the old one.
- Reagent Prices: the shop picked in "Which shop?" now stays picked when the question came while the window was minimised and a shop was added or removed before you restored it.
- Reagent Prices: a one-page book is now called "1 page" in the journal, and the Skip old prices tooltip reads clearly.
- Reagent Prices: with two clients open, a save no longer undoes a shop change, a newer read or history rows the other client saved, and a client that saves nothing still takes in the other client's changes.
- Reagent Prices: a read with a reagent code the window doesn't know no longer stops the grid view.
- Reagent Prices: opening a second unknown vendor while "Which shop?" is open no longer loses the first read; it is stored with your answer when it is nearby, or asked next, and the question names the vendor.
- Reagent Prices: a vendor read again after being marked gone comes back when the data file loads.
- Reagent Prices: after Skip, the window shows the cheapest list again instead of every reagent as out.
- Reagent Prices: with a book that holds other writing, the last-read line names the last read again.
- Reagent Prices: the "Which shop?" row no longer shrinks the window's text when it fits at full size.
- Reagent Prices: a buy list is read even when another vendor's sell list is still open.
- Reagent Prices: resizing the window while a list is read keeps the size you dragged it to.
- Reagent Prices: two clients adding a shop at the same time no longer give both shops the same number.
- Reagent Prices: removing a shop no longer reads the open buy list a second time.
- Reagent Prices: the Add field empties after a shop is added, and Add waits until the shop list has loaded.
- Reagent Prices: a book line of what a stop lacks starts with the stop number when the shop name doesn't fit.
- Reagent Prices: Overwrite on a book of more than 18 pages clears the pages after the prices.
- Reagent Prices: the shop picked in "Which shop?" stays picked when a shop is added or removed.
- Reagent Prices: the SHOPS Add button uses the same art as other Add buttons, and the shopping list tooltip gives its range as (0-9999, 0 = not on the list).
- Reagent Prices: a shop name cut at 24 letters can no longer end in half an emoji and stop saving.

### Skills

- Training Alarm: I'm here clears only the alarm's own lines from the banner and ends its pause at once, also while Alerts are quiet; another module's line or alarm stays, and the window and journal say when another alarm still pauses skill loops.
- Training Alarm: switching it off clears its own alarm lines from the banner.
- Training Alarm: a guild member's name label (Grey Fox [WLF]) no longer raises "said your name".
- Skills: a stat that crossed its target while Bless or a potion held it is locked once the change wears off, and the line says where it ended.
- Skills: a skill above 100.0 that is set to go up no longer counts as stuck at the total skill cap.
- Skills: when the client's skill list can't be read, the first list stops at the first skill it can't find, so pins, targets, locks and session gains stay on the right skills.
- Skills: a skill button made for a window at the right edge of the screen goes to the window's left instead of off screen.
- Skill Bags: the "at most 300 done items" line says to move the done items out or split the bag (Reset couldn't help).
- Skill Bags: an Auto rule whose bag the client doesn't know yet says so once.
- Skill Bags: an Auto tool rule with no tool in the backpack says so once instead of every 10 s.
- Skill Bags: a Cartography or Double-click rule with an empty Text asks for part of the item name instead of saying "0 of 0 handled".
- Skill Bags: a rule at 300 done items makes room from items known to have left the bag first, and keeps the ones still in it.
- Skills: the skill sheet and Skill Bags exports are written safely in UTF-8 (letters outside the Windows code page no longer empty the file), and the journal names the VirtueAssistantSettings folder instead of the full path.
- Skills: the exported sheet and results headers no longer use a dash.
- Skills: a stat target no longer locks a stat early while Bless, Curse or a potion changes it; the lock comes once the change has worn off.
- Skills: skill points above 100.0 no longer count toward the total skill cap.
- Skills: no false gains when the window switches from its first skill list to the client's.
- Skills: in a zone, the picked skill section no longer has an empty row at the bottom.
- Skills: the settings page's number fields apply once you stop typing, so typing a total cap no longer prints a false cap warning.
- Skills: the GROUPS "first group" note stays inside the settings page.
- Training Alarm: I'm here no longer clears another module's alarm from the banner, and it clears the banner when it shows an earlier reason of the same alarm.
- Training Alarm: the client's own name labels (a grey wolf near a character called Grey Wolf, your corpse) no longer raise "said your name".
- Training Alarm: a staff member whose name arrives late is still checked.
- Skill Bags: an Auto rule on a bag inside a bag you haven't opened yet stays on and shows closed, instead of switching itself off.
- Skill Bags: a rule with more than 300 items stops with a line instead of handling the same items again.
- Skill Bags: Cartography or Double-click with an empty name filter no longer double-clicks every item.
- Skill Bags: a custom tool graphic out of range is refused with a line.
- Skill Bags: changing a rule's action drops its unfinished item; removing a rule while its bag is being targeted cancels the pick.
- Skill Bags: a damaged saved rule no longer moves the done lists of the rules after it.
- Skill Bags: the delay box accepts a decimal comma.
- Skill Bags: pauses on any module's alarm while the Training Alarm is off.
- Skill Bags: unticking "Pause in guard zones" in town says so, instead of "out of the guard zone".
- Skill Bags: results rows and hint lines keep a 20 px pitch, and an emptied results row drops its old tooltip.

### Property Butler

- Property Butler: a visitor row keeps its player; when a player leaves, their row stays empty for a moment instead of the rows below moving up, so Friend, Eject and Ban act only on the player you aimed at.
- Property Butler: a click on a row in the first second after it shows a new player isn't acted on; it says the row changed, so check the name and click again.
- Property Butler: house and sweep replies said out loud by any player nearby, listed or not, are no longer taken as the house's replies.
- Property Butler: the visits log shows grey visitors as "(grey)".
- Property Butler: after Clear in the visits log, a red or Foe still inside is logged as stepping in again.
- Property Butler: the Ban confirmation setting now says it is for the row's Ban button; Ban... needs no second click.
- Property Butler: a Detect Hidden sweep in your house that finds nobody no longer reports that someone was revealed.
- Property Butler: visits and the red or Foe alarm count only in your own house, and only players standing in that same house; a house becomes yours the first time a Release (or Friend) of yours works there, and stops being yours when the house says you are not a co-owner.
- Property Butler: "This is already locked down" and the house's other refusals (a bigger boot, the ban limit, a friend or vendor that can't be ejected) are logged as failures, and lines that nearby players say are no longer taken as house replies.
- Property Butler: a red or Foe the alert can't show is logged once a visit instead of every 10 s.
- Property Butler: a sweep pause is said in the journal at most once a minute for each reason and is kept out of the action log.
- Property Butler: visitor rows keep their order while players move about, so Friend, Eject and Ban hit the player you aimed at.
- Property Butler: Ban... bans the player you pick at once; the pick is the confirmation.
- Property Butler: Eject..., Ban... and the other picks wait while a sweep is using the target cursor.
- Property Butler: the sweep now waits 3 s between uses by default, the shard's Detect Hidden delay.
- Property Butler: a visit that began before the visitor's name arrived now shows the name.
- Property Butler: the house commands note shows in full on a narrow settings page.
- Property Butler: a damaged time in the saved log or visits is skipped instead of switching the module off.

### Meters

- Meters and Social: with the one-panel look on, the death recap and the note editor open as free windows instead of covering the module's window in its zone.
- Meters: a damaged saved window size or place can no longer freeze the game at login or put a window off screen.
- Meters: a damaged saved window number no longer opens the first Meters window twice.
- Meters: a window in a zone keeps the place it had outside the zone, also right after it is rebuilt.
- Meters: newbied items left in your pack at death are no longer held back from Items gained for an hour, and the first pack change after resurrection is counted.
- Meters: streamer mode keeps hiding the players you saw most recently when its name list is trimmed.
- Meters: a party member's spell words heard as the name list is trimmed are no longer blamed for your damage.
- Meters: saved spots with an overlong name or a place off the map are cut or skipped.
- Meters: Spells cast now counts your own fizzles and "Insufficient mana" casts, and its total counts casts only.
- Meters: skill gains, bandage and fizzle texts other players say are no longer counted as yours.
- Meters: dying no longer counts your pack's gold as spent or its reagents as used, and taking them back from your corpse no longer counts as gold or items gained.
- Meters: gold you already carry no longer shows as gained when Meters starts before your status arrives.
- Meters: mana for a targeted spell goes to that spell when you take a moment to pick the target.
- Meters: a hit that lands as the name list is trimmed keeps the mobile's name instead of "Unknown".
- Meters: streamer mode now hides player names in the death recap, in fight names (segment list, Session summary, minimised bar) and in Report.
- Meters: Export writes UTF-8 and keeps the previous export whole if writing fails.
- Meters: a window in a zone or behind a tab keeps the place it had outside the zone.
- Meters: Reset sizes and Rows per window with Meters off now work on the saved windows.
- Meters: Reset all meters and New meter window say to turn Meters on first while it is off.
- Meters: the death recap and the displays, segment and details lists take a new look or streamer mode at once.
- Meters: the Name this spot row fits a narrow settings page.
- Meters: death recap times read "-3.2 s".

### Mongotchi

- Mongotchi: a damaged or hand-edited save (a stage out of range, or a huge, infinite or missing number) now loads with safe values instead of stopping Mongotchi at every login.
- Mongotchi: a meditation called home before halfway no longer counts as a meditation or towards Pilgrimage.
- Mongotchi: a new pup no longer finishes the old pet's meal, toy or milk nap.
- Mongotchi: the Name tooltip says accents are dropped.
- Mongotchi: Sacrifice reads "+1 food per 4 levels" instead of "+0 food", and Compassion's line is shorter so it fits its Journeys row.
- Mongotchi: Shop > Summon says when your pet is away or has gone wild instead of "flutters out to join you".
- Mongotchi: Shop rows update when a treat arrives, the companion leaves or a price changes.
- Mongotchi: while your pet is away the Playpen shows five visitor places, and a wild pet's empty Playpen no longer says to share its code.
- Mongotchi: a clock set back while Mongotchi was switched off no longer stalls saving, wandering and reminders.
- Mongotchi: "1 squeak" reads right in hunt hauls, Shop tooltips, purchases and companion finds.
- Mongotchi: meals, trips, cooldowns, saving and the companion no longer stall for a while when the computer's clock is set back.
- Mongotchi: the Companion Charm, War Training and Compassion texts no longer say the pet heals you or joins fights; they describe what you see.
- Mongotchi: a treasure hunt called home before halfway no longer counts as a visit, and calling a trip home pays its flat squeaks in proportion.
- Mongotchi: Call home can no longer end a forage early.
- Mongotchi: "the Avatar title is for sale" shows only when the eighth virtue reaches level 5 and you don't own the title yet.
- Mongotchi: the list of visitors told "the playpen is full" no longer grows all session.
- Mongotchi: a gremlin that reaches an empty pantry says so instead of "stole 0 of 0 food".
- Mongotchi: a hunt's haul reads "a sugared peach (x2) and a lucky horseshoe" instead of repeating names.
- Mongotchi: spoken commands work for pet names that start or end with punctuation, and for names that are a command word.
- Mongotchi: the companion's victory squeak now comes when your war target dies nearby.
- Mongotchi: the need bars keep their size when the window is scaled down to fit a narrow zone.
- Mongotchi: "fetch" and "good" rest 20 s between rewards, like "dance".
- Mongotchi: "<name> follow" while the pet is away says it joins you when back.
- Mongotchi: the Adopt button no longer overlaps the farewell line in a short zone.
- Mongotchi: in a zone, the title row's buttons sit at the right edge like other windows'.
- Mongotchi: companion effects are queued without making new functions on every pass.
- Mongotchi: Release needs a second click at least 0.6 s after the first, so a double-click can't release the pet.
- Mongotchi: Share only notes that the pet has gone wild instead of posting its code.
- Mongotchi: your pet leaves the Playpen while it is away on a trip, and a visitor's close button always sends that visitor home.
- Mongotchi: Shop prices and requirement lines update as squeaks and swats change, without reopening the Shop.
- Mongotchi: "1 second" and "1 squeak" read right, the Pace tooltip shows its range and the empty Playpen hint is one short line.

### Main script

- Buttons: a click on a window's button runs its action once again (Skills' Use buttons used the skill twice, and binding a key by clicking a button also pressed it).
- Text: names and labels with wide letters (W, M, Cyrillic or Chinese letters) are shortened to fit instead of spilling out of their box.
- Alerts: with "Show the banner" off, an alarm still pauses skill loops for 30 s.
- Alert History: an alarm without a person's name no longer keeps its alert text as the name.
- Speed: on a client where TazUO's game-thread queue can't be reached, closed text labels are cleared from memory again.
- Snapping: windows rebuilt often (the grid, tab strips, Character HUD's Swing Bar and Bandages bar after a look change) no longer pile up in memory.
- Saving: a typed or pasted name with a broken emoji no longer stops a file saving; the broken letter is saved as ?.
- Saving: two clients sharing a file no longer lose each other's entries when one reads it while the other swaps it in.
- Run alone: a module's settings window is as wide as the main settings column, so its pages fit, and its hotkey page binds work there too.
- Modules: a modules folder that can't be read says so in the journal, and the saved module and part choices are kept for the next start.
- Snapping: a window keeps its snapped and tied neighbours after it is rebuilt (minimised, restored or restyled), even in the middle of a drag.
- Virtue Assistant: A themed module that is off (or a new character's) no longer switches itself on at the next Play with only one part ticked (Inventory with only Supplies).
- Virtue Assistant: Three quick clicks no longer confirm a harmful cursor on a blue or green player in a guard zone; the confirming press needs a short pause after the last click.
- Virtue Assistant: An alarm now pauses Skill Bags and the Inventory trap jobs even with the Training Alarm part off.
- Virtue Assistant: A module that couldn't start because the client didn't answer in time keeps its saved settings and is tried again at the next Play.
- Virtue Assistant: A module's settings page redraws at once when the module starts or stops, for example after errors switch it off.
- Virtue Assistant: Each settings page's buttons now have their own hotkeys, so a key bound to Reset on the Meters page can't press Reset on the Interface page; keys bound to a settings page button before need binding again.
- Virtue Assistant: A damaged backup is refused instead of restored (backups made from this version on), and the Restore list shows the seconds.
- Virtue Assistant: Journal lines keep the time they came in, so an old reply is no longer taken as the answer to a new move, and lines are no longer read again after the clocks go back.
- Virtue Assistant: The What's new window takes a new look or text size at once.
- Virtue Assistant: The guard zone and alerts keep working when a window fails to update, and the pack and journal listeners stay on when the module that started them stops.
- Virtue Assistant: Settings are still saved when the computer's clock goes back.
- Virtue Assistant: Loading a profile or restoring a backup restarts every module even when the window can't be rebuilt, and starts the zone owner first, so windows no longer jump into their zones.
- Virtue Assistant: Profiles no longer copy one character's own progress and lists to another (Skills session, Mongotchi pet, guild roster, Property Butler log and houses), and loading an old profile no longer rolls them back.
- Virtue Assistant: A part that fails to start is switched off with a journal line instead of running half started.
- Virtue Assistant: A part ticked while another part was busy now starts safely, without slowing the game.
- Virtue Assistant: A profile whose settings file can't be read is refused instead of being marked as loaded.
- Virtue Assistant: The favourite profile now puts every module's settings on a character at start, the same as loading it by hand.
- Virtue Assistant: Settings are still saved every second after the computer's clock goes back.
- Virtue Assistant: A module can be run alone at once after the suite is stopped.
- Virtue Assistant: Backing up no longer redraws the whole Virtue Assistant window.
- Virtue Assistant: A profile can no longer be named like the favourite file, and a name cut through an emoji still saves.
- Virtue Assistant: A module's Settings button opens its page even after a settings search.
- Virtue Assistant: Letting go of the gear after dragging it no longer opens the window.
- Virtue Assistant: At a larger scale the window's columns fit the screen height, and "found" or "new" tags no longer cover long part descriptions.
- Virtue Assistant: The journal and the Modules tab say "1 setting" and "1 module on".
- Settings: unticking one part on the Modules tab or in a module's PARTS section turns off only that part again, not the whole module.
- Snapping: windows snapped in a chain can be pulled apart again; dragging the top one no longer locks them together.
- Snapping: a window let go right after a quick drag takes its snapped neighbours all the way.
- Snapping: a tied window whose main window closes snaps and stays on screen again.
- Snapping: snapped windows stay together when the game window changes size.
- Quick Launcher: a window layout deleted since it ran is refused from the last runs instead of freeing every window.
- Quick Launcher: "Window: ..." brings a window behind a tab to the front.
- Quick Launcher: last-run rows show the current caption, so quiet alerts reads "Resume alerts" while quiet is on.
- Grid: its label also names Settings > Interface as a way to hide it.
- Modules: a module file saved as UTF-8 with a byte-order mark loads again, in the suite and run alone.
- Modules: an empty or cut-short module file says so in the journal.
- Run alone: a module's window never fades.
- Saving: a shared file left half-saved by a crash or a stopped script is put back after 5 s instead of being lost, and Reagent Prices keeps saving meanwhile.
- Saving: a data file saved in Notepad as ANSI or Unicode (accented shop or bag names) loads again instead of being refused; it is saved back as UTF-8.
- Text: a name or note cut to fit no longer ends in half an emoji.
- Windows: with more than 48 framed windows open (large parties, many bag windows), windows keep their frame when the screen size changes.
- Windows: a window in a zone no longer saves its zone place as its own place right after it is rebuilt.
- Alerts: unticking "Show the banner" while an alarm is up keeps skill loops paused for 30 s instead of resuming them at once.
- Alerts: a banner holding more than 50 alerts keeps its alarm when the oldest lines are trimmed.
- Hotkeys: a key bound to a settings page button in this version is left unbound in older versions (instead of doing nothing there and blocking the key), and still works when you come back.
- Hotkeys: a settings page button pressed by a key bound in an older version shows that key in its tooltip.
- Settings: slider values read "1 tile", not "1 tiles".
- Virtue Assistant: The journal and backpack listeners stay on when the module or part that first used them stops, and cliloc records waiting for their line are kept.
- Virtue Assistant: When a modules folder can't be read at start, loading a profile or restoring a backup keeps the saved module and part choices, and the journal says once that settings changes aren't saved this session.
- Virtue Assistant: Saving a profile, backing up and restoring work again while settings can't be saved.
- Virtue Assistant: A module whose file can't be read at start keeps its saved choice instead of coming up off at the next start.
- Virtue Assistant: The guard zone, alerts and hotkeys keep working if the Virtue Assistant window can't be built.
- Virtue Assistant: An option picked in the Quick Launcher is marked "found" on its page again.
- Virtue Assistant: A profile name that isn't allowed says so instead of asking for a name.
- Virtue Assistant: Journal lines read just before the computer's clock was set back are no longer taken as new.
- Virtue Assistant: Profiles and backups hold the settings of every module, even one whose settings are named after its title.
- Virtue Assistant: Another player typing "X is attacking you" in red no longer pauses skill loops.
- Run alone: A new part that starts on by default is on in alone runs too, and a part unticked alone stays off.
- Virtue Assistant: The start-up check of TazUO no longer switches Social off over macro parts it doesn't use.

## The review pass

- Rules check R1-R8 on every change (above).
- Round 1: each module and slice of the main script read by its own fresh reviewer, plus whole-program audits
  (damaged saved data, a fuzzer for every saved format, every button and hotkey, every window size and zone,
  text encodings, thread use, docs against code, and writes to client properties that can't be set). Round 2:
  fresh reviewers read every round-1 change, and the audits ran again. Every fix group had its own fresh review
  of its change, and its findings were fixed.
- Older checks that tested the old behaviour on purpose now run only on the old code, each with a new check in
  its place. The test mock now fails on a write to a client property that can't be set (that found the empty
  Share code field).
- Release checks: the IronPython 3.4 compile under TazUO's own IronPython, the mock run with every module and
  with a saved character, every module run on its own, the start-up counter, the item tests, and the checks of
  the installed copy and the release zip.
- Left for a later version: Social's guild read and Grimoire's hidden runebook read can still meet in rare
  timing and show one gump; this was already so in 2.7.0.38. The main script now has the shared claim they will
  use.

## Install

Copy `VirtueAssistantV2-7-0-39.py` and the `VirtueAssistantModules` folder into `TazUO/LegionScripts/`, as
before: the files at the top of the GitHub page, or the zip from the Releases page, which unzips straight into
`TazUO/LegionScripts/`. Replace the whole modules folder, then run the main script. You can delete the 2.7.0.38
main script. The commented `readable` copy of this version comes in a later upload; it is never for
installing.

Only in game:
- World Map marker names now end in a character tag; markers under the old names clear at the next start;
- Get my things in every corpse container style;
- the text widths of Lookout rows and other fitted texts;
- that real attackers still land on Ultima Tracker's bars, and that real "is attacking you" lines still pause
  skill loops;
- a data file saved by Notepad as ANSI or Unicode loading again;
- that Share now fills the Code field.

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
- **2.7.0.38:** Reagent Prices keeps every vendor by name, keeps a price history and has a resizable, scaled
  window.
- **2.7.0.39:** a full bug sweep: about 430 fixes across every module and the main script, each with a test.
