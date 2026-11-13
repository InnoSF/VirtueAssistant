# Reagent Prices (key prices, category The world): a module of Virtue Assistant.
#
# It reads the price and stock of the eight reagents from every vendor buy list the player opens,
# keeps them per shop, shows the cheapest and a shop-by-shop grid in one window, ranks the best
# stops for a shopping list and writes the result into a book the player picks.
#
# Rules it keeps: the vendor buy list opens only when the player presses the Buy list button or
# its hotkey, one vendor per press (R1); nothing here buys anything or hands over gold (R7); Follow
# is the shared Alt+click toggle on the Buy list button (R5).
#
# Like every module it is one function that the mother script calls with HOST and Kit already in
# its namespace; the function returns the table of callbacks at its end. The client is reached by
# reflection (Tz) for the buy list, vendor items and book gump, because the API has no calls for
# them. Client work runs on the client tick (_tick); file work and the context menu run on the
# script thread (_thread_tick).
def _module_prices():
    """Build the Reagent Prices module and return its callback table for the mother script.

    Holds all of the module's state in the closure: settings (saved), st (run state), data (shops,
    vendors, reads, price history and the per-vendor observations), win (window parts) and bridge
    (cached client reflection). The returned dict has start, tick, stop, the settings page callbacks
    (config_height, build_config, poll_config, config_closed) and thread_tick / thread_wanted for the
    script thread.
    """
    KEY = "prices"
    TITLE = "Reagent Prices"
    SETTINGS_KEY = "ReagentPrices_settings"
    POS_KEY = "ReagentPrices_pos"
    MIN_KEY = "ReagentPrices_min"
    W = 420
    ROW_H = 22
    MINI = (340, 46)
    TRAY_ICON = 0x0F7A
    LIMITS = {"dist": (5, 60), "old": (1, 60)}
    CHECK_EVERY = 0.5
    AGE_EVERY = 10.0
    REREAD_GAP = 3.0
    RETRY = 5.0
    HIST_KEEP = 10
    ITEM_CAP = 400
    NAME_MAX = 24
    ORDER = ("SS", "NS", "BP", "GA", "SA", "BM", "GI", "MR")
    CODES = dict((Kit.REAGENTS[k][1], k) for k in ORDER)
    START_SHOPS = ("Castle British", "Delucia", "East Britain", "Jhelom", "Magincia", "Moonglow", "Moonglow 2",
                   "Moonglow/Papua", "Ocllo", "Serpent's Hold", "Skara Brae", "Trinsic", "Upper W Britain", "Vesper",
                   "West Britain", "Yew Abbey")
    DATA_FILE = "ReagentPrices_data.txt"
    KINDS = ("P", "V", "R", "H")
    NEW_SHOP = "New shop"
    PRE_KEEP = 30.0
    UI_MANAGER = "ClassicUO.Game.Managers.UIManager"
    SHOP_GUMPS = (("ClassicUO.Game.UI.Gumps.ShopGump", "IsBuyGump"),
                  ("ClassicUO.Game.UI.Gumps.ModernShopGump", "isPurchaseGump"))
    BUY_LAYERS = (0x1A, 0x1B)
    AGE = ((60, 1, "just now"), (3600, 60, "%d min ago"), (86400, 3600, "%d h ago"), (0, 86400, "%d d ago"))
    ASK_H = 36
    NAME_H = 28
    LINE_H = 34
    OVER_H = 36
    BOOK_KEY = "ReagentPrices_book"
    BOOK_GUMP = "ClassicUO.Game.UI.Gumps.ModernBookGump"
    BOOK_TITLE = "Reagent Prices"
    BOOK_FONT = 1
    LINE_MAX = 147
    BOOK_PAGES = 18
    BOOK_LINES = 8
    PAGES_PER_TICK = 4
    BOOK_WAIT = 1.0
    BOOK_REACH = 1
    WIDTH_CAP = 3000
    PICK_TIMEOUT = 15
    DAY = 86400
    GUMP_FAILS = 3
    BOOK_NAMES = {"SS": "Silk", "NS": "Shade", "BP": "Pearl", "GA": "Garlic", "SA": "Ash", "BM": "Moss",
                  "GI": "Ginseng", "MR": "Mandrake"}
    PAIRS = (("SS", "NS"), ("BP", "GA"), ("SA", "BM"), ("GI", "MR"))
    MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    BUY_RANGE = 8
    VENDOR_TITLES = ("mage", "alchemist", "herbalist")
    MENU_ENTRY = "Buy"
    MENU_WAIT = 3
    VENDOR_NOTO = 1
    HELD_GAP = 0.6
    PACK_AGE = 0.5
    KEEP_KEY = "ReagentPrices_keep"
    KEEP_MAX = 9999
    KEEPS = tuple("keep_" + k for k in ORDER)
    STRS = ("hk",)
    STOPS = 3
    LIMITS.update((k, (0, KEEP_MAX)) for k in KEEPS)
    GRID_MAX = 60
    SHOP_ROW = 28
    GONE_GAP = 3600
    GONE_REACH = 12
    HERE = " (here)"
    SIZE_KEY = "ReagentPrices_size"
    FONT = 14
    SC_MIN = 60
    SC_MAX = 150
    SETTLE = 0.3
    TTF_CAP = 4000
    HD = 27
    PAD = 9
    DD_MIN = 80
    GRID_TITLE = "ALL VENDORS  (price, stock; ^ up, v down)"
    VIEW_TIP = "Switch between the cheapest list and every vendor"
    LOG_FILE = "ReagentPrices_log.csv"
    LOG_MAX = 5000
    LOG_HEAD = "time,shop,reagent,price,stock,vendor,serial"
    HIST_FILE = "ReagentPrices_history.txt"
    HIST_ALL = 10000
    HIST_VENDOR = 400
    BUY_TIP = ("Open the nearest reagent vendor's buy list (within %d tiles). Alt+click: auto-follow (again to stop)"
               % BUY_RANGE)
    settings = {"say": True, "dist": 20, "book_open": True, "book_head": True, "old": 7, "hk": "", "skip_old": False,
                "grid": False, "keep_SS": 0, "keep_NS": 0, "keep_BP": 0, "keep_GA": 0, "keep_SA": 0, "keep_BM": 0,
                "keep_GI": 0, "keep_MR": 0}
    DEFAULTS = dict(settings)
    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "loaded": False, "seen": None,
          "check_at": 0.0, "aged_at": 0.0, "save_at": 0.0, "ask": None, "warned": set(), "load_fails": 0,
          "book": None, "book_serial": 0, "bookver": 0, "foreign": None, "ok_books": set(), "picking": None,
          "jobs": [], "have": None, "here": None, "hooked": None, "menu": False, "followed": None, "hk_at": 0.0,
          "pv": None, "logq": [], "log_at": 0.0, "log_fails": 0, "histq": [], "drops": [], "hist_at": 0.0,
          "hist_fails": 0, "obs_ok": False, "memo": {}, "miss": {}, "size": None, "resize_at": 0.0, "drawn": None,
          "sc": 1.0, "f": FONT, "hd": HD}
    win = {"g": None, "c": {}, "store": ({}, {})}
    data = {"shops": {}, "vendors": {}, "reads": {}, "hist": {}, "dirty": {}, "marks": 0, "obs": {}}
    bridge = {}
    widths = {}
    tw = {}
    page_c = {"tb": {}, "typed": {}, "n": 0}
    # Kit.basics gives the cleanup list, the queue of named actions and the journal say function.
    cleanup, queue, say = Kit.basics(st, TITLE)
    # The data file is read once while the module loads, so the first start needs no wait; it is used
    # only when it is fresh (PRE_KEEP seconds).
    pre = {"text": Kit.read_merge(Kit.data_path(DATA_FILE)), "at": time.time()}

    def load_settings():
        """Load the saved settings and the shopping list.

        Settings are one pipe-separated Kit variable (SETTINGS_KEY). The picked book serial is a hex
        string in BOOK_KEY, and the shopping list is a comma list of CODE:count in KEEP_KEY. Bad or
        missing values fall back to the defaults (0 for each count).
        """
        Kit.kv_load(SETTINGS_KEY, "|", settings, LIMITS, STRS)
        try:
            st["book_serial"] = int(Kit.get_var(BOOK_KEY, "") or "0", 16)
        except ValueError:
            st["book_serial"] = 0
        settings.update((k, 0) for k in KEEPS)
        for part in Kit.get_var(KEEP_KEY, "").split(","):
            code, _, n = part.partition(":")
            if code not in ORDER:
                continue
            try:
                settings["keep_" + code] = max(0, min(KEEP_MAX, int(n)))
            except ValueError:
                continue

    def save_settings():
        """Save the settings and the shopping list (only reagents with a count above 0).

        The keep_ counts go to KEEP_KEY, the rest to SETTINGS_KEY.
        """
        Kit.kv_save(SETTINGS_KEY, "|", settings, [k for k in sorted(DEFAULTS) if k not in KEEPS], LIMITS, STRS)
        Kit.put_var(KEEP_KEY, ",".join("%s:%d" % (k, settings["keep_" + k]) for k in ORDER if settings["keep_" + k]))

    def lost(what):
        """Say once per run that a client member could not be reached (TazUO changed); what names it."""
        if what not in st["warned"]:
            st["warned"].add(what)
            say("couldn't reach the client's %s (TazUO changed)." % what, Kit.HUE_BAD)

    def gump_getter(t):
        """Return the client's generic UIManager.GetGump method closed over the gump type t.

        The generic definition is found once and cached in bridge. Raises if the client has no such
        method (callers treat that as lost).
        """
        if "gg" not in bridge:
            bridge["gg"] = [m for m in Tz.T(UI_MANAGER).GetMethods(Client.flags(static=True))
                            if m.Name == "GetGump" and m.IsGenericMethodDefinition][0]
        return bridge["gg"].MakeGenericMethod(t)

    def shop_open():
        """Return (gump, vendor serial) of the open vendor buy list, or None when none is open.

        The client has two shop gump classes (classic and modern); each is asked through its own
        GetGump with a None serial and its buy-list flag is checked. The members are resolved once; if
        any is missing the module says so once and answers None from then on.
        """
        # Reflection lookups are cached in bridge; a stored None means the lookup failed and is not
        # repeated.
        if bridge.get("shop") is None:
            if "shop" in bridge:
                return None
            bridge["shop"] = None
            try:
                import System
                found = []
                for name, flag in SHOP_GUMPS:
                    t = Tz.T(name)
                    if not Tz.has(t, flag, Client.flags()):
                        raise Exception("no %s" % flag)
                    found.append((gump_getter(t), flag))
                bridge["none"] = System.Array[object]([None])
                bridge["shop"] = found
            except Exception:
                lost("shop list")
                return None
        try:
            for gg, flag in bridge["shop"]:
                g = gg.Invoke(None, bridge["none"])
                if g is not None and not g.IsDisposed and Tz.get(g, flag):
                    return g, int(g.LocalSerial)
        except Exception:
            pass
        return None

    def vendor_items(serial):
        """Read the items a vendor offers as (graphic, price, amount) tuples, or None.

        Reads the vendor mobile's buy-container layers straight from the client world, because the
        price shown in the buy list is held on the item itself (Item.Price) and the API does not expose
        it. The list is a chain of items linked by Next; ITEM_CAP guards against a loop. Returns None
        when the mobile is not known to the client or on any reflection error.
        """
        if bridge.get("mobs") is None:
            if "mobs" in bridge:
                return None
            bridge["mobs"] = None
            try:
                import System
                # The API's World when it has one, else the client's own World object.
                world = Typing._get(API, "World")
                if world is None:
                    world = Tz.get(Tz.get(Tz.get(None, "Game", Tz.T("ClassicUO.Client")), "UO"), "World")
                # Layer constants must be real enum values for FindItemByLayer; the serial must be a UInt32.
                lt = Tz.T("ClassicUO.Game.Data.Layer")
                bridge["layers"] = [System.Enum.ToObject(lt, n) for n in BUY_LAYERS]
                bridge["u32"] = System.UInt32
                bridge["mobs"] = Tz.get(world, "Mobiles")
            except Exception:
                lost("shop list")
                return None
        try:
            mobs = bridge["mobs"]
            key = bridge["u32"](serial)
            if not mobs.ContainsKey(key):
                return None
            mob = mobs[key]
            out = []
            for layer in bridge["layers"]:
                box = mob.FindItemByLayer(layer)
                it = box.Items if box is not None else None
                # Walk the item chain of each buy container; the cap keeps a broken chain from hanging the tick.
                for _ in range(ITEM_CAP):
                    if it is None:
                        break
                    out.append((int(it.Graphic), int(it.Price), int(it.Amount)))
                    it = it.Next
            return out
        except Exception:
            return None

    def book_parts():
        """Resolve and cache the client members the book writer needs, or return None.

        Covers the modern book gump (its lines, redraw method, title and author boxes), the network
        senders for a page and for the header, the socket, the keyboard focus, the font table used to
        measure line widths and the array types for reflective calls. If any one is missing the module
        says so once and the book is never written.
        """
        if bridge.get("book") is None:
            if "book" in bridge:
                return None
            bridge["book"] = None
            try:
                import System
                bt = Tz.T(BOOK_GUMP)
                fl = Client.flags()
                sfl = Client.flags(static=True)
                ext = Tz.T("ClassicUO.Network.NetClientExt")
                net = Tz.T("ClassicUO.Network.AsyncNetClient")
                uo = Tz.get(Tz.get(None, "Game", Tz.T("ClassicUO.Client")), "UO")
                parts = {"get": gump_getter(bt), "lines": bt.GetProperty("BookLines", fl),
                         "redraw": bt.GetMethod("ServerSetBookText", fl), "title": bt.GetField("_titleTextBox", fl),
                         "author": bt.GetField("_authorTextBox", fl), "page": ext.GetMethod("Send_BookPageData", sfl),
                         "head": ext.GetMethod("Send_BookHeaderChanged", sfl),
                         "head_old": ext.GetMethod("Send_BookHeaderChanged_Old", sfl),
                         "socket": net.GetProperty("Socket", sfl),
                         "focus": Tz.T(UI_MANAGER).GetProperty("KeyboardFocusControl", sfl),
                         "ctl": Tz.T("ClassicUO.Game.UI.Controls.Control"),
                         "root": Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("RootParent", fl),
                         "fonts": Tz.get(Tz.get(uo, "FileManager"), "Fonts"), "u32": System.UInt32,
                         "objs": System.Array[object], "strs": System.Array[System.String]}
                if any(v is None for v in parts.values()):
                    raise Exception("no book member")
                bridge["book"] = parts
            except Exception:
                lost("book")
                return None
        return bridge["book"]

    def book_gump(serial):
        """Return the open book gump for a serial, or None when it is not open.

        Three failures in a row drop the cached members so they are looked up again.
        """
        b = book_parts()
        if b is None:
            return None
        try:
            g = b["get"].Invoke(None, b["objs"]([b["u32"](serial)]))
        except Exception:
            bridge["fails"] = bridge.get("fails", 0) + 1
            if bridge["fails"] >= GUMP_FAILS:
                bridge["book"] = None
                lost("book")
            return None
        bridge["fails"] = 0
        return g if g is not None and not g.IsDisposed else None

    def book_view(g):
        """Read the open book gump into a dict, or None on a reflection error.

        Keys: pages (count), known (pages the server has sent), edit (writable), lines (all text lines),
        new (new-style header), title, author and typing (a text box of this gump has keyboard focus).
        """
        b = bridge["book"]
        try:
            focus = b["focus"].GetValue(None)
            return {"pages": int(g.BookPageCount), "known": set(int(p) for p in g.KnownPages),
                    "edit": bool(g.IsEditable),
                    "lines": [str(x or "").rstrip("\n") for x in b["lines"].GetValue(g)], "new": bool(g.UseNewHeader),
                    "title": str(b["title"].GetValue(g).Text or ""), "author": str(b["author"].GetValue(g).Text or ""),
                    "typing": focus is not None and (focus is g or b["ctl"].IsInstanceOfType(focus) and
                                                     b["root"].GetValue(focus) is g)}
        except Exception:
            lost("book")
            return None

    def book_send(g, serial, pages, head):
        """Send pages and an optional header of the book to the server and mirror them in the gump.

        pages is a list of (page number, list of lines); head is (title, author, new-style flag) or
        None. Returns True when everything was sent, False on a reflection error. The page and header
        packets go straight to the server, then the gump's own line list and header boxes are updated so
        the player sees the same text without a re-request. Client tick.
        """
        b = bridge["book"]
        try:
            sock = b["socket"].GetValue(None)
            raw = b["lines"].GetValue(g)
            u = b["u32"](serial)
            if head is not None:
                b["head" if head[2] else "head_old"].Invoke(None, b["objs"]([sock, u, head[0], head[1]]))
                g.SetTile(head[0], True)
                g.SetAuthor(head[1], True)
            for page, lines in pages:
                # One packet per page; the local copy is written line by line to match what the server now holds.
                b["page"].Invoke(None, b["objs"]([sock, u, b["strs"](lines), page]))
                for i, text in enumerate(lines):
                    raw[(page - 1) * BOOK_LINES + i] = text
            if pages:
                b["redraw"].Invoke(g, None)
            return True
        except Exception:
            lost("book")
            return False

    def font_w(text):
        """Width in pixels of text in the book font; raises if the client cannot measure it."""
        b = book_parts()
        try:
            return int(b["fonts"].GetWidthUnicode(BOOK_FONT, text))
        except Exception:
            lost("book")
            raise

    def reagents_of(items):
        """Turn a vendor's items into {code: (price, stock)} for the eight reagents.

        Items with no price or no stock are ignored. When a vendor lists a reagent several times the
        lowest price wins, and equal prices add their stock.
        """
        got = {}
        for graphic, price, stock in items:
            code = CODES.get(graphic)
            if code is None or price <= 0 or stock <= 0:
                continue
            old = got.get(code)
            if old is None or price < old[0]:
                got[code] = (price, stock)
            elif price == old[0]:
                got[code] = (price, old[1] + stock)
        return got

    def spot_of(fields):
        """Return (map, x, y) from three text fields, or None when they are not three whole numbers."""
        try:
            return tuple(int(x) for x in fields) if len(fields) == 3 else None
        except ValueError:
            return None

    def spot_text(spot):
        """Return a spot as three text fields for the data file (empty when unknown)."""
        return [str(x) for x in spot] if spot else ["", "", ""]

    def parse(text):
        """Parse the data file text into {shops, vendors, reads, hist} (the model).

        Each line is pipe separated and starts with a kind letter: P shop (id, name, order, map x y),
        V vendor (serial in hex, shop id, map x y, name, first read time, last read time, time it was
        found gone), R read (serial, time, CODE:price:stock list) and H history (shop id, reagent code,
        list of time:price:stock). Anything after the known fields is kept as tail so a longer line
        survives a round trip. Lines that do not parse are skipped. A vendor's first and last times are
        raised to its read's time when they are older.
        """
        out = {"shops": {}, "vendors": {}, "reads": {}, "hist": {}}
        for line in (text or "").split("\n"):
            f = line.rstrip("\r").split("|")
            try:
                if f[0] == "P":
                    out["shops"][int(f[1])] = {"name": f[2], "order": int(f[3]), "spot": spot_of(f[4:7]), "tail": f[7:]}
                elif f[0] == "V":
                    out["vendors"][int(f[1], 16)] = {"shop": int(f[2]), "spot": spot_of(f[3:6]),
                                                     "name": clean(f[6]) if len(f) > 6 else "", "first": num(f, 7),
                                                     "last": num(f, 8), "gone": num(f, 9), "tail": f[10:]}
                elif f[0] == "R":
                    p = {}
                    for part in f[3].split(","):
                        if part:
                            code, price, stock = part.split(":")[:3]
                            p[code] = (int(price), int(stock))
                    out["reads"][int(f[1], 16)] = {"t": int(f[2]), "p": p, "tail": f[4:]}
                elif f[0] == "H":
                    rows = [tuple(int(x) for x in part.split(":")[:3]) for part in f[3].split(";") if part]
                    out["hist"][(int(f[1]), f[2])] = {"rows": [r for r in rows if len(r) == 3], "tail": f[4:]}
            except (IndexError, ValueError):
                continue
        for serial, v in out["vendors"].items():
            rd = out["reads"].get(serial)
            if rd is not None:
                v["first"] = v["first"] or rd["t"]
                v["last"] = max(v["last"], rd["t"])
        return out

    def num(f, i):
        """Whole number at index i of a split line, or 0 when it is missing or not a number."""
        try:
            return int(f[i])
        except (IndexError, ValueError):
            return 0

    def line_of(key):
        """Build the data file line for a key such as P|3, V|1A2B, R|1A2B or H|3|SS from the model.

        Returns None when the entry no longer exists (the caller then drops the line).
        """
        f = key.split("|")
        kind = f[0]
        if kind == "P":
            e = data["shops"].get(int(f[1]))
            body = e and [e["name"], str(e["order"])] + spot_text(e["spot"])
        elif kind == "V":
            e = data["vendors"].get(int(f[1], 16))
            body = e and [str(e["shop"])] + spot_text(e["spot"]) + [e.get("name", "")] + [
                str(e.get(k, 0)) for k in ("first", "last", "gone")]
        elif kind == "R":
            e = data["reads"].get(int(f[1], 16))
            body = e and [str(e["t"]), ",".join("%s:%d:%d" % (k, v[0], v[1]) for k, v in sorted(e["p"].items()))]
        else:
            e = data["hist"].get((int(f[1]), f[2]))
            body = e and [";".join("%d:%d:%d" % r for r in e["rows"])]
        return None if e is None else "|".join([key] + body + e["tail"])

    def key_of(line):
        """Return the key of a data file line (kind plus id, three parts for history), or None.

        Used by the merge so that a save replaces only the lines this module changed.
        """
        f = line.split("|")
        n = 3 if f[0] == "H" else 2
        return "|".join(f[:n]) if f[0] in KINDS and len(f) > n else None

    def mark(key):
        """Mark one data file line as changed so the next save writes it."""
        data["dirty"][key] = True
        data["marks"] += 1

    def use(model):
        """Replace the model with a freshly parsed one and queue a redraw."""
        data.update(model)
        queue.add("show")

    def load_data(text=None):
        """Load the data file (or the text given) into the model.

        When the file cannot be read it is retried every RETRY seconds and the journal says so on the
        second failure. An empty file starts with the 16 START_SHOPS. Script thread, or the start-up
        call with text read earlier.
        """
        if text is None:
            text = Kit.read_merge(Kit.data_path(DATA_FILE))
        if text is None:
            st["save_at"] = time.time() + RETRY
            st["load_fails"] += 1
            if st["load_fails"] == 2:
                say("couldn't read %s (trying again)." % DATA_FILE, Kit.HUE_BAD)
            return
        model = parse(text)
        if not text.strip():
            for i, name in enumerate(START_SHOPS):
                model["shops"][i + 1] = {"name": name, "order": i + 1, "spot": None, "tail": []}
                mark("P|%d" % (i + 1))
        st["loaded"] = True
        st["bookver"] += 1
        use(model)

    def save_data():
        """Write the changed lines to the data file, merged with what other characters wrote.

        Kit.merge_save re-reads the file and replaces only the dirty keys, so two characters sharing
        the file do not overwrite each other. A failure retries later. If the model changed while
        saving (a different mark count) the dirty flags stay for the next save. The merged result is
        parsed back as the model. Script thread.
        """
        keys = list(data["dirty"])
        entries = dict((k, line_of(k)) for k in keys)
        marks = data["marks"]
        try:
            out = Kit.merge_save(Kit.data_path(DATA_FILE), entries, key_of)
        except Exception:
            out = None
        if out is None:
            st["save_at"] = time.time() + RETRY
            return
        if data["marks"] != marks:
            return
        for k in keys:
            data["dirty"].pop(k, None)
        use(parse("\n".join(out)))

    def shop_ids():
        """Shop ids in display order (their order number, then id)."""
        return sorted(data["shops"], key=lambda sid: (data["shops"][sid]["order"], sid))

    def shop_name(sid):
        """Name of a shop id, or a question mark when it is gone."""
        return data["shops"][sid]["name"] if sid in data["shops"] else "?"

    def shop_of(serial):
        """Shop id a vendor is linked to, or None when unknown or the shop was removed."""
        v = data["vendors"].get(serial)
        return v["shop"] if v is not None and v["shop"] in data["shops"] else None

    def vkey(serial):
        """Sort key that puts a vendor in its shop's order, then by when it was first read (never-read last)."""
        v = data["vendors"][serial]
        sh = data["shops"].get(v["shop"])
        return (sh["order"] if sh else 0, not v.get("first"), v.get("first", 0), serial)

    def roster(live=False):
        """Group vendor serials by shop id, each group in vkey order.

        With live set, vendors marked gone are left out. Vendors of a removed shop are never listed.
        """
        out = {}
        for serial, v in data["vendors"].items():
            if v["shop"] in data["shops"] and not (live and v.get("gone")):
                out.setdefault(v["shop"], []).append(serial)
        for mates in out.values():
            mates.sort(key=vkey)
        return out

    def labels():
        """Name every vendor: {serial: (full label, short label)}.

        A named vendor is its name (a repeat of a name in the same shop gets a count) and the full label
        adds the shop. A vendor with no name yet is "vendor", or "vendor N" by its place in the shop when
        the shop has several.
        """
        out = {}
        for sid, mates in roster().items():
            seen = {}
            shop = shop_name(sid)
            for i, serial in enumerate(mates):
                name = data["vendors"][serial].get("name", "")
                low = name.lower()
                seen[low] = seen.get(low, 0) + 1
                if name:
                    short = name if seen[low] == 1 else "%s %d" % (name, seen[low])
                    full = short + ", " + shop
                elif len(mates) == 1:
                    short, full = "vendor", shop
                else:
                    short = "vendor %d" % (i + 1)
                    full = shop + " " + short
                out[serial] = (full, short)
        return out

    def tag(serial, tags=None):
        """Full label of a vendor, or just the shop name when the vendor has no label. Pass tags to reuse a
        labels() result.
        """
        return (tags or labels()).get(serial, (shop_name(shop_of(serial)), ""))[0]

    def vendor_prices(now=None):
        """Latest read per vendor: {serial: {code: (price, stock, read time)}}.

        Vendors that are gone or whose shop was removed are left out. With now given and Skip old prices
        on, reads older than Old after days are left out as well.
        """
        out = {}
        lim = settings["old"] * DAY if now is not None and settings["skip_old"] else None
        for serial, rd in data["reads"].items():
            v = data["vendors"].get(serial)
            if v is None or v["shop"] not in data["shops"] or v.get("gone") or lim is not None and now - rd["t"] > lim:
                continue
            out[serial] = dict((code, (price, stock, rd["t"])) for code, (price, stock) in rd["p"].items())
        return out

    def shop_prices(now=None, vp=None):
        """Best price per shop: {shop id: {code: (price, stock, read time)}}.

        When two vendors belong to one shop the lower price of each reagent counts, and a tie adds the
        stocks together. vp is a vendor_prices result to reuse; with it left out, now decides whether
        old reads are skipped as in vendor_prices.
        """
        out = {}
        for serial, p in (vendor_prices(now) if vp is None else vp).items():
            sp = out.setdefault(data["vendors"][serial]["shop"], {})
            for code, row in p.items():
                old = sp.get(code)
                if old is None or row[0] < old[0]:
                    sp[code] = row
                elif row[0] == old[0]:
                    sp[code] = (row[0], old[1] + row[1], max(old[2], row[2]))
        return out

    def cheapest(prices, rank=None):
        """Cheapest source per reagent: {code: (key, (price, stock, time))}.

        The keys of prices can be shop ids or vendor serials. A tie goes to the lower rank; rank defaults
        to the shop order and is given as a function of the key (vkey when the keys are vendors).
        """
        rank = rank or (lambda sid: data["shops"][sid]["order"])
        best = {}
        ranks = {}
        for key, sp in prices.items():
            r = rank(key)
            for code, row in sp.items():
                old = best.get(code)
                if old is None or (row[0], r) < (old[1][0], ranks[code]):
                    best[code] = (key, row)
                    ranks[code] = r
        return best

    def commas(n):
        """Format a whole number with thousands separators."""
        return "{:,}".format(int(n))

    def here_view():
        """What the open buy list shows for its own vendor, or None when no vendor is open.

        Returns (shop id or None, {code: (price, stock)}). While a read waits for the shop answer the
        pending prices are shown with no shop.
        """
        serial, a = st["here"], st["ask"]
        if serial is None:
            return None
        if a is not None and a["mode"] == "read" and a["serial"] == serial:
            return None, a["pend"]["p"]
        rd = data["reads"].get(serial)
        return shop_of(serial), (rd["p"] if rd else {})

    def ranking(prices, vp=None):
        """Rank the shops by what the shopping list costs there.

        How many to buy is the keep count minus what the backpack holds (from the pack count); with no
        list it is 1 of each reagent. Returns (want, whether a list is set, reagents still needed, the
        best STOPS shops). A ranked entry is (missing + short count, total cost, shop order, shop id,
        missing codes, short codes); fewer gaps come first, then the lower cost. Cost buys from a shop's
        vendors cheapest first and counts only the stock they really have. vp is the vendor_prices result
        that gives the individual vendors' offers; without it each shop's best price is used alone.
        """
        keep = dict((k, settings["keep_" + k]) for k in ORDER if settings["keep_" + k] > 0)
        have = st["have"] or {}
        want = dict((k, max(0, n - have.get(k, 0))) for k, n in keep.items()) if keep else dict((k, 1) for k in ORDER)
        need = [k for k in ORDER if want.get(k)]
        ranked = []
        offers = {}
        for serial, p in (vp or {}).items():
            for code, row in p.items():
                offers.setdefault((data["vendors"][serial]["shop"], code), []).append(row[:2])
        for sid, sp in (prices.items() if need else ()):
            got = {}
            for k in [k for k in need if k in sp]:
                left = want[k]
                cost = 0
                rows = sorted(offers.get((sid, k)) or [sp[k][:2]])
                for price, stock in rows:
                    n = min(left, stock)
                    cost += n * price
                    left -= n
                got[k] = (cost, sum(r[1] for r in rows))
            outs = [k for k in need if k not in got]
            shorts = [k for k in need if k in got and got[k][1] < want[k]]
            ranked.append((len(outs) + len(shorts), sum(x[0] for x in got.values()), data["shops"][sid]["order"], sid,
                           outs, shorts))
        ranked.sort()
        return want, bool(keep), need, ranked[:STOPS]

    def lack_text(r):
        """Text for what a ranked shop lacks: "no ..." for reagents it does not list, "short ..." for too
        little stock.
        """
        return "; ".join((["no " + ", ".join(r[4])] if r[4] else []) + (["short " + ", ".join(r[5])] if r[5] else []))

    def cost_line(prices, hv, want, listed, need):
        """The cost line shown above the best stops.

        Gives the total at the cheapest shops, and when a buy list is open also the cost here (with
        what is short). Without a shopping list it prices 1 of each reagent.
        """
        if not listed:
            return "For 1 of each reagent; set a shopping list in Settings"
        if not need:
            return "Your list: nothing to buy"
        best = cheapest(prices)
        gone = [k for k in need if k not in best]
        text = "%s at the cheapest" % commas(sum(want[k] * best[k][1][0] for k in need if k in best))
        if hv is not None:
            mine = hv[1]
            short = [k for k in need if k not in mine or mine[k][1] < want[k]]
            here = commas(sum(min(want[k], mine[k][1]) * mine[k][0] for k in need if k in mine))
            text = "%s here%s, %s" % (here, " (short %s)" % ", ".join(short) if short else "", text)
        return "Your list: " + text + ("; no price for %s" % ", ".join(gone) if gone else "")

    def last_read():
        """Serial of the vendor read most recently among vendors that belong to a shop, or None."""
        last = None
        for serial, rd in data["reads"].items():
            if shop_of(serial) is not None and (last is None or rd["t"] > data["reads"][last]["t"]):
                last = serial
        return last

    def first_unread():
        """Index of the first shop (in display order) that no vendor read has covered yet, else 0.

        It is the pick the "Which shop?" list starts on.
        """
        done = set(shop_of(s) for s in data["reads"])
        ids = shop_ids()
        return next((i for i, sid in enumerate(ids) if sid not in done), 0)

    def shape():
        """A tuple of the facts that decide the window's layout.

        When it differs from the one stored at build time the window is rebuilt; otherwise only the texts
        are refreshed. Index 4 says whether a shopping list is set and index 7 is the column widths.
        """
        a = st["ask"]
        return (a and a["mode"], bool(a and a["new"]), last_read() is not None, st["foreign"] is not None,
                any(settings[k] for k in KEEPS), settings["grid"], len(data["shops"]), cols(st["f"]))

    def sc(v, s=None):
        """Scale a pixel size by the window scale (or by s when given), rounded."""
        return int(round(v * (st["sc"] if s is None else s)))

    def fsize(s):
        """Pixel size of the body font at scale s, through the client's text size setting (at least 6)."""
        return max(6, Kit.tsize(int(round(FONT * s))))

    def pitch(s):
        """Row height at scale s: never less than 1.5 times the font size."""
        return max(sc(ROW_H, s), int(round(fsize(s) * 1.5)))

    def head_h(s):
        """Height of a section's title strip at scale s: never less than 1.9 times the font size."""
        return max(sc(HD, s), int(round(fsize(s) * 1.9)))

    def ty(bh):
        """Top offset that centres a line of text in a band of height bh."""
        return max(0, (bh - int(round(st["f"] * 1.3))) // 2)

    def ttf_w(text, size):
        """Pixel width of text in the smooth font at a size, cached.

        The cache is cleared when it holds TTF_CAP entries. A width the client cannot give is estimated
        from the length of the text and is not cached.
        """
        k = (text, size)
        w = tw.get(k)
        if w is None:
            if len(tw) >= TTF_CAP:
                tw.clear()
            w = 0
            if text:
                l = G.CreateGumpTTFLabel(text, size, "#FFFFFF")
                w = int(l.GetWidth() or 0)
                Kit.dispose(l)
                if not w:
                    return int(0.6 * size * len(text))
            tw[k] = w
        return w

    def tfit(text, room):
        """Cut text with two dots so that it fits in room pixels (found by bisection)."""
        f = st["f"]
        text = str(text or "")
        if ttf_w(text, f) <= room:
            return text
        lo, hi = 0, len(text) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ttf_w(text[:mid].rstrip() + "..", f) <= room:
                lo = mid
            else:
                hi = mid - 1
        return text[:lo].rstrip() + ".."

    def lab(g, text, x, y, hue=None):
        """Add one non-clickable smooth-font label to gump g at x, y and return it. The hue defaults to the
        normal text hue.
        """
        l = Kit.inert(G.CreateGumpTTFLabel(text, st["f"], "#FFFFFF"))
        l.Hue = Kit.HUE_TEXT if hue is None else hue
        l.SetPos(x, y)
        g.Add(l)
        return l

    def section(g, x, y, w, h, title=None):
        """Add a section frame to gump g, with its title (cut to fit) in the title hue when one is given."""
        Kit.add_section(g, x, y, w, h)
        if title:
            lab(g, tfit(title, w - 2 * sc(8)), x + sc(8), y + ty(st["hd"]), Kit.HUE_TITLE)

    def grid_rows():
        """The grid's rows as (shop id, vendor serial) pairs, in shop order.

        A shop with no live vendor gets one row with a serial of None.
        """
        live = roster(True)
        return [x for sid in shop_ids() for x in [(sid, s) for s in live.get(sid, [])] or [(sid, None)]]

    def cell(serial, code, row):
        """Grid cell text: price, the trend mark and the stock in brackets."""
        return "%d%s (%d)" % (row[0], trend(serial, code, row), row[1])

    def cols(f):
        """Natural column widths in pixels at font size f, measured from the longest text of each column.

        In the cheapest view this is (reagent name, price, buy count, age, shop-less message). In the grid
        view it is (shop, vendor, widest cell, row count).
        """
        if not settings["grid"]:
            return (max(ttf_w(Kit.REAGENTS[k][0], f) for k in ORDER), ttf_w("9999", f),
                    ttf_w("buy 9999", f) if any(settings[k] for k in KEEPS) else 0, ttf_w("59 min ago", f),
                    max(ttf_w("No price yet", f), ttf_w("Only old prices", f)))
        rows = grid_rows()
        tags = labels()
        vp = vendor_prices()
        first = set()
        shops = ["Shop"]
        names = ["Vendor"]
        cells = ["-"] + list(ORDER)
        for sid, serial in rows[:GRID_MAX]:
            if sid not in first:
                first.add(sid)
                shops.append(shop_name(sid))
            if serial is None:
                continue
            names.append(tags[serial][1] + (HERE if serial == st["here"] else ""))
            cells += [cell(serial, k, r) for k, r in vp.get(serial, {}).items()]
        return (max(ttf_w(x, f) for x in shops), max(ttf_w(x, f) for x in names), max(ttf_w(x, f) for x in cells),
                len(rows))

    def ctrl_w(f):
        """Width the controls below the list need at font size f: the Change line, the "Which shop?"
        question or the Overwrite bar, whichever is widest.
        """
        a = st["ask"]
        need = 0
        if a is None and last_read() is not None:
            need = 16 + 35 + Kit.text_w("Change") + 6 + 60
        if a is not None:
            need = 24 + ttf_w("Which shop?", f) + DD_MIN + 90 + Kit.text_w("OK") + Kit.text_w(
                "Skip" if a["mode"] == "read" else "Cancel")
        if st["foreign"] is not None:
            need = max(need, 26 + 35 + Kit.text_w("Overwrite") + 60)
        return need

    def need_w(s):
        """Smallest window width at scale s: the margins plus the widest of the base width, the columns
        and the controls.
        """
        f = fsize(s)
        m = cols(f)
        p = sc(8, s)
        if settings["grid"]:
            inner = sc(16, s) + m[0] + m[1] + 2 * p + len(ORDER) * (m[2] + p)
        else:
            inner = (sc(34, s) + m[0] + m[1] + 2 * sc(10, s) + m[4] + 2 * p + m[3] +
                     (m[2] + sc(10, s) if any(settings[k] for k in KEEPS) else 0))
        return 2 * Kit.MARGIN + max(sc(W - 2 * Kit.MARGIN, s), inner, ctrl_w(f))

    def bands():
        """Number of row bands: the grid's header and rows (capped at GRID_MAX), or one per reagent."""
        return 1 + max(1, min(GRID_MAX, len(grid_rows()))) if settings["grid"] else len(ORDER)

    def parts(s):
        """Heights of the optional parts at scale s: (status line, shop question, name box, best stops,
        Overwrite bar). Parts that are not shown are 0.
        """
        a = st["ask"]
        ah = max(ASK_H, sc(ASK_H, s)) if a else 0
        nh = max(NAME_H, sc(NAME_H, s)) if a and a["new"] else 0
        oh = max(OVER_H, sc(OVER_H, s)) if st["foreign"] is not None else 0
        sh = 0 if settings["grid"] else head_h(s) + (STOPS + 1) * pitch(s) + sc(PAD, s)
        return max(LINE_H, sc(LINE_H, s)), ah, nh, sh, oh

    def tail_h(p):
        """Total height of the parts below the list in p (from parts), each with its gap."""
        return sum(Kit.GAP + x for x in (p[0], p[1] + p[2], p[3], p[4]) if x)

    def need_h(s, k):
        """Window height needed at scale s for k row bands."""
        return 2 * Kit.MARGIN + 30 + Kit.GAP + head_h(s) + k * pitch(s) + sc(PAD, s) + tail_h(parts(s))

    def min_size():
        """Smallest (width, height) the window can have in the current view: the view at the smallest scale."""
        s = SC_MIN / 100.0
        return need_w(s), need_h(s, bands())

    def pick(w, h, k, mw):
        """Choose the largest scale in percent steps that fits a window of w by h with k row bands.

        The scale is limited by the height first, then by the width given the natural width mw at the
        smallest scale. Returns the scale as a fraction.
        """
        lo, hi = SC_MIN, SC_MAX
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if need_h(mid / 100.0, k) <= h:
                lo = mid
            else:
                hi = mid - 1
        M2 = 2 * Kit.MARGIN
        room = w - M2
        s = max(SC_MIN, min(lo, int(SC_MIN * room / max(1, mw - M2)))) / 100.0
        nw = need_w(s)
        while nw > w and s > SC_MIN / 100.0:
            s = max(SC_MIN, min(int(round(s * 100)) - 1, int(100.0 * s * room / (nw - M2)))) / 100.0
            nw = need_w(s)
        return s

    def own_size(mw, mh, k):
        """Window size to build at: the saved size, kept on screen and not below mw by mh.

        With no saved size it is the natural size at scale 1.0.
        """
        z = st["size"]
        W0, H0 = Kit.screen()
        if z is None:
            return max(mw, need_w(1.0)), max(mh, need_h(1.0, k))
        return max(mw, min(z[0], W0) if W0 > 0 else z[0]), max(mh, min(z[1], H0) if H0 > 0 else z[1])

    def load_size():
        """Saved window size (width, height) from the size variable, or None when it is missing or invalid."""
        try:
            w, h = [int(p) for p in Kit.get_var(SIZE_KEY, "").split(",")[:2]]
        except ValueError:
            return None
        return (w, h) if w > 0 and h > 0 else None

    def on_resized(*args):
        """Resize callback: note when the window was last resized, so the rebuild waits until the drag
        settles.
        """
        st["resize_at"] = time.time()

    def apply_resize():
        """Rebuild the window at its new size once a resize has settled. The size is saved for the next
        start. Ignored while minimised, while a layout holds the window or when the size is unchanged.
        """
        g = win["g"]
        if not Kit.is_open(g) or st["minimized"] or HOST.layout_holds(KEY):
            return
        gw, gh = int(g.GetWidth()), int(g.GetHeight())
        d = st["drawn"] or (0, 0)
        if abs(gw - d[0]) <= 2 and abs(gh - d[1]) <= 2:
            return
        st["size"] = (gw, gh)
        Kit.put_var(SIZE_KEY, "%d,%d" % (gw, gh))
        build_window()

    def trend(serial, code, row):
        """Price trend of one grid cell: "^" if it rose, "v" if it fell, empty if equal or no earlier read.

        Compares with this vendor's newest observation older than this read (the observations come from
        the history file).
        """
        i = ORDER.index(code)
        for t, p, _ in reversed(data["obs"].get(serial, ())):
            if t < row[2]:
                return "" if not p[i] else "^" if row[0] > p[i] else "v" if row[0] < p[i] else ""
        return ""

    def draw_ask(g, store, c, M, y, IW, a, ah, nh):
        """Draw the "Which shop?" section: the drop-down of shops (plus New shop), the name box when New
        shop is picked and the Skip / Cancel and OK buttons.

        The first button reads Skip for a pending read (the read is dropped) and Cancel when only
        changing the shop of the last vendor.
        """
        Kit.add_section(g, M, y, IW, ah + nh)
        x = M + IW - 8
        by = y + (ah - 24) // 2
        cancel = ("Skip", "Drop this read") if a["mode"] == "read" else ("Cancel", "Keep this vendor's shop")
        for key, art, cap, tip in (("ask_skip", Kit.ART_CLOSE) + cancel,
                                   ("ask_ok", Kit.ART_OK, "OK", "Link this vendor to the picked shop")):
            x -= 35 + Kit.text_w(cap)
            Kit.art_button(g, store, key, art, x, by, cap, tip, on_click=queue(key))
            x -= 10
        lab(g, "Which shop?", M + sc(8), y + ty(ah))
        dx = M + sc(8) + 8 + ttf_w("Which shop?", st["f"])
        ids = c["ask_ids"] = shop_ids()
        names = [shop_name(sid) for sid in ids] + [NEW_SHOP]
        if a["new"]:
            lab(g, "Name:", M + sc(8), y + ah + ty(nh))
            tb = Kit.add_textbox(g, "", dx, y + ah + (nh - NAME_H) // 2, x - dx, numbers=False)
            c["ask_name"] = Kit.with_tip(tb, "Name of the new shop (up to %d letters)" % NAME_MAX)
        dd = G.CreateDropDown(x - dx, names, max(0, min(a["pick"], len(ids))))
        dd.SetPos(dx, by)
        g.Add(dd)
        c["ask_dd"] = Kit.with_tip(dd, "Shop this vendor is in")

    def draw_over(g, store, M, y, IW, oh):
        """Draw the Overwrite bar shown when the picked book holds other writing."""
        Kit.add_section(g, M, y, IW, oh)
        x = M + IW - 8 - 35 - Kit.text_w("Overwrite")
        Kit.art_button(g, store, "overwrite", Kit.ART_OK, x, y + (oh - 24) // 2, "Overwrite",
                       "Write the prices over this book's text (this book only)", on_click=queue("overwrite"))
        lab(g, tfit("The book holds other writing", x - M - sc(8) - 10), M + sc(8), y + ty(oh), Kit.HUE_BAD)

    def draw_grid(g, c, M, y, IW, sh, n, m, rp):
        """Draw the grid section: headings, then n empty label rows that fill_grid fills.

        Column widths come from m (from cols) and rp is the row height.
        """
        section(g, M, y, IW, sh, GRID_TITLE)
        p8 = sc(8)
        sw, vw = m[0] + p8, m[1] + p8
        cw = max(m[2] + p8, (IW - sc(16) - sw - vw) // len(ORDER))
        vx = M + p8 + sw
        x0 = vx + vw
        c["name_w"] = sw - p8
        c["vendor_w"] = vw - p8
        c["cell_w"] = cw - sc(4)
        top = y + st["hd"] + ty(rp)
        for x, text in [(M + p8, "Shop"), (vx, "Vendor")] + [(x0 + i * cw, k) for i, k in enumerate(ORDER)]:
            lab(g, text, x, top, Kit.HUE_TITLE)
        c["grid"] = [(lab(g, "", M + p8, top + (j + 1) * rp),
                      [lab(g, "", x0 + i * cw, top + (j + 1) * rp) for i in range(len(ORDER))],
                      lab(g, "", vx, top + (j + 1) * rp)) for j in range(n)]

    def build_window():
        """Build the whole window from the current state, then refresh it.

        The scale is the largest that fits the window size (the zone slot, the saved size or the natural
        size). Layout: title row with the Buy list and View buttons, the cheapest list or the grid, the
        status line with Change, the "Which shop?" question, best stops and the Overwrite bar. Client tick.
        """
        grid = settings["grid"]
        if st["minimized"]:
            g, store, c = wnd.begin(MINI[0], MINI[1])
            wnd.end(g)
            st["drawn"] = None
            refresh()
            return
        k = bands()
        mw, mh = min_size()
        z = wnd.zone_slot(mw, mh)
        w, h = z if z else own_size(mw, mh, k)
        s = 1.0 if z is None and st["size"] is None else pick(w, h, k, mw)
        st.update(sc=s, f=fsize(s), hd=head_h(s), resize_at=0.0)
        rh = pitch(s)
        hd = st["hd"]
        rs = None if HOST.layout_holds(KEY) else (mw, mh, on_resized)
        g, store, c = wnd.begin(w, h, resize=rs)
        c["shape"] = shape()
        wnd.frame(g, mouse=rs is None, extra=[("buy", Kit.ART_PLAY, "Buy list", BUY_TIP, press_buy),
                                              ("view", Kit.ART_PAGE, "View: grid" if grid else "View: cheapest",
                                               VIEW_TIP, queue("view"))])
        M = Kit.MARGIN
        IW = w - 2 * M
        y = M + 30 + Kit.GAP
        a = st["ask"]
        listed = c["shape"][4]
        m = c["shape"][7]
        p = parts(s)
        lh, ah, nh, sh, oh = p
        bh = h - M - tail_h(p) - y
        rp = max(rh, (bh - hd - sc(PAD)) // k)
        if grid:
            draw_grid(g, c, M, y, IW, bh, k - 1, m, rp)
        else:
            section(g, M, y, IW, bh, "CHEAPEST")
            p8 = sc(8)
            nx = M + sc(34)
            px = nx + m[0] + sc(10)
            bx = px + m[1] + sc(10)
            sx = bx + (m[2] + sc(10) if listed else 0)
            ax = M + IW - p8 - m[3]
            c["shop_w"] = ax - p8 - sx
            c["rows"] = []
            pz = sc(20)
            dy = ty(rp)
            for i, code in enumerate(ORDER):
                ry = y + hd + i * rp
                name, graphic = Kit.REAGENTS[code]
                pic = G.CreateGumpItemPic(graphic, pz, pz)
                pic.SetPos(M + p8, ry + (rp - pz) // 2)
                Kit.inert(pic)
                g.Add(pic)
                lab(g, name, nx, ry + dy)
                c["rows"].append((code, lab(g, "", px, ry + dy), lab(g, "", sx, ry + dy),
                                  lab(g, "", ax, ry + dy, Kit.HUE_INFO),
                                  lab(g, "", bx, ry + dy, Kit.HUE_INFO) if listed else None))
        ys = y + bh + Kit.GAP
        section(g, M, ys, IW, lh)
        c["line_w"] = IW - 2 * sc(8)
        if a is None and last_read() is not None:
            bx = M + IW - 8 - 35 - Kit.text_w("Change")
            c["line_w"] = bx - 6 - M - sc(8)
            Kit.art_button(g, store, "change", Kit.ART_PAGE, bx, ys + (lh - 26) // 2, "Change",
                           "Pick another shop for the last vendor read", on_click=queue("change"))
        c["line"] = lab(g, "", M + sc(8), ys + ty(lh), Kit.HUE_INFO)
        ys += lh + Kit.GAP
        if a is not None:
            draw_ask(g, store, c, M, ys, IW, a, ah, nh)
            ys += ah + nh + Kit.GAP
        if not grid:
            section(g, M, ys, IW, sh, "BEST STOPS")
            c["stops_w"] = IW - 2 * sc(8)
            dy = ys + hd + ty(rh)
            c["stops"] = [lab(g, "", M + sc(8), dy + i * rh, Kit.HUE_INFO) for i in range(STOPS + 1)]
            ys += sh + Kit.GAP
        if st["foreign"] is not None:
            draw_over(g, store, M, ys, IW, oh)
        wnd.end(g)
        st["drawn"] = (int(g.GetWidth()), int(g.GetHeight()))
        refresh()

    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=MINI, icon=TRAY_ICON, cleanup=cleanup)

    def fill_rows(c, vall, vpool, hv, want, now):
        """Fill the cheapest list rows with text and colours.

        Without an open buy list each row shows the cheapest price, its shop (the vendor when the shop has
        more than one) and its age (grey when older than Old after). With one open, each row shows this
        vendor's price (green when it ties the best elsewhere or beats it) beside the best of every other
        vendor. hv is the here_view result, want how many to buy, vall all vendors' prices and vpool those
        that count for the cheapest.
        """
        here = st["here"] if hv else None
        tags = labels()
        live = roster(True)
        best = cheapest(dict((s, p) for s, p in vpool.items() if s != here) if hv else vpool, vkey)
        every = cheapest(vall, vkey)
        olds = settings["old"] * DAY
        for code, lp, ls, la, lb in c["rows"]:
            hit = best.get(code)
            if lb is not None:
                Kit.set_text(lb, "buy %d" % want[code] if code in want else "",
                             Kit.HUE_TEXT if want.get(code) else Kit.HUE_INFO)
            if hv is not None:
                mine = hv[1].get(code)
                good = mine is not None and (hit is None or mine[0] <= hit[1][0])
                Kit.set_text(lp, "out" if mine is None else str(mine[0]),
                             Kit.HUE_GOOD if good else Kit.HUE_INFO if mine is None else Kit.HUE_TEXT)
                Kit.set_text(ls, tfit("best %d %s" % (hit[1][0], tag(hit[0], tags)) if hit else "no other shop",
                                         c["shop_w"]), Kit.HUE_INFO)
                Kit.set_text(la, Kit.ago(now - hit[1][2], AGE) if hit else "", Kit.HUE_INFO)
                continue
            if hit is None:
                Kit.set_text(lp, "-", Kit.HUE_INFO)
                Kit.set_text(ls, tfit("Only old prices" if code in every else "No price yet", c["shop_w"]),
                             Kit.HUE_INFO)
                Kit.set_text(la, "")
                continue
            serial, row = hit
            hue = Kit.HUE_INFO if now - row[2] > olds else Kit.HUE_TEXT
            sid = shop_of(serial)
            name = tag(serial, tags) if len(live.get(sid, ())) > 1 else shop_name(sid)
            Kit.set_text(lp, str(row[0]), hue)
            Kit.set_text(ls, tfit(name, c["shop_w"]), hue)
            Kit.set_text(la, Kit.ago(now - row[2], AGE), Kit.HUE_INFO)

    def fill_grid(c, prices, vall, vpool, now):
        """Fill the grid cells: price, trend and stock per vendor and reagent.

        The cheapest of each column is green, an old price grey, a dash means not listed. The vendor of
        the open buy list is marked. When there are more vendors than rows the last row says how many are
        left out.
        """
        best = cheapest(vpool, vkey)
        ids = grid_rows()
        rows = c["grid"]
        more = len(ids) - len(rows) + 1
        olds = settings["old"] * DAY
        tags = labels()
        here = st["here"]
        for j, (ln, cells, lv) in enumerate(rows):
            hit = ids[j] if j < len(ids) and (more <= 1 or j < len(rows) - 1) else None
            sid, serial = hit or (None, None)
            sp = vall.get(serial)
            if hit is None:
                Kit.set_text(ln, tfit("+%d more vendors" % more, c["name_w"] + c["vendor_w"])
                             if j < len(ids) else "", Kit.HUE_INFO)
            else:
                first = j == 0 or ids[j - 1][0] != sid
                Kit.set_text(ln, tfit(shop_name(sid), c["name_w"]) if first else "",
                             Kit.HUE_INFO if sid not in prices else Kit.HUE_TEXT)
            text = tags[serial][1] + (HERE if serial == here else "") if serial is not None else ""
            Kit.set_text(lv, tfit(text, c["vendor_w"]), Kit.HUE_GOOD if serial is not None and serial == here else
                         Kit.HUE_INFO if sp is None else Kit.HUE_TEXT)
            for code, lbl in zip(ORDER, cells):
                row = sp.get(code) if sp else None
                if row is None:
                    Kit.set_text(lbl, "-" if sp is not None else "", Kit.HUE_INFO)
                    continue
                old = now - row[2] > olds
                low = code in best and row[0] <= best[code][1][0]
                Kit.set_text(lbl, tfit(cell(serial, code, row), c["cell_w"]),
                             Kit.HUE_INFO if old else Kit.HUE_GOOD if low else Kit.HUE_TEXT)

    def refresh():
        """Refresh the texts of the window from the model (client tick, cheap).

        Minimised, only the one-line status is updated; otherwise rows or grid, the status line, the
        cost line and the best stops.
        """
        c = win["c"]
        now = time.time()
        last = last_read()
        if last is None:
            text = "no reads yet"
        else:
            text = "read %s %s" % (tag(last), Kit.ago(now - data["reads"][last]["t"], AGE))
        if st["foreign"] is not None:
            text = "book holds other writing; Restore to overwrite"
        if st["ask"] is not None:
            text = "which shop? Restore to pick"
        if "status" in c:
            Kit.set_text(c["status"], "%s: %s" % (TITLE, text))
        elif "line" in c:
            vall = vendor_prices()
            vpool = vendor_prices(now)
            pool = shop_prices(vp=vpool)
            hv = here_view()
            want, listed, need, ranked = ranking(pool, vpool)
            if "grid" in c:
                fill_grid(c, shop_prices(vp=vall), vall, vpool, now)
            else:
                fill_rows(c, vall, vpool, hv, want, now)
            if st["ask"] is not None:
                line = "Which shop is this vendor in? Pick it below"
            elif last is None:
                line = "No reads yet: open a reagent vendor's buy list"
            else:
                line = "Last %s" % text
            Kit.set_text(c["line"], tfit(line, c["line_w"]), Kit.HUE_INFO)
            if "stops" not in c:
                return
            rows = [cost_line(pool, hv, want, listed, need)] + [
                "%d %s %s%s" % (i + 1, shop_name(r[3]), commas(r[1]), ": " + lack_text(r) if r[0] else "")
                for i, r in enumerate(ranked)]
            if need and not ranked:
                rows.append("No prices yet")
            for i, lbl in enumerate(c["stops"]):
                r = ranked[i - 1] if 0 < i <= len(ranked) else None
                Kit.set_text(lbl, tfit(rows[i] if i < len(rows) else "", c["stops_w"]),
                             Kit.HUE_TEXT if r is not None and not r[0] else Kit.HUE_INFO)

    def show():
        """Redraw after the model or the state changed: rebuild when the layout facts differ, else refresh.

        Also re-reads typed shop names when the shop count changed behind the settings page.
        """
        if page_c["tb"] and page_c["n"] != len(data["shops"]):
            read_names()
            page_c["n"] = len(data["shops"])
            HOST.refresh_settings(KEY)
        if not st["minimized"] and win["c"].get("shape") != shape():
            build_window()
        else:
            refresh()

    def ask(mode, serial, pend, pick):
        """Open the "Which shop?" question for a vendor.

        mode is "read" (a new read waits in pend) or "change" (relink the last vendor); pick is the
        index the list starts on. A minimised window cannot show it, so the journal asks the player to
        restore the window.
        """
        st["ask"] = {"mode": mode, "serial": serial, "pend": pend, "pick": pick, "new": False}
        show()
        if st["minimized"]:
            say("which shop is this vendor in? Restore the window to pick.")

    def add_hist(sid, code, row):
        """Add a read to the history of a shop and reagent, newest last, keeping HIST_KEEP rows."""
        h = data["hist"].setdefault((sid, code), {"rows": [], "tail": []})
        h["rows"].append(row)
        h["rows"].sort()
        del h["rows"][:-HIST_KEEP]
        mark("H|%d|%s" % (sid, code))

    def link(serial, sid, spot, picked=False, name="", t=0):
        """Link a vendor to a shop and remember where the vendor stands.

        Keeps the vendor's first read time, name and old place when the new values are empty, takes the
        newest last-read time and clears its gone mark when a read time is given. When the player picked
        the shop it also remembers that spot for the shop, so later vendors close to it are placed
        without asking.
        """
        old = data["vendors"].get(serial) or {"spot": None, "tail": []}
        data["vendors"][serial] = {"shop": sid, "spot": spot or old["spot"], "name": name or old.get("name", ""),
                                   "first": old.get("first") or t, "last": max(t, old.get("last", 0)),
                                   "gone": 0 if t else old.get("gone", 0), "tail": old["tail"]}
        mark("V|%X" % serial)
        if picked and (spot or old["spot"]):
            data["shops"][sid]["spot"] = spot or old["spot"]
            mark("P|%d" % sid)

    def shop_near(spot):
        """Shop id of the nearest known shop spot on the same map within Shop distance, or None.

        Spots come from the shops and from the vendors linked to them; distance is the larger of the
        two coordinate differences.
        """
        best, near = None, settings["dist"] + 1
        pins = [(sid, s["spot"]) for sid, s in data["shops"].items() if s["spot"]]
        pins += [(v["shop"], v["spot"]) for v in data["vendors"].values() if v["spot"] and v["shop"] in data["shops"]]
        for sid, sp in (pins if spot else ()):
            d = max(abs(sp[1] - spot[1]), abs(sp[2] - spot[2]))
            if sp[0] == spot[0] and d < near:
                best, near = sid, d
        return best

    def store_read(pend, sid, picked=False):
        """Store a vendor read under a shop.

        Links the vendor, replaces its read, adds history rows, queues the log and history lines and,
        when the journal line is on, says which reagents this vendor is cheapest for. Raises the book
        version so the book is written again. picked is True when the player chose the shop.
        """
        serial, t = pend["serial"], pend["t"]
        link(serial, sid, pend["spot"], picked, pend.get("name", ""), t)
        old = data["reads"].get(serial) or {"tail": []}
        data["reads"][serial] = {"t": t, "p": dict(pend["p"]), "tail": old["tail"]}
        mark("R|%X" % serial)
        for code, (price, stock) in pend["p"].items():
            add_hist(sid, code, (t, price, stock))
        log_read(pend, sid)
        line = hist_line(t, "%X" % serial, pend["p"])
        r = hist_row(line)
        q = st["histq"]
        obs = data["obs"].setdefault(serial, [])
        obs.append((r[0], r[2], r[3]))
        del obs[:-HIST_VENDOR]
        q.append(line)
        if len(q) > HIST_ALL:
            del q[:-HIST_ALL]
        st["miss"].pop(serial, None)
        if settings["say"]:
            pool = vendor_prices(time.time())
            best = cheapest(pool, vkey)
            here = pool.get(serial, {})
            won = [k for k in ORDER if k in here and here[k][0] == best[k][1][0]]
            say("%s read%s." % (tag(serial), "; cheapest for " + ", ".join(won) if won else ""), Kit.HUE_GOOD)
        st["bookver"] += 1
        show()

    def log_read(pend, sid):
        """Queue the csv log lines of a read, one per reagent (price empty and stock 0 when not listed).

        Each line is time, shop, reagent, price, stock, vendor name and serial in hex. Names with a comma
        or quote are quoted. The queue keeps at most LOG_MAX lines.
        """
        name = csv(shop_name(sid))
        when = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pend["t"]))
        q = st["logq"]
        who = "%s,%X" % (csv((data["vendors"].get(pend["serial"]) or {}).get("name", "")), pend["serial"])
        q.extend("%s,%s,%s,%s,%d,%s" % (when, name, Kit.REAGENTS[k][0], pend["p"][k][0] if k in pend["p"] else "",
                                        pend["p"][k][1] if k in pend["p"] else 0, who) for k in ORDER)
        if len(q) > LOG_MAX:
            del q[:-LOG_MAX]

    def csv(text):
        """Quote a field for the csv log when it holds a comma or a quote."""
        return '"%s"' % text.replace('"', '""') if "," in text or '"' in text else text

    def hist_line(t, who, p):
        """History file line for a read: time, who (vendor serial in hex) and the CODE:price:stock list."""
        return "%d|%s|%s" % (t, who, ",".join("%s:%d:%d" % (k, p[k][0], p[k][1]) for k in ORDER if k in p))

    def hist_key(line):
        """Key of a history file line (time and who), or None when it is malformed. Used to merge the file."""
        f = line.split("|")
        return "|".join(f[:2]) if len(f) > 2 else None

    def hist_row(line):
        """Parse a history line into (time, who, prices, stocks), or None when it does not parse.

        who is the vendor serial, or "S" and the shop id for old lines written before vendors were told
        apart. Prices and stocks are tuples in ORDER with 0 for a reagent not listed.
        """
        f = line.split("|")
        got = {}
        try:
            who = f[1].upper()
            key = "S%d" % int(who[1:]) if who[:1] == "S" else int(who, 16)
            for part in f[2].split(","):
                if part:
                    c = part.split(":")
                    got[c[0]] = (int(c[1]), int(c[2]))
            return (int(f[0]), key, tuple(got[k][0] if k in got else 0 for k in ORDER),
                    tuple(got[k][1] if k in got else 0 for k in ORDER))
        except (IndexError, ValueError):
            return None

    def fill_lines():
        """Build history lines for an empty history file from the saved model: the per-shop history rows,
        then each vendor's newest read.

        A row is credited to the vendor that read it when that is certain, else to the shop's only vendor,
        else to the shop alone.
        """
        vend, reads, by, owners, out = dict(data["vendors"]), dict(data["reads"]), {}, {}, []
        for (sid, code), h in list(data["hist"].items()):
            for t, price, stock in list(h["rows"]):
                by.setdefault((sid, t), {})[code] = (price, stock)
        for serial, v in vend.items():
            owners.setdefault(v["shop"], []).append(serial)
        for (sid, t), p in sorted(by.items()):
            mine = owners.get(sid, [])
            hit = [s for s in mine if s in reads and reads[s]["t"] == t]
            who = hit[0] if len(hit) == 1 else mine[0] if len(mine) == 1 else None
            out.append(hist_line(t, "S%d" % sid if who is None else "%X" % who, p))
        out.extend(hist_line(rd["t"], "%X" % s, rd["p"]) for s, rd in sorted(reads.items()) if s in vend)
        return out

    def flush_hist():
        """Write the queued history lines, unless another thread is already writing (script thread).

        A failed write retries after RETRY seconds and the journal says so on the second failure.
        """
        lock = st["log_lock"]
        if not lock.acquire(False):
            return
        try:
            ok = write_hist()
        except Exception:
            ok = False
        finally:
            lock.release()
        if not ok:
            st["hist_at"] = time.time() + RETRY
            st["hist_fails"] += 1
            if st["hist_fails"] == 2:
                say("couldn't write %s (trying again)." % HIST_FILE, Kit.HUE_BAD)
            return
        st["hist_fails"] = 0

    def write_hist():
        """Merge the queued history lines into the history file, trimmed to HIST_ALL lines and HIST_VENDOR
        per vendor, and rebuild the observations used for the trend marks (script thread).

        Rows of removed shops are dropped by the times in drops. Only the first n queued lines are
        removed, so lines queued meanwhile survive. Returns True when done, False when the file could not
        be read.
        """
        q, drops = st["histq"], st["drops"]
        n, nd = len(q), len(drops)
        path = Kit.data_path(HIST_FILE)
        text = Kit.read_merge(path)
        if text is None:
            return False
        new = (fill_lines() if not st["obs_ok"] and not text.strip() else []) + q[:n]
        gone = {}
        for k, at in drops[:nd]:
            gone[k] = max(at, gone.get(k, 0))
        merged = Kit.merge_text(text, dict((hist_key(x), x) for x in new), hist_key)[1]
        memo = st["memo"]
        rows = []
        for x in merged:
            r = memo.get(x) or hist_row(x)
            if r is not None and not (r[1] in gone and r[0] <= gone[r[1]]):
                rows.append((r, x))
        rows.sort(key=lambda e: e[0][0])
        per = {}
        keep = []
        for r, x in reversed(rows):
            if len(keep) >= HIST_ALL:
                break
            if per.get(r[1], 0) < HIST_VENDOR:
                per[r[1]] = per.get(r[1], 0) + 1
                keep.append((r, x))
        keep.reverse()
        out = "\n".join(x for r, x in keep)
        if out != "\n".join(x.rstrip("\r") for x in text.split("\n") if x.strip()):
            Kit.write_safe(path, out + "\n" if keep else "")
        obs = {}
        for r, x in keep:
            obs.setdefault(r[1], []).append((r[0], r[2], r[3]))
        for r in [hist_row(x) for x in q[n:]]:
            if r is not None:
                obs.setdefault(r[1], []).append((r[0], r[2], r[3]))
        st["memo"] = dict((x, r) for r, x in keep)
        data["obs"] = obs
        st["obs_ok"] = True
        del q[:n]
        del drops[:nd]
        return True

    def hist_due(now):
        """True when the history file needs work: data is loaded, the start-up settle time has passed, the
        retry time is reached and there are observations to build, lines queued or drops to apply.
        """
        return (st["loaded"] and HOST.settled_at is not None and now >= st["hist_at"] and
                (not st["obs_ok"] or bool(st["histq"]) or bool(st["drops"])))

    def flush_log():
        """Write the queued log lines unless another thread is already writing.

        A failed write retries after RETRY seconds and the journal says so on the second failure.
        Script thread (also from stop).
        """
        lock = st["log_lock"]
        # Non-blocking: if another thread holds the lock, the lines stay queued and go out next time.
        if not lock.acquire(False):
            return
        try:
            ok = write_log()
        finally:
            lock.release()
        if not ok:
            st["log_at"] = time.time() + RETRY
            st["log_fails"] += 1
            if st["log_fails"] == 2:
                say("couldn't write %s (trying again)." % LOG_FILE, Kit.HUE_BAD)
            return
        st["log_fails"] = 0

    def write_log():
        """Append the queued lines to the csv log, keeping its header and the last LOG_MAX lines.

        Returns True when written (the lines written are then removed from the queue), False when the
        file could not be read or written. Only the first n lines are removed so lines queued meanwhile
        survive.
        """
        q = st["logq"]
        n = len(q)
        path = Kit.data_path(LOG_FILE)
        text = Kit.read_safe(path)
        if text is None:
            return False
        rows = [x for x in text.replace("\r", "").split("\n") if x.strip()]
        rows = (rows[1:] if rows and rows[0].lower().startswith("time,") else rows) + q[:n]
        try:
            Kit.write_safe(path, "\n".join([LOG_HEAD] + rows[-LOG_MAX:]) + "\n")
        except Exception:
            return False
        del q[:n]
        return True

    def take_read(serial, now, got):
        """Handle a freshly opened buy list: skip a repeat, find the shop, then store or ask.

        A read identical to the stored one within REREAD_GAP seconds is ignored. The vendor's spot and
        name are taken from the mobile. A vendor with a known shop is stored at once; else the nearest
        known shop within Shop distance; else the window asks "Which shop?".
        """
        old = data["reads"].get(serial)
        if old is not None and now - old["t"] < REREAD_GAP and old["p"] == got:
            return
        mob = API.FindMobile(serial)
        spot = (int(API.GetMap()), int(mob.X), int(mob.Y)) if mob else None
        try:
            name = clean(mob.Name) if mob else ""
        except Exception:
            name = ""
        pend = {"serial": serial, "t": int(now), "p": got, "spot": spot, "name": name}
        sid = shop_of(serial)
        if sid is None:
            sid = shop_near(spot)
        if sid is None:
            ask("read", serial, pend, first_unread())
        else:
            store_read(pend, sid)

    def check_shop(now):
        """Watch the client for an open vendor buy list (client tick, every CHECK_EVERY seconds).

        A new list is read once: the same gump object is not read again, a list whose prices are not
        filled in yet is waited for, and a vendor with no reagents and no shop is ignored. After a read it
        also checks the shop's other vendors (sweep). While the same list stays open a change of the
        backpack asks for a new count of the pack. While a shop question for a read is open, nothing else
        is read.
        """
        a = st["ask"]
        hit = shop_open()
        if a is not None and a["mode"] == "read" and (hit is None or hit[1] == a["serial"]):
            return
        if hit is None:
            st["seen"] = None
            if st["here"] is not None:
                st["here"] = None
                want_count()
                show()
            return
        if st["seen"] is hit[0]:
            pv = HOST.pack_ver()
            if st["here"] is not None and pv != st["pv"]:
                st["pv"] = pv
                want_count()
            return
        items = vendor_items(hit[1])
        if items is not None and max([it[1] for it in items] or [0]) <= 0:
            return
        st["seen"] = hit[0]
        if items is None:
            return
        got = reagents_of(items)
        if got or shop_of(hit[1]) is not None:
            st["here"], st["pv"] = hit[1], HOST.pack_ver()
            want_count()
            take_read(hit[1], now, got)
            sweep(hit[1], now)
            show()
        elif st["here"] is not None:
            st["here"] = None
            show()

    def sweep(serial, now):
        """Check the other vendors of a shop after a read: learn their names and mark absent ones as gone.

        A vendor found in the client's world is present and gets its name if it has none. One that is not
        there while the player is within GONE_REACH tiles of its place counts as missing; missing on two
        checks at least GONE_GAP seconds apart marks it gone, which hides it until it is read again.
        """
        sid = shop_of(serial)
        miss = st["miss"]
        done = False
        try:
            me = (int(API.GetMap()), int(API.Player.X), int(API.Player.Y))
        except Exception:
            return
        for s in roster(True).get(sid, []) if sid is not None else ():
            v = data["vendors"][s]
            sp = v["spot"]
            if s == serial:
                continue
            try:
                mob = API.FindMobile(s)
            except Exception:
                continue
            if mob is not None:
                miss.pop(s, None)
                try:
                    name = "" if v.get("name") else clean(mob.Name)
                except Exception:
                    name = ""
                if name:
                    v["name"] = name
                    mark("V|%X" % s)
                    done = True
                continue
            if not sp or sp[0] != me[0] or max(abs(sp[1] - me[1]), abs(sp[2] - me[2])) > GONE_REACH:
                continue
            at = miss.get(s)
            if at is None or at < v.get("last", 0):
                miss[s] = now
            elif now - at >= GONE_GAP:
                v["gone"] = int(now)
                miss.pop(s)
                mark("V|%X" % s)
                done = True
        for s in sorted(miss, key=miss.get)[:max(0, len(miss) - ITEM_CAP)]:
            del miss[s]
        if done:
            st["bookver"] += 1

    def book_w(text):
        """Pixel width of book text, cached; the cache is cleared when it grows past WIDTH_CAP."""
        w = widths.get(text)
        if w is None:
            if len(widths) >= WIDTH_CAP:
                widths.clear()
            w = widths[text] = font_w(text)
        return w

    def fit_line(head, tail="", end=""):
        """Fit a book line into LINE_MAX pixels.

        The text is head + tail + end. The tail is cut first (with two dots marking the cut), then the
        end, then the head. Returns the line that fits.
        """
        text = head + tail + end
        while book_w(text) > LINE_MAX:
            if tail:
                tail = tail[:-1].rstrip()
                text = head + tail + ".." + end
            elif end:
                end = end[:-1]
                text = head + end
            else:
                head = head[:-1]
                text = head
        return text

    def stamp(t):
        """Format a time as day, month and clock, for example 5 Nov 14:30."""
        lt = time.localtime(t)
        return "%d %s %02d:%02d" % (lt.tm_mday, MONTHS[lt.tm_mon - 1], lt.tm_hour, lt.tm_min)

    def book_pages(now):
        """Build the 18 pages of the book, each a list of BOOK_LINES lines.

        Page 1: the cheapest shop for each reagent (an asterisk marks an old price). Page 2: the best
        stops with what each lacks. Pages 3 to 18: one shop each with when its newest vendor was read,
        the number of vendors when more than one, and the lowest prices in pairs (full names, short codes
        when too wide). Unused lines and pages are blank.
        """
        vall = vendor_prices()
        vpool = vendor_prices(now)
        prices = shop_prices(vp=vall)
        pool = shop_prices(vp=vpool)
        best = cheapest(pool)
        every = cheapest(prices)
        old = settings["old"] * DAY
        seen = {}
        many = {}
        for serial, p in vall.items():
            sid = shop_of(serial)
            many[sid] = many.get(sid, 0) + 1
            seen[sid] = max(seen.get(sid, 0), data["reads"][serial]["t"])

        def cost(row):
            """Price text for a row, with an asterisk when its read is older than Old after."""
            return "%d%s" % (row[0], "*" if now - row[2] > old else "")

        pages = [[fit_line("%s %s " % (code, cost(best[code][1])), shop_name(best[code][0])) if code in best
                  else "%s - (old)" % code if code in every else "%s - (no read)" % code for code in ORDER]]
        want, listed, need, ranked = ranking(pool, vpool)
        top = ["Best stops", "For: your list" if listed else "For: 1 of each"]
        if not ranked:
            top.append("No prices yet" if need else "Nothing to buy")
        top += [fit_line("%d " % (i + 1), shop_name(r[3]), " " + commas(r[1])) for i, r in enumerate(ranked)]
        pages.append(top + [fit_line("", shop_name(r[3]), ": " + lack_text(r)) for r in ranked if r[0]])
        for sid in shop_ids()[:BOOK_PAGES - 2]:
            sp = prices.get(sid, {})
            lines = [fit_line("", shop_name(sid))]
            if sid not in seen:
                lines.append("Not read yet")
            else:
                lines.append("Read " + stamp(seen[sid]))
                if many[sid] > 1:
                    lines.append("%d vendors" % many[sid])
                for a, z in PAIRS:
                    pa, pz = [cost(sp[k]) if k in sp else "out" for k in (a, z)]
                    line = "%s %s  %s %s" % (BOOK_NAMES[a], pa, BOOK_NAMES[z], pz)
                    lines.append(fit_line("", line if book_w(line) <= LINE_MAX else "%s %s  %s %s" % (a, pa, z, pz)))
            pages.append(lines)
        pages += [[] for _ in range(BOOK_PAGES - len(pages))]
        return [(p + [""] * BOOK_LINES)[:BOOK_LINES] for p in pages]

    def book_ours(view):
        """True when the book may be written without asking.

        That is a book titled Reagent Prices, one already in this layout (page 1 lines start with the
        reagent codes) or a completely blank one.
        """
        lines, known = view["lines"], view["known"]
        mine = (0 in known and len(lines) >= BOOK_LINES and
                all(lines[i].startswith(k + " ") for i, k in enumerate(ORDER)))
        blank = all(p in known for p in range(view["pages"])) and not any(x.strip() for x in lines)
        return view["title"].strip() == BOOK_TITLE or mine or blank

    def book_head(view, now):
        """Header to write (title, author, new-style flag), or None when it is already right or the option
        is off.

        The author carries the date of the last read.
        """
        if not settings["book_head"]:
            return None
        last = last_read()
        at = data["reads"][last]["t"] if last is not None else now
        head = (BOOK_TITLE, "Updated " + stamp(at), view["new"])
        return head if (view["title"], view["author"]) != head[:2] else None

    def book_near(serial):
        """True when the book is within reach: in the backpack, an open bank box, or on the ground within
        BOOK_REACH tiles.
        """
        top, holder = Kit.top_of(serial)
        if holder and top == int(API.Bank or 0):
            it = Kit.find_item(top)
            return it is not None and bool(it.Opened)
        if holder:
            return top == int(API.Backpack or 0)
        it = Kit.find_item(top)
        try:
            return it is not None and int(it.Distance) <= BOOK_REACH
        except Exception:
            return False

    def book_say(bk, text):
        """Journal a book problem once per open book."""
        if text not in bk["said"]:
            bk["said"].add(text)
            say(text, Kit.HUE_BAD)

    def drop_foreign():
        """Clear the Overwrite question."""
        if st["foreign"] is not None:
            st["foreign"] = None
            show()

    def book_start(bk, serial, view, now):
        """Start writing the book: check it and take a snapshot of the pages to send.

        Returns False (and says why, once) when the book cannot be written, is too far, or holds other
        writing and the player has not pressed Overwrite. Tells the player when the book has too few
        pages or the shops do not all fit. On success stores the pages and header in bk.
        """
        if not view["edit"]:
            book_say(bk, "couldn't write the book (can't be written).")
            return False
        if not book_near(serial):
            book_say(bk, "couldn't write the book (too far away).")
            return False
        if serial not in st["ok_books"] and not book_ours(view):
            if st["foreign"] != serial:
                st["foreign"] = serial
                show()
                say("the book holds other writing: press Overwrite to write over it.")
            return False
        try:
            pages = book_pages(now)
        except Exception:
            bk["ver"] = st["bookver"]
            return False
        st["ok_books"].discard(serial)
        drop_foreign()
        n = min(view["pages"], BOOK_PAGES)
        if n < BOOK_PAGES:
            book_say(bk, "book has %d pages; %d needed." % (n, BOOK_PAGES))
        extra = len(data["shops"]) - (BOOK_PAGES - 2)
        if extra > 0:
            book_say(bk, "the book holds %d shops; %d left out." % (BOOK_PAGES - 2, extra))
        bk.update({"ver": st["bookver"], "todo": pages[:n], "sent": set(), "head": book_head(view, now)})
        return True

    def book_tick(now):
        """Write the picked book while its gump is open (client tick, at the CHECK_EVERY pace).

        Waits until the book is not being typed in and the server has sent its pages. Sends at most
        PAGES_PER_TICK pages per tick, only those that differ, and stops when the book already matches
        or the data version has not changed. Closing the book drops the work.
        """
        serial = st["book_serial"]
        g = book_gump(serial) if serial else None
        bk = st["book"]
        if g is None:
            if bk is not None:
                st["book"] = None
                drop_foreign()
            return
        if bk is None or bk["g"] is not g:
            # With Write when opened off, the first pass waits for a data change instead of writing at once.
            bk = st["book"] = {"g": g, "at": now, "ver": None if settings["book_open"] else st["bookver"],
                               "said": set(), "todo": None, "sent": set(), "head": None}
        if bk["todo"] is None and bk["ver"] == st["bookver"]:
            return
        view = book_view(g)
        # Never write while the player types in the book; give the server BOOK_WAIT seconds to send pages.
        if view is None or view["typing"] or not view["known"] and now - bk["at"] < BOOK_WAIT:
            return
        if bk["todo"] is None:
            if not book_start(bk, serial, view, now):
                return
        elif not view["edit"] or not book_near(serial):
            bk["todo"], bk["ver"] = None, None
            return
        lines = view["lines"]
        todo = [(i + 1, p) for i, p in enumerate(bk["todo"])
                if i + 1 not in bk["sent"] and lines[i * BOOK_LINES:(i + 1) * BOOK_LINES] != p][:PAGES_PER_TICK]
        head, bk["head"] = bk["head"], None
        if not todo and head is None:
            bk["todo"] = None
            return
        if book_send(g, serial, todo, head):
            bk["sent"].update(p for p, _ in todo)
        else:
            bk["todo"] = None

    def pick_book():
        """Ask the player to target the book (Pick book... in the settings).

        The target is a client prompt through HOST; the answer comes back as a queued book_picked
        action. A second press while waiting is ignored.
        """
        if st["picking"] is not None:
            return
        token = st["picking"] = object()
        say("target the book for the prices.", Kit.HUE_INFO)

        def done(serial):
            """Target callback: queue the picked serial (0 when cancelled) unless a newer pick replaced it."""
            if st["picking"] is not token:
                return
            st["picking"] = None
            queue.add(("book_picked", int(serial or 0)), dup=True, front=True)

        HOST.pick_target(PICK_TIMEOUT, done, KEY)

    def book_picked(serial):
        """Remember the picked book (saved as a hex serial) and clear book state."""
        if not serial:
            say("no book picked.", Kit.HUE_INFO)
            return
        if Kit.find_item(serial) is None:
            say("that isn't an item.", Kit.HUE_BAD)
            return
        st.update({"book_serial": serial, "book": None, "ok_books": set()})
        drop_foreign()
        apply_names()
        Kit.put_var(BOOK_KEY, "%X" % serial)
        say("book picked; open it to write the prices.", Kit.HUE_GOOD)
        HOST.refresh_settings(KEY)

    def overwrite():
        """Allow writing over the book that holds other writing (this book only, this run)."""
        if st["foreign"] is not None:
            st["ok_books"].add(st["foreign"])
            drop_foreign()

    def clean(text):
        """Clean a typed shop name: no pipes, single spaces, at most NAME_MAX letters."""
        return " ".join(str(text or "").replace("|", " ").split())[:NAME_MAX]

    def add_shop(name):
        """Add a shop by name (or return the existing one with that name) and return its id."""
        for sid, s in data["shops"].items():
            if s["name"].lower() == name.lower():
                return sid
        sid = max(list(data["shops"]) + [len(START_SHOPS)]) + 1
        order = max([s["order"] for s in data["shops"].values()] + [0]) + 1
        data["shops"][sid] = {"name": name, "order": order, "spot": None, "tail": []}
        mark("P|%d" % sid)
        return sid

    def remove_shop(sid):
        """Remove a shop with its vendors, reads and history; at least one shop must stay.

        Pending typed names are applied first. The removed history is also queued as drops so the history
        file forgets it. A shop question for the removed shop's vendor is closed.
        """
        apply_names()
        if sid not in data["shops"]:
            return
        if len(data["shops"]) == 1:
            say("keep at least one shop.", Kit.HUE_BAD)
            return
        name = shop_name(sid)
        del data["shops"][sid]
        mark("P|%d" % sid)
        at = int(time.time())
        drops = st["drops"]
        for serial in [v for v, e in data["vendors"].items() if e["shop"] == sid] + ["S%d" % sid]:
            data["obs"].pop(serial, None)
            drops.append((serial, at))
            if serial not in data["vendors"]:
                continue
            del data["vendors"][serial]
            mark("V|%X" % serial)
            if data["reads"].pop(serial, None) is not None:
                mark("R|%X" % serial)
        del drops[:-ITEM_CAP]
        for key in [k for k in data["hist"] if k[0] == sid]:
            del data["hist"][key]
            mark("H|%d|%s" % key)
        a = st["ask"]
        if a is not None and a["mode"] == "change" and shop_of(a["serial"]) is None:
            st["ask"] = None
        st["seen"] = None
        st["bookver"] += 1
        say("removed %s." % name, Kit.HUE_INFO)
        show()

    def taken(name, sid=None):
        """True when another shop already has this name (case ignored)."""
        return any(s["name"].lower() == name.lower() and k != sid for k, s in data["shops"].items())

    def read_names(*args):
        """Copy what is typed in the shop name boxes of the settings page.

        The text is kept because the page is rebuilt while it is open.
        """
        for key, tb in list(page_c["tb"].items()):
            try:
                page_c["typed"][key] = str(tb.Text or "")
            except Exception:
                continue

    def apply_names():
        """Apply the typed shop names (renames), skipping empty, unchanged and duplicate names.

        Runs when the settings page closes and before add or remove.
        """
        read_names()
        typed = page_c["typed"]
        done = False
        for sid in [k for k in typed if k != "add"]:
            name = clean(typed.pop(sid))
            if sid not in data["shops"] or not name or name == data["shops"][sid]["name"]:
                continue
            if taken(name, sid):
                say("%s is already a shop." % name, Kit.HUE_BAD)
                continue
            data["shops"][sid]["name"] = name
            mark("P|%d" % sid)
            done = True
        if done:
            st["bookver"] += 1
            show()

    def add_typed():
        """Add the shop typed in the new shop box of the settings page."""
        apply_names()
        name = clean(page_c["typed"].get("add", ""))
        if not name:
            say("type a name for the new shop.", Kit.HUE_BAD)
            return
        if taken(name):
            say("%s is already a shop." % name, Kit.HUE_BAD)
            return
        page_c["typed"].pop("add", None)
        add_shop(name)
        st["bookver"] += 1
        say("added %s." % name, Kit.HUE_GOOD)
        show()

    def view():
        """Switch between the cheapest view and the grid view and rebuild the window."""
        settings["grid"] = not settings["grid"]
        save_settings()
        build_window()

    def relink(serial, sid):
        """Move a vendor and its history rows to another shop (the Change button)."""
        v, rd = data["vendors"].get(serial), data["reads"].get(serial)
        if v is None or v["shop"] == sid:
            return
        for code, (price, stock) in (rd["p"].items() if rd else ()):
            h, row = data["hist"].get((v["shop"], code)), (rd["t"], price, stock)
            if h is None or row not in h["rows"]:
                continue
            h["rows"].remove(row)
            mark("H|%d|%s" % (v["shop"], code))
            add_hist(sid, code, row)
            if not h["rows"]:
                del data["hist"][(v["shop"], code)]
        link(serial, sid, v["spot"], True)
        st["bookver"] += 1

    def watch_ask():
        """Watch the shop drop-down on the client tick and show the name box when New shop is picked."""
        a, c = st["ask"], win["c"]
        if a is None or "ask_dd" not in c:
            return
        try:
            idx = int(c["ask_dd"].GetSelectedIndex())
        except Exception:
            return
        if idx == a["pick"]:
            return
        a["pick"] = idx
        new = idx >= len(c["ask_ids"])
        if new != a["new"]:
            a["new"] = new
            show()

    def answer():
        """Answer the shop question (OK button).

        A picked shop stores a waiting read or relinks the vendor. New shop with no name typed asks for
        one and keeps the question open.
        """
        a, c = st["ask"], win["c"]
        if a is None or "ask_dd" not in c:
            return
        ids = c["ask_ids"]
        idx = int(c["ask_dd"].GetSelectedIndex())
        if 0 <= idx < len(ids):
            sid = ids[idx]
        else:
            name = clean(c["ask_name"].Text) if "ask_name" in c else ""
            if not name:
                if a["new"]:
                    say("type a name for the new shop.", Kit.HUE_BAD)
                a["new"], a["pick"] = True, len(ids)
                show()
                return
            sid = add_shop(name)
        st["ask"] = None
        if a["mode"] == "read":
            store_read(a["pend"], sid, True)
        else:
            relink(a["serial"], sid)
            show()

    def change():
        """Open the shop question for the last vendor read, starting on its current shop."""
        serial = last_read()
        if serial is not None and st["ask"] is None:
            ask("change", serial, None, shop_ids().index(shop_of(serial)))

    def skip():
        """Close the shop question; a waiting read is dropped."""
        st["ask"] = None
        show()

    def want_count():
        """Queue a pack count for the script thread, only when a shopping list is set."""
        if any(settings[k] for k in KEEPS) and ("count",) not in st["jobs"]:
            st["jobs"].append(("count",))

    def count_pack():
        """Count the eight reagents in the backpack and queue the result (script thread).

        Uses the shared pack item list (HOST.pack_items) with a short cache; bags inside are included.
        """
        got = dict((k, 0) for k in ORDER)
        try:
            items = HOST.pack_items(True, PACK_AGE)
        except Exception:
            return
        for it in items:
            try:
                code = CODES.get(int(it.Graphic))
                if code is not None:
                    got[code] += max(1, int(it.Amount or 1))
            except Exception:
                continue
        queue.add(("counted", got), dup=True)

    def counted(got):
        """Store the new pack count and redraw when it changed."""
        if got != st["have"]:
            st["have"] = got
            st["bookver"] += 1
            show()

    def open_menu(serial):
        """Open a vendor's buy list from its context menu (script thread).

        Runs only from the Buy list press (R1: the list never opens on its own). The menu entry is
        Buy. A failure is reported unless the module is stopping.
        """
        try:
            ok = API.ContextMenu(serial, MENU_ENTRY, MENU_WAIT)
        except Exception:
            ok = False
        st["menu"] = False
        if not ok and not st["shutting"]:
            say("couldn't open that vendor's buy list.", Kit.HUE_BAD)

    JOBS = {"count": count_pack, "menu": open_menu}

    def is_vendor(m, me):
        """True when a mobile can be a reagent vendor: already linked to a shop, or an invulnerable one
        whose name or properties hold mage, alchemist or herbalist.
        """
        serial = int(m.Serial)
        if serial == me:
            return False
        if shop_of(serial) is not None:
            return True
        if int(m.Notoriety) != VENDOR_NOTO:
            return False
        words = ("%s %s" % (m.Name or "", m.raw.NameAndProps(False) or "")).lower().split()
        return any(t in words for t in VENDOR_TITLES)

    def vendor_near():
        """Serial of the nearest reagent vendor within BUY_RANGE, or None."""
        best, near = None, BUY_RANGE + 1
        try:
            me = int(API.Player.Serial)
        except Exception:
            me = 0
        for m in HOST.mobiles(BUY_RANGE):
            try:
                d = int(m.Distance)
                if d < near and is_vendor(m, me):
                    best, near = int(m.Serial), d
            except Exception:
                continue
        return best

    def buy():
        """Open the buy list of the nearest reagent vendor (one press, one vendor)."""
        if st["menu"]:
            return
        serial = vendor_near()
        if serial is None:
            say("no reagent vendor in reach.", Kit.HUE_INFO)
            return
        st["menu"] = True
        st["jobs"].append(("menu", serial))

    def follow():
        """Toggle auto-follow of the nearest reagent vendor (Alt+click on the Buy list button).

        Follow is the shared toggle (R5): the same press ends it when it is already following this
        vendor.
        """
        was = st["followed"]
        target = was if was is not None and Follow.current() == was else vendor_near()
        if target is None:
            say("no reagent vendor in reach.", Kit.HUE_INFO)
            return
        st["followed"] = target if Follow.toggle(target, TITLE) else None

    buy_once = Kit.once(lambda: queue.add("buy", key=KEY), (KEY, "buy"))
    follow_once = Kit.once(lambda: queue.add("follow", key=KEY), (KEY, "follow"))

    def press_buy(*args):
        """Button handler: Alt held starts or stops Follow, a plain click opens the buy list."""
        if Follow.alt_held():
            follow_once()
            return
        buy_once()

    def hot_key(*args):
        """Hotkey handler: open the buy list. Ignored while the key repeats or the player is typing."""
        now = time.time()
        held = now - st["hk_at"] < HELD_GAP
        st["hk_at"] = now
        if not held and not HOST.typing():
            buy_once()

    def rehook():
        """Bring the registered hotkey in line with the Buy list setting.

        Releases the old key, registers the new one and tells the player when the text is not a key.
        """
        combo = _norm_key(settings["hk"]) if settings["hk"] else ""
        if combo == (st["hooked"] or ""):
            return
        if st["hooked"]:
            HOST.hotkey_off(st["hooked"], TITLE)
        st["hooked"] = None
        if not combo:
            return
        if HOST.hotkey_on(combo, TITLE, hot_key, "open a reagent vendor's buy list") is False:
            say("%s isn't a key." % settings["hk"], Kit.HUE_BAD)
            return
        st["hooked"] = combo

    # Names of the actions the queue can run on the client tick; tuples carry arguments.
    ACTIONS = {"show": show, "ask_ok": answer, "ask_skip": skip, "change": change, "pick_book": pick_book,
               "book_picked": book_picked, "overwrite": overwrite, "counted": counted, "buy": buy, "follow": follow,
               "view": view, "rm_shop": remove_shop, "add_shop": add_typed}

    def draw_shops(f, x, y):
        """Draw the SHOPS section of the settings page: one name box per shop with Remove, then an empty
        box with Add.
        """
        tb = page_c["tb"]
        tb.clear()
        page_c["n"] = len(data["shops"])
        bx = x + f.w - 12 - 35 - Kit.text_w("Remove")
        for i, sid in enumerate(shop_ids() + ["add"]):
            ry = y + i * SHOP_ROW
            new = sid == "add"
            name = "" if new else shop_name(sid)
            tb[sid] = Kit.with_tip(Kit.add_textbox(f.g, page_c["typed"].get(sid, name), x + 12, ry, bx - 20 - x,
                                                   numbers=False),
                                   ("Name of a new shop" if new else "Type a new name to rename this shop") +
                                   " (up to %d letters)" % NAME_MAX)
            if new:
                Kit.art_button(f.g, f.store, "add_shop", Kit.ART_PLAY, bx, ry - 2, "Add", "Add a shop with this name",
                               on_click=queue("add_shop"))
            else:
                Kit.art_button(f.g, f.store, "rm_%d" % sid, Kit.ART_CLOSE, bx, ry - 2, "Remove",
                               "Remove %s and its prices" % name, on_click=queue(("rm_shop", sid)))

    def page_table(w):
        """Table for the settings page: BOOK, SHOPPING LIST, SHOPS, OPTIONS, NUMBERS and HOTKEYS."""
        return (("BOOK", (("buttons", (("pick_book", Kit.ART_PLAY, "Pick book...", "Target the book the prices go in",
                                        queue("pick_book")),)),
                          ("note", "Book picked: open it to write" if st["book_serial"] else "No book picked yet"),
                          ("check", "book_open", "Write when opened", "Write the prices each time you open the book"),
                          ("check", "book_head", "Set title and date",
                           "Title the book Reagent Prices, with the last read's date as its author"))),
                ("SHOPPING LIST", tuple(("num", k, Kit.REAGENTS[k[5:]][0] + ":",
                                         "How many to keep in your backpack, bags included; 0 = not on the list", "",
                                         0, KEEP_MAX) for k in KEEPS), {"align": True}),
                ("SHOPS", (("custom", SHOP_ROW * (len(data["shops"]) + 1), draw_shops),)),
                ("OPTIONS", (("check", "say", "Journal line after each read",
                              "Say the shop and what it's cheapest for"),
                             ("check", "skip_old", "Skip old prices for the cheapest",
                              "Leave prices past Old after out of the cheapest and best stops"))),
                ("NUMBERS", (("num", "dist", "Shop distance:", "A vendor this close to a known shop belongs to it",
                              "tiles", 5, 60),
                             ("num", "old", "Old after:", "A price this old shows grey, with * in the book", "days",
                              1, 60)), {"align": True}), ("HOTKEYS", (("text", "hk", "Buy list:",
                              "Key for the Buy list button (F5, CTRL+Q, SHIFT+F2; blank = none)", {"tw": 100}),)))

    def on_change(old, new):
        """Settings change hook: a changed shopping list recounts the pack; a changed list, Old after or
        Skip old prices redraws and rewrites the book.
        """
        if any(old[k] != new[k] for k in KEEPS):
            want_count()
        if any(old[k] != new[k] for k in KEEPS + ("old", "skip_old")):
            st["bookver"] += 1
            queue.add("show")

    cfg = Kit.Page(settings, page_table, save_settings, on_change, final=True, adjust=read_names)

    def page_closed():
        """Settings page closed: save, apply typed shop names and re-register the hotkey."""
        cfg.closed()
        apply_names()
        page_c["tb"].clear()
        page_c["typed"].clear()
        rehook()

    def _start():
        """Module start: reset the state, load the data and settings, hook the key, build the window.

        The data text read while the module loaded is used when it is fresh; else the script thread
        loads it. Creates the lock that guards the log and history files and reads the saved window size.
        """
        import _thread
        st.update({"shutting": False, "docked": False, "queue": [], "loaded": False, "seen": None, "check_at": 0.0,
                   "aged_at": 0.0, "save_at": 0.0, "ask": None, "load_fails": 0, "book": None, "foreign": None,
                   "ok_books": set(), "picking": None, "minimized": wnd.start_min(), "jobs": [], "have": None,
                   "here": None, "hooked": None, "menu": False, "followed": None, "hk_at": 0.0, "pv": None,
                   "logq": [], "log_at": 0.0, "log_fails": 0, "log_lock": _thread.allocate_lock(), "histq": [],
                   "drops": [], "hist_at": 0.0, "hist_fails": 0, "obs_ok": False, "memo": {}, "miss": {},
                   "size": load_size(), "resize_at": 0.0, "drawn": None})
        data.update({"shops": {}, "vendors": {}, "reads": {}, "hist": {}, "dirty": {}, "marks": 0, "obs": {}})
        text, at = pre.pop("text", None), pre.pop("at", 0.0)
        if text is not None and time.time() - at < PRE_KEEP:
            load_data(text)
        load_settings()
        rehook()
        want_count()
        build_window()
        wnd.dock(fit=True, min=min_size)

    def _tick():
        """Client tick: run queued actions, watch the shop question, then check for a buy list and the book.

        Reading the buy list and writing the book are done every CHECK_EVERY seconds, the window text
        ages every AGE_EVERY seconds, and a window resize is applied once it has settled.
        """
        q = st["queue"]
        while q:
            action = q.pop(0)
            if wnd.action(action):
                continue
            if type(action) is tuple:
                ACTIONS[action[0]](*action[1:])
            else:
                ACTIONS[action]()
        now = time.time()
        watch_ask()
        if st["loaded"] and now >= st["check_at"]:
            st["check_at"] = now + CHECK_EVERY
            check_shop(now)
            book_tick(now)
        if now >= st["aged_at"]:
            st["aged_at"] = now + AGE_EVERY
            refresh()
        if st["resize_at"] and now - st["resize_at"] >= SETTLE and not (SNAP.drag or SNAP.pressed() is True):
            st["resize_at"] = 0.0
            apply_resize()

    def _thread_tick():
        """Script thread tick: run queued jobs (pack count, buy list menu), write the log and history files
        and save or load the data file.

        Slow file and context menu work lives here so the client tick stays light. Stops when the
        module is shutting down.
        """
        jobs = st["jobs"]
        while jobs and not st["shutting"]:
            job = jobs.pop(0)
            JOBS[job[0]](*job[1:])
        now = time.time()
        if st["logq"] and now >= st["log_at"]:
            flush_log()
        if hist_due(now):
            flush_hist()
        if now < st["save_at"]:
            return
        if not st["loaded"]:
            load_data()
        elif data["dirty"]:
            save_data()

    def _thread_wanted():
        """True when the script thread has work: jobs, log or history lines waiting, or data to load or save."""
        now = time.time()
        return bool(st["jobs"]) or bool(st["logq"]) and now >= st["log_at"] or hist_due(now) or (
            not st["loaded"] or bool(data["dirty"])) and now >= st["save_at"]

    def _stop():
        """Module stop: save settings and data, flush the log and history, release the hotkey and Follow,
        close the window.
        """
        st["shutting"] = True
        save_settings()
        if st["hooked"]:
            HOST.hotkey_off(st["hooked"], TITLE)
            st["hooked"] = None
        if st["followed"] is not None and Follow.current() == st["followed"]:
            Follow.stop(TITLE)
        st["followed"] = None
        if st["loaded"] and data["dirty"]:
            save_data()
        if st["logq"]:
            flush_log()
        if st["loaded"] and (st["histq"] or st["drops"]):
            flush_hist()
        cleanup.close()

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": page_closed,
            "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("prices", "Reagent Prices", "Reagent prices and a price book", _module_prices, 0.25, category="The world")
