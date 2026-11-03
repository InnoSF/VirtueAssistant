# =============================================================================
#  Inventory  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, Journal, the main loop and the settings window), so run
#  that instead and tick Inventory on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "inventory"
#
#  A module made of PARTS (2.6.5): each part below was a module of its own in
#  2.6.06 and keeps every saved key, window place, list and file it had. A
#  part has its own box under the module's row on the Modules tab (click the
#  arrow on the row to see them) and runs only while it is ticked; the mother
#  script's PartSet runs the ticked parts side by side. The old module keys
#  still answer (the Action Bar's mod: cells, HOST.enable, HOST.by_key).
#
#     Bags             (was UnifiedBag)       Every bag in one window: a grid, filters and sorting
#     Paperdoll        (was Character)        Your character, what you wear and your stats, in one window
#     Storage          (was StorageIndex)     What is in every container you opened, on every character
#     Restock          (was Restock)          Tops your supplies up from a chest or the bank, on a press
#
#  Bags starts before Paperdoll (the paperdoll joins the bag window through
#  the bag.* services) and stops after it, as the two modules did in 2.6.06.
#
#  2.6.82: speed pass: fewer client reads per tick and per frame (the bag
#  canvas, Find, the paperdoll's look, the shared backpack scan), same game.
# =============================================================================


def _module_inventory():
    """Builds the module from its parts and returns its hooks."""
    KEY = "inventory"
    TITLE = "Inventory"


    def _part_bags():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by its mother script from the VirtueAssistantModules folder.
        # =============================================================================
        #  MODULE: Bags  (was Unified Bag; from UnifiedBag v1.5)  -  every bag in one window
        #  For default containers (NOT TazUO grid containers).
        #
        #  Giant-inventory mode (default)
        #    Each assigned bag is trimmed to just its item drop area: the bag artwork is
        #    hidden, the bag's clickable area is shrunk to the area that accepts items,
        #    and the bags are butted edge-to-edge on one shared panel. Items can be
        #    dragged freely from any bag to any other, as if it were one big inventory.
        #    (2.6.78) the bag canvas: in a zone (combined with the Paperdoll, or Bags
        #    alone), the bags fill the zone with no empty margin. The client's bag
        #    windows stay open but hidden, and every item is drawn on one canvas;
        #    each bag has a region sized to its real item area and kept close to its
        #    shape, and an item let go at any pixel stays at that pixel (pinned for
        #    the session; the bag position sent is one the client itself could
        #    send). Container Scale is never changed in a zone. Bags alone in a zone
        #    is one window (the canvas, its title row and side panel), exactly its
        #    slot. See canvas_tick, canvas_parts, canvas_resync, canvas_mouse_up.
        #
        #  Title bar:  [Slots] [Trap bags] [Settings] [Fold into bar] [Minimize] [X]
        #    Minimize (or double-click the title) folds the window to its title bar
        #    and hides the bags in it; restoring shows them again exactly as they
        #    were, minimized or not. The title bar stays on screen, Action Bar or
        #    not. The gold arrow left of Minimize folds it into the Action Bar
        #    instead (title bar hidden too; the bar's bag slots bring it back).
        #    X turns Bags off and gives every bag back to the client as it was.
        #  Side panel (right of the slots, reflows into columns to match the grid):
        #    bag icons = Minimize all / Restore all, spell icons = Magic Trap / Untrap, Stop,
        #    the filter box (filters live as you type; its Find arrow is gone since 2.6.51)
        #    and Sort (with the Sort rules button beside it)
        #  Find (2.6.05): type a name (or a graphic: 0x0F7A or 3962; several terms
        #    with commas) and the matching items in every slot's bag light up for a
        #    few seconds, client-side only (the hue is put back exactly afterwards,
        #    and nothing is sent to the server); each slot shows how many it holds.
        #    Names come from what the client already knows (the tooltip text, else
        #    the item's name, else its tile name). A bag inside a slot's bag that
        #    holds a match lights up too.
        #  Sort (2.6.05): the Sort rules window says what each slot's bag holds
        #    (reagents, gems, potions, scrolls, gold, bandages, or graphics you add
        #    by targeting an item). Sort moves the matching items from the backpack
        #    and the other slots' bags into their bag, one move every SORT_GAP
        #    seconds, and stops on Stop, when another cursor is in use, when you
        #    pick something up, or when a bag is full. Only when you press Sort.
        #  Bags-only toggle: the small gem button at the bottom right hides the title
        #    bar and side panel; the slots move up to where the title bar was. A gilded
        #    knot on the slots' bottom-right corner is the drag handle (closed / empty
        #    slots drag too), with the gem just left of it. Click the gem to bring the
        #    title bar and side panel back. Combined with Paperdoll (one window, the
        #    bags under the doll) the gem stays, at the bottom right of the slots:
        #    there it hides and shows the side panel only, since Paperdoll's window
        #    is the title bar and the frame.
        #  Slots always resize to fit the largest open bag.
        #    Slots     assign / clear bags per slot, auto-fill with open bags
        #    Trap bags tick which bags the side panel's Trap / Untrap buttons cast on
        #    Settings  slots, columns/rows, bag scale, opacity, trim on/off, Diagnose
        #              (the Bags block of the Inventory settings page)
        #
        #  Action Bar link
        #    The Action Bar's bag slots show this window and fold it back "into the
        #    bar" (folded, with the title strip hidden too), as does the gold arrow.
        #    They talk through two shared vars, so this works whether the Action
        #    Bar is merged or runs as its own script. If the bar stops (or is
        #    minimized), the title strip comes back by itself within ten
        #    seconds, and folds in again when the bar returns (the wish is kept by
        #    Virtue Assistant under DOCK_KEY until the window is shown again).
        #
        #  Notes
        #    - Turn OFF TazUO grid containers so bags open as classic container windows.
        #    - "Bag scale" is the client's own Container Scale option (all containers).
        #    - Items inside default containers always draw at full opacity; the client
        #      hard-codes that. "Bag opacity" fades the bag panels (what you see behind
        #      items when trimmed) and the bag art / minimized icons.
        #    - Opacity, Trim and "Scale items" apply instantly; slots, columns, rows and
        #      bag scale apply with the LAYOUT section's Apply button.
        #    - Diagnose (the DEBUG section) prints what the module sees; send it
        #      along if something misbehaves.
        #    - A magic-trapped bag explodes on whoever opens it, including you.
        #      Untrap before opening (for example after a relog).
        #    - Settings are saved per character in a hidden file next to this script.
        #    - Windows snapped on to the Bags window (Virtue Assistant's window
        #      snapping) stay anchored to it when its edges move: bags only on or
        #      off, the side panel coming or going, the slots growing. Each one is
        #      put back against the edge it was on, where that edge is now.
        # =============================================================================

        KEY = "bag"                   # module key (the saved keys and shared vars keep their names)
        TITLE = "Bags"                # (was "Unified Bag"; the file name and shared vars keep that)

        try:
            import clr
            from System import Array, Object, Byte, Single, Func, UInt16, UInt32
            from System.Reflection import BindingFlags
            HAVE_CLR = True
        except Exception:
            HAVE_CLR = False

        # ----------------------------- tunable defaults ------------------------------
        DEFAULT_SLOTS = 8
        MIN_SLOTS, MAX_SLOTS = 1, 50
        BACKPACK_INTERIOR = (142, 94)   # backpack drop area at 100% scale
        LOOSE_CELL = (150, 130)         # starting slot size when trimming is off
        MAX_CELL = 600
        LOOSE_GAP = 4                   # gap between slots when trimming is off
        SHRINK_MIN = 30                 # (2.6.67) the least container scale (%) the combined
        #                                 grid is shrunk to so it fits its zone (Bag scale's floor;
        #                                 2.6.73: 30, was 50, so the bags fit their zone whatever)
        # (2.6.78) the bag canvas (see canvas_tick): in a zone, one canvas the bags share
        CLOSED_W, CLOSED_H = 104, 64    # a closed (or minimized) bag's share: its region's shape
        SPLIT_KEEP = 0.10               # a resize keeps its layout unless a new one costs 10% less
        COLUMNS_BEAT = 0.8              # columns only when they cost under 0.8 of the rows
        SPLIT_SLOW = 0.002              # s: a split slower than this runs on the script thread after
        DRAG_RANGE = 3                  # TazUO Constants.DRAG_ITEMS_DISTANCE
        SOUND_CANT = 0x0051             # the client's "can't drop it there" sound
        PIN_CAP = 1000                  # pins kept (memory only); full: the oldest 500 go
        BOARDS = (0x091A, 0x092E)       # the chessboard and backgammon board gumps
        STACK_ON = (0x0EFA, 0x2253, 0x2252, 0x238C, 0x23A0, 0x2D50)   # items that take a drop
        #                                 (ContainerGump.OnMouseUp: keep the two lists in step)
        LABEL_MIN_W, LABEL_MIN_H, LABEL_TWO_H = 60, 30, 46   # a region's labels: none / one line
        LABEL_PITCH = 20                # px between a region's two label lines
        LABEL_LINE_H = 20               # the label line a click on minimizes an open bag
        COUNT_DIGITS = "999"            # the room a region's item count is cut for
        SHRINK_KEY = "UnifiedBag_shrunk"   # (2.6.67) per character: "pct|items" of your own Bag
        #                                    scale while the grid is shown shrunk ("" when not)
        BAR_H = 44                      # stone title bar above the slots
        BAR_MIN_W = 500                 # room for the title and its six buttons
        SIDE_COL_W = 132              # side button panel: width of one column
        SIDE_BTN_W = 116
        SIDE_RIM = 6                  # stone visible round the side panel's black section
        SIDE_PAD = 8
        SIDE_GAP = 5
        SIDE_SEP_H = 9
        ICON_BOX = (36, 32)           # max size of the minimize / maximize bag icons
        DEFAULT_ICONS = (0x003C, 0x0050)   # backpack art, minimized backpack
        ICON_MAGIC_TRAP = 0x1B64      # spellbook icons for the two spells
        ICON_MAGIC_UNTRAP = 0x1B65
        ART_BARE = (2117, 2118, 2118) # small gem button: bags-only on / off
        BARE_PAD = 4                  # space round the bags-only button
        PANE_OVERHANG = 20            # (2.6.72) px (at 100%) an item's art may reach past its bag's item area
        SCREEN_SLACK = 24             # 2.6.81: px kept under the free window's slots (the gem)
        GRIP_OUT = 10                 # bags only: how far the gilded corner knot sticks out of the slots
        CATCHER_TAG = 0x7E57CA7C      # marks our drop catchers, even ones left by an earlier run
        FIT_STABLE_TICKS = 3          # slot size must stay the same this many ticks before resizing
        TICK = 0.1
        DRIVE_TICK = 0.05             # faster ticks when the script drives the bags itself
        SCAN_EVERY_FRAMES = 6
        FRONT_LOOK = 8                # bag windows the client just opened go in at the front of its
                                      # window list: this many are looked at whenever that front changes
        HOOK_STALL = 0.5              # seconds without a draw-hook call before the script keeps the bags
        FULL_GAP = 0.09               # ...and never more often than this (seconds): see frame_tick
        SAVE_DELAY_TICKS = 20
        OPACITY_SETTLE_POLLS = 4      # settings polls the opacity slider must hold still before it applies
        DETACH_SETTLE = 0.3           # seconds after parting from Paperdoll before the place is saved again
        GEM_BELOW = 2                 # the gem sits this far under the slots (bags only / combined)
        NAME_CACHE_CAP = 200          # bag names remembered per serial (cleared when the slots change)

        TRAP_MANA = 6                   # 2nd circle
        TRAP_TARGET_TIMEOUT = 5.0
        TRAP_RECOVERY = 1.3
        TRAP_CAST_MIN = 1.0             # 2.6.81: seconds before a cast's cursor can come (2nd circle
                                        # takes longer, +0.5 s on this shard): an earlier cursor isn't ours
        TRAP_RETRY_PAUSE = 1.0
        TRAP_RETRIES = 3
        J_FIZZLE = ["fizzles", "concentration is disturbed"]
        J_BUSY = ["already casting", "not yet recovered"]
        J_REAGENTS = ["More reagents are needed"]
        J_MANA = ["Insufficient mana", "not have enough mana"]

        # item search (Find, 2.6.05): client-side hues only, nothing sent to the server
        SEARCH_HUE = 0x0044             # the hue matching items light up in (68: bright green)
        SEARCH_LIT = 8.0                # seconds they stay lit
        SEARCH_SETTLE = 0.15            # seconds after the last key before the box searches (2.6.51:
        #                                 it filters live as you type; was 0.6 with a Find arrow)
        SEARCH_MIN = 2                  # characters before the box searches by itself (Find: any)
        SEARCH_SCAN_CAP = 3000          # items looked at per search, every slot together
        SEARCH_LIT_CAP = 400            # items lit at once
        SEARCH_DEPTH = 8                # bags inside bags followed to find what a slot's bag holds
        HUE_MEMORY = 2.0                # seconds a put-back hue is remembered (see light)
        TILE_NAME_CAP = 600             # tile names remembered per graphic
        # sort (2.6.05): rules per slot; moves only when the player presses Sort
        SORT_GAP = 0.7                  # seconds between two moves (the shard's drag delay: unchecked)
        SORT_CAP = 600                  # moves planned by one Sort
        SORT_FAIL_STOP = 3              # moves refused in a row before Sort gives up
        SORT_RECHECK = 2                # extra looks at a move the server hasn't answered yet
        SORT_GRAPHICS_CAP = 24          # graphics added by target, per slot
        BAG_MAX_ITEMS = 125             # items a bag holds, nested ones counted (RunUO's default: unchecked)
        J_FULL = ["cannot hold more"]   # "That container cannot hold more items / weight." (unchecked)
        J_WAIT = ["must wait to perform another action"]   # cliloc 500119
        # what a slot's bag can hold: (key saved in the file, caption, graphics); the
        # graphics are the classic tile ids (Tiledata), edit here if the shard differs
        SORT_KINDS = (
            ("reagents", "Reagents", (0x0F7A, 0x0F7B, 0x0F84, 0x0F85, 0x0F86, 0x0F88, 0x0F8C,
                                      0x0F8D)                  # the eight of Kit.REAGENTS
             + (0x0F78, 0x0F7D, 0x0F8A, 0x0F8E, 0x0F8F)),      # + bat wing, daemon blood,
            #                                                     pig iron, nox crystal, grave dust
            ("gems", "Gems", tuple(range(0x0F0F, 0x0F31))),     # star sapphire .. diamond, amber
            ("potions", "Potions", tuple(range(0x0F06, 0x0F0E))),   # black .. purple (not empty bottles)
            ("scrolls", "Scrolls", tuple(range(0x1F2D, 0x1F6D)) + (0x0EF3,)),   # 64 spells + blank
            ("gold", "Gold", (0x0EED, 0x0EEE, 0x0EEF)),
            ("bandages", "Bandages", (0x0E21, 0x0EE9)),         # clean bandages
        )
        SORT_KIND_KEYS = tuple(k[0] for k in SORT_KINDS)

        C_SEAM = "#5C544A"              # stone-grey lines between slots
        C_EDGE = "#7A7066"              # stone-grey edge round the slots

        HUE_OK, HUE_INFO, HUE_ERR = Kit.HUE_GOOD, Kit.HUE_INFO, Kit.HUE_BAD   # journal hues (2.6.52:
        #                                                                    info lines grey, not gold)

        LINK_CMD = "UnifiedBag_cmd"      # Action Bar -> here: "show" / "dock"
        LINK_STATE = "UnifiedBag_state"  # here -> Action Bar: open / collapsed / docked / off
        DOCK_KEY = KEY                   # the fold-into-the-bar wish, kept by the host

        # --------------------------------- state -------------------------------------
        class Bag(object):
            pass

        st = Bag()
        st.slots = DEFAULT_SLOTS
        st.cols = 0                  # 0 = auto
        st.rows = 0                  # 0 = auto
        st.assign = {}               # slot index (0-based) -> container serial
        st.frame_x, st.frame_y = 200, 120
        st.saved_fx, st.saved_fy = 200, 120
        st.cell_w, st.cell_h = BACKPACK_INTERIOR
        st.fit_pending = True
        st.fit_seen = None           # (wanted slot size, ticks it has held)
        st.trim = True
        st.opacity = 0.90            # bag panels + bag art / minimized icons
        st.scale_pct = 100           # mirrors the client's Container Scale
        st.scale_items = False
        st.driving = False           # True when the script, not the draw hook, keeps bags in place
        st.drive_fixed = False       # ...for good: the hook couldn't be installed
        st.drive_told = False        # the "hook isn't being called" note was given this run
        st.hb_frame = -1
        st.hb_time = 0.0
        st.opacity_pending = None    # (value, polls unchanged) while the slider moves
        st.icons_used = None
        st.status_text = ""                 # (2.6.72) empty when idle
        st.sort_say = False          # debug (settings page): Sort repeats the server's replies
        st.mgr_x, st.mgr_y = 120, 140
        st.trp_x, st.trp_y = 200, 180
        st.mgr_min = st.trp_min = False
        st.collapsed = False         # window folded to its title bar, bags hidden
        st.docked = False            # folded into the Action Bar: title bar hidden too (not saved)
        st.bare = False              # bags only: title bar and side panel hidden
        st.side_hidden = False       # combined with Paperdoll: the side panel hidden (the gem there)
        st.link_state = None         # last state published for the Action Bar
        st.attach = None             # combined with Paperdoll: the dict it shares (see attach_to)
        st.attach_g = None           # (2.6.66) the Paperdoll gump the grid is attached to
        st.canvas = None             # (2.6.78) the bag canvas: None, "combined" or "alone"
        st.side_pw = 0
        st.detached_at = 0.0         # when we last parted from Paperdoll (no place saved right after)
        st.grid_wh = None            # (w, h) of the slots + side panel as last drawn
        st.names = {}                # container serial -> name, as last read (see bag_name)
        st.wait_player = False
        st.wait_load = False         # 2.6.81: start() waits for the settings file (read on the script thread)
        st.load_wanted = False       # ...which thread_tick reads next
        st.load_text = None          # ...and hands back as (text or None,) for start() to apply
        st.trap_sel = set()
        st.trap_extra = []
        st.job = None
        st.actions = []              # clicks waiting for the module's next pass
        st.reported = False
        st.dirty_frame = True
        st.dirty_mgr = False
        st.dirty_trp = False
        st.open_mgr = st.open_trp = False
        st.want_mgr = st.want_trp = False   # open when last saved
        st.save_in = -1
        st.to_write = None           # (path, text) prepared by save(), written by write_saved()
        st.stopping = False
        st.flt_pick = None           # (2.6.85) the filter waiting for its bag to be picked
        st.quick_at = 0.0            # (2.6.85) when the sidebar's parts were last looked at
        st.filters = []              # (2.6.85) the sort filters, first match wins
        st.open_flt = st.dirty_flt = False
        st.flt_min = False
        st.flt_x, st.flt_y = 260, 120
        st.rules = {}                # slot index -> (frozenset of SORT_KIND_KEYS, tuple of graphics)
        st.sort = None               # the Sort under way (see start_sort), or None
        st.srt_x, st.srt_y = 240, 160    # the Sort rules window
        st.srt_min = False
        st.open_srt = st.want_srt = st.dirty_srt = False
        # published for the draw hook (replaced atomically, never mutated)
        st.layout = ()
        st.geom = (1, BACKPACK_INTERIOR[0], BACKPACK_INTERIOR[1], 0)
        st.bar_raw = None
        st.grid_raw = None
        st.grid_info = (None, False)  # (grid, built bags-only?) published together for the draw hook
        st.slot_raws = ()

        ui = {"side_status": None, "bar": None, "grid": None, "mgr": None, "trp": None,
              "trap_checks": [], "store": ({}, {}),
              "srt": None, "rule_checks": [],                      # the Sort rules window
              "search_box": None,                                  # the side panel's Find box
              "counts": [], "count_state": {}}                     # per slot: the "n found" caption

        # -------------------------------- helpers ------------------------------------
        def act(fn, *args):
            """Click handler: fn(*args) runs on the module's next pass, once, however
            many clicks arrive before then."""
            def _run(*_ignored):
                if (fn, args) not in st.actions:
                    st.actions.append((fn, args))
            return _run

        def run_actions():
            while st.actions:
                fn, args = st.actions.pop(0)
                try:
                    fn(*args)
                except Exception as e:
                    API.SysMsg(TITLE + ": couldn't do that (%s)." % e, HUE_ERR)

        def dispose(key):
            g = ui.get(key)
            if g is not None:
                safe(lambda: g.Dispose())
            ui[key] = None

        def no_mouse(ctrl):
            safe(lambda: ctrl.SetAcceptMouseInput(False))
            return ctrl

        def box(x, y, w, h, color, alpha):
            b = G.CreateGumpColorBox(alpha, color)
            b.SetRect(x, y, w, h)
            return b

        def label(g, text, x, y, hue=None):
            return no_mouse(Kit.add_label(g, text, x, y, hue))

        def framed_window(key, x, y, w, h, title, minimized, on_min, on_close):
            """A stone window with a title section, Minimize and Close. Returns
            (gump, button registry, y below the title)."""
            M = Kit.MARGIN
            g = G.CreateGump(True, True)
            Kit.place(g, x, y, w, h)                     # wholly on screen
            Kit.add_window_frame(g, w, h, corners=not minimized)
            Kit.add_section(g, M, M, w - 2 * M, 30)
            Kit.add_label(g, title, M + 30, M + 7, Kit.HUE_TITLE)
            Kit.title_catcher(g, M, M, w - 2 * M - 84, 30, on_min, key=key)
            store = ({}, {})
            Kit.art_button(g, store, "min", Kit.ART_RESTORE if minimized else Kit.ART_MIN,
                           w - M - 74, M + 7, None,
                           "Restore" if minimized else "Minimize (double-click the title does too)",
                           on_click=on_min)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close",
                           on_click=on_close)
            return g, store, M + 30 + Kit.GAP

        def schedule_save():
            st.save_in = SAVE_DELAY_TICKS

        def short(text, n):
            text = text or ""
            return text if len(text) <= n else text[: n - 1] + "~"

        def get_item(serial):
            return safe(lambda: API.FindItem(serial))

        def bag_name(serial, with_serial=True):
            """The bag's name, read once per serial (API.FindItem is a client call)
            and remembered until the slots change (forget_names)."""
            name = st.names.get(serial)
            if name is None:
                it = get_item(serial)
                if not it:
                    return "0x%08X (not loaded)" % serial
                name = safe(lambda: it.Name, "") or "Container"
                if len(st.names) >= NAME_CACHE_CAP:
                    st.names = {}
                st.names[serial] = name
            return ("%s  0x%08X" % (name, serial)) if with_serial else name

        def forget_names():
            st.names = {}

        # ------------------------------- client interop -------------------------------
        #  Default container windows expose no trim/minimize API to scripts, so this
        #  section reaches into the client (IronPython + .NET reflection). If anything
        #  here fails, the script falls back to plain position pinning.
        R = Bag()
        R.tried = R.ok = False
        R.can_ok = False          # (2.6.78) the bag canvas's classes built (canvas_interop)
        R.error = ""
        R.main_call = None

        H = Bag()                 # state owned by the draw hook (main thread)
        H.frame = 0
        H.gumps = {}              # serial -> ContainerGump
        H.managed = set()         # gumps we have changed
        H.trimmed = set()         # gumps currently trimmed
        H.bounds = {}             # container graphic -> unscaled drop rect (l, t, r, b)
        H.scale = 1.0
        H.max_w = 0
        H.max_h = 0
        H.disabled = False
        H.error = ""
        H.fail_streak = 0
        H.open_count = 0
        H.catchers = {}          # trimmed bag -> its drop catcher
        H.icons = None           # (bag art, minimized icon) of the first open bag
        H.hook_calls = 0          # times the draw hook itself ran (vs. script-driven ticks)
        H.pre_calls = 0           # ...of them from PreDraw (after every update, before any drawing)
        H.glist = None            # the client's window list (UIManager.Gumps; the same list always)
        H.head = None             # its front window and length on the last frame (see front_check)
        H.count = -1
        H.lay = None              # the layout H.want was made from
        H.want = frozenset()      # serials of the bags in the slots
        H.placed = {}            # bag -> ((slot, look, minimized), (w, h), art control, trimmed)
        H.bar_at = None          # where the title bar was on the last frame
        H.full_frame = -1000     # frame of the last full look (see frame_tick)
        H.full_at = 0.0          # and its time
        H.fulls = 0              # full looks so far
        H.labels_for = (None, None)   # (open slots, slot captions) the captions were last set for
        H.meas = {}               # (2.6.73) slot -> (w, h, container scale, minimized) as last placed
        H.opened = frozenset()    # (2.6.73) the slots whose bag is open
        H.hold = None             # (2.6.73) the client's held item (the cursor), once found
        H.ginfo = {}              # (2.6.82) bag window -> (graphic, board): fixed for a window's
        #                           life (the client makes a new window on a reopen)
        H.catch_ok = {}           # (2.6.82) trimmed bag -> (catcher, child count, last child, rect)
        H.gtr = {}                # (2.6.82) bag window -> its TextRenderer (canvas_texts)
        # (2.6.78) the bag canvas's split (canvas_tick), published whole: each slot's
        # region (x, y, w, h) in the canvas's pixels, the slots in order, rows or
        # columns, its break points (kept on a resize: no flip-flop), what each
        # slot holds (kind, the bag's graphic, its serial), and a version: a new
        # version drops the pins and draws every item again
        CANVAS = {"ver": 0, "regions": {}, "order": [], "orient": "rows", "breaks": None,
                  "sig": None, "items": None, "kinds": {}, "size": None, "slow": False,
                  "job": None, "done": None}
        JR = {"rd": None}         # a journal reader (canvas_say_tick's fallback), made at start
        PIN = {}                  # item serial -> (bag, bag x, bag y, centre x, centre y): see pin_set
        PIN_ORDER = []            # their serials, oldest first
        # the canvas itself (client thread): its control, where it sits in the grid,
        # the split it was built for, its parts (background, seams, icons, labels,
        # counts), one layer per region (that bag's items, in the bag's order), the
        # item controls by serial, which bag each is in, each bag's items as drawn,
        # what the change detector saw last (child count, last child, minimized),
        # each item's spot (centre x, top) for its single-click text
        CV = {"ctrl": None, "rect": None, "built": -1, "bsize": None, "parts": [],
              "icons": [], "bg": None, "layers": {}, "pool": {}, "owner": {}, "items": {},
              "seen_n": {}, "seen_last": {}, "seen_min": {}, "spot": {}, "label": {},
              "count": {}, "tip": None, "texts": True, "said": None, "sum_i": 0, "sums": {},
              "art": {}, "world": None, "tiles": None, "say_lbl": None, "under": set(),
              "prof_at": 0.0, "sum_at": 0.0, "sum_part": None, "alpha_set": None,
              "say_shown": False}

        def init_interop():
            if not HAVE_CLR:
                R.error = "clr module unavailable"
                return
            try:
                asm = API.GetType().Assembly
                clr.AddReference(asm)
                from ClassicUO.Game.Managers import MainThreadQueue
                from ClassicUO.Game.UI.Controls import Control
                from ClassicUO.Game.UI.Gumps import ContainerGump
                from ClassicUO.Game.UI.Controls import ClickPriority

                inst = BindingFlags.Instance | BindingFlags.NonPublic
                stat = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                cg = clr.GetClrType(ContainerGump)
                R.MTQ = MainThreadQueue
                R.ContainerGump = ContainerGump
                R.f_data = cg.GetField("_data", inst)
                R.f_pic = cg.GetField("_gumpPicContainer", inst)
                R.f_hit = cg.GetField("_hitBox", inst)
                ctl = clr.GetClrType(Control)
                R.m_offset = ctl.GetMethod("SetHitTestOffset", inst)
                # X/Y/Width/Height are by-reference properties IronPython can't use, so
                # positions go through Location and sizes through the private _bounds field.
                R.f_bounds = ctl.GetField("_bounds", inst)
                R.Point = clr.GetPythonType(ctl.GetProperty("Location").PropertyType)
                R.Rect = clr.GetPythonType(R.f_bounds.FieldType)
                uim = asm.GetType("ClassicUO.Game.Managers.UIManager")
                R.p_gumps = uim.GetProperty("Gumps", stat)
                R.p_cscale = uim.GetProperty("ContainerScale", stat)
                pm = asm.GetType("ClassicUO.Configuration.ProfileManager")
                R.p_profile = pm.GetProperty("CurrentProfile", stat)
                # the script wrapper's client control: a fast path only; raw_of also
                # finds it by its "Control" property on whatever the wrapper class is
                # called in this build (Kit.client_control), so a renamed wrapper class
                # no longer turns the whole trimming off
                base = asm.GetType("ClassicUO.LegionScripting.ApiClasses.ApiUiBaseControl")
                R.p_ctrl = base.GetProperty("Control", inst) if base is not None else None
                for name in ("f_data", "f_pic", "f_hit", "m_offset", "f_bounds", "p_gumps",
                             "p_cscale", "p_profile"):
                    if getattr(R, name) is None:
                        raise Exception("client member not found: " + name)

                class FrameHook(Control):
                    """Invisible control on the slots' window. Its PreDraw runs every
                    frame on the client thread after the client has updated every
                    window (a bag rebuilt, opened, reopened or re-shown) and before
                    anything is drawn, whatever the window order and even while the
                    slots are hidden, so a bag is never drawn untrimmed. (Draw used to
                    do this: it missed a hidden slots window and anything the client
                    did between that window's draw and a bag's.) Draw is only the
                    fallback for a client without PreDraw."""
                    def PreDraw(self):
                        H.pre_calls += 1
                        H.hook_calls += 1
                        guarded_tick()

                    def Draw(self, batcher, x, y):
                        if H.pre_calls == 0:
                            H.hook_calls += 1
                            guarded_tick()
                        return True

                class DropCatcher(Control):
                    """Invisible, mouse-accepting area under a trimmed bag's items. Clicks and drops
                    bubble up to the bag window itself, so the client handles them as usual."""
                    def Draw(self, batcher, x, y):
                        return True

                R.Hook = FrameHook
                R.Catcher = DropCatcher
                R.LowPriority = ClickPriority.Low
                R.ok = True
            except Exception as e:
                R.ok = False
                R.error = str(e)
                return
            canvas_interop()

        def canvas_interop():
            """(2.6.78) The bag canvas's client classes. Any that won't build leaves
            the canvas off (canvas_ok False): the zone keeps 2.6.77's own forms."""
            R.can_ok = False
            try:
                from ClassicUO.Game.UI.Controls import Control, ItemGump

                class BagCanvas(Control):
                    """The canvas: every slot's bag drawn on one control filling the
                    zone, clipped to it. It takes the mouse at low priority, so its
                    items win; a press, a let-go, a double-click and the tooltip on
                    empty space, a label or an icon are its own (canvas_mouse_up,
                    canvas_double, canvas_hover)."""
                    def Draw(self, batcher, x, y):
                        try:
                            w, h = self.va_wh
                        except Exception:
                            return True
                        try:
                            canvas_rehide()
                        except Exception:
                            pass
                        if batcher.ClipBegin(int(x), int(y), int(w), int(h)):
                            try:
                                Control.Draw(self, batcher, x, y)
                                if CV["texts"]:
                                    canvas_texts(batcher, int(x), int(y))
                            finally:
                                batcher.FlushBatch()   # drawn under its own clip, nested or not
                                batcher.ClipEnd()
                        return True

                    def OnMouseUp(self, x, y, button):
                        try:
                            if canvas_mouse_up(int(x), int(y), button):
                                return
                        except Exception as e:
                            H.error = "canvas: %s" % e
                        Control.OnMouseUp(self, x, y, button)

                    def OnMouseDoubleClick(self, x, y, button):
                        try:
                            if canvas_double(int(x), int(y), button):
                                return True
                        except Exception as e:
                            H.error = "canvas: %s" % e
                        return Control.OnMouseDoubleClick(self, x, y, button)

                    def OnMouseOver(self, x, y):
                        try:
                            canvas_hover(self, int(x), int(y))
                        except Exception:
                            pass
                        Control.OnMouseOver(self, x, y)

                class BagLayer(Control):
                    """One region's items, in its bag's own order (the layers go in slot
                    order, so a later bag's items draw over an earlier neighbour's).
                    Takes no mouse itself; its items do."""
                    pass

                class CanvasItem(ItemGump):
                    """An item on the canvas: the client's own item control (press and
                    drag lifts it, double-click uses it, its tooltip is the item's);
                    a let-go on it is noted for the canvas, which decides."""
                    def OnMouseUp(self, x, y, button):
                        R.up_item = self
                        ItemGump.OnMouseUp(self, x, y, button)

                R.Canvas, R.Layer, R.CanvasItem, R.ItemGump = BagCanvas, BagLayer, CanvasItem, ItemGump
                R.up_item = None
                R.Mouse = Tz.T("ClassicUO.Input.Mouse")
                R.Actions = Tz.T("ClassicUO.Game.GameActions")
                # the tile data (is it a container, a stack), as the Paperdoll part finds it
                from System import AppDomain
                for a in AppDomain.CurrentDomain.GetAssemblies():
                    t = a.GetType("ClassicUO.Assets.TileDataLoader")
                    if t is not None:
                        R.f_tiles = t.GetField("_staticData", BindingFlags.Static | BindingFlags.NonPublic)
                        break
                else:
                    R.f_tiles = None              # (a drop on an item then goes to its bag window)
                R.can_ok = True
            except Exception as e:
                R.can_ok = False
                H.error = "canvas: %s" % e

        def make_hook():
            try:
                h = R.Hook()
            except Exception:
                h = R.Hook(None)
            h.AcceptMouseInput = False
            return h

        def add_hook(grid):
            """Put a draw hook on a new slots window. On the client thread it goes
            straight onto the client's control (the script wrapper's Add only
            queues it, which can leave a frame or two with no hook at all)."""
            hook = make_hook()
            raw = st.grid_info[0]
            if raw is not None and safe(Client.on_client_thread, False):
                try:
                    hook.Parent = raw                 # (on the client thread: added at once)
                    if raw.Children.Contains(hook):
                        return
                except Exception:
                    pass
            grid.Add(hook)

        _raw_way = {}             # wrapper type -> the way to its client control that worked

        def _raw_gump(w):
            return w.Gump

        def _raw_ctrl(w):
            return R.p_ctrl.GetValue(w)

        def _raw_kit(w):
            return Kit.client_control(w)

        RAW_WAYS = (_raw_gump, _raw_ctrl, _raw_kit)

        def raw_of(wrapper):
            """The client's own control behind a script control (or None). The way
            that worked is kept per wrapper type, so a window of a hundred captions
            doesn't raise and catch a hundred missing-attribute errors."""
            if wrapper is None:
                return None
            t = type(wrapper)
            way = _raw_way.get(t)
            if way is not None:
                try:
                    v = way(wrapper)
                    if v is not None:
                        return v
                except Exception:
                    pass
            for fn in RAW_WAYS:
                if fn is way:
                    continue
                try:
                    v = fn(wrapper)
                except Exception:
                    continue
                if v is not None:
                    _raw_way[t] = fn
                    return v
            return None

        def on_main(fn, *args):
            """Run fn on the client thread and wait for it. Exceptions never reach the client.
            Already on the client thread (the module's tick runs there): fn runs in place."""
            out = {}

            def run():
                try:
                    out["v"] = fn(*args)
                except Exception as e:
                    out["e"] = str(e)
                except:
                    out["e"] = "unknown error"

            if safe(Client.on_client_thread, False):
                run()
                if "e" in out:
                    raise Exception(out["e"])
                return out.get("v")
            if R.main_call is None:
                R.main_call = pick_main_call()
            R.main_call(run)
            if "e" in out:
                raise Exception(out["e"])
            return out.get("v")

        def pick_main_call():
            """Find a way to run code on the client thread that works in this IronPython build."""
            def generic(run):
                R.MTQ.InvokeOnMainThread[object](Func[object](run))

            def inferred(run):
                R.MTQ.InvokeOnMainThread(Func[object](run))

            def with_event(run):
                from System import Action
                from System.Threading import ManualResetEventSlim
                done = ManualResetEventSlim(False)

                def wrapped():
                    try:
                        run()
                    finally:
                        done.Set()
                R.MTQ.EnqueueAction(Action(wrapped))
                done.Wait(5000)

            for candidate in (generic, inferred, with_event):
                probe = {}

                def run_probe():
                    probe["ok"] = True
                try:
                    candidate(run_probe)
                    if probe.get("ok"):
                        return candidate
                except Exception:
                    continue
            raise Exception("no way to reach the client thread")

        def guarded_tick():
            try:
                frame_tick()
                H.fail_streak = 0
            except Exception as e:
                H.error = str(e)
                H.fail_streak += 1
            except:
                H.error = "unknown error"
                H.fail_streak += 1
            if H.fail_streak > 120:          # failing every frame for ~2s: give up cleanly
                H.disabled = True

        def set_offset(g, x, y):
            off = g.Offset
            if off.X != x or off.Y != y:
                R.m_offset.Invoke(g, Array[Object]([x, y]))

        def scan_gumps():
            found = {}
            lst = R.p_gumps.GetValue(None)
            H.glist = lst
            node = lst.First
            while node is not None:
                v = node.Value
                if isinstance(v, R.ContainerGump) and not v.IsDisposed:
                    found[int(v.LocalSerial)] = v
                node = node.Next
            H.gumps = found
            try:
                H.scale = float(R.p_cscale.GetValue(None))
            except Exception:
                pass

        def front_check():
            """A bag window the client opened or replaced (reopening a bag disposes
            its window and adds a new one) goes in at the front of the client's
            window list. Whenever that front changes, the first few windows are
            looked at, so a bag of the slots is pinned and trimmed before its
            first frame instead of showing its art until the next full look.
            Otherwise this is three reads a frame."""
            lst = H.glist
            if lst is None:
                return
            node = lst.First
            head = node.Value if node is not None else None
            cnt = lst.Count
            if head is H.head and cnt == H.count:
                return
            H.head, H.count = head, cnt
            want = H.want
            if not want:
                return
            gumps = H.gumps
            n = 0
            while node is not None and n < FRONT_LOOK:
                v = node.Value
                if isinstance(v, R.ContainerGump) and not v.IsDisposed:
                    ser = int(v.LocalSerial)
                    if ser in want and gumps.get(ser) is not v:
                        gumps[ser] = v
                node = node.Next
                n += 1

        def interior(g):
            graphic = int(g.Graphic)
            b = H.bounds.get(graphic)
            if b is None:
                r = R.f_data.GetValue(g).Bounds
                b = (int(r.X), int(r.Y), int(r.Width), int(r.Height))  # Width/Height are right/bottom edges
                H.bounds[graphic] = b
            s = H.scale
            left, top = int(b[0] * s), int(b[1] * s)
            return left, top, int(b[2] * s) - left, int(b[3] * s) - top

        def cell_xy(idx):
            cols, cw, ch, gap = st.geom
            r, c = divmod(idx, cols)
            return st.frame_x + c * (cw + gap), st.frame_y + top_off() + r * (ch + gap)

        def get_pos(c):
            loc = c.Location
            return int(loc.X), int(loc.Y)

        def move(c, x, y):
            loc = c.Location
            if loc.X != x or loc.Y != y:
                c.Location = R.Point(x, y)

        def get_size(c):
            r = R.f_bounds.GetValue(c)
            return int(r.Width), int(r.Height)

        def release(g):
            """Give a bag back to the client exactly as it was."""
            H.managed.discard(g)
            H.placed.pop(g, None)
            was_trimmed = g in H.trimmed
            H.trimmed.discard(g)
            if g.IsDisposed:
                H.catchers.pop(g, None)
                return
            remove_catcher(g)
            if not g.IsVisible:
                g.IsVisible = True
            set_offset(g, 0, 0)
            g.AcceptMouseInput = True
            g.CanMove = True
            pic = R.f_pic.GetValue(g)
            if pic is not None:
                pic.Alpha = 1.0
            if was_trimmed and not g.IsMinimized:
                g.RequestUpdateContents()  # client rebuilds art, size and minimize button

        def detach(g, c):
            kids = g.Children
            while kids.Contains(c):
                kids.Remove(c)

        def drop_child(g, c):
            detach(g, c)
            if not c.IsDisposed:
                c.Dispose()

        def remove_catcher(g):
            H.catch_ok.pop(g, None)
            c = H.catchers.pop(g, None)
            if c is not None:
                drop_child(g, c)

        def purge_stray_catchers(g):
            """Drop catchers from an earlier run (or a stale copy) would steal clicks from items."""
            mine = H.catchers.get(g)
            for child in list(g.Children):
                if child is not mine and int(child.LocalSerial) == CATCHER_TAG:
                    drop_child(g, child)

        def ensure_catcher(g, left, top, iw, ih):
            c = H.catchers.get(g)
            kids = g.Children
            # (2.6.82) as placed last time (same catcher, same child list by its
            # count and last child, same rect): nothing to look at again
            n = kids.Count
            ok = H.catch_ok.get(g)
            if ok is not None and c is not None and ok[0] is c and ok[1] == n \
                    and ok[2] is (kids[n - 1] if n else None) and ok[3] == (left, top, iw, ih) \
                    and not c.IsDisposed:
                return
            if c is None or c.IsDisposed or not kids.Contains(c):
                if g not in H.catchers:
                    purge_stray_catchers(g)
                c = R.Catcher()
                c.LocalSerial = CATCHER_TAG
                c.AcceptMouseInput = True
                c.Priority = R.LowPriority   # items in the bag always win the click
                # Setting Parent already appends the control; move that single entry to the front
                # so items (later in the list) are hit-tested after it. Control.Insert would add it twice.
                c.Parent = g
                detach(g, c)
                kids.Insert(0, c)
                H.catchers[g] = c
            elif kids.IndexOf(c) != 0 or kids.LastIndexOf(c) != 0:
                detach(g, c)
                kids.Insert(0, c)
            r = R.f_bounds.GetValue(c)
            if (r.X, r.Y, r.Width, r.Height) != (left, top, iw, ih):
                R.f_bounds.SetValue(c, R.Rect(left, top, iw, ih))
            if not c.IsVisible:
                c.IsVisible = True
            n = kids.Count
            if len(H.catch_ok) >= GINFO_CAP:
                H.catch_ok.clear()
            H.catch_ok[g] = (c, n, kids[n - 1] if n else None, (left, top, iw, ih))

        GINFO_CAP = 64                  # (2.6.82) bag windows remembered by gump_info

        def gump_info(g):
            """(2.6.82) (graphic, board) of a bag window, read once per window: a
            ContainerGump sets its Graphic only when it is made (IsChessboard and
            IsBackgammonBoard are tests of it; a reopen is a new window), so
            neither changes while the window lives."""
            gi = H.ginfo.get(g)
            if gi is None:
                gi = (int(g.Graphic), bool(g.IsChessboard or g.IsBackgammonBoard))
                if len(H.ginfo) >= GINFO_CAP:
                    H.ginfo.clear()
                H.ginfo[g] = gi
            return gi

        def place_bag(g, idx, trim):
            """Pin one open bag into its slot; trimmed to its drop area when trim is on.
            Returns (w, h, art, trimmed): the size the slot needs (0, 0 for a
            minimized bag), the bag's art control as placed (the client makes a
            new one whenever it rebuilds the bag) and whether it was trimmed."""
            if g.CanMove:
                g.CanMove = False
            set_offset(g, 0, 0)              # undo hit-area shifts left by older versions
            cx, cy = cell_xy(idx)
            board = gump_info(g)[1]

            if g.IsMinimized or board or not trim:
                if g in H.trimmed:
                    H.trimmed.discard(g)
                    remove_catcher(g)
                    if not g.IsMinimized:
                        g.RequestUpdateContents()
                if not g.AcceptMouseInput and g.IsVisible:
                    g.AcceptMouseInput = True
                pic = R.f_pic.GetValue(g)
                if pic is not None and abs(pic.Alpha - st.opacity) > 0.01:
                    pic.Alpha = st.opacity
                move(g, cx, cy)
                if g.IsMinimized:
                    return 0, 0, pic, False
                w, h = get_size(g)
                return w, h, pic, False

            # Trimmed: hide the art + minimize button, stop the bare window from taking
            # clicks (so a neighbour's window can't steal them), and catch clicks/drops
            # only over the item area. The window keeps its normal size and coordinates.
            left, top, iw, ih = interior(g)
            pic = R.f_pic.GetValue(g)
            if pic is not None and pic.IsVisible:
                pic.IsVisible = False
            hit = R.f_hit.GetValue(g)
            if hit is not None and hit.IsVisible:
                hit.IsVisible = False
            if g.AcceptMouseInput:
                g.AcceptMouseInput = False
            ensure_catcher(g, left, top, iw, ih)
            move(g, cx - left, cy - top)
            H.trimmed.add(g)
            # (2.6.72) the slot also holds the items' art past the item area's right and
            # bottom edges (an item's top-left is kept inside it, not its picture), so
            # the art no longer runs over the next slot or the side panel
            ov = int(round(PANE_OVERHANG * H.scale))
            return iw + ov, ih + ov, pic, True

        def frame_tick():
            if H.disabled or st.stopping:
                return

            bar = st.bar_raw
            grid, gbare = st.grid_info        # the mode the grid on screen was built in
            moved = False
            att = st.attach
            hidden = st.collapsed
            if att is not None:
                # combined with Paperdoll: its window leads, the slots sit in its
                # hole (dx, dy), and the bags hide with it
                hidden = hidden or not att.get("shown", True)
                lead = attach_raw()
                if lead is not None and not lead.IsDisposed:
                    bx, by = get_pos(lead)
                    bx, by = bx + int(att.get("dx", 0)), by + int(att.get("dy", 0))
                    moved = (bx, by) != H.bar_at
                    H.bar_at = (bx, by)
                    st.frame_x, st.frame_y = bx, by
                    if grid is not None and not grid.IsDisposed:
                        move(grid, bx, by)
                        if grid.IsVisible == hidden:
                            grid.IsVisible = not hidden
            else:
                # bags only: the slots are dragged directly and the hidden title bar
                # follows; otherwise the title bar leads and the slots follow
                if gbare and grid is not None and not grid.IsDisposed:
                    lead, other, dy = grid, bar, 0
                else:
                    lead, other, dy = bar, grid, BAR_H
                if lead is not None and not lead.IsDisposed:
                    bx, by = get_pos(lead)
                    moved = (bx, by) != H.bar_at
                    H.bar_at = (bx, by)
                    st.frame_x, st.frame_y = bx, by
                    if other is not None and not other.IsDisposed:
                        move(other, bx, by + dy)

            lay = st.layout
            if lay is not H.lay:                       # (st.layout is only replaced when it changes)
                H.lay = lay
                H.want = frozenset([s for _, s in lay])

            # Every sixth frame, but not more than about ten times a second,
            # everything is looked at again (new bags found, every bag placed); in
            # between only what changed. (Was: every sixth frame, so a client at 144
            # fps did 24 full looks a second instead of 10; at 60 fps or less it is
            # the same as before.)
            H.frame += 1
            now = time.time()
            full = H.frame - H.full_frame >= SCAN_EVERY_FRAMES and now - H.full_at >= FULL_GAP
            if full:
                H.full_frame, H.full_at = H.frame, now
                H.fulls += 1
                scan_gumps()
            else:
                front_check()                          # a bag window opened / replaced just now
            rescanned = full
            icons_due = full and H.fulls % 10 == 1       # the bags' own art, about once a second
            full = full or moved

            trim = st.trim
            # what a placement depends on besides the bag itself: the slots' size and
            # layout too, so a bag follows a rebuilt grid on the same frame
            look = (trim, st.opacity, st.geom, top_off(), CANVAS["ver"])
            active = set()
            opened = set()
            mw = mh = 0
            first = None
            f_pic = R.f_pic
            canv = st.canvas is not None and not hidden
            if canv:                                   # (2.6.78) where hidden windows are parked
                cr = CV["rect"] or (0, 0, 0, 0)
                px, py = st.frame_x + cr[0], st.frame_y + cr[1]
                park = full or st.driving
                seen = (CV["seen_n"], CV["seen_last"], CV["seen_min"])
            for idx, serial in lay:
                g = H.gumps.get(serial)
                if g is None:
                    continue
                if g.IsDisposed:                       # (2.6.82: read once)
                    if rescanned:
                        continue
                    # closed, or reopened (a new window) and missed by front_check:
                    # one look at every window, at most once a frame
                    rescanned = True
                    scan_gumps()
                    g = H.gumps.get(serial)
                    if g is None or g.IsDisposed:
                        continue
                opened.add(idx)
                if canv:
                    try:
                        if canvas_bag(g, serial, px, py, park, seen):
                            if first is None:
                                first = g
                            active.add(g)
                            H.managed.add(g)
                    except Exception as e:
                        H.error = "bag 0x%08X: %s" % (serial, e)
                    continue
                if first is None:
                    first = g
                active.add(g)
                H.managed.add(g)
                try:
                    if hidden:
                        if g.IsVisible:
                            g.IsVisible = False
                        H.placed.pop(g, None)
                        continue
                    if not g.IsVisible:
                        g.IsVisible = True
                    # Between the full looks a bag is left as it is unless the
                    # client rebuilt it (a new art control: an item moved in or out,
                    # trimmed or not, minimized or not), re-showed a trimmed bag's
                    # art (e.g. "open backpack" on an open backpack), or it was
                    # minimized or restored; this keeps the work every frame small.
                    mini = bool(g.IsMinimized)
                    key = (idx, look, mini)
                    done = H.placed.get(g)
                    pic = f_pic.GetValue(g)
                    if not full and done is not None and done[0] == key and pic is done[2] \
                            and not (done[3] and pic is not None and pic.IsVisible):
                        w, h = done[1]
                    else:
                        w, h, pic, trimmed = place_bag(g, idx, trim)
                        H.placed[g] = (key, (w, h), pic, trimmed)
                        # (2.6.73) its size for the packed area (a minimized bag: its icon)
                        if mini:
                            iw_, ih_ = get_size(g)
                            H.meas[idx] = (iw_, ih_, H.scale, True, None)
                        else:
                            H.meas[idx] = (w, h, H.scale, False,
                                           int(g.Graphic) if trimmed else None)
                    mw, mh = max(mw, w), max(mh, h)
                except Exception as e:          # one odd bag must not stop the others
                    H.error = "bag 0x%08X: %s" % (serial, e)
            H.open_count = len(opened)
            if opened != H.opened:
                H.opened = frozenset(opened)
                for idx in [i for i in H.meas if i not in opened]:
                    H.meas.pop(idx, None)
            if first is not None and icons_due:
                try:
                    iconized = int(R.f_data.GetValue(first).IconizedGraphic) or DEFAULT_ICONS[1]
                    H.icons = (int(first.Graphic), iconized)
                except Exception:
                    pass

            if len(H.managed) > len(active):           # (every active bag is in managed)
                for g in [g for g in H.managed if g not in active]:
                    release(g)

            H.max_w, H.max_h = mw, mh

            # the "#n / name / (closed)" captions of the slots without an open bag:
            # only touched when a bag opened or closed, or the slots were redrawn
            raws = st.slot_raws
            if opened != H.labels_for[0] or raws is not H.labels_for[1]:
                for idx, labs in enumerate(raws):
                    show = idx not in opened
                    for lab in labs:
                        if lab is not None and lab.IsVisible != show:
                            lab.IsVisible = show
                H.labels_for = (opened, raws)

        def canvas_bag(g, serial, px, py, park, seen):
            """(2.6.78) Canvas mode, every frame (the draw hook's pre-draw pass,
            after the client's Update): a slot's bag window stays open but hidden
            (the client shows it again on every contents rebuild), parked at the
            canvas's top-left; its change detector (child count, last child,
            minimized) resyncs its items on the canvas. A game board's window is
            given back and left to the client (False). seen: (2.6.82) CV's
            (seen_n, seen_last, seen_min), bound once a frame by frame_tick."""
            if gump_info(g)[1]:
                if g in H.managed:
                    release(g)
                return False
            if g.IsVisible:
                g.IsVisible = False
            if g.AcceptMouseInput:
                g.AcceptMouseInput = False
            if park:
                if g.CanMove:
                    g.CanMove = False
                move(g, px, py)
            kids = g.Children
            n = kids.Count
            if seen[0].get(serial) != n or seen[1].get(serial) is not \
                    (kids[n - 1] if n else None) or seen[2].get(serial) != g.IsMinimized:
                if CV["built"] == CANVAS["ver"] and CV["ctrl"] is not None:
                    canvas_resync(serial, g)
            return True

        def canvas_rehide():
            """The canvas's Draw: a slot's window the client showed again since the
            pre-draw pass (or with no draw hook at all) is hidden before it draws."""
            gumps = H.gumps
            for slot in CANVAS["order"]:
                info = CANVAS["kinds"].get(slot)
                if info is None or info[0] == "board" or info[0] == "closed":
                    continue
                g = gumps.get(info[2])
                if g is not None and g.IsVisible:
                    g.IsVisible = False

        def restore_all():
            for g in list(H.managed):
                try:
                    release(g)
                except Exception:
                    pass

        def set_minimized_all(minimize):
            serials = set(st.assign.values())

            def run():
                scan_gumps()
                n = 0
                for s in serials:
                    g = H.gumps.get(s)
                    if g is None or g.IsDisposed or g.IsChessboard or g.IsBackgammonBoard:
                        continue
                    if bool(g.IsMinimized) != minimize:
                        g.IsMinimized = minimize
                        n += 1
                return n

            return on_main(run)

        def read_scale():
            def run():
                prof = R.p_profile.GetValue(None)
                return (int(prof.ContainersScale), bool(prof.ScaleItemsInsideContainers))
            return on_main(run)

        def apply_scale(pct, items):
            def run():
                prof = R.p_profile.GetValue(None)
                changed = int(prof.ContainersScale) != pct or bool(prof.ScaleItemsInsideContainers) != items
                prof.ContainersScale = Byte(pct)
                prof.ScaleItemsInsideContainers = items
                R.p_cscale.SetValue(None, Single(pct / 100.0))
                H.scale = pct / 100.0
                if changed:
                    node = R.p_gumps.GetValue(None).First
                    while node is not None:
                        v = node.Value
                        if isinstance(v, R.ContainerGump) and not v.IsDisposed:
                            v.RequestUpdateContents()
                        node = node.Next
                return changed
            return on_main(run)

        def bag_is_open(serial):
            if R.ok and not H.disabled:
                g = H.gumps.get(serial)
                return g is not None and not safe(lambda: g.IsDisposed, True)
            it = get_item(serial)
            return bool(it) and Kit.is_open(safe(lambda: it.GetContainerGump()))

        # ------------------------------- persistence ---------------------------------
        def cfg_file():
            base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
            serial = safe(lambda: int(API.Player.Serial), 0)
            name = "_unified_bag_%d.cfg" % serial
            return (base + "/" + name) if base else name

        def save():
            st.save_in = -1
            # combined: the frame follows Paperdoll; (2.6.78) alone in a zone: the layout's
            # place, not yours (the free window's place is saved from the bar)
            if not attached() and st.canvas != "alone":
                st.saved_fx, st.saved_fy = st.frame_x, st.frame_y
            lines = [
                "slots=%d" % st.slots, "cols=%d" % st.cols, "rows=%d" % st.rows,
                "frame_x=%d" % st.saved_fx, "frame_y=%d" % st.saved_fy,
                "cell_w=%d" % st.cell_w, "cell_h=%d" % st.cell_h,
                "trim=%d" % int(st.trim), "collapsed=%d" % int(st.collapsed), "bare=%d" % int(st.bare),
                "side=%d" % int(st.side_hidden),
                "opacity=%d" % int(round(st.opacity * 100)),
                "mgr_x=%d" % st.mgr_x, "mgr_y=%d" % st.mgr_y,
                "trp_x=%d" % st.trp_x, "trp_y=%d" % st.trp_y,
                "mgr_open=%d" % int(st.open_mgr), "mgr_min=%d" % int(st.mgr_min),
                "trp_open=%d" % int(st.open_trp), "trp_min=%d" % int(st.trp_min),
                "trapsel=" + ",".join(str(s) for s in sorted(st.trap_sel)),
                "trapextra=" + ",".join(str(s) for s in st.trap_extra),
            ]
            for idx in sorted(st.assign):
                lines.append("slot.%d=%d" % (idx, st.assign[idx]))
            # 2.6.05: the Sort rules window and the rules. New keys and a new line
            # type ("sort.<slot>=<kinds>;<graphics>", never a whole number) that the
            # 2.6.04 loader keeps aside unused, so the file still loads there
            lines += ["srt_x=%d" % st.srt_x, "srt_y=%d" % st.srt_y,
                      "srt_open=%d" % int(st.open_srt), "srt_min=%d" % int(st.srt_min),
                      "sort_say=%d" % int(st.sort_say)]
            for idx in sorted(st.rules):
                kinds, graphics = st.rules[idx]
                if kinds or graphics:
                    lines.append("sort.%d=%s;%s" % (idx, ",".join(sorted(kinds)),
                                                    ",".join(str(g) for g in graphics)))
            # the file is written by write_saved() on the script's own thread (the
            # module's thread_tick): a disk write on the client thread is a frame hitch
            st.to_write = (cfg_file(), "\n".join(lines))
            if not safe(lambda: HOST.by_key[KEY].running, False):
                write_saved()        # switched off (settings page): no thread_tick will come

        def others_cursor():
            """Another module's claim or a HOST.pick_target cursor: never ours to aim
            or cancel."""
            return bool(safe(lambda: HOST.cursor_busy(KEY), None))

        def write_saved():
            """Write the settings save() prepared (thread_tick; returns at once when
            there is nothing to write)."""
            job = st.to_write
            if job is None:
                return
            st.to_write = None
            path, text = job
            try:
                f = open(path, "w")
                try:
                    f.write(text)
                finally:
                    f.close()
            except Exception as e:
                API.SysMsg(TITLE + ": couldn't save its settings (%s)." % e, HUE_ERR)

        def parse_serials(text):
            return [int(p) for p in (text or "").split(",") if p.strip().isdigit()]

        def read_cfg():
            """The settings file's text, or None (2.6.81: on the script thread, from
            thread_tick, once start() asks; at load time in place)."""
            try:
                f = open(cfg_file(), "r")
                try:
                    return f.read()
                finally:
                    f.close()
            except Exception:
                return None

        def load():
            parse_cfg(read_cfg())

        def parse_cfg(raw):
            """Apply the settings file's text (None: no file, nothing changes)."""
            if raw is None:
                return
            vals, ints = {}, {}
            for line in raw.splitlines():
                if "=" in line:
                    k, v = [p.strip() for p in line.split("=", 1)]
                    vals[k] = v
                    try:
                        ints[k] = int(v)
                    except ValueError:
                        pass
            st.slots = max(MIN_SLOTS, min(MAX_SLOTS, ints.get("slots", st.slots)))
            st.cols = max(0, min(MAX_SLOTS, ints.get("cols", 0)))
            st.rows = max(0, min(MAX_SLOTS, ints.get("rows", 0)))
            st.frame_x = st.saved_fx = ints.get("frame_x", st.frame_x)
            st.frame_y = st.saved_fy = ints.get("frame_y", st.frame_y)
            # a saved place: on the screen of today (the host keeps the window on it)
            st.frame_x, st.frame_y = Kit.adapt(st.frame_x, st.frame_y)
            st.saved_fx, st.saved_fy = st.frame_x, st.frame_y
            st.cell_w = max(20, min(MAX_CELL, ints.get("cell_w", st.cell_w)))
            st.cell_h = max(20, min(MAX_CELL, ints.get("cell_h", st.cell_h)))
            st.fit_pending = "cell_w" not in ints
            st.trim = ints.get("trim", 1) == 1
            st.collapsed = ints.get("collapsed", 0) == 1
            st.bare = ints.get("bare", 0) == 1
            st.side_hidden = ints.get("side", 0) == 1
            st.opacity = max(10, min(100, ints.get("opacity", ints.get("panel_a", 90)))) / 100.0
            for k in ("mgr_x", "mgr_y", "trp_x", "trp_y"):
                if k in ints:
                    setattr(st, k, ints[k])
            st.mgr_x, st.mgr_y = Kit.adapt(st.mgr_x, st.mgr_y)
            st.trp_x, st.trp_y = Kit.adapt(st.trp_x, st.trp_y)
            st.mgr_min = ints.get("mgr_min", 0) == 1      # the Bag Manager / Traps windows
            st.trp_min = ints.get("trp_min", 0) == 1      # as you left them
            st.want_mgr = ints.get("mgr_open", 0) == 1
            st.want_trp = ints.get("trp_open", 0) == 1
            st.trap_sel = set(parse_serials(vals.get("trapsel")))
            st.trap_extra = parse_serials(vals.get("trapextra"))
            st.assign = {}
            for k, v in ints.items():
                if k.startswith("slot."):
                    try:
                        idx = int(k[5:])
                    except ValueError:
                        continue
                    if 0 <= idx < st.slots and v > 0:
                        st.assign[idx] = v
            # 2.6.05 (a 2.6.04 file has none of these: no rules, the window closed)
            if "srt_x" in ints:
                st.srt_x = ints["srt_x"]
            if "srt_y" in ints:
                st.srt_y = ints["srt_y"]
            st.srt_x, st.srt_y = Kit.adapt(st.srt_x, st.srt_y)
            st.srt_min = ints.get("srt_min", 0) == 1
            st.want_srt = ints.get("srt_open", 0) == 1
            st.sort_say = ints.get("sort_say", 0) == 1
            st.rules = {}
            for k, v in vals.items():
                if k.startswith("sort."):
                    try:
                        idx = int(k[5:])
                    except ValueError:
                        continue
                    if 0 <= idx < st.slots:
                        rule = parse_rule(v)
                        if rule is not None:
                            st.rules[idx] = rule

        def parse_rule(text):
            """'reagents,gems;3962,3963' -> (frozenset kinds, tuple graphics), or None."""
            kpart, _, gpart = (text or "").partition(";")
            kinds = frozenset(k for k in (p.strip() for p in kpart.split(","))
                              if k in SORT_KIND_KEYS)
            graphics = []
            for p in gpart.split(","):
                p = p.strip()
                if p.isdigit() and 0 < int(p) <= 0xFFFF and int(p) not in graphics:
                    graphics.append(int(p))
            graphics = tuple(graphics[:SORT_GRAPHICS_CAP])
            return (kinds, graphics) if (kinds or graphics) else None

        # ------------------------------- geometry ------------------------------------
        fitov = {"told": None,       # (2.6.71) the slot (w, h) the layout last gave, or None
                 "cols": None,       # (2.6.55) columns the zone fit asks for (None: the setting)
                 "cell": None,       # (2.6.56) the slots' size that fills the zone (None: the bags')
                 "area": None}       # (2.6.57) combined with a fitted Paperdoll: the hole (w, h)

        def layout_dims(slots=None, cols=None, rows=None):
            slots = st.slots if slots is None else slots
            if cols is None and rows is None and fitov["cols"]:
                c = max(1, min(slots, fitov["cols"]))     # the zone's width decides the columns
                return c, int(math.ceil(slots / float(c)))
            cols = st.cols if cols is None else cols
            rows = st.rows if rows is None else rows
            if cols > 0 and rows > 0:
                return cols, rows
            if cols > 0:
                return cols, int(math.ceil(slots / float(cols)))
            if rows > 0:
                c = int(math.ceil(slots / float(rows)))
                return c, int(math.ceil(slots / float(c)))
            c = max(1, int(math.ceil(math.sqrt(slots))))
            return c, int(math.ceil(slots / float(c)))

        def trimming():
            return st.trim and R.ok and not H.disabled

        LAYOUT_SEEN = [None, None]      # (2.6.82) the assignment and slot count it was made from

        def publish_layout():
            a = st.assign
            if a == LAYOUT_SEEN[0] and st.slots == LAYOUT_SEEN[1]:
                return                        # (every tick: nothing changed, nothing built)
            lay = tuple(sorted((i, s) for i, s in a.items() if i < st.slots))
            if lay != st.layout:              # replaced only on a change (the draw hook keys on it)
                st.layout = lay
            LAYOUT_SEEN[0], LAYOUT_SEEN[1] = dict(a), st.slots

        def default_cell():
            s = H.scale if R.ok else 1.0
            if trimming():
                return int(BACKPACK_INTERIOR[0] * s), int(BACKPACK_INTERIOR[1] * s)
            return int(LOOSE_CELL[0] * s), int(LOOSE_CELL[1] * s)

        def refit_cells():
            st.cell_w, st.cell_h = default_cell()
            st.fit_pending = True
            st.dirty_frame = True
            schedule_save()

        # --------------------------------- frame -------------------------------------
        def side_items():
            """Side panel contents in order; 'break' becomes a divider (dropped at column edges)."""
            return [("bagicons", ICON_BOX[1] + 22), ("break", SIDE_SEP_H),
                    ("spellicons", ICON_BOX[1] + 22),
                    ("stop", 22 + 4 + 18),       # Stop button with the progress line under it
                    ("quick", 4 * 24),           # (2.6.85) Restock, Sort, Storage, Supplies
                    ("tools", 24 + 26 + 24)]     # the filter box, Rules, Filters (2.6.05; 2.6.72; 2.6.85)

        def side_columns(avail_h):
            """Pack the panel items into as few columns as fit the grid's height."""
            inner = max(avail_h - 2 * (SIDE_PAD + SIDE_RIM), 0)
            cols, used = [[]], 0
            for item in side_items():
                kind, h = item
                need = h + (SIDE_GAP if cols[-1] else 0)
                if cols[-1] and used + need > inner and kind != "break":
                    cols.append([])
                    used, need = 0, h
                if kind == "break" and not cols[-1]:
                    continue
                cols[-1].append(item)
                used += need
            for col in cols:
                while col and col[0][0] == "break":
                    col.pop(0)
                while col and col[-1][0] == "break":
                    col.pop()
            cols = [c for c in cols if c]
            heights = [sum(i[1] for i in c) + SIDE_GAP * (len(c) - 1) for c in cols]
            return cols, heights

        def icon_pic(graphic, x, y, box_w, box_h, tip, handler):
            pic = G.CreateGumpPic(graphic)
            nw = safe(lambda: pic.GetWidth(), 0) or box_w
            nh = safe(lambda: pic.GetHeight(), 0) or box_h
            k = min(box_w / float(nw), box_h / float(nh), 1.0)
            w, h = max(1, int(nw * k)), max(1, int(nh * k))
            pic.SetRect(x + (box_w - w) // 2, y + (box_h - h) // 2, w, h)
            safe(lambda: setattr(pic, "ContainsByBounds", True))   # click anywhere on the shrunken art
            safe(lambda: pic.SetTooltip(tip))
            G.AddControlOnClick(pic, handler)
            return pic

        def build_side_panel(grid, x0, gh, y0=0):
            """Draw the stone side panel at (x0, y0) inside the overlay; returns (width, height)."""
            tw, th = bare_btn_size()
            reserve = th + BARE_PAD                     # strip along the bottom for the bags-only button
            cols, heights = side_columns(gh - reserve)
            pw = len(cols) * SIDE_COL_W + 2 * SIDE_RIM
            ph = max(gh, max(heights) + 2 * (SIDE_PAD + SIDE_RIM) + reserve)
            # (2.6.72) riding in the Paperdoll with one frame on: panels only, no stone
            # (2.6.78: Bags alone in a zone with one frame on too)
            if not canvas_unified():
                Kit.add_resizepic(grid, Kit.WINDOW_BG, x0, y0, pw, ph)
            Kit.add_section(grid, x0 + SIDE_RIM, y0 + SIDE_RIM, pw - 2 * SIDE_RIM, ph - 2 * SIDE_RIM)
            art, iconized = st.icons_used
            for ci, col in enumerate(cols):
                cx = x0 + SIDE_RIM + ci * SIDE_COL_W
                if ci:
                    grid.Add(no_mouse(box(cx, y0 + SIDE_RIM + SIDE_PAD, 1,
                                          ph - 2 * (SIDE_RIM + SIDE_PAD), C_SEAM, 0.8)))
                bx = cx + (SIDE_COL_W - SIDE_BTN_W) // 2
                y = y0 + (ph - reserve - heights[ci]) // 2
                for kind, h in col:
                    if kind in ("bagicons", "spellicons"):
                        if kind == "bagicons":
                            pair = ((iconized, "Minimize every open bag in the slots",
                                     act(set_min, True), "Minimize"),
                                    (art, "Restore every minimized bag in the slots",
                                     act(set_min, False), "Restore"))
                        else:
                            pair = ((ICON_MAGIC_TRAP,
                                     "Cast Magic Trap on every bag ticked in the trap bags window",
                                     act(start_job, "Magic Trap"), "Trap"),
                                    (ICON_MAGIC_UNTRAP,
                                     "Cast Magic Untrap on every bag ticked in the trap bags window",
                                     act(start_job, "Magic Untrap"), "Untrap"))
                        half = SIDE_BTN_W // 2
                        for j, (graphic, tip, handler, cap) in enumerate(pair):
                            grid.Add(icon_pic(graphic, bx + j * half, y, half, ICON_BOX[1], tip, handler))
                            label(grid, cap, bx + j * half + max(0, (half - Kit.text_w(cap)) // 2),
                                  y + ICON_BOX[1] + 3, Kit.HUE_INFO)
                    elif kind == "stop":
                        # (2.6.72) Stop shows only while a run is going (next to Minimize
                        # and Restore its X read as Close); the line under it is empty
                        # when idle, or says the scale the bags are shown at to fit
                        cap = Kit.art_button(grid, ui["store"], "stop", Kit.ART_CLOSE, bx, y, "Stop",
                                             "Stop the trap, untrap or sort run that is going",
                                             on_click=act(stop_all))
                        ui["stop_ctrls"] = [ui["store"][0].get("stop"), cap]
                        ui["side_status"] = label(grid, st.status_text, bx, y + 26, Kit.HUE_INFO)
                        show_stop()
                    elif kind == "quick":
                        build_quick(grid, bx, y)
                    elif kind == "tools":
                        build_tools(grid, bx, y)
                    elif kind == "break":
                        grid.Add(no_mouse(box(bx, y + h // 2, SIDE_BTN_W, 1, C_SEAM, 0.8)))
                    y += h + SIDE_GAP
            # the gem: bags only (combined with Paperdoll it hides this side panel)
            add_bare_button(grid, x0 + pw - SIDE_RIM - BARE_PAD - tw, y0 + ph - SIDE_RIM - BARE_PAD - th,
                            False)
            return pw, ph

        def attached():
            """Combined into the Paperdoll window (its title bar, our slots)."""
            return st.attach is not None

        def bare_on():
            """Bags only and not folded: no title bar, slots start at its top."""
            return st.bare and not st.collapsed and not attached()

        def layout_gump():
            """The window that leads (the title bar, or the slots when bags only),
            for the layout's registry. (2.6.66) Combined with Paperdoll it is the
            grid: it rides in Paperdoll's window (attached, so the layout never
            places it itself), but it is what sits in the bags' zone, the one
            under Paperdoll's, so that zone counts as taken and keeps its room."""
            if attached():
                return ui.get("grid")
            if st.canvas == "alone":                 # (2.6.78) the zone's one window
                return ui.get("grid")
            return ui.get("grid") if bare_on() else ui.get("bar")

        def layout_state():
            """(2.6.78) The layout's "state" hook (Bags alone with the canvas): None
            (off), "open", "minimized" (folded to its title bar) or "docked"."""
            if st.stopping or st.wait_player or not Kit.is_open(ui.get("grid")):
                return None
            return "docked" if st.docked else ("minimized" if st.collapsed else "open")

        def layout_fit(w, h, mode):
            """The layout: the window's slot in a zone is w x h px (None: freed).
            (2.6.56) The window fills it exactly: the columns that make the
            slots biggest in it, then each slot grown to share out the room left
            (a slot is never drawn smaller than the bag it shows; the side panel
            keeps its size). Your Columns and Rows are untouched. Runs on the
            client thread in the keeper's pass: only records and asks for a
            rebuild."""
            new = (None, None)
            geom = st.geom
            if not attached():                    # (2.6.71) kept: shared out again at each build
                told = (int(w), int(h)) if (w is not None and h is not None) else None
                if canvas_ok() and (told != fitov["told"] or (mode == "again" and told is not None)):
                    st.dirty_frame = True         # (2.6.78) the canvas window: drawn at that size
                fitov["told"] = told
                if canvas_ok() and told is not None:
                    return                        # (its slot is its size: no cells to share out)
            if w is not None and h is not None and geom is not None:
                cols_now, cw_now, ch_now, gap = geom
                gw_now = cols_now * cw_now + (cols_now - 1) * gap
                gap = 0 if trimming() else LOOSE_GAP   # (2.6.71) the gap of now (Trim may have changed)
                extra = max(0, (st.grid_wh[0] if st.grid_wh else gw_now) - gw_now)   # the side panel
                if attached():                    # (2.6.57) grid_wh may be the hole: the panel's own
                    extra = 0 if side_off() else int(getattr(st, "side_pw", 0) or 0)
                aw = int(w) - extra
                ah = int(h) - top_off()
                cw, ch = st.cell_w, st.cell_h
                n = max(1, st.slots)
                best = None
                for c in range(1, n + 1):
                    r = int(math.ceil(n / float(c)))
                    fw = (aw - (c - 1) * gap) // c
                    fh = (ah - (r - 1) * gap) // r
                    if fw < cw or fh < ch:
                        continue
                    k = min(fw / float(cw), fh / float(ch))   # how big the slots come out
                    if best is None or k > best[0]:
                        best = (k, c, fw, fh)
                if best is None:                  # no layout fits: as many columns as its width holds
                    c = max(1, min(n, (aw + gap) // max(1, cw + gap)))
                    r = int(math.ceil(n / float(c)))
                    best = (0, c, max(cw, (aw - (c - 1) * gap) // c),
                            max(ch, (ah - (r - 1) * gap) // r))
                new = (best[1], (best[2], best[3]))
            if new != (fitov["cols"], fitov["cell"]):
                fitov["cols"], fitov["cell"] = new
                st.dirty_frame = True

        def bag_cell():
            """(2.6.58) bag.cell: (cell w, cell h, gap, slots, side panel width) of
            the grid at the bags' own cell size, for the fitted Paperdoll's sums.
            (2.6.67) Then (scale now, your scale, the least it may be shrunk to),
            in percent: the cells are measured at the scale of now."""
            gap = 0 if trimming() else LOOSE_GAP
            side = 0 if side_off() else int(getattr(st, "side_pw", 0) or 0)
            area = fitov.get("area")
            if side and area is not None:
                # (2.6.72) the side panel's width at the area's height, not at the height
                # the grid happens to have now (it went from 1 column to 2 and back as
                # the grid shrank, so the scale worked out from it flipped: 105%, 110%)
                tw, th = bare_btn_size()
                cols, _h = side_columns(area[1] - th - BARE_PAD)
                side = len(cols) * SIDE_COL_W + 2 * SIDE_RIM
            cur = int(round(H.scale * 100)) if R.ok else st.scale_pct
            own = st.scale_pct if shrink["pct"] is not None else cur
            floor = SHRINK_MIN if (R.ok and not H.disabled) else own
            # (2.6.72) the cells at your own scale, from fixed data: measured while not
            # shrunk and kept; while shrunk, converted once as floats (int truncation of
            # cells measured shrunk made the next pass ask for another scale)
            if shrink["pct"] is None or cur == own:
                st.own_cell = (st.cell_w, st.cell_h, st.slots)
                cw, ch = float(st.cell_w), float(st.cell_h)
            else:
                oc = getattr(st, "own_cell", None)
                if oc is not None and oc[2] == st.slots:
                    cw, ch = float(oc[0]), float(oc[1])
                else:
                    f = own / float(max(1, cur))
                    cw, ch = st.cell_w * f, st.cell_h * f
            return cw, ch, gap, st.slots, side, own, own, min(floor, own)

        # ---------- (2.6.78) the bag canvas ----------
        #  In a zone (combined with the Paperdoll, or Bags alone in one), the bags
        #  fill the zone completely. Bags no longer shows the client's bag windows
        #  there: they stay open (so the client keeps their contents current) but
        #  hidden, and every item is drawn on one canvas that fills the zone. Each
        #  slot's bag gets a region in proportion to its real item area, laid out
        #  in rows (or columns) with no gap, each as close as it can be to its
        #  bag's own shape (canvas_split). An item let go at any pixel of the
        #  canvas goes into the bag there, at the one bag position the canvas
        #  draws back centred on that pixel (the map: item_spot / canvas_drop), and
        #  a pin keeps it on that pixel exactly for the session. A picture may hang
        #  over a neighbour's region; at the zone's own edges it is kept inside.
        ROOM_MEMO = {}                  # (2.6.82) side_width / title_fits answers (pure functions)

        def side_width(h):
            """Width of the side panel at a grid h px high (a pure function of h:
            kept per h, 2.6.82)."""
            k = ("sw", h)
            v = ROOM_MEMO.get(k)
            if v is None:
                tw, th = bare_btn_size()
                cols, _h = side_columns(h - th - BARE_PAD)
                v = len(cols) * SIDE_COL_W + 2 * SIDE_RIM
                if len(ROOM_MEMO) >= 200:
                    ROOM_MEMO.clear()
                ROOM_MEMO[k] = v
            return v

        def own_pct():
            """Your Bag scale (%): what the bags are drawn at when nothing shrinks them."""
            return st.scale_pct if shrink["pct"] is not None else (
                int(round(H.scale * 100)) if R.ok else st.scale_pct)

        def canvas_ok():
            """The canvas can be used: client access and its classes built."""
            return R.ok and R.can_ok and not H.disabled

        def holds():
            try:                                      # (2.6.82: every tick, no lambda)
                return bool(HOST.layout_holds(KEY))
            except Exception:
                return False

        def canvas_mode():
            """None, "combined" (in the Paperdoll's hole in a zone) or "alone" (Bags
            alone in a zone), from what the module knows now."""
            if not canvas_ok() or st.collapsed or st.docked or st.stopping:
                return None
            if attached():
                if fitov["area"] is None or not st.attach.get("shown", True):
                    return None
                return "combined"
            if fitov["told"] is not None and holds():
                return "alone"
            return None

        CANVAS_MIN_W = 120              # px of bags the side panel always leaves beside it

        def title_buttons():
            return [("Settings",), ("Trap bags",), ("Slots",)]

        def title_fits(w):
            """Bags alone's title row fits w px: its buttons (captions dropped if
            need be) leave room for at least a cut title. (2.6.82: kept per w and
            slot count, the only things it depends on.)"""
            k = ("tf", w, st.slots)
            v = ROOM_MEMO.get(k)
            if v is None:
                plan = Kit.title_plan(w, TITLE, title_buttons(), str(st.slots))
                v = len(plan[3]) == len(title_buttons()) and \
                    plan[4] >= Kit.MARGIN + 30 + Kit.text_w("..") + Kit.TITLE_GAP
                if len(ROOM_MEMO) >= 200:
                    ROOM_MEMO.clear()
                ROOM_MEMO[k] = v
            return v

        def canvas_room(mode):
            """(x, y, w, h, side): the canvas in the grid gump's pixels, and the side
            panel's width beside it (0: none). Bags alone: no title row when bags
            only, or when the zone is too narrow for the row's buttons (the canvas
            fills it then); no side panel when it would leave the bags under
            CANVAS_MIN_W px."""
            if mode == "combined":
                a = fitov["area"]
                side = 0 if side_off() else side_width(a[1])
                return 0, 0, max(1, a[0] - side), max(1, a[1]), side
            w, h = fitov["told"]
            M = Kit.MARGIN
            if st.bare or not title_fits(w):             # bags only / too narrow: no title row
                return M, M, max(1, w - 2 * M), max(1, h - 2 * M), 0
            top = M + 30 + Kit.GAP
            ch = max(1, h - top - M)
            side = side_width(ch)
            if w - 2 * M - side < CANVAS_MIN_W:
                side = 0
            return M, top, max(1, w - 2 * M - side), ch, side

        def bounds_of(g, graphic=None):
            """The bag's item area at 100% (left, top, right, bottom), kept per graphic."""
            if graphic is None:
                graphic = int(g.Graphic)
            b = H.bounds.get(graphic)
            if b is None:
                r = R.f_data.GetValue(g).Bounds
                b = (int(r.X), int(r.Y), int(r.Width), int(r.Height))  # Width/Height: right/bottom
                H.bounds[graphic] = b
            return b

        def is_board(g, graphic):
            try:
                return gump_info(g)[1] or graphic in BOARDS
            except Exception:
                return graphic in BOARDS

        def split_input():
            """((slot, graphic, kind, bag), ...) in slot order: kind "open", "mini",
            "closed" (no window, or a TazUO grid container) or "board". A bag in
            two slots (a hand-edited save) keeps the first."""
            out = []
            seen = set()
            for idx, serial in st.layout:
                if serial in seen:
                    continue
                seen.add(serial)
                g = H.gumps.get(serial)
                kind, graphic = "closed", 0
                try:
                    if g is not None and not g.IsDisposed:
                        gi = H.ginfo.get(g)           # (2.6.82) read once per window
                        graphic = gi[0] if gi is not None else int(g.Graphic)
                        if is_board(g, graphic):
                            kind = "board"
                        elif g.IsMinimized:
                            kind = "mini"
                        else:
                            bounds_of(g, graphic)
                            kind = "open"
                except Exception:
                    kind, graphic = "closed", 0
                out.append((idx, graphic, kind, serial))
            return tuple(out)

        def split_weights(items):
            """[(slot, area, shape)]: an open bag its item area at 100%, any other its
            closed tile."""
            out = []
            for slot, graphic, kind, _bag in items:
                b = H.bounds.get(graphic) if kind == "open" else None
                if b is not None:
                    w, h = max(1, b[2] - b[0]), max(1, b[3] - b[1])
                else:
                    w, h = CLOSED_W, CLOSED_H
                out.append((slot, float(w * h), w / float(h)))
            return out

        def split_dp(ws, W, H_):
            """The best break points of ws laid out in rows across W x H_ (a row's
            regions share its height; each region's cost is how far its shape is
            from its bag's, weighted by its area). O(n^2): with L_i = ln(A_i / r_i)
            a row costs sum a (L - 2 ln h)^2, three prefix sums."""
            n = len(ws)
            S = 0.0
            for x in ws:
                S += x[1]
            pa, pal, pall, pA = [0.0], [0.0], [0.0], [0.0]
            for slot, a, r in ws:
                A = W * H_ * a / S
                L = math.log(A / r)
                pa.append(pa[-1] + a)
                pal.append(pal[-1] + a * L)
                pall.append(pall[-1] + a * L * L)
                pA.append(pA[-1] + A)
            inf = float("inf")
            best = [0.0] + [inf] * n
            back = [0] * (n + 1)
            for k in range(1, n + 1):
                bk, jk = inf, 0
                for j in range(k):
                    h = (pA[k] - pA[j]) / W
                    if h <= 0:
                        continue
                    lh = 2.0 * math.log(h)
                    c = best[j] + (pall[k] - pall[j]) - 2.0 * lh * (pal[k] - pal[j]) \
                        + lh * lh * (pa[k] - pa[j])
                    if c < bk:
                        bk, jk = c, j
                best[k], back[k] = bk, jk
            breaks = []
            k = n
            while k > 0:
                breaks.append(k)
                k = back[k]
            breaks.reverse()
            return best[n], breaks

        def split_cost(ws, W, H_, breaks):
            """The cost of given break points (rows across W x H_)."""
            S = 0.0
            for x in ws:
                S += x[1]
            c, j = 0.0, 0
            for k in breaks:
                area = 0.0
                for i in range(j, k):
                    area += W * H_ * ws[i][1] / S
                h = area / W
                if h <= 0:
                    return float("inf")
                for i in range(j, k):
                    w = (W * H_ * ws[i][1] / S) / h
                    c += ws[i][1] * math.log((w / h) / ws[i][2]) ** 2
                j = k
            return c

        def split_plan(ws, W, H_, keep=None):
            """(orient, breaks, cost): rows, or columns when they cost under
            COLUMNS_BEAT of the rows. keep: the (orient, breaks) of now, kept unless
            the best costs under (1 - SPLIT_KEEP) of it (a resize never flips back
            and forth)."""
            if not ws:
                return "rows", [], 0.0
            cr, br = split_dp(ws, W, H_)
            # 2.6.81 (IN1-1): columns are rows on the canvas turned 90 degrees, so
            # each bag's shape turns with it (w/h becomes h/w); before, the columns
            # were scored against the bags' shapes untransposed and won wrongly
            wsT = [(s, a, 1.0 / r) for s, a, r in ws]
            cc, bc = split_dp(wsT, H_, W)
            best = ("columns", bc, cc) if cc < COLUMNS_BEAT * cr else ("rows", br, cr)
            if keep is not None and keep[1] and keep[1][-1] == len(ws):
                o, b = keep
                kc = split_cost(ws, W, H_, b) if o == "rows" else split_cost(wsT, H_, W, b)
                if not best[2] < (1.0 - SPLIT_KEEP) * kc:
                    return o, list(b), kc
            return best

        def split_pixels(ws, W, H_, orient, breaks):
            """{slot: (x, y, w, h)} covering W x H_ exactly once: row edges at the
            rows' running area / W, each region's edges at the row's running share
            (neighbours share their edges: no gap, no overlap)."""
            if not ws:
                return {}
            if orient == "columns":
                sw = split_pixels(ws, H_, W, "rows", breaks)
                out = {}
                for s, (x, y, w, h) in sw.items():
                    out[s] = (y, x, h, w)
                return out
            S = 0.0
            for x in ws:
                S += x[1]
            out = {}
            j, cum_rows, y0 = 0, 0.0, 0
            n = len(ws)
            for k in breaks:
                row = 0.0
                for i in range(j, k):
                    row += W * H_ * ws[i][1] / S
                cum_rows += row
                y1 = int(round(cum_rows / W)) if k < n else H_
                cum, x0 = 0.0, 0
                for i in range(j, k):
                    cum += W * H_ * ws[i][1] / S
                    x1 = int(round(W * cum / row)) if i < k - 1 else W
                    out[ws[i][0]] = (x0, y0, x1 - x0, y1 - y0)
                    x0 = x1
                y0 = y1
                j = k
            return out

        # ---- the map: a bag position <-> a canvas pixel (an item's picture centre) ----
        def client_clamp(b, aw, ah, cs, x, y):
            """Where the client stores (x, y) for that art (CheckItemControlPosition,
            ported: with art bigger than the area its clamp turns lo into hi)."""
            bw = b[2] - int(aw / cs)
            bh = b[3] - int(ah / cs)
            if x < b[0]:
                x = b[0]
            elif x > bw:
                x = bw
            if y < b[1]:
                y = b[1]
            elif y > bh:
                y = bh
            return x, y

        # (2.6.80) The map keeps a bag's own picture: each item's CENTRE in the bag
        # (its stored top-left plus half its art, in the bag's own units, as the
        # client draws it) is placed at the same fraction of its region's item box
        # (the region less its label line), the same affine map for every item of
        # the bag, so the items keep their places relative to one another whatever
        # shape and size the region takes. A picture is then kept wholly inside its
        # region: no item hangs over another bag's region any more. 2.6.78 mapped
        # each item's own legal range, which differs with the art's size, so items
        # of different sizes drifted apart and big ones hung over the neighbours.
        def has_line(reg):
            """2.6.81 (IN1-2): True when an open bag's region has a label line
            (region_labels draws it, items stay below it, a click on it minimizes):
            the one test all of them share."""
            return reg[2] >= LABEL_MIN_W and reg[3] >= LABEL_MIN_H + LABEL_LINE_H

        def item_box(reg):
            """The part of a region items are drawn in: below its label line when
            the region shows labels (region_labels), else the whole region."""
            if has_line(reg):
                rx, ry, rw, rh = reg
                return rx, ry + LABEL_LINE_H, rw, rh - LABEL_LINE_H
            return reg

        def art_units(aw, ah, cs):
            """An item's art size in its bag's own units, as the client draws it
            (Scale items inside containers: the art scales with the bag)."""
            if CANVAS.get("si"):
                return float(aw), float(ah)
            return aw / cs, ah / cs

        def centre_range(box, pw, ph):
            """(cx_lo, cx_hi, cy_lo, cy_hi): where a picture's centre may go so that
            the whole picture is inside box; a picture bigger than the box on an
            axis is centred on it."""
            bx_, by_, bw, bh = box
            xl, xh = bx_ + pw // 2, bx_ + bw - 1 - (pw - pw // 2)
            yl, yh = by_ + ph // 2, by_ + bh - 1 - (ph - ph // 2)
            if xh < xl:
                xl = xh = bx_ + bw // 2
            if yh < yl:
                yl = yh = by_ + bh // 2
            return xl, xh, yl, yh

        def bag_to_canvas(b, box, aw, ah, cs, bx, by):
            """The canvas point an item's centre maps to (before the keep-inside)."""
            uw, uh = art_units(aw, ah, cs)
            sw, sh = float(max(1, b[2] - b[0])), float(max(1, b[3] - b[1]))
            u = 0.5 if uw >= sw else (bx + uw / 2.0 - b[0]) / sw
            v = 0.5 if uh >= sh else (by + uh / 2.0 - b[1]) / sh
            u = 0.0 if u < 0 else (1.0 if u > 1 else u)
            v = 0.0 if v < 0 else (1.0 if v > 1 else v)
            return box[0] + u * box[2], box[1] + v * box[3]

        def canvas_to_bag(b, box, aw, ah, cs, px, py):
            """The bag position (top-left, bag units) whose centre maps to canvas
            point (px, py): bag_to_canvas the other way (the client clamps it)."""
            uw, uh = art_units(aw, ah, cs)
            u = (px - box[0]) / float(max(1, box[2]))
            v = (py - box[1]) / float(max(1, box[3]))
            u = 0.0 if u < 0 else (1.0 if u > 1 else u)
            v = 0.0 if v < 0 else (1.0 if v > 1 else v)
            bx = int(round(b[0] + u * (b[2] - b[0]) - uw / 2.0))
            by = int(round(b[1] + v * (b[3] - b[1]) - uh / 2.0))
            return bx, by

        def pic_size(aw, ah):
            """An item's drawn size: 100%, or at Container Scale with "Scale items"."""
            if CANVAS.get("si"):
                cs = H.scale or 1.0
                return max(1, int(aw * cs)), max(1, int(ah * cs))
            return aw, ah

        def spot_ctx(slot):
            """(2.6.82) What item_spot needs of slot's region, looked up once per
            bag sync: (bag, item box, the bag's item area or None, scale), or
            None when the slot has no region."""
            reg = CANVAS["regions"].get(slot)
            info = CANVAS["kinds"].get(slot)
            if reg is None or info is None:
                return None
            return info[2], item_box(reg), H.bounds.get(info[1]), H.scale or 1.0

        def item_spot(ctx, serial, aw, ah, pw, ph, bx, by):
            """(left, top) on the canvas of an item at bag position (bx, by) in the
            region of ctx (spot_ctx), drawn pw x ph (pic_size): its pin while it is
            still where it was let go, else the map, the picture kept wholly
            inside its region."""
            if ctx is None:
                return 0, 0
            bag, box, b, cs = ctx
            pin = PIN.get(serial)
            if pin is not None and pin[0] == bag and pin[1] == bx and pin[2] == by:
                return int(pin[3]) - pw // 2, int(pin[4]) - ph // 2
            cl_x, ch_x, cl_y, ch_y = centre_range(box, pw, ph)
            if b is None:
                cx, cy = (cl_x + ch_x) // 2, (cl_y + ch_y) // 2
            else:
                cx, cy = bag_to_canvas(b, box, aw, ah, cs, bx, by)
                cx = max(cl_x, min(ch_x, cx))
                cy = max(cl_y, min(ch_y, cy))
            return int(round(cx)) - pw // 2, int(round(cy)) - ph // 2

        def pin_set(serial, bag, bx, by, cx, cy):
            if serial not in PIN:
                if len(PIN_ORDER) >= PIN_CAP:
                    for s in PIN_ORDER[:PIN_CAP // 2]:
                        PIN.pop(s, None)
                    del PIN_ORDER[:PIN_CAP // 2]
                PIN_ORDER.append(serial)
            PIN[serial] = (bag, bx, by, cx, cy)

        def pins_drop():
            PIN.clear()
            del PIN_ORDER[:]

        # ---- the split: on the module tick, when its signature changes ----
        def scale_items_now():
            """The client's "Scale items inside containers", read once a second."""
            now = time.time()
            if now >= CV["prof_at"]:
                CV["prof_at"] = now + 1.0
                try:
                    st.scale_items = bool(R.p_profile.GetValue(None).ScaleItemsInsideContainers)
                except Exception:
                    pass
            return st.scale_items

        def canvas_publish(sig, items, ws, W, H_, plan):
            orient, breaks, _cost = plan
            new = split_pixels(ws, W, H_, orient, breaks)
            kinds, slot_of = {}, {}
            for slot, graphic, kind, bag in items:
                kinds[slot] = (kind, graphic, bag)
                slot_of[bag] = slot
            CANVAS.update({"ver": CANVAS["ver"] + 1, "regions": new, "slot_of": slot_of,
                           "order": [i[0] for i in items], "orient": orient,
                           "breaks": list(breaks), "sig": sig, "items": items, "kinds": kinds,
                           "size": (W, H_), "si": sig[4]})
            pins_drop()                               # (the pins were for the old map)

        def dragging():
            """(2.6.85) An item is on the cursor: the bags on screen stay as they are,
            and whatever would rebuild them waits for the drop (the mouse's press
            and the item's control are in those windows)."""
            try:
                return item_hold() is not None
            except Exception:
                return False

        def canvas_tick():
            """Module tick (client thread): canvas mode on or off, and the split
            worked out again when its signature (the canvas's size, the slots'
            bags and their states, Container Scale, Scale items) changed.
            (2.6.85) Neither while an item is being dragged."""
            mode = canvas_mode()
            if mode != st.canvas:
                if dragging():
                    return
                if st.canvas is not None:
                    canvas_leave()
                st.canvas = mode
                H.placed.clear()                      # every bag placed afresh, either way
                st.dirty_frame = True
            if mode is None:
                return
            done = CANVAS["done"]
            if done is not None and dragging():
                return
            if done is not None:                      # a split from thread_tick
                CANVAS["done"] = None
                if done[0] == CANVAS["job"]:
                    canvas_publish(*done)
                CANVAS["job"] = None
            room = canvas_room(mode)
            items = split_input()
            sig = (room[2], room[3], items, round(H.scale or 1.0, 4), scale_items_now())
            if sig == CANVAS["sig"] or sig == CANVAS["job"] or dragging():
                return
            W, H_ = room[2], room[3]
            ws = split_weights(items)
            keep = None
            if CANVAS["items"] == items and CANVAS["breaks"] is not None:
                keep = (CANVAS["orient"], CANVAS["breaks"])   # only the size changed
            if CANVAS["slow"]:                        # (2.6.78) too slow here: thread_tick
                CANVAS["job"] = sig
                CANVAS["pending"] = (sig, items, ws, W, H_, keep)
                return
            t0 = time.time()
            plan = split_plan(ws, W, H_, keep)
            if time.time() - t0 > SPLIT_SLOW and len(ws) > 8:
                CANVAS["slow"] = True
            canvas_publish(sig, items, ws, W, H_, plan)

        def canvas_thread():
            """thread_tick: a split too slow for the client tick."""
            job = CANVAS.get("pending")
            if job is None:
                return
            CANVAS["pending"] = None
            sig, items, ws, W, H_, keep = job
            plan = split_plan(ws, W, H_, keep)
            CANVAS["done"] = (sig, items, ws, W, H_, plan)

        # ---- the canvas control: placed in the grid, kept across its rebuilds ----
        def canvas_detach():
            """Before the grid gump goes: the canvas out of it, so it lives on."""
            c = CV["ctrl"]
            if c is None:
                return
            try:
                p = c.Parent
                if p is not None:
                    kids = p.Children
                    while kids.Contains(c):
                        kids.Remove(c)
            except Exception:
                pass

        def canvas_place(raw, index, x, y, w, h):
            """The canvas into the grid gump (raw) at child index, at (x, y), w x h."""
            c = CV["ctrl"]
            if c is None or c.IsDisposed:
                canvas_clear()
                try:
                    c = R.Canvas()
                except Exception:
                    c = R.Canvas(None)
                c.AcceptMouseInput = True
                c.Priority = R.LowPriority            # the items always win the press
                CV["ctrl"] = c
            c.va_wh = (int(w), int(h))
            c.Parent = raw                            # (appends) then put back once at index
            kids = raw.Children
            while kids.Contains(c):
                kids.Remove(c)
            kids.Insert(min(index, kids.Count), c)
            R.f_bounds.SetValue(c, R.Rect(int(x), int(y), int(w), int(h)))
            CV["rect"] = (int(x), int(y), int(w), int(h))
            for lay in CV["layers"].values():
                R.f_bounds.SetValue(lay, R.Rect(0, 0, int(w), int(h)))

        def canvas_clear():
            """Forget the canvas's contents (the control is gone or going)."""
            CV.update({"built": -1, "bsize": None, "parts": [], "icons": [], "bg": None,
                       "layers": {}, "pool": {}, "owner": {}, "items": {}, "seen_n": {},
                       "seen_last": {}, "seen_min": {}, "spot": {}, "label": {}, "count": {},
                       "tip": None, "sums": {}, "say_lbl": None, "under": set(),
                       "sum_part": None, "alpha_set": None, "say_shown": False})

        def canvas_leave():
            """Canvas mode ends (zone left, folded, Paperdoll hiding the bags, Bags
            stopping): the canvas and every pin go; the bags go back to 2.6.77's
            forms on the next frames (H.placed cleared by the caller)."""
            canvas_detach()
            c = CV["ctrl"]
            CV["ctrl"] = None
            if c is not None:
                try:
                    c.Dispose()
                except Exception:
                    pass
            canvas_clear()
            CV["rect"] = None
            pins_drop()
            CANVAS.update({"sig": None, "items": None, "breaks": None, "regions": {},
                           "kinds": {}, "slot_of": {}, "order": [], "job": None, "done": None,
                           "pending": None, "size": None})
            CANVAS["ver"] += 1
            ui["counts"] = []
            ui["count_state"] = {}

        def canvas_alpha():
            """Bag opacity on the canvas, in place: its background and the minimized
            bags' icons (items always draw solid). One frame on: SECTION_ALPHA."""
            a = Kit.SECTION_ALPHA if canvas_unified() else st.opacity
            bg = CV["bg"]
            # (2.6.82) the canvas is the only writer of these: what it set last is
            # what they hold, so nothing is read back while it is the same
            # (CV["alpha_set"] goes back to None when canvas_parts makes them again)
            want = (a, st.opacity, bg)
            if CV["alpha_set"] == want:
                return
            try:
                if bg is not None and abs(float(bg.Alpha) - a) > 0.001:
                    bg.Alpha = a
            except Exception:
                pass
            for ic in CV["icons"]:
                try:
                    if abs(float(ic.Alpha) - st.opacity) > 0.001:
                        ic.Alpha = st.opacity
                except Exception:
                    pass
            CV["alpha_set"] = want

        def canvas_unified():
            try:                                      # (2.6.82: every tick, no lambdas)
                if attached() and HOST.layout_unified():
                    return True
            except Exception:
                pass
            try:
                return bool(HOST.layout_unified(KEY))
            except Exception:
                return False

        def into_canvas(w):
            """A Kit-made control (flushed) moved on to the end of the canvas,
            taking no mouse; returns its client control."""
            raw = raw_of(w) if w is not None else None
            if raw is None:
                return None
            raw.Parent = CV["ctrl"]
            raw.AcceptMouseInput = False
            return raw

        def canvas_parts():
            """The canvas's background, seams, minimized bags' icons, the bag labels
            and Find's count labels, for the split of now; the layers kept (made
            for new regions, gone with old ones); every item drawn again."""
            c = CV["ctrl"]
            grid = ui.get("grid")
            if c is None or grid is None:
                return
            for p in CV["parts"]:
                try:
                    kids = c.Children
                    while kids.Contains(p):
                        kids.Remove(p)
                    p.Dispose()
                except Exception:
                    pass
            CV["parts"], CV["icons"], CV["label"], CV["count"] = [], [], {}, {}
            CV["tip"] = None
            CV["alpha_set"] = None                    # (2.6.82) made again below: set afresh
            say = CV["say_lbl"]                       # (the journal fallback's label: made again)
            CV["say_lbl"] = None
            if say is not None:
                safe(say.Dispose)
            W, H_ = CANVAS["size"] or (CV["rect"][2], CV["rect"][3])
            regions, kinds = CANVAS["regions"], CANVAS["kinds"]
            made = []                                 # (wrapper, kind) in drawing order
            made.append((Kit.add_tiled(grid, Kit.SECTION_TILE, 0, 0, W, H_,
                                       Kit.SECTION_ALPHA if canvas_unified() else st.opacity), "bg"))
            for slot in CANVAS["order"]:              # the seams: right and bottom edges
                x, y, w, h = regions[slot]
                if x + w < W:
                    made.append((box(x + w - 1, y, 1, h, C_SEAM, 0.8), "seam"))
                if y + h < H_:
                    made.append((box(x, y + h - 1, w, 1, C_SEAM, 0.8), "seam"))
            for slot in CANVAS["order"]:              # a minimized bag's own icon, centred
                kind, graphic, bag = kinds[slot]
                if kind != "mini":
                    continue
                g = H.gumps.get(bag)
                try:
                    icon = int(R.f_data.GetValue(g).IconizedGraphic) or DEFAULT_ICONS[1]
                except Exception:
                    icon = DEFAULT_ICONS[1]
                x, y, w, h = regions[slot]
                iw, ih = Kit.pic_size(icon)
                iw, ih = (iw or 30), (ih or 30)
                made.append((Kit.add_pic(grid, icon, x + (w - iw) // 2, y + (h - ih) // 2,
                                         mouse=False), "icon"))
            labels = []
            for slot in CANVAS["order"]:
                labels.extend(region_labels(grid, slot, regions[slot], kinds[slot]))
            made.extend(labels)
            if not CANVAS["order"]:                   # no bag in any slot yet
                for i, line in enumerate(Kit.wrap("No bags yet. Click Slots to put a bag in "
                                                  "each slot.", max(60, W - 16))[:3]):
                    made.append((Kit.add_label(grid, line, 8, 8 + 20 * i, Kit.HUE_INFO), "lbl"))
            counts = []
            for idx in range(st.slots):               # Find's "n found", one per slot
                cnt = Kit.add_label(grid, "", 0, 0, Kit.HUE_GOOD)
                try:                                  # (2.6.82: no lambda per label)
                    cnt.IsVisible = False
                except Exception:
                    pass
                r = regions.get(idx)
                counts.append((cnt, r[0], r[1], r[2], r[3]) if r else (cnt, 0, 0, 0, 0))
                made.append((cnt, "count"))
            Kit.flush()                               # the Adds land on the grid first
            layers_at = len([m for m in made if m[1] != "count"])
            parts = []
            for w, kind in made:
                raw = into_canvas(w)
                if raw is None:
                    continue
                parts.append(raw)
                if kind == "bg":
                    CV["bg"] = raw
                elif kind == "icon":
                    raw.Alpha = st.opacity
                    CV["icons"].append(raw)
            CV["parts"] = parts
            # the layers: one per region, in slot order, between the labels and the counts
            old = CV["layers"]
            keep = {}
            for slot in CANVAS["order"]:
                lay = old.pop(slot, None)
                if lay is None or lay.IsDisposed:
                    try:
                        lay = R.Layer()
                    except Exception:
                        lay = R.Layer(None)
                    lay.AcceptMouseInput = False
                R.f_bounds.SetValue(lay, R.Rect(0, 0, int(W), int(H_)))
                keep[slot] = lay
            if old:                                   # regions gone: their items go too
                gone = list(old.values())             # (2.6.82: one pass over the items)
                pool = CV["pool"]
                drop = []
                for s in CV["owner"]:
                    pc = pool.get(s)
                    if pc is not None:
                        par = pc.Parent
                        for lay in gone:
                            if par is lay:
                                drop.append(s)
                                break
                for s in drop:
                    item_drop(s)
                for lay in gone:
                    try:
                        lay.Dispose()
                    except Exception:
                        pass
            CV["layers"] = keep
            kids = c.Children
            order = parts[:layers_at] + [keep[s] for s in CANVAS["order"]] + parts[layers_at:]
            for ctl in order:                         # exactly this order, each once
                ctl.Parent = c
            in_order = set(order)                     # (2.6.82: hashed once, not a list scan)
            for ctl in list(kids):
                if ctl not in in_order:
                    kids.Remove(ctl)
            ui["counts"] = counts
            ui["count_state"] = {}
            CV["built"] = CANVAS["ver"]
            CV["bsize"] = (W, H_)
            CV["seen_n"], CV["seen_last"], CV["seen_min"] = {}, {}, {}   # every bag synced again
            for slot in CANVAS["order"]:
                kind, graphic, bag = kinds[slot]
                g = H.gumps.get(bag)
                if g is not None and kind in ("open", "mini"):
                    canvas_resync(bag, g)
                elif CV["items"].get(bag):            # closed since: its items go
                    for s in list(CV["items"][bag]):
                        item_drop(s)
                    CV["items"][bag] = []
            if SR["counts"]:
                show_counts()                         # a search still lit: on the new regions

        def region_labels(grid, slot, reg, info):
            """[(label wrapper, kind)] of one region (section 8): the first line
            (#slot gold, the bag's name grey, the count grey), the second (Closed /
            Minimized); none in a region under LABEL_MIN_W x LABEL_MIN_H, the
            first line only under LABEL_TWO_H. A board: #slot and Game board."""
            kind, graphic, bag = info
            x, y, w, h = reg
            if w < LABEL_MIN_W or h < LABEL_MIN_H:
                return []
            if kind == "open" and not has_line(reg):
                # 2.6.81 (IN1-2): an open bag's items fill a region too low for a
                # label line (item_box), so no label is drawn under them; closed /
                # minimized / board regions hold no items and keep theirs
                return []
            out = []
            tag = "#%d" % (slot + 1)
            out.append((Kit.add_label(grid, tag, x + 5, y + 3, Kit.HUE_TITLE), "lbl"))
            nx = x + 5 + Kit.text_w(tag) + 6
            if kind == "board":
                name = Kit.fit("Game board", max(8, x + w - 4 - nx))
                out.append((Kit.add_label(grid, name, nx, y + 3, Kit.HUE_INFO), "lbl"))
                return out
            whole = bag_name(bag, False)
            room = x + w - nx - (6 + Kit.text_w(COUNT_DIGITS) if kind == "open" else 0) - 10
            name = Kit.fit(whole, max(8, room))
            out.append((Kit.add_label(grid, name, nx, y + 3, Kit.HUE_INFO), "lbl"))
            CV["label"][slot] = (whole, name != whole)
            if kind == "open":
                n = len(CV["items"].get(bag) or ())
                cnt = Kit.add_label(grid, str(n), nx + Kit.text_w(name) + 6, y + 3, Kit.HUE_INFO)
                CV["count"][bag] = cnt
                out.append((cnt, "lbl"))
            elif h >= LABEL_TWO_H:
                out.append((Kit.add_label(grid, "Minimized" if kind == "mini" else "Closed",
                                          x + 5, y + 3 + LABEL_PITCH, Kit.HUE_INFO), "lbl"))
            return out

        def canvas_sync():
            """Module tick: the canvas's parts built again when the split or its
            size changed; its opacity in place."""
            if st.canvas is None or CV["ctrl"] is None or CANVAS["size"] is None:
                return
            if CV["built"] != CANVAS["ver"] or CV["bsize"] != CANVAS["size"]:
                if CV["rect"] is not None and (CV["rect"][2], CV["rect"][3]) != CANVAS["size"]:
                    return                            # the grid is drawn at the new size first
                if dragging():                        # (2.6.85) at the drop
                    return
                canvas_parts()
            canvas_alpha()
            canvas_safety()

        # ---- items: one client item control per item, pooled by serial ----
        def world_of(g):
            w = CV["world"]
            if w is None:
                try:
                    w = CV["world"] = g.World
                except Exception:
                    w = None
            return w

        def world_item(g, serial):
            """The client's item `serial`, or None. (2.6.79) Through World.Get:
            World.Items is a plain Dictionary, and its Get is a C# extension
            method IronPython can't see (2.6.78 always got None here)."""
            w = world_of(g)
            try:
                return w.Get(UInt32(int(serial))) if w is not None else None
            except Exception:
                return None

        def art_of(ctl, graphic):
            """An item graphic's art size at 100%, read off a control whose Graphic
            was just set (it is the art's size then), and kept per graphic."""
            r = R.f_bounds.GetValue(ctl)
            a = (int(r.Width), int(r.Height))
            if graphic not in CV["art"]:
                if len(CV["art"]) > 2000:
                    CV["art"].clear()
                CV["art"][graphic] = a
            return a

        def art_size(graphic):
            """The art size of any graphic (an item held from elsewhere): kept, or
            read off a probe control made once for it."""
            a = CV["art"].get(graphic)
            if a is not None:
                return a
            g = st.grid_raw
            try:
                probe = R.CanvasItem(g, UInt32(0), UInt16(int(graphic)), UInt16(0), 0, 0, False)
            except Exception:
                return 44, 44
            try:
                if probe.IsDisposed:                  # no art for it
                    return 1, 1
                return art_of(probe, graphic)
            finally:
                safe(probe.Dispose)

        def item_drop(serial):
            c = CV["pool"].pop(serial, None)
            bag = CV["owner"].pop(serial, None)
            CV["spot"].pop(serial, None)
            if c is not None:
                try:
                    p = c.Parent
                    if p is not None:
                        kids = p.Children
                        while kids.Contains(c):
                            kids.Remove(c)
                    c.Dispose()
                except Exception:
                    pass
            if bag is not None:
                lst = CV["items"].get(bag)
                if lst and serial in lst:
                    lst.remove(serial)

        def canvas_resync(bag, g):
            """One bag's items again, from its hidden window's own item controls
            (the client's filtering, draw order and drawn graphic), the place,
            amount and hue from the client's item: controls re-used by serial, made
            only for new serials, gone ones disposed."""
            kids = g.Children
            n = kids.Count
            mini = bool(g.IsMinimized)
            CV["seen_n"][bag] = n
            CV["seen_last"][bag] = kids[n - 1] if n else None
            CV["seen_min"][bag] = mini
            slot = CANVAS["slot_of"].get(bag)
            lay = CV["layers"].get(slot) if slot is not None else None
            if lay is None:
                return
            want = []
            if not mini and CANVAS["kinds"][slot][0] == "open":
                for i in range(n):
                    ch = kids[i]
                    if isinstance(ch, R.ItemGump) and not ch.IsDisposed:
                        want.append(ch)
            pool, owner = CV["pool"], CV["owner"]
            old = CV["items"].get(bag) or []
            new = []
            ctrls = []
            # (2.6.82) per bag once: the world, the region's map, the scale; per
            # item what the canvas set last is kept on its control (va_gr, va_hue,
            # va_sz, va_xy: the canvas is its only writer, see canvas_hue), so only
            # a change is written and nothing is read back; bag_sum's sum is made
            # in the same loop (one World lookup an item, not two)
            w = world_of(g)
            ctx = spot_ctx(slot)
            si = CANVAS.get("si")
            cs = H.scale or 1.0
            spots = CV["spot"]
            mk, U32, U16 = R.CanvasItem, UInt32, UInt16
            t = 0
            for ch in want:
                s = int(ch.LocalSerial)
                gr = int(ch.Graphic)
                try:
                    it = w.Get(U32(s)) if w is not None else None
                except Exception:
                    it = None
                hue = int(it.Hue) if it is not None else int(ch.Hue)   # (Find's client hue too)
                c = pool.get(s)
                if c is not None and c.IsDisposed:
                    item_drop(s)
                    c = None
                if c is None:
                    try:
                        c = mk(g, U32(s), U16(gr), U16(hue), 0, 0, False)
                    except Exception:
                        continue
                    if c.IsDisposed:                  # no art: the client shows nothing either
                        continue
                    c.va_art = art_of(c, gr)          # (its size now is its art at 100%)
                    c.va_gr, c.va_hue, c.va_sz, c.va_xy = gr, hue, None, None
                    pool[s] = c
                elif c.va_gr != gr:                   # (coins: the amount picks the art)
                    c.Graphic = U16(gr)               # (resets its size to the art's)
                    if c.IsDisposed:                  # no art for it: a fresh one next resync
                        pool.pop(s, None)
                        owner.pop(s, None)
                        continue
                    c.va_art = art_of(c, gr)
                    c.va_gr, c.va_sz = gr, None
                if c.va_hue != hue:
                    c.Hue = U16(hue)
                    c.va_hue = hue
                was = owner.get(s)
                if was is not None and was != bag:    # moved here from another slot's bag
                    lst = CV["items"].get(was)
                    if lst and s in lst:
                        lst.remove(s)
                owner[s] = bag
                aw, ah = c.va_art
                if si:                                # (pic_size)
                    pw, ph = max(1, int(aw * cs)), max(1, int(ah * cs))
                else:
                    pw, ph = aw, ah
                if c.va_sz != (pw, ph):
                    r = R.f_bounds.GetValue(c)
                    if int(r.Width) != pw or int(r.Height) != ph:
                        R.f_bounds.SetValue(c, R.Rect(int(r.X), int(r.Y), pw, ph))
                    c.va_sz = (pw, ph)
                if it is not None:
                    bx, by = int(it.X), int(it.Y)
                else:                                 # (a client control's X / Y are by-ref:
                    bx, by = get_pos(ch)              # never read them straight, 2.6.79)
                x, y = item_spot(ctx, s, aw, ah, pw, ph, bx, by)
                if c.va_xy != (x, y):
                    move(c, x, y)
                    c.va_xy = (x, y)
                spots[s] = (x + pw // 2, y)
                new.append(s)
                ctrls.append(c)
                if it is None:                        # (bag_sum, item by item, in this order)
                    t += s
                else:
                    try:
                        am = int(it.Amount)
                    except Exception:
                        am = 0
                    t = (t * 31 + s * 7 + bx * 131 + by * 137 + hue * 139 + am * 149) & 0x7FFFFFFF
            if old:
                in_new = set(new)                     # (2.6.82: a set, not a list scan)
                for s in old:                         # gone from this bag
                    if s not in in_new and owner.get(s) == bag:
                        item_drop(s)
                        PIN.pop(s, None)
            CV["items"][bag] = new
            lk = lay.Children
            same = lk.Count == len(ctrls)
            if same:
                for i in range(len(ctrls)):
                    if lk[i] is not ctrls[i]:
                        same = False
                        break
            if not same:
                for c in ctrls:                       # in the bag's own order, each once
                    c.Parent = lay
                keep = set(ctrls)                     # (2.6.82: hashed once, no .NET Equals scan)
                for c in list(lk):
                    if c not in keep:
                        lk.Remove(c)
            cnt = CV["count"].get(bag)
            if cnt is not None:
                Kit.set_text(cnt, str(len(new)))
            CV["sums"][bag] = t

        def bag_sum(g, serials, t=0):
            """A cheap sum of (serial, x, y, hue, amount) of a bag's items as drawn
            (canvas_resync makes the same sum as it goes). (2.6.82) From t: a bag
            summed a part at a time carries its sum on."""
            w = world_of(g)
            U32 = UInt32
            for s in serials:
                try:
                    it = w.Get(U32(int(s))) if w is not None else None
                except Exception:
                    it = None
                if it is None:
                    t += s
                    continue
                t = (t * 31 + s * 7 + int(it.X) * 131 + int(it.Y) * 137 + int(it.Hue) * 139
                     + int(it.Amount) * 149) & 0x7FFFFFFF
            return t

        SAFETY_EVERY = 0.2              # (2.6.82) s between two looks of canvas_safety
        SAFETY_CHUNK = 30               # (2.6.82) items summed per look (a big bag: over several)

        def canvas_safety():
            """Module tick: a bag whose items changed with no rebuild of its window
            (a hue set client-side) is synced again. (2.6.82) One look every
            SAFETY_EVERY s, at most SAFETY_CHUNK items a look: a big bag is summed
            over several looks (started again if it was synced meanwhile), so a
            look never costs more than that; was every bag whole every tick."""
            order = CANVAS["order"]
            if not order:
                return
            now = time.time()
            if 0 <= CV["sum_at"] - now <= SAFETY_EVERY:
                return
            CV["sum_at"] = now + SAFETY_EVERY
            part = CV["sum_part"]
            if part is not None:
                bag, g, src, n, lst, i, t = part
                if CV["items"].get(bag) is not src or len(src) != n or g.IsDisposed \
                        or H.gumps.get(bag) is not g:
                    part = None                       # synced (or gone) since: no sum owed
                    CV["sum_part"] = None
            if part is None:
                i = CV["sum_i"] % len(order)
                CV["sum_i"] = i + 1
                kind, graphic, bag = CANVAS["kinds"][order[i]]
                if kind != "open":
                    return
                g = H.gumps.get(bag)
                if g is None or g.IsDisposed:
                    return
                src = CV["items"].get(bag)
                lst = tuple(src) if src else ()
                n, i, t = len(src) if src is not None else -1, 0, 0
            end = i + SAFETY_CHUNK
            if end < len(lst):
                CV["sum_part"] = (bag, g, src, n, lst, end, bag_sum(g, lst[i:end], t))
                return
            CV["sum_part"] = None
            if bag_sum(g, lst[i:], t) != CV["sums"].get(bag):
                canvas_resync(bag, g)

        def canvas_hue(serial, hue):
            """(2.6.78) Find set an item's hue client-side: the canvas shows it now."""
            c = CV["pool"].get(serial)
            if c is None:
                return
            h = int(hue) & 0xFFFF
            try:
                if not c.IsDisposed and c.va_hue != h:    # (2.6.82: what the canvas set last)
                    c.Hue = UInt16(h)
                    c.va_hue = h
            except Exception:
                pass

        # ---- the mouse on the canvas (client thread: a mouse event) ----
        def region_at(x, y):
            for slot in CANVAS["order"]:
                r = CANVAS["regions"].get(slot)
                if r is not None and r[0] <= x < r[0] + r[2] and r[1] <= y < r[1] + r[3]:
                    return slot
            return None

        def tile_of(graphic):
            arr = CV["tiles"]
            if arr is None:
                f = getattr(R, "f_tiles", None)
                if f is None:
                    return None
                arr = CV["tiles"] = f.GetValue(None)
            if arr is None or graphic < 0 or graphic >= arr.Length:
                return None
            return arr[graphic]

        def takes_drop(it, hold):
            """An item the held one goes into or on to: a container, a stack of the
            same graphic, or one of STACK_ON (as ContainerGump.OnMouseUp)."""
            try:
                gr = int(it.Graphic)
            except Exception:
                return True
            if gr in STACK_ON:
                return True
            t = tile_of(gr)
            if t is None:
                return True                           # no tile data: the client decides
            try:
                if bool(t.IsContainer):
                    return True
                return bool(t.IsStackable) and gr == int(Tz.get(hold, "Graphic"))
            except Exception:
                return True

        def bag_window_up(serial, button):
            """Hand a let-go to the bag window the item is in: the client picks the
            target (into a container, on to a stack, a target cursor, the name of
            a single click), checks the distance and plays its own sound."""
            bag = CV["owner"].get(serial)
            g = H.gumps.get(bag) if bag is not None else None
            if g is None or g.IsDisposed:
                return False
            g.OnMouseUp(0, 0, button)
            return True

        def in_reach(bag):
            g = H.gumps.get(bag)
            w = world_of(g) if g is not None else CV["world"]
            if w is None:
                return True
            try:
                it = w.Get(UInt32(int(bag)))       # (2.6.79: not Items.Get, see world_item)
                if it is None:
                    return True
                root = w.Get(it.RootContainer)
                return root is None or int(root.Distance) <= DRAG_RANGE
            except Exception:
                return True                           # the server decides

        def cant():
            safe(lambda: API.PlaySound(SOUND_CANT))

        def canvas_mouse_up(x, y, button):
            """Section 7's table. True when handled."""
            b = str(button)
            up = R.up_item
            R.up_item = None
            up_s = int(up.LocalSerial) if up is not None and not up.IsDisposed else None
            if b == "Left":
                hold = item_hold()
                if hold is not None:
                    if up_s is not None:
                        it = world_item(H.gumps.get(CV["owner"].get(up_s)), up_s)
                        if it is not None and takes_drop(it, hold):
                            return bag_window_up(up_s, button)
                    slot = region_at(x, y)
                    if slot is None:
                        return True
                    canvas_drop(slot, x, y, hold)
                    return True
                if st.flt_pick is not None:           # (2.6.85) a filter waits for its bag
                    slot = region_at(x, y)
                    if slot is not None:
                        kinds = CANVAS["kinds"].get(slot)
                        slots = dict((b, i) for i, b in st.layout)
                        if kinds is not None and kinds[2] in slots:
                            act(filter_canvas_pick, slots[kinds[2]])()
                            return True
                if up_s is not None:                  # a target cursor, or a single click
                    if not CV["texts"] and not target_up():
                        CV["said"] = (up_s, time.time())   # its name: from the journal
                    return bag_window_up(up_s, button)
                slot = region_at(x, y)
                if slot is None:
                    return False
                kind, graphic, bag = CANVAS["kinds"][slot]
                r = CANVAS["regions"][slot]
                # 2.6.81 (IN1-2): only where a label line is drawn (items fill the rest)
                if kind == "open" and has_line(r) and y < r[1] + LABEL_LINE_H and not target_up():
                    act(bag_min, bag, True)()          # its label line: minimize it
                    return True
                return False
            if b == "Right":
                if up_s is not None:
                    return True                       # on an item: nothing
                slot = region_at(x, y)
                if slot is not None and CANVAS["kinds"][slot][0] == "open":
                    act(bag_close, CANVAS["kinds"][slot][2])()
                    return True
            return False

        def target_up():
            try:
                return bool(API.HasTarget())
            except Exception:
                return False

        def canvas_drop(slot, x, y, hold):
            """An item let go on slot's region (empty space, a label, an icon, or an
            item that takes nothing)."""
            kind, graphic, bag = CANVAS["kinds"][slot]
            if not in_reach(bag):
                cant()
                return
            hs = int(Tz.get(hold, "Serial"))
            if hs == bag:                             # a bag into itself: DropItem refuses it
                cant()
                return
            import System
            if kind != "open":                        # closed, minimized, a grid container, a board
                Tz.call(None, "DropItem", (System.UInt32(hs), 0xFFFF, 0xFFFF, 0,
                                           System.UInt32(int(bag)), False), R.Actions)
                return
            px, py = x, y
            try:
                if bool(R.p_profile.GetValue(None).RelativeDragAndDropItems):
                    off = Tz.get(hold, "MouseOffset")
                    px, py = px + int(off.X), py + int(off.Y)
            except Exception:
                pass
            b = H.bounds.get(graphic)
            if b is None:
                Tz.call(None, "DropItem", (System.UInt32(hs), 0xFFFF, 0xFFFF, 0,
                                           System.UInt32(int(bag)), False), R.Actions)
                return
            aw, ah = art_size(int(Tz.get(hold, "DisplayedGraphic")))
            pw, ph = pic_size(aw, ah)
            cs = H.scale or 1.0
            box = item_box(CANVAS["regions"][slot])
            cl_x, ch_x, cl_y, ch_y = centre_range(box, pw, ph)
            cx = max(cl_x, min(ch_x, px))             # where it shows: wholly in its region
            cy = max(cl_y, min(ch_y, py))
            bx, by = canvas_to_bag(b, box, aw, ah, cs, cx, cy)
            sx, sy = client_clamp(b, aw, ah, cs, bx, by)   # what the client will store
            Tz.call(None, "DropItem", (System.UInt32(hs), sx, sy, 0, System.UInt32(int(bag)),
                                       False), R.Actions)
            pin_set(hs, int(bag), sx, sy, cx, cy)
            try:
                Tz.put(None, "CancelDoubleClick", True, R.Mouse)
            except Exception:
                pass

        def canvas_double(x, y, button):
            if str(button) != "Left":
                return False
            slot = region_at(x, y)
            if slot is None:
                return False
            kind, graphic, bag = CANVAS["kinds"][slot]
            if kind in ("closed", "board"):
                act(bag_use, bag)()
                return True
            if kind == "mini":
                act(bag_min, bag, False)()
                return True
            return False

        TIPS = {"closed": "Double-click to open this bag; an item let go here goes into it",
                "mini": "Double-click to restore this bag; an item let go here goes into it",
                "board": "Double-click to open this board; an item let go here goes into it",
                "body": "Right-click to close this bag",
                "line": "Click to minimize this bag"}

        def canvas_hover(c, x, y):
            """The canvas's tooltip follows the region under the mouse (set only when
            the region or its part changes)."""
            slot = region_at(x, y)
            part = None
            if slot is not None:
                kind = CANVAS["kinds"][slot][0]
                part = kind
                if kind == "open":
                    r = CANVAS["regions"][slot]
                    # 2.6.81 (IN1-2): a label line only where one is drawn
                    part = "line" if has_line(r) and y < r[1] + LABEL_LINE_H else "body"
            key = (slot, part, CANVAS["ver"])
            if key == CV["tip"]:
                return
            CV["tip"] = key
            text = TIPS.get(part, "")
            if part == "line":
                lab = CV["label"].get(slot)
                if lab is not None and lab[1]:        # its name was cut: whole, first
                    text = "%s. Click to minimize this bag." % lab[0]
            c.SetTooltip(text)

        def bag_use(bag):
            """A closed (or grid-container, or board) region double-clicked: the
            player's own press opens it."""
            API.UseObject(bag)

        def bag_min(bag, value):
            g = H.gumps.get(bag)
            if g is not None and not g.IsDisposed and bool(g.IsMinimized) != value:
                g.IsMinimized = value

        def bag_close(bag):
            """Right-click on an open bag's region: the client's close for its window."""
            g = H.gumps.get(bag)
            if g is not None and not g.IsDisposed:
                g.Dispose()

        # ---- single-click names: the hidden bag windows' texts, drawn on the canvas ----
        def canvas_texts(batcher, sx, sy):
            """The canvas's Draw, after its items: each hidden bag window's overhead
            texts (an item's name after a single click), over that item. A quiet
            frame costs one read per bag."""
            try:
                spots = CV["spot"]
                trs = H.gtr
                for slot in CANVAS["order"]:
                    info = CANVAS["kinds"][slot]
                    if info[0] != "open":
                        continue
                    g = H.gumps.get(info[2])
                    if g is None:
                        continue
                    tr = trs.get(g)                   # (2.6.82) a window's own renderer, made
                    if tr is None:                    # with it (get-only): read once
                        tr = g.TextRenderer
                        if len(trs) >= GINFO_CAP:
                            trs.clear()
                        trs[g] = tr
                    o = tr.DRight
                    if o is None:
                        continue
                    while o is not None:
                        own = o.Owner
                        if not o.IsDestroyed and own is not None and o.TextBox is not None:
                            try:
                                os_ = int(own.Serial or 0)
                            except Exception:
                                os_ = 0
                            sp = spots.get(os_)
                            if sp is not None:
                                o.X, o.Y = sp[0], sp[1]
                                tw, th = get_size(o.TextBox)   # (2.6.79: by-ref Width / Height)
                                o.RealScreenPosition = R.Point(
                                    sp[0] - (tw >> 1),
                                    sp[1] - int(o.OffsetY) - th)
                        o = o.DRight
                    tr.Draw(batcher, sx, sy, True)
            except Exception as e:
                CV["texts"] = False                   # this build: the journal fallback instead
                H.error = "canvas texts: %s" % e

        SAY_SECS = 4.0                                # a name shown for this long (the client's 4 s)
        SAY_WAIT = 1.5                                # ...from a journal line this soon after the click

        def canvas_say_tick(now):
            """(2.6.78) The fallback when the hidden windows' texts can't be drawn on
            this build: the journal line that follows a single click on an item is
            shown over the item for SAY_SECS, as one pooled label."""
            if CV["texts"] or st.canvas is None:
                return
            lbl = CV["say_lbl"]
            said = CV["said"]
            rd = JR["rd"]
            if said is not None and rd is not None:
                serial, t0 = said
                for ln in rd.new():
                    if ln.at < t0 - 0.05 or ":" in ln.text[:24]:
                        continue                      # older, or a module's own line
                    sp = CV["spot"].get(serial)
                    CV["said"] = None
                    if sp is None or CV["ctrl"] is None:
                        break
                    if lbl is None:
                        grid = ui.get("grid")
                        if grid is None:
                            break
                        lbl = Kit.add_label(grid, "", 0, 0, Kit.HUE_TEXT)
                        Kit.flush()
                        into_canvas(lbl)
                        CV["say_lbl"] = lbl
                    text = Kit.fit(ln.text, 200)
                    Kit.set_text(lbl, text)
                    lbl.SetPos(max(0, sp[0] - Kit.text_w(text) // 2), max(0, sp[1] - 18))
                    lbl.IsVisible = True
                    CV["say_shown"] = True
                    CV["say_until"] = now + SAY_SECS
                    break
                else:
                    if now - t0 > SAY_WAIT:
                        CV["said"] = None
            if lbl is not None and CV["say_shown"] and now >= CV.get("say_until", 0.0):
                CV["say_shown"] = False               # (2.6.82) hidden once, not every tick
                try:
                    lbl.IsVisible = False
                except Exception:
                    pass

        def item_hold():
            """The client's held item (ItemHold) while one is on the cursor, else None."""
            h = H.hold
            if h is None:
                game = Tz.get(None, "Game", Tz.T("ClassicUO.Client"))
                h = H.hold = Tz.get(Tz.get(game, "UO"), "GameCursor")
                h = H.hold = Tz.get(h, "ItemHold")
            if not bool(Tz.get(h, "Enabled")) or bool(Tz.get(h, "IsFixedPosition")):
                return None
            return h

        # ---------- (2.6.67) shrunk to fit the zone under the Paperdoll ----------
        #  While combined in two zones, a bag grid with more rows than the lower
        #  zone holds is shown at a smaller container scale (the client's own
        #  Container Scale, items scaled with it) so it fits; your Bag scale is
        #  kept aside (SHRINK_KEY, in case the script stops without putting it
        #  back) and given back when the room is there again, when the bags part
        #  from the Paperdoll, and when Bags stops.
        shrink = {"pct": None, "said": None}

        def scale_now():
            """(pct, items) the client gets: your Bag scale, or less while shrunk."""
            p = shrink["pct"]
            if p is not None and p < st.scale_pct:
                return p, True
            return st.scale_pct, st.scale_items

        def note_shrunk():
            if shrink["pct"] is None:
                Kit.put_var(SHRINK_KEY, "")
            else:
                Kit.put_var(SHRINK_KEY, "%d|%d" % (st.scale_pct, 1 if st.scale_items else 0))

        def bag_shrink(pct, by_pack=False):
            """(2.6.67) bag.shrink: show the combined grid at pct % so it fits its
            zone (None, or your own scale or more: your Bag scale again). Only
            while combined, with client access; never under SHRINK_MIN. (2.6.78)
            Never while the canvas can be used: Container Scale is never changed
            in a zone again (a scale left shrunk goes back)."""
            if pct is not None and not (R.ok and not H.disabled and attached()):
                pct = None
            if pct is not None and canvas_ok():
                pct = None
            if pct is not None and shrink["pct"] is None:
                got = safe(read_scale)                # yours, as the client has it now
                if got:
                    st.scale_pct, st.scale_items = got
            if pct is not None:
                pct = max(SHRINK_MIN, int(pct))
                if pct >= st.scale_pct:
                    pct = None
            if pct == shrink["pct"]:
                return
            was = shrink["pct"]
            before = H.scale
            shrink["pct"] = pct
            try:
                apply_scale(*scale_now())
            except Exception as e:
                shrink["pct"] = was
                API.SysMsg(TITLE + ": couldn't change the bag scale (%s)." % e, HUE_ERR)
                return
            note_shrunk()
            # the slots follow the new scale at once (the open bags are measured
            # again on the next frames and the slots set to them exactly), so the
            # Paperdoll's sums never see the backpack's size in between
            if before > 0 and H.scale > 0:
                f = H.scale / before
                st.cell_w = max(1, min(MAX_CELL, int(round(st.cell_w * f))))
                st.cell_h = max(1, min(MAX_CELL, int(round(st.cell_h * f))))
            st.fit_pending = True
            st.dirty_frame = True
            schedule_save()
            # (2.6.72) no journal line: the side panel's status line says it
            if not (st.job or st.sort):
                set_status("Idle")

        def unshrink_left():
            """At start: a scale left shrunk (the script stopped before putting it
            back) is put back."""
            raw = Kit.get_var(SHRINK_KEY)
            if not raw:
                return
            p = raw.split("|")
            try:
                pct, items = int(p[0]), (len(p) > 1 and p[1] == "1")
            except Exception:
                Kit.put_var(SHRINK_KEY, "")
                return
            if R.ok and 50 <= pct <= 200:
                try:
                    apply_scale(pct, items)
                    st.scale_pct, st.scale_items = pct, items
                except Exception:
                    return                            # tried again next start
            Kit.put_var(SHRINK_KEY, "")

        def paperdoll_fit(w, h):
            """(2.6.57) bag.fit: the fitted Paperdoll's hole for the grid is w x h
            (None: the grid at its own size again). The grid fills it edge to edge
            in the Paperdoll's look: the columns from the hole's shape, the slots
            grown to share it, the whole hole backed with the black section so no
            spare cell shows the game through. Only while combined."""
            area = (int(w), int(h)) if (w is not None and h is not None and attached()) else None
            if area is None:
                if fitov["area"] is not None:
                    fitov["area"] = None
                    layout_fit(None, None, None)
                    st.dirty_frame = True
                return
            if area != fitov["area"]:
                fitov["area"] = area
                layout_fit(area[0], area[1], "w")
                st.dirty_frame = True

        def bag_pack(width, height):
            """bag.pack, for the Paperdoll's sums: (None, need) while the canvas can
            be used combined (whatever Trim says): the height the bags take across
            width (less the side panel) at your own Bag scale, their item areas
            with no shelf waste, at least 80 px. None otherwise (the Paperdoll then
            uses bag.cell). (2.6.78: the canvas never shrinks anything.)"""
            if not (canvas_ok() and attached()):
                return None
            side = 0 if side_off() else side_width(max(60, min(int(height), 1000)))
            aw = int(width) - side
            if aw < 40:
                return None
            tot = 0.0
            for _slot, a, _r in split_weights(split_input()):
                tot += a
            k = own_pct() / 100.0
            need = max(80, int(math.ceil(tot * k * k / aw)))
            if int(height) < (1 << 19):           # a real room: the canvas fills it, never more
                need = min(need, max(1, int(height)))
            return None, need

        def side_off():
            """Combined with Paperdoll and bags only: the slots alone, no side
            panel (Paperdoll's window is the title bar and the frame)."""
            return st.side_hidden and not st.collapsed and attached()

        def top_off():
            """Distance from the title bar's top to the slots' top."""
            return 0 if (bare_on() or attached()) else BAR_H

        def attach_raw():
            """The client control of the Paperdoll window we follow (cached on it)."""
            att = st.attach
            if att is None:
                return None
            raw = att.get("raw")
            if raw is None or raw.IsDisposed:
                raw = raw_of(att.get("g")) if R.ok else None
                att["raw"] = raw
                if raw is not None:               # Paperdoll rebuilt its window: follow the new one
                    safe(lambda: Kit.attach(ui["grid"], att.get("g")))
            return raw

        def attach_to(info):
            """Paperdoll's one-window link: info is the dict it keeps up to date
            (g: its window, dx/dy: where our slots go inside it, shown: bags
            visible, state: open / collapsed / docked for the Action Bar, cmd: a
            callback for the bar's show / dock), or None to part again."""
            if info is None and st.attach is not None:
                safe(lambda: bag_shrink(None, True))  # (2.6.67) your Bag scale again
                if fitov["area"] is not None:         # (2.6.57) no longer in a fitted Paperdoll
                    fitov["area"] = None
                    layout_fit(None, None, None)
                st.frame_x, st.frame_y = st.saved_fx, st.saved_fy   # back to our own place
                st.detached_at = time.time()          # no place saved until the move settled
                # the draw hook and the fallback tracker take the lead position from the
                # title bar on the next frame: move it there first, or the bags would
                # stay at Paperdoll's hole and that place would be saved as ours
                H.bar_at = None
                for raw in (st.bar_raw, st.grid_raw):
                    try:
                        if raw is not None and not raw.IsDisposed:
                            move(raw, st.frame_x, st.frame_y)
                    except Exception:
                        pass
                for key in ("bar", "grid"):
                    g = ui.get(key)
                    if Kit.is_open(g):
                        safe(lambda g=g: g.SetPos(st.frame_x, st.frame_y))
                        safe(lambda g=g: Kit.moved_by_code(g))      # placed by code, not dragged
            elif info is not None:
                st.collapsed = st.docked = False      # Paperdoll's window folds and hides for us
                set_dock_wish(False)
                # the slots are built straight at Paperdoll's hole when it says where
                # that is (dx/dy), not at our old place and tracked over a frame later
                try:
                    lead = info.get("g")
                    if Kit.is_open(lead) and (info.get("dx") or info.get("dy")):
                        st.frame_x = int(lead.GetX()) + int(info.get("dx", 0))
                        st.frame_y = int(lead.GetY()) + int(info.get("dy", 0))
                except Exception:
                    pass
            st.attach = info
            st.dirty_frame = True

        def bare_btn_size():
            w, h = Kit.pic_size(ART_BARE[0])
            return (w or 15), (h or 15)

        def add_bare_button(grid, x, y, strip=True):
            if strip:                        # (2.6.85) sidebar minimized: its four actions stay
                add_quick_strip(grid, x - 4, y + max(0, (bare_btn_size()[1] - QUICK_ICON) // 2))
            if attached():                   # Paperdoll's window is the title bar
                # (2.6.72) a gold flap (it was the same gem as Sort)
                tip = "Show the side panel" if st.side_hidden else "Hide the side panel"
                Kit.art_button(grid, ui["store"], "bare", Kit.ART_DOCK, x, y, None, tip,
                               on_click=act(toggle_bare))
                return
            else:
                tip = ("Show the title bar and side panel again" if st.bare
                       else "Bags only: hide the title bar and side panel (click again to show them)")
            Kit.art_button(grid, ui["store"], "bare", ART_BARE, x, y, None, tip,
                           on_click=act(toggle_bare))

        def build_slots(grid, slot_raws, cols, cw, ch, gap, gw, gh, trim):
            """Draw the slot panels and the side panel; returns the overlay's width."""
            fit = max(4, (cw - 8) // 7)                 # characters of a bag name that fit a slot
            area = fitov["area"] if attached() else None
            if area is not None:
                # (2.6.57) in a fitted Paperdoll: the whole hole is the black section,
                # so a cell with no bag (and any odd pixel the cells leave) is black,
                # never the game showing through
                no_mouse(Kit.add_tiled(grid, Kit.SECTION_TILE, 0, 0, area[0], area[1],
                                       Kit.SECTION_ALPHA))
            for idx in range(st.slots):
                r, c = divmod(idx, cols)
                x, y = c * (cw + gap), r * (ch + gap)
                # The near-invisible box takes the mouse, so an item released on an
                # unused spot stays on your cursor instead of falling to the ground.
                drop = box(x, y, cw, ch, "#000000", 0.01)
                if bare_on():                           # drag a closed / empty slot to move the bags
                    try:
                        drop.CanMove = True
                    except Exception:
                        pass
                grid.Add(drop)
                Kit.add_tiled(grid, Kit.SECTION_TILE, x, y, cw, ch, st.opacity)
                if trim:
                    if c < cols - 1:
                        grid.Add(no_mouse(box(x + cw - 1, y, 1, ch, C_SEAM, 0.8)))
                    if idx + cols < st.slots:
                        grid.Add(no_mouse(box(x, y + ch - 1, cw, 1, C_SEAM, 0.8)))
                else:
                    for bx, by, bw, bh in ((x, y, cw, 1), (x, y + ch - 1, cw, 1),
                                           (x, y, 1, ch), (x + cw - 1, y, 1, ch)):
                        grid.Add(no_mouse(box(bx, by, bw, bh, C_EDGE, 0.9)))
                labs = [label(grid, "#%d" % (idx + 1), x + 5, y + 3, Kit.HUE_TITLE)]
                if idx in st.assign:
                    labs.append(label(grid, short(bag_name(st.assign[idx], False), fit), x + 5, y + 21,
                                      Kit.HUE_INFO))
                    labs.append(label(grid, "Closed", x + 5, y + 39, Kit.HUE_INFO))
                else:
                    labs.append(label(grid, short("Empty: click Slots", fit), x + 5, y + 21,
                                      Kit.HUE_INFO))
                slot_raws.append(tuple(raw_of(l) for l in labs) if R.ok else ())
                # Find's "n found" for this slot (bottom right, under the bag's items;
                # hidden until a search finds something here; see show_counts)
                cnt = label(grid, "", x + 5, y + max(0, ch - 18), Kit.HUE_GOOD)
                try:
                    cnt.IsVisible = False
                except Exception:
                    pass
                ui["counts"].append((cnt, x, y, cw, ch))
            if area is not None:
                # (2.6.58) the grid's spare cells (8 bags in a 3 x 3 grid) are black
                # cells too, never the game showing through
                for idx in range(st.slots, cols * int(math.ceil(st.slots / float(cols)))):
                    r, c = divmod(idx, cols)
                    no_mouse(Kit.add_tiled(grid, Kit.SECTION_TILE, c * (cw + gap), r * (ch + gap),
                                           cw, ch, st.opacity))
            if trim:
                for bx, by, bw, bh in ((0, 0, gw, 1), (0, gh - 1, gw, 1), (0, 0, 1, gh), (gw - 1, 0, 1, gh)):
                    grid.Add(no_mouse(box(bx, by, bw, bh, C_EDGE, 0.9)))
            if bare_on():                               # bags only: gilded corner + toggle
                kw, kh = Kit.pic_size(Kit.CORNER_ART)
                kw, kh = (kw or 30), (kh or 30)
                tw, th = bare_btn_size()
                kx, ky = gw - kw + GRIP_OUT, gh - kh + GRIP_OUT
                no_mouse(Kit.add_pic(grid, Kit.CORNER_ART, kx, ky))
                # the part of the knot outside the bags takes the drag (bags sit on top of the rest)
                Kit.catcher(grid, kx, ky, kw, kh, lambda *a: None, "Drag to move the bags",
                            movable=True)
                add_bare_button(grid, kx - tw - 3, gh + GEM_BELOW)
                total_w = kx + kw
                total_h = max(ky + kh, gh + GEM_BELOW + th)
                grid.SetRect(st.frame_x, st.frame_y, total_w, total_h)
                # kept current here too: Paperdoll reads it (bag.grid_size) the tick it
                # attaches, before the first combined rebuild
                st.grid_wh = (total_w, total_h)
                return total_w
            if side_off():                              # combined, bags only: the slots and the gem
                tw, th = bare_btn_size()
                if area is not None:                    # (2.6.57) the gem inside the hole
                    add_bare_button(grid, area[0] - tw - 2, area[1] - th - 2)
                    grid.SetRect(st.frame_x, st.frame_y, area[0], area[1])
                    st.grid_wh = area
                    return area[0]
                add_bare_button(grid, gw - tw, gh + GEM_BELOW)
                total_h = gh + GEM_BELOW + th
                grid.SetRect(st.frame_x, st.frame_y, gw, total_h)
                st.grid_wh = (gw, total_h)
                return gw
            pw, ph = build_side_panel(grid, gw + gap, gh)
            st.side_pw = gap + pw                       # (2.6.57) for the fit's sums
            total_w = gw + gap + pw
            if area is not None:                        # (2.6.57) the whole hole, edge to edge
                total_w, ph = max(total_w, area[0]), max(ph, area[1])
            grid.SetRect(st.frame_x, st.frame_y + top_off(), total_w, max(gh, ph))
            st.grid_wh = (total_w, max(gh, ph))
            return total_w

        # ---------- windows anchored to the Bags window ----------
        # The mother's Snap links a window the player let go against another to
        # that window (SNAP.links: follower -> leader), and moves it along when the
        # leader is dragged. Every rebuild here disposes the title bar and the
        # slots and makes new ones, which would drop those links; and bags only
        # (no title bar, no side panel, slots up where the bar was), or the slots
        # growing to fit a bag, moves the window's edges while the anchored windows
        # stay where they were. So before a rebuild the anchored windows are
        # collected, and after it each is linked to the new gumps and, when the
        # outline changed, put back against the edge it was on.
        anch = {"outline": None,      # the last full outline, relative to (frame_x, frame_y)
                "told": False}        # the player has been told anchored windows follow the edges

        def snap_reg():
            """The mother's Snap registry, or None on a build without it."""
            s = globals().get("SNAP")
            return s if s is not None and hasattr(s, "links") else None

        def gump_rect(g):
            """(x, y, w, h) of an open window with a real size, else None."""
            try:
                if g is None or g.IsDisposed:
                    return None
                x, y = int(g.GetX()), int(g.GetY())
                w, h = int(g.GetWidth() or 0), int(g.GetHeight() or 0)
            except Exception:
                return None
            if w <= 1 or h <= 1:          # the folded grid is a 1 x 1 carrier for the draw hook
                return None
            return x, y, w, h

        def frame_outline():
            """(x, y, w, h) round what is on screen of the Bags window: the title bar
            (unless bags only) and the slots with the side panel. None while it is
            folded (collapsed) or in the Action Bar (docked)."""
            if st.collapsed or st.docked:
                return None
            rects = []
            if not bare_on() and not attached() and st.canvas != "alone":   # combined: Paperdoll's
                r = gump_rect(ui["bar"])
                if r is not None:
                    rects.append(r)
            r = gump_rect(ui["grid"])
            if r is not None:
                rects.append(r)
            if not rects:
                return None
            x0 = min(r[0] for r in rects)
            y0 = min(r[1] for r in rects)
            x1 = max(r[0] + r[2] for r in rects)
            y1 = max(r[1] + r[3] for r in rects)
            return x0, y0, x1 - x0, y1 - y0

        def anchors_capture():
            """[(window, (x, y, w, h))] for every open window snapped on to the title
            bar or the slots, read before they are disposed."""
            out = []
            snap = snap_reg()
            if snap is None:
                return out
            bar, grid = ui["bar"], ui["grid"]
            try:
                items = list(snap.links.items())
            except Exception:
                return out
            for g, leader in items:
                if (leader is bar or leader is grid) and leader is not None and Kit.is_open(g):
                    r = gump_rect(g)
                    if r is not None:
                        out.append((g, r))
            return out

        def edge_pos(f0, f1, o0, o1, n0, n1):
            """One axis: where edge f0 of a window (spanning f0..f1) goes when the
            outline it sat against moves from o0..o1 to n0..n1. It keeps its offset
            from the outline's far edge when it is beyond it or lined up nearer to
            it, else from the near edge."""
            if f0 >= o1 - 2 or (f1 > o0 + 2 and abs(f1 - o1) < abs(f0 - o0)):
                return n1 + (f0 - o1)
            return n0 + (f0 - o0)

        def anchors_apply(followers):
            """After a rebuild: link the collected windows to the new title bar (the
            slots when bags only) and, when the outline changed, move each one with
            the edge it was anchored to (windows snapped on to those follow)."""
            snap = snap_reg()
            if snap is None:
                return
            leader = ui["grid"] if (bare_on() or attached() or st.canvas == "alone") else ui["bar"]
            if leader is None:
                leader = ui["grid"]
            safe(Kit.flush)                 # the bar / grid were just SetRect'ed: that is queued
            new = frame_outline()
            old = anch["outline"]
            if old is not None:            # back to where the window is now
                old = (st.frame_x + old[0], st.frame_y + old[1], old[2], old[3])
            if new is not None:
                anch["outline"] = (new[0] - st.frame_x, new[1] - st.frame_y, new[2], new[3])
            moved_n = 0
            for g, (fx, fy, fw, fh) in followers:
                if leader is None or not Kit.is_open(g):
                    continue
                try:
                    snap.links[g] = leader
                except Exception:
                    continue
                if old is None or new is None or old == new:
                    continue
                nx = edge_pos(fx, fx + fw, old[0], old[0] + old[2], new[0], new[0] + new[2])
                ny = edge_pos(fy, fy + fh, old[1], old[1] + old[3], new[1], new[1] + new[3])
                if (nx, ny) == (fx, fy):
                    continue
                try:
                    g.SetPos(int(nx), int(ny))
                except Exception:
                    continue
                moved_n += 1
                try:
                    if snap.last is not None:
                        snap.last[g] = (nx, ny)
                    Kit.moved_by_code(g)                           # placed by code, not dragged
                    snap.follow(g, nx - fx, ny - fy, set([g]))     # the windows snapped on to it
                except Exception:
                    pass
                fn = None
                try:
                    fn = snap.moved_cb.get(g)                       # it saves its new place
                except Exception:
                    pass
                if fn is not None:
                    try:
                        fn()
                    except Exception:
                        pass
            if moved_n and not anch["told"]:
                # said once per run: nothing else tells the player that windows snapped
                # on to the bag follow its edges when they move
                anch["told"] = True
                API.SysMsg(TITLE + ": %d window%s snapped on to the bags moved with its edge "
                           "(windows snapped on to the bags follow their edges)."
                           % (moved_n, "" if moved_n == 1 else "s"), HUE_INFO)

        def free_window():
            """2.6.81 (IN1-8): the Bags window is its own (not riding in Paperdoll,
            not the canvas, not given a slot in a zone): it is placed here, on
            screen, rather than by the layout or Paperdoll."""
            return not attached() and st.canvas is None and fitov["told"] is None \
                and not safe(lambda: HOST.layout_locked(KEY), False)

        def screen_dims(cols, rows, ch, gap):
            """2.6.81 (IN1-8): (cols, rows) so the free window's slots fit the
            screen's height: more columns when the rows would run off the bottom.
            The bags on the slots are the client's own windows, which can't scroll,
            so the grid is the one window that never scrolls (window rules 1): it
            is laid out to fit instead. Your Columns / Rows setting is untouched."""
            sh = Kit.screen()[1]
            if sh <= 0 or st.slots <= 1:
                return cols, rows
            fit_rows = max(1, (sh - top_off() - SCREEN_SLACK + gap) // (ch + gap))
            if rows <= fit_rows:
                return cols, rows
            c = int(math.ceil(st.slots / float(fit_rows)))
            return c, int(math.ceil(st.slots / float(c)))

        def build_frame():
            followers = anchors_capture()           # before the old gumps go (see above)
            canvas_detach()                         # (2.6.78) the canvas outlives the grid gump
            dispose("grid")
            dispose("bar")
            if st.canvas is not None and canvas_mode() == st.canvas:
                build_canvas_frame(followers)
                return
            if fitov["area"] is not None and attached() and st.geom is not None:
                # (2.6.67) in a fitted Paperdoll the slots are shared out from the
                # bags' size of now (grown, or shrunk to fit the zone), not the size
                # they had when the hole was last given
                layout_fit(fitov["area"][0], fitov["area"][1], "w")
                st.dirty_frame = False               # being drawn now
            elif fitov["told"] is not None and not attached() and st.geom is not None:
                # (2.6.71) the same in a zone of its own: a bigger bag, Trim or a
                # shrink changed the cells since the slot was given
                layout_fit(fitov["told"][0], fitov["told"][1], "w")
                st.dirty_frame = False
            cols, rows = layout_dims()
            trim = trimming()
            gap = 0 if trim else LOOSE_GAP
            cw, ch = fitov["cell"] or (st.cell_w, st.cell_h)   # (2.6.56) grown to fill a zone
            free = free_window()
            if free and not st.collapsed:
                cols, rows = screen_dims(cols, rows, ch, gap)  # 2.6.81 (IN1-8): never off the bottom
            gw = cols * cw + (cols - 1) * gap
            gh = rows * ch + (rows - 1) * gap
            st.geom = (cols, cw, ch, gap)
            st.icons_used = H.icons or DEFAULT_ICONS
            ui["store"] = ({}, {})
            ui["side_status"] = None
            ui["search_box"] = None          # (re)made with the side panel, if it is drawn
            ui["counts"] = []                # one per slot, made with the slots
            ui["count_state"] = {}

            bare = bare_on()
            grid = G.CreateGump(bare, bare)
            ui["grid_bare"] = bare
            st.grid_info = (raw_of(grid) if R.ok else None, bare)   # before the hook can run
            slot_raws = []
            if st.collapsed:                            # folded: the grid only carries the draw hook
                total_w = BAR_MIN_W
                grid.SetRect(st.frame_x, st.frame_y + BAR_H, 1, 1)
            else:
                total_w = build_slots(grid, slot_raws, cols, cw, ch, gap, gw, gh, trim)
            if free:
                # 2.6.81 (IN1-8): the pair (title bar and slots) starts wholly on screen
                # (as Kit.place does for a window); the keeper keeps it there as one
                pair_w = total_w if bare else max(total_w, BAR_MIN_W)
                pair_h = BAR_H if st.collapsed else \
                    top_off() + (st.grid_wh[1] if st.grid_wh else gh)
                nx, ny = Kit.clamp(st.frame_x, st.frame_y, pair_w, pair_h)
                if (nx, ny) != (st.frame_x, st.frame_y):
                    st.frame_x, st.frame_y = nx, ny
                    safe(lambda: grid.SetPos(nx, ny + (BAR_H if st.collapsed else top_off())))
            if R.ok and not H.disabled and not st.drive_fixed:
                try:
                    add_hook(grid)
                except Exception as e:
                    st.driving = st.drive_fixed = True
                    H.error = "draw hook: %s" % e
                    API.SysMsg(TITLE + ": couldn't install the draw hook (%s); keeping bags in "
                               "place from the script instead." % e, HUE_INFO)
            no_right_click_close(grid)
            try:
                enum_type = type(grid.LayerOrder)
                grid.LayerOrder = getattr(enum_type, "Under")
            except Exception:
                pass
            G.AddGump(grid)
            ui["grid"] = grid

            bar = make_bar(total_w, st.docked or bare or attached(), free)
            if attached():
                # Paperdoll's window leads; the host's keeper moves the two as one
                st.attach_g = st.attach.get("g")
                safe(lambda: Kit.attach(grid, st.attach_g))
            # the one that leads the drag (the title bar, or the slots when bags only)
            # is kept on screen with the other in tow (the host's keeper)
            if attached():
                pass                                # the grid follows Paperdoll (above), not the bar
            elif bare:
                safe(lambda: Kit.attach(bar, grid))
            else:
                safe(lambda: Kit.attach(grid, bar))
            anchors_apply(followers)                # anchored windows: on to the new edges

            st.slot_raws = tuple(slot_raws)
            if SR["counts"]:
                show_counts()                       # a search still lit: its counts on the new slots
            st.grid_raw = raw_of(grid) if R.ok else None
            st.bar_raw = raw_of(bar) if R.ok else None
            if R.ok and not H.disabled and (st.grid_raw is None or st.bar_raw is None):
                # the draw hook can't follow windows it can't reach: basic pinning
                # instead, from the next pass (see _tick), and said once
                H.error = "can't reach the client's own window controls"
                H.disabled = True

        def no_right_click_close(g):
            safe(lambda: setattr(g, "CanCloseWithRightClick", False))

        CLOSE_TIP = ("Close " + TITLE + " (turns it off and gives every bag back; "
                     "the Modules tab turns it back on)")
        SLOTS_TIP = "Open the bag manager window: put a bag in each slot"
        TRAPS_TIP = "Open the trap bags window: tick the bags Trap and Untrap cast on"

        def make_bar(total_w, hide, free=False):
            """The stone title bar: drag it to move everything, double-click it to
            fold the window (and hide its bags) or unfold it. (2.6.78) The title is
            BAGS with the slot count as a grey label after it (ui-text 2.1)."""
            bar_w = max(total_w, BAR_MIN_W)
            bar = G.CreateGump(True, True)
            if free:
                Kit.place(bar, st.frame_x, st.frame_y, bar_w, BAR_H)   # 2.6.81 (IN1-8): window rule 1
            else:
                bar.SetRect(st.frame_x, st.frame_y, bar_w, BAR_H)      # Paperdoll's / the layout's
            Kit.add_window_frame(bar, bar_w, BAR_H, corners=False)
            Kit.add_section(bar, 8, 8, bar_w - 16, BAR_H - 16)
            Kit.add_label(bar, TITLE.upper(), 18, 14, Kit.HUE_TITLE)
            Kit.add_label(bar, str(st.slots), 18 + Kit.text_w(TITLE.upper()) + 8, 14, Kit.HUE_INFO)
            store = ui["store"]
            x = bar_w - 12 - 30
            if Kit.zone_up(KEY):                  # (2.6.85) a window in a zone is always up
                x += 20
            else:
                Kit.art_button(bar, store, "close", Kit.ART_CLOSE, x, 11, None, CLOSE_TIP,
                               on_click=act(HOST.disable, KEY))
                x -= 20
                Kit.art_button(bar, store, "min", Kit.ART_RESTORE if st.collapsed else Kit.ART_MIN, x, 14,
                               None, "Restore" if st.collapsed
                               else "Minimize (double-click the title does too)",
                               on_click=act(user_collapse))
                Kit.dock_button(bar, store, x, 14, on_click=act(fold_to_bar))
                x -= Kit.DOCK_DX
            for key, text, tip, fn in (
                    ("settings", "Settings", "Open the " + TITLE + " settings page",
                     act(HOST.show_settings, KEY)),
                    ("traps", "Trap bags", TRAPS_TIP, act(open_traps)),
                    ("bags", "Slots", SLOTS_TIP, act(open_manager))):
                x -= 10 + 35 + Kit.text_w(text)
                Kit.art_button(bar, store, key, Kit.ART_PAGE, x, 11, text, tip, on_click=fn)
            Kit.title_catcher(bar, 8, 8, max(20, x - 14), BAR_H - 16, act(user_collapse), key=KEY)
            no_right_click_close(bar)
            if hide:                       # folded into the Action Bar / bags only / Paperdoll
                safe(lambda: setattr(bar, "IsVisible", False))
            G.AddGump(bar)
            ui["bar"] = bar
            return bar

        def build_canvas_frame(followers):
            """(2.6.78) The grid gump in canvas mode: combined, the canvas fills the
            Paperdoll's hole beside the side panel (or the flap); alone, the grid is
            the zone's one window, exactly its slot: the stone frame, the title row
            (Kit.title_bar: Slots and Trap bags left of Settings, captions dropped
            when the row is tight), the canvas and the side panel. The canvas
            control is kept (re-parented); its contents are rebuilt only when the
            split or its size changes (canvas_sync)."""
            mode = st.canvas
            alone = mode == "alone"
            st.icons_used = H.icons or DEFAULT_ICONS
            ui["store"] = ({}, {})
            ui["side_status"] = None
            ui["search_box"] = None
            x0, y0, cw, ch, side = canvas_room(mode)
            if alone:
                W, H_ = fitov["told"]
            else:
                W, H_ = fitov["area"]
            grid = G.CreateGump(alone, alone)
            ui["grid_bare"] = alone                 # the grid leads (Bags alone: the window)
            raw = raw_of(grid)
            st.grid_info = (raw, alone)
            store = ui["store"]
            titled = alone and not st.bare and title_fits(W)
            if alone:
                Kit.add_window_frame(grid, W, H_)
                if titled:
                    Kit.title_bar(grid, store, W, TITLE, KEY, act(user_collapse), act(fold_to_bar),
                                  act(HOST.show_settings, KEY), close_tip=CLOSE_TIP,
                                  extra=[("traps", Kit.ART_PAGE, "Trap bags", TRAPS_TIP,
                                          act(open_traps)),
                                         ("bags", Kit.ART_PAGE, "Slots", SLOTS_TIP,
                                          act(open_manager))],
                                  after=str(st.slots))
                    b = store[0].get("close")
                    if b is not None:
                        Kit.on_click(b, act(HOST.disable, KEY))
            Kit.flush()                              # the frame and title land first: the canvas
            index = raw.Children.Count               # goes over them, under the panel and gem
            canvas_place(raw, index, x0, y0, cw, ch)
            tw, th = bare_btn_size()
            if alone:
                st.side_pw = 0
                if st.bare and title_fits(W):        # bags only: the gem in the canvas's corner
                    add_bare_button(grid, x0 + cw - tw - 2, y0 + ch - th - 2)
                elif titled and side:
                    pw, ph = build_side_panel(grid, x0 + cw, ch, y0)
                    st.side_pw = pw
                else:                                # (2.6.85) no panel: its four actions stay
                    add_quick_strip(grid, x0 + cw - 2, y0 + ch - QUICK_ICON - 2)
            elif side_off():
                add_bare_button(grid, W - tw - 2, H_ - th - 2)
                st.side_pw = 0
            else:
                pw, ph = build_side_panel(grid, cw, H_)
                st.side_pw = pw
            grid.SetRect(st.frame_x, st.frame_y, W, H_)
            st.grid_wh = (W, H_)
            if R.ok and not H.disabled and not st.drive_fixed:
                try:
                    add_hook(grid)
                except Exception as e:
                    st.driving = st.drive_fixed = True
                    H.error = "draw hook: %s" % e
            no_right_click_close(grid)
            if not alone:
                try:
                    enum_type = type(grid.LayerOrder)
                    grid.LayerOrder = getattr(enum_type, "Under")
                except Exception:
                    pass
            elif safe(lambda: HOST.layout_locked(KEY), False):
                safe(lambda: setattr(grid, "CanMove", False))      # held in its zone
            G.AddGump(grid)
            ui["grid"] = grid
            if alone:
                safe(lambda: Kit.note_scene(grid, x0, y0, cw, ch))  # items overlap on purpose
            bar = make_bar(W, True)                  # (hidden: nothing reads it as the window)
            if attached():
                st.attach_g = st.attach.get("g")
                safe(lambda: Kit.attach(grid, st.attach_g))
            anchors_apply(followers)
            st.slot_raws = ()
            st.grid_raw = raw
            st.bar_raw = raw_of(bar) if R.ok else None
            if st.grid_raw is None:
                H.error = "can't reach the client's own window controls"
                H.disabled = True
                return
            canvas_sync()

        def toggle_collapsed():
            st.collapsed = not st.collapsed
            st.docked = False
            st.dirty_frame = True
            schedule_save()

        def dock_wish():
            """Folded into the Action Bar by the player's choice (kept per character)."""
            return bool(safe(lambda: HOST.dock_wanted(DOCK_KEY), False))

        def set_dock_wish(on):
            safe(lambda: HOST.dock_want_set(DOCK_KEY, on))

        def bar_alive():
            return bool(safe(HOST.bar_alive, False))

        def user_collapse():
            """Minimize / Restore (and the title double-click): the title bar, never
            the Action Bar (the gold arrow is for that)."""
            if Kit.zone_up(KEY):                  # (2.6.85) a window in a zone is always up
                return
            set_dock_wish(False)
            toggle_collapsed()

        def fold_to_bar():
            """The gold arrow / the bar's bag slots: folded into the Action Bar, or
            (no bar up) folded to the title bar until the bar comes."""
            set_dock_wish(True)
            alive = bar_alive()
            if not st.collapsed or st.docked != alive:
                st.collapsed, st.docked = True, alive
                st.dirty_frame = True
                schedule_save()
            if not alive:
                HOST.dock_note(TITLE)

        def toggle_bare():
            if attached():                   # the combined window: only the side panel
                st.side_hidden = not st.side_hidden
            else:
                st.bare = not st.bare
            st.dirty_frame = True
            schedule_save()

        _link = {"next": 0.0}

        def link_tick():
            """Commands from the Action Bar, and this window's state for it
            (shared variables, read every 0.1 s)."""
            now = time.time()
            if now < _link["next"]:
                return
            _link["next"] = now + 0.1
            try:                                      # (shared vars don't touch the client)
                cmd = API.GetSharedVar(LINK_CMD)
            except Exception:
                cmd = None
            if cmd:
                try:
                    API.RemoveSharedVar(LINK_CMD)
                except Exception:
                    pass
                cmd = str(cmd)
                if attached():                        # Paperdoll's window stands for ours
                    fn = st.attach.get("cmd")
                    if fn is not None:
                        safe(lambda: fn(cmd))
                elif cmd == "show" and (st.collapsed or st.docked):
                    set_dock_wish(False)
                    st.collapsed = st.docked = False
                    st.dirty_frame = True
                    schedule_save()
                elif cmd == "dock" and not st.docked:
                    fold_to_bar()
            if attached():
                state = str(st.attach.get("state") or "open")
                if state != st.link_state:
                    st.link_state = state
                    safe(lambda: API.SetSharedVar(LINK_STATE, state))
                return
            if st.docked:
                if not bar_alive():
                    st.docked = False                 # bar gone: show the folded title strip
                    st.dirty_frame = True             # (the wish is kept: back in when it returns)
            elif st.collapsed and now >= _link.get("wish", 0.0):
                _link["wish"] = now + 0.25
                if dock_wish() and bar_alive():       # folded in by choice: back into the bar
                    st.docked = True
                    st.dirty_frame = True
            elif not st.collapsed and now >= _link.get("wish", 0.0):
                _link["wish"] = now + 1.0
                if dock_wish():
                    set_dock_wish(False)              # shown again: no longer folded
            state = "docked" if st.docked else ("collapsed" if st.collapsed else "open")
            if state != st.link_state:
                st.link_state = state
                safe(lambda: API.SetSharedVar(LINK_STATE, state))

        def set_min(value):
            if not R.ok:
                API.SysMsg(TITLE + ": minimizing bags needs client access (%s)." % R.error, HUE_ERR)
                return
            n = set_minimized_all(value) or 0
            API.SysMsg(TITLE + ": %s %d bag%s." % ("minimized" if value else "restored", n,
                                                   "" if n == 1 else "s"), HUE_INFO)

        # ----------------------- fallback pinning (no client access) ------------------
        def fallback_tick():
            """Basic pinning without client access: every tick, so plain try/except
            (no closures) round each bag."""
            track_wrapper_frame()
            grew = False
            hidden = st.collapsed or (attached() and not st.attach.get("shown", True))
            for idx, serial in st.layout:
                try:
                    it = API.FindItem(serial)
                    g = it.GetContainerGump() if it else None
                    if not Kit.is_open(g):
                        continue
                    try:
                        g.IsVisible = not hidden
                    except Exception:
                        pass
                    if hidden:
                        continue
                    cx, cy = cell_xy(idx)
                    if g.GetX() != cx or g.GetY() != cy:
                        g.SetPos(cx, cy)
                    w = g.GetWidth() or 0
                    h = g.GetHeight() or 0
                except Exception:
                    continue                        # one odd bag must not stop the others
                if st.cell_w < w <= MAX_CELL:
                    st.cell_w, grew = w, True
                if st.cell_h < h <= MAX_CELL:
                    st.cell_h, grew = h, True
            if grew:
                st.dirty_frame = True
                schedule_save()

        def follow_lead():
            """(2.6.66) The grid attached to Paperdoll's window of the moment: a
            rebuilt Paperdoll window is a new gump, and a grid left attached to
            the old one would be a free window the layout places on its own."""
            lead = st.attach.get("g") if attached() else None
            if lead is not None and lead is not st.attach_g and Kit.is_open(lead) \
                    and Kit.is_open(ui.get("grid")):
                st.attach_g = lead
                safe(lambda: Kit.attach(ui["grid"], lead))

        def track_wrapper_frame():
            if attached():                            # Paperdoll's window leads
                lead, att = st.attach.get("g"), st.attach
                if not Kit.is_open(lead):
                    return
                follow_lead()
                x = safe(lambda: lead.GetX(), st.frame_x - att.get("dx", 0)) + att.get("dx", 0)
                y = safe(lambda: lead.GetY(), st.frame_y - att.get("dy", 0)) + att.get("dy", 0)
                grid = ui.get("grid")
                if (x, y) != (st.frame_x, st.frame_y):
                    st.frame_x, st.frame_y = x, y
                    if Kit.is_open(grid):
                        safe(lambda: grid.SetPos(x, y))               # tracked to the hole: not a drag
                        safe(lambda: Kit.moved_by_code(grid))
                elif Kit.is_open(grid):
                    # (2.6.66) moved by something else (the keeper, a layout pass
                    # before it was attached): back to the hole
                    try:
                        if (int(grid.GetX()), int(grid.GetY())) != (x, y):
                            grid.SetPos(x, y)
                            Kit.moved_by_code(grid)
                    except Exception:
                        pass
                return
            # bags only: follow the dragged slots; otherwise the title bar
            if ui.get("grid_bare"):
                lead, other, dy = ui["grid"], ui["bar"], 0
            else:
                lead, other, dy = ui["bar"], ui["grid"], BAR_H
            if not Kit.is_open(lead):
                return
            x = safe(lambda: lead.GetX(), st.frame_x)
            y = safe(lambda: lead.GetY(), st.frame_y)
            if x != st.frame_x or y != st.frame_y:
                st.frame_x, st.frame_y = x, y
                if Kit.is_open(other):
                    safe(lambda: other.SetPos(x, y + dy))        # moved along by code, not dragged
                    safe(lambda: Kit.moved_by_code(other))

        # ------------------------------ bag manager ----------------------------------
        def open_manager():
            st.open_mgr = True
            st.dirty_mgr = True
            schedule_save()

        def close_manager():
            remember_window_pos()
            dispose("mgr")
            st.open_mgr = False
            schedule_save()

        def toggle_mgr_min():
            st.mgr_min = not st.mgr_min
            st.dirty_mgr = True
            schedule_save()

        def sub_window_moved():
            """The Bag Manager or Traps window was dragged and let go: save."""
            remember_window_pos()
            schedule_save()

        def build_manager():
            remember_window_pos()
            dispose("mgr")
            M, GAP = Kit.MARGIN, Kit.GAP
            w, row_h, h_act = 480, 28, 40
            list_h = min(st.slots * row_h + 8, 430)
            h = M + 30 + M if st.mgr_min else M + 30 + GAP + h_act + GAP + list_h + M
            g, store, y = framed_window("bag_mgr", st.mgr_x, st.mgr_y, w, h, "BAG MANAGER",
                                        st.mgr_min, act(toggle_mgr_min), act(close_manager))
            if not st.mgr_min:
                IW = w - 2 * M
                Kit.add_section(g, M, y, IW, h_act)
                Kit.art_button(g, store, "fill", Kit.ART_OK, M + 12, y + 9, "Auto-fill",
                               "Put every open bag that has no slot into an empty slot",
                               on_click=act(auto_fill))
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, M + 200, y + 9, "Clear all",
                               "Take the bag out of every slot", on_click=act(clear_all))
                y += h_act + GAP
                Kit.add_section(g, M, y, IW, list_h)
                sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                inner_w = IW - 8 - 20
                for idx in range(st.slots):
                    ry = idx * row_h
                    Kit.add_label(sa, "#%d" % (idx + 1), 6, ry + 5, Kit.HUE_TITLE)
                    if idx in st.assign:
                        Kit.add_label(sa, short(bag_name(st.assign[idx]), 28), 44, ry + 5)
                    else:
                        Kit.add_label(sa, "No bag yet: click Set...", 44, ry + 5, Kit.HUE_INFO)
                    Kit.art_button(sa, store, "set%d" % idx, Kit.ART_PLAY, inner_w - 165, ry + 3,
                                   "Set...", "Target a bag for slot #%d" % (idx + 1),
                                   on_click=act(assign_slot, idx))
                    Kit.art_button(sa, store, "clr%d" % idx, Kit.ART_CLOSE, inner_w - 80, ry + 3, "Clear",
                                   "Take the bag out of slot #%d" % (idx + 1),
                                   on_click=act(clear_slot, idx))
                g.Add(sa)
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, sub_window_moved))
            ui["mgr"] = g

        def changed_bags():
            forget_names()               # the slots' bag names are read again
            st.dirty_frame = True
            st.dirty_mgr = True
            st.dirty_trp = True
            st.dirty_srt = True
            publish_layout()
            save()

        def pick_then(fn, *args):
            """A target cursor that doesn't hold anything up: fn(*args, serial) runs on
            the module's next pass once the player targets (serial 0: cancelled /
            timed out)."""
            def done(serial):
                st.actions.append((fn, args + (int(serial or 0),)))
            HOST.pick_target(15, done)

        def assign_slot(idx):
            API.SysMsg(TITLE + ": target a bag for slot #%d." % (idx + 1), HUE_INFO)
            pick_then(assign_slot_to, idx)

        def assign_slot_to(idx, target):
            if not target:
                API.SysMsg(TITLE + ": cancelled.", HUE_INFO)
                return
            it = get_item(target)
            if not it or not safe(lambda: it.IsContainer, False):
                API.SysMsg(TITLE + ": that isn't a container.", HUE_ERR)
                return
            serial = int(target)
            for k in [k for k, v in st.assign.items() if v == serial]:
                del st.assign[k]
            st.assign[idx] = serial
            changed_bags()
            if bag_is_open(serial):
                API.SysMsg(TITLE + ": slot #%d set." % (idx + 1), HUE_OK)
            else:
                API.SysMsg(TITLE + ": slot #%d set. Open the bag and it will snap in." % (idx + 1), HUE_OK)

        def clear_slot(idx):
            if idx in st.assign:
                del st.assign[idx]
                changed_bags()

        def clear_all():
            st.assign = {}
            changed_bags()
            API.SysMsg(TITLE + ": all slots cleared.", HUE_INFO)

        def auto_fill():
            candidates = []
            pack = safe(lambda: int(API.Backpack), 0)
            if pack:
                candidates.append(pack)
            for it in safe(lambda: API.ItemsInContainer(API.Backpack, True), []) or []:
                if safe(lambda: it.IsContainer, False):
                    candidates.append(int(it.Serial))
            bank = safe(lambda: int(API.Bank), 0)
            if bank:
                candidates.append(bank)
                for it in safe(lambda: API.ItemsInContainer(bank, True), []) or []:
                    if safe(lambda: it.IsContainer, False):
                        candidates.append(int(it.Serial))
            used = set(st.assign.values())
            free = [i for i in range(st.slots) if i not in st.assign]
            added = 0
            for serial in candidates:
                if not free:
                    break
                if serial in used or not bag_is_open(serial):
                    continue
                st.assign[free.pop(0)] = serial
                used.add(serial)
                added += 1
            changed_bags()
            if added:
                API.SysMsg(TITLE + ": added %d open bag%s." % (added, "" if added == 1 else "s"), HUE_OK)
            elif not free:
                API.SysMsg(TITLE + ": no empty slots left.", HUE_ERR)
            else:
                API.SysMsg(TITLE + ": no open bag without a slot found.", HUE_INFO)

        # --------------------- settings (Virtue Assistant window) --------------------
        H_LAYOUT, H_LOOK, H_STATUS, H_DEBUG = 182, 116, 86, 60   # (2.6.52: the Sort debug box
        #                                                            moved from STATUS to DEBUG)
        page = {"fields": None, "checks": None, "slider": None, "pct": None, "status": None,
                "size": None, "store": ({}, {}), "next_status": 0.0}

        def size_line():
            if st.canvas is not None:                # (2.6.78)
                return "In a zone the bags share the zone. Items always draw fully solid."
            return "Slots fit the open bags (%d x %d px). Items always draw fully solid." % (
                st.cell_w, st.cell_h)

        def config_height(w):
            return H_LAYOUT + Kit.GAP + H_LOOK + Kit.GAP + H_STATUS + Kit.GAP + H_DEBUG

        def build_config(g, x, y, w):
            if R.ok and shrink["pct"] is None:       # (2.6.67) shrunk: yours is kept aside
                got = safe(read_scale)
                if got:
                    st.scale_pct, st.scale_items = got
            store = ({}, {})
            Kit.add_section(g, x, y, w, H_LAYOUT, "LAYOUT  (click Apply to use it)")
            fields = {}
            for i, (key, caption, unit, value, tip) in enumerate((
                    ("slots", "Slots:", "", st.slots,
                     "Bag slots the window has (%d-%d)" % (MIN_SLOTS, MAX_SLOTS)),
                    ("cols", "Columns:", "", st.cols,
                     "Slots per row, not in a zone (0-%d, 0 = a near-square layout)" % MAX_SLOTS),
                    ("rows", "Rows:", "", st.rows,
                     "Rows of slots, not in a zone (0-%d, 0 = a near-square layout)" % MAX_SLOTS),
                    ("scale", "Bag scale:", "%", st.scale_pct,
                     "The client's own Container Scale option, for every container window "
                     "(50-200)"))):
                ry = y + 32 + i * 28
                Kit.add_label(g, caption, x + 12, ry + 2)
                fields[key] = Kit.add_textbox(g, str(value), x + w - 100, ry, 60)
                safe(lambda: fields[key].SetTooltip(tip))
                if unit:
                    Kit.add_label(g, unit, x + w - 34, ry + 2, Kit.HUE_INFO)
            Kit.art_button(g, store, "apply", Kit.ART_OK, x + 12, y + 148, "Apply",
                           "Use the slots, columns, rows and bag scale above")

            yo = y + H_LAYOUT + Kit.GAP
            pct = int(round(st.opacity * 100))
            Kit.add_section(g, x, yo, w, H_LOOK, "LOOK")
            Kit.add_label(g, "Bag opacity:", x + 12, yo + 34)
            slider = Kit.add_slider(g, x + 180, yo + 38, 200, 10, 100, pct)
            safe(lambda: slider.SetTooltip("How solid the bag panels and bag art are (10-100%); "
                                           "the items in them always draw fully solid"))
            pct_label = Kit.add_label(g, "%d%%" % pct, x + 400, yo + 34, Kit.HUE_INFO)
            checks = {"trim": Kit.add_check(g, "Trim bags to their item area", x + 12, yo + 62, st.trim,
                                            "Hide each bag's art and butt the item areas edge to "
                                            "edge (needs client access; in a zone the bags always "
                                            "fill it)"),
                      "items": Kit.add_check(g, "Scale items with the bags", x + 12, yo + 88,
                                             st.scale_items,
                                             "The client's option to draw items at the bag scale too")}

            ys = yo + H_LOOK + Kit.GAP
            Kit.add_section(g, x, ys, w, H_STATUS, "STATUS")
            status = Kit.add_label(g, short(status_line(), 64), x + 12, ys + 32, Kit.HUE_INFO)
            size = Kit.add_label(g, size_line(), x + 12, ys + 56, Kit.HUE_INFO)

            yd = ys + H_STATUS + Kit.GAP
            Kit.add_section(g, x, yd, w, H_DEBUG, "DEBUG  (for checking the shard's texts)")
            Kit.art_button(g, store, "diag", Kit.ART_PAGE, x + w - 140, yd + 4, "Diagnose",
                           "Print what " + TITLE + " sees in the journal (for a bug report)")
            checks["say"] = Kit.add_check(g, "Print the shard's replies to Sort in the journal",
                                          x + 12, yd + 30, st.sort_say,
                                          "Every journal line Sort sees and what became of each move, "
                                          "to check the texts it listens for (a full bag, \"you must "
                                          "wait\")")
            page.update({"fields": fields, "checks": checks, "slider": slider, "pct": pct_label,
                         "status": status, "size": size, "store": store, "next_status": 0.0,
                         "seen": {"trim": st.trim, "items": st.scale_items, "say": st.sort_say}})

        def config_closed():
            page.update({"fields": None, "checks": None, "slider": None, "pct": None,
                         "status": None, "size": None})

        def poll_config():
            """Live settings: checkboxes and opacity take effect without pressing Apply."""
            if page["fields"] is None:
                return
            if Kit.was_clicked(page["store"], "apply"):
                apply_config()
                return
            if Kit.was_clicked(page["store"], "diag"):
                diagnose()
            checks = page["checks"]
            for key, apply in (("trim", set_trim), ("items", set_scale_items), ("say", set_sort_say)):
                try:                                  # (2.6.82: no lambda per check)
                    ticked = bool(checks[key].IsChecked)
                except Exception:
                    ticked = None
                if ticked is not None and ticked != page["seen"][key]:   # you clicked it
                    page["seen"][key] = ticked
                    apply(ticked)
            try:
                v = int(page["slider"].Value)
            except Exception:
                v = None
            if v is not None and 10 <= v <= 100:
                if page.get("pct_v") != (v, page["pct"]):    # (2.6.82) formatted on a change
                    page["pct_v"] = (v, page["pct"])
                    Kit.set_text(page["pct"], "%d%%" % v)
                value = v / 100.0
                if abs(value - st.opacity) > 0.001:
                    # wait until the slider stops so the slots aren't redrawn at every step
                    pend = st.opacity_pending
                    if pend and pend[0] == value:
                        st.opacity_pending = (value, pend[1] + 1)
                    else:
                        st.opacity_pending = (value, 0)
                    if st.opacity_pending[1] >= OPACITY_SETTLE_POLLS:
                        st.opacity = value
                        st.opacity_pending = None
                        st.dirty_frame = True
                        safe(canvas_alpha)        # (2.6.78) the canvas in place, at once
                        schedule_save()
                else:
                    st.opacity_pending = None
            now = time.time()
            if now >= page["next_status"]:
                page["next_status"] = now + 1.0
                Kit.set_text(page["status"], short(status_line(), 64))
                Kit.set_text(page["size"], size_line())

        def status_line():
            if not R.tried:
                return "Off: tick " + TITLE + " on the Modules tab"
            if not R.ok:
                return "No client access: " + R.error
            if H.disabled:
                return "Trimming stopped after errors: " + H.error
            if st.canvas is not None:                # (2.6.78)
                tail = "%d open, filling the zone" % H.open_count
            else:
                tail = "%d open, %d trimmed" % (H.open_count, len(H.trimmed))
            if st.driving:
                return "Running (script-driven): " + tail
            if H.hook_calls == 0:
                return "Starting"
            return "Running: " + tail

        def diagnose():
            lines = [
                "client access: " + ("OK" if R.ok else "failed (" + R.error + ")"),
                "draw hook calls: %d (%s), script-driven: %s, disabled: %s"
                % (H.hook_calls, "before drawing" if H.pre_calls else "while drawing", st.driving,
                   H.disabled),
                "assigned %d, open %d, trimmed %d, trim %s, drop catchers %d"
                % (len(st.layout), H.open_count, len(H.trimmed), st.trim, len(H.catchers)),
                "opacity %d%%, slot %d x %d, scale %d%%, container scale seen %.2f"
                % (int(round(st.opacity * 100)), st.cell_w, st.cell_h, st.scale_pct, H.scale),
                "last error: " + (H.error or "none"),
            ]
            if st.canvas is not None and CANVAS["size"] is not None:      # (2.6.78)
                lines.append("canvas %d x %d, regions %d (%s), items %d, pins %d, layout %d"
                             % (CANVAS["size"][0], CANVAS["size"][1], len(CANVAS["regions"]),
                                CANVAS["orient"], len(CV["pool"]), len(PIN), CANVAS["ver"]))
            if R.ok:
                missing = [s for _, s in st.layout if s not in H.gumps]
                if missing:
                    lines.append("not open (or a grid container): " + ", ".join("0x%08X" % s for s in missing))
            for line in lines:
                API.SysMsg(TITLE + ": " + line + ".", HUE_INFO)

        def set_trim(value):
            f = page["checks"]
            if value and not (R.ok and not H.disabled):
                API.SysMsg(TITLE + ": trimming isn't available (%s)." % status_line(), HUE_ERR)
                if f:
                    safe(lambda: f["trim"].SetIsChecked(False))
                    page["seen"]["trim"] = False
                value = False
            if value == st.trim:
                return
            st.trim = value
            refit_cells()
            save()
            API.SysMsg(TITLE + ": trim " + ("on." if value else "off."), HUE_INFO)

        def set_sort_say(value):
            if value != st.sort_say:
                st.sort_say = value
                schedule_save()

        def set_scale_items(value):
            if value == st.scale_items:
                return
            if not R.ok:
                API.SysMsg(TITLE + ": scaling items needs client access (%s)." % R.error, HUE_ERR)
                return
            try:
                old = st.scale_items
                st.scale_items = value
                try:
                    apply_scale(*scale_now())         # (2.6.67) still shrunk when it is
                except Exception:
                    st.scale_items = old
                    raise
                if shrink["pct"] is not None:
                    note_shrunk()
                refit_cells()
                API.SysMsg(TITLE + ": items %s with the bags." % ("scale" if value else "don't scale"),
                           HUE_INFO)
            except Exception as e:
                API.SysMsg(TITLE + ": couldn't change the item scaling (%s)." % e, HUE_ERR)

        def read_int(field, name, lo, hi):
            raw = (safe(lambda: field.Text, "") or "").strip()
            if not raw.isdigit() or not (lo <= int(raw) <= hi):
                raise ValueError("%s must be a whole number from %d to %d." % (name, lo, hi))
            return int(raw)

        def apply_config():
            f = page["fields"]
            if not f:
                return
            try:
                slots = read_int(f["slots"], "Slots", MIN_SLOTS, MAX_SLOTS)
                cols = read_int(f["cols"], "Columns", 0, MAX_SLOTS)
                rows = read_int(f["rows"], "Rows", 0, MAX_SLOTS)
                scale = read_int(f["scale"], "Bag scale", 50, 200)
            except ValueError as e:
                API.SysMsg(TITLE + ": " + str(e), HUE_ERR)
                return
            if cols > 0 and rows > 0 and cols * rows < slots:
                API.SysMsg(TITLE + ": %d columns x %d rows only fits %d slots, not %d."
                           % (cols, rows, cols * rows, slots), HUE_ERR)
                return
            dropped = [k for k in st.assign if k >= slots]
            for k in dropped:
                del st.assign[k]
            sync_rules()
            for k in [k for k in st.rules if k >= slots]:     # rules of removed slots go too
                del st.rules[k]
            st.slots, st.cols, st.rows = slots, cols, rows
            if R.ok and scale != st.scale_pct:
                try:
                    old = st.scale_pct
                    st.scale_pct = scale
                    try:
                        apply_scale(*scale_now())     # (2.6.67) still shrunk when it is
                    except Exception:
                        st.scale_pct = old
                        raise
                    if shrink["pct"] is not None:
                        if shrink["pct"] >= scale:    # yours is no bigger: nothing to shrink
                            shrink["pct"] = shrink["said"] = None
                        note_shrunk()
                    refit_cells()
                except Exception as e:
                    API.SysMsg(TITLE + ": couldn't change the bag scale (%s)." % e, HUE_ERR)
            changed_bags()
            c, r = layout_dims()
            msg = TITLE + ": %d slot%s in %d x %d." % (slots, "" if slots == 1 else "s", c, r)
            if dropped:
                msg += " Released %d bag%s from removed slots." % (len(dropped),
                                                                   "" if len(dropped) == 1 else "s")
            API.SysMsg(msg, HUE_OK)
            config_closed()
            HOST.refresh_settings(KEY)

        # --------------------------------- traps -------------------------------------
        def open_traps():
            st.open_trp = True
            st.dirty_trp = True
            schedule_save()

        def close_traps():
            sync_trap_sel()
            remember_window_pos()
            dispose("trp")
            ui["trap_checks"] = []
            st.open_trp = False
            schedule_save()

        def toggle_trp_min():
            sync_trap_sel()
            st.trp_min = not st.trp_min
            st.dirty_trp = True
            schedule_save()

        def trap_candidates():
            out = []
            for s in [st.assign[i] for i in sorted(st.assign)] + st.trap_extra:
                if s not in out:
                    out.append(s)
            return out

        def sync_trap_sel():
            checks = ui["trap_checks"]
            if not checks or not Kit.is_open(ui["trp"]):
                return
            for serial, chk in checks:
                if safe(lambda: chk.IsChecked, False):
                    st.trap_sel.add(serial)
                else:
                    st.trap_sel.discard(serial)

        def build_traps():
            sync_trap_sel()
            remember_window_pos()
            dispose("trp")
            bags = trap_candidates()
            M, GAP = Kit.MARGIN, Kit.GAP
            w, row_h, h_act, h_foot = 480, 28, 40, 52
            list_h = min(max(1, len(bags)) * row_h + 8, 400)
            h = (M + 30 + M if st.trp_min
                 else M + 30 + GAP + h_act + GAP + list_h + GAP + h_foot + M)
            g, store, y = framed_window("bag_trp", st.trp_x, st.trp_y, w, h, "TRAP BAGS",
                                        st.trp_min, act(toggle_trp_min), act(close_traps))
            checks = []
            if not st.trp_min:
                IW = w - 2 * M
                Kit.add_section(g, M, y, IW, h_act)
                bx = M + 12
                for key, art, cap, tip, fn in (
                        ("all", Kit.ART_OK, "Tick all", "Tick every bag on the list",
                         act(select_all_traps, True)),
                        ("none", Kit.ART_CLOSE, "Untick all", "Untick every bag on the list",
                         act(select_all_traps, False)),
                        ("add", Kit.ART_PLAY, "Add bag...", "Target a bag that has no slot to put it "
                         "on the list", act(add_trap_bag))):
                    Kit.art_button(g, store, key, art, bx, y + 9, cap, tip, on_click=fn)
                    bx += 35 + Kit.text_w(cap) + 16
                y += h_act + GAP
                Kit.add_section(g, M, y, IW, list_h)
                sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                inner_w = IW - 8 - 20
                if not bags:
                    Kit.add_label(sa, "No bags yet. Put bags in the slots, or click Add bag... and "
                                  "target one.", 6, 6, Kit.HUE_INFO)
                for i, serial in enumerate(bags):
                    ry = i * row_h
                    chk = Kit.add_check(sa, short(bag_name(serial), 32), 6, ry + 4, serial in st.trap_sel,
                                        "Trap and Untrap cast on this bag when it is ticked")
                    checks.append((serial, chk))
                    if serial in st.trap_extra and serial not in st.assign.values():
                        Kit.art_button(sa, store, "rm%d" % i, Kit.ART_CLOSE, inner_w - 110, ry + 3,
                                       "Remove", "Take this bag off the list",
                                       on_click=act(remove_trap_bag, serial))
                g.Add(sa)
                y += list_h + GAP
                Kit.add_section(g, M, y, IW, h_foot)
                Kit.add_label(g, "Tick the bags, then click Trap or Untrap on the side panel.",
                              M + 12, y + 8, Kit.HUE_INFO)
                Kit.add_label(g, "A trapped bag explodes on whoever opens it, you included.",
                              M + 12, y + 28, Kit.HUE_BAD)
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, sub_window_moved))
            ui["trp"] = g
            ui["trap_checks"] = checks

        def traps_changed():
            ui["trap_checks"] = []
            st.dirty_trp = True
            save()

        def select_all_traps(value):
            st.trap_sel = set(trap_candidates()) if value else set()
            traps_changed()

        def add_trap_bag():
            sync_trap_sel()
            API.SysMsg(TITLE + ": target a bag to add to the trap list.", HUE_INFO)
            pick_then(add_trap_bag_to)

        def add_trap_bag_to(target):
            if not target:
                return
            sync_trap_sel()                 # ticks changed while the cursor was up
            it = get_item(target)
            if not it or not safe(lambda: it.IsContainer, False):
                API.SysMsg(TITLE + ": that isn't a container.", HUE_ERR)
                return
            serial = int(target)
            if serial not in st.trap_extra:
                st.trap_extra.append(serial)
            st.trap_sel.add(serial)
            traps_changed()

        def remove_trap_bag(serial):
            sync_trap_sel()
            if serial in st.trap_extra:
                st.trap_extra.remove(serial)
            st.trap_sel.discard(serial)
            traps_changed()

        def start_job(spell):
            sync_trap_sel()
            save()
            if st.job:
                API.SysMsg(TITLE + ": already casting %s; press Stop first." % st.job["spell"], HUE_ERR)
                return
            if st.sort:
                API.SysMsg(TITLE + ": busy sorting; press Stop first.", HUE_ERR)
                return
            targets = [s for s in trap_candidates() if s in st.trap_sel]
            if not targets:
                API.SysMsg(TITLE + ": tick the bags to cast on in the Trap bags window first.", HUE_ERR)
                open_traps()
                return
            st.job = {"spell": spell, "queue": targets, "i": 0, "phase": "mana", "t": 0.0,
                      "tries": 0, "done": 0, "failed": 0, "warned": False, "cast": 0.0}
            st.dirty_trp = True
            set_status("Starting")
            API.SysMsg(TITLE + ": casting %s on %d bag%s." % (spell, len(targets),
                                                             "" if len(targets) == 1 else "s"), HUE_INFO)

        def job_held(now):
            """Why the Trap / Untrap run may not cast now (a HOLD_TEXT key), else
            None. 2.6.81 (IN1-3): the mother's shared holds, so every loop agrees:
            HOST.fight_hold (dead, war mode, hurt, a hostile near, an item on the
            cursor, an alarm), then HOST.guard_hold (a guard zone, or one not known
            yet: the strict reading holds there too). The fight test runs first and
            on every look, so it keeps track of your HP."""
            try:
                return HOST.fight_hold(now) or HOST.guard_hold()
            except Exception:
                return None

        def stop_job(user=False):
            if st.job:
                # only the cursor our own cast raised (cast, not yet aimed) is cleared;
                # a cursor the player or another module has up is left alone. 2.6.81
                # (IN1-4): and only a neutral one once the spell can have been cast
                j0 = st.job
                if j0.get("phase") == "target" and time.time() - j0.get("cast", 0.0) >= TRAP_CAST_MIN \
                        and safe(lambda: HOST.cursor_ok(KEY, "neutral"), False):
                    safe(lambda: API.CancelTarget())
                safe(lambda: HOST.release_cursor(KEY))
                if user:
                    API.SysMsg(TITLE + ": %s stopped." % st.job["spell"], HUE_INFO)
                    set_status("Stopped")
            st.job = None
            st.dirty_trp = True

        def idle_text():
            """(2.6.72) The side panel's status line when nothing runs: empty, or the
            scale the bags are shown at to fit their zone."""
            p = shrink["pct"]
            return ("Shown at %d%% to fit" % p) if p is not None and p < st.scale_pct else ""

        def show_stop():
            """(2.6.72) Stop is shown only while a trap, untrap or sort run is going."""
            on = bool(st.job or st.sort)
            for ctrl in ui.get("stop_ctrls") or ():
                if ctrl is not None:
                    safe(lambda: setattr(ctrl, "IsVisible", on))

        def set_status(text):
            if text == "Idle":                       # (2.6.72) idle: empty, or the fit's scale
                text = idle_text()
            show_stop()
            if text == st.status_text:
                return
            st.status_text = text
            lab = ui.get("side_status")
            if lab is not None:
                Kit.set_text(lab, text)

        J_RESULTS = tuple((res, tuple(w.lower() for w in words))
                          for res, words in (("reagents", J_REAGENTS), ("mana", J_MANA),
                                             ("fizzle", J_FIZZLE), ("busy", J_BUSY)))

        def journal_result(j):
            """What the server said about the job's last cast. The shared journal
            (Journal, read once per pass for every module) hands over the lines that
            came in since the cast (a reader started at the cast); they are kept on
            the job, so every look sees all of them. Never cleared, never re-read
            from the client here (before: API.GetJournalEntries every tick while the
            cursor was awaited)."""
            rd = j.get("jr")
            if rd is None:
                return None
            texts = j["jt"]
            for ln in rd.new():
                if ln.text and not ln.text.startswith(TITLE):
                    texts.append(ln.low)
            if not texts:
                return None
            for res, words in J_RESULTS:
                for w in words:
                    for t in texts:
                        if w in t:
                            return res
            return None

        def job_next(j, success):
            if success:
                j["done"] += 1
            else:
                j["failed"] += 1
            j["i"] += 1
            j["tries"] = 0
            j["phase"] = "mana"

        def job_retry(j, now, reason):
            j["tries"] += 1
            if j["tries"] > TRAP_RETRIES:
                API.SysMsg(TITLE + ": giving up on %s (%s)." % (bag_name(j["queue"][j["i"]], False), reason), HUE_ERR)
                job_next(j, False)
            else:
                j["phase"] = "pause"
                j["t"] = now + TRAP_RETRY_PAUSE

        def job_step():
            j = st.job
            if not j:
                return
            now = time.time()
            if j["i"] >= len(j["queue"]):
                API.SysMsg(TITLE + ": %s finished: %d done, %d failed." % (j["spell"], j["done"], j["failed"]),
                           HUE_OK if not j["failed"] else HUE_ERR)
                set_status("Done %d/%d" % (j["done"], len(j["queue"])))
                stop_job()
                return
            serial = j["queue"][j["i"]]
            ph = j["phase"]

            if ph == "pause":
                if now >= j["t"]:
                    j["phase"] = "mana"
                return

            if ph == "mana":
                # (2.6.5) a run of casts is a skill loop under the shard's rules: it
                # waits in a guard zone, in any fight and on death. 2.6.81 (IN1-3): the
                # shared holds (taking damage, a hostile near, an item on the cursor, an
                # alarm, an unknown guard zone too)
                held = job_held(now)
                if held:
                    if j.get("held") != held:
                        j["held"] = held
                        text = HOLD_TEXT.get(held, held)
                        API.SysMsg(TITLE + ": %s waits (%s)." % (j["spell"], text[:1].lower() + text[1:]),
                                   HUE_INFO)
                        set_status(text if held == "unknown" else "Paused: " + text)
                    return
                if j.get("held"):
                    j["held"] = None
                    set_status("Starting")
                mana = safe(lambda: API.Player.Mana, 999)
                if mana < TRAP_MANA:
                    if not j["warned"]:
                        API.SysMsg(TITLE + ": waiting for mana (%d/%d)." % (mana, TRAP_MANA), HUE_INFO)
                        set_status("Need mana")
                        j["warned"] = True
                    return
                j["warned"] = False
                if not get_item(serial):
                    API.SysMsg(TITLE + ": bag 0x%08X is out of reach; skipping it." % serial, HUE_ERR)
                    job_next(j, False)
                    return
                # 2.6.81 (IN1-X1): another module has the cursor spoken for (its cursor
                # may not be up yet): never cast over its claim, which would take its
                # cursor. Status only: no journal line for every Action Bar press
                if others_cursor():
                    set_status("Cursor busy")
                    return
                if safe(lambda: API.HasTarget("any"), False):
                    # 2.6.81 (IN1-4): any cursor up waits, never cancelled: it may be the
                    # player's own (a late cursor of our last cast: Esc clears it, then
                    # the run goes on)
                    set_status("Cursor busy")
                    return
                API.SysMsg(TITLE + ": %s %d/%d: %s." % (j["spell"], j["i"] + 1, len(j["queue"]),
                                                          bag_name(serial, False)), HUE_INFO)
                set_status("%s %d/%d" % ("Untrap" if "Untrap" in j["spell"] else "Trap", j["i"] + 1, len(j["queue"])))
                j["cast"] = time.time()
                j["jr"], j["jt"] = Journal.reader(), []   # journal lines after this are the cast's
                HOST.claim_cursor(KEY, TRAP_TARGET_TIMEOUT + 0.5)   # the cursor that comes is ours
                API.CastSpell(j["spell"])
                j["phase"] = "target"
                j["t"] = now
                return

            if ph == "target":
                res = journal_result(j)
                if res:
                    HOST.release_cursor(KEY)   # no cursor coming for this cast
                if res == "reagents":
                    API.SysMsg(TITLE + ": out of reagents for %s." % j["spell"], HUE_ERR)
                    stop_job()
                    return
                if res == "mana":
                    j["phase"] = "mana"
                    return
                if res in ("fizzle", "busy"):
                    job_retry(j, now, res)
                    return
                # 2.6.81 (IN1-4): only a neutral cursor (the kind Magic Trap / Untrap
                # raises: never the player's harmful or beneficial spell), only once the
                # spell can have been cast, and only while nobody else has the cursor
                # spoken for (HOST.cursor_ok)
                if now - j["cast"] >= TRAP_CAST_MIN and HOST.cursor_ok(KEY, "neutral"):
                    API.Target(serial)
                    HOST.release_cursor(KEY)
                    j["phase"] = "recover"
                    j["t"] = now
                elif now - j["t"] > TRAP_TARGET_TIMEOUT:
                    HOST.release_cursor(KEY)
                    job_retry(j, now, "no target cursor")
                return

            if ph == "recover":
                if now - j["t"] < TRAP_RECOVERY:
                    return
                res = journal_result(j)
                if res == "reagents":
                    API.SysMsg(TITLE + ": out of reagents for %s." % j["spell"], HUE_ERR)
                    stop_job()
                elif res in ("fizzle", "busy", "mana"):
                    job_retry(j, now, res)
                else:
                    job_next(j, True)

        # ------------------------------ item hues (Find) -------------------------------
        #  Recoloured the way World Map > Traps & Fields does it: the item's own SetHue (current
        #  TazUO), else its Hue, else an API call; the way that worked is kept per
        #  wrapper type. Client-side only: the server never hears of it.
        _hue_way = {}

        def _hue_method(it, hue):
            fn = getattr(it, "SetHue", None)
            if fn is None:
                return False
            try:
                fn(hue)
                return True
            except Exception:
                return False

        def _hue_attr(it, hue):
            try:
                it.Hue = hue
                return int(it.Hue) == hue
            except Exception:
                return False

        def _hue_api(it, hue):
            for name in ("SetHue", "SetItemHue"):
                fn = getattr(API, name, None)
                if fn is not None:
                    try:
                        fn(it.Serial, hue)
                        return True
                    except Exception:
                        pass
            return False

        HUE_WAYS = (_hue_method, _hue_attr, _hue_api)

        def set_hue(it, hue):
            hue = int(hue) & 0xFFFF
            t = type(it)
            way = _hue_way.get(t)
            if way is not None and way(it, hue):
                return True
            for fn in HUE_WAYS:
                if fn is not way and fn(it, hue):
                    _hue_way[t] = fn
                    return True
            return False

        def hue_of(it):
            try:
                return int(it.Hue or 0)
            except Exception:
                return -1

        # ------------------------------ item search (Find) ------------------------------
        SR = {"text": "",        # what the Find box holds, as last read
              "typed": 0.0,      # when it last changed
              "armed": False,    # a change waits SEARCH_SETTLE before it searches
              "lit": {},         # item serial -> the hue it had before it lit up
              "until": 0.0,      # when the lit items are put back (0: nothing lit)
              "counts": {},      # slot index -> matches in its bag
              "restored": {},    # item serial -> (hue put back, when): see light
              "tiles": {},       # graphic -> its tile name, lower case (capped)
              "status": None,    # the side panel line Find wrote last
              "texts": {},       # (2.6.82) item serial -> its tooltip text, lower case, for
              "texts_at": 0.0,   #  one typing spell (at most SEARCH_LIT s old; see item_text)
              "objs": {}}        # (2.6.82) item serial -> the item as the last scan read it

        def search_terms(q):
            """'nightshade, 0x0F7A' -> [(text, graphic or None), ...]: a number
            (0x hex, or plain digits) is a graphic, anything else part of a name."""
            out = []
            for part in (q or "").lower().split(","):
                p = part.strip()
                if not p:
                    continue
                g = None
                try:
                    if p.startswith("0x") and len(p) > 2:
                        g = int(p, 16)
                    elif p.isdigit():
                        g = int(p)
                except ValueError:
                    g = None
                out.append((p, g))
            return out

        def expand_tile(raw):
            """Tiledata's 'rub%ies/y%' -> 'ruby rubies' (singular and plural)."""
            if "%" not in raw:
                return raw
            one, many = [], []
            for i, p in enumerate(raw.split("%")):
                if i % 2 == 0:
                    one.append(p)
                    many.append(p)
                else:
                    pl, _, sg = p.partition("/")
                    one.append(sg)
                    many.append(pl)
            return "".join(one) + " " + "".join(many)

        def tile_name(it, graphic):
            names = SR["tiles"]
            t = names.get(graphic)
            if t is None:
                try:
                    d = it.GetItemData()
                    raw = str(d.Name or "") if d is not None else ""
                except Exception:
                    raw = ""
                t = expand_tile(raw).lower()
                if len(names) >= TILE_NAME_CAP:
                    names.clear()
                names[graphic] = t
            return t

        def item_text(it, serial, graphic):
            """What the client already knows of an item's name, lower case: its
            tooltip text (name and properties), else its name; with its tile name.
            Never asks the server: ItemNameAndProps without wait only reads what
            the client has. (2.6.82) A tooltip text found is kept for the typing
            spell (SR["texts"], dropped SEARCH_LIT s after it began and when the
            search clears): typing on asks the client again only for the rest."""
            tc = SR["texts"]
            t = tc.get(serial)
            if t is not None:
                return t + "\n" + tile_name(it, graphic)
            try:
                t = API.ItemNameAndProps(serial) or ""
            except Exception:
                t = ""
            if t:
                t = str(t).lower()
                if "\n" in t and len(tc) < SEARCH_SCAN_CAP:   # (2.6.83) only with its properties in:
                    tc[serial] = t                             # a name alone may be still arriving
                return t + "\n" + tile_name(it, graphic)
            if not t:
                try:
                    t = it.Name or ""
                except Exception:
                    t = ""
            return str(t).lower() + "\n" + tile_name(it, graphic)

        def scan_matches(terms):
            """Every slot's bag looked at once: ({item serial: slot}, {slot: count}).
            An item in a bag inside the slot's bag counts for that slot, and that
            bag lights up with it; what another slot's bag holds counts there only."""
            assigned = set(s for _, s in st.layout)
            found, counts = {}, {}
            objs = {}                             # (2.6.82) the items read here, for light
            seen = 0
            for idx, bag in st.layout:
                if seen >= SEARCH_SCAN_CAP:
                    break
                try:
                    items = API.ItemsInContainer(bag, True) or []
                except Exception:
                    items = []
                # (2.6.82) every item's serial read once (the pass below reuses it), its
                # graphic only for an item this slot holds
                parent = {}
                sers = []
                for it in items:
                    try:
                        xs = int(it.Serial)
                    except Exception:
                        sers.append(None)
                        continue
                    sers.append(xs)
                    try:
                        parent[xs] = int(it.Container)
                    except Exception:
                        pass
                n = 0
                for j in range(len(sers)):
                    if seen >= SEARCH_SCAN_CAP:
                        break
                    seen += 1
                    serial = sers[j]
                    if serial is None or serial in assigned:
                        continue                  # (a slot's own bag: searched as that slot)
                    top, c, depth = serial, parent.get(serial, bag), 0
                    while c != bag and depth < SEARCH_DEPTH and c not in assigned:
                        top, c = c, parent.get(c, bag)
                        depth += 1
                    if c != bag:
                        continue                  # in another slot's bag (or too deep)
                    it = items[j]
                    try:
                        graphic = int(it.Graphic)
                    except Exception:
                        continue
                    text = None
                    hit = False
                    for p, g in terms:
                        if g is not None:
                            if graphic == g:
                                hit = True
                                break
                        else:
                            if text is None:
                                text = item_text(it, serial, graphic)
                            if p in text:
                                hit = True
                                break
                    if not hit:
                        continue
                    n += 1
                    if len(found) < SEARCH_LIT_CAP:
                        found[serial] = idx
                        objs[serial] = it
                        if top != serial and len(found) < SEARCH_LIT_CAP:
                            found[top] = idx      # the bag in the slot's bag that holds it
                if n:
                    counts[idx] = n
            SR["objs"] = objs
            return found, counts

        def scanned(serial):
            """(2.6.82) The item as scan_matches read it in this same pass (a fresh
            wrapper of the same item: what API.FindItem gives), else FindItem."""
            it = SR["objs"].get(serial)
            if it is not None:
                return it
            try:
                return API.FindItem(serial)
            except Exception:
                return None

        def light(serial, now):
            """Light an item up and remember its hue. A hue put back by a search a
            moment ago may not have reached the client yet: then the item still
            shows ours, and the remembered one is its own."""
            it = scanned(serial)
            if not it:
                return False
            cur = hue_of(it)
            if cur < 0:
                return False
            orig = cur
            if cur == SEARCH_HUE:
                rec = SR["restored"].get(serial)
                if rec is not None and now - rec[1] < HUE_MEMORY:
                    orig = rec[0]
            if not set_hue(it, SEARCH_HUE):
                return False
            canvas_hue(serial, SEARCH_HUE)        # (2.6.78) no rebuild comes: the canvas told
            SR["lit"][serial] = orig
            return True

        def unlight(serial, orig, now):
            """Put an item's hue back, wherever it is now. Gone from the client:
            nothing to put back (it comes back with the server's hue). A hue that
            is neither ours nor the one it had was given by the server since (the
            item was moved and sent again, or recoloured): that one stands."""
            try:
                it = API.FindItem(serial)
            except Exception:
                it = None
            if not it:
                return
            cur = hue_of(it)
            if cur == SEARCH_HUE or cur == orig:
                if set_hue(it, orig):             # (also when it shows orig: a light still queued)
                    canvas_hue(serial, orig)
                SR["restored"][serial] = (orig, now)

        def prune_restored(now):
            rs = SR["restored"]
            if rs:
                for s in [s for s, rec in rs.items() if now - rec[1] >= HUE_MEMORY]:
                    del rs[s]
                if len(rs) > 2 * SEARCH_LIT_CAP:
                    rs.clear()

        def run_search(q, now):
            """Light up what matches q (what no longer matches is put back first;
            what still matches stays as it is) and show the counts."""
            terms = search_terms(q)
            if not terms:
                clear_search(now)
                return
            prune_restored(now)
            if not 0 <= now - SR["texts_at"] <= SEARCH_LIT:
                SR["texts"] = {}                  # (2.6.82) a new typing spell: texts read afresh
                SR["texts_at"] = now
            found, counts = scan_matches(terms)
            lit = SR["lit"]
            for serial in [s for s in lit if s not in found]:
                unlight(serial, lit.pop(serial), now)
            try:
                for serial in found:
                    if serial not in lit:
                        light(serial, now)
                    else:
                        relight(serial)
            finally:
                SR["objs"] = {}                   # (only for this pass: the next reads afresh)
            SR["counts"] = counts
            SR["until"] = now + SEARCH_LIT
            show_counts()
            total = 0
            for n in counts.values():
                total += n
            text = ("%d found" % total) if total else "None found"
            SR["status"] = text
            set_status(text)

        def relight(serial):
            """Still matching and still lit, unless the server sent the item again
            since (moved: its own hue is back): then that hue is its own now."""
            it = scanned(serial)
            if not it:
                return
            cur = hue_of(it)
            if 0 <= cur != SEARCH_HUE and set_hue(it, SEARCH_HUE):
                canvas_hue(serial, SEARCH_HUE)
                SR["lit"][serial] = cur

        def clear_search(now):
            """Every lit item back to its own hue; the counts gone."""
            lit = SR["lit"]
            for serial in list(lit):
                unlight(serial, lit.pop(serial), now)
            SR["texts"] = {}                      # (2.6.82) the typing spell is over
            SR["texts_at"] = 0.0
            SR["until"] = 0.0
            if SR["counts"]:
                SR["counts"] = {}
                show_counts()
            if SR["status"] is not None:
                if st.status_text == SR["status"]:
                    set_status("Idle")               # (empty, or the fit's scale)
                SR["status"] = None

        def show_counts():
            """The "n found" caption on each slot (only the ones that change)."""
            counts = SR["counts"]
            state = ui["count_state"]
            for idx, (lab, x, y, cw, ch) in enumerate(ui["counts"]):
                n = counts.get(idx, 0)
                text = ("%d found" % n) if n else ""
                if state.get(idx) == text:
                    continue
                state[idx] = text
                try:
                    if n:
                        lab.SetPos(x + max(5, cw - 5 - Kit.text_w(text)), y + max(0, ch - 18))
                        Kit.set_text(lab, text)
                    lab.IsVisible = bool(n)
                except Exception:
                    pass

        def search_tick(now):
            """The Find box, read every pass (in place on the client thread): it
            searches SEARCH_SETTLE after the last key; the lit items go back when
            their time is up."""
            box = ui["search_box"]
            if box is not None and not (st.collapsed or st.docked):   # (2.6.82) not while hidden
                try:
                    txt = box.Text
                except Exception:
                    txt = None
                if txt is not None:
                    txt = str(txt)
                    if txt != SR["text"]:
                        SR["text"], SR["typed"], SR["armed"] = txt, now, True
            if SR["armed"]:
                if now - SR["typed"] >= SEARCH_SETTLE:
                    SR["armed"] = False
                    q = SR["text"].strip()
                    if len(q) >= SEARCH_MIN:
                        run_search(q, now)
                    elif SR["lit"] or SR["counts"]:
                        clear_search(now)
            elif SR["until"] and now >= SR["until"]:
                clear_search(now)

        def build_tools(grid, bx, y):
            """The side panel's filter box (it filters live as you type: no button
            since 2.6.51), and Sort with the Sort rules button under it."""
            # (2.6.72) the box has its label (UI rules 3.5); Rules has its caption, on a row
            # of its own under Sort
            lw = Kit.text_w("Find:") + 6
            label(grid, "Find:", bx + 2, y + 3, Kit.HUE_TEXT)
            box = Kit.add_textbox(grid, SR["text"], bx + 2 + lw, y, SIDE_BTN_W - 4 - lw, numbers=False)
            safe(lambda: box.SetTooltip("Part of an item's name, or a graphic (0x0F7A or 3962); commas "
                                        "for several. Matching items light up for %d s as you type."
                                        % int(SEARCH_LIT)))
            ui["search_box"] = box
            Kit.art_button(grid, ui["store"], "rules", Kit.ART_PAGE, bx, y + 28,
                           "Rules", "Open the sort rules window: what each slot's bag holds",
                           on_click=act(open_rules))
            Kit.art_button(grid, ui["store"], "filters", Kit.ART_PAGE, bx, y + 52,
                           "Filters", "Open the sort filters window: pick an item or a preset, "
                           "and the bag it goes to", on_click=act(open_filters))

        # ---------- (2.6.85) Restock, Sort, Storage and Supplies, on the sidebar ----------
        #  Each press is one action: Restock and Sort start one bounded run, Storage and
        #  Supplies open their window or bring it to the front. A part that is off shows
        #  grey and says where to turn it on.
        QUICK = (("q_restock", "Restock", Kit.ART_PLAY, 0x0E76, "restock",
                  "Top your supplies up once, from the chest or bank set on the Restock window",
                  "restock.run"),
                 ("q_sort", "Sort", Kit.ART_PLAY, 0x0E79, None,
                  "Move the items into their bags once; picking an item up or Stop ends it", None),
                 ("q_storage", "Storage", Kit.ART_PAGE, 0x0E40, "storage",
                  "Open the Storage window, or bring it to the front", "storage.show"),
                 ("q_supplies", "Supplies", Kit.ART_PAGE, 0x0F7A, "supplies",
                  "Open the Supplies table, or bring it to the front", "supplies.open"))

        def quick_on(part):
            if part is None:
                return True
            try:
                return bool(HOST.part_on(part, "inventory"))
            except Exception:
                return False

        def quick_tip(part, tip):
            if quick_on(part):
                return tip
            return "%s is off: tick Inventory > %s on the Modules tab" % (part.title(), part.title())

        def quick_press(key):
            """One press of a sidebar button, on the module's next pass."""
            for k, cap, _art, _icon, part, _tip, svc in QUICK:
                if k != key:
                    continue
                if part is None:
                    start_sort()
                    return
                fn = HOST.services.get(svc) if quick_on(part) else None
                if fn is None:
                    API.SysMsg("%s: %s is off; tick Inventory > %s on the Modules tab." %
                               (TITLE, cap, cap), HUE_INFO)
                    return
                fn()
                return

        def quick_sig():
            return tuple(quick_on(q[4]) for q in QUICK)

        def build_quick(grid, bx, y):
            """The four captioned buttons of the side panel; a part that is off is grey."""
            ui["quick_sig"] = quick_sig()
            for i, (k, cap, art, _icon, part, tip, _svc) in enumerate(QUICK):
                Kit.art_button(grid, ui["store"], k, art, bx, y + i * 24, cap, quick_tip(part, tip),
                               hue=None if quick_on(part) else Kit.HUE_INFO, on_click=act(quick_press, k))

        QUICK_ICON = 18                 # the minimized strip's item art, this square
        QUICK_STEP = 22

        def add_quick_strip(grid, x_right, y):
            """(2.6.85) With the sidebar minimized: the same four actions as small item
            art with tooltips, in a row ending at x_right."""
            ui["quick_sig"] = quick_sig()
            x = x_right - len(QUICK) * QUICK_STEP
            for i, (k, cap, _art, icon, part, tip, _svc) in enumerate(QUICK):
                try:
                    pic = G.CreateGumpItemPic(icon, QUICK_ICON, QUICK_ICON)
                    pic.SetRect(x + i * QUICK_STEP, y, QUICK_ICON, QUICK_ICON)
                    if not quick_on(part):
                        safe(lambda: setattr(pic, "Hue", Kit.HUE_INFO))
                    safe(lambda: setattr(pic, "DrawBorder", False))
                    t = quick_tip(part, tip)
                    safe(lambda: pic.SetTooltip(t if not quick_on(part) else cap + ": " + t))
                    G.AddControlOnClick(pic, act(quick_press, k))
                    grid.Add(pic)
                except Exception:
                    pass

        # ---------------------------------- sort (Sort) ---------------------------------
        KIND_GRAPHICS = dict((k, frozenset(gs)) for k, _c, gs in SORT_KINDS)
        NO_RULE = (frozenset(), ())

        def rule_graphics(idx):
            """Every graphic slot idx's bag holds (its kinds and its own graphics)."""
            kinds, extra = st.rules.get(idx, NO_RULE)
            out = set(extra)
            for k in kinds:
                out |= KIND_GRAPHICS.get(k, frozenset())
            return out

        def held_item():
            try:
                return int(API.GetHeldItem() or 0)
            except Exception:
                return 0

        def in_corpse(serial):
            """(2.6.84) The bag is a corpse or sits in one: Sort never takes from it
            (lifting from a corpse is looting, which can flag you criminal: R6)."""
            try:
                s = int(serial or 0)
            except Exception:
                return True
            for _ in range(12):
                it = safe(lambda: API.FindItem(s))
                if it is None:
                    return False
                if int(safe(lambda: it.Graphic, 0) or 0) == 0x2006 or \
                        bool(safe(lambda: it.IsCorpse, False)):
                    return True
                c = int(safe(lambda: it.Container, 0) or 0)
                if not c or c == 0xFFFFFFFF or c < 0x40000000:
                    return False                    # on the ground or on a mobile
                s = c
            return False


        def sort_plan():
            """The moves one Sort would make: [(serial, from, to, slot)], or None when
            no filter or rule is set. (2.6.85) Filters first, the first match wins; a
            filter that matches sends the item even from a bag whose rules hold it.
            Then the rules: every item in the backpack or a slot's bag that another
            slot's bag holds, unless the bag it is in holds it too. The first slot that
            holds a graphic gets it."""
            flt = [f for f in st.filters if f["on"] and f["slot"] is not None and f["set"]]
            wants = {}
            for idx, bag in st.layout:
                gs = rule_graphics(idx)
                if gs:
                    wants[idx] = gs
            if not wants and not flt:
                return None
            by_graphic = {}
            for idx in sorted(wants):
                for g in wants[idx]:
                    if g not in by_graphic:
                        by_graphic[g] = idx
            slot_of = dict((s, i) for i, s in st.layout)
            sources = []
            pack = safe(lambda: int(API.Backpack), 0)
            if pack:
                sources.append(pack)
            for _, bag in st.layout:
                if bag not in sources and not in_corpse(bag):   # (2.6.84) never a corpse (R6)
                    sources.append(bag)
            plan = []
            for src in sources:
                here = wants.get(slot_of.get(src), ())    # what this bag holds itself
                try:
                    items = API.ItemsInContainer(src, False) or []
                except Exception:
                    items = []
                for it in items:
                    if len(plan) >= SORT_CAP:
                        break
                    try:
                        serial, graphic = int(it.Serial), int(it.Graphic)
                    except Exception:
                        continue
                    if serial in slot_of:
                        continue
                    idx = None
                    if flt:
                        hue = int(getattr(it, "Hue", 0) or 0) & 0x3FFF
                        for f in flt:
                            if graphic in f["set"] and (f["hue"] is None or f["hue"] == hue):
                                idx = f["slot"]
                                break
                    if idx is None:
                        idx = by_graphic.get(graphic)
                        if idx is None or graphic in here:
                            continue
                    try:
                        if it.IsContainer:
                            continue                     # bags are never moved
                    except Exception:
                        pass
                    dest = st.assign.get(idx)
                    if dest and dest != src:
                        plan.append((serial, src, dest, idx))
            return plan

        def start_sort():
            """Plan the moves and start one bounded run (player-started only)."""
            sync_rules()
            if st.sort:
                API.SysMsg(TITLE + ": already sorting; press Stop first.", HUE_ERR)
                return
            if st.job:
                API.SysMsg(TITLE + ": busy with %s; press Stop first." % st.job["spell"], HUE_ERR)
                return
            plan = sort_plan()
            if plan is None:
                API.SysMsg(TITLE + ": no slot's bag has a sort rule yet; tick what each bag holds "
                           "in the Sort rules window.", HUE_ERR)
                open_rules()
                return
            if not plan:
                API.SysMsg(TITLE + ": nothing to sort; every item with a rule is in its bag.", HUE_INFO)
                set_status("Nothing to sort")
                return
            st.sort = {"plan": plan, "i": 0, "move": None, "check": None, "at": 0.0, "hold": 0.0,
                       "moved": 0, "refused": 0, "streak": 0, "rechecks": 0, "waits": 0,
                       "why": None, "last": 0, "sent_at": 0.0, "jr": None}
            set_status("Sort 0/%d" % len(plan))
            API.SysMsg(TITLE + ": sorting %d item%s." % (len(plan), "" if len(plan) == 1 else "s"),
                       HUE_INFO)

        def say_replies(s):
            """Debug (settings page): the journal lines since the move was picked."""
            for ln in s["jr"].new():
                if ln.text and not ln.text.startswith(TITLE):
                    API.SysMsg(TITLE + ": reply: " + ln.text.strip(), HUE_INFO)

        def say_move(s, what):
            if st.sort_say:
                API.SysMsg(TITLE + ": move %d/%d: %s." % (s["i"], len(s["plan"]), what), HUE_INFO)

        def check_move(s, now):
            """The last move's answer, SORT_GAP after it went out: True to go on with
            the next item, False when the sort stopped or waits a little longer."""
            serial, src, dest, idx = s["check"]
            t0 = s["sent_at"]
            if Journal.find(t0, J_FULL) is not None:
                stop_sort("bag #%d (%s) is full" % (idx + 1, bag_name(dest, False)))
                return False
            try:
                it = API.FindItem(serial)
                where = int(it.Container) if it else None
            except Exception:
                where = None
            if where is None and s["rechecks"] < SORT_RECHECK and not stacked(s, dest):
                # out of view and its bag's pile hasn't grown: the client lifts an item
                # out of the world until the server answers, so on a slow connection
                # wait for the answer before counting it as stacked
                say_move(s, "not answered yet")
                s["rechecks"] += 1
                s["at"] = now + SORT_GAP * 0.5
                return False
            if where is None or where == dest:           # in (or stacked into) its bag
                say_move(s, "in its bag" if where == dest else "gone from view (stacked)")
                s["moved"] += 1
                s["streak"] = s["rechecks"] = s["waits"] = 0
                s["check"] = None
                return True
            if where == src and Journal.find(t0, J_WAIT) is not None and s["waits"] < SORT_FAIL_STOP:
                say_move(s, "too soon for the server; again in %.1f s" % SORT_GAP)
                s["waits"] += 1                          # too soon for the server: the same item again
                s["i"] -= 1
                s["check"] = None
                s["rechecks"] = 0
                s["hold"] = now + SORT_GAP
                return False
            if s["rechecks"] < SORT_RECHECK:            # no answer yet: look again a little later
                say_move(s, "no answer yet")
                s["rechecks"] += 1
                s["at"] = now + SORT_GAP * 0.5
                return False
            say_move(s, "still where it was (refused)")
            s["check"] = None
            s["rechecks"] = 0
            s["refused"] += 1
            s["streak"] += 1
            if s["streak"] >= SORT_FAIL_STOP:
                stop_sort("%d moves in a row were refused" % s["streak"])
                return False
            return True

        def stack_total(bag, graphic, deep=None):
            """How many of `graphic` lie loose in `bag` (a stacked move adds to it).
            (2.6.82) deep: the bag's deep list already read this pass; its items
            whose container is the bag are exactly its top level (one scan, not two)."""
            n = 0
            try:
                if deep is None:
                    for x in (API.ItemsInContainer(bag, False) or []):
                        if int(x.Graphic) == graphic:
                            n += int(x.Amount or 1)
                else:
                    for x in deep:
                        if int(x.Graphic) == graphic and int(x.Container) == bag:
                            n += int(x.Amount or 1)
            except Exception:
                pass
            return n

        def stacked(s, bag):
            """The moved item's pile grew in its bag (or nothing to tell by)."""
            pre = s.get("pre")
            if not pre or not pre[0]:
                return True
            return stack_total(bag, pre[0]) >= pre[2] + pre[1]

        def sort_tick(now):
            """One step of the sort (client tick): the last move's answer, the
            stops, then the next item, which thread_tick sends."""
            s = st.sort
            if s is None:
                return
            if st.sort_say and s.get("jr") is not None:
                say_replies(s)
            if s["move"] is not None:
                return                                   # a move waits for thread_tick
            if s["why"]:
                stop_sort(s["why"])
                return
            if s["check"] is not None:
                if now < s["at"] or not check_move(s, now):
                    return
            if now < s["hold"]:
                return
            if others_cursor():
                stop_sort("another target cursor is in use")
                return
            h = held_item()
            if h and not (h == s["last"] and now - s["sent_at"] < 2 * SORT_GAP):
                stop_sort("you picked something up")
                return
            plan = s["plan"]
            while s["i"] < len(plan):
                serial, src, dest, idx = plan[s["i"]]
                s["i"] += 1
                try:
                    it = API.FindItem(serial)
                    where = int(it.Container) if it else 0
                except Exception:
                    where = 0
                if where != src:
                    continue                             # gone, or moved by hand since the plan
                if st.assign.get(idx) != dest:
                    continue                             # that slot's bag changed since the plan
                if not get_item(dest):
                    stop_sort("slot #%d's bag is out of reach" % (idx + 1))
                    return
                try:
                    deep = API.ItemsInContainer(dest, True) or []
                    inside = len(deep)
                except Exception:
                    deep = None
                    inside = 0
                if inside >= BAG_MAX_ITEMS:
                    stop_sort("bag #%d (%s) is full" % (idx + 1, bag_name(dest, False)))
                    return
                s["move"] = (serial, src, dest, idx)
                gr = int(getattr(it, "Graphic", 0) or 0)      # (2.6.82: read once)
                s["pre"] = (gr, int(getattr(it, "Amount", 1) or 1),
                            stack_total(dest, gr, deep))
                if st.sort_say:
                    s["jr"] = Journal.reader()           # debug: the server's replies to this move
                set_status("Sort %d/%d" % (s["i"], len(plan)))
                return
            finish_sort()

        def sort_send():
            """thread_tick: the move the client tick picked goes out, in one hop
            that looks at the cursor and your hand first (nothing is moved while
            you hold an item or another cursor is up)."""
            s = st.sort
            if s is None or s["move"] is None:
                return
            mv = s["move"]

            def run():
                if st.sort is not s or s["move"] is not mv or st.stopping:
                    return "gone"
                if others_cursor():
                    return "another target cursor is in use"
                if held_item():
                    return "you picked something up"
                API.MoveItem(mv[0], mv[2])
                return "sent"
            try:
                res = Kit.on_client(run)
            except Exception as e:
                res = "a move failed (%s)" % e
            if st.sort is not s:
                return
            s["move"] = None
            if res == "sent":
                try:
                    HOST.pack_dirty()                    # (2.6.82) the shared pack list read anew
                except Exception:
                    pass
                s["check"] = mv
                s["last"] = mv[0]
                s["sent_at"] = time.time()
                s["at"] = s["sent_at"] + SORT_GAP
            elif res != "gone":
                s["why"] = res                           # the next client tick stops it and says why

        def finish_sort():
            s, st.sort = st.sort, None
            if s is None:
                return
            msg = "%d moved" % s["moved"]
            if s["refused"]:
                msg += ", %d refused" % s["refused"]
            API.SysMsg(TITLE + ": sort done: %s." % msg, HUE_ERR if s["refused"] else HUE_OK)
            set_status("Sorted %d" % s["moved"])

        def stop_sort(why=None, user=False):
            s, st.sort = st.sort, None
            if s is None:
                return
            if user:
                API.SysMsg(TITLE + ": sort stopped (%d moved)." % s["moved"], HUE_INFO)
                set_status("Stopped")
            elif why:
                API.SysMsg(TITLE + ": sort stopped: %s (%d moved)." % (why, s["moved"]), HUE_ERR)
                set_status("Sort stopped")

        def stop_all():
            """The side panel's Stop: trapping / untrapping and sorting."""
            stop_job(True)
            stop_sort(user=True)

        # ------------------------------ Sort filters window (2.6.85) --------------------
        #  A filter: (name, the graphics it matches, a hue or None, the slot it sends to,
        #  on or off). Saved in a key of their own, so a save of an older version loads
        #  as before and the rules' format never changes. How broadly a picked item matches:
        #  this exact item (graphic and hue), this kind (graphic) or its category.
        FILTERS_KEY = "UnifiedBag_filters"
        FILTERS_CAP = 40
        BROAD = ("exact", "kind", "category")
        BROAD_CAP = {"exact": "this exact item", "kind": "this kind", "category": "its category"}
        # the presets' words in the client's item names; the rest by the tile data's flags
        PRESETS = (("reagents", "Reagents"), ("potions", "Potions"), ("bandages", "Bandages"),
                   ("gold", "Gold and gems"), ("scrolls", "Scrolls"), ("maps", "Treasure maps"),
                   ("ores", "Ores and ingots"), ("wood", "Wood"), ("hides", "Hides and cloth"),
                   ("food", "Food"), ("weapons", "Weapons"), ("armour", "Armour"),
                   ("jewellery", "Jewellery"), ("keys", "Keys and tools"))
        CAT_WORDS = {"maps": ("treasure map", "tattered map", "map"),
                     "ores": (" ore", "ingot"), "wood": ("log", "board"),
                     "hides": ("hide", "leather", "cloth", "wool", "cotton", "flax", "yarn",
                               "thread", "bolt of"),
                     "food": ("bread", "cake", "muffin", "pie", "apple", "pear", "peach", "grape",
                              "fish steak", "ham", "bacon", "sausage", "ribs", "cheese", "carrot",
                              "lettuce", "cabbage", "turnip", "onion", "melon", "squash", "gourd",
                              "lemon", "lime", "banana", "date", "coconut", "chicken", "bird",
                              "egg", "cookie", "wedge", "corn", "pumpkin", "meat", "jar of honey"),
                     "keys": ("key", "tongs", "hammer", "saw", "scissors", "pickaxe", "shovel",
                              "lockpick", "sewing", "tinker", "mortar", "fletcher", "dovetail",
                              "skillet", "rolling pin", "scorp", "plane", "inshave", "fishing pole",
                              "hatchet", "smith")}
        LAYER_JEWEL = (0x06 + 2, 0x0A, 0x0E, 0x12)   # ring, neck, bracelet, earrings (client Layer)
        FLAG_ARMOUR = 0x08000000                     # the tile data's Armor flag
        cats = {"data": None, "wanted": False}       # category -> frozenset of graphics

        def build_cats():
            """thread_tick, once: every category from the client's tile data."""
            f = getattr(R, "f_tiles", None)
            arr = f.GetValue(None) if f is not None else None
            out = dict((k, set()) for k, _c in PRESETS)
            for k, _c, gs in SORT_KINDS:
                if k == "gems":
                    out["gold"].update(gs)
                elif k in out:
                    out[k].update(gs)
            if arr is not None:
                for gr in range(min(int(arr.Length), 0x10000)):
                    try:
                        t = arr[gr]
                        name = str(t.Name or "").lower()
                        if not name:
                            continue
                        fl = int(t.Flags)
                        if bool(t.IsImpassable):             # not something you carry
                            continue
                        if bool(t.IsWeapon):
                            out["weapons"].add(gr)
                        if fl & FLAG_ARMOUR:
                            out["armour"].add(gr)
                        if bool(t.IsWearable) and int(t.Layer) in LAYER_JEWEL:
                            out["jewellery"].add(gr)
                        if fl & 0x00200000 or bool(t.IsContainer):   # (a container, a door...)
                            continue
                        padded = " " + name
                        for k, words in CAT_WORDS.items():
                            for w in words:
                                if w in padded:
                                    out[k].add(gr)
                                    break
                    except Exception:
                        continue
            cats["data"] = dict((k, frozenset(v)) for k, v in out.items())
            st.dirty_flt = st.open_flt

        def category_of(graphic):
            """The first preset holding graphic, or None."""
            data = cats["data"] or {}
            for k, _c in PRESETS:
                if graphic in data.get(k, ()):
                    return k
            return None

        def load_filters():
            """Saved as name~graphics~hue~slot~on;... (graphics in hex, comma separated;
            a category's name instead of graphics, read when the categories are)."""
            st.filters = []
            for part in str(Kit.get_var(FILTERS_KEY, "") or "").split(";"):
                p = part.split("~")
                if len(p) < 5 or len(st.filters) >= FILTERS_CAP:
                    continue
                try:
                    slot = int(p[3]) if p[3] != "" else None
                    hue = int(p[2]) if p[2] != "" else None
                    gs = tuple(int(x, 16) for x in p[1].split(",") if x and not x.startswith("@"))
                except ValueError:
                    continue
                cat = p[1][1:] if p[1].startswith("@") else None
                st.filters.append({"name": p[0], "gr": gs, "cat": cat, "hue": hue, "slot": slot,
                                   "on": p[4] == "1", "set": frozenset(gs)})
            cats["wanted"] = cats["wanted"] or any(f["cat"] for f in st.filters)

        def save_filters():
            out = []
            for f in st.filters:
                out.append("~".join((f["name"].replace(";", " ").replace("~", " "),
                                     "@" + f["cat"] if f["cat"] else
                                     ",".join("%X" % g for g in f["gr"]),
                                     "" if f["hue"] is None else str(f["hue"]),
                                     "" if f["slot"] is None else str(f["slot"]),
                                     "1" if f["on"] else "0")))
            Kit.put_var(FILTERS_KEY, ";".join(out))
            st.dirty_flt = st.open_flt

        def filter_sets():
            """A category's graphics, once the categories are read."""
            data = cats["data"]
            if data is None:
                return
            for f in st.filters:
                if f["cat"]:
                    f["set"] = data.get(f["cat"], frozenset())

        def open_filters():
            cats["wanted"] = True
            st.open_flt = True
            st.dirty_flt = True

        def close_filters():
            remember_filter_pos()
            dispose("flt")
            st.open_flt = False
            ui["flt_checks"] = []

        def remember_filter_pos():
            g = ui.get("flt")
            if Kit.is_open(g):
                try:
                    st.flt_x, st.flt_y = int(g.GetX()), int(g.GetY())
                except Exception:
                    pass

        def toggle_flt_min():
            remember_filter_pos()
            st.flt_min = not st.flt_min
            st.dirty_flt = True

        def filter_add(name, gr, hue, cat=None, broad=None):
            if len(st.filters) >= FILTERS_CAP:
                API.SysMsg(TITLE + ": %d filters is the most; remove one first." % FILTERS_CAP, HUE_ERR)
                return None
            f = {"name": name, "gr": tuple(gr), "cat": cat, "hue": hue, "slot": None, "on": True,
                 "set": frozenset(gr), "broad": broad}
            st.filters.append(f)
            filter_sets()
            save_filters()
            return f

        def filter_preset(key):
            for k, cap in PRESETS:
                if k == key:
                    for f in st.filters:
                        if f["cat"] == key:
                            API.SysMsg(TITLE + ": %s is already on the list." % cap, HUE_INFO)
                            return
                    filter_add(cap, (), None, key)

        def filter_by_target():
            API.SysMsg(TITLE + ": target an item for the new filter.", HUE_INFO)
            pick_then(filter_targeted)

        def filter_targeted(target):
            if not target:
                API.SysMsg(TITLE + ": cancelled.", HUE_INFO)
                return
            it = get_item(target)
            if not it:
                API.SysMsg(TITLE + ": that isn't an item.", HUE_ERR)
                return
            if safe(lambda: bool(it.IsContainer), False):
                API.SysMsg(TITLE + ": bags aren't sorted; target an item.", HUE_ERR)
                return
            filter_from(int(it.Graphic), int(getattr(it, "Hue", 0) or 0) & 0x3FFF,
                        str(safe(lambda: it.Name, "") or ""))

        def filter_from(graphic, hue, name):
            """A new filter from a picked item: this exact item, until Match is clicked."""
            if not name:
                t = tile_of(graphic)
                name = str(getattr(t, "Name", "") or "") if t is not None else ""
            filter_add((name or "0x%04X" % graphic)[:30], (graphic,), hue, None, "exact")

        def filter_dropped():
            """The list area was clicked: an item let go there fills a new filter, and
            goes straight back where it came from."""
            try:
                hold = item_hold()
            except Exception:
                hold = None
            if hold is None:
                return
            try:
                hs = int(Tz.get(hold, "Serial"))
                gr = int(Tz.get(hold, "Graphic"))
                hue = int(Tz.get(hold, "Hue")) & 0x3FFF
                home = int(Tz.get(hold, "Container"))
            except Exception:
                return
            if safe(lambda: bool(tile_of(gr).IsContainer), False):
                API.SysMsg(TITLE + ": bags aren't sorted; drop an item.", HUE_ERR)
                return
            filter_from(gr, hue, "")
            if home and home != 0xFFFFFFFF:
                import System
                Tz.call(None, "DropItem", (System.UInt32(hs), 0xFFFF, 0xFFFF, 0,
                                           System.UInt32(home), False), R.Actions)

        def filter_broader(i):
            """Match: this exact item, this kind, its category, and round again."""
            if not 0 <= i < len(st.filters):
                return
            f = st.filters[i]
            if f.get("base") is None and f["gr"]:
                f["base"] = (f["gr"][0], f["hue"] or 0)
            base = f.get("base")
            if base is None:
                return
            now = f.get("broad") or ("category" if f["cat"] else ("exact" if f["hue"] is not None else "kind"))
            nxt = BROAD[(BROAD.index(now) + 1) % len(BROAD)]
            if nxt == "category":
                cat = category_of(base[0])
                if cat is None:
                    nxt = "exact"                      # not in any category: back round
                else:
                    f.update({"cat": cat, "hue": None, "gr": (base[0],)})
            if nxt == "exact":
                f.update({"cat": None, "hue": base[1], "gr": (base[0],), "set": frozenset((base[0],))})
            elif nxt == "kind":
                f.update({"cat": None, "hue": None, "gr": (base[0],), "set": frozenset((base[0],))})
            f["broad"] = nxt
            filter_sets()
            save_filters()

        def filter_move(i, d):
            j = i + d
            if 0 <= i < len(st.filters) and 0 <= j < len(st.filters):
                st.filters[i], st.filters[j] = st.filters[j], st.filters[i]
                save_filters()

        def filter_remove(i):
            if 0 <= i < len(st.filters):
                del st.filters[i]
                save_filters()

        def filter_pick_bag(i):
            """Its bag: a target cursor on any bag or item in a slot, or a click on its
            region of the canvas."""
            if not 0 <= i < len(st.filters):
                return
            st.flt_pick = st.filters[i]
            API.SysMsg(TITLE + ": click a bag on the bags display, or target a bag in a slot.", HUE_INFO)
            pick_then(filter_bag_targeted, st.flt_pick)

        def filter_bag_targeted(f, target):
            if st.flt_pick is not f:
                return                                 # the canvas took it
            st.flt_pick = None
            if not target:
                return
            slots = dict((b, i) for i, b in st.layout)
            s = int(target)
            for _ in range(8):                         # the bag itself, or what it sits in
                if s in slots:
                    f["slot"] = slots[s]
                    save_filters()
                    return
                it = get_item(s)
                s = int(safe(lambda: it.Container, 0) or 0) if it else 0
                if not s:
                    break
            API.SysMsg(TITLE + ": that isn't in a bag slot; put the bag in a slot first (Slots).", HUE_ERR)

        def filter_canvas_pick(slot_index):
            """A click on a bag's region of the canvas while a filter waits for its bag."""
            f, st.flt_pick = st.flt_pick, None
            if f is None:
                return False
            f["slot"] = slot_index
            save_filters()
            safe(API.CancelTarget)                     # the cursor raised for this pick
            return True

        def filter_poll():
            """The on / off boxes: a change is saved at once."""
            for i, chk in ui.get("flt_checks") or ():
                if i < len(st.filters):
                    on = bool(safe(lambda: chk.IsChecked, st.filters[i]["on"]))
                    if on != st.filters[i]["on"]:
                        st.filters[i]["on"] = on
                        save_filters()
                        return

        def build_filters():
            remember_filter_pos()
            dispose("flt")
            filter_sets()
            M, GAP = Kit.MARGIN, Kit.GAP
            n = len(st.filters)
            row_h, h_add, h_prev = 28, 30 + 3 * 26 + 8, 40
            list_h = max(row_h * 2, min(n, 12) * row_h + 8)
            w = 640
            h = (M + 30 + M if st.flt_min else
                 M + 30 + GAP + h_prev + GAP + h_add + GAP + list_h + M)
            g, store, y = framed_window("bag_flt", st.flt_x, st.flt_y, w, h, "SORT FILTERS",
                                        st.flt_min, act(toggle_flt_min), act(close_filters))
            checks = []
            if not st.flt_min:
                IW = w - 2 * M
                Kit.add_section(g, M, y, IW, h_prev)
                Kit.art_button(g, store, "sort", Kit.ART_PLAY, M + 12, y + 9, "Sort",
                               "Move the matching items into their bags once; picking an item up "
                               "or Stop ends it", on_click=act(start_sort))
                plan = safe(sort_plan)
                k = len(plan) if plan else 0
                Kit.add_label(g, "%d item%s would move" % (k, "" if k == 1 else "s"), M + 100, y + 12,
                              Kit.HUE_INFO)
                y += h_prev + GAP
                Kit.add_section(g, M, y, IW, h_add, "ADD A FILTER")
                bx = M + 12
                Kit.art_button(g, store, "add", Kit.ART_PLAY, bx, y + 28, "Add by target...",
                               "Target an item: the filter fills in from it", on_click=act(filter_by_target))
                cols = 5
                cw = (IW - 24) // cols
                for pi, (key, cap) in enumerate(PRESETS):
                    col, row = (pi + 1) % cols, (pi + 1) // cols
                    Kit.art_button(g, store, "pre_" + key, Kit.ART_OK, M + 12 + col * cw, y + 28 + row * 26,
                                   Kit.fit(cap, cw - 40),
                                   "Add the %s preset to the list" % cap.lower(),
                                   on_click=act(filter_preset, key))
                y += h_add + GAP
                Kit.add_section(g, M, y, IW, list_h)
                Kit.catcher(g, M, y, IW, list_h, act(filter_dropped),
                            "Drop an item here: a new filter fills in from it")
                if not n:
                    Kit.add_label(g, "No filters yet. Press a preset above, or Add by target and pick "
                                  "an item.", M + 12, y + 8, Kit.HUE_INFO)
                else:
                    sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                    for i, f in enumerate(st.filters):
                        ry = i * row_h
                        chk = Kit.add_check(sa, "", 4, ry + 3, f["on"],
                                            "Use this filter (unticked: kept, but it moves nothing)")
                        checks.append((i, chk))
                        Kit.add_label(sa, Kit.fit(f["name"], 150), 30, ry + 5)
                        broad = f.get("broad") or ("category" if f["cat"] else
                                                   ("exact" if f["hue"] is not None else "kind"))
                        if f["cat"] and not f.get("base"):
                            Kit.add_label(sa, "A preset", 186, ry + 5, Kit.HUE_INFO)
                        else:
                            Kit.art_button(sa, store, "m%d" % i, Kit.ART_PAGE, 186, ry + 2,
                                           "Match: " + broad,
                                           "How broadly it matches: %s; click for the next" % BROAD_CAP[broad],
                                           on_click=act(filter_broader, i))
                        if f["slot"] is None or f["slot"] not in st.assign:
                            cap, hue = "No bag", Kit.HUE_BAD
                        else:
                            cap, hue = short(bag_name(st.assign[f["slot"]], False), 14), Kit.HUE_TEXT
                        Kit.add_label(sa, cap, 330, ry + 5, hue)
                        Kit.art_button(sa, store, "b%d" % i, Kit.ART_PLAY, 424, ry + 2, "Bag...",
                                       "Click a bag on the bags display, or target a bag in a slot",
                                       on_click=act(filter_pick_bag, i))
                        Kit.art_button(sa, store, "u%d" % i, Kit.ART_PAGE, 508, ry + 2, None,
                                       "Move up: the first filter that matches wins",
                                       on_click=act(filter_move, i, -1))
                        Kit.art_button(sa, store, "d%d" % i, Kit.ART_PAGE, 536, ry + 2, None,
                                       "Move down: the first filter that matches wins",
                                       on_click=act(filter_move, i, 1))
                        Kit.art_button(sa, store, "x%d" % i, Kit.ART_CLOSE, 564, ry + 2, None,
                                       "Remove this filter", on_click=act(filter_remove, i))
                    g.Add(sa)
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, remember_filter_pos))
            ui["flt"] = g
            ui["flt_checks"] = checks

        # ------------------------------ Sort rules window -------------------------------
        def open_rules():
            st.open_srt = True
            st.dirty_srt = True
            schedule_save()

        def close_rules():
            sync_rules()
            remember_window_pos()
            dispose("srt")
            ui["rule_checks"] = []
            st.open_srt = False
            schedule_save()

        def toggle_srt_min():
            sync_rules()
            st.srt_min = not st.srt_min
            st.dirty_srt = True
            schedule_save()

        _srt = {"sync_at": 0.0}

        def sync_rules():
            """The ticks of the Sort rules window into st.rules (when it closes,
            folds or is rebuilt, before a Sort, on stop, and once a second while
            it is open). True when a rule changed."""
            checks = ui["rule_checks"]
            if not checks or not Kit.is_open(ui["srt"]):
                return False
            ticked, rows = {}, set()
            for idx, kind, chk in checks:
                if idx >= st.slots:
                    continue                 # a row of a slot just removed (apply_config)
                rows.add(idx)
                try:
                    on = bool(chk.IsChecked)
                except Exception:
                    on = kind in st.rules.get(idx, NO_RULE)[0]
                if on:
                    ticked.setdefault(idx, set()).add(kind)
            changed = False
            for idx in rows:
                old = st.rules.get(idx)
                graphics = old[1] if old is not None else ()
                kinds = frozenset(ticked.get(idx, ()))
                new = (kinds, graphics) if (kinds or graphics) else None
                if new != old:
                    changed = True
                    if new is None:
                        del st.rules[idx]
                    else:
                        st.rules[idx] = new
            return changed

        def graphics_caption(graphics):
            n = len(graphics)
            return ("+%d graphic%s" % (n, "" if n == 1 else "s")) if n else ""

        def build_rules():
            sync_rules()
            remember_window_pos()
            dispose("srt")
            M, GAP = Kit.MARGIN, Kit.GAP
            w, row_h, h_act, h_foot = 580, 52, 40, 52
            list_h = min(st.slots * row_h + 8, 430)
            h = (M + 30 + M if st.srt_min
                 else M + 30 + GAP + h_act + GAP + list_h + GAP + h_foot + M)
            g, store, y = framed_window("bag_srt", st.srt_x, st.srt_y, w, h, "SORT RULES",
                                        st.srt_min, act(toggle_srt_min), act(close_rules))
            checks = []
            if not st.srt_min:
                IW = w - 2 * M
                Kit.add_section(g, M, y, IW, h_act)
                Kit.art_button(g, store, "sort", Kit.ART_PLAY, M + 12, y + 9, "Sort",
                               "Move the matching items from your backpack and the other slots' "
                               "bags into their bag, one at a time", on_click=act(start_sort))
                Kit.art_button(g, store, "stop", Kit.ART_CLOSE, M + 150, y + 9, "Stop",
                               "Stop sorting (nothing more is moved)", on_click=act(stop_sort, None, True))
                Kit.add_label(g, "Tick what each slot's bag holds.", M + 250, y + 12, Kit.HUE_INFO)
                y += h_act + GAP
                Kit.add_section(g, M, y, IW, list_h)
                sa = G.CreateGumpScrollArea(M + 4, y + 4, IW - 8, list_h - 8)
                inner_w = IW - 8 - 20
                gx = inner_w - 171 - Kit.text_w("+%d graphics" % SORT_GRAPHICS_CAP)
                for idx in range(st.slots):
                    ry = idx * row_h
                    kinds, graphics = st.rules.get(idx, NO_RULE)
                    Kit.add_label(sa, "#%d" % (idx + 1), 6, ry + 5, Kit.HUE_TITLE)
                    if idx in st.assign:
                        Kit.add_label(sa, short(bag_name(st.assign[idx], False), 24), 44, ry + 5)
                    else:
                        Kit.add_label(sa, "No bag in this slot", 44, ry + 5, Kit.HUE_INFO)
                    gl = Kit.add_label(sa, graphics_caption(graphics), gx, ry + 5, Kit.HUE_INFO)
                    if graphics:
                        safe(lambda: gl.SetTooltip(", ".join("0x%04X" % v for v in graphics)))
                    Kit.art_button(sa, store, "add%d" % idx, Kit.ART_PLAY, inner_w - 165, ry + 3,
                                   "Add...", "Target an item; slot #%d's bag then holds its graphic too"
                                   % (idx + 1), on_click=act(add_rule_graphic, idx))
                    Kit.art_button(sa, store, "clr%d" % idx, Kit.ART_CLOSE, inner_w - 80, ry + 3,
                                   "Clear", "Forget the graphics added to slot #%d" % (idx + 1),
                                   on_click=act(clear_rule_graphics, idx))
                    x = 24
                    for key, cap, _gs in SORT_KINDS:
                        chk = Kit.add_check(sa, cap, x, ry + 27, key in kinds,
                                            "Slot #%d's bag holds %s" % (idx + 1, cap.lower()))
                        checks.append((idx, key, chk))
                        x += 36 + Kit.text_w(cap)
                g.Add(sa)
                y += list_h + GAP
                Kit.add_section(g, M, y, IW, h_foot)
                Kit.add_label(g, "Sort moves them from your backpack and the other bags, one every "
                              "%.1f s." % SORT_GAP, M + 12, y + 8, Kit.HUE_INFO)
                Kit.add_label(g, "It stops when you pick something up or a bag is full.",
                              M + 12, y + 28, Kit.HUE_INFO)
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, sub_window_moved))
            ui["srt"] = g
            ui["rule_checks"] = checks
            _srt["sync_at"] = time.time() + 1.0

        def add_rule_graphic(idx):
            API.SysMsg(TITLE + ": target an item; slot #%d's bag will hold its graphic." % (idx + 1),
                       HUE_INFO)
            pick_then(add_rule_graphic_to, idx)

        def add_rule_graphic_to(idx, target):
            if not target:
                API.SysMsg(TITLE + ": cancelled.", HUE_INFO)
                return
            sync_rules()                    # ticks changed while the cursor was up
            if idx >= st.slots:
                return                      # the slot was removed while the cursor was up
            it = get_item(target)
            if not it:
                API.SysMsg(TITLE + ": that isn't an item.", HUE_ERR)
                return
            if safe(lambda: bool(it.IsContainer), False):
                API.SysMsg(TITLE + ": bags aren't sorted; target an item.", HUE_ERR)
                return
            graphic = safe(lambda: int(it.Graphic), 0)
            kinds, graphics = st.rules.get(idx, NO_RULE)
            if not graphic or graphic in graphics:
                API.SysMsg(TITLE + ": slot #%d's bag already holds that." % (idx + 1), HUE_INFO)
                return
            if len(graphics) >= SORT_GRAPHICS_CAP:
                API.SysMsg(TITLE + ": slot #%d already holds %d graphics; click Clear first."
                           % (idx + 1, SORT_GRAPHICS_CAP), HUE_ERR)
                return
            st.rules[idx] = (kinds, graphics + (graphic,))
            st.dirty_srt = True
            save()
            API.SysMsg(TITLE + ": slot #%d's bag holds graphic 0x%04X too." % (idx + 1, graphic),
                       HUE_OK)

        def clear_rule_graphics(idx):
            sync_rules()
            kinds, graphics = st.rules.get(idx, NO_RULE)
            if not graphics:
                return
            if kinds:
                st.rules[idx] = (kinds, ())
            else:
                st.rules.pop(idx, None)
            st.dirty_srt = True
            save()

        # ------------------------------ window upkeep --------------------------------
        def remember_window_pos():
            for key, ax, ay in (("mgr", "mgr_x", "mgr_y"), ("trp", "trp_x", "trp_y"),
                                ("srt", "srt_x", "srt_y")):
                g = ui[key]
                if Kit.is_open(g):
                    setattr(st, ax, safe(lambda: g.GetX(), getattr(st, ax)))
                    setattr(st, ay, safe(lambda: g.GetY(), getattr(st, ay)))

        def upkeep_windows():
            if st.open_flt:
                if st.dirty_flt:
                    st.dirty_flt = False
                    build_filters()
                elif not Kit.is_open(ui.get("flt")):
                    st.open_flt = False
                    ui["flt_checks"] = []
                else:
                    filter_poll()
            if st.open_mgr:
                if st.dirty_mgr:
                    st.dirty_mgr = False
                    build_manager()
                elif not Kit.is_open(ui["mgr"]):
                    st.open_mgr = False
            else:
                st.dirty_mgr = False
            if st.open_trp:
                if st.dirty_trp:
                    st.dirty_trp = False
                    build_traps()
                elif not Kit.is_open(ui["trp"]):
                    st.open_trp = False
                    ui["trap_checks"] = []
            else:
                st.dirty_trp = False
            if st.open_srt:
                if st.dirty_srt:
                    st.dirty_srt = False
                    build_rules()
                elif not Kit.is_open(ui["srt"]):
                    st.open_srt = False
                    ui["rule_checks"] = []
                elif ui["rule_checks"]:
                    now = time.time()
                    if now >= _srt["sync_at"]:           # ticks saved within a second or so
                        _srt["sync_at"] = now + 1.0
                        if sync_rules():
                            schedule_save()
            else:
                st.dirty_srt = False

        def grow_cells():
            """Keep slots exactly the size of the largest open bag's item area (or whole bag when
            untrimmed). Waits a few ticks for the size to settle so layouts don't flicker."""
            mw, mh = H.max_w, H.max_h
            if mw <= 0 or mh <= 0:
                st.fit_seen = None
                return
            want = (min(mw, MAX_CELL), min(mh, MAX_CELL))
            if want == (st.cell_w, st.cell_h):
                st.fit_seen = None
                return
            seen = st.fit_seen
            st.fit_seen = (want, seen[1] + 1 if seen and seen[0] == want else 1)
            if st.fit_seen[1] >= FIT_STABLE_TICKS or st.fit_pending:
                st.fit_pending = False
                st.fit_seen = None
                st.cell_w, st.cell_h = want
                st.dirty_frame = True
                schedule_save()

        def check_hook():
            """While the draw hook isn't being called, the bags are kept in place
            from the script; as soon as it runs again it takes over again. (Was:
            two seconds without a call switched to the script for the rest of the
            session, and a hidden slots window - Paperdoll minimized or folded -
            stopped the old Draw hook, so from then on bags flashed their art
            whenever an item moved.)"""
            if st.drive_fixed or not Kit.is_open(ui["grid"]):
                return
            now = time.time()
            if H.hook_calls != st.hb_frame:
                st.hb_frame = H.hook_calls
                st.hb_time = now
                if st.driving:
                    st.driving = False                # the hook runs again: every frame
                return
            if not st.driving and now - st.hb_time > HOOK_STALL:
                st.driving = True
                if H.hook_calls == 0 and not st.drive_told:
                    st.drive_told = True
                    API.SysMsg(TITLE + ": draw hook isn't being called by this client; keeping bags in "
                               "place from the script instead (bags may flicker briefly when items "
                               "move).", HUE_INFO)

        # ---------------------------------- module -----------------------------------
        def _start():
            if not safe(lambda: API.Player):
                # not in the world yet (the script started with the client): a raised
                # error here would untick the module for good; wait for the player instead
                st.wait_player = True
                st.stopping = False
                return
            st.wait_player = False
            st.stopping = False
            # 2.6.81 (IN1-7): start() runs on the client thread, where no file is read:
            # thread_tick reads the settings file and the next tick starts for real
            # with it (off the client thread, an older host: read in place)
            pre = st.load_text
            st.load_text = None
            if pre is None and safe(lambda: Client.on_client_thread(), False):
                st.wait_load = st.load_wanted = True
                st.to_write = None       # (as below: the file on disk is what loads)
                return
            st.wait_load = st.load_wanted = False
            st.driving = st.drive_fixed = st.drive_told = False    # the draw hook gets a fresh try
            st.job = None
            st.to_write = None       # load() below reads what's on disk
            st.actions = []
            st.reported = False
            st.detached_at = 0.0
            anch["told"] = False
            forget_names()
            st.docked, st.link_state = False, None
            safe(lambda: API.RemoveSharedVar(LINK_CMD))       # ignore a stale command
            _link["wish"] = 0.0
            fitov["cols"], fitov["cell"], fitov["area"], fitov["told"] = None, None, None, None
            shrink["pct"] = shrink["said"] = None
            canvas_leave()                                    # (2.6.78) no canvas, no pins yet
            load_filters()                                    # (2.6.85) per character
            st.canvas = None
            JR["rd"] = safe(lambda: Journal.reader())
            H.meas.clear()
            H.opened = frozenset()
            if not R.tried:
                R.tried = True
                init_interop()
            add_layout = getattr(HOST, "layout_add", None)   # the layout can slot the window
            if add_layout is not None:
                # (2.6.66) "riding": while the grid rides in Paperdoll's window the layout
                # counts it as its zone's occupant but never places it. (2.6.78) With the
                # canvas, Bags alone in a zone is one window exactly its slot ("exact",
                # measured by the layout: "verify"; "state": a folded one is left alone);
                # registered after the client classes are known
                hooks = {"fit": layout_fit, "riding": attached}
                if canvas_ok():
                    hooks.update({"exact": True, "verify": True, "state": layout_state})
                try:                                          # 2.6.55: with the zone fit hook
                    add_layout(KEY, layout_gump, TITLE, hooks)
                except TypeError:                             # an older mother: no hooks
                    safe(lambda: add_layout(KEY, layout_gump, TITLE))
                except Exception:
                    pass
            if R.ok:
                safe(unshrink_left)                           # (2.6.67) a scale left shrunk
            st.sort = None
            SR.update({"armed": False, "lit": {}, "until": 0.0, "counts": {}, "status": None})
            if pre is not None:
                parse_cfg(pre[0])                             # read by thread_tick (2.6.81)
            else:
                load()
            # the Bag Manager, Traps and Sort rules windows come back if they were open
            st.open_mgr = st.dirty_mgr = st.want_mgr
            st.open_trp = st.dirty_trp = st.want_trp
            st.open_srt = st.dirty_srt = st.want_srt
            if dock_wish():
                st.collapsed = True                           # folded into the bar when you left
            link_tick()                                       # tell the Action Bar right away
            H.disabled, H.fail_streak, H.error = False, 0, ""
            if R.ok:
                try:
                    on_main(scan_gumps)           # start() runs on the client thread: in place
                except Exception as e:
                    H.error = "client thread: %s" % e
            else:
                # (the Trim choice is kept: trimming() is False without client access anyway,
                #  and saving it as off would lose the choice for good)
                HOST.refresh_settings(KEY)
                API.SysMsg(TITLE + ": no client access (%s); using basic pinning." % R.error,
                           HUE_ERR)
            publish_layout()
            st.dirty_frame = True
            st.hb_frame, st.hb_time = -1, time.time()
            # what another part (Paperdoll's one-window link) may ask of us
            if hasattr(HOST, "services"):
                HOST.services["bag.attach"] = attach_to
                HOST.services["bag.grid_size"] = lambda: st.grid_wh
                HOST.services["bag.fit"] = paperdoll_fit          # (2.6.57)
                HOST.services["bag.cell"] = bag_cell              # (2.6.58)
                HOST.services["bag.shrink"] = bag_shrink          # (2.6.67)
                HOST.services["bag.pack"] = bag_pack              # (2.6.73)
                HOST.services["bag.open_manager"] = act(open_manager)
                HOST.services["bag.open_traps"] = act(open_traps)
            API.SysMsg(TITLE + ": on, %d slot%s." % (st.slots, "" if st.slots == 1 else "s"), HUE_OK)

        def _tick():
            if st.wait_player:
                # not in the world yet: the window waits (never an error here, which
                # would untick the module for good)
                try:
                    if not API.Player:
                        return
                except Exception:
                    return
                _start()                                  # logged in: start for real
                return
            if st.wait_load:
                # 2.6.81 (IN1-7): the settings file comes from thread_tick; then start
                if st.load_text is not None:
                    _start()
                return
            run_actions()
            if st.stopping:
                return
            link_tick()
            publish_layout()

            if R.ok and H.disabled and not st.reported:
                st.reported = True
                API.SysMsg(TITLE + ": draw hook stopped (%s); using basic pinning." % H.error, HUE_ERR)
                safe(lambda: on_main(restore_all))
                st.dirty_frame = True

            if not Kit.is_open(ui["bar"]) or not Kit.is_open(ui["grid"]):
                st.dirty_frame = True
            if (H.icons or DEFAULT_ICONS) != st.icons_used:
                st.dirty_frame = True     # panel icons follow your bags' own art
            if R.ok and not H.disabled:
                check_hook()
                if st.driving:
                    try:
                        on_main(guarded_tick)
                    except Exception as e:
                        H.error = "client thread: %s" % e
                grow_cells()
                canvas_tick()                   # (2.6.78) the bag canvas, in a zone
            else:
                if st.canvas is not None:
                    # 2.6.81 (IN1-5): the draw hook went off while the canvas was on:
                    # canvas_tick no longer runs, so leave canvas mode here (the canvas
                    # and its pins disposed, the normal window built next)
                    canvas_leave()
                    st.canvas = None
                    H.placed.clear()
                    st.dirty_frame = True
                fallback_tick()
            if st.dirty_frame and not dragging():     # (2.6.85) under a drag: at the drop
                st.dirty_frame = False
                build_frame()
            else:
                if attached():
                    follow_lead()                         # (2.6.66) Paperdoll's window of the moment
                canvas_sync()                             # (2.6.78) a new split: the canvas again

            upkeep_windows()
            job_step()
            now = time.time()
            if not 0 <= st.quick_at - now <= 1.0:
                st.quick_at = now + 1.0
                if ui.get("quick_sig") is not None and ui["quick_sig"] != quick_sig():
                    st.dirty_frame = True
            search_tick(now)                # Find: the box, and lit items going back on time
            sort_tick(now)                  # Sort: one step (the move itself goes from thread_tick)
            canvas_say_tick(now)            # (2.6.78) a single-click name, when drawn from the journal

            if (st.frame_x, st.frame_y) != (st.saved_fx, st.saved_fy) and st.save_in < 0 \
                    and not attached() and st.canvas != "alone" \
                    and now - st.detached_at >= DETACH_SETTLE:
                # (right after parting from Paperdoll the bar is still on its way back
                #  to our own place: that transient position is never saved)
                schedule_save()
            if st.save_in > 0:
                st.save_in -= 1
            elif st.save_in == 0:
                remember_window_pos()
                save()

        def _stop():
            st.stopping = True
            if st.wait_player or st.wait_load:             # never really started: nothing to save
                st.wait_player = st.wait_load = st.load_wanted = False
                st.load_text = None
                return
            safe(stop_job)                                 # (2.6.84) its cursor claim goes too
            st.job = None
            st.actions = []
            st.sort = None                                 # nothing more is moved
            try:
                clear_search(time.time())                  # every lit item back to its own hue
            except Exception:
                pass
            sync_rules()                                   # ticks not yet read: kept (Sort rules
            sync_trap_sel()                                #  and Traps windows left open)
            if hasattr(HOST, "services"):
                for name in ("bag.attach", "bag.grid_size", "bag.open_manager", "bag.open_traps",
                             "bag.fit", "bag.cell", "bag.shrink", "bag.pack"):
                    HOST.services.pop(name, None)
            drop_layout = getattr(HOST, "layout_remove", None)
            if drop_layout is not None:
                safe(lambda: drop_layout(KEY))
            if shrink["pct"] is not None:                  # (2.6.67) your Bag scale back
                safe(lambda: bag_shrink(None, True))
            if st.attach is not None:
                st.attach = None
                st.frame_x, st.frame_y = st.saved_fx, st.saved_fy
            st.grid_wh = None
            st.docked, st.link_state = False, None
            safe(lambda: API.SetSharedVar(LINK_STATE, "off"))
            safe(canvas_leave)                             # (2.6.78) the canvas and every pin go
            st.canvas = None
            if R.ok:
                safe(lambda: on_main(restore_all))
            remember_window_pos()
            save()
            write_saved()          # now: no thread_tick comes after stop
            for key in ("grid", "bar", "mgr", "trp", "srt"):
                dispose(key)
            st.open_mgr = st.open_trp = st.open_srt = False
            ui["side_status"] = None
            ui["trap_checks"] = []
            ui["rule_checks"] = []
            ui["search_box"] = None
            ui["counts"] = []
            st.bar_raw = st.grid_raw = None
            st.grid_info = (None, False)
            st.slot_raws = ()

        def _interval():
            return DRIVE_TICK if st.driving else TICK

        def _thread_tick():
            """Script thread, right after the client tick: Sort's next move (one hop)
            and the settings file. Returns at once when there is nothing to do."""
            if st.load_wanted:
                # 2.6.81 (IN1-7): the file start() asked for; the next client tick applies it
                st.load_wanted = False
                text = read_cfg()
                if st.wait_load and not st.stopping:
                    st.load_text = (text,)
            if st.sort is not None:
                sort_send()
            canvas_thread()                 # (2.6.78) a split too slow for the client tick
            if cats["wanted"] and cats["data"] is None:   # (2.6.85) once: from the tile data
                cats["wanted"] = False
                try:
                    build_cats()
                except Exception:
                    cats["data"] = {}
            write_saved()

        def _thread_wanted():
            """(2.6.82) thread_tick has work: the settings file to read or write,
            Sort's move to send, a split to work out (each is set by a tick)."""
            return bool(st.load_wanted or st.to_write is not None
                        or (st.sort is not None and st.sort["move"] is not None)
                        or CANVAS.get("pending") is not None
                        or (cats["wanted"] and cats["data"] is None))

        load()
        # The tick runs on the client thread, batched with the other modules (no
        # waits anywhere in it: target cursors go through HOST.pick_target, the
        # draw-hook work runs in place); the settings file is written, and Sort's
        # moves sent, from thread_tick on the script's own thread.
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "interval": _interval,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE

    def _part_paperdoll():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  tab.
        # ============================ MODULE START ===================================
        #  MODULE: Paperdoll  (was Character)  -  a Diablo-style paperdoll
        #
        #  Your character in the middle with twenty equipment slots around it, one
        #  per layer: armour down the left, clothes, hands and jewellery down the
        #  right. The doll is drawn by this module from the client's own paperdoll
        #  art (since 2.6.0: the client's paperdoll control stays blank inside a
        #  script window): the body gump for your race and sex in your skin hue,
        #  then every worn layer's paperdoll picture in the order the client
        #  draws them, hair, beard and face included, with the same covering rules
        #  (a robe hides the chest, leg armour hides the pants, ...). Hover a
        #  piece on the doll for its properties, double-click it to use it, drop
        #  an item on the doll to wear it.
        #  Each slot shows the item worn there as the client draws it in a bag, so
        #  it works like one: hover for the item's properties, drag it out to pick
        #  it up (into a bag, on to the ground), double-click to use it. Drop an item
        #  from a bag (or the ground) on any slot to wear it; it goes to the layer it
        #  belongs to, and whatever was worn there goes back to your backpack.
        #  A stats strip under the doll shows Str/Dex/Int, hits, mana, stamina,
        #  weight, gold and followers (2.6.51: no resists or luck; three rows, each
        #  kept inside the strip's box). Weight also shows as a bar against
        #  your maximum (2.6.05): green, yellow from WEIGHT_WARN, red from
        #  WEIGHT_RED, with one alert (Settings > Alerts, "Weight near the limit")
        #  when you cross the red line; it is armed again once you are back under
        #  it. The alert works with the window minimized or the strip off too.
        #
        #  With Bags
        #    When Bags runs too, the two become ONE window, stacked: the
        #    Paperdoll title bar on top, the paperdoll with its slots (and the
        #    stats strip) under it, and Bags' slots (every bag in one grid)
        #    underneath those, so an item can be dragged from a bag straight up on
        #    to the doll and back, Diablo-style. Minimize, the gold arrow and Close
        #    act on the whole thing; Bags' own Slots / Traps buttons move on
        #    to this title bar, and its gem button (bags only) stays at the
        #    bottom right of the bag grid, hiding and showing the bags' side
        #    panel. Turn the combining off on this module's settings page to keep
        #    two separate windows. The settings page can also put the bags BESIDE
        #    the doll instead (right of it, or left with "Bags on the left"); and
        #    when a stacked window would be taller than the screen the bags go
        #    beside the doll by themselves (said once in the journal).
        #
        #  Title bar:  [Slots] [Traps] [Settings] [Fold into bar] [Minimize] [X]
        #    (Slots and Traps only while Bags is combined in.)
        #
        #  In two zones (2.6.66)
        #    In a zone the combined window takes two: the doll (and the stats
        #    strip) in the window's own zone, the bag grid in the zone flush under
        #    it. The mother finds or makes that zone (HOST.layout_pair: the zone
        #    the bags were in when it is under ours, else any window zone under
        #    ours, else one made in the free room under ours or by splitting ours
        #    in two). The window is drawn over both: its own slot on top, the bag
        #    hole where the lower zone is, one stone frame round it all. With no
        #    zone under ours (none can be made) the bags stack under the doll in
        #    the one zone, as in 2.6.58.
        # =============================================================================
        KEY = "character"
        TITLE = "Paperdoll"                   # (was "Character"; the saved keys keep that)

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Character_settings"   # per character: "stats|combine|beside|left" (trailing
        #                                       fields added in 2.6.01; older saves load)
        POS_KEY = "Character_pos"
        MIN_KEY = "Character_min"             # minimized when last seen (Kit.load_min / save_min)
        MINI_W, MINI_H = 240, 46
        TRAY_ICON = 0x1F03                    # robe: item art on the Action Bar's tray button
        SLOT = 48                             # equipment slot, outer size (gold frame included)
        SLOT_GAP = 6
        SLOT_ART = 0x0A3C                     # 9-piece black panel with a gold frame (0x0A3C..0x0A44)
        CAPTION_UP = 16                       # an empty slot's caption sits this far above its bottom edge
        DOLL_W, DOLL_H = 260, 237             # the client's paperdoll art (body + clothes)
        STATS_H = 80                          # the stats strip (three rows: Str/Dex/Int; hits, mana,
        #                                       stamina; weight, its bar, gold and followers)
        STATS_EVERY = 0.5                     # seconds between stat reads
        WEIGHT_WARN = 0.85                    # the weight bar turns yellow at this share of your maximum
        WEIGHT_RED = 0.95                     # ...and red here, with one alert as you cross it
        WEIGHT_BAR_W = 90                     # the bar's width at most (less when the strip is tight)
        WEIGHT_BAR_MIN = 30                   # ...and at least
        WEIGHT_HUE_OK, WEIGHT_HUE_WARN = 0, 0x0035    # hues on the green / yellow line art
        WEIGHT_BG_HUE = 946                   # grey hue on the red line under the bar
        WEIGHT_ALERT_SOUND = 0x04A            # default sound of the alert (lever; the player picks)
        #  Max weight when the client doesn't know it (an older status packet):
        #  RunUO's 40 + 3.5 x Str. Unchecked against the shard.
        WEIGHT_MAX_BASE, WEIGHT_MAX_PER_STR = 40, 3.5
        DOLL_EVERY = 0.25                     # seconds between looks at what is worn (doll AND slots:
        #                                       one look serves both, see look_worn)
        COMBINE_HOLE_GAP = Kit.GAP            # stone between the doll panel and the bag grid
        PAIR_EVERY = 0.5                      # (2.6.66) seconds between looks at the two zones
        SHRINK_STEP = 5                       # (2.6.67) percent per step when the bags are shrunk
        MALE_GUMP_OFFSET, FEMALE_GUMP_OFFSET = 50000, 60000   # client Constants
        SHROUD_ANIM, GARGOYLE_SHROUD = 0x03CA, 0x0223          # a dead gargoyle's shroud draws as 0x0223
        GARGOYLE_BODIES = (0x02B6, 0x02B7)
        # -----------------------------------------------------------------------------

        try:
            import clr
            from System import Array, Object, UInt32, UInt16, Int32, Double, Enum
            from System.Reflection import BindingFlags
            HAVE_CLR = True
        except Exception:
            HAVE_CLR = False

        # Equipment slots: (layer number, API layer name, short caption, tooltip).
        # Left two columns top to bottom, then the right two columns.
        LAYERS = (
            (0x06, "helmet", "Helm", "Head"),
            (0x0D, "torso", "Chest", "Chest armour"),
            (0x13, "arms", "Arms", "Arms"),
            (0x07, "gloves", "Gloves", "Gloves"),
            (0x18, "legs", "Legs", "Leg armour"),
            (0x12, "earrings", "Ears", "Earrings"),
            (0x0A, "neck", "Neck", "Necklace / gorget"),
            (0x11, "tunic", "Tunic", "Tunic / surcoat (over the chest)"),
            (0x0C, "waist", "Belt", "Belt / half apron"),
            (0x03, "shoes", "Feet", "Shoes / boots"),
            (0x05, "shirt", "Shirt", "Shirt"),
            (0x16, "robe", "Robe", "Robe"),
            (0x14, "cloak", "Cloak", "Cloak / quiver"),
            (0x17, "skirt", "Kilt", "Skirt / kilt"),
            (0x04, "pants", "Pants", "Pants"),
            (0x01, "onehanded", "Main", "Main hand (one-handed weapon)"),
            (0x02, "twohanded", "Off", "Off hand (shield, two-handed weapon)"),
            (0x08, "ring", "Ring", "Ring"),
            (0x0E, "bracelet", "Brace", "Bracelet"),
            (0x09, "talisman", "Talis", "Talisman"),
        )
        COLS, ROWS = 4, 5
        LAYER_SET = set(l[0] for l in LAYERS)
        SLOT_LAYERS = tuple(l[0] for l in LAYERS)        # slot order
        # API.FindLayer names the client may spell differently (its Layer enum); each
        # is tried only when the first spelling found nothing, and the one that
        # answered is kept per layer (see find_layer). No extra waits: the tick
        # runs on the client thread.
        LAYER_ALT = {"neck": ("Necklace",), "onehanded": ("OneHanded",),
                     "twohanded": ("TwoHanded",), "earrings": ("Earrings",),
                     "bracelet": ("Bracelet",), "talisman": ("Talisman",)}

        # Paperdoll layers (client Layer enum) and the client's drawing orders
        # (PaperDollInteractable._layerOrder and its quiver / parrot variants).
        L_ONE, L_TWO, L_SHOES, L_PANTS, L_SHIRT, L_HELMET, L_GLOVES, L_RING = 1, 2, 3, 4, 5, 6, 7, 8
        L_TALIS, L_NECK, L_HAIR, L_WAIST, L_TORSO, L_BRACE, L_FACE, L_BEARD = 9, 10, 11, 12, 13, 14, 15, 16
        L_TUNIC, L_EARS, L_ARMS, L_CLOAK, L_ROBE, L_SKIRT, L_LEGS = 17, 18, 19, 20, 22, 23, 24
        API_LAYER_NAME = dict((l[0], l[1]) for l in LAYERS)
        API_LAYER_NAME.update({L_HAIR: "hair", L_BEARD: "beard", L_FACE: "face"})
        ORDER_NORMAL = (L_CLOAK, L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_RING,
                        L_BRACE, L_FACE, L_GLOVES, L_SKIRT, L_ROBE, L_WAIST, L_NECK, L_HAIR, L_BEARD,
                        L_EARS, L_HELMET, L_ONE, L_TWO, L_TALIS)
        ORDER_QUIVER = (L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_RING, L_BRACE,
                        L_FACE, L_GLOVES, L_SKIRT, L_ROBE, L_CLOAK, L_WAIST, L_NECK, L_HAIR, L_BEARD,
                        L_EARS, L_HELMET, L_ONE, L_TWO, L_TALIS)
        ORDER_PARROT = (L_SHIRT, L_PANTS, L_SHOES, L_LEGS, L_ARMS, L_TORSO, L_TUNIC, L_CLOAK, L_RING,
                        L_BRACE, L_FACE, L_GLOVES, L_SKIRT, L_WAIST, L_NECK, L_HAIR, L_BEARD, L_EARS,
                        L_HELMET, L_ONE, L_TWO, L_TALIS, L_ROBE)
        DOLL_LAYERS = tuple(sorted(set(ORDER_NORMAL)))
        ROBES_OPEN = (0x9985, 0x9986, 0xA412, 0xA2CB, 0xA2CA)   # robes that don't cover the chest
        # body graphic -> paperdoll body gump (PaperDollInteractable.UpdateUI), the
        # same table Character HUD > Frames draws its snapshots from: human / elf / gargoyle,
        # alive and ghost, the goblin (0x04E5) and the GM body (0x03DB)
        PAPERDOLL_BODY = {0x0190: 0x000C, 0x0192: 0x000C, 0x0191: 0x000D, 0x0193: 0x000D,
                          0x025D: 0x000E, 0x025F: 0x000E, 0x025E: 0x000F, 0x0260: 0x000F,
                          0x029A: 0x029A, 0x02B6: 0x029A, 0x029B: 0x0299, 0x02B7: 0x0299,
                          0x04E5: 0xC835, 0x03DB: 0x000C}
        FEMALE_BODIES = (0x0191, 0x0193, 0x025E, 0x0260, 0x029B, 0x02B7)
        GM_BODY, GM_BODY_HUE, GM_EXTRA = 0x03DB, 0x03EA, 0xC72B

        # window geometry (full form)
        M = Kit.MARGIN
        PANEL_PAD = 8
        COL_PITCH = SLOT + SLOT_GAP
        DOLL_AREA_H = ROWS * COL_PITCH - SLOT_GAP        # 264: five slot rows
        PANEL_W = PANEL_PAD * 2 + 2 * (2 * SLOT + SLOT_GAP) + 2 * PANEL_PAD + DOLL_W   # 496
        PANEL_H = PANEL_PAD * 2 + DOLL_AREA_H            # 280
        # (2.6.75) in a zone the panel is drawn the zone's shape (wider spreads the
        # slot pairs to its edges, taller spreads the slot rows top to bottom) and
        # the doll fills the middle: the slot pairs and pads take SIDE_OWN of its
        # width, the middle at least DOLL_MIN_OWN (the doll is scaled into it)
        SIDE_OWN = 4 * PANEL_PAD + 2 * (2 * SLOT + SLOT_GAP)   # 236
        DOLL_MIN_OWN = 100
        PANEL_W_MIN = SIDE_OWN + DOLL_MIN_OWN            # 336
        DOLL_FIG = (150, 235)                 # a figure's usual size in the doll art (choose_fit)
        DOLL_INSET = 2                        # px the figure keeps clear of the middle's edges
        BOUNDS_CAP = 300                      # measured pictures kept (outlines of worn art)
        W = PANEL_W + 2 * M                              # 520
        Y_BODY = M + 30 + Kit.GAP                        # 50: under the title section

        settings = {"stats": True, "combine": True,
                    "beside": False,        # bags beside the doll instead of underneath
                    "left": False,          # ...on its left (right when off)
                    "flap": False}          # (2.6.85) the Storage tab went: kept in the saved string
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "sig": None,            # (serial per slot) as last drawn
              "doll_sig": None,       # what the doll wore when it was last drawn
              "stats_at": 0.0,
              "doll_at": 0.0,
              "px": M,                # x of the doll panel inside the window (centred when wider)
              "attached": None,       # the dict shared with Bags while combined
              "beside_said": False,   # told once that the bags went beside the doll (too tall)
              "layer_name": {},       # layer -> the API.FindLayer spelling that answered
              "wait_player": False,
              "saved_min": False,
              "w_armed": True,        # the weight alert is raised when you next cross the red line
              "w_at": 0.0,            # last weight reading for the alert while the strip isn't read
              "wbar": None,           # (fill shown, width) of the weight bar as last set
              # (2.6.57) in a zone: the slot's size, and the doll panel drawn at a scale
              "fit": None,            # (w, h) the layout gave the window, or None (its own size)
              "k": 1.0,               # the doll panel's scale (1.0 = as drawn)
              "py": None,             # top of the doll panel, in its own (unscaled) pixels
              "strip_w": None,        # width of the stats strip (PANEL_W when not fitted)
              # (2.6.71) in a zone the panel fills its width: its own width (PANEL_W
              # when not fitted; wider spreads the slot columns to the panel's edges,
              # the doll in the middle) and the stats as a column beside it (x, y, w,
              # h in window pixels) when that lets the doll be drawn bigger, else None
              "pw": PANEL_W, "col": None,
              # (2.6.75) the panel's own height (PANEL_H when not fitted; taller spreads
              # the slot rows to its top and bottom) and the slot rows' pitch; the stats
              # layout picked
              "ph": PANEL_H, "rp": COL_PITCH, "mode": None,
              # (2.6.66) the two zones: (top rect, bottom rect) as last read, and when
              "pair": None, "pair_at": 0.0,
              # (2.6.67) the room the bag grid has in its zone (w, h) as last laid out,
              # the scale it was told to shrink to (None: its own) and whether the
              # hole had to grow past the zone even so
              "room": None, "room_fs": None, "told_shrink": None, "grew": False,
              # (2.6.66) the Storage tab: the side it is on ("R" / "L"), what Storage
              # was last told (gump, side) or None, and until when Storage is waited for
              "flap_side": "R", "flap_told": None, "flap_wait": 0.0, "flap_fn": None,
              "side_at": 0.0}         # when the side was last checked
        win = {"g": None, "c": {}, "store": ({}, {}), "slots": [], "raw": None, "doll": []}
        page = {"c": None, "store": ({}, {})}

        # ---------- saved settings ----------
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) >= 2:
                settings["stats"] = p[0] == "1"
                settings["combine"] = p[1] == "1"
            if len(p) >= 3:                              # trailing fields (2.6.01)
                settings["beside"] = p[2] == "1"
            if len(p) >= 4:
                settings["left"] = p[3] == "1"
            if len(p) >= 5:                              # (2.6.66) the Storage tab
                settings["flap"] = False            # (2.6.85) tucked in for good
            st["saved_min"] = bool(safe(lambda: Kit.load_min(MIN_KEY), False))

        def save_settings():
            Kit.put_var(SETTINGS_KEY, "|".join(["1" if settings["stats"] else "0",
                                                "1" if settings["combine"] else "0",
                                                "1" if settings["beside"] else "0",
                                                "1" if settings["left"] else "0",
                                                "1" if settings["flap"] else "0"]))

        def save_state():
            Kit.save_min(MIN_KEY, st["minimized"])

        def save_place():
            """Where the window is, the moment it is let go (and in stop)."""
            Kit.save_pos(POS_KEY, win["g"])

        # ------------------------------- client interop -------------------------------
        #  Equipping by drop and the native item controls need the client itself
        #  (IronPython + .NET reflection). Without it the module still shows the
        #  slots (API item pictures), draws the doll from the API's item data and
        #  equips with API.EquipItem.
        class Box(object):
            pass

        R = Box()
        R.tried = R.ok = False
        R.error = ""
        R.m_animid = R.m_covered = R.MobileType = None
        R.cursor = None                   # (2.6.57) the client's GameCursor, found once by reflection
        R.SlotItem = R.DollPiece = None   # (2.6.76 / 2.6.77) see init_interop
        R.m_pixel = R.gumps = None        # (2.6.77) the client's gump pixel test, found once
        R.pixel_n = 0                     # ...and how many arguments it takes (4: with the scale)
        R.f_tiles = R.tiles = None        # (2.6.71) the client's tile data array, found once

        def init_interop():
            if not HAVE_CLR:
                R.error = "clr module unavailable"
                return
            try:
                asm = API.GetType().Assembly
                clr.AddReference(asm)
                # (2.6.57) ClassicUO.Client, GameController and UltimaOnline are
                # internal types, which IronPython can't import ("Cannot import name
                # Client": the paperdoll fell back to pictures only). The cursor is
                # reached through reflection instead: Client.Game.UO.GameCursor (a
                # public type, so its ItemHold reads directly). ItemGump and Control
                # are public and import as before.
                from ClassicUO.Game.UI.Controls import ItemGump, Control
                stat = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                inst = BindingFlags.Instance | BindingFlags.NonPublic
                anyi = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                cli = asm.GetType("ClassicUO.Client")
                R.p_game = cli.GetProperty("Game", stat) if cli is not None else None
                gct = asm.GetType("ClassicUO.GameController")
                R.p_uo = gct.GetProperty("UO", anyi) if gct is not None else None
                uot = asm.GetType("ClassicUO.UltimaOnline")
                R.p_cursor = uot.GetProperty("GameCursor", anyi) if uot is not None else None
                R.ItemGump = ItemGump
                # (2.6.76) a slot's item takes the click anywhere on its picture: the
                # client's ItemGump tests a click against its art at its own size,
                # so art shrunk (or grown) to fit the slot missed most clicks and
                # couldn't be dragged out
                try:
                    class SlotItem(ItemGump):
                        def Contains(self, x, y):
                            return True          # the client has tested its drawn rect first
                    R.SlotItem = SlotItem
                except Exception:
                    R.SlotItem = None
                # (2.6.77) a worn piece on the doll: the same client item control as the
                # slots (its own press-and-drag lifts the item, double-click uses it, its
                # tooltip is the item's), drawing the piece's paperdoll gump art; its
                # click test is the client's gump pixel test at its scale, so only the
                # visible figure takes a press (2.6.76's GumpPicEquipment isn't in every
                # TazUO build, and fell back to plain pictures that can't be lifted)
                try:
                    class DollPiece(ItemGump):
                        def Contains(self, x, y):
                            try:
                                k = self.va_k
                                if R.pixel_n == 4:
                                    a = [UInt32(self.va_gid), Int32(int(x)), Int32(int(y)), Double(k)]
                                else:                # an older build: no scale argument
                                    a = [UInt32(self.va_gid), Int32(int(x / k)), Int32(int(y / k))]
                                return bool(R.m_pixel.Invoke(R.gumps, Array[Object](a)))
                            except Exception:
                                return True      # the client has tested its drawn rect first

                        def OnMouseDown(self, x, y, button):
                            self.va_down = True
                            ItemGump.OnMouseDown(self, x, y, button)

                        def OnMouseUp(self, x, y, button):
                            self.va_down = False
                            ItemGump.OnMouseUp(self, x, y, button)

                        def Update(self):
                            ItemGump.Update(self)
                            if self.va_down:             # (only while pressed: every frame)
                                doll_lifted(self)
                    R.DollPiece = DollPiece
                except Exception:
                    R.DollPiece = None
                ga = asm.GetType("ClassicUO.Game.GameActions")
                R.m_equip = ga.GetMethod("Equip", stat)
                R.m_swap = ga.GetMethod("QueueEquipSwap", stat)
                R.LayerType = asm.GetType("ClassicUO.Game.Data.Layer")
                ctl = clr.GetClrType(Control)
                R.f_bounds = ctl.GetField("_bounds", inst)
                R.Point = clr.GetPythonType(ctl.GetProperty("Location").PropertyType)
                for name in ("m_equip", "m_swap", "LayerType", "f_bounds", "p_game", "p_uo",
                             "p_cursor"):
                    if getattr(R, name) is None:
                        raise Exception("client member not found: " + name)
                R.ok = True
            except Exception as e:
                R.ok = False
                R.error = str(e)
                return
            # (2.6.77) the client's gump pixel test (Client.Game.UO.Gumps.PixelCheck),
            # for the doll pieces' click test
            try:
                game = R.p_game.GetValue(None, None)
                uo = R.p_uo.GetValue(game, None) if game is not None else None
                gp = uo.GetType().GetProperty("Gumps") if uo is not None else None
                R.gumps = gp.GetValue(uo, None) if gp is not None else None
                R.m_pixel, R.pixel_n = None, 0
                if R.gumps is not None:
                    for m in R.gumps.GetType().GetMethods():
                        n = len(m.GetParameters())
                        if m.Name == "PixelCheck" and n in (3, 4) and n > R.pixel_n:
                            R.m_pixel, R.pixel_n = m, n
            except Exception:
                R.gumps = R.m_pixel = None
            if R.m_pixel is None:
                R.DollPiece = None               # no pixel test: plain pictures (a whole-rect
                #                                  piece would take presses meant for others)
            # (2.6.71) the tile data, for the layer of the item on the cursor
            try:
                from System import AppDomain
                for a in AppDomain.CurrentDomain.GetAssemblies():
                    t = a.GetType("ClassicUO.Assets.TileDataLoader")
                    if t is not None:
                        R.f_tiles = t.GetField("_staticData", BindingFlags.Static | BindingFlags.NonPublic)
                        break
            except Exception:
                R.f_tiles = None
            # the client's own paperdoll arithmetic, when it can be reached (else
            # the module's own copy of it is used: see anim_gump / covered)
            try:
                pdi = asm.GetType("ClassicUO.Game.UI.Controls.PaperDollInteractable")
                R.m_animid = pdi.GetMethod("GetAnimID", stat) if pdi is not None else None
                # three parameters upstream (graphic, anim, female); some builds take the
                # item graphic too: the call below is built to match
                R.animid_n = int(R.m_animid.GetParameters().Length) if R.m_animid is not None else 0
            except Exception:
                R.m_animid = None
            try:
                R.MobileType = asm.GetType("ClassicUO.Game.GameObjects.Mobile")
                R.m_covered = (R.MobileType.GetMethod("IsCovered", stat)
                               if R.MobileType is not None else None)
            except Exception:
                R.m_covered = None

        def raw_of(wrapper):
            """The client's own control behind a script control (or None)."""
            if wrapper is None:
                return None
            try:
                v = wrapper.Gump
                if v is not None:
                    return v
            except Exception:
                pass
            return safe(lambda: Kit.client_control(wrapper))

        LAYER_ENUMS = {}                # (2.6.82) layer number -> its client enum value, made once

        def layer_enum(layer):
            e = LAYER_ENUMS.get(layer)
            if e is None:
                e = LAYER_ENUMS[layer] = Enum.ToObject(R.LayerType, layer)
            return e

        WORN_DATA = {}                  # (2.6.82) (serial, graphic) -> (anim, partial hue, container)
        WORN_DATA_CAP = 256

        def world():
            raw = win["raw"]
            return None if raw is None else raw.World

        def player_raw():
            w = world()
            return None if w is None else w.Player

        def held():
            """(serial, wearable, layer) of the item on the cursor, or None. (2.6.71)
            The layer comes from the cursor itself (ItemHold.Layer, else its tile
            data): the client takes a picked-up item out of its item list, so the
            item can't be looked up by its serial while it is held."""
            try:
                cur = R.cursor
                if cur is None:                  # found once: the cursor object never changes
                    game = R.p_game.GetValue(None, None)
                    uo = R.p_uo.GetValue(game, None) if game is not None else None
                    cur = R.cursor = R.p_cursor.GetValue(uo, None) if uo is not None else None
                h = cur.ItemHold
                if h.Enabled and not h.IsFixedPosition:
                    # where it is worn: the tile data of what is held (the cursor's
                    # own Layer is only set for an item taken off the body)
                    layer = tile_layer(int(h.Graphic))
                    if layer not in LAYER_SET:
                        try:
                            layer = int(h.Layer)
                        except Exception:
                            layer = 0
                    return int(h.Serial), bool(h.IsWearable), layer
            except Exception:
                pass
            return None

        def doll_lifted(piece):
            """(2.6.85) A doll piece draws gump art, so the client lifts it as a gump:
            the cursor then looks for a gump numbered from the item's graphic (often
            none: nothing under the cursor) and centres on the whole figure's art (it
            lands far off). Straight after the lift, on the same frame, the cursor is
            told it holds plain item art, centred on the mouse: as a lift from a bag."""
            try:
                cur = R.cursor
                if cur is None:
                    game = R.p_game.GetValue(None, None)
                    uo = R.p_uo.GetValue(game, None) if game is not None else None
                    cur = R.cursor = R.p_cursor.GetValue(uo, None) if uo is not None else None
                h = cur.ItemHold
                if h.Enabled and int(h.Serial) == int(piece.LocalSerial):
                    piece.va_down = False
                    h.IsGumpTexture = False
                    h.MouseOffset = R.Point(0, 0)
            except Exception:
                piece.va_down = False

        def tile_layer(graphic):
            """(2.6.71) The layer an item graphic is worn on, from the client's tile
            data (TileDataLoader._staticData, a plain static array: no by-ref
            property to read), or 0 when it can't be read."""
            try:
                arr = R.tiles
                if arr is None:
                    if R.f_tiles is None:
                        return 0
                    arr = R.tiles = R.f_tiles.GetValue(None)
                if arr is None or graphic < 0 or graphic >= arr.Length:
                    return 0
                return int(arr[graphic].Layer)
            except Exception:
                return 0

        def set_pos(c, x, y):
            c.Location = R.Point(x, y)

        def size_of(c):
            r = R.f_bounds.GetValue(c)
            return int(r.Width), int(r.Height)

        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        BLOCK_W = 2 * SLOT + SLOT_GAP                    # one side's two slot columns

        def slot_xy(i):
            """Top-left of slot i inside the window (left columns 0-1, right 2-3).
            (2.6.71) The left pair keeps to the panel's left edge and the right
            pair to its right edge, so a panel drawn wider (st["pw"]) spreads
            them out instead of leaving stone either side."""
            col, row = divmod(i, ROWS)
            if col < 2:
                x = st["px"] + PANEL_PAD + col * COL_PITCH
            else:
                x = st["px"] + st["pw"] - PANEL_PAD - BLOCK_W + (col - 2) * COL_PITCH
            # (2.6.75) a taller panel spreads the rows (pitch st["rp"]) top to bottom
            return x, panel_y() + PANEL_PAD + int(round(row * st["rp"]))

        def zoned_lock():
            """(2.6.72) The window is held in its zone (no drag by its body)."""
            return bool(safe(lambda: HOST.layout_locked(KEY), False))

        def mid_rect():
            """(2.6.75) The middle of the doll panel, between the two slot pairs and
            the panel's pads, in its own pixels (x, y, w, h): the doll fills it."""
            x = st["px"] + 2 * PANEL_PAD + BLOCK_W
            return (x, panel_y() + PANEL_PAD, max(1, st["pw"] - SIDE_OWN),
                    max(1, st["ph"] - 2 * PANEL_PAD))

        def panel_y():
            """Top of the doll panel in its own pixels (2.6.57: in a zone the panel
            is drawn at st["k"] and placed by its own coordinates / k)."""
            py = st["py"]
            return Y_BODY if py is None else py

        # ---------- in a zone (2.6.57) ----------
        #  The layout tells the window its slot (layout_fit, hooks "fit" + "exact")
        #  and the window is drawn exactly that size: the title row across it, the
        #  doll and its two slot columns scaled AS ONE PIECE (the client's own
        #  control scaling, the doll's aspect kept, the drop targets scaled with
        #  them) and centred in their share, the stats strip at the share's width,
        #  and with Bags combined, the bag grid filling the rest (told its room
        #  through bag.fit). Freed, it is drawn at its own size again.
        FIT_K_MIN, FIT_K_MAX = 0.4, 2.0          # how far the doll panel is scaled
        STRIP_MIN_W = 300                        # a stats strip narrower than this is left out

        def layout_fit(w, h, mode):
            """The layout's "fit" hook: the window's slot is w x h (None: freed).
            Client thread, the keeper's pass: only records and asks for a rebuild."""
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != st["fit"]:
                st["fit"] = new
                st["pair"] = pair_rects() if new is not None else None   # (2.6.66) the two zones
                st["pair_at"] = time.time()
                queue("redraw")()

        # ---------- the two zones (2.6.66) ----------
        def pair_rects():
            """(top rect, bottom rect) of the window's zone and the zone flush under
            it for the bags (the mother finds or makes it), or None: not in a zone,
            not combined, or no zone under ours can be made (the bags then stack
            under the doll in the one zone)."""
            fn = getattr(HOST, "layout_pair", None)
            if fn is None or st["attached"] is None:
                return None
            try:
                pr = fn(KEY, "bag")
            except Exception:
                return None
            if not pr or pr[0] is None or pr[1] is None:
                return None
            return (tuple(int(v) for v in pr[0]), tuple(int(v) for v in pr[1]))

        def pair_hole(x, y, fw, fh, pr):
            """The bag hole (window pixels) for a window at (x, y) whose slot is
            fw x fh with the zones pr under it: the lower zone's rect, M in from
            the sides and the bottom, a half gap under the slot; taller when the
            grid needs more rows (never past the screen's bottom). None when the
            lower zone isn't flush under this window's slot."""
            (tx, ty, tw, th), (bx, by, bw, bh) = pr
            if abs((y + fh) - by) > 2 * SNAP_DIST:
                return None
            hx0, hx1 = max(0, bx - x), min(fw, bx + bw - x)
            hw = hx1 - hx0 - 2 * M
            if hw < 40:
                return None
            half = COMBINE_HOLE_GAP // 2
            hy = fh + half
            hh = (by + bh - y) - hy - M
            if hh < 20:
                return None
            # (2.6.67) the hole is the lower zone: a grid with more rows than it
            # holds is shown smaller until it fits (fit_scale), never let run down
            # over the next zone (the journal there would cover the bags). Only
            # when even the smallest scale can't fit does the hole grow, and never
            # past the screen's bottom
            st["room"] = (hw, hh)
            fs = fit_scale(hw, hh)
            st["room_fs"] = fs
            need = fs[1] if fs is not None else grid_need(hw)
            st["grew"] = need > hh
            if need > hh:
                try:
                    sh = int(Kit.screen()[1])
                except Exception:
                    sh = 0
                cap = (sh - y - M - hy) if sh > 0 else need
                hh = max(hh, min(need, cap))
            return (hx0 + M, hy, hw, hh)

        def scale_ctrl(c, raw=False, flushed=False):
            """Draw control c (a script control, or a client one when raw) at the
            doll panel's scale: place, size and mouse area (the client's own
            control scaling). Nothing when not scaled."""
            k = st["k"]
            if abs(k - 1.0) < 0.001 or c is None:
                return
            try:
                if not raw and not flushed:
                    Kit.flush()                  # its queued SetPos / SetRect land first
                rc = c if raw else Kit.client_control(c)
                if rc is None:
                    return
                if str(rc.GetType().Name) == "GumpPicTiled":
                    rc.ScaleTiledTexture = True
                rc.ApplyScale(k, True, True, False)
            except Exception:
                pass

        def cell_info():
            """(2.6.67) Bags' cells as they would be at your own Bag scale (bag.cell
            measures them at the scale of now, which may be shrunk): (cell w,
            cell h, gap, slots, side panel width, your scale, the least scale),
            or None when Bags can't tell yet."""
            fn = bag_service("bag.cell")
            if fn is None:
                return None
            try:
                v = fn()
                cw, ch, gap, n, side = v[0], v[1], v[2], v[3], v[4]
                cur, own, floor = (v[5], v[6], v[7]) if len(v) >= 8 else (100, 100, 100)
            except Exception:
                return None
            if n <= 0 or cw <= 0 or ch <= 0 or cur <= 0 or own <= 0:
                return None
            if cur != own:
                cw, ch = cw * own / float(cur), ch * own / float(cur)
            return cw, ch, gap, n, side, own, min(floor, own)

        def need_at(ci, f, width):
            """(rows, height) of the grid across `width` with its cells at f of
            their size at your scale (as many columns as fit, at least one)."""
            cw0, ch0, gap, n, side = ci[0], ci[1], ci[2], ci[3], ci[4]
            cw = int(math.ceil(cw0 * f - 0.01))
            ch = int(math.ceil(ch0 * f - 0.01))
            aw = max(cw, width - side)
            cols = max(1, min(n, (aw + gap) // (cw + gap)))
            rows = int(math.ceil(n / float(cols)))
            return rows, rows * ch + (rows - 1) * gap, cw + side

        def grid_need(width):
            """(2.6.58) The least height the combined bag grid needs across `width`:
            as many columns of the bags' own cell width as fit (Bags tells its cell
            size and gap, bag.cell), its rows at their own height. (2.6.67) At your
            own Bag scale, whatever it is shrunk to now, so the layout never chases
            its own shrinking."""
            fn = bag_service("bag.pack")          # (2.6.73) the bags packed: their own sums
            if fn is not None:
                try:
                    got = fn(width, 1 << 20)
                except Exception:
                    got = None
                if got is not None:
                    return got[1]
            ci = cell_info()
            if ci is None:
                return 120                        # not known yet: a third of a zone or so
            return need_at(ci, 1.0, width)[1]

        def fit_scale(hw, hh):
            """(2.6.67) (pct, need): the container scale the bag grid fits hw x hh
            at (None: your own, it fits as it is; else the biggest step down that
            fits, never under the least Bags allows) and the height it needs
            there. A step back up needs a few pixels to spare per row, so a grid
            on the edge doesn't flip between two scales. None when Bags can't
            tell."""
            fn = bag_service("bag.pack")          # (2.6.73) the bags packed: their own sums
            if fn is not None:
                try:
                    got = fn(hw, hh)
                except Exception:
                    got = None
                if got is not None:
                    return got
            ci = cell_info()
            if ci is None:
                return None
            own, floor = ci[5], ci[6]
            told = st["told_shrink"]
            p = own
            while True:
                rows, need, wneed = need_at(ci, p / float(own), hw)
                spare = 3 * rows if (told is not None and p > told) else 0
                if (need + spare <= hh and wneed <= hw) or p <= floor:
                    return (None if p >= own else p), need
                p = max(floor, p - SHRINK_STEP)

        COL_ROWS = 10                            # (2.6.71) the stats column's text rows
        COL_PITCH_MIN, COL_PITCH_MAX = 20, 26    # ...their pitch
        COL_BAR_H = 14                           # ...and the weight bar's row under Weight
        COL_NEED_H = 2 * 8 + COL_ROWS * COL_PITCH_MIN + COL_BAR_H
        geo = {"col_w": None,
               "bounds": {}}      # (2.6.75) gump id -> its opaque outline (x0, y0, x1, y1) or None

        def col_w():
            """Width of the stats column: its widest line at its biggest numbers."""
            if geo["col_w"] is None:
                widest = 0
                for t in ("Stamina 999/999", "Followers 99/99", "Gold 9,999,999",
                          "Weight 0000/0000", "Mana 999/999", "HP 999/999"):
                    widest = max(widest, Kit.text_w(t))
                geo["col_w"] = max(WEIGHT_BAR_MIN, widest) + 2 * STATS_IN + 4
            return geo["col_w"]

        def choose_fit(bw, room):
            """(2.6.75) (mode, aw, ah, k) for a fitted window whose body is bw wide
            with room px of height for the panel (and the stats): where the stats
            go ("strip" under the panel, "col" beside it, "none"), the panel's
            rect aw x ah (window px) and the slots' scale k. The panel is drawn
            that exact shape, so the pick is the layout that shows a usual figure
            (DOLL_FIG) biggest; ties go to the bigger slots. (2.6.76) The pick
            depends on the zone alone, never on what you wear (a wide figure
            flipped 2.6.75's layout): the figure goes behind the slots instead."""
            fig = DOLL_FIG
            cands = []
            if settings["stats"]:
                if bw >= STRIP_MIN_W:
                    cands.append(("strip", bw, room - STATS_H - Kit.GAP))
                cands.append(("col", bw - col_w() - Kit.GAP, room))
            else:
                cands.append(("none", bw, room))
            fw_, fh_ = float(max(1, fig[0])), float(max(1, fig[1]))
            best = None
            for mode, aw, ah in cands:
                if mode == "col" and ah < COL_NEED_H:
                    continue                      # the column wouldn't fit beside the doll
                k = min(aw / float(PANEL_W_MIN), ah / float(PANEL_H), FIT_K_MAX)
                if k < FIT_K_MIN:
                    continue
                f = min((aw - 2 * PANEL_PAD * k) / fw_, (ah - 2 * PANEL_PAD * k) / fh_)
                if best is None or f > best[0] + 0.001 or (f > best[0] - 0.001 and k > best[4]):
                    best = (f, mode, aw, ah, k)
            if best is None:                      # no room for the stats: the doll alone
                k = min(bw / float(PANEL_W_MIN), room / float(PANEL_H), FIT_K_MAX)
                return "none", bw, room, max(FIT_K_MIN, k)
            return best[1], best[2], best[3], best[4]

        def fitted_geom(fw, fh, combined):
            """(k, px, py, ys, strip_w, hole, sxy, pw, col, ph) of a window fitted
            to fw x fh: the slots' scale, the doll panel's place in its own pixels
            (px, py: drawn there, then scaled), the stats strip's top (window
            pixels, None: no strip), its width, the hole for the bag grid (None
            when not combined), the strip's (left, panel bottom), the panel's own
            width, the stats column (x, y, w, h) or None, and the panel's own
            height. (2.6.75) The panel fills its share of the zone both ways (no
            stone above, below or beside it): drawn in its own pixels at the
            share's shape, the slot pairs out at its sides and the slot rows
            spread top to bottom, the doll filling the middle (draw_doll)."""
            bx, by = M, Y_BODY
            bw, bh = max(1, fw - 2 * M), max(1, fh - Y_BODY - M)
            gap = COMBINE_HOLE_GAP
            # (2.6.58) combined: the bag grid's rows at the bags' own cell height
            # are taken first, the doll panel fills what is left
            room = (bh - grid_need(bw) - gap) if combined else bh
            mode, aw, ah, k = choose_fit(bw, room)
            st["mode"] = mode
            pw = max(PANEL_W_MIN, int(round(aw / k)))
            ph = max(PANEL_H, int(round(ah / k)))
            ppw, pph = int(round(pw * k)), int(round(ph * k))
            sh = (STATS_H + Kit.GAP) if mode == "strip" else 0
            top, left = by, bx
            if combined:
                used = max(room, pph + sh)
                hole = (bx, by + used + gap, bw, max(1, bh - used - gap))
            else:
                hole = None
            ys = (top + pph + Kit.GAP) if mode == "strip" else None
            strip_w = bw if mode == "strip" else None
            col = (bx + bw - col_w(), top, col_w(), pph) if mode == "col" else None
            return (k, int(round(left / k)), int(round(top / k)), ys, strip_w, hole, (bx, top + pph),
                    pw, col, ph)

        def body_h():
            h = PANEL_H
            if settings["stats"]:
                h += Kit.GAP + STATS_H
            return h

        # ---------- the combined window's geometry ----------
        #  (w, h, px, hole): the window size, where the doll panel starts and the
        #  rectangle the bag grid shows through. Stacked (bags under the doll) by
        #  default; beside the doll when asked on the settings page, or when the
        #  stacked window would be taller than the screen.
        def stacked_geom(gw, gh):
            iw = max(PANEL_W, gw)
            w = iw + 2 * M
            px = M + (iw - PANEL_W) // 2
            yh = Y_BODY + body_h() + COMBINE_HOLE_GAP
            hole = (M + (iw - gw) // 2, yh, gw, gh)
            return w, yh + gh + M, px, hole

        def beside_geom(gw, gh):
            w = M + PANEL_W + COMBINE_HOLE_GAP + gw + M
            if settings["left"]:
                hx, px = M, M + gw + COMBINE_HOLE_GAP
            else:
                hx, px = M + PANEL_W + COMBINE_HOLE_GAP, M
            return w, Y_BODY + max(body_h(), gh) + M, px, (hx, Y_BODY, gw, gh)

        def combined_geom(gw, gh):
            if not settings["beside"]:
                w, h, px, hole = stacked_geom(gw, gh)
                try:
                    sh = int(Kit.screen()[1])
                except Exception:
                    sh = 0
                if sh <= 0 or h <= sh:
                    return w, h, px, hole
                if not st["beside_said"]:                # too tall to stack: beside, said once
                    st["beside_said"] = True
                    API.SysMsg(TITLE + ": the bag grid is too tall to stack under the doll on "
                               "this screen; the bags go beside it instead.", Kit.HUE_INFO)
            return beside_geom(gw, gh)

        def hole_guess():
            """Where the bag grid will go, before Bags has said how big it is
            (so its slots are not drawn over the title bar for a tick)."""
            if settings["beside"]:
                return (M, Y_BODY) if settings["left"] else (M + PANEL_W + COMBINE_HOLE_GAP, Y_BODY)
            return M, Y_BODY + body_h() + COMBINE_HOLE_GAP

        def frame_with_hole(g, w, h, hole):
            """The stone frame, painted round a hole (the bag grid shows through)."""
            hx, hy, hw, hh = hole
            base = Kit.WINDOW_BG
            s = [Kit.pic_size(base + i) for i in range(9)]
            tl, t, tr, l, c, r, bl, b, br = s
            parts = []                                   # (2.6.72) noted as the window's frame
            for rx, ry, rw, rh in ((0, 0, w, hy), (0, hy, hx, h - hy),
                                   (hx + hw, hy, w - hx - hw, h - hy),
                                   (hx, hy + hh, hw, h - hy - hh)):
                if rw > 0 and rh > 0:
                    parts.append(Kit.add_tiled(g, base + 4, rx, ry, rw, rh))
            if all(p[0] > 0 and p[1] > 0 for p in s):
                parts += [Kit.add_tiled(g, base + 1, tl[0], 0, w - tl[0] - tr[0], t[1]),
                          Kit.add_tiled(g, base + 7, bl[0], h - b[1], w - bl[0] - br[0], b[1]),
                          Kit.add_tiled(g, base + 3, 0, tl[1], l[0], h - tl[1] - bl[1]),
                          Kit.add_tiled(g, base + 5, w - r[0], tr[1], r[0], h - tr[1] - br[1]),
                          Kit.add_pic(g, base + 0, 0, 0),
                          Kit.add_pic(g, base + 2, w - tr[0], 0),
                          Kit.add_pic(g, base + 6, 0, h - bl[1]),
                          Kit.add_pic(g, base + 8, w - br[0], h - br[1])]
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch and Kit.CORNER_ART:
                for cx, cy in ((0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)):
                    # a knot is left out where it would sit on the bag grid
                    if cx < hx + hw and cx + cw > hx and cy < hy + hh and cy + ch > hy:
                        continue
                    parts.append(Kit.add_pic(g, Kit.CORNER_ART, cx, cy))
            # (2.6.72) "Join zone windows in one frame" hides these like any Kit frame
            try:
                Kit._frame_parts[g] = [p for p in parts if p is not None]
            except Exception:
                pass

        def build_window():
            old, win["g"] = win["g"], None
            clear_slots()
            store = ({}, {})
            c = {}
            slots = []
            att = st["attached"]
            hole = None
            st["px"] = M
            st["k"], st["py"], st["strip_w"] = 1.0, None, None
            st["pw"], st["col"] = PANEL_W, None
            st["ph"], st["rp"], st["mode"] = PANEL_H, COL_PITCH, None
            fit = st["fit"] if not st["minimized"] else None
            spx = M                                      # the stats strip's left edge
            # where it sits (2.6.66: read first, the two-zone hole is laid out from it)
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            else:
                x, y = Kit.load_pos(POS_KEY, (200, 120), (W, Y_BODY + body_h() + M))
            if st["minimized"]:
                w, h = MINI_W, MINI_H
                g = G.CreateGump(True, True)
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
                if att is not None:
                    Kit.set_text(c["status"], TITLE + " & bags")
                else:
                    Kit.set_text(c["status"], TITLE)
            else:
                w, h = W, Y_BODY + body_h() + M
                # the window itself takes no mouse: the hole for the bag grid must
                # let clicks and dropped items through to Bags' slots
                g = G.CreateGump(False, True)
                if fit is not None:
                    # (2.6.57) in a zone: exactly the slot, the doll panel scaled in it
                    w, h = fit
                    hole2 = pair_hole(x, y, w, h, st["pair"]) if (att is not None
                                                                   and st["pair"]) else None
                    if hole2 is not None:
                        # (2.6.66) two zones: the doll in the slot, the bags in the
                        # zone under it; the window reaches over both
                        half = COMBINE_HOLE_GAP // 2
                        (k, st["px"], st["py"], ys_fit, st["strip_w"], _h, sxy, st["pw"],
                         st["col"], st["ph"]) = fitted_geom(w, h - half + M, False)
                        hole = hole2
                        h = hole[1] + hole[3] + M
                    else:
                        (k, st["px"], st["py"], ys_fit, st["strip_w"], hole, sxy, st["pw"],
                         st["col"], st["ph"]) = fitted_geom(w, h, att is not None)
                    st["k"] = k
                    # (2.6.75) the five slot rows spread over the panel's own height
                    st["rp"] = (st["ph"] - 2 * PANEL_PAD - SLOT) / float(ROWS - 1)
                    spx = sxy[0]
                    if hole is not None:
                        frame_with_hole(g, w, h, hole)
                        att["dx"], att["dy"] = hole[0], hole[1]
                        if hole2 is None:                 # (2.6.67) one zone: its hole is the room
                            st["room"] = (hole[2], hole[3])
                            st["room_fs"] = fit_scale(hole[2], hole[3])
                            st["grew"] = (st["room_fs"] is not None
                                          and st["room_fs"][1] > hole[3])
                        tell_bags((hole[2], hole[3]))     # the grid fills the hole edge to edge
                        fs = st["room_fs"]
                        tell_shrink(fs[0] if fs is not None else None)   # (2.6.67) small enough
                    else:
                        Kit.add_window_frame(g, w, h)
                        tell_bags(None)
                elif att is not None and att.get("grid_wh"):
                    # combined: the doll panel (and stats) with the bag grid under it
                    # (or beside it), the frame painted round the grid's hole
                    gw, gh = att["grid_wh"]
                    w, h, st["px"], hole = combined_geom(int(gw), int(gh))
                    frame_with_hole(g, w, h, hole)
                    att["dx"], att["dy"] = hole[0], hole[1]
                else:
                    Kit.add_window_frame(g, w, h)
                if fit is None:
                    tell_bags(None)                      # (2.6.57) the grid at its own size
                px = st["px"]
                extra = None
                if att is not None:          # Bags' own buttons live here now (2.6.78: in the
                    #                          title row's fit, Kit.title_bar's extra)
                    extra = [("traps", Kit.ART_PAGE, "Traps", "Open the trap bags window: tick the "
                              "bags Trap and Untrap cast on", queue("bag_traps")),
                             ("bags", Kit.ART_PAGE, "Slots", "Open the bag manager window: put a "
                              "bag in each slot", queue("bag_mgr"))]
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), extra=extra)
                # the paperdoll panel: a catcher under everything so clicks on the
                # panel stay in the window and an item let go off a slot stays on
                # the cursor; it also drags the window
                # (2.6.58) the panel's own controls, listed as they are made, are what
                # is scaled in a zone (2.6.57 counted the window's children, which
                # could take in the stone frame too)
                body = []
                py = panel_y()
                pw, ph = st["pw"], st["ph"]
                body.append(Kit.add_section(g, px, py, pw, ph))
                # (2.6.72) no tooltip: it showed over the stats and the worn items (the
                # title strip drags the window and says so)
                body.append(Kit.catcher(g, px, py, pw, ph, lambda *a: None,
                                        None, movable=not zoned_lock()))
                # (2.6.75) the doll's background and drop area are the whole middle
                mx, my, mw, mh = mid_rect()
                c["doll_bg"] = Kit.add_tiled(g, 0x243A, mx, my, mw, mh, 0.35)
                body.append(c["doll_bg"])
                # dropped on the doll's background: wear it
                c["doll_drop"] = Kit.catcher(g, mx, my, mw, mh, queue(("drop", 0)),
                                             "Drop an item here to wear it", movable=True)
                body.append(c["doll_drop"])
                for i, (layer, name, cap, tip) in enumerate(LAYERS):
                    sx, sy = slot_xy(i)
                    body.extend(Kit.add_resizepic(g, SLOT_ART, sx, sy, SLOT, SLOT, mouse=False) or [])
                    # the slot's drop target (and its tooltip while empty)
                    drop = G.CreateGumpColorBox(0.01, "#000000")
                    drop.SetRect(sx, sy, SLOT, SLOT)
                    Kit.on_click(drop, queue(("drop", layer)))
                    stip = tip + ": drop an item here to wear it"
                    safe(lambda: drop.SetTooltip(stip))
                    g.Add(drop)
                    # the caption along the slot's bottom edge, clear of where a dropped
                    # item's picture (and its tooltip) lands
                    lbl = Kit.add_label(g, cap, sx + (SLOT - Kit.text_w(cap)) // 2,
                                        sy + SLOT - CAPTION_UP, Kit.HUE_TEXT)   # (2.6.72) readable
                    safe(lambda: lbl.SetAcceptMouseInput(False))
                    body.append(drop)
                    body.append(lbl)
                    slots.append({"layer": layer, "name": name, "x": sx, "y": sy, "drop": drop,
                                  "label": lbl, "serial": 0, "ctrl": None, "raw": None,
                                  "tip": stip})
                scale_body(body)                         # (2.6.57) drawn at st["k"] in a zone
                if fit is not None:
                    ys, spw, sx0 = ys_fit, st["strip_w"], spx
                else:
                    ys = (Y_BODY + PANEL_H + Kit.GAP) if settings["stats"] else None
                    spw, sx0 = PANEL_W, px
                if ys is not None:
                    Kit.add_section(g, sx0, ys, spw, STATS_H)
                    Kit.catcher(g, sx0, ys, spw, STATS_H, lambda *a: None, None,
                                movable=not zoned_lock())
                    c["stats1"] = Kit.add_label(g, "", sx0 + 10, ys + 8, Kit.HUE_TEXT)
                    c["stats2"] = Kit.add_label(g, "", sx0 + 10, ys + 32, Kit.HUE_TEXT)
                    # line 3: "Weight w/max", the weight bar, then gold / followers
                    c["stats3"] = Kit.add_label(g, "", sx0 + 10, ys + 56, Kit.HUE_TEXT)
                    build_weight_bar(g, c, sx0, ys + 56)
                elif st["col"] is not None:             # (2.6.71) the stats beside the doll
                    build_stats_col(g, c, st["col"])
            Kit.place(g, x, y, w, h)                     # wholly on screen (window rule 1)
            if zoned_lock():
                safe(lambda: setattr(g, "CanMove", False))   # 2.6.81 (IN2-3): held in its zone
            win.update({"g": g, "c": c, "store": store, "slots": slots})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_place))    # remembered the moment it is let go
            win["raw"] = raw_of(g) if R.ok else None
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            if att is not None:
                att["g"], att["raw"] = g, None
                att["shown"] = not st["minimized"]
                att["state"] = dock_state()
            st["sig"] = None                             # draw the slots on the next tick
            st["doll_sig"] = None                        # and the doll
            st["stats_at"] = 0.0
            st["stats_key"] = None                       # (2.6.82) the stats written afresh
            st["doll_at"] = 0.0
            st["wbar"] = None                            # and the weight bar (new controls)
            Kit.dispose(old)

        def tell_bags(room):
            """(2.6.57) Tell the combined bag grid the room it fills (w, h), or None
            for its own size; only when that changes (Bags then redraws)."""
            if room is None:
                st["room"] = None
                tell_shrink(None)                    # (2.6.67) your Bag scale again
            if room == st.get("told_bags"):
                return
            st["told_bags"] = room
            fn = bag_service("bag.fit")
            if fn is not None:
                if room is None:
                    safe(lambda: fn(None, None))
                else:
                    safe(lambda: fn(room[0], room[1]))

        def tell_shrink(pct):
            """(2.6.67) Tell Bags the scale its grid is shown at so it fits its zone
            (None: your own); only when that changes."""
            if pct == st["told_shrink"]:
                return
            st["told_shrink"] = pct
            fn = bag_service("bag.shrink")
            if fn is not None:
                safe(lambda: fn(pct))

        def scale_body(ctrls):
            """The doll panel's controls drawn at its scale (one flush first, so
            their queued places land before they are scaled)."""
            if abs(st["k"] - 1.0) < 0.001:
                return
            Kit.flush()
            for ctl in ctrls:
                if ctl is not None:
                    scale_ctrl(ctl, flushed=True)

        def clear_slots():
            for s in win["slots"]:
                if s["ctrl"] is not None:
                    Kit.dispose(s["ctrl"])
                    s["ctrl"] = None
            win["slots"] = []
            clear_doll()

        def clear_doll():
            for p in win["doll"]:
                Kit.dispose(p)
            win["doll"] = []

        def dock_state():
            return "docked" if st["docked"] else ("collapsed" if st["minimized"] else "open")

        # ---------- the doll ----------
        #  What the client's PaperDollInteractable does, done here with gump pics:
        #  the body gump, then each worn layer's paperdoll art in the client's
        #  order, skipping the layers another piece covers.
        def find_layer(name):
            """API.FindLayer(name), trying the client's other spellings of the layer
            when the first finds nothing (the one that answered is kept). Runs on
            the client thread, so each try is in place, never a wait."""
            known = st["layer_name"].get(name)
            if known is not None:
                try:
                    return API.FindLayer(known)
                except Exception:
                    return None
            for spelling in (name,) + LAYER_ALT.get(name, ()):
                try:
                    it = API.FindLayer(spelling)
                except Exception:
                    it = None
                if it:
                    st["layer_name"][name] = spelling
                    return it
            return None

        def item_data_api(serial):
            """The item's tile data through the API (what Character HUD > Frames reads)."""
            try:
                return API.FindItem(serial).GetItemData()
            except Exception:
                return None

        def worn(p, keep=None):
            """{layer: (serial, graphic, hue, anim id, partial hue, is container)}
            for every paperdoll layer that has an item, and (player graphic,
            player hue, female). `p` is the client's own player (taken once per
            look) or None; a failure in the raw branch falls through to the API.
            keep: (2.6.82) a dict that gets {layer: the client's Item} of the raw
            branch, for refresh_slots in the same look. The tile data of a worn
            item (a by-value copy of its whole record) is read once per (serial,
            graphic): it is the graphic's, it never changes."""
            out = {}
            if R.ok and p is not None:
                try:
                    wd = WORN_DATA
                    for layer in DOLL_LAYERS:
                        it = p.FindItemByLayer(layer_enum(layer))
                        if it is None:
                            continue
                        serial, graphic, hue = int(it.Serial), int(it.Graphic), int(it.Hue)
                        if keep is not None:
                            keep[layer] = it
                        k = (serial, graphic)
                        dat = wd.get(k)
                        if dat is not None:
                            out[layer] = (serial, graphic, hue) + dat
                            continue
                        try:
                            d = it.ItemData          # a ref-returning property: not every build reads it
                            dat = (int(d.AnimID), bool(d.IsPartialHue), bool(d.IsContainer))
                        except Exception:
                            d = item_data_api(serial)
                            if d is not None:
                                dat = (int(d.AnimID or 0), bool(d.IsPartialHue), bool(d.IsContainer))
                            else:
                                out[layer] = (serial, graphic, hue, 0, False, False)
                                continue             # (not kept: the next look asks again)
                        if len(wd) >= WORN_DATA_CAP:
                            wd.clear()
                        wd[k] = dat
                        out[layer] = (serial, graphic, hue) + dat
                    who = (int(p.Graphic), int(p.Hue), bool(p.IsFemale))
                    return out, who
                except Exception:
                    out = {}                         # the API's view instead
                    if keep is not None:
                        keep.clear()
            try:
                ap = API.Player
            except Exception:
                ap = None
            if not ap:
                return out, None
            for layer in DOLL_LAYERS:
                it = find_layer(API_LAYER_NAME[layer])
                if not it:
                    continue
                try:
                    serial, graphic, hue = int(it.Serial or 0), int(it.Graphic or 0), int(it.Hue or 0)
                except Exception:
                    continue
                anim, partial, cont = 0, False, False
                try:
                    d = it.GetItemData()
                    if d is not None:
                        anim, partial, cont = int(d.AnimID or 0), bool(d.IsPartialHue), bool(d.IsContainer)
                except Exception:
                    pass
                out[layer] = (serial, graphic, hue, anim, partial, cont)
            try:
                graphic = int(ap.Graphic or 0x0190)
            except Exception:
                graphic = 0x0190
            try:
                phue = int(ap.Hue or 0)
            except Exception:
                phue = 0
            who = (graphic, phue, graphic in FEMALE_BODIES)
            return out, who

        def body_gump(graphic, hue, female):
            """(body gump id, hue, extra gump id or 0): PaperDollInteractable.UpdateUI."""
            if graphic == GM_BODY:
                return PAPERDOLL_BODY[GM_BODY], GM_BODY_HUE, GM_EXTRA
            body = PAPERDOLL_BODY.get(graphic)
            if body is None:
                body = 0x000D if female else 0x000C
            return body, hue, 0

        def anim_gump(mob_graphic, item_graphic, anim, female):
            """Gump id of a worn item's paperdoll art: the client's own GetAnimID
            when it can be reached, else anim + sex offset, the other sex's art
            when that one is missing."""
            if R.m_animid is not None:
                try:
                    if getattr(R, "animid_n", 4) == 4:
                        args = [UInt16(mob_graphic), UInt16(item_graphic), UInt16(anim), bool(female)]
                    else:
                        args = [UInt16(mob_graphic), UInt16(anim), bool(female)]
                    v = int(R.m_animid.Invoke(None, Array[Object](args)))
                    if v > 0:
                        return v
                except Exception:
                    R.m_animid = None            # not callable this way: the module's own arithmetic
            if anim == SHROUD_ANIM and mob_graphic in GARGOYLE_BODIES:
                anim = GARGOYLE_SHROUD           # a dead gargoyle's shroud (the client's rule)
            if female:
                first, second = FEMALE_GUMP_OFFSET, MALE_GUMP_OFFSET
            else:
                first, second = MALE_GUMP_OFFSET, FEMALE_GUMP_OFFSET
            gid = anim + first
            if Kit.pic_size(gid) == (0, 0):
                alt = anim + second
                if Kit.pic_size(alt) != (0, 0):
                    return alt
            return gid

        def covered(layer, gfx, p=None):
            """Mobile.IsCovered: is `layer` hidden by something else worn? gfx is
            {layer: graphic} of the worn items, p the client's own player (taken
            once per redraw) when there is one."""
            if R.m_covered is not None and R.ok and p is not None:
                try:
                    return bool(R.m_covered.Invoke(None, Array[Object]([p, layer_enum(layer)])))
                except Exception:
                    pass
            robe = gfx.get(L_ROBE)
            pants = gfx.get(L_PANTS)
            if layer == L_SHOES:
                if gfx.get(L_LEGS) is not None or pants == 0x1411:
                    return True
                if pants in (0x0513, 0x0514) or robe == 0x0504:
                    return True
            elif layer == L_PANTS:
                if gfx.get(L_LEGS) is not None or robe == 0x0504:
                    return True
                if pants in (0x01EB, 0x03E5, 0x03EB):
                    skirt = gfx.get(L_SKIRT)
                    if skirt is not None and skirt not in (0x01C7, 0x01E4):
                        return True
                    if robe is not None and robe != 0x0229 and (robe <= 0x04E7 or robe > 0x04EB):
                        return True
            elif layer == L_TUNIC:               # any closed robe covers the tunic (the client's rule)
                if robe is not None:
                    return robe != 0 and robe not in ROBES_OPEN
            elif layer == L_TORSO:
                if robe is not None and robe != 0 and robe not in ROBES_OPEN:
                    return True
                tunic = gfx.get(L_TUNIC)
                if tunic is not None and tunic not in (0x1541, 0x1542):
                    if gfx.get(L_TORSO) in (0x782A, 0x782B):
                        return True
            elif layer == L_ARMS:
                return robe is not None and robe != 0 and robe not in ROBES_OPEN
            elif layer in (L_HELMET, L_HAIR):
                if robe is not None:
                    if robe > 0x3173:
                        if robe in (0x4B9D, 0x7816):
                            return True
                    elif robe <= 0x2687:
                        if robe < 0x2683:
                            return 0x204E <= robe <= 0x204F
                        return True
                    elif robe in (0x2FB9, 0x3173):
                        return True
            return False

        def layer_order(items):
            """The client's drawing order for what is worn (GetOrderedLayers)."""
            gfx = dict((k, v[1]) for k, v in items.items())
            cloak = items.get(L_CLOAK)
            order = ORDER_NORMAL
            if cloak is not None:
                if gfx.get(L_ROBE) in (0xA2CA, 0xA2CB):
                    order = ORDER_PARROT
                elif cloak[5]:                      # a quiver: a container worn as a cloak
                    order = ORDER_QUIVER
            order = list(order)
            torso = gfx.get(L_TORSO)
            if torso in (0x1C06, 0x1C02, 0x1C04):   # female leather / studded / plate: under the pants
                pi, ti = order.index(L_PANTS), order.index(L_TORSO)
                if pi < ti:
                    order.pop(ti)
                    order.insert(pi, L_TORSO)
            arms = gfx.get(L_ARMS)
            if arms in (0x13CD, 0x13DC, 0x13EE):    # leather / studded sleeves, ringmail arms: over the chest
                ai, ti = order.index(L_ARMS), order.index(L_TORSO)
                if ai < ti:
                    order.pop(ai)
                    order.insert(ti, L_ARMS)
            if arms in (0x1410, 0x1417):            # platemail arms draw as the torso and back
                order = [L_TORSO if l == L_ARMS else (L_ARMS if l == L_TORSO else l) for l in order]
            return order, gfx

        def doll_signature(items, who):
            return (who, tuple(sorted((k, v[0], v[1], v[2]) for k, v in items.items())))

        def art_bounds(gid):
            """(2.6.75) The opaque outline (x0, y0, x1, y1) of gump art gid in its own
            pixels, read once from the client's pixels (Tex) and kept; the art's
            whole size when the pixels can't be read; None when it shows nothing.
            Only rows and columns up to the first opaque one are looked at, each
            with one max() over its slice."""
            cache = geo["bounds"]
            if gid in cache:
                return cache[gid]
            b = None
            got = None
            try:
                if Tex.find():
                    got = Tex.gump_pixels(gid)
            except Exception:
                got = None
            if got is not None:
                px, w, h = got
                T = 0x01000000                   # alpha in the high byte; (signed) negatives too

                def solid(part):
                    return bool(part) and (max(part) >= T or min(part) < 0)
                top = 0
                while top < h and not solid(px[top * w:(top + 1) * w]):
                    top += 1
                if top < h:
                    bot = h - 1
                    while bot > top and not solid(px[bot * w:(bot + 1) * w]):
                        bot -= 1
                    lo, hi = top * w, (bot + 1) * w
                    x0 = 0
                    while x0 < w - 1 and not solid(px[lo + x0:hi:w]):
                        x0 += 1
                    x1 = w - 1
                    while x1 > x0 and not solid(px[lo + x1:hi:w]):
                        x1 -= 1
                    b = (x0, top, x1 + 1, bot + 1)
            else:
                pw_, ph_ = Kit.pic_size(gid)
                if pw_ > 0 and ph_ > 0:
                    b = (0, 0, pw_, ph_)
            if len(cache) >= BOUNDS_CAP:
                cache.clear()
            cache[gid] = b
            return b

        def draw_doll(items, who, praw=None):
            """Dispose the doll's pictures and draw them again for what is worn now
            (praw: the client's own player, taken once by the caller, or None).
            (2.6.75) The figure fills the panel's middle: the outline of every
            picture drawn (body and worn art, art_bounds) is scaled and centred in
            it, at any panel size, free or in a zone. (2.6.76) It fills the
            middle's height, running behind the slot columns when it is wider than
            the middle (drawn under them); each worn piece is the client's own
            paperdoll piece, so it can be dragged off the doll. (2.6.77) Each worn
            piece is a client item control drawing its gump art (DollPiece): press
            and drag lifts it, as in a slot."""
            g = win["g"]
            clear_doll()
            if g is None or who is None:
                return
            graphic, hue, female = who
            pics = []
            win["doll"] = pics          # from here on, so clear_doll sees every picture made,
            #                             even when one of them raises half way
            # what is drawn, bottom to top: (gump, hue, partial hue, serial for its hooks)
            draw = []
            body, bhue, extra = body_gump(graphic, hue, female)
            draw.append((body, bhue, True, 0, 0))
            if extra:
                draw.append((extra, hue, True, 0, 0))
            order, gfx = layer_order(items)
            for layer in order:
                it = items.get(layer)
                if it is None:
                    continue
                serial, igraphic, ihue, anim, partial, _c = it
                if covered(layer, gfx, praw):
                    continue
                if anim == 0 and R.m_animid is None:
                    continue
                gid = anim_gump(graphic, igraphic, anim, female)
                if gid <= 0 or Kit.pic_size(gid) == (0, 0):
                    continue
                # hair, beard and face aren't items to use or swap: no hooks on them
                draw.append((gid, ihue & 0x3FFF, partial,
                             0 if layer in (L_HAIR, L_BEARD, L_FACE) else serial, layer))
            # the figure's outline: every picture's, as they all share one origin
            fx0 = fy0 = 1 << 20
            fx1 = fy1 = -(1 << 20)
            for d in draw:
                b = art_bounds(d[0])
                if b is not None:
                    fx0, fy0 = min(fx0, b[0]), min(fy0, b[1])
                    fx1, fy1 = max(fx1, b[2]), max(fy1, b[3])
            if fx1 <= fx0 or fy1 <= fy0:
                fx0, fy0, fx1, fy1 = 0, 0, DOLL_W, DOLL_H
            fig = (fx1 - fx0, fy1 - fy0)
            # (2.6.76) the figure fills the middle's height and may run wider than the
            # middle, behind the slot columns (drawn under them), up to the panel's
            # inner width; centred on the middle (the panel's own centre)
            k = st["k"]
            mx, my, mw, mh = mid_rect()
            MX, MY = mx * k + DOLL_INSET, my * k + DOLL_INSET
            MW, MH = max(1.0, mw * k - 2 * DOLL_INSET), max(1.0, mh * k - 2 * DOLL_INSET)
            PW = max(1.0, (st["pw"] - 2 * PANEL_PAD) * k - 2 * DOLL_INSET)
            S = min(MH / fig[1], PW / fig[0])
            ox = int(round(MX + MW / 2.0 - S * (fx0 + fx1) / 2.0))
            oy = int(round(MY + MH / 2.0 - S * (fy0 + fy1) / 2.0))
            # unscaled (no client control): the art at its own size, centred the same way
            ux = int(round((MX + MW / 2.0) / k - (fx0 + fx1) / 2.0))
            uy = int(round((MY + MH / 2.0) / k - (fy0 + fy1) / 2.0))
            scaled = abs(S - 1.0) > 0.001
            # (2.6.76) where the figure goes in the window's list: right above the doll's
            # drop area, so the slots (made after it) draw over it and get its clicks.
            # (2.6.77) Added, then moved in the list itself: the client's Control.Insert
            # sets the parent first (which adds the control at the end) and then
            # inserts it again, so 2.6.76 had every piece twice, the last copy on top
            raw_g = win["raw"]
            at = [-1]
            if R.ok and raw_g is not None:
                try:
                    Kit.flush()
                    anchor = Kit.client_control(win["c"].get("doll_drop"))
                    if anchor is not None:
                        at[0] = raw_g.Children.IndexOf(anchor) + 1
                except Exception:
                    at[0] = -1

            def place(rc):
                """Into the window under the slots (or on top when the place isn't known)."""
                if at[0] <= 0:
                    return False
                ch = raw_g.Children
                rc.Parent = raw_g                # the client adds it at the end...
                while ch.Remove(rc):             # ...taken out (every copy)...
                    pass
                ch.Insert(min(at[0], ch.Count), rc)   # ...and put back once, under the slots
                at[0] += 1
                return True

            def doll_piece(gid, phue, partial, serial):
                """(2.6.77) A worn piece that can be lifted off the doll, or None."""
                if R.DollPiece is None or raw_g is None or at[0] <= 0:
                    return None
                try:
                    rc = R.DollPiece(raw_g, UInt32(int(serial)), UInt16(int(gid)),
                                     UInt16(int(phue)), 0, 0, True)
                except Exception:
                    R.DollPiece = None               # not this way on this build: plain pictures
                    return None
                try:
                    rc.va_gid, rc.va_k, rc.va_down = int(gid), float(S), False
                    rc.HighlightOnMouseOver = False
                    rc.IsPartialHue = bool(partial)
                    set_pos(rc, ox, oy)
                    if scaled:
                        rc.ApplyScale(S, False, True, False)
                    G.AddControlOnClick(rc, queue(("drop", 0)))   # an item let go on it: wear it
                    if not place(rc):
                        raise Exception("no place")
                except Exception:
                    safe(rc.Dispose)
                    return None
                return rc

            def pic(gid, phue, partial, serial=0, layer=0):
                if serial:                       # hair, beard, face and the body come with 0
                    rc = doll_piece(gid, phue, partial, serial)
                    if rc is not None:
                        pics.append(rc)
                        return
                p = G.CreateGumpPic(gid, ux, uy, phue) if phue else G.CreateGumpPic(gid, ux, uy)
                p.SetPos(ux, uy)
                rc = None
                try:
                    Kit.flush()
                    rc = Kit.client_control(p)
                    set_pos(rc, ox, oy)
                    if scaled:
                        rc.ApplyScale(S, False, True, False)
                except Exception:
                    rc = None
                    scale_ctrl(p)                # (2.6.57) at the panel's scale, as before
                if partial:                      # on the client's own control, not the wrapper
                    raw = safe(lambda: Kit.client_control(p))
                    safe(lambda: setattr(raw if raw is not None else p, "IsPartialHue", True))
                if serial:
                    safe(lambda: p.SetEntityTooltip(serial))
                    Kit.on_click(p, queue(("drop", 0)))          # an item let go on it: wear it
                    Kit.hook_double(p, queue(("use", serial)))   # double-click: use it
                else:
                    safe(lambda: p.SetAcceptMouseInput(False))
                placed = False
                if rc is not None:
                    try:
                        placed = place(rc)
                    except Exception:
                        placed = False
                if not placed:
                    g.Add(p)
                pics.append(p)

            for gid, phue, partial, serial, layer in draw:
                pic(gid, phue, partial, serial, layer)

        def look_worn(force=False):
            """ONE look at what is worn, every DOLL_EVERY seconds (or when forced:
            after a drop, a rebuild): it serves the doll and the slots both, so the
            twenty-odd layer reads happen four times a second instead of fourteen.
            The doll is redrawn when its signature changed; only the slots whose
            item changed are redrawn."""
            if st["minimized"] or win["g"] is None:
                return
            now = time.time()
            if not force and st["sig"] is not None and st["doll_sig"] is not None \
                    and 0 <= now - st["doll_at"] < DOLL_EVERY:
                return
            st["doll_at"] = now
            p = player_raw() if R.ok else None       # the client's player, once per look
            got = {}
            items, who = worn(p, got)
            # the slots: (serial per slot) from the same look (a plain loop: hot path)
            sig = []
            for l in SLOT_LAYERS:
                it = items.get(l)
                sig.append(it[0] if it is not None else 0)
            sig = tuple(sig)
            if sig != st["sig"]:
                refresh_slots(sig, p, got)
            dsig = doll_signature(items, who)
            if dsig != st["doll_sig"]:
                st["doll_sig"] = dsig
                draw_doll(items, who, p)

        # ---------- the slots ----------
        def show_item(s, item, api_item):
            """Draw `item` (client Item, or None with api_item) in slot s."""
            g = win["g"]
            if s["ctrl"] is not None:
                Kit.dispose(s["ctrl"])
                s["ctrl"] = None
            if item is None and api_item is None:
                safe(lambda: setattr(s["label"], "IsVisible", True))
                if s.get("tip"):                         # (2.6.72) its "drop here" tooltip back
                    safe(lambda: s["drop"].SetTooltip(s["tip"]))
                return
            safe(lambda: setattr(s["label"], "IsVisible", False))
            safe(lambda: s["drop"].SetTooltip(""))       # (2.6.72) the item's own tooltip only
            if R.ok and item is not None and win["raw"] is not None:
                try:
                    args = (win["raw"], UInt32(int(item.Serial)), UInt16(int(item.DisplayedGraphic)),
                            UInt16(int(item.Hue)), 0, 0)
                    ig = None
                    if R.SlotItem is not None:           # (2.6.76) clicks anywhere on it
                        try:
                            ig = R.SlotItem(*args)
                        except Exception:
                            R.SlotItem = None            # not on this build: the client's own
                    if ig is None:
                        ig = R.ItemGump(*args)
                    iw, ih = size_of(ig)
                    # (2.6.72) fitted into its slot (big art was pinned top-left at its own
                    # size and ran over the slots beside it), centred; the client's own
                    # control scale, so its mouse area matches what is drawn
                    f = min(1.0, (SLOT - 6) / float(max(1, iw)), (SLOT - 6) / float(max(1, ih)))
                    k = st["k"]
                    set_pos(ig, int(round((s["x"] + (SLOT - iw * f) / 2.0) * k)),
                            int(round((s["y"] + (SLOT - ih * f) / 2.0) * k)))
                    if abs(k * f - 1.0) > 0.001:
                        try:
                            ig.ApplyScale(k * f, False, True, False)
                        except Exception:
                            scale_ctrl(ig, True)
                    try:
                        G.AddControlOnClick(ig, queue(("drop", s["layer"])))   # before Add: a
                    except Exception as e:                                        # failure leaves
                        safe(ig.Dispose)                                          # nothing behind
                        raise e
                    g.Add(ig)
                    s["ctrl"] = ig
                    return
                except Exception as e:
                    R.error = "item control: %s" % e
            # no client access: the API's picture, with the item's property tooltip
            serial = int(api_item.Serial) if api_item is not None else int(item.Serial)
            graphic = int(api_item.Graphic) if api_item is not None else int(item.DisplayedGraphic)
            pic = G.CreateGumpItemPic(graphic, SLOT - 6, SLOT - 6)
            pic.SetRect(s["x"] + 3, s["y"] + 3, SLOT - 6, SLOT - 6)
            scale_ctrl(pic)
            safe(lambda: pic.SetEntityTooltip(serial))
            Kit.on_click(pic, queue(("drop", s["layer"])))
            Kit.hook_double(pic, queue(("use", serial)))
            g.Add(pic)
            s["ctrl"] = pic

        def refresh_slots(sig, p, got=None):
            """Redraw only the slots whose item changed. `sig` is (serial per slot)
            from look_worn's look; the item itself is fetched for the changed slots
            only (the client's own Item through p, else the API's)."""
            slots = win["slots"]
            if len(slots) != len(sig):
                return
            old = st["sig"] or (None,) * len(slots)
            for i, s in enumerate(slots):
                if sig[i] == old[i]:
                    continue
                s["serial"] = sig[i]
                item = api_item = None
                if sig[i]:
                    if R.ok and p is not None:
                        item = got.get(s["layer"]) if got else None   # (2.6.82) from the look
                        if item is None:
                            try:
                                item = p.FindItemByLayer(layer_enum(s["layer"]))
                            except Exception:
                                item = None
                    if item is None:
                        api_item = find_layer(s["name"])
                show_item(s, item, api_item)
            st["sig"] = sig

        # ---------- equipping ----------
        def on_drop(layer):
            """An item on the cursor was let go on a slot: wear it. Goes to the layer
            the item belongs to (the slot clicked only needs to be a slot)."""
            if R.ok:
                h = held()
                if h is None:
                    return
                serial, wearable, item_layer = h
                if not wearable:
                    API.SysMsg(TITLE + ": that can't be worn.", Kit.HUE_BAD)
                    return
                if item_layer not in LAYER_SET and item_layer > 0:
                    API.SysMsg(TITLE + ": that doesn't go in an equipment slot.", Kit.HUE_BAD)
                    return
                try:
                    w = world()
                    p = w.Player
                    # layer 0: the tile data couldn't be read; the client's own Equip
                    # still finds the layer (no swap, so an occupied layer refuses)
                    worn_it = p.FindItemByLayer(layer_enum(item_layer)) if item_layer else None
                    if worn_it is not None and int(worn_it.Serial) == serial:
                        worn_it = None                   # putting it back where it was
                    if worn_it is None:
                        R.m_equip.Invoke(None, Array[Object]([w, UInt32(int(p.Serial))]))
                    else:
                        R.m_swap.Invoke(None, Array[Object]([w, UInt32(int(p.Serial)),
                                                             layer_enum(item_layer),
                                                             UInt32(int(worn_it.Serial))]))
                    st["sig"] = None
                except Exception as e:
                    API.SysMsg(TITLE + ": couldn't equip that (%s)." % e, Kit.HUE_BAD)
                return
            # no client access: the API equips what the cursor holds
            serial = int(safe(API.GetHeldItem, 0) or 0)
            if serial:
                API.EquipItem(serial)
                st["sig"] = None

        # ---------- stats ----------
        STAT_KEYS = ("Strength", "Dexterity", "Intelligence", "Hits", "HitsMax", "Mana", "ManaMax",
                     "Stamina", "StaminaMax", "Weight", "WeightMax", "Gold", "Followers",
                     "FollowersMax", "PhysicalResistance")   # 2.6.51: no other resists, no luck
        STATS_IN = 10                            # text keeps this far inside the strip's box

        def fmt_n(v):
            try:
                v = int(v)
            except Exception:
                return "?"
            s = str(abs(v))
            out = ""
            while len(s) > 3:
                out = "," + s[-3:] + out
                s = s[:-3]
            return ("-" if v < 0 else "") + s + out

        def build_weight_bar(g, c, px, y):
            """The weight bar on stats line 3, after "Weight w/max" (room kept for
            four-digit weights) and before gold / followers: the client's
            red status line hued grey under one fill per colour (only one shows).
            Its width is what the line leaves, between WEIGHT_BAR_MIN and _W."""
            wslot = Kit.text_w("Weight 0000/0000")
            rest_w = Kit.text_w("Gold 9,999,999   Followers 99/99")
            bx = px + 10 + wslot + 6
            sw = st["strip_w"] or PANEL_W
            room = sw - (bx - px) - 10 - rest_w - 14
            bw = max(WEIGHT_BAR_MIN, min(WEIGHT_BAR_W, room))
            add_weight_fills(g, c, bx, y, bw)
            c["stats4"] = Kit.add_label(g, "", bx + bw + 10, y, Kit.HUE_TEXT)
            # room each line's text has inside the box (2.6.51: nothing runs past its edge)
            c["room"] = sw - 2 * STATS_IN
            c["room3"] = wslot
            c["room4"] = max(0, sw - (bx + bw + 10 - px) - STATS_IN)

        def add_weight_fills(g, c, bx, top, bw):
            """The weight bar's grey line and its three fills (one shows), bw wide,
            in the 16 px text row starting at `top` (2.6.71: shared by the strip
            and the column)."""
            lw, lh = Kit.pic_size(Kit.LINE_RED)
            fh = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or lh or 9))
            by = top + max(0, (16 - fh) // 2)
            if lw > 0:
                Kit.add_tiled(g, Kit.LINE_RED, bx, by, bw, fh, hue=WEIGHT_BG_HUE)
            else:
                Kit.add_tiled(g, Kit.SECTION_TILE, bx, by, bw, fh, 1.0)
            fills = {}
            for kind, art, hue in (("ok", Kit.LINE_POISON, WEIGHT_HUE_OK),
                                   ("warn", Kit.LINE_BLUE, WEIGHT_HUE_WARN),
                                   ("red", Kit.LINE_RED, 0)):
                f = Kit.add_tiled(g, art, bx, by, 1, fh, hue=hue)
                if f is not None:
                    safe(lambda f=f: setattr(f, "IsVisible", False))
                    fills[kind] = f
            c["wfills"] = fills
            c["wbar_w"] = bw

        def build_stats_col(g, c, col):
            """(2.6.71) The stats as a column beside the doll, the panel's height:
            one line each (Str, Dex, Int, HP, Mana, Stamina, Weight with its bar
            under it, Gold, Followers), centred top to bottom."""
            x, y, w, h = col
            Kit.add_section(g, x, y, w, h)
            Kit.catcher(g, x, y, w, h, lambda *a: None, None, movable=not zoned_lock())
            pitch = max(COL_PITCH_MIN, min(COL_PITCH_MAX,
                                           (h - 16 - COL_BAR_H) // COL_ROWS))
            ty = y + max(8, (h - COL_ROWS * pitch - COL_BAR_H) // 2)
            labels = []
            for i in range(COL_ROWS):
                ly = ty + i * pitch + (COL_BAR_H if i >= 7 else 0)   # the bar's row after Weight
                labels.append(Kit.add_label(g, "", x + STATS_IN, ly, Kit.HUE_TEXT))
            c["scol"] = labels
            c["room"] = w - 2 * STATS_IN
            add_weight_fills(g, c, x + STATS_IN, ty + 7 * pitch - 1, w - 2 * STATS_IN)

        def weight_update(wt, wmax, strength):
            """One weight reading: the alert (once per crossing of the red line,
            armed again below it) and, when it is drawn, the bar."""
            if wmax <= 0 and strength > 0:            # the client doesn't know your max
                wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0
            if frac >= WEIGHT_RED:
                if st["w_armed"]:
                    # disarmed once it is raised; "not now" (the alerts' 10 s rate limit,
                    # or the kind turned off) keeps it armed, so it comes when it can
                    raised = True
                    if hasattr(HOST, "alert"):
                        try:
                            raised = HOST.alert("character.weight", "Weight %d/%d (%d%%): nearly "
                                                "overloaded" % (wt, wmax, int(frac * 100)),
                                                level="warn", who="weight") is not False
                        except Exception:
                            raised = True
                    if raised:
                        st["w_armed"] = False
            elif frac >= 0:
                st["w_armed"] = True
            fills = win["c"].get("wfills")
            if not fills or st["minimized"]:
                return
            if frac < 0:
                kind, width = None, 0
            else:
                kind = "red" if frac >= WEIGHT_RED else ("warn" if frac >= WEIGHT_WARN else "ok")
                bw = win["c"]["wbar_w"]
                width = max(1, min(bw, int(round(bw * min(1.0, frac)))))
            if (kind, width) == st["wbar"]:
                return
            st["wbar"] = (kind, width)
            for k, f in fills.items():
                try:
                    if k == kind:
                        Kit.ui_w(f, width)
                    f.IsVisible = k == kind
                except Exception:
                    pass

        def weight_tick():
            """The alert's own reading (STATS_EVERY) while the strip isn't read:
            minimized, folded into the Action Bar or the strip turned off."""
            now = time.time()
            if 0 <= now - st["w_at"] < STATS_EVERY:
                return
            st["w_at"] = now
            try:
                p = API.Player
            except Exception:
                p = None
            if not p:
                return
            try:
                wt, wmax, strength = int(p.Weight), int(p.WeightMax), int(p.Strength)
            except Exception:
                return
            weight_update(wt, wmax, strength)

        def refresh_stats():
            """The stats strip, every STATS_EVERY. False when the strip isn't up
            (then weight_tick reads the weight for the alert)."""
            c = win["c"]
            if st["minimized"] or ("stats1" not in c and "scol" not in c):
                return False
            now = time.time()
            if 0 <= now - st["stats_at"] < STATS_EVERY:
                return True
            st["stats_at"] = now
            try:
                p = HOST.me()                        # (2.6.82) the pass's player (read once a pass)
            except Exception:
                p = None
            if not p:
                return True
            v = {}
            vals = []
            for k in STAT_KEYS:                      # a plain loop: this runs all the time
                try:
                    x = int(getattr(p, k))
                except Exception:
                    x = 0
                v[k] = x
                vals.append(x)
            room = c["room"]
            col = c.get("scol")
            # (2.6.82) the same numbers into the same labels as last time: nothing
            # to format or fit (the weight alert still sees every reading)
            s1 = c.get("stats1")
            old = st.get("stats_key")
            if old is not None and old[0] == vals and old[1] is col and old[2] is s1 \
                    and old[3] == (room, c.get("room3"), c.get("room4")):
                weight_update(v["Weight"], v["WeightMax"], v["Strength"])
                return True
            st["stats_key"] = (vals, col, s1, (room, c.get("room3"), c.get("room4")))
            if col is not None:                      # (2.6.71) the column: a line each
                for lbl, text in zip(col, (
                        "Str %d" % v["Strength"], "Dex %d" % v["Dexterity"],
                        "Int %d" % v["Intelligence"], "HP %d/%d" % (v["Hits"], v["HitsMax"]),
                        "Mana %d/%d" % (v["Mana"], v["ManaMax"]),
                        "Stamina %d/%d" % (v["Stamina"], v["StaminaMax"]),
                        "Weight %d/%d" % (v["Weight"], v["WeightMax"]),
                        "Gold %s" % fmt_n(v["Gold"]),
                        "Followers %d/%d" % (v["Followers"], v["FollowersMax"]),
                        "AR %d" % v["PhysicalResistance"])):
                    Kit.set_text(lbl, Kit.fit(text, room))
                weight_update(v["Weight"], v["WeightMax"], v["Strength"])
                return True
            line1 = "Str %d   Dex %d   Int %d   AR %d" % (v["Strength"], v["Dexterity"],
                                                          v["Intelligence"], v["PhysicalResistance"])
            line2 = "HP %d/%d   Mana %d/%d   Stamina %d/%d" % (
                v["Hits"], v["HitsMax"], v["Mana"], v["ManaMax"], v["Stamina"], v["StaminaMax"])
            line3 = "Weight %d/%d" % (v["Weight"], v["WeightMax"])
            line4 = "Gold %s   Followers %d/%d" % (fmt_n(v["Gold"]), v["Followers"], v["FollowersMax"])
            # each line kept inside the box (cut short with ".." if it ever would run
            # past: a huge number, a bigger font); Kit.fit is a quick length check
            # when it fits, and set_text writes only what changed
            room = c["room"]
            Kit.set_text(c["stats1"], Kit.fit(line1, room))
            Kit.set_text(c["stats2"], Kit.fit(line2, room))
            Kit.set_text(c["stats3"], Kit.fit(line3, c["room3"]))
            Kit.set_text(c["stats4"], Kit.fit(line4, c["room4"]))
            weight_update(v["Weight"], v["WeightMax"], v["Strength"])
            return True

        # ---------- Bags: one window ----------
        def bag_service(name):
            return HOST.services.get(name) if hasattr(HOST, "services") else None

        def bag_cmd(cmd):
            """The Action Bar's bag buttons (relayed by Bags while combined)."""
            if cmd == "show":
                queue("show")()
            elif cmd == "dock":
                queue("to_bar")()

        def combine_tick():
            """Attach to Bags when both run (and the setting is on); let go
            when it stops or the setting is turned off; follow its grid size."""
            attach = bag_service("bag.attach")
            size = bag_service("bag.grid_size")
            att = st["attached"]
            want = settings["combine"] and attach is not None and size is not None
            if att is None:
                if not want:
                    return
                # take the bag on as soon as it is there; the hole for its slots is
                # cut once it has drawn them and says how big they are. dx/dy start
                # where the hole will be, so its grid is never drawn over the title
                # bar for the tick or two before that
                hx, hy = hole_guess()
                att = {"g": win["g"], "raw": None, "dx": hx, "dy": hy, "shown": not st["minimized"],
                       "state": dock_state(), "grid_wh": None, "cmd": bag_cmd}
                st["attached"] = att
                try:
                    attach(att)
                except Exception as e:
                    st["attached"] = None
                    API.SysMsg(TITLE + ": couldn't combine with Bags (%s)." % e, Kit.HUE_BAD)
                    return
                build_window()
                return
            if not want:
                detach()
                return
            try:                                     # every tick: no safe() wrapper here
                wh = size()
            except Exception:
                wh = None
            wh = tuple(wh) if wh else None
            if wh != att["grid_wh"]:
                att["grid_wh"] = wh
                build_window()

        def detach():
            att, st["attached"] = st["attached"], None
            tell_bags(None)
            st["told_shrink"] = None                 # (2.6.67) Bags gives its scale back itself
            if att is not None:
                attach = bag_service("bag.attach")
                if attach is not None:
                    safe(lambda: attach(None))
            if win["g"] is not None and not st["shutting"]:
                build_window()

        def sync_attached():
            att = st["attached"]
            if att is not None:
                att["shown"] = not st["minimized"]
                att["state"] = dock_state()

        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        PAGE_H = 170

        def config_height(w):
            return PAGE_H

        def build_config(g, x, y, w):
            Kit.add_section(g, x, y, w, PAGE_H, "WINDOW")
            c = {"stats": Kit.add_check(g, "Show your stats with the paperdoll", x + 12, y + 32,
                                        settings["stats"],
                                        "Str / Dex / Int, HP, mana, stamina, weight bar, gold, "
                                        "followers: under the doll, or beside it in a zone"),
                 "combine": Kit.add_check(g, "Combine with Bags into one window",
                                          x + 12, y + 58, settings["combine"],
                                          "One window: this title bar, the doll and its slots, and "
                                          "the Bags grid in it (unticked: two separate windows)"),
                 "beside": Kit.add_check(g, "Bags beside the doll (instead of underneath)",
                                         x + 12, y + 84, settings["beside"],
                                         "Combined: put the bag grid next to the doll panel rather "
                                         "than under it. A grid too tall to stack goes beside the "
                                         "doll anyway."),
                 "left": Kit.add_check(g, "Bags on the left", x + 12, y + 110, settings["left"],
                                       "When the bags sit beside the doll: on its left (unticked: "
                                       "on its right)")}
            Kit.add_label(g, "Drop an item on any slot to wear it; drag a worn item out to take it off.",
                          x + 12, y + 140, Kit.HUE_INFO)
            page.update({"c": c})

        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for key in ("stats", "combine", "beside", "left"):
                v = bool(safe(lambda: c[key].IsChecked, settings[key]))
                if v != settings[key]:
                    settings[key] = v
                    changed = True
            if changed:
                save_settings()
                if win["g"] is not None:
                    queue("redraw")()
                    HOST.poke()

        def config_closed():
            page["c"] = None

        # ---------- module hooks ----------
        def _start():
            if not safe(lambda: API.Player):
                st["wait_player"] = True             # built on the first tick with a player
                load_settings()
                return
            st["wait_player"] = False
            load_settings()
            if not R.tried:
                R.tried = True
                init_interop()
            st.update({"shutting": False, "docked": False, "queue": [], "sig": None, "doll_sig": None,
                       "attached": None, "beside_said": False, "fit": None, "k": 1.0, "py": None,
                       "strip_w": None, "pw": PANEL_W, "col": None,
                       "ph": PANEL_H, "rp": COL_PITCH, "mode": None,
                       "told_bags": None, "pair": None, "pair_at": 0.0,
                       "room": None, "room_fs": None, "told_shrink": None, "grew": False,
                       "w_armed": True, "w_at": 0.0, "wbar": None,
                       "minimized": st["saved_min"] or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            if hasattr(HOST, "alert_kind"):          # listed on Settings > Alerts (sound / on-off)
                safe(lambda: HOST.alert_kind("character.weight", "Weight near the limit",
                                             WEIGHT_ALERT_SOUND))
            build_window()
            hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
            # (2.6.57) in a zone the window is drawn exactly its slot's size: the doll
            # panel scaled as one piece, the bag grid filling the rest (layout_fit)
            hooks["fit"] = layout_fit
            hooks["exact"] = True
            hooks["pieces_out"] = True      # (nothing rides beside it now: the whole slot is its)
            HOST.dock_add(KEY, hooks)
            if not R.ok:
                API.SysMsg(TITLE + ": no client access (%s); the slots show pictures, and an item "
                           "dropped on them is equipped without swapping out what was worn there."
                           % R.error, Kit.HUE_INFO)

        def _tick():
            if st["wait_player"]:
                # not in the world yet: the window waits (never an error here, which
                # would untick the module for good)
                try:
                    if not API.Player:
                        return
                except Exception:
                    return
                st["wait_player"] = False
                _start()                         # now the window can be built
                return
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                save_place()                     # the place is kept before the window goes
                Kit.dispose(win["g"])            # on_disposed turns the module off
                return
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)
                    save_state()
                    build_window()
                elif action == "show":
                    st["minimized"] = st["docked"] = False
                    HOST.dock_forget(KEY)
                    save_state()
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)
                elif action == "redraw":
                    if held() is not None:           # (2.6.85) never under a drag: at the drop
                        st["redraw_due"] = True
                    else:
                        build_window()
                elif action == "bag_mgr":
                    fn = bag_service("bag.open_manager")
                    if fn is not None:
                        fn()
                elif action == "bag_traps":
                    fn = bag_service("bag.open_traps")
                    if fn is not None:
                        fn()
                elif kind == "drop":
                    on_drop(action[1])
                elif kind == "use":
                    API.UseObject(action[1])
                elif kind == "follow":
                    Follow.toggle(action[1], TITLE)
            sync_attached()
            combine_tick()
            if win["g"] is None:
                return
            drag = held() is not None                # (2.6.85) rebuilds wait for the drop
            if st.get("redraw_due") and not drag:
                st["redraw_due"] = False
                build_window()
                return
            if st["attached"] is not None and not drag:
                # (2.6.66) the two zones: a change in the one under ours (resized,
                # made, taken away) redraws the window; with the window free the
                # mother still pairs the two (the bags slotted alone bring the doll
                # into the zone over them, or go free with it)
                now = time.time()
                if now - st["pair_at"] >= PAIR_EVERY or now < st["pair_at"]:
                    st["pair_at"] = now
                    pr = pair_rects()
                    if pr != st["pair"]:
                        st["pair"] = pr
                        if st["fit"] is not None:
                            build_window()
                            return
                    # (2.6.67) bags opened, closed or grown since: the scale the grid
                    # fits its room at is looked at again (a rebuild only on a change)
                    # (2.6.72) only when Bags' own data changed (a bag opened, closed,
                    # minimized or grew; the zone changed): never on the timer alone
                    room = st["room"]
                    if room is not None and st["fit"] is not None and not st["minimized"]:
                        ci = cell_info()
                        sig = (room, None if ci is None else (round(ci[0], 1), round(ci[1], 1),
                                                              ci[2], ci[3], ci[4], ci[5]))
                        if sig != st.get("room_sig"):
                            st["room_sig"] = sig
                            fs = fit_scale(room[0], room[1])
                            if fs is not None and (fs[0] != st["told_shrink"]
                                                   or (fs[1] > room[1]) != st["grew"]):
                                build_window()
                                return
            look_worn()                              # the doll and the slots, from one look
            if not refresh_stats():                  # (the strip reads weight for the bar and
                weight_tick()                        #  the alert; else the alert reads it)

        def _stop():
            st["shutting"] = True
            HOST.dock_remove(KEY)
            Kit.save_pos(POS_KEY, win["g"])
            save_state()
            save_settings()
            att, st["attached"] = st["attached"], None
            if att is not None:
                attach = bag_service("bag.attach")
                if attach is not None:
                    safe(lambda: attach(None))
            clear_slots()
            g, win["g"] = win["g"], None
            win["raw"] = None
            Kit.dispose(g)

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_storage():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  on its Modules tab.
        #
        #  WHAT IT DOES - remembers what is in every container you open, on every
        #  character of the account, and finds things again:
        #    - Open your bank box, a chest, a bag inside them or a pack animal's pack,
        #      and its items are noted (graphic, hue, amount and the name the client
        #      already has; nothing is sent to the server). Opening it again replaces
        #      what was noted before. Bags inside it that the client knows are noted
        #      too, each under the place it is in.
        #    - The Storage window: type part of a name ("nightshade") or a
        #      graphic ("0x0F88"; several with commas) in its Find box and it lists
        #      every place holding it, grouped by place, with how many and when that
        #      place was last seen: "Bank box (A): 140, Wooden chest at 1432, 1690
        #      (B): 60, seen 3 days ago". Your own backpack is counted live ("on you
        #      now"), never stored.
        #    - With the box empty it shows your favourites (reagents and bandages at
        #      first) with their totals across the account. "Add favourite" adds what
        #      is in the box; the settings page takes them off again.
        #    - Click a place to pick it; "Name" gives it a name of your own,
        #      "Forget" takes it (and the bags in it) out of the index. A pack
        #      animal's rows can be Alt+clicked to auto-follow it (again to stop).
        #  The index is one file per account next to Virtue Assistant
        #  (_storage_index_<id>.txt, made by the module itself; nothing to install),
        #  shared by every character of the account and by a second client on the
        #  same PC: each one merges the other's changes before it writes. It keeps at
        #  most MAX_CONTAINERS containers and MAX_ITEMS item lines, and forgets a
        #  place not seen for the number of days set on the settings page.
        #
        #  Other modules can ask HOST.services["storage.find"](text) (stored places
        #  holding it) and HOST.services["storage.total"](graphic, hue=None).
        # ============================ MODULE START ===================================
        #  MODULE: Storage  (was Storage Index)  -  what is in your bank, chests and pack animals
        # =============================================================================
        KEY = "storage"
        TITLE = "Storage"                     # (was "Storage Index"; the saved keys and file keep that)

        # ------------------------------- CONFIG --------------------------------------
        MAX_CONTAINERS = 300        # containers kept in the index (oldest places drop first)
        MAX_ITEMS = 20000           # item lines (one per kind of item per container) at most
        STALE_DAYS = 60             # default for "forget places not seen for N days" (settings)
        READ_DELAYS = (0.6, 2.0)    # s after a container opens: read it (its contents follow the open)
        REREAD_SECS = 15.0          # while its window stays open, look again this often
        OPEN_CHECK = 1.0            # s between looks at whether a read container is still open
        WATCH_MAX = 600.0           # s: stop watching a container that seems open this long
        WATCH_CAP = 20              # containers watched at once
        READ_MAX = 1500             # items read from one container (and the bags in it) at most
        SAVE_DELAY = 5.0            # s after a change before the index file is written
        MERGE_CHECK = 10.0          # s between looks at the file for another client's changes
        TOMB_DAYS = 30              # a forgotten place is remembered as forgotten this long
        SEARCH_WAIT = 0.4           # s after the last key in the Find box before it searches
        LIVE_EVERY = 3.0            # s between reads of your backpack while the window shows
        ROWS = 14                   # result rows on a page
        MAX_RESULT_ROWS = ROWS * 30  # lines a search lists at most (the rest: "and N more")
        MAX_FAVS = 12               # favourites
        NAME_MAX = 40               # longest name of your own for a place
        #  Mobiles (body graphic) whose pack is a pack animal's pack. UNCHECKED IN GAME:
        #  the classic bodies; any other pet of yours with a pack shows as "Pack animal".
        PACK_BODIES = {0x0123: "Pack horse", 0x0124: "Pack llama", 0x0317: "Giant beetle"}
        #  Never indexed: corpses, the secure-trade box. UNCHECKED IN GAME (classic ids).
        SKIP_GRAPHICS = (0x2006, 0x1E5E)
        FILE_FMT = "_storage_index_%s.txt"      # next to Virtue Assistant, one per account
        FILE_HEAD = "# Virtue Assistant Storage Index 1"
        SETTINGS_KEY = "StorageIndex_settings"   # per character
        FAVS_KEY = "StorageIndex_favs"           # per character: "label=term;label=term"
        ACCOUNT_KEY = "StorageIndex_account"     # per account: an id, only when the client's
        #                                          profile can't be read
        POS_KEY = "StorageIndex_pos"
        MIN_KEY = "StorageIndex_min"
        W = 420
        MINI_W, MINI_H = 260, 46
        ROW_H = 20
        TRAY_ICON = 0x0E7C                       # a strong box, on the Action Bar's tray button
        FOLLOW_TIP = "Alt+click: auto-follow (again to stop)"
        # -----------------------------------------------------------------------------

        M = Kit.MARGIN
        IW = W - 2 * M
        Y_FIND = M + 30 + Kit.GAP
        H_FIND = 64
        Y_LIST = Y_FIND + H_FIND + Kit.GAP
        H_LIST = 12 + ROWS * ROW_H + 8
        Y_STAT = Y_LIST + H_LIST + Kit.GAP
        H_STAT = 30
        H = Y_STAT + H_STAT + M

        def default_favs():
            out = []
            regs = getattr(Kit, "REAGENTS", None) or {}
            for name, gfx in sorted(regs.values()):
                out.append([name, "0x%04X" % gfx])
            out.append(["Bandages", "0x0E21"])
            return out

        settings = {"bank": True, "ground": True, "pack": True, "days": STALE_DAYS, "say": False}
        favs = []                                  # [label, term]
        st = {"shutting": True, "minimized": False, "docked": False, "queue": [],
              "active": False, "hooked": False, "events": False,
              # (2.6.66) popped out as a tab beside another window: {"g": its gump,
              # "side": "R" / "L"}, or None; the gump the window was attached to
              }
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        page = {"c": None, "store": ({}, {})}
        # the index: container serial -> record (see new_rec); forgotten places
        idx = {"recs": {}, "tombs": {}, "ver": 0, "dirty": False, "dirty_at": 0.0,
               "loaded": False, "path": None, "mtime": None, "merge_at": 0.0, "err": ""}
        summ = {"ver": -1, "keys": {}, "places": {}, "items": 0, "chars": 0}
        view = {"query": "", "seen_text": None, "changed_at": 0.0, "page": 0, "rows": [],
                "sel": None, "naming": None, "forget_arm": (None, 0.0), "status": "",
                "status_hue": Kit.HUE_INFO, "status_at": 0.0, "dirty": True, "built_for": None,
                "live": {}, "live_at": 0.0, "live_ver": 0, "live_sig": None, "data": [], "prev": [],
                "last_read": ("", 0.0)}
        watching = {}                              # serial -> [opened at, next read, step]
        reads = []                                 # results of container reads, for thread_tick
        opens = []                                 # serials the open event reported (script thread)
        known_open = set()                         # (fallback poll) container windows open
        tile_names = {}                            # graphic -> its tiledata name (cleaned)
        quick = {}                                 # container -> a quick signature of its last read
        fcache = {"key": None, "stats": []}        # the favourites' stored totals (see fav_stored)
        scache = {"key": None, "by": {}}           # the stored part of the last search
        NAME_JUNK = re.compile(r"%[^%]*%|%s")

        # ---------- small helpers ----------
        def clean_text(s):
            return str(s or "").replace("|", "/").replace("\r", " ").replace("\n", " ").strip()

        def ago(secs):
            if secs < 60:
                return "just now"
            if secs < 3600:
                return "%dm ago" % (secs // 60)
            if secs < 86400:
                return "%dh ago" % (secs // 3600)
            d = int(secs // 86400)
            return "1 day ago" if d == 1 else "%d days ago" % d

        def num(n):
            try:
                return format(int(n), ",")
            except Exception:
                return str(n)

        def fnv(text):
            h = 0x811C9DC5
            for ch in text:
                h = ((h ^ ord(ch)) * 0x01000193) & 0xFFFFFFFF
            return "%08x" % h

        def tile_name(it, graphic):
            """The tiledata name of a graphic (cached), for items the client has no name for."""
            n = tile_names.get(graphic)
            if n is None:
                try:
                    d = it.GetItemData()
                    n = NAME_JUNK.sub("", str(d.Name or "")).strip() if d is not None else ""
                except Exception:
                    n = ""
                if len(tile_names) > 3000:
                    tile_names.clear()
                tile_names[graphic] = n
            return n

        def item_name(it, graphic, amount):
            try:
                n = str(it.Name or "")
            except Exception:
                n = ""
            if "%" in n:
                n = NAME_JUNK.sub("", n)
            n = n.strip()
            if amount > 1:
                a = str(amount)
                if n.startswith(a + " "):
                    n = n[len(a) + 1:].strip()
            if not n:
                n = tile_name(it, graphic) or ("item 0x%04X" % graphic)
            n = clean_text(n)
            return n[:1].upper() + n[1:]

        def parse_terms(text):
            """Find-box text -> [("g", graphic) / ("n", lower-case name part)]."""
            out = []
            for t in str(text or "").split(","):
                t = t.strip().lower()
                if not t:
                    continue
                g = None
                try:
                    if t.startswith("0x") and len(t) > 2:
                        g = int(t, 16)
                    elif t.isdigit() and len(t) >= 3:
                        g = int(t)
                except ValueError:
                    g = None
                out.append(("g", g) if g is not None else ("n", t))
            return out

        def matches(terms, key):
            g, ln = key[0], key[2]
            for kind, v in terms:
                if kind == "g":
                    if g == v:
                        return True
                elif v in ln:
                    return True
            return False

        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if k in ("bank", "ground", "pack", "say"):
                    settings[k] = v == "1"
                elif k == "days":
                    try:
                        settings["days"] = max(1, min(3650, int(v)))
                    except ValueError:
                        pass

        def save_settings():
            Kit.put_var(SETTINGS_KEY, "bank=%d;ground=%d;pack=%d;days=%d;say=%d" % (
                settings["bank"], settings["ground"], settings["pack"], settings["days"],
                settings["say"]))

        def load_favs():
            raw = Kit.get_var(FAVS_KEY, "")
            del favs[:]
            if not raw:
                favs.extend(default_favs())
                return
            if raw == "-":                          # every favourite taken off
                return
            for part in raw.split(";"):
                if "=" not in part:
                    continue
                label, term = part.split("=", 1)
                label, term = label.strip(), term.strip()
                if term and len(favs) < MAX_FAVS:
                    favs.append([label or term, term])

        def save_favs():
            if not favs:
                Kit.put_var(FAVS_KEY, "-")
                return
            Kit.put_var(FAVS_KEY, ";".join("%s=%s" % (l.replace(";", ",").replace("=", "-"),
                                                      t.replace(";", ",")) for l, t in favs))

        # ---------- the index file (script thread only) ----------
        def account_id():
            """One id per account (client thread, at start): from the client's
            profile (server and account, hashed), else an id saved per account."""
            try:
                Typing._find()
                prof = Typing.prof
                cur = Typing._get(None, "CurrentProfile", prof) if prof is not None else None
                user = Typing._get(cur, "Username") if cur is not None else None
                if user:
                    server = Typing._get(cur, "ServerName") or ""
                    return fnv(("%s|%s" % (server, user)).lower())
            except Exception:
                pass
            try:
                scope = API.PersistentVar.Account
                v = str(API.GetPersistentVar(ACCOUNT_KEY, "", scope) or "")
                if not v:
                    import random
                    v = "a%07x" % random.randint(0, 0xFFFFFFF)
                    API.SavePersistentVar(ACCOUNT_KEY, v, scope)
                return "".join(ch for ch in v if ch.isalnum())[:16] or "account"
            except Exception:
                return "account"

        def script_dir():
            base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
            if base and safe(lambda: os.path.isfile(base), False):
                base = os.path.dirname(base)
            return base

        def new_rec(serial):
            return {"s": serial, "parent": 0, "root": serial, "kind": "bag", "cs": 0, "cname": "",
                    "label": "", "custom": "", "facet": 0, "x": 0, "y": 0, "seen": 0.0, "mob": 0,
                    "plabel": "", "stub": False, "items": {}}

        def parse_file(text):
            """(records, tombstones) from the file's text; a damaged line is skipped.
            Item lines follow their container's line; a container written twice
            keeps its last block only."""
            recs, tombs = {}, {}
            for line in text.split("\n"):
                line = line.rstrip("\r")
                if not line or line.startswith("#"):
                    continue
                p = line.split("|")
                try:
                    if p[0] == "C" and len(p) >= 15:
                        s = int(p[1])
                        r = new_rec(s)
                        r.update({"parent": int(p[2]), "root": int(p[3]), "kind": p[4],
                                  "cs": int(p[5]), "cname": p[6], "label": p[7], "custom": p[8],
                                  "facet": int(p[9]), "x": int(p[10]), "y": int(p[11]),
                                  "seen": float(p[12]), "mob": int(p[13]), "plabel": p[14],
                                  "stub": len(p) > 15 and p[15] == "1"})
                        recs[s] = r
                    elif p[0] == "I" and len(p) >= 6:
                        r = recs.get(int(p[1]))
                        a = int(p[4])
                        if r is not None and a > 0:
                            name = p[5]
                            key = (int(p[2]), int(p[3]), name.lower())
                            e = r["items"].get(key)
                            if e is None:
                                r["items"][key] = [name, a]
                            else:
                                e[1] += a
                    elif p[0] == "D" and len(p) >= 3:
                        tombs[int(p[1])] = float(p[2])
                except (ValueError, IndexError):
                    continue
            return recs, tombs

        def file_text():
            out = [FILE_HEAD]
            for s, r in idx["recs"].items():
                out.append("C|%d|%d|%d|%s|%d|%s|%s|%s|%d|%d|%d|%d|%d|%s|%d" % (
                    s, r["parent"], r["root"], r["kind"], r["cs"], clean_text(r["cname"]),
                    clean_text(r["label"]), clean_text(r["custom"]), r["facet"], r["x"], r["y"],
                    int(r["seen"]), r["mob"], clean_text(r["plabel"]), 1 if r["stub"] else 0))
                for key, e in r["items"].items():
                    out.append("I|%d|%d|%d|%d|%s" % (s, key[0], key[1], e[1], clean_text(e[0])))
            for s, t in idx["tombs"].items():
                out.append("D|%d|%d" % (s, int(t)))
            return "\n".join(out) + "\n"

        def read_file(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                try:
                    import System
                    return str(System.IO.File.ReadAllText(path))
                except Exception:
                    return None

        def write_file(path, text):
            tmp = path + ".tmp"
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(text)
                try:
                    os.replace(tmp, path)
                except Exception:
                    if os.path.exists(path):
                        os.remove(path)
                    os.rename(tmp, path)
                return True
            except Exception as ex:
                idx["err"] = str(ex)[:60]
                try:
                    import System
                    System.IO.File.WriteAllText(path, text)
                    return True
                except Exception:
                    return False

        def mtime(path):
            try:
                return os.path.getmtime(path)
            except Exception:
                return None

        def merge(recs, tombs):
            """Another client's (or an earlier session's) records into ours: per
            container the newer one wins; a place forgotten after it was seen stays out."""
            changed = False
            mine = idx["recs"]
            cut = time.time() - settings["days"] * 86400.0
            for s, t in tombs.items():
                if t > idx["tombs"].get(s, 0.0):
                    idx["tombs"][s] = t
            for s, r in recs.items():
                if r["seen"] < cut:
                    continue                      # stale: not taken back in
                cur = mine.get(s)
                if cur is None or r["seen"] > cur["seen"]:
                    if cur is not None and cur["custom"] and not r["custom"]:
                        r["custom"] = cur["custom"]   # a name given on one side is kept
                    mine[s] = r
                    quick.pop(s, None)                # our next look reads it in full
                    changed = True
                elif r["custom"] and not cur["custom"]:
                    cur["custom"] = r["custom"]
                    changed = True
            for s in [s for s in mine if s in idx["tombs"] and mine[s]["seen"] <= idx["tombs"][s]]:
                del mine[s]
                changed = True
            return changed

        def prune():
            """Stale places out, then whole places (oldest first) until under the caps."""
            now = time.time()
            recs = idx["recs"]
            cut = now - settings["days"] * 86400.0
            tcut = now - TOMB_DAYS * 86400.0
            for s in [s for s, t in idx["tombs"].items() if t < tcut]:
                del idx["tombs"][s]
            if len(idx["tombs"]) > 4 * MAX_CONTAINERS:          # a cap: the oldest go first
                for s, _ in sorted(idx["tombs"].items(), key=lambda kv: kv[1])[:len(idx["tombs"]) -
                                                                             4 * MAX_CONTAINERS]:
                    del idx["tombs"][s]
            groups = {}
            for s, r in recs.items():
                g = groups.get(r["root"])
                if g is None:
                    g = groups[r["root"]] = [0.0, [], 0]
                g[0] = max(g[0], r["seen"])
                g[1].append(s)
                g[2] += len(r["items"])
            dropped = False
            for root in [k for k, g in groups.items() if g[0] < cut]:
                for s in groups.pop(root)[1]:
                    recs.pop(s, None)
                dropped = True
            n_recs = len(recs)
            n_items = sum(g[2] for g in groups.values())
            if n_recs > MAX_CONTAINERS or n_items > MAX_ITEMS:
                for root, g in sorted(groups.items(), key=lambda kv: kv[1][0]):
                    if n_recs <= MAX_CONTAINERS and n_items <= MAX_ITEMS:
                        break
                    for s in g[1]:
                        recs.pop(s, None)
                    n_recs -= len(g[1])
                    n_items -= g[2]
                    dropped = True
            return dropped

        def load_index():
            path = idx["path"]
            if not path:
                return
            text = read_file(path) if os.path.exists(path) else ""
            idx["mtime"] = mtime(path)
            if text:
                recs, tombs = parse_file(text)
                merge(recs, tombs)
            prune()
            idx["loaded"] = True
            idx["ver"] += 1

        def save_index():
            path = idx["path"]
            if not path:
                return
            mt = mtime(path)
            if mt is not None and mt != idx["mtime"]:
                text = read_file(path)            # another client wrote since: theirs first
                if text:
                    recs, tombs = parse_file(text)
                    if merge(recs, tombs):
                        idx["ver"] += 1
            if prune():
                idx["ver"] += 1
            if write_file(path, file_text()):
                idx["mtime"] = mtime(path)
                idx["dirty"] = False
                idx["err"] = ""

        def check_others():
            """Every MERGE_CHECK s: did another client write the file? Take their changes."""
            path = idx["path"]
            mt = mtime(path)
            if mt is None or mt == idx["mtime"]:
                return
            text = read_file(path)
            idx["mtime"] = mt
            if text:
                recs, tombs = parse_file(text)
                if merge(recs, tombs) | prune():
                    idx["ver"] += 1

        def mark_dirty():
            idx["ver"] += 1
            if not idx["dirty"]:
                idx["dirty"] = True
                idx["dirty_at"] = time.time()

        # ---------- reading containers (client thread) ----------
        def place_of(it):
            """(kind, root item, owner mobile or None) for the container `it`, or None
            when it isn't stored: your backpack (counted live), corpses, other
            people's containers, a kind switched off on the settings page."""
            cur, depth = it, 0
            while depth < 12:
                c = int(cur.Container or 0)
                if c == 0 or c < 0x40000000:
                    break
                nxt = API.FindItem(c)
                if nxt is None:
                    return None
                cur, depth = nxt, depth + 1
            else:
                return None
            owner = int(cur.Container or 0)
            top = int(cur.Serial)
            if int(cur.Graphic) in SKIP_GRAPHICS or int(it.Graphic) in SKIP_GRAPHICS:
                return None
            if owner == 0:
                if bool(safe(lambda: cur.IsCorpse, False)):
                    return None
                return ("chest", cur, None) if settings["ground"] else None
            me = API.Player
            if me is None:
                return None
            if owner == int(me.Serial):
                bank = int(API.Bank or 0)
                if bank and top == bank:
                    return ("bank", cur, None) if settings["bank"] else None
                return None                       # your backpack (live) or something you wear
            m = API.FindMobile(owner)
            if m is not None and bool(m.IsRenamable) and settings["pack"]:
                return ("pack", cur, m)
            return None

        def read_container(serial, final):
            """Read container `serial` and the bags in it the client knows: the
            result goes to thread_tick (reads). True when it was read, False when
            nothing has arrived in it yet, None when it isn't kept (or is gone)."""
            it = API.FindItem(serial)
            if it is None:
                return None
            place = place_of(it)
            if place is None:
                return None                       # not a container that is kept
            kind, top, mob = place
            me = API.Player
            if me is None:
                return None
            items = API.ItemsInContainer(serial, True) or []
            # a quick look first (three reads an item): unchanged since the last read
            # of it, only its "seen" time moves (no file write, no new summary).
            # (2.6.82) what it read is kept for the full read below
            q, n = 0, 0
            first = []
            for x in items:
                n += 1
                if n > READ_MAX:
                    break
                try:
                    xs, am, xc = int(x.Serial), x.Amount, int(x.Container)
                    q = (q * 31 + xs + 7 * int(am or 0) + 13 * xc) & 0xFFFFFFFFFFFF
                except Exception:
                    first.append(None)
                    continue
                first.append((xs, am, xc))
            sig = (q, n)
            if quick.get(serial) == sig and serial in idx["recs"]:
                if len(reads) < 40:
                    reads.append({"serial": serial, "same": True, "at": time.time()})
                return True
            cs, cname = int(me.Serial), str(me.Name or "")
            try:
                facet = int(API.GetMap())
            except Exception:
                facet = 0
            by = {serial: []}
            parents, names = {}, {}
            n = 0
            capped = False
            for x in items:
                n += 1
                if n > READ_MAX:
                    capped = True
                    break
                try:
                    f = first[n - 1]
                    if f is not None:
                        xs, am, c = f
                        a = max(1, int(am or 1))
                    else:
                        xs = int(x.Serial)
                        c = int(x.Container)
                        a = None
                    g = int(x.Graphic)
                    h = int(x.Hue)
                    if a is None:
                        a = max(1, int(x.Amount or 1))
                    name = item_name(x, g, a)
                    if bool(x.IsContainer):
                        parents[xs] = c           # a bag in it (its contents only if the client has them)
                        names[xs] = name
                except Exception:
                    continue
                lst = by.get(c)
                if lst is None:
                    lst = by[c] = []
                lst.append((g, h, a, name))
            if not by[serial] and not final and len(by) == 1:
                return False                      # nothing arrived yet: the next read will tell
            top_serial = int(top.Serial)
            top_name = item_name(top, int(top.Graphic), 1)
            if kind == "bank":
                label = ("Bank box (%s)" % cname) if cname else "Bank box"
            elif kind == "chest":
                label = "%s at %d, %d" % (top_name or "Chest", int(top.X), int(top.Y))
            else:
                body = int(safe(lambda: mob.Graphic, 0) or 0)
                label = "%s %s" % (PACK_BODIES.get(body, "Pack animal"), str(mob.Name or ""))
                label = label.strip()
            res = {"serial": serial, "parent": int(it.Container or 0), "kind": kind,
                   "root": top_serial, "label": label, "top_name": top_name,
                   "own_name": item_name(it, int(it.Graphic), 1), "cs": cs, "cname": cname,
                   "facet": facet, "x": int(top.X), "y": int(top.Y),
                   "mob": int(mob.Serial) if mob is not None else 0, "by": by,
                   "parents": parents, "names": names, "capped": capped, "at": time.time()}
            if len(reads) < 40:
                reads.append(res)
                if len(quick) > 200:
                    quick.clear()
                quick[serial] = sig
            return True

        def under(recs, s, anc):
            """Is record s (or a record below it) under anc, by parent links?"""
            depth = 0
            while s and depth < 14:
                if s == anc:
                    return True
                r = recs.get(s)
                if r is None:
                    return False
                s, depth = r["parent"], depth + 1
            return False

        def integrate(res):
            """A read into the index (thread_tick): the container and the bags in it
            replace what was noted of them (bags no longer in it drop out); the
            place they are in keeps its record (one is made to carry its name
            when only a bag inside it was read)."""
            recs = idx["recs"]
            if res.get("same"):
                serial, now, root = res["serial"], res["at"], None
                for s, r in recs.items():
                    if under(recs, s, serial):
                        r["seen"] = now
                        root = r["root"]
                p = summ["places"].get(root) if root is not None else None
                if p is not None:
                    p["seen"] = now
                    view["dirty"] = True
                return
            serial, root, now = res["serial"], res["root"], res["at"]
            if serial == root:
                old = [s for s, r in recs.items() if r["root"] == root or s == root]
            else:
                old = [s for s in recs if under(recs, s, serial)]
            place = {"kind": res["kind"], "root": root, "cs": res["cs"], "cname": res["cname"],
                     "facet": res["facet"], "x": res["x"], "y": res["y"], "mob": res["mob"],
                     "plabel": res["label"]}
            # a bag still in it whose contents the client doesn't show now is kept
            # as it was (and the bags inside that one); a read cut short keeps all
            parents = res["parents"]
            keep = set()
            for s in old:
                if s not in res["by"] and s != root and (s in parents or res["capped"]):
                    keep.add(s)
            more = True
            while more:
                more = False
                for s in old:
                    if s not in keep and s not in res["by"] and s != root \
                            and recs[s]["parent"] in keep:
                        keep.add(s)
                        more = True
            customs = {}
            gone = []
            for s in old:
                r = recs[s]
                if s in keep:
                    r.update(place)
                    r["kind"] = "bag"
                    if s in parents:
                        r["parent"] = parents[s]
                    continue
                if s in res["by"] and r["custom"]:
                    customs[s] = r["custom"]
                elif s not in res["by"]:
                    gone.append(s)
                del recs[s]                           # read again just now (below), or gone
            tombs = idx["tombs"]
            for s in gone:                            # no longer in it: remembered as gone, so a
                tombs[s] = now                        # second client's older copy can't bring it back
            if serial != root:
                rr = recs.get(root)
                if rr is None:
                    rr = recs[root] = new_rec(root)
                    rr["stub"] = True                 # the place itself, until it is opened
                rr.update(place)
                rr["parent"] = 0
                rr["label"] = res["label"]
                if rr["stub"]:
                    rr["seen"] = max(rr["seen"], now)
            for cont, lst in res["by"].items():
                r = new_rec(cont)
                r.update(place)
                r["custom"] = customs.get(cont, "")
                r["seen"] = now
                if cont == root:
                    r["parent"], r["label"] = 0, res["label"]
                elif cont == serial:
                    r["kind"], r["parent"], r["label"] = "bag", res["parent"], res["own_name"]
                else:
                    r["kind"], r["parent"] = "bag", res["parents"].get(cont, 0)
                    r["label"] = res["names"].get(cont, "Bag")
                items = r["items"]
                for g, h, a, name in lst:
                    k = (g, h, name.lower())
                    e = items.get(k)
                    if e is None:
                        items[k] = [name, a]
                    else:
                        e[1] += a
                recs[cont] = r
                idx["tombs"].pop(cont, None)
            idx["tombs"].pop(root, None)
            prune()                               # the caps hold at every moment
            mark_dirty()
            view["last_read"] = (res["label"], now)
            if settings["say"]:
                nk = sum(len(v) for v in res["by"].values())
                nb = len(res["by"]) - 1
                what = res["label"] if serial == root else "%s in %s" % (res["own_name"], res["label"])
                API.SysMsg("%s: read %s: %d kind%s of item%s." % (
                    TITLE, what, nk, "" if nk == 1 else "s",
                    (", %d bag%s inside" % (nb, "" if nb == 1 else "s")) if nb else ""),
                    Kit.HUE_INFO)

        def on_open(*args):
            """API.Events.OnOpenContainer (script thread): only noted here."""
            if not st["active"]:
                return
            for a in reversed(args):
                s = None
                try:
                    s = int(a)
                except Exception:
                    try:
                        s = int(a.Serial)
                    except Exception:
                        s = None
                if s and s >= 0x40000000:
                    if len(opens) < 40:
                        opens.append(s)
                    return

        def hook_events():
            """Subscribe once a session (subscriptions can't be taken back; the
            handler does nothing while the module is off)."""
            if st["hooked"]:
                return
            st["hooked"] = True
            try:
                API.Events.OnOpenContainer(on_open)
                st["events"] = True
            except Exception:
                st["events"] = False

        def poll_open_gumps():
            """Fallback when the open event isn't there: the container windows the
            client has open, read by reflection once a second."""
            Typing._find()
            uim = Typing.uim
            if uim is None:
                return
            gumps = Typing._get(None, "Gumps", uim)
            if gumps is None:
                return
            now_open = set()
            try:
                for g in gumps:
                    try:
                        tn = str(g.GetType().Name)
                        if "Container" not in tn:
                            continue
                        s = int(g.LocalSerial)
                    except Exception:
                        continue
                    if s >= 0x40000000:
                        now_open.add(s)
            except Exception:
                return
            for s in now_open - known_open:
                note_open(s)
            known_open.clear()
            known_open.update(now_open)

        def note_open(serial):
            now = time.time()
            w = watching.get(serial)
            if w is None and len(watching) >= WATCH_CAP:
                oldest = min(watching, key=lambda k: watching[k][0])
                watching.pop(oldest, None)
            watching[serial] = [now, now + READ_DELAYS[0], 0]

        def watch_tick(now):
            """Read the watched containers when due; a closed one gets one last read."""
            if not watching:
                return
            check = now >= st.get("check_at", 0.0) or st.get("check_at", 0.0) - now > OPEN_CHECK
            if check:
                st["check_at"] = now + OPEN_CHECK
            for serial in list(watching):
                w = watching[serial]
                closed = False
                if check and w[2] >= len(READ_DELAYS):
                    it = API.FindItem(serial)
                    closed = it is None or not bool(it.Opened)
                    if it is None:
                        watching.pop(serial, None)
                        continue
                if closed or now - w[0] > WATCH_MAX:
                    read_container(serial, True)
                    watching.pop(serial, None)
                    continue
                if now < w[1] and w[1] - now <= REREAD_SECS + 1.0:
                    continue
                done = read_container(serial, w[2] >= len(READ_DELAYS) - 1)
                if done is None:
                    watching.pop(serial, None)      # gone, or not a container that is kept
                    continue
                w[2] += 1
                if w[2] < len(READ_DELAYS):
                    w[1] = w[0] + READ_DELAYS[w[2]]
                else:
                    w[1] = now + REREAD_SECS

        # ---------- the summary the window searches (thread_tick) ----------
        def build_summary():
            keys, places = {}, {}
            recs = idx["recs"]
            chars = set()
            n = 0
            for s, r in recs.items():
                root = r["root"]
                p = places.get(root)
                if p is None:
                    rr = recs.get(root)
                    src = rr if rr is not None else r
                    label = src["custom"] or src["label"] or r["plabel"] or "A container"
                    p = places[root] = {"label": label, "seen": 0.0, "kind": src["kind"],
                                        "mob": src["mob"], "cname": src["cname"],
                                        "facet": src["facet"], "x": src["x"], "y": src["y"]}
                if r["seen"] > p["seen"]:
                    p["seen"] = r["seen"]
                if r["cname"]:
                    chars.add(r["cname"])
                for key, e in r["items"].items():
                    n += 1
                    k = keys.get(key)
                    if k is None:
                        k = keys[key] = [e[0], {}]
                    k[1][root] = k[1].get(root, 0) + e[1]
            summ.update({"ver": idx["ver"], "keys": keys, "places": places, "items": n,
                         "chars": len(chars)})
            view["dirty"] = True

        def fav_stored():
            """[(total, {place: amount})] of each favourite in the stored places
            (worked out in thread_tick after each new summary; here only when the
            favourites themselves changed)."""
            key = (summ["ver"], tuple(t for _, t in favs))
            if fcache["key"] != key:
                stats = []
                keys = summ["keys"]
                for label, term in favs:
                    terms = parse_terms(term)
                    total, per = 0, {}
                    for k, e in keys.items():
                        if matches(terms, k):
                            for root, a in e[1].items():
                                per[root] = per.get(root, 0) + a
                                total += a
                    stats.append((total, per))
                fcache["key"], fcache["stats"] = key, stats
            return fcache["stats"]

        def search_stored(q):
            """{place: {item key: (name, amount)}} for a search, in the stored places
            (cached per search and summary)."""
            key = (summ["ver"], q.lower())
            if scache["key"] != key:
                terms = parse_terms(q)
                by = {}
                for k, e in summ["keys"].items():
                    if matches(terms, k):
                        for root, a in e[1].items():
                            d = by.get(root)
                            if d is None:
                                d = by[root] = {}
                            d[k] = (e[0], a)
                scache["key"], scache["by"] = key, by
            return scache["by"]

        # ---------- services for other modules ----------
        def svc_find(text):
            """HOST.services["storage.find"](text): [(place, item name, amount, seen)]
            of the stored places holding it (your backpack not included)."""
            terms = parse_terms(text)
            out = []
            if not terms:
                return out
            places = summ["places"]
            for key, e in summ["keys"].items():
                if matches(terms, key):
                    for root, a in e[1].items():
                        p = places.get(root)
                        if p is not None:
                            out.append((p["label"], e[0], a, p["seen"]))
            out.sort(key=lambda t: -t[2])
            return out

        def svc_total(graphic, hue=None):
            """HOST.services["storage.total"](graphic, hue=None): how many are stored
            across the account (your backpack not included)."""
            n = 0
            for key, e in summ["keys"].items():
                if key[0] == graphic and (hue is None or key[1] == hue):
                    for a in e[1].values():
                        n += a
            return n

        # ---------- the window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        def row_click(i):
            def handler(*args):
                alt = Follow.alt_held()             # read at the click: it may be up by the tick
                if len(st["queue"]) < 20:
                    st["queue"].append(("row", i, alt, time.time()))
            return handler

        def build_window():
            x, y = Kit.load_pos(POS_KEY, (240, 160), (W, H))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            store = ({}, {})
            c = {}
            rows = []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                w, h = MINI_W, MINI_H
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                w, h = W, H
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                # the Find section: the box, Add favourite; Name, Forget, the pages
                Kit.add_section(g, M, Y_FIND, IW, H_FIND)
                fav_w = 35 + Kit.text_w("Add favourite")
                Kit.add_label(g, "Find:", M + 10, Y_FIND + 12, Kit.HUE_TEXT)
                bx = M + 16 + Kit.text_w("Find:")
                bw = IW - (bx - M) - fav_w - 22
                c["box"] = Kit.add_textbox(g, view["query"], bx, Y_FIND + 9, bw, numbers=False)
                safe(lambda: c["box"].SetTooltip("Part of an item's name, or a graphic (0x0F88); "
                                                 "commas for several. Empty: your favourites."))
                Kit.art_button(g, store, "fav", Kit.ART_OK, M + IW - fav_w - 6, Y_FIND + 8,
                               "Add favourite", "Add what is in the Find box to your favourites "
                               "(the list shown when the box is empty)", on_click=queue("fav"))
                yb = Y_FIND + 36
                xb = M + 10
                Kit.art_button(g, store, "name", Kit.ART_OK, xb, yb, "Name",
                               "Give the picked place a name of your own: click a place, type the "
                               "name in the Find box, then click Name again",
                               on_click=queue("name"))
                xb += 35 + Kit.text_w("Name") + 12
                Kit.art_button(g, store, "forget", Kit.ART_CLOSE, xb, yb, "Forget",
                               "Take the picked place, and the bags in it, out of the index "
                               "(click twice)", on_click=queue("forget"))
                nx_w = 35 + Kit.text_w("Next")
                xn = M + IW - nx_w - 6
                Kit.art_button(g, store, "next", Kit.ART_PAGE, xn, yb, "Next", "Next page",
                               on_click=queue("next"))
                xp = xn - 12 - (35 + Kit.text_w("Prev"))
                Kit.art_button(g, store, "prev", Kit.ART_PAGE, xp, yb, "Prev", "Previous page",
                               on_click=queue("prev"))
                c["page"] = Kit.add_label(g, "", xp - 50, yb + 3, Kit.HUE_INFO)
                # the result rows (a pool, relabelled; never rebuilt per search)
                Kit.add_section(g, M, Y_LIST, IW, H_LIST)
                for i in range(ROWS):
                    ry = Y_LIST + 8 + i * ROW_H
                    r = {"l": Kit.add_label(g, "", M + 10, ry, Kit.HUE_TEXT),
                         "r": Kit.add_label(g, "", M + IW - 60, ry, Kit.HUE_INFO),
                         "lx": M + 10, "rx": M + IW - 60, "tip": "", "y": ry}
                    r["c"] = Kit.catcher(g, M + 4, ry - 2, IW - 8, ROW_H, row_click(i))
                    rows.append(r)
                Kit.add_section(g, M, Y_STAT, IW, H_STAT)
                c["status"] = Kit.add_label(g, "", M + 10, Y_STAT + 7, Kit.HUE_INFO)
            Kit.place(g, x, y, w, h)
            if safe(lambda: HOST.layout_locked(KEY), False):
                safe(lambda: setattr(g, "CanMove", False))   # 2.6.81 (IN2-3): held in its zone
            win.update({"g": g, "c": c, "store": store, "rows": rows})
            view["data"] = [None] * len(rows)
            view["prev"] = [(None, 0.0)] * len(rows)
            view["seen_text"] = None
            view["built_for"] = None
            view["dirty"] = True
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:
                safe(lambda: setattr(g, "IsVisible", False))
            refresh(time.time())
            Kit.dispose(old)

        def full_shown():
            return win["g"] is not None and not st["minimized"] and not st["docked"]

        def set_status(text, hue=None):
            view["status"] = text
            view["status_hue"] = Kit.HUE_INFO if hue is None else hue
            view["status_at"] = time.time()

        def idle_status():
            n = len(summ["places"])
            if not idx["loaded"]:
                return "Reading the index"
            if idx["err"]:
                return "Index file: %s" % idx["err"]
            label, t = view["last_read"]
            s = "%d place%s noted" % (n, "" if n == 1 else "s")
            if summ["chars"] > 1:
                s += " on %d characters" % summ["chars"]
            if label:
                s += "; last read %s" % label
            return s

        def place_tip(p, root):
            where = ""
            if p["kind"] == "chest":
                where = " (facet %d, %d, %d)" % (p["facet"], p["x"], p["y"])
            who = (" by %s" % p["cname"]) if p["cname"] else ""
            tip = "%s\nSeen%s %s%s\nClick to pick it (then Name or Forget)" % (
                p["label"], who, ago(max(0.0, time.time() - p["seen"])), where)
            if p["mob"]:
                tip += "\n" + FOLLOW_TIP
            return tip

        def results(now):
            """The rows for the current query (or the favourites with the box empty)."""
            rows = []
            live = view["live"]
            places = summ["places"]
            q = view["query"]
            if not q:
                if not favs:
                    return [("No favourites yet. Type what to look for, then click Add favourite.",
                             "", Kit.HUE_INFO, 0, "", None)]
                rows.append(("FAVOURITES  (click one to see where)", "", Kit.HUE_TITLE, 0,
                             "Totals across the account: every place noted, and your backpack now",
                             None))
                stats = fav_stored()
                for i, (label, term) in enumerate(favs):
                    terms = parse_terms(term)
                    total, per = stats[i] if i < len(stats) else (0, {})
                    mine = 0
                    for key, e in live.items():
                        if matches(terms, key):
                            mine += e[1]
                    total += mine
                    n = len(per) + (1 if mine else 0)
                    lines = []
                    if mine:
                        lines.append("On you now: %s" % num(mine))
                    for root, a in sorted(per.items(), key=lambda kv: -kv[1])[:10]:
                        p = places.get(root)
                        lines.append("%s: %s" % (p["label"] if p else "?", num(a)))
                    tip = "%s (%s)\n%s\nClick to see where" % (label, term, "\n".join(lines)
                                                             if lines else "None noted")
                    rows.append((label, ("%s in %d place%s" % (num(total), n, "" if n == 1 else "s"))
                                 if total else "none", Kit.HUE_TEXT, 0, tip, ("fav", term)))
                return rows
            terms = parse_terms(q)
            by_place = search_stored(q)
            mine = {}
            for key, e in live.items():
                if matches(terms, key):
                    mine[key] = (e[0], e[1])
            n = len(by_place) + (1 if mine else 0)
            if not n:
                return [("Nothing noted holds \"%s\"." % q, "", Kit.HUE_INFO, 0,
                         "Open the container it is in once (bank box, chest, pack animal) "
                         "and it is noted", None)]
            sums, names = {}, {}                  # place -> how many it holds; kind -> its name
            for root, d in by_place.items():      # (one pass over the matches)
                t = 0
                for k, v in d.items():
                    t += v[1]
                    names[k] = v[0]
                sums[root] = t
            total = sum(sums.values()) + sum(a for _, a in mine.values())
            for k, v in mine.items():
                names[k] = v[0]
            name = list(names.values())[0] if len(names) == 1 else "%d kinds" % len(names)
            rows.append((name, "%s in %d place%s" % (num(total), n, "" if n == 1 else "s"),
                         Kit.HUE_TITLE, 0, "Everything noted that matches \"%s\"" % q, None))
            # (built on the client thread: a broad search of a full index stops at
            # MAX_RESULT_ROWS lines, the rest counted in one last line)
            left = 0
            if mine:
                me_name = str(safe(lambda: API.Player.Name, "") or "")
                rows.append(("Backpack%s" % ((" (%s)" % me_name) if me_name else ""), "on you now",
                             Kit.HUE_TITLE, 0, "Your backpack and the bags in it, right now", None))
                lst = sorted(mine.items(), key=lambda kv: -kv[1][1])
                room = max(0, MAX_RESULT_ROWS - len(rows))
                left += max(0, len(lst) - room)
                for key, (nm, a) in lst[:room]:
                    rows.append((nm, num(a), Kit.HUE_TEXT, 14,
                                 "%s x%s on you (graphic 0x%04X, hue %d)" % (nm, num(a), key[0], key[1]),
                                 None))
            order = sorted(by_place.items(), key=lambda kv: -sums[kv[0]])
            for root, d in order:
                p = places.get(root)
                if p is None:
                    continue
                if len(rows) >= MAX_RESULT_ROWS:
                    left += 1 + len(d)
                    continue
                hue = Kit.HUE_GOOD if view["sel"] == root else Kit.HUE_TITLE
                rows.append((p["label"], "seen %s" % ago(max(0.0, now - p["seen"])), hue, 0,
                             place_tip(p, root), ("place", root, p["mob"], True)))
                data = ("place", root, p["mob"], False)
                lst = sorted(d.items(), key=lambda kv: -kv[1][1])
                room = max(0, MAX_RESULT_ROWS - len(rows))
                left += max(0, len(lst) - room)
                for key, (nm, a) in lst[:room]:
                    tip = "%s x%s in %s (graphic 0x%04X, hue %d)\nClick to pick this place" % (
                        nm, num(a), p["label"], key[0], key[1])
                    if p["mob"]:
                        tip += "\n" + FOLLOW_TIP
                    rows.append((nm, num(a), Kit.HUE_TEXT, 14, tip, data))
            if left:
                rows.append(("... and %s more line%s: type more of the name" % (
                    num(left), "" if left == 1 else "s"), "", Kit.HUE_INFO, 0,
                    "A search lists %d lines at most; the total above counts them all"
                    % MAX_RESULT_ROWS, None))
            return rows

        def refresh(now):
            """Draw what changed (client thread). Hidden: nothing; minimized: the status."""
            g = win["g"]
            if g is None or st["docked"]:
                return
            c = win["c"]
            if st["minimized"]:
                n = len(summ["places"])
                view["status_key"] = None
                Kit.set_text(c.get("status"), TITLE + ": " + ("%d place%s noted" % (n, "" if n == 1 else "s")
                                                              if idx["loaded"] else "reading the index"),
                             Kit.HUE_INFO)
                return
            key = (view["query"], summ["ver"], view["live_ver"], view["sel"], view["page"],
                   int(now // 30))                 # (the "seen" times age)
            if view["dirty"] or key != view["built_for"]:
                view["dirty"] = False
                view["built_for"] = key
                view["rows"] = results(now)
                pages = max(1, (len(view["rows"]) + ROWS - 1) // ROWS)
                if view["page"] >= pages:
                    view["page"] = pages - 1
                    view["built_for"] = (key[0], key[1], key[2], key[3], view["page"], key[5])
                draw_rows(now, pages)
            if view["status"] and view["naming"] is None and not 0 <= now - view["status_at"] <= 8.0:
                view["status"] = ""                # a note lasts 8 s (the naming prompt stays)
            # (2.6.82) the line is made and fitted only when what it says changed
            lbl = c.get("status")
            skey = (lbl, view["status"], view["status_hue"], idx["loaded"], idx["err"],
                    len(summ["places"]), summ["chars"], view["last_read"])
            old = view.get("status_key")
            if old is not None and old[0] is lbl and old[1:] == skey[1:]:
                return
            view["status_key"] = skey
            Kit.set_text(lbl, Kit.fit(view["status"] or idle_status(), IW - 20),
                         view["status_hue"] if view["status"] else Kit.HUE_INFO)

        def draw_rows(now, pages):
            rows = win["rows"]
            off = view["page"] * ROWS
            data, prev = view["data"], view["prev"]
            right_edge = M + IW - 10
            for i, r in enumerate(rows):
                j = off + i
                if j < len(view["rows"]):
                    lt, rt, hue, indent, tip, d = view["rows"][j]
                else:
                    lt, rt, hue, indent, tip, d = "", "", Kit.HUE_TEXT, 0, "", None
                rw = Kit.text_px(rt) if rt else 0
                lx = M + 10 + indent
                room = right_edge - lx - (rw + 8 if rt else 0)
                Kit.set_text(r["l"], Kit.fit(lt, room) if lt else "", hue)
                Kit.set_text(r["r"], rt, Kit.HUE_INFO)
                if lx != r["lx"]:
                    r["lx"] = lx
                    try:
                        Kit.ui_pos(r["l"], lx, r["y"])
                    except Exception:
                        pass
                rx = right_edge - rw
                if rt and rx != r["rx"]:
                    r["rx"] = rx
                    try:
                        Kit.ui_pos(r["r"], rx, r["y"])
                    except Exception:
                        pass
                if tip != r["tip"]:
                    r["tip"] = tip
                    try:
                        r["c"].SetTooltip(tip)
                    except Exception:
                        pass
                if d != data[i]:
                    prev[i] = (data[i], now)
                    data[i] = d
            c = win["c"]
            Kit.set_text(c.get("page"), "%d / %d" % (view["page"] + 1, pages) if pages > 1 else "",
                         Kit.HUE_INFO)

        def poll_box(now):
            """The Find box, read in place on the client thread (nothing waits)."""
            box = win["c"].get("box")
            if box is None:
                return
            try:
                t = str(box.Text or "")
            except Exception:
                return
            if t != view["seen_text"]:
                if view["seen_text"] is not None:
                    view["changed_at"] = now
                view["seen_text"] = t
                return
            if view["changed_at"] and (now - view["changed_at"] >= SEARCH_WAIT
                                       or now < view["changed_at"]):
                view["changed_at"] = 0.0
                if view["naming"] is not None:
                    return                         # the box holds a name being typed
                q = t.strip()
                if q.lower() != view["query"].lower():
                    view["query"] = q
                    view["page"] = 0
                    view["dirty"] = True

        def set_box(text):
            box = win["c"].get("box")
            view["seen_text"] = text
            view["changed_at"] = 0.0
            if box is not None:
                try:
                    box.SetText(text)
                except Exception:
                    try:
                        box.Text = text
                    except Exception:
                        pass

        def live_tick(now):
            if not full_shown():
                return
            if now < view["live_at"] and view["live_at"] - now <= LIVE_EVERY:
                return
            view["live_at"] = now + LIVE_EVERY
            live = {}
            # (2.6.82) the mother's shared backpack list (one deep scan for every
            # module that counts the pack; up to 1 s old, this looks every 3 s)
            try:
                items = HOST.pack_items(True, 1.0)
            except Exception:
                try:
                    bp = int(API.Backpack or 0)      # (a serial, not an item: 2.6.52 fix)
                except Exception:
                    bp = 0
                items = (API.ItemsInContainer(bp, True) or []) if bp else []
            q, n = 0, 0
            for x in items:
                n += 1
                if n > READ_MAX:
                    break
                try:
                    q = (q * 31 + int(x.Serial) + 7 * int(x.Amount or 0) + 13 * int(x.Container)) \
                        & 0xFFFFFFFFFFFF
                except Exception:
                    continue
            if (q, n) == view["live_sig"]:
                return                            # nothing moved in your backpack
            view["live_sig"] = (q, n)
            if items:
                n = 0
                for x in items:
                    n += 1
                    if n > READ_MAX:
                        break
                    try:
                        g, h = int(x.Graphic), int(x.Hue)
                        a = max(1, int(x.Amount or 1))
                        name = item_name(x, g, a)
                    except Exception:
                        continue
                    k = (g, h, name.lower())
                    e = live.get(k)
                    if e is None:
                        live[k] = [name, a]
                    else:
                        e[1] += a
            if live != view["live"]:
                view["live"] = live
                view["live_ver"] += 1

        def resolve_row(i, t):
            """The row's data as the player saw it when they clicked."""
            if i >= len(view["data"]):
                return None
            old, changed = view["prev"][i]
            if changed and (changed >= t or t - changed < 0.15):
                return old                         # it changed under the click: what they saw
            return view["data"][i]

        def end_naming():
            if view["naming"] is not None:
                view["naming"] = None
                set_box(view["query"])

        def do_action(action, now):
            kind = action[0] if isinstance(action, tuple) else action
            if action == "settings":
                HOST.show_settings(KEY)
            elif action == "show":                       # (2.6.85) the bag sidebar's Storage
                if st["minimized"] or st["docked"]:
                    st["minimized"] = st["docked"] = False
                    HOST.dock_forget(KEY)
                    Kit.save_min(MIN_KEY, False)
                    build_window()
                safe(lambda: Kit.client_control(win["g"]).BringOnTop())
            elif action == "toggle_min":
                st["minimized"] = not st["minimized"]
                st["docked"] = False
                HOST.dock_forget(KEY)
                Kit.save_min(MIN_KEY, st["minimized"])
                build_window()
            elif action == "to_bar":
                HOST.dock_to_bar(KEY, TITLE)
            elif action == "redraw":
                build_window()
            elif kind == "follow":
                Follow.toggle(action[1], TITLE)
            elif kind == "row":
                _, i, alt, t = action
                d = resolve_row(i, t)
                if d is None:
                    return
                if alt:
                    if len(d) > 2 and d[2]:
                        Follow.toggle(d[2], TITLE)
                    return
                end_naming()
                if d[0] == "fav":
                    view["query"] = d[1]
                    view["page"] = 0
                    set_box(d[1])
                    set_status("")
                elif d[0] == "place":
                    # its own row picks it or lets it go again; an item row picks it
                    view["sel"] = None if (d[3] and view["sel"] == d[1]) else d[1]
                    p = summ["places"].get(view["sel"]) if view["sel"] else None
                    set_status(("Picked: %s" % p["label"]) if p else "")
                view["dirty"] = True
            elif action == "fav":
                end_naming()
                q = view["query"] or (view["seen_text"] or "").strip()
                if not q:
                    set_status("Type what to look for first (a name, or a graphic like 0x0F88).",
                               Kit.HUE_BAD)
                elif any(t.lower() == q.lower() for _, t in favs):
                    set_status("\"%s\" is already a favourite." % q)
                elif len(favs) >= MAX_FAVS:
                    set_status("%d favourites at most: take one off on the settings page." % MAX_FAVS,
                               Kit.HUE_BAD)
                else:
                    favs.append([clean_text(q)[:NAME_MAX], clean_text(q)])
                    save_favs()
                    safe(lambda: HOST.refresh_settings(KEY))
                    set_status("Added \"%s\" to the favourites." % q, Kit.HUE_GOOD)
                view["dirty"] = True
            elif action == "name":
                sel = view["sel"]
                p = summ["places"].get(sel) if sel else None
                if view["naming"] is not None:
                    root = view["naming"]
                    text = clean_text(view["seen_text"] or "")[:NAME_MAX]
                    r = idx["recs"].get(root)
                    view["naming"] = None
                    if r is not None:
                        r["custom"] = text
                        mark_dirty()
                        set_status(("Named it \"%s\"." % text) if text else "Its own name is back.",
                                   Kit.HUE_GOOD)
                    set_box(view["query"])
                elif p is None or sel not in idx["recs"]:
                    set_status("Click a place in the list first, then Name.", Kit.HUE_BAD)
                else:
                    view["naming"] = sel
                    set_box(p["label"])
                    set_status("Type its new name in the Find box, then click Name again "
                               "(empty: its own name).", Kit.HUE_TITLE)
            elif action == "forget":
                end_naming()
                sel = view["sel"]
                p = summ["places"].get(sel) if sel else None
                arm, at = view["forget_arm"]
                if p is None:
                    set_status("Click a place in the list first, then Forget.", Kit.HUE_BAD)
                elif arm == sel and 0 <= now - at <= 4.0:
                    view["forget_arm"] = (None, 0.0)
                    forget_place(sel)
                    view["sel"] = None
                    set_status("Forgot %s." % p["label"], Kit.HUE_GOOD)
                else:
                    view["forget_arm"] = (sel, now)
                    set_status("Click Forget again to forget %s (and the bags in it)." % p["label"],
                               Kit.HUE_TITLE)
            elif action in ("next", "prev"):
                pages = max(1, (len(view["rows"]) + ROWS - 1) // ROWS)
                view["page"] = max(0, min(pages - 1, view["page"] + (1 if action == "next" else -1)))
                view["dirty"] = True

        def forget_place(root):
            recs = idx["recs"]
            now = time.time()
            for s in [s for s, r in recs.items() if r["root"] == root or s == root]:
                del recs[s]
                idx["tombs"][s] = now
            mark_dirty()

        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        H_S1 = 134                  # (2.6.52: the debug box moved to its own DEBUG section)
        H_S3 = 92
        H_DEBUG = 60

        def fav_h():
            return 32 + max(1, len(favs)) * 24 + 8

        def config_height(w):
            return H_S1 + Kit.GAP + fav_h() + Kit.GAP + H_S3 + Kit.GAP + H_DEBUG

        def build_config(g, x, y, w):
            store = ({}, {})
            c = {}
            Kit.add_section(g, x, y, w, H_S1, "WHAT IT NOTES  (when you open a container)")
            c["bank"] = Kit.add_check(g, "Bank boxes (and the bags in them)", x + 12, y + 30,
                                      settings["bank"],
                                      "Note what your bank box and the bags in it hold when you open it")
            c["ground"] = Kit.add_check(g, "Chests and containers on the ground (in houses too)",
                                        x + 12, y + 54, settings["ground"],
                                        "Note what a chest or other container on the ground holds "
                                        "when you open it")
            c["pack"] = Kit.add_check(g, "Your pack animals' packs", x + 12, y + 78, settings["pack"],
                                      "Note what your pack horse, llama or beetle carries when you "
                                      "open its pack")
            Kit.add_label(g, "Forget places not seen for:", x + 12, y + 104)
            dx = x + 18 + Kit.text_w("Forget places not seen for:")
            c["days"] = Kit.add_textbox(g, str(settings["days"]), dx, y + 101, 44)
            safe(lambda: c["days"].SetTooltip("Days a place stays in the index after it was last "
                                              "opened (1-3650)"))
            Kit.add_label(g, "days", dx + 52, y + 104, Kit.HUE_INFO)
            y2 = y + H_S1 + Kit.GAP
            Kit.add_section(g, x, y2, w, fav_h(), "FAVOURITES  (shown when the Find box is empty)")
            if not favs:
                Kit.add_label(g, "No favourites yet. Type something in the " + TITLE + " window's "
                              "Find box, then click Add favourite.", x + 12, y2 + 32, Kit.HUE_INFO)
            for i, (label, term) in enumerate(favs):
                ry = y2 + 30 + i * 24
                Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + 12, ry, None,
                               "Take %s off the favourites" % label)
                Kit.add_label(g, Kit.fit(label, 170), x + 48, ry + 3, Kit.HUE_TEXT)
                Kit.add_label(g, Kit.fit(term, w - 240), x + 226, ry + 3, Kit.HUE_INFO)
            y3 = y2 + fav_h() + Kit.GAP
            Kit.add_section(g, x, y3, w, H_S3, "THE INDEX  (every character of the account)")
            n = len(summ["places"])
            Kit.add_label(g, Kit.fit("%d place%s, %d container%s, %d item line%s, %d character%s" % (
                n, "" if n == 1 else "s", len(idx["recs"]), "" if len(idx["recs"]) == 1 else "s",
                summ["items"], "" if summ["items"] == 1 else "s", summ["chars"],
                "" if summ["chars"] == 1 else "s"), w - 24), x + 12, y3 + 30, Kit.HUE_TEXT)
            fname = os.path.basename(idx["path"]) if idx["path"] else "(not known yet)"
            Kit.add_label(g, Kit.fit("File: %s, next to Virtue Assistant" % fname, w - 24),
                          x + 12, y3 + 50, Kit.HUE_INFO)
            c["wipe_lbl"] = Kit.art_button(g, store, "wipe", Kit.ART_CLOSE, x + 12, y3 + 64,
                                           "Forget everything",
                                           "Empty the whole index for every character of the "
                                           "account (click twice)")
            y4 = y3 + H_S3 + Kit.GAP
            Kit.add_section(g, x, y4, w, H_DEBUG, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print every container read in the journal", x + 12, y4 + 30,
                                     settings["say"],
                                     "One line per container read: what it is and how many kinds of "
                                     "item it holds, to check the shard's names")
            page.update({"c": c, "store": store, "wipe_at": 0.0})

        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for k in ("bank", "ground", "pack", "say"):
                try:
                    v = bool(c[k].IsChecked)
                except Exception:
                    v = settings[k]
                if v != settings[k]:
                    settings[k] = v
                    changed = True
            try:
                d = int(str(c["days"].Text or "").strip() or "0")
            except Exception:
                d = 0
            if d >= 1:
                d = min(3650, d)
                if d != settings["days"]:
                    settings["days"] = d
                    changed = True
            if changed:
                save_settings()
            store = page["store"]
            for i in range(len(favs)):
                if Kit.was_clicked(store, "rm%d" % i):
                    del favs[i]
                    save_favs()
                    view["dirty"] = True
                    HOST.refresh_settings(KEY)
                    return
            # 2.6.81 (IN2-2): the 4 s arm ran out: the button reads as before again
            at = page.get("wipe_at", 0.0)
            if at and not 0 <= time.time() - at <= 4.0:
                page["wipe_at"] = 0.0
                Kit.set_text(c.get("wipe_lbl"), "Forget everything", Kit.HUE_TEXT)
            if Kit.was_clicked(store, "wipe"):
                now = time.time()
                if 0 <= now - page.get("wipe_at", 0.0) <= 4.0:
                    page["wipe_at"] = 0.0
                    for s in list(idx["recs"]):
                        idx["tombs"][s] = now
                    idx["recs"].clear()
                    quick.clear()
                    view["sel"] = None
                    mark_dirty()
                    API.SysMsg("%s: the index is empty." % TITLE, Kit.HUE_GOOD)
                    HOST.refresh_settings(KEY)
                else:
                    page["wipe_at"] = now
                    Kit.set_text(c.get("wipe_lbl"), "Click again to empty it", Kit.HUE_BAD)

        def config_closed():
            page["c"] = None

        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "active": True,
                       "check_at": 0.0, "poll_at": 0.0, "merge_at": 0.0,
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            load_favs()
            watching.clear()
            del reads[:]
            del opens[:]
            known_open.clear()
            view.update({"sel": None, "naming": None, "status": "", "page": 0, "dirty": True})
            idx["path"] = os.path.join(script_dir(), FILE_FMT % account_id())
            hook_events()
            build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            HOST.services["storage.find"] = svc_find
            HOST.services["storage.total"] = svc_total
            HOST.services["storage.show"] = queue("show")    # (2.6.85) the bag sidebar's button

        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                # on_disposed turns the module off
                return
            now = time.time()
            while opens:
                note_open(opens.pop(0))
            if not st["events"] and (now >= st["poll_at"] or st["poll_at"] - now > 1.0):
                st["poll_at"] = now + 1.0
                poll_open_gumps()
            watch_tick(now)
            while st["queue"]:
                do_action(st["queue"].pop(0), now)
                if win["g"] is None:
                    return
            if full_shown():
                poll_box(now)
                live_tick(now)
            refresh(now)

        def _thread_tick():
            """Script thread: the file, the reads' bookkeeping and the summary."""
            if st["shutting"]:
                return
            if not idx["loaded"]:
                try:
                    load_index()
                except Exception as ex:           # never again every tick: go on without it
                    idx["loaded"], idx["err"] = True, str(ex)[:60]
            while reads:
                integrate(reads.pop(0))
            now = time.time()
            if idx["dirty"] and (now - idx["dirty_at"] >= SAVE_DELAY or now < idx["dirty_at"]):
                save_index()
                st["merge_at"] = now + MERGE_CHECK
            elif now >= st["merge_at"] or st["merge_at"] - now > MERGE_CHECK:
                st["merge_at"] = now + MERGE_CHECK
                check_others()
            if summ["ver"] != idx["ver"]:
                build_summary()
                fav_stored()                      # (worked out here, off the game's thread)
                if view["query"]:
                    search_stored(view["query"])

        def _thread_wanted():
            """(2.6.82) thread_tick has work: the index to load, reads to take in,
            the file to write or look at again (their times as thread_tick has
            them), the summary to make."""
            if st["shutting"]:
                return False
            if not idx["loaded"] or reads or summ["ver"] != idx["ver"]:
                return True
            now = time.time()
            if idx["dirty"] and (now - idx["dirty_at"] >= SAVE_DELAY or now < idx["dirty_at"]):
                return True
            return now >= st["merge_at"] or st["merge_at"] - now > MERGE_CHECK

        def _stop():
            st["shutting"] = True
            st["active"] = False
            HOST.dock_remove(KEY)
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            for k, fn in (("storage.find", svc_find), ("storage.total", svc_total)):
                if HOST.services.get(k) is fn:
                    HOST.services.pop(k, None)
            HOST.services.pop("storage.show", None)
            if reads or idx["dirty"]:
                try:
                    if not idx["loaded"]:
                        load_index()              # (merges the file: nothing of it is lost)
                    while reads:
                        integrate(reads.pop(0))
                    save_index()
                except Exception:
                    pass
            watching.clear()
            del reads[:]
            del opens[:]
            g, win["g"] = win["g"], None
            win["rows"] = []
            Kit.dispose(g)

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,
                  "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_restock():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  Modules tab.
        # ============================ MODULE START ===================================
        #  MODULE: Restock  -  top your supplies up from a chest or your bank box
        #
        #  A shopping list (reagents, potions, scrolls, bandages, arrows and bolts:
        #  the same items, by the same graphics, as Inventory > Supplies and
        #  Grimoire's reagent panel, so the counts agree) with a target amount for
        #  each, set on the settings page. Open a chest or your bank box, press
        #  Restock, and just enough of each item is moved into your backpack (or a
        #  bag in it you picked) to reach its target: one stack per move, one move
        #  every MOVE_GAP seconds, never more than the target.
        #
        #  Where from: the container you opened last (the default), your bank box,
        #  or a chest you picked with a target cursor (remembered per character).
        #  A picked chest that isn't open yet is opened once when you press Restock.
        #
        #  Player-started only: nothing moves until you press Restock, and it stops
        #  by itself when everything is topped up, when you press Stop, when a
        #  target cursor is up (yours or another module's), when you pick something
        #  up, at your weight limit, when the bag is full, after FAIL_STOP refused
        #  moves in a row, when the source goes out of reach, or when you die.
        #  One move at a time, each checked before the next: the count in your pack
        #  must have grown, or the move was refused (on a slow connection it waits
        #  for the server's answer, up to ANSWER_WAIT). A move still on its way when
        #  you press Stop is held back from the next Restock too, so a target is
        #  never passed.
        #
        #  Buying from NPC vendors is not part of it: the Legion API has no call
        #  that fills a vendor's buy list (TazUO's own Buy Agent, in the Legion
        #  Assistant window, can buy "up to" an amount from vendors).
        # =============================================================================
        KEY = "restock"
        TITLE = "Restock"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Restock_settings"     # options and where from / to (per character)
        TARGETS_KEY = "Restock_targets"       # the shopping list: "bp=50,ga=30" (per character)
        POS_KEY = "Restock_pos"               # where the window sits
        MIN_KEY = "Restock_min"               # minimized when last seen
        W = 400                               # the window's width (its height follows the list)
        MINI_W, MINI_H = 240, 46              # minimized bar
        TRAY_ICON = 0x0E79                    # a pouch, on the Action Bar's tray button
        ROW_H = 22                            # one list row
        ICON = 20                             # item art box at the front of a row
        PAGE_ROWS = 12                        # list rows per page of the window
        ART_BACK = (4014, 4016, 4015)         # the previous-page arrow (client gump art)
        MOVE_GAP = 0.7                        # seconds between two moves (the shard's item-move
        #                                       delay: unchecked in game)
        NOCHANGE_WAIT = 3.0                   # seconds a move may show no change at all (still in the
        #                                       source, not in your pack) before it counts as refused
        ANSWER_WAIT = 10.0                    # seconds a move that left the source may take to show up
        #                                       in your pack; past that the run stops (no more moves
        #                                       while the server hasn't answered)
        FAIL_STOP = 3                         # moves refused in a row before Restock gives up
        WAIT_RETRY = 3                        # "you must wait" answers before a move counts as refused
        LIMBO_WAIT = ANSWER_WAIT              # seconds an amount that may still arrive is held back
        #                                       from the next moves (a move refused without a word)
        OPEN_WAIT = 3.0                       # seconds for a picked chest to show its items once opened
        REACH = 2                             # tiles: a container on the ground farther than this is
        #                                       out of reach (RunUO's lift range: unchecked)
        WEIGHT_SPARE = 0                      # stones kept free under your weight limit
        TARGET_MAX = 60000                    # the largest target amount
        COUNT_EVERY = 1.0                     # seconds between counts for the window
        POLL_EVERY = 0.25                     # seconds between reads of the settings page's fields
        PICK_TIMEOUT = 20.0                   # seconds a pick cursor stays up
        #  Lines the shard answers a move with (RunUO texts; unchecked in game: "Say the
        #  server's replies" on the settings page prints the lines that come after each move)
        J_FULL = ("cannot hold more",)        # "That container cannot hold more items / weight."
        J_WAIT = ("must wait to perform another action",)   # cliloc 500119
        #  the client's own lines when the server refuses a lift (ClassicUO's pick-up errors)
        J_DENY = ("can not pick that up", "cannot pick that up", "that is too far away",
                  "that is out of sight", "does not belong to you", "already holding an item")
        #  Weight of one of each kind, in stones (RunUO pre-AoS: reagents, bandages, arrows
        #  and bolts 0.1, potions and spell scrolls 1). Unchecked in game; used only to stop
        #  short of your weight limit.
        UNIT_WEIGHT = {"REAGENTS": 0.1, "POTIONS": 1.0, "SCROLLS": 1.0, "OTHER": 0.1}
        WEIGHT_FALLBACK = (40.0, 3.5)         # max weight 40 + 3.5 x Str when the client has none
        ALERT_STOP = "restock.stopped"        # Settings > Alerts: a run that stopped before it was done
        ALERT_STOP_SOUND = 0x04A              # lever (the player can pick another or Silent)
        GROUPS = ("REAGENTS", "POTIONS", "SCROLLS", "OTHER")
        #  The list: (key, group, name, graphic). The first eight are Kit.REAGENTS (the
        #  mother's shared table); the rest are Inventory > Supplies, key for key and
        #  graphic for graphic (edit both if the shard differs).
        REG_ORDER = ("BP", "BM", "GA", "GI", "MR", "NS", "SS", "SA")
        REG_FALLBACK = {"BP": ("Black Pearl", 0x0F7A), "BM": ("Blood Moss", 0x0F7B),
                        "GA": ("Garlic", 0x0F84), "GI": ("Ginseng", 0x0F85),
                        "MR": ("Mandrake Root", 0x0F86), "NS": ("Nightshade", 0x0F88),
                        "SS": ("Spiders' Silk", 0x0F8D), "SA": ("Sulfurous Ash", 0x0F8C)}
        MORE_ITEMS = (
            ("bw", "REAGENTS", "Bat Wing", 0x0F78), ("gd", "REAGENTS", "Grave Dust", 0x0F8F),
            ("db", "REAGENTS", "Daemon Blood", 0x0F7D), ("nc", "REAGENTS", "Nox Crystal", 0x0F8E),
            ("pi", "REAGENTS", "Pig Iron", 0x0F8A),
            ("p_heal", "POTIONS", "Heal", 0x0F0C), ("p_cure", "POTIONS", "Cure", 0x0F07),
            ("p_refresh", "POTIONS", "Refresh", 0x0F0B), ("p_str", "POTIONS", "Strength", 0x0F09),
            ("p_agi", "POTIONS", "Agility", 0x0F08), ("p_ns", "POTIONS", "Night Sight", 0x0F06),
            ("p_expl", "POTIONS", "Explosion", 0x0F0D), ("p_poison", "POTIONS", "Poison", 0x0F0A),
            ("s_recall", "SCROLLS", "Recall", 0x1F4C), ("s_gate", "SCROLLS", "Gate Travel", 0x1F60),
            ("s_mark", "SCROLLS", "Mark", 0x1F59), ("s_gheal", "SCROLLS", "Greater Heal", 0x1F49),
            ("s_heal", "SCROLLS", "Heal", 0x1F31), ("s_cure", "SCROLLS", "Cure", 0x1F37),
            ("s_acure", "SCROLLS", "Arch Cure", 0x1F45),
            ("s_mr", "SCROLLS", "Magic Reflection", 0x1F50),
            ("s_invis", "SCROLLS", "Invisibility", 0x1F58), ("s_reveal", "SCROLLS", "Reveal", 0x1F5C),
            ("s_tele", "SCROLLS", "Teleport", 0x1F42), ("s_prot", "SCROLLS", "Protection", 0x1F3B),
            ("s_bless", "SCROLLS", "Bless", 0x1F3D), ("s_res", "SCROLLS", "Resurrection", 0x1F67),
            ("o_band", "OTHER", "Bandages", 0x0E21), ("o_arrow", "OTHER", "Arrows", 0x0F3F),
            ("o_bolt", "OTHER", "Bolts", 0x1BFB))
        CORPSE = 0x2006                       # a corpse is never a source
        # -----------------------------------------------------------------------------

        def _items():
            regs = getattr(Kit, "REAGENTS", None) or REG_FALLBACK
            out = []
            for a in REG_ORDER:
                name, graphic = regs.get(a) or REG_FALLBACK[a]
                out.append((a.lower(), "REAGENTS", str(name), int(graphic)))
            return tuple(out) + MORE_ITEMS
        ITEMS = _items()
        ORDER = tuple(r[0] for r in ITEMS)
        BY_KEY = dict((r[0], r) for r in ITEMS)
        KEY_OF = dict((r[3], r[0]) for r in ITEMS)          # graphic -> row key (one each)
        SRC_MODES = ("last", "bank", "pick")

        settings = {"deep": True, "src_deep": True, "say": False, "src": "last", "src_serial": 0,
                    "dest": 0}
        targets = {}                          # row key -> target amount (> 0 only)
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [], "run": None,
              "halt": False, "status": ("Idle", Kit.HUE_INFO), "last_open": 0, "opened": [],
              "page": 0, "count_at": 0.0, "short": {}, "layout": None,
              "picking": None, "hooked": False, "active": False, "redraw": False, "shown_moved": 0,
              "sent_at": 0.0,                 # the last move of any run (gaps hold across runs)
              "flight": []}                   # moves a stopped run left unanswered: [key, amount,
        #                                       held back until] (kept across Stop and off / on)
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "tips": {}}
        page = {"c": None, "seen": None, "at": 0.0}

        def noop():
            pass

        # ---------- saved settings ----------
        def load_settings():
            settings.update({"deep": True, "src_deep": True, "say": False, "src": "last",
                             "src_serial": 0, "dest": 0})
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = [s.strip() for s in part.split("=", 1)]
                if k in ("deep", "src_deep", "say"):
                    settings[k] = v == "1"
                elif k == "src" and v in SRC_MODES:
                    settings["src"] = v
                elif k in ("src_serial", "dest"):
                    try:
                        settings[k] = max(0, int(v))
                    except ValueError:
                        pass
            targets.clear()
            for part in Kit.get_var(TARGETS_KEY).split(","):
                if "=" not in part:
                    continue
                k, v = [s.strip() for s in part.split("=", 1)]
                if k in BY_KEY and v.isdigit():
                    n = min(TARGET_MAX, int(v))
                    if n > 0:
                        targets[k] = n

        def save_settings():
            Kit.put_var(SETTINGS_KEY, "deep=%d;src_deep=%d;say=%d;src=%s;src_serial=%d;dest=%d" % (
                1 if settings["deep"] else 0, 1 if settings["src_deep"] else 0,
                1 if settings["say"] else 0, settings["src"], settings["src_serial"],
                settings["dest"]))

        def save_targets():
            Kit.put_var(TARGETS_KEY, ",".join("%s=%d" % (k, targets[k]) for k in ORDER
                                              if targets.get(k, 0) > 0))

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        # ---------- the world (client thread: every read below runs in place) ----------
        def num(obj, attr, default=0):
            try:
                v = getattr(obj, attr)
                return default if v is None else int(v)
            except Exception:
                return default

        def no_container(c):
            return not c or c == 0xFFFFFFFF

        def top_of(serial):
            """(top item, what it sits on) for an item: the item at the top of its
            container chain and the mobile it is on (0 when it lies on the ground).
            A mobile's serial is under 0x40000000."""
            s = int(serial or 0)
            for _ in range(10):
                it = API.FindItem(s)
                if it is None:
                    return s, 0
                c = num(it, "Container")
                if no_container(c):
                    return s, 0
                if c < 0x40000000:
                    return s, c
                s = c
            return s, 0

        def backpack():
            try:
                return int(API.Backpack or 0)
            except Exception:
                return 0

        def bank_box():
            try:
                return int(API.Bank or 0)
            except Exception:
                return 0

        def in_pack(serial):
            """Inside your backpack (anywhere in it), or the backpack itself."""
            pack = backpack()
            return bool(pack) and top_of(serial)[0] == pack

        def item_name(it, fallback="container"):
            try:
                n = str(it.Name or "").strip()
            except Exception:
                n = ""
            return n or fallback

        def contents(serial, deep):
            try:
                return list(API.ItemsInContainer(int(serial), bool(deep)) or [])
            except Exception:
                return []

        def held_item():
            try:
                return int(API.GetHeldItem() or 0)
            except Exception:
                return 0

        def cursor_up():
            """Another module's cursor or claim, a pick cursor, or any target cursor."""
            if safe(lambda: HOST.cursor_busy(KEY), None):
                return True
            try:
                return bool(API.HasTarget())
            except Exception:
                return False

        def dest_serial():
            d = settings["dest"]
            return d if d else backpack()

        def pack_items(deep, max_age):
            """(2.6.82) The backpack's items through the mother's shared list (one
            scan a pass for every module that counts the pack), else read here."""
            try:
                return HOST.pack_items(deep, max_age)
            except Exception:
                return contents(backpack(), deep)

        def pack_counts(dest, deep=None, max_age=0.0):
            """Every list item in your pack, by row key (one pass over the pack):
            the whole pack with "Count inside bags", else its top level and the
            destination bag (so a move into that bag always shows in the count).
            A run passes the option it started with (a tick on the settings page
            mid-run must not change what "landed" means). max_age: (2.6.82) how
            old the shared pack list may be (0: this pass's only; a run uses 0)."""
            pack = backpack()
            if not pack:
                return {}
            if settings["deep"] if deep is None else deep:
                items = pack_items(True, max_age)
            else:
                items = pack_items(False, max_age)
                if dest and dest != pack:
                    items = items + contents(dest, False)
            out = {}
            for it in items:
                try:
                    k = KEY_OF.get(int(it.Graphic))
                    if k is None:
                        continue
                    out[k] = out.get(k, 0) + max(1, int(it.Amount or 1))
                except Exception:
                    continue
            return out

        def source_stacks(src, deep):
            """{row key: [(amount, serial), ...]} of the list items in the source."""
            out = {}
            for it in contents(src, deep):
                try:
                    k = KEY_OF.get(int(it.Graphic))
                    if k is None:
                        continue
                    out.setdefault(k, []).append((max(1, int(it.Amount or 1)), int(it.Serial)))
                except Exception:
                    continue
            return out

        def weight_room():
            """Stones you can still carry (None when the client doesn't say)."""
            try:
                p = API.Player
                w = float(p.Weight or 0)
                mx = float(p.WeightMax or 0)
                if mx <= 0:
                    mx = WEIGHT_FALLBACK[0] + WEIGHT_FALLBACK[1] * float(p.Strength or 0)
                if mx <= 0:
                    return None
                return mx - WEIGHT_SPARE - w
            except Exception:
                return None

        # ---------- where from / to ----------
        def source_info():
            """(serial or 0, label, why-not or None) for the chosen source."""
            mode = settings["src"]
            if mode == "bank":
                b = bank_box()
                if not b:
                    return 0, "Your bank box (not open)", "open your bank box first (say \"bank\" " \
                                                         "near a banker)"
                try:                              # (2.6.82: no list copy just to test it)
                    open_ = len(API.ItemsInContainer(b, False) or ()) > 0
                except Exception:
                    open_ = False
                return b, "Your bank box" + ("" if open_ else " (not open)"), None
            if mode == "pick":
                s = settings["src_serial"]
                if not s:
                    return 0, "Nothing picked yet", "pick the chest first (Pick...)"
                it = API.FindItem(s)
                if it is None:
                    return 0, "The picked chest (out of view)", "the chest you picked is out of view"
                return s, where_text(it), None
            s = st["last_open"]
            it = API.FindItem(s) if s else None
            if it is None:
                return 0, "Last opened: none yet", "open a chest or your bank box first"
            return s, "Last opened: " + where_text(it), None

        def where_text(it):
            if int(it.Serial) == bank_box():
                return "your bank box"
            name = item_name(it)
            if num(it, "OnGround") or no_container(num(it, "Container")):
                return "%s at %d, %d" % (name, num(it, "X"), num(it, "Y"))
            return name

        def dest_info():
            d = settings["dest"]
            if not d:
                return "Your backpack", None
            it = API.FindItem(d)
            if it is None or not in_pack(d):
                return "The picked bag (not in your backpack)", \
                    "the bag you picked isn't in your backpack: pick it again or choose Backpack"
            return item_name(it, "bag") + " in your backpack", None

        def source_ok(serial):
            """None when serial can be a source, else why not."""
            if not serial:
                return "nothing was targeted"
            it = API.FindItem(serial)
            if it is None:
                return "that isn't an item"
            # 2.6.81 (IN2-1): nor a bag inside a corpse (the top of its chain): a run
            # out of one would loot a corpse (R6: looting can flag you criminal)
            top, _on = top_of(serial)
            t = API.FindItem(top) if top != int(serial) else it
            for x in (it, t):
                if x is not None and (num(x, "Graphic") == CORPSE or num(x, "IsCorpse")):
                    return "a corpse (or a bag in one) isn't a source"
            if in_pack(serial):
                return "that is in your backpack"
            if not (num(it, "IsContainer") or contents(serial, False)):
                return "that isn't a container"
            return None

        def out_of_reach(src):
            """Why the source can't be reached now, or None."""
            it = API.FindItem(src)
            if it is None:
                return "the source is out of view"
            top, on = top_of(src)
            if on:                                   # on a mobile: the bank box on you is fine
                p = API.Player
                if on == num(p, "Serial"):
                    return None
                m = API.FindMobile(on)               # a pack animal of yours, next to you
                if m is None or not num(m, "IsRenamable"):
                    return "the source is on someone else"
                d = max(abs(num(m, "X") - num(p, "X")), abs(num(m, "Y") - num(p, "Y")))
                return "your pack animal is out of reach (step next to it)" if d > REACH else None
            t = API.FindItem(top)
            if t is None:
                return None
            try:
                p = API.Player
                d = max(abs(num(t, "X") - num(p, "X")), abs(num(t, "Y") - num(p, "Y")))
            except Exception:
                return None
            return "the source is out of reach (step next to it)" if d > REACH else None

        # ---------- containers opened (an event: noted only, the tick reads it) ----------
        def on_open(*args):
            if not st["active"]:
                return
            for a in args:
                s = 0
                try:
                    s = int(getattr(a, "Serial", a) or 0)
                except Exception:
                    s = 0
                if s:
                    st["opened"].append(s)
                    del st["opened"][:-8]
                    return

        def hook_events():
            if st["hooked"]:
                return
            st["hooked"] = True
            ev = safe(lambda: API.Events)
            if ev is not None:
                safe(lambda: ev.OnOpenContainer(on_open))

        def take_opened():
            while st["opened"]:
                s = st["opened"].pop(0)
                if source_ok(s) is None:
                    st["last_open"] = s

        # ---------- the run ----------
        def set_status(text, hue=None):
            st["status"] = (text, Kit.HUE_INFO if hue is None else hue)
            lbl = win["c"].get("status")
            if lbl is not None:
                if st["minimized"]:                  # the minimized bar: "Restock: <status>"
                    text = TITLE + ": " + text[:1].lower() + text[1:]
                Kit.set_text(lbl, Kit.fit(text, win["c"].get("status_w", 200)), st["status"][1])

        def say(msg, hue=None):
            API.SysMsg("%s: %s" % (TITLE, msg), Kit.HUE_INFO if hue is None else hue)

        def start_run():
            if st["run"] is not None:
                say("already restocking; press Stop first.", Kit.HUE_BAD)
                return
            rows = [k for k in ORDER if targets.get(k, 0) > 0]
            if not rows:
                say("the list is empty: set how many of each item to carry on the settings page.",
                    Kit.HUE_BAD)
                HOST.show_settings(KEY)
                return
            src, _lbl, why = source_info()
            if why is None:
                why = source_ok(src) or out_of_reach(src)
            if why is None:
                dest = dest_serial()
                why = None if dest else "you have no backpack"
                if why is None:
                    why = dest_info()[1]
            if why is None and cursor_up():
                why = "a target cursor is up"
            if why is None and held_item():
                why = "you are holding an item"
            if why is None and num(API.Player, "IsDead"):
                why = "you are dead"
            if why is not None:
                say("can't restock: %s." % why, Kit.HUE_BAD)
                set_status("Can't: " + why, Kit.HUE_BAD)
                return
            now = time.time()
            r = {"src": src, "dest": dest, "deep": settings["deep"], "src_deep": settings["src_deep"],
                 "phase": "go", "open_until": 0.0, "move": None,
                 "check": None, "at": now, "hold": 0.0, "sent_at": 0.0, "last": 0, "left": False,
                 "c0": 0,
                 "moved": 0, "moves": 0, "refused": 0, "streak": 0, "waits": 0,
                 "why": None, "bad": set(), "limbo": [], "jr": None}
            if 0 <= now - st["sent_at"] < MOVE_GAP:     # a gap after the last run's last move too
                r["at"] = st["sent_at"] + MOVE_GAP
            # a move an earlier run left on its way still counts against the targets
            r["limbo"] = [e for e in st["flight"] if 0 <= e[2] - now <= LIMBO_WAIT]
            st["flight"] = []
            st["short"] = {}
            st["halt"] = False
            if not contents(src, False):
                if src == bank_box():
                    say("your bank box isn't open: say \"bank\" near a banker first.", Kit.HUE_BAD)
                    set_status("Bank box not open", Kit.HUE_BAD)
                    return
                API.UseObject(src)                   # one double-click: the chest opens
                r["phase"] = "open"
                r["open_until"] = now + OPEN_WAIT
                set_status("Opening the chest")
            else:
                set_status("Restocking")
            st["run"] = r
            say("restocking %d item%s." % (len(rows), "" if len(rows) == 1 else "s"))
            refresh_buttons()

        def limbo_of(r, key, now):
            n = 0
            keep = []
            for e in r["limbo"]:
                if 0 <= e[2] - now <= LIMBO_WAIT:
                    keep.append(e)
                    if e[0] == key:
                        n += e[1]
            r["limbo"] = keep
            return n

        def run_step(now):
            """One step of a run (client tick): the last move's answer, the stops,
            then the next move, which thread_tick sends."""
            r = st["run"]
            if r is None:
                return
            if settings["say"] and r["jr"] is not None:
                for ln in r["jr"].new():
                    if ln.text and not ln.text.startswith(TITLE + ":"):
                        say("reply: " + ln.text.strip())
            if r["move"] is not None:
                return                               # the move waits for thread_tick
            if r["check"] is not None and not r["left"]:
                # the client lifts the stack out of the source the frame after the move
                # goes out; seeing that (one look by serial a tick) tells a refusal that
                # came back from a move that never left
                it = API.FindItem(r["check"][1])
                if it is None or num(it, "Container") != r["c0"]:
                    r["left"] = True
            if r["why"]:
                stop_run(r["why"])
                return
            if r["phase"] == "open":
                if contents(r["src"], False):
                    r["phase"] = "go"
                    set_status("Restocking")
                elif not 0 <= r["open_until"] - now <= OPEN_WAIT:
                    stop_run("the chest didn't open (or it is empty)")
                return
            if r["check"] is not None:
                if 0 < r["at"] - now <= MOVE_GAP or not check_move(r, now):
                    return
            if 0 < r["hold"] - now <= MOVE_GAP or 0 < r["at"] - now <= MOVE_GAP:
                return
            if cursor_up():
                stop_run("a target cursor is up")
                return
            h = held_item()
            if h and not (h == r["last"] and 0 <= now - r["sent_at"] < 2 * MOVE_GAP):
                stop_run("you picked something up")
                return
            if num(HOST.me(), "IsDead"):            # (2.6.82: the pass's player)
                stop_run("you died")
                return
            why = out_of_reach(r["src"])
            if why:
                stop_run(why)
                return
            next_move(r, now)

        def next_move(r, now):
            have = pack_counts(r["dest"], r["deep"])
            stacks = source_stacks(r["src"], r["src_deep"])
            waiting = False
            for key in ORDER:
                t = targets.get(key, 0)
                if t <= 0:
                    continue
                held_back = limbo_of(r, key, now)
                need = t - have.get(key, 0) - held_back
                if need <= 0:
                    if held_back:
                        waiting = True
                    st["short"].pop(key, None)
                    continue
                mine = [s for s in stacks.get(key, ()) if s[1] not in r["bad"]]
                if not mine:
                    st["short"][key] = need
                    continue
                amount, serial = max(mine)
                take = min(amount, need)
                room = weight_room()
                if room is not None:
                    fit = int(room / UNIT_WEIGHT.get(BY_KEY[key][1], 1.0) + 1e-6)
                    if fit < 1:
                        stop_run("you are at your weight limit")
                        return
                    take = min(take, fit)
                st["short"].pop(key, None)
                it = API.FindItem(serial)
                r["c0"] = num(it, "Container") if it is not None else 0
                r["move"] = (key, serial, take, have.get(key, 0))
                if settings["say"]:
                    r["jr"] = Journal.reader()        # debug: the server's replies to this move
                set_status("Moving %d %s (%d moved)" % (take, BY_KEY[key][2], r["moved"]))
                return
            if waiting:
                set_status("Waiting for the server")
                r["hold"] = now + MOVE_GAP
                return
            finish_run()

        def check_move(r, now):
            """The last move's answer, a gap after it went out: True to go on with
            the next move, False when the run stopped or waits a little longer.
            One move at a time: the next goes only once this one has landed in
            your pack or was refused, so no answer still on its way can add to a
            later move and pass a target. Where the moved stack is tells: in your
            pack (or your count grew), back where it was, or neither (on its way)."""
            key, serial, amt, have0 = r["check"]
            t0 = r["sent_at"]
            if Journal.find(t0, J_FULL) is not None:
                stop_run("your %s can't hold more" % ("backpack" if r["dest"] == backpack() else "bag"))
                return False
            have1 = pack_counts(r["dest"], r["deep"]).get(key, 0)
            age = now - t0
            it = API.FindItem(serial)
            where = num(it, "Container") if it is not None else 0
            landed = have1 > have0
            if not landed and it is not None and not no_container(where) and where != r["c0"]:
                # in your pack as its own stack (while some of that item was used up
                # meanwhile, so the count didn't grow)
                landed = in_pack(serial)
                if landed:
                    have1 = have0 + amt
            if landed:                               # it landed (or part of it)
                got = min(have1 - have0, amt)
                r["moved"] += got
                if got < amt:                        # the rest may still be on its way
                    r["limbo"].append([key, amt - got, now + LIMBO_WAIT])
                r["check"] = None
                r["left"] = False
                r["streak"] = r["waits"] = 0
                return True
            back = it is not None and where == r["c0"]
            if not back or held_item() == serial:    # on its way: lifted, not in your pack yet
                r["left"] = True
                if not 0 <= age < ANSWER_WAIT:
                    stop_run("the server hasn't answered a move for %d s" % int(ANSWER_WAIT))
                    return False
                if age >= 2 * MOVE_GAP:
                    set_status("Waiting for the server")
                r["at"] = now + MOVE_GAP * 0.5
                return False
            # where it was: it came back (seen leaving), or it never left. A "must wait"
            # or refusal line can belong to an earlier move given up on; unless this
            # stack was seen leaving and coming back, its amount is held back (it may
            # still come)
            if Journal.find(t0, J_WAIT) is not None and r["waits"] < WAIT_RETRY:
                r["waits"] += 1                      # too soon for the server: the same move again
                if not r["left"]:
                    r["limbo"].append([key, amt, now + LIMBO_WAIT])
                r["check"] = None
                r["left"] = False
                r["hold"] = now + MOVE_GAP
                return False
            said = Journal.find(t0, J_DENY) is not None
            if not (said or r["left"]) and 0 <= age < NOCHANGE_WAIT:
                r["at"] = now + MOVE_GAP * 0.5       # no answer yet: look again a little later
                return False
            if not r["left"]:                        # refused without being seen to leave: it may
                r["limbo"].append([key, amt, now + LIMBO_WAIT])      # still come
            r["check"] = None                        # back (or still) where it was: refused
            r["left"] = False
            r["waits"] = 0
            r["refused"] += 1
            r["streak"] += 1
            r["bad"].add(serial)
            if r["streak"] >= FAIL_STOP:
                stop_run("%d moves in a row were refused" % r["streak"])
                return False
            return True

        def send_move():
            """thread_tick: the move the client tick picked goes out (a queued call:
            nothing waits). Stop pressed since then: it doesn't go."""
            r = st["run"]
            if r is None or r["move"] is None:
                return
            mv = r["move"]
            r["move"] = None
            if st["halt"] or st["shutting"]:
                return
            try:
                API.MoveItem(mv[1], r["dest"], mv[2])
            except Exception as ex:
                r["why"] = "a move failed (%s)" % ex
                return
            try:
                HOST.pack_dirty()                    # (2.6.82) the shared pack list read anew
            except Exception:
                pass
            r["check"] = mv
            r["left"] = False
            r["last"] = mv[1]
            r["sent_at"] = st["sent_at"] = time.time()
            r["at"] = r["sent_at"] + MOVE_GAP
            r["moves"] += 1

        def short_text():
            if not st["short"]:
                return ""
            parts = ["%s %d" % (BY_KEY[k][2], n) for k, n in
                     sorted(st["short"].items(), key=lambda kv: ORDER.index(kv[0]))]
            return "; short (none left in the source): " + ", ".join(parts[:6]) + \
                (" and %d more" % (len(parts) - 6) if len(parts) > 6 else "")

        def keep_flight(r):
            """A run ends with a move unanswered (or amounts held back): the next run
            holds them back too, or an answer still on its way could pass a target."""
            if r is None:
                return
            out = [list(e) for e in r["limbo"]]
            if r["check"] is not None:
                key, _serial, amt, _h0 = r["check"]
                out.append([key, amt, r["sent_at"] + ANSWER_WAIT])
            if out:
                st["flight"] = (st["flight"] + out)[-20:]

        def finish_run():
            r, st["run"] = st["run"], None
            if r is None:
                return
            keep_flight(r)
            msg = "done: %d moved in %d move%s" % (r["moved"], r["moves"], "" if r["moves"] == 1 else "s")
            if r["refused"]:
                msg += ", %d refused" % r["refused"]
            say(msg + short_text() + ".", Kit.HUE_BAD if st["short"] or r["refused"] else Kit.HUE_GOOD)
            set_status("Done: %d moved%s" % (r["moved"], ", some short" if st["short"] else ""),
                       Kit.HUE_TITLE if st["short"] else Kit.HUE_GOOD)
            st["count_at"] = 0.0
            refresh_buttons()

        def stop_run(why=None, user=False):
            r, st["run"] = st["run"], None
            st["halt"] = True
            if r is None:
                return
            keep_flight(r)
            if user:
                say("stopped (%d moved)." % r["moved"])
                set_status("Stopped (%d moved)" % r["moved"])
            else:
                text = "%s (%d moved)" % (why or "stopped", r["moved"])
                fn = getattr(HOST, "alert", None)
                raised = False
                if fn is not None:
                    try:
                        raised = bool(fn(ALERT_STOP, "Stopped: " + text, "warn"))
                    except Exception:
                        raised = False
                if not raised:
                    say("stopped: " + text + ".", Kit.HUE_BAD)
                set_status("Stopped: " + (why or ""), Kit.HUE_BAD)
            st["count_at"] = 0.0
            refresh_buttons()

        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def halt_click():
            st["halt"] = True                        # thread_tick won't send a move armed before it
            queue("stop")()

        def list_keys():
            return [k for k in ORDER if targets.get(k, 0) > 0]

        def layout_now():
            keys = list_keys()
            pages = max(1, (len(keys) + PAGE_ROWS - 1) // PAGE_ROWS)
            pg = min(st["page"], pages - 1)
            return (st["minimized"], st["docked"], pg, pages,
                    tuple(keys[pg * PAGE_ROWS:(pg + 1) * PAGE_ROWS]))

        def build_window():
            lay = layout_now()
            st["page"] = lay[2]
            st["layout"] = lay
            mini = st["minimized"]
            w, h = (MINI_W, MINI_H) if mini else (W, window_h(len(lay[4])))
            x, y = Kit.load_pos(POS_KEY, (240, 220), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            rows = []
            g = G.CreateGump(True, True)
            if mini:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
                c["status_w"] = w - 90
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                # where from, where to
                ya = M + 30 + Kit.GAP
                Kit.add_section(g, M, ya, IW, 136, "FROM AND TO")
                Kit.add_label(g, "From:", M + 12, ya + 30, Kit.HUE_INFO)
                lx = M + 12 + max(Kit.text_w("From:"), Kit.text_w("Into:")) + 10
                c["src"] = Kit.add_label(g, "", lx, ya + 30)
                c["src_w"] = IW - (lx - M) - 8
                bx = M + 12
                for mode, cap, tip in (("last", "Last opened",
                                        "Take from the container you opened last"),
                                       ("bank", "Bank box", "Take from your bank box (say \"bank\" "
                                                            "near a banker to open it)"),
                                       ("pick", "Pick...", "Target a chest to take from; it is "
                                                           "remembered (opened once if it is closed)")):
                    c["m_" + mode] = Kit.art_button(
                        g, store, "m_" + mode, Kit.ART_PAGE, bx, ya + 52, cap, tip,
                        Kit.HUE_TITLE if settings["src"] == mode else Kit.HUE_TEXT,
                        on_click=queue(("src", mode)))
                    bx += 35 + Kit.text_w(cap) + 14
                Kit.add_label(g, "Into:", M + 12, ya + 84, Kit.HUE_INFO)
                c["dest"] = Kit.add_label(g, "", lx, ya + 84)
                bx = M + 12
                for mode, cap, tip in (("pack", "Backpack", "Restock into your backpack"),
                                       ("bag", "Pick bag...", "Target a bag in your backpack to "
                                                              "restock into")):
                    c["d_" + mode] = Kit.art_button(
                        g, store, "d_" + mode, Kit.ART_PAGE, bx, ya + 106, cap, tip,
                        Kit.HUE_TITLE if (mode == "bag") == bool(settings["dest"]) else Kit.HUE_TEXT,
                        on_click=queue(("dest", mode)))
                    bx += 35 + Kit.text_w(cap) + 14
                # the list
                yb = ya + 136 + Kit.GAP
                hb = list_h(len(lay[4]))
                Kit.add_section(g, M, yb, IW, hb, "LIST  (carried / to carry)")
                if lay[3] > 1:
                    px = M + IW - 12 - 21
                    Kit.art_button(g, store, "next", Kit.ART_PLAY, px, yb + 4, None, "Next page",
                                   on_click=queue(("page", 1)))
                    c["pg"] = Kit.add_label(g, "%d/%d" % (lay[2] + 1, lay[3]),
                                            px - 8 - Kit.text_w("%d/%d" % (lay[3], lay[3])), yb + 6,
                                            Kit.HUE_INFO)
                    Kit.art_button(g, store, "prev", ART_BACK,
                                   px - 16 - Kit.text_w("%d/%d" % (lay[3], lay[3])) - 21, yb + 4,
                                   None, "Previous page", on_click=queue(("page", -1)))
                if not lay[4]:
                    Kit.add_label(g, "Nothing on the list yet. Set how many of each", M + 12,
                                  yb + 30, Kit.HUE_INFO)
                    Kit.add_label(g, "to carry on the " + TITLE + " settings page.", M + 12, yb + 50,
                                  Kit.HUE_INFO)
                cx = M + IW - 100
                for i, k in enumerate(lay[4]):
                    ry = yb + 28 + i * ROW_H
                    _key, _grp, name, graphic = BY_KEY[k]
                    item_pic(g, graphic, M + 12, ry)
                    Kit.add_label(g, Kit.fit(name, cx - (M + 12 + ICON + 6) - 8),
                                  M + 12 + ICON + 6, ry + 2)
                    lbl = Kit.add_label(g, "", cx, ry + 2)
                    tip = Kit.catcher(g, M + 8, ry, IW - 16, ROW_H, noop, name)
                    rows.append({"key": k, "count": lbl, "tip": tip})
                # restock / stop, status
                yc = yb + hb + Kit.GAP
                Kit.add_section(g, M, yc, IW, 64)
                Kit.art_button(g, store, "go", Kit.ART_PLAY, M + 12, yc + 8, "Restock",
                               "Top every item on the list up to its target from the source "
                               "(one move every %.1f s)" % MOVE_GAP, on_click=queue("go"))
                sx = M + 12 + 35 + Kit.text_w("Restock") + 18
                Kit.art_button(g, store, "stop", Kit.ART_CLOSE, sx, yc + 8, "Stop",
                               "Stop restocking (nothing more is moved)", on_click=halt_click)
                c["status"] = Kit.add_label(g, "", M + 12, yc + 40, st["status"][1])
                c["status_w"] = IW - 24
            Kit.place(g, x, y, w, h)
            if safe(lambda: HOST.layout_locked(KEY), False):
                safe(lambda: setattr(g, "CanMove", False))   # 2.6.81 (IN2-3): held in its zone
            win.update({"g": g, "c": c, "store": store, "rows": rows, "tips": {}})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            Kit.dispose(old)
            set_status(*st["status"])
            st["count_at"] = 0.0
            refresh(time.time())

        def item_pic(g, graphic, x, y):
            try:
                p = G.CreateGumpItemPic(graphic, ICON, ICON)
                p.SetRect(x, y, ICON, ICON)
                safe(lambda: setattr(p, "DrawBorder", False))
                safe(lambda: p.SetAcceptMouseInput(False))
                g.Add(p)
            except Exception:
                pass

        def list_h(n):
            return 30 + max(2, n) * ROW_H + 6

        def window_h(n):
            M = Kit.MARGIN
            return M + 30 + Kit.GAP + 136 + Kit.GAP + list_h(n) + Kit.GAP + 64 + M

        def refresh_buttons():
            c = win["c"]
            for mode in SRC_MODES:
                lbl = c.get("m_" + mode)
                if lbl is not None:
                    Kit.set_text(lbl, {"last": "Last opened", "bank": "Bank box",
                                       "pick": "Pick..."}[mode],
                                 Kit.HUE_TITLE if settings["src"] == mode else Kit.HUE_TEXT)
            for mode, cap in (("pack", "Backpack"), ("bag", "Pick bag...")):
                lbl = c.get("d_" + mode)
                if lbl is not None:
                    Kit.set_text(lbl, cap, Kit.HUE_TITLE if (mode == "bag") == bool(settings["dest"])
                                 else Kit.HUE_TEXT)

        def refresh(now):
            """The labels that change: source, destination, counts (once a second,
            or at once after a run step reset count_at). Nothing while folded; only
            the status while minimized."""
            g = win["g"]
            if g is None or st["minimized"]:
                return
            if 0 <= now - st["count_at"] < COUNT_EVERY:
                return
            st["count_at"] = now
            c = win["c"]
            _s, slbl, _why = source_info()
            Kit.set_text(c["src"], Kit.fit(slbl, c["src_w"]))
            dlbl, dwhy = dest_info()
            Kit.set_text(c["dest"], Kit.fit(dlbl, c["src_w"]), Kit.HUE_BAD if dwhy else Kit.HUE_TEXT)
            if not win["rows"]:
                return
            # (2.6.82) between runs the shared pack list may be up to 0.5 s old
            have = pack_counts(dest_serial(), None, 0.0 if st["run"] is not None else 0.5)
            tips = win["tips"]
            for row in win["rows"]:
                k = row["key"]
                n, t = have.get(k, 0), targets.get(k, 0)
                if n >= t:
                    hue = Kit.HUE_GOOD
                elif n == 0:
                    hue = Kit.HUE_BAD
                else:
                    hue = Kit.HUE_TITLE
                Kit.set_text(row["count"], "%d / %d" % (n, t), hue)
                tkey = (n, t, st["short"].get(k))     # (2.6.82) the tip made only on a change
                if tips.get(k) == tkey:
                    continue
                tip = "%s: %d in your pack, target %d" % (BY_KEY[k][2], n, t)
                if k in st["short"]:
                    tip += " (short by %d: none left in the source)" % st["short"][k]
                tips[k] = tkey
                try:
                    row["tip"].SetTooltip(tip)
                except Exception:
                    pass

        # ---------- picks ----------
        def ask_pick(what):
            if st["run"] is not None:
                say("press Stop first.", Kit.HUE_BAD)
                return
            st["picking"] = what
            say("target the chest to take from." if what == "src" else
                "target a bag in your backpack.")

            def done(serial):
                queue(("picked", what, int(serial or 0)))()
            HOST.pick_target(PICK_TIMEOUT, done, KEY)

        def picked(what, serial):
            st["picking"] = None
            if not serial:
                return
            if what == "src":
                why = source_ok(serial)
                if why:
                    say("not a source: %s." % why, Kit.HUE_BAD)
                    return
                settings["src"], settings["src_serial"] = "pick", serial
                save_settings()
                it = API.FindItem(serial)
                say("taking from %s." % (where_text(it) if it is not None else "it"), Kit.HUE_GOOD)
            else:
                pack = backpack()
                if serial == pack:
                    settings["dest"] = 0
                else:
                    it = API.FindItem(serial)
                    if it is None or not in_pack(serial) or not (num(it, "IsContainer") or
                                                                 contents(serial, False)):
                        say("pick a bag that is in your backpack.", Kit.HUE_BAD)
                        return
                    settings["dest"] = serial
                save_settings()
            st["count_at"] = 0.0
            refresh_buttons()

        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        def group_rows(grp):
            return [r for r in ITEMS if r[1] == grp]

        def group_h(grp):
            n = len(group_rows(grp))
            return 30 + ((n + 1) // 2) * 26 + 6

        OPT_H = 30 + 2 * 28 + 24 + 8          # (2.6.52: the debug box moved to its own DEBUG section)
        DEBUG_H = 60

        def config_height(w):
            return sum(group_h(gp) for gp in GROUPS) + OPT_H + DEBUG_H + (len(GROUPS) + 1) * Kit.GAP

        def build_config(g, x, y, w):
            boxes = {}
            yy = y
            half = (w - 24) // 2
            for gp in GROUPS:
                hint = "how many to carry, 0 = leave alone" if gp == "REAGENTS" else "how many to carry"
                Kit.add_section(g, x, yy, w, group_h(gp), "%s  (%s)" % (gp, hint))
                for i, (k, _grp, name, _gr) in enumerate(group_rows(gp)):
                    cx = x + 12 + (i % 2) * half
                    ry = yy + 30 + (i // 2) * 26
                    Kit.add_label(g, Kit.fit(name, half - 76), cx, ry + 3)
                    tb = Kit.add_textbox(g, str(targets.get(k, 0)), cx + half - 68, ry, 52)
                    safe(lambda: tb.SetTooltip("How many %s to carry (0-%d, 0 = leave it alone)"
                                               % (name, TARGET_MAX)))
                    boxes[k] = tb
                yy += group_h(gp) + Kit.GAP
            Kit.add_section(g, x, yy, w, OPT_H, "OPTIONS")
            c = {"boxes": boxes,
                 "deep": Kit.add_check(g, "Count inside bags in your pack", x + 12, yy + 30,
                                       settings["deep"],
                                       "What you carry counts the bags inside your backpack too "
                                       "(as Inventory > Supplies and Grimoire do)"),
                 "src_deep": Kit.add_check(g, "Take from bags inside the source too", x + 12,
                                           yy + 58, settings["src_deep"],
                                           "Also take from bags inside the chest or bank box (only "
                                           "those whose contents you have seen)")}
            Kit.add_label(g, "One move every %.1f s; it stops when you pick something up." % MOVE_GAP,
                          x + 12, yy + 88, Kit.HUE_INFO)
            yy += OPT_H + Kit.GAP
            Kit.add_section(g, x, yy, w, DEBUG_H, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print the shard's replies in the journal", x + 12, yy + 30,
                                     settings["say"],
                                     "The journal lines that come after each move, to check the "
                                     "texts " + TITLE + " listens for (a full bag, \"you must wait\")")
            page.update({"c": c, "seen": None, "at": 0.0})

        def poll_config():
            c = page["c"]
            if c is None:
                return
            now = time.time()
            if 0 <= now - page["at"] < POLL_EVERY:
                return
            page["at"] = now
            try:
                texts = tuple(str(c["boxes"][k].Text).strip() for k in ORDER)
                ticks = (bool(c["deep"].IsChecked), bool(c["src_deep"].IsChecked),
                         bool(c["say"].IsChecked))
            except Exception:
                return
            changed = False
            for k, v in zip(("deep", "src_deep", "say"), ticks):
                if v != settings[k]:
                    settings[k] = v
                    changed = True
            if changed:
                save_settings()
                st["count_at"] = 0.0
            if texts == page["seen"]:
                return
            page["seen"] = texts
            new = False
            for k, t in zip(ORDER, texts):
                if not t.isdigit():
                    continue                          # typing: wait for a whole number
                n = min(TARGET_MAX, int(t))
                if n != targets.get(k, 0):
                    if n > 0:
                        targets[k] = n
                    else:
                        targets.pop(k, None)
                    new = True
            if new:
                save_targets()
                st["count_at"] = 0.0
                if layout_now() != st["layout"]:
                    st["redraw"] = True

        def config_closed():
            page["c"] = None
            page["seen"] = None

        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "run": None, "halt": False,
                       "status": ("Idle", Kit.HUE_INFO), "opened": [], "page": 0,
                       "count_at": 0.0, "short": {}, "layout": None, "picking": None,
                       "active": True, "redraw": False, "shown_moved": 0,
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            fn = getattr(HOST, "alert_kind", None)      # listed on Settings > Alerts
            if fn is not None:
                safe(lambda: fn(ALERT_STOP, "Restock stopped early", ALERT_STOP_SOUND))
            hook_events()
            build_window()
            HOST.services["restock.run"] = queue("go")   # (2.6.85) the bag sidebar's button: one run
            try:                                     # 2.6.55: rebuilt whole, so the layout may
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True)
            except TypeError:                        # an older mother
                hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
            HOST.dock_add(KEY, hooks)

        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                # on_disposed turns the module off
                return
            if st["opened"]:
                take_opened()
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)
                    Kit.save_min(MIN_KEY, st["minimized"])
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)
                elif action == "redraw":
                    build_window()
                elif action == "go":
                    start_run()
                elif action == "stop":
                    if st["run"] is not None:
                        stop_run(user=True)
                elif kind == "src":
                    if st["run"] is not None:
                        say("press Stop first.", Kit.HUE_BAD)
                    elif action[1] == "pick":
                        ask_pick("src")
                    else:
                        settings["src"] = action[1]
                        save_settings()
                        st["count_at"] = 0.0
                        refresh_buttons()
                elif kind == "dest":
                    if st["run"] is not None:
                        say("press Stop first.", Kit.HUE_BAD)
                    elif action[1] == "bag":
                        ask_pick("dest")
                    else:
                        settings["dest"] = 0
                        save_settings()
                        st["count_at"] = 0.0
                        refresh_buttons()
                elif kind == "picked":
                    picked(action[1], action[2])
                elif kind == "page":
                    pages = layout_now()[3]
                    st["page"] = (st["page"] + action[1]) % pages
                    build_window()
            if st["redraw"]:
                st["redraw"] = False
                if layout_now() != st["layout"]:
                    build_window()
            now = time.time()
            r = st["run"]
            if r is not None:
                run_step(now)
                if r["moved"] != st["shown_moved"]:
                    st["shown_moved"] = r["moved"]
                    st["count_at"] = 0.0             # the counts show each move as it lands
            refresh(now)

        def _thread_tick():
            if st["run"] is not None and not st["shutting"]:
                send_move()

        def _thread_wanted():
            """(2.6.82) thread_tick has work: a move picked and not sent yet."""
            r = st["run"]
            return r is not None and r["move"] is not None and not st["shutting"]

        def _stop():
            HOST.services.pop("restock.run", None)
            st["shutting"] = True
            st["halt"] = True
            st["active"] = False
            r, st["run"] = st["run"], None
            keep_flight(r)
            HOST.dock_remove(KEY)
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            g, win["g"] = win["g"], None
            win["c"], win["rows"] = {}, []
            Kit.dispose(g)

        def _interval():
            return 0.05 if st["run"] is not None else 0.1

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "thread_tick": _thread_tick,  # the moves go out here
                  "thread_wanted": _thread_wanted,
                  "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_supplies():
        """Builds the part in its own namespace and returns its hooks."""
        # =============================================================================
        #  PART: Supplies  (Inventory; from Character HUD > Frames, moved in 2.6.85)
        #
        #  A table of what is in your pack, row by row, with yellow and red counts.
        #  It works as it did in Frames, and keeps Frames' saved keys (UnitFrames_*).
        #  Its options lived in the UnitFrames_settings string: from 2.6.85 they are
        #  in UnitFrames_supset, read from the old string the first time.
        #  The bag sidebar's Supplies button opens it ("supplies.open"), its own
        #  Close folds it away. With Frames off it stands free at its saved place.
        # =============================================================================
        KEY = "supplies"
        TITLE = "Supplies"
        OLD_SETTINGS_KEY = "UnitFrames_settings"
        SET_KEY = "UnitFrames_supset"        # (2.6.85) "sup_open=1,sup_deep=1,..."
        SAVE_EVERY = 10.0                    # seconds between belt-and-braces saves
        # The table of what is in your pack. Each row: (key, group, caption, graphic, hue)
        # with hue None for any hue. Add shard-specific items here (e.g. a potion
        # that is told apart by hue) and they appear on the settings page.
        PACK_AGE = 0.5                                       # (2.6.82) a shared pack list this old will do
        SUPPLY_EVERY = 1.0                                   # seconds between pack counts
        SUPPLY_W = 220                                       # table width
        SUPPLY_ROW = 22                                      # row height
        SUPPLY_ICON = 20                                     # item art box in front of each name
        SUPPOS_KEY = "UnitFrames_suppos"                     # where a free-floating table sits
        SUPPLY_SIDES = ("Below the frame", "Left of the frame", "Right of the frame")
        SUPPLY_LOW_DEFAULT = 10                              # counts at or below show red
        ROWS_POLL = 0.25                                     # seconds between reads of the rows window's boxes
        SUPPLY_ITEMS = (
            ("bp", "REAGENTS", "Black Pearl", 0x0F7A, None),
            ("bm", "REAGENTS", "Blood Moss", 0x0F7B, None),
            ("ga", "REAGENTS", "Garlic", 0x0F84, None),
            ("gi", "REAGENTS", "Ginseng", 0x0F85, None),
            ("mr", "REAGENTS", "Mandrake Root", 0x0F86, None),
            ("ns", "REAGENTS", "Nightshade", 0x0F88, None),
            ("ss", "REAGENTS", "Spiders' Silk", 0x0F8D, None),
            ("sa", "REAGENTS", "Sulfurous Ash", 0x0F8C, None),
            ("bw", "REAGENTS", "Bat Wing", 0x0F78, None),
            ("gd", "REAGENTS", "Grave Dust", 0x0F8F, None),
            ("db", "REAGENTS", "Daemon Blood", 0x0F7D, None),
            ("nc", "REAGENTS", "Nox Crystal", 0x0F8E, None),
            ("pi", "REAGENTS", "Pig Iron", 0x0F8A, None),
            ("p_heal", "POTIONS", "Heal", 0x0F0C, None),
            ("p_cure", "POTIONS", "Cure", 0x0F07, None),
            ("p_refresh", "POTIONS", "Refresh", 0x0F0B, None),
            ("p_str", "POTIONS", "Strength", 0x0F09, None),
            ("p_agi", "POTIONS", "Agility", 0x0F08, None),
            ("p_ns", "POTIONS", "Night Sight", 0x0F06, None),
            ("p_expl", "POTIONS", "Explosion", 0x0F0D, None),
            ("p_poison", "POTIONS", "Poison", 0x0F0A, None),
            ("s_recall", "SCROLLS", "Recall", 0x1F4C, None),
            ("s_gate", "SCROLLS", "Gate Travel", 0x1F60, None),
            ("s_mark", "SCROLLS", "Mark", 0x1F59, None),
            ("s_gheal", "SCROLLS", "Greater Heal", 0x1F49, None),
            ("s_heal", "SCROLLS", "Heal", 0x1F31, None),
            ("s_cure", "SCROLLS", "Cure", 0x1F37, None),
            ("s_acure", "SCROLLS", "Arch Cure", 0x1F45, None),
            ("s_mr", "SCROLLS", "Magic Reflection", 0x1F50, None),
            ("s_invis", "SCROLLS", "Invisibility", 0x1F58, None),
            ("s_reveal", "SCROLLS", "Reveal", 0x1F5C, None),
            ("s_tele", "SCROLLS", "Teleport", 0x1F42, None),
            ("s_prot", "SCROLLS", "Protection", 0x1F3B, None),
            ("s_bless", "SCROLLS", "Bless", 0x1F3D, None),
            ("s_res", "SCROLLS", "Resurrection", 0x1F67, None),
            ("o_band", "OTHER", "Bandages", 0x0E21, None),
            ("o_arrow", "OTHER", "Arrows", 0x0F3F, None),
            ("o_bolt", "OTHER", "Bolts", 0x1BFB, None))
        SUPPLY_GROUPS = ("REAGENTS", "POTIONS", "SCROLLS", "OTHER")
        SUPPLY_DEFAULT = ("bp", "bm", "ga", "gi", "mr", "ns", "ss", "sa",
                          "p_heal", "p_cure", "p_refresh", "s_recall", "s_gate", "o_band")
        SUPPLIES_KEY = "UnitFrames_supplies"                 # the ticked rows
        SUPWARN_KEY = "UnitFrames_supwarn"                   # per row: low / critical amounts
        HUE_LOW = Kit.HUE_TITLE                              # a count at or below its low amount
        WARN_READ_EVERY = 0.25                               # seconds between reads of those boxes
        WARN_MAX = 9999


        settings = {"sup_open": False, "sup_deep": True, "sup_hide0": False, "sup_follow": True,
                    "sup_low": SUPPLY_LOW_DEFAULT, "sup_side": 0}
        NUMBERS = {"sup_low": (0, 9999), "sup_side": (0, 2)}
        st = {"next_supply": 0.0, "counts": {}, "next_save": 0.0, "shutting": False, "queue": []}
        supplies = set(SUPPLY_DEFAULT)     # keys of the rows shown in the supplies table
        sup = {"g": None, "c": {}, "rows": (), "at": None}   # the table
        warn = {}                          # supplies row key -> [low or None, critical or None]
        page = {"c": None, "store": ({}, {}), "next_warn": 0.0}
        _get, _put = Kit.get_var, Kit.put_var
        queue = Kit.queuer(st)


        def mute(ctrl):
            safe(lambda: ctrl.SetAcceptMouseInput(False))
            return ctrl


        def fit(text, width):
            return Kit.fit(text, width)


        def with_commas(n):
            return "{:,}".format(int(n))


        def with_tip(ctrl, text):
            """A settings control with its tooltip (every control on the page has one)."""
            safe(lambda: ctrl.SetTooltip(text))
            return ctrl


        def read_pairs(raw):
            for part in str(raw or "").split(","):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                if k not in settings:
                    continue
                if k in NUMBERS:
                    try:
                        lo, hi = NUMBERS[k]
                        settings[k] = max(lo, min(hi, int(v)))
                    except ValueError:
                        pass
                else:
                    settings[k] = v.strip() == "1"


        def load_settings():
            raw = _get(SET_KEY, "")
            read_pairs(raw if raw else _get(OLD_SETTINGS_KEY, ""))


        def save_settings():
            _put(SET_KEY, ",".join("%s=%s" % (k, settings[k] if k in NUMBERS
                                              else ("1" if settings[k] else "0"))
                                   for k in sorted(settings)))


        def load_supplies():
            raw = _get(SUPPLIES_KEY, "-")
            if raw == "-":                                   # never saved: the defaults
                return
            known = set(r[0] for r in SUPPLY_ITEMS)
            supplies.clear()
            supplies.update(k for k in raw.split(",") if k in known)


        def save_supplies():
            _put(SUPPLIES_KEY, ",".join(r[0] for r in SUPPLY_ITEMS if r[0] in supplies) or "none")


        def load_warn():
            """The supplies rows' own amounts: "bp=10/5,ga=/3" (low / critical, either
            left empty). A key of its own, which 2.6.04 never reads."""
            warn.clear()
            known = set(r[0] for r in SUPPLY_ITEMS)
            for part in _get(SUPWARN_KEY, "").split(","):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                if k not in known:
                    continue
                vals = []
                for txt in (v.split("/") + ["", ""])[:2]:
                    try:
                        vals.append(max(0, min(WARN_MAX, int(txt))))
                    except ValueError:
                        vals.append(None)
                if vals[0] is not None or vals[1] is not None:
                    warn[k] = vals


        def save_warn():
            parts = []
            for r in SUPPLY_ITEMS:
                lw = warn.get(r[0])
                if lw:
                    parts.append("%s=%s/%s" % (r[0], "" if lw[0] is None else lw[0],
                                               "" if lw[1] is None else lw[1]))
            _put(SUPWARN_KEY, ",".join(parts))


        # ---------- the table ----------
        def count_supplies():
            """Totals of every tracked row from your pack, by graphic (and hue
            where the row names one). One read of the pack every SUPPLY_EVERY."""
            wanted = {}
            for key, _grp, _cap, graphic, hue in SUPPLY_ITEMS:
                if key in supplies:
                    wanted.setdefault(graphic, []).append((key, hue))
            counts = dict((r[0], 0) for r in SUPPLY_ITEMS if r[0] in supplies)
            if not wanted:
                return counts
            pack_items = getattr(HOST, "pack_items", None)
            if pack_items is not None:            # (2.6.82) the pass's shared pack list
                try:
                    items = pack_items(bool(settings["sup_deep"]), PACK_AGE)
                except Exception:
                    items = []
            else:
                pack = int(safe(lambda: API.Backpack, 0) or 0)
                items = safe(lambda: list(API.ItemsInContainer(pack, bool(settings["sup_deep"]))),
                             []) if pack else []
            for it in items or ():
                try:                                  # the whole pack: no closure per item
                    rows = wanted.get(int(it.Graphic or 0))
                    if not rows:
                        continue
                    hue = int(it.Hue or 0) & 0x3FFF
                    amount = max(1, int(it.Amount or 1))
                except Exception:
                    rows = wanted.get(int(safe(lambda: it.Graphic, 0) or 0))
                    if not rows:
                        continue
                    hue = int(safe(lambda: it.Hue, 0) or 0) & 0x3FFF
                    amount = max(1, int(safe(lambda: it.Amount, 1) or 1))
                for key, want_hue in rows:
                    if want_hue is None or want_hue == hue:
                        counts[key] += amount
            return counts


        def supply_rows():
            """The rows to show: ticked, in table order, minus empties if asked."""
            return tuple((key, grp, cap) for key, grp, cap, _gr, _h in SUPPLY_ITEMS
                         if key in supplies and not (settings["sup_hide0"] and
                                                     not st["counts"].get(key, 0)))


        def supply_text(key):
            """The row's count and its colour: red at or below its critical amount
            (the page's "Red at or below" for a row without one), yellow at or
            below its low amount (none: no yellow)."""
            n = st["counts"].get(key, 0)
            lw = warn.get(key)
            crit = lw[1] if lw is not None and lw[1] is not None else settings["sup_low"]
            if n <= crit:
                hue = Kit.HUE_BAD
            elif lw is not None and lw[0] is not None and n <= lw[0]:
                hue = HUE_LOW
            else:
                hue = Kit.HUE_TEXT
            return with_commas(n), hue


        def build_supplies(rows):
            old = sup["g"]
            w = SUPPLY_W
            groups = [(grp, [r for r in rows if r[1] == grp]) for grp in SUPPLY_GROUPS
                      if any(r[1] == grp for r in rows)]
            heights = [26 + len(grows) * SUPPLY_ROW + 4 for _grp, grows in groups] or \
                [26 + 2 * SUPPLY_ROW + 4]
            h = 16 + sum(heights) + Kit.GAP * (len(heights) - 1)
            follow = bool(settings["sup_follow"])
            g = G.CreateGump(True, not follow)              # follows the frame, or is dragged
            Kit.add_window_frame(g, w, h, corners=False)
            c = {}
            y = 8
            art = dict((key, (graphic, hue)) for key, _g, _c, graphic, hue in SUPPLY_ITEMS)
            if not groups:
                Kit.add_section(g, 8, y, w - 16, heights[0], "SUPPLIES")
                hint = "None of these in your pack." if supplies else "No rows ticked yet."
                Kit.add_label(g, hint, 18, y + 26, Kit.HUE_INFO)
                Kit.add_label(g, "Pick rows: its settings page.", 18, y + 26 + SUPPLY_ROW,
                              Kit.HUE_INFO)
            for (grp, grows), sh in zip(groups, heights):
                Kit.add_section(g, 8, y, w - 16, sh, grp)
                for i, (key, _grp, cap) in enumerate(grows):
                    ry = y + 26 + i * SUPPLY_ROW
                    item_pic(g, art[key][0], art[key][1], 16, ry + (SUPPLY_ROW - SUPPLY_ICON) // 2 - 1)
                    text, hue = supply_text(key)
                    c[key] = Kit.add_label(g, text, w - 18 - Kit.text_w(text), ry + 2, hue)
                    Kit.add_label(g, fit(cap, w - 18 - SUPPLY_ICON - 4 - 18 - 6 - 44),
                                  18 + SUPPLY_ICON + 4, ry + 2)
                y += sh + Kit.GAP
            at = None
            if not follow:                                   # drag anywhere on the stone
                Kit.catcher(g, 0, 0, w, h, lambda: None, "Drag to move the supplies table",
                            movable=True)
                x, y0 = sup_pos()
                if Kit.is_open(old):
                    x, y0 = old.GetX(), old.GetY()
                Kit.place(g, x, y0, w, h)                # wholly on screen
            else:                                            # beside the frame from the first frame on
                a = frame_anchor(w, h)
                at = a[1] if a is not None else sup_pos()
                Kit.place(g, at[0], at[1], w, h)
            # (2.6.85) with the frame's arrow gone, its own way to close (after the
            # catcher, so it takes the click); the bag sidebar's Supplies opens it
            Kit.art_button(g, ({}, {}), "close", Kit.ART_CLOSE, w - 8 - 30, 10, None, "Close",
                           on_click=queue("close"))
            sup.update({"g": g, "c": c, "rows": rows, "at": at, "w": w, "h": h, "follow": follow,
                        "leader": None, "sig": None})   # (2.6.83) placed afresh after a build
            G.AddGump(g)
            if not follow:
                safe(lambda: Kit.on_moved(g, save_sup_pos))
            Kit.dispose(old)
            place_supplies()


        def item_pic(g, graphic, hue, x, y):
            """The item's own art, shrunk into a SUPPLY_ICON box."""
            try:
                p = G.CreateGumpItemPic(graphic, SUPPLY_ICON, SUPPLY_ICON)
                p.SetRect(x, y, SUPPLY_ICON, SUPPLY_ICON)
                if hue:
                    safe(lambda: setattr(p, "Hue", hue))
                safe(lambda: setattr(p, "DrawBorder", False))
                g.Add(mute(p))
            except Exception:
                pass


        SUP_DEFAULT_POS = (60, 620)                      # a free-floating table, never saved


        def sup_pos():
            raw = _get(SUPPOS_KEY, "")
            sup["saved"] = raw                           # what is on disk: written only on change
            try:
                x, y = (int(v) for v in raw.split(","))
                return Kit.adapt(x, y, sup.get("w", 0), sup.get("h", 0))   # on the screen of today
            except ValueError:
                a = frame_anchor(sup.get("w", SUPPLY_W), sup.get("h", 0))   # first time: by the frame
                return a[1] if a is not None else SUP_DEFAULT_POS


        def save_sup_pos():
            """Where a free-floating table sits, written only when it differs from
            what was last written (this runs every SAVE_EVERY as well as on a drop)."""
            g = sup["g"]
            if Kit.is_open(g) and not sup.get("follow", True):
                try:
                    data = "%d,%d" % (int(g.GetX()), int(g.GetY()))
                except Exception:
                    return                               # a failed read is never saved
                if data != sup.get("saved"):
                    sup["saved"] = data
                    _put(SUPPOS_KEY, data)


        def frame_anchor(w, h):
            """(the player frame's window, where the table goes), or None with Frames off."""
            fn = HOST.services.get("frames.player_anchor")
            if fn is None:
                return None
            try:
                return fn(w, h, settings["sup_side"])
            except Exception:
                return None


        def place_supplies():
            """Keep the table beside the player frame (it follows a drag)."""
            g = sup["g"]
            if not Kit.is_open(g) or not sup.get("follow", True):
                return
            a = frame_anchor(sup["w"], sup["h"])
            if a is None:
                return
            leader, at = a
            if sup.get("leader") is not leader:              # kept on screen with the frame
                sup["leader"] = leader
                safe(lambda: Kit.attach(g, leader))
            if at != sup["at"]:
                sup["at"] = at                           # the spot asked for (not re-placed)
                try:
                    # 2.6.81: Kit.place, not a raw SetRect: on screen, and a table cut
                    # to the screen keeps its cut height and scrollbar band
                    Kit.place(g, at[0], at[1], sup["w"], sup["h"])
                    Kit.moved_by_code(g)                 # our move, not a drag
                except Exception:
                    pass


        def update_supplies(now):
            if not settings["sup_open"]:
                if sup["g"] is not None:
                    save_sup_pos()
                    g, sup["g"] = sup["g"], None
                    Kit.dispose(g)
                return
            recount = now >= st["next_supply"] or not st["counts"]
            if recount:
                st["next_supply"] = now + SUPPLY_EVERY
                st["counts"] = count_supplies()
            # the rows and their numbers only change with a recount (a settings or
            # rows change asks for one at once): between recounts the table only
            # follows the frame
            if not Kit.is_open(sup["g"]) or sup.get("follow") != bool(settings["sup_follow"]):
                save_sup_pos()
                build_supplies(supply_rows())
            elif recount:
                rows = supply_rows()
                if rows != sup["rows"]:
                    save_sup_pos()
                    build_supplies(rows)
                else:
                    for key, _grp, _cap in rows:
                        text, hue = supply_text(key)
                        lbl = sup["c"].get(key)
                        if lbl is not None and Kit.set_text(lbl, text, hue):
                            safe(lambda: lbl.SetPos(sup["w"] - 18 - Kit.text_w(text), lbl.GetY()))
                    place_supplies()
            else:
                place_supplies()


        # ---------- "choose rows" window (what the supplies table tracks) ----------
        ROWS_W = 620
        ROWS_POS_KEY = "UnitFrames_rowspos"
        rows_win = {"g": None, "c": {}, "store": ({}, {})}


        def save_rows_pos(g):
            _put(ROWS_POS_KEY, "%d,%d" % (safe(lambda: int(g.GetX()), 260),
                                          safe(lambda: int(g.GetY()), 160)))


        def build_rows_window():
            old = rows_win["g"]
            M, GAP = Kit.MARGIN, Kit.GAP
            w = ROWS_W
            IW = w - 2 * M
            longest = max(sum(1 for r in SUPPLY_ITEMS if r[1] == grp) for grp in SUPPLY_GROUPS)
            h_list = 52 + longest * SUP_ROW + 4          # title, group row, then the boxes
            h = M + 30 + GAP + h_list + M
            x, y = Kit.load_pos(ROWS_POS_KEY, (260, 160), (w, h))
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            Kit.add_window_frame(g, w, h)
            Kit.add_section(g, M, M, IW, 30)
            Kit.add_label(g, "SUPPLIES TABLE ROWS", M + 30, M + 7, Kit.HUE_TITLE)
            bx = w - M - 54 - 20 - 35 - Kit.text_w("Untick all")
            Kit.art_button(g, store, "none", Kit.ART_CLOSE, bx, M + 4, "Untick all",
                           "Take every row out of the table")
            bx -= 14 + 35 + Kit.text_w("Tick all")
            Kit.art_button(g, store, "all", Kit.ART_OK, bx, M + 4, "Tick all",
                           "Put every row in the table")
            Kit.catcher(g, M, M, bx - M - 6, 30, lambda: None, "Drag to move", movable=True)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close")
            yl = M + 30 + GAP
            Kit.add_section(g, M, yl, IW, h_list, "ROWS  (ticked rows show in the table)")
            cw = (IW - 16) // len(SUPPLY_GROUPS)
            for col, grp in enumerate(SUPPLY_GROUPS):
                cx = M + 10 + col * cw
                Kit.add_label(g, grp, cx, yl + 30, Kit.HUE_TITLE)
                for i, (key, _grp, cap, _gr, _h) in enumerate(r for r in SUPPLY_ITEMS if r[1] == grp):
                    c[key] = Kit.add_check(g, fit(cap, cw - 34), cx, yl + 52 + i * SUP_ROW,
                                           key in supplies)
            Kit.place(g, x, y, w, h)                     # wholly on screen
            rows_win.update({"g": g, "c": c, "store": store, "next_poll": 0.0})
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, lambda: save_rows_pos(g)))
            Kit.dispose(old)


        def close_rows_window():
            g, rows_win["g"] = rows_win["g"], None
            if Kit.is_open(g):
                save_rows_pos(g)
            Kit.dispose(g)
            rows_win["c"] = {}


        def poll_rows_window(now):
            """Read the ticks; save and refresh the table when they change. The
            boxes (38 reads) are read only on a pass a click poked, or every
            ROWS_POLL, not on every tick."""
            g = rows_win["g"]
            if g is None:
                return
            if not Kit.is_open(g):
                rows_win["g"] = None
                rows_win["c"] = {}
                return
            store, c = rows_win["store"], rows_win["c"]
            if Kit.was_clicked(store, "close"):
                close_rows_window()
                return
            poked = False
            for name, on in (("all", True), ("none", False)):
                if Kit.was_clicked(store, name):
                    poked = True
                    for cb in c.values():
                        safe(lambda: cb.SetIsChecked(on))
            if not poked and not getattr(HOST, "pass_poked", False) and \
                    now < rows_win.get("next_poll", 0.0):
                return
            rows_win["next_poll"] = now + ROWS_POLL
            ticked = set()
            for key, cb in c.items():
                try:
                    on = bool(cb.IsChecked)
                except Exception:
                    on = key in supplies
                if on:
                    ticked.add(key)
            if ticked != supplies:
                supplies.clear()
                supplies.update(ticked)
                save_supplies()
                st["next_supply"] = 0.0
                # the page's SUPPLY WARNINGS section (one box pair per row) and the
                # button's "(n of m)" tooltip: measured again even while the page
                # isn't shown (the list stays open when you switch page)
                HOST.refresh_settings(KEY)


        SUP_CHECKS = (("sup_follow", "The table sticks to the player frame",
                       "Untick to drag the table anywhere on the screen"),
                      ("sup_deep", "Count inside bags in your backpack",
                       "Also count items in bags and pouches inside your backpack"),
                      ("sup_hide0", "Hide rows you have none of",
                       "A row whose count is 0 is left out of the table"))
        SUP_LOW_TIP = ("Count at or below which a row shows red, unless the row has its own red "
                       "amount below (0-%d)" % NUMBERS["sup_low"][1])
        SUP_ROW = 24
        CFG_H = 118
        WARN_LINE = 26
        WARN_BOX = 44


        def warn_rows():
            """The supplies rows ticked (in table order): each gets its amounts."""
            return [r for r in SUPPLY_ITEMS if r[0] in supplies]


        def warn_height():
            return 30 + 20 + max(1, (len(warn_rows()) + 1) // 2) * WARN_LINE + 4


        def config_height(w):
            return CFG_H + Kit.GAP + warn_height()


        def build_config(g, x, y, w):
            c = {}
            store = ({}, {})
            y4 = y
            Kit.add_section(g, x, y4, w, CFG_H, "TABLE")
            spots = ((x + 12, y4 + 30), (x + 12 + (w // 2), y4 + 30), (x + 12, y4 + 56))
            for (k, text, tip), (cx, cy) in zip(SUP_CHECKS, spots):
                c[k] = Kit.add_check(g, text, cx, cy, settings[k], tip)
            Kit.add_label(g, "Red at or below:", x + 12, y4 + 86)
            tx = x + 24 + Kit.text_w("Red at or below:")
            c["sup_low"] = with_tip(Kit.add_textbox(g, str(settings["sup_low"]), tx, y4 + 82, 60),
                                    SUP_LOW_TIP)
            Kit.add_label(g, "Opens:", x + 12 + (w // 2), y4 + 86)
            dx = x + 24 + (w // 2) + Kit.text_w("Opens:")
            bx = x + w - 10 - 35 - Kit.text_w("Choose rows")
            Kit.art_button(g, store, "sup_rows", Kit.ART_PAGE, bx, y4 + 4, "Choose rows",
                           "Open the list of reagents, potions and scrolls the table can show "
                           "(%d of %d ticked)" % (len(supplies), len(SUPPLY_ITEMS)))
            # each ticked row's own amounts (2.6.05)
            y5 = y4 + CFG_H + Kit.GAP
            rows = warn_rows()
            Kit.add_section(g, x, y5, w, warn_height(),
                            "SUPPLY WARNINGS  (yellow and red counts, per row)")
            cw = (w - 36) // 2                           # two columns, 12 px clear of the edge
            boxes = []
            if not rows:
                Kit.add_label(g, "No rows ticked yet. Click Choose rows above to tick some.",
                              x + 12, y5 + 32, Kit.HUE_INFO)
            for col in range(2 if len(rows) > 1 else (1 if rows else 0)):
                bx = x + 12 + col * (cw + 12) + cw - 2 * WARN_BOX - 8
                Kit.add_label(g, "Yellow", bx, y5 + 28, Kit.HUE_TITLE)
                Kit.add_label(g, "Red", bx + WARN_BOX + 8, y5 + 28, Kit.HUE_BAD)
            for i, (key, _grp, cap, _gr, _h) in enumerate(rows):
                cx = x + 12 + (i % 2) * (cw + 12)
                ry = y5 + 50 + (i // 2) * WARN_LINE
                bx = cx + cw - 2 * WARN_BOX - 8
                Kit.add_label(g, fit(cap, bx - cx - 8), cx, ry + 3)
                lw = warn.get(key) or (None, None)
                lb = with_tip(Kit.add_textbox(g, "" if lw[0] is None else str(lw[0]), bx, ry, WARN_BOX),
                              "Yellow when %s is at or below this count (empty: never yellow)" % cap)
                cb = with_tip(Kit.add_textbox(g, "" if lw[1] is None else str(lw[1]),
                                              bx + WARN_BOX + 8, ry, WARN_BOX),
                              "Red when %s is at or below this count (empty: the Red at or below "
                              "number above)" % cap)
                boxes.append((key, lb, cb))
            c["warn"] = boxes
            # the drop-down goes last so its open list draws on top (of the
            # warnings section under it, too)
            try:
                dd = G.CreateDropDown(150, list(SUPPLY_SIDES), int(settings["sup_side"]))
                dd.SetPos(dx, y4 + 82)
                g.Add(dd)
                c["sup_side"] = with_tip(dd, "Which side of the player frame the table opens on "
                                         "(it flips to the other side when there is no room)")
            except Exception:
                c["sup_side"] = None
                Kit.add_label(g, SUPPLY_SIDES[settings["sup_side"]], dx, y4 + 86, Kit.HUE_INFO)
            page.update({"c": c, "store": store, "next_warn": 0.0})


        def checked(c, k, default):
            try:
                return bool(c[k].IsChecked)
            except Exception:
                return default


        def poll_config():
            c = page["c"]
            if c is None:
                return
            sup_changed = False
            for k, _t, _tip in SUP_CHECKS:
                v = checked(c, k, settings[k])
                if v != settings[k]:
                    settings[k] = v
                    sup_changed = True
            try:
                txt = c["sup_low"].Text
            except Exception:
                txt = ""
            try:
                low = int(str(txt or "").strip() or -1)
            except ValueError:
                low = -1
            if low >= 0:
                low = max(NUMBERS["sup_low"][0], min(NUMBERS["sup_low"][1], low))
                if low != settings["sup_low"]:
                    settings["sup_low"] = low
                    sup_changed = True
            dd = c.get("sup_side")
            if dd is not None:
                try:
                    side = int(dd.GetSelectedIndex())
                except Exception:
                    side = settings["sup_side"]
                if side is not None and 0 <= side < len(SUPPLY_SIDES) and side != settings["sup_side"]:
                    settings["sup_side"] = side
                    sup_changed = True
            if Kit.was_clicked(page["store"], "sup_rows"):
                queue("sup_rows")()
            if c.get("warn") and time.time() >= page.get("next_warn", 0.0):
                page["next_warn"] = time.time() + WARN_READ_EVERY   # not every pass
                if read_warn_boxes(c):
                    st["next_supply"] = 0.0                       # recolour the table now
            if sup_changed:
                save_settings()
                st["next_supply"] = 0.0                       # recount and redraw the table
                sup["at"] = None


        def read_warn_boxes(c):
            """The SUPPLY WARNINGS boxes: empty = none, a number = that amount, else
            (not a number) the amount stays. Saved when one changed; True then."""
            changed = False
            for key, lb, cb in c.get("warn") or ():
                old = warn.get(key) or [None, None]
                new = list(old)
                for i, box in ((0, lb), (1, cb)):
                    try:
                        if box.IsDisposed:               # a gone box reads "": not "cleared"
                            continue
                        txt = str(box.Text or "").strip()
                    except Exception:
                        continue
                    if not txt:
                        new[i] = None
                    else:
                        try:
                            new[i] = max(0, min(WARN_MAX, int(txt)))
                        except ValueError:
                            pass
                if new != list(old):
                    if new[0] is None and new[1] is None:
                        warn.pop(key, None)
                    else:
                        warn[key] = new
                    changed = True
            if changed:
                save_warn()
            return changed


        def config_closed():
            c = page["c"]
            if c is not None and c.get("warn") and read_warn_boxes(c):   # the last typed amounts
                st["next_supply"] = 0.0
            page["c"] = None


        def open_table():
            """"supplies.open": the table up, or to the front if it is up (a press)."""
            queue("open")()


        def bring_front():
            g = sup["g"]
            if Kit.is_open(g):
                safe(lambda: Kit.client_control(g).BringOnTop())


        def _start():
            st.update({"next_supply": 0.0, "counts": {}, "next_save": 0.0, "shutting": False,
                       "queue": []})
            sup["saved"] = None                    # read with the table's place (sup_pos)
            load_settings()
            load_supplies()
            load_warn()
            HOST.services["supplies.open"] = open_table


        def _tick():
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                if action == "open":
                    if not settings["sup_open"]:
                        settings["sup_open"] = True
                        save_settings()
                        st["next_supply"] = 0.0
                    update_supplies(now)
                    bring_front()
                elif action == "close":
                    settings["sup_open"] = False
                    save_settings()
                elif action == "sup_rows":                   # Settings: Choose rows
                    build_rows_window()
            poll_rows_window(now)
            update_supplies(now)
            if now >= st["next_save"]:
                st["next_save"] = now + SAVE_EVERY
                save_sup_pos()                   # (written only when it moved)


        def _stop():
            st["shutting"] = True
            HOST.services.pop("supplies.open", None)
            save_settings()
            save_supplies()
            save_sup_pos()
            g, sup["g"] = sup["g"], None
            Kit.dispose(g)
            close_rows_window()


        # the settings page can be drawn (and polled) while the part is off, or
        # before its start(): it shows the saved rows and amounts, so polling its
        # boxes never takes empty ones for amounts you cleared
        load_settings()
        load_supplies()
        load_warn()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                "config_height": config_height, "build_config": build_config,
                "poll_config": poll_config, "config_closed": config_closed}

    # ---------- the parts, run side by side by the mother's PartSet ----------
    #  (part key, builder, tick interval, the 2.6.06 module key it keeps)
    PARTS = (
        ("bags", _part_bags, 0.1, "bag"),
        ("paperdoll", _part_paperdoll, 0.1, "character"),
        ("storage", _part_storage, 0.1, "storage"),
        ("restock", _part_restock, 0.1, "restock"),
        ("supplies", _part_supplies, 0.1, "supplies"),
    )
    MODULE = PartSet(KEY, TITLE, PARTS).hooks()
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("inventory", "Inventory",
             "Your bags, paperdoll, containers, restocking and supplies",
             _module_inventory, 0.1,
             category="Your things",
             parts=(
                 ("bags", "Bags",
                  "Every bag in one window: a grid, filters and sorting", True, ("bag",)),
                 ("paperdoll", "Paperdoll",
                  "Your character, what you wear and your stats, in one window", True, ("character",)),
                 ("storage", "Storage",
                  "What is in every container you opened, on every character", False, ("storage",)),
                 ("restock", "Restock",
                  "Tops your supplies up from a chest or the bank, on a press", False, ("restock",)),
                 ("supplies", "Supplies",
                  "A table of what is in your pack, with low counts marked", True, (), True),
             ),
             aliases=('Character', 'Unified Bag', 'Storage Index', 'Restock', 'paperdoll', 'bank', 'chest', 'find', 'sort', 'supplies', 'supplies table'))
else:
    import API
    API.SysMsg("Inventory is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
