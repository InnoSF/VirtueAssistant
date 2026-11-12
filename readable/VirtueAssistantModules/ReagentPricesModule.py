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
    vendors, reads and price history), win (window parts) and bridge (cached client reflection).
    The returned dict has start, tick, stop, the settings page callbacks (config_height,
    build_config, poll_config, config_closed) and thread_tick / thread_wanted for the script thread.
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
    STOPS_H = 30 + (STOPS + 1) * ROW_H + 6
    LIMITS.update((k, (0, KEEP_MAX)) for k in KEEPS)
    GRID_MAX = 30
    GRID_NAME = "Upper W Britain"
    GRID_CELL = "99^ (999)"
    SHOP_ROW = 28
    GRID_TITLE = "ALL SHOPS  (price, stock; ^ up, v down)"
    VIEW_TIP = "Switch between the cheapest list and every shop"
    LOG_FILE = "ReagentPrices_log.csv"
    LOG_MAX = 5000
    LOG_HEAD = "time,shop,reagent,price,stock"
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
          "pv": None, "logq": [], "log_at": 0.0, "log_fails": 0}
    win = {"g": None, "c": {}, "store": ({}, {})}
    data = {"shops": {}, "vendors": {}, "reads": {}, "hist": {}, "dirty": {}, "marks": 0}
    bridge = {}
    widths = {}
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
        V vendor (serial in hex, shop id, map x y), R read (serial, time, CODE:price:stock list) and
        H history (shop id, reagent code, list of time:price:stock). Anything after the known fields is
        kept as tail so a longer line survives a round trip. Lines that do not parse are skipped.
        """
        out = {"shops": {}, "vendors": {}, "reads": {}, "hist": {}}
        for line in (text or "").split("\n"):
            f = line.rstrip("\r").split("|")
            try:
                if f[0] == "P":
                    out["shops"][int(f[1])] = {"name": f[2], "order": int(f[3]), "spot": spot_of(f[4:7]), "tail": f[7:]}
                elif f[0] == "V":
                    out["vendors"][int(f[1], 16)] = {"shop": int(f[2]), "spot": spot_of(f[3:6]), "tail": f[6:]}
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
        return out

    def line_of(key):
        """Build the data file line for a key such as P|3, V|1A2B or H|3|SS from the model.

        Returns None when the entry no longer exists (the caller then drops the line).
        """
        f = key.split("|")
        kind = f[0]
        if kind == "P":
            e = data["shops"].get(int(f[1]))
            body = e and [e["name"], str(e["order"])] + spot_text(e["spot"])
        elif kind == "V":
            e = data["vendors"].get(int(f[1], 16))
            body = e and [str(e["shop"])] + spot_text(e["spot"])
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

    def shop_prices(now=None):
        """Best price per shop: {shop id: {code: (price, stock, read time)}}.

        When two vendors belong to one shop the lower price of each reagent counts. With now given and
        Skip old prices on, reads older than Old after days are left out.
        """
        out = {}
        lim = settings["old"] * DAY if now is not None and settings["skip_old"] else None
        for serial, rd in data["reads"].items():
            sid = shop_of(serial)
            if sid is None or lim is not None and now - rd["t"] > lim:
                continue
            sp = out.setdefault(sid, {})
            for code, (price, stock) in rd["p"].items():
                if code not in sp or price < sp[code][0]:
                    sp[code] = (price, stock, rd["t"])
        return out

    def cheapest(prices):
        """Cheapest shop per reagent: {code: (shop id, (price, stock, time))}.

        A tie goes to the shop that comes first in the shop order.
        """
        shops = data["shops"]
        best = {}
        for sid, sp in prices.items():
            for code, row in sp.items():
                old = best.get(code)
                if old is None or (row[0], shops[sid]["order"]) < (old[1][0], shops[old[0]]["order"]):
                    best[code] = (sid, row)
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

    def ranking(prices):
        """Rank the shops by what the shopping list costs there.

        How many to buy is the keep count minus what the backpack holds (from the pack count); with no
        list it is 1 of each reagent. Returns (want, whether a list is set, reagents still needed, the
        best STOPS shops). A ranked entry is (missing + short count, total cost, shop order, shop id,
        missing codes, short codes); fewer gaps come first, then the lower cost. Cost counts only the
        stock a shop really has.
        """
        keep = dict((k, settings["keep_" + k]) for k in ORDER if settings["keep_" + k] > 0)
        have = st["have"] or {}
        want = dict((k, max(0, n - have.get(k, 0))) for k, n in keep.items()) if keep else dict((k, 1) for k in ORDER)
        need = [k for k in ORDER if want.get(k)]
        ranked = []
        for sid, sp in (prices.items() if need else ()):
            outs = [k for k in need if k not in sp]
            shorts = [k for k in need if k in sp and sp[k][1] < want[k]]
            total = sum(sp[k][0] * min(want[k], sp[k][1]) for k in need if k in sp)
            ranked.append((len(outs) + len(shorts), total, data["shops"][sid]["order"], sid, outs, shorts))
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

        When it differs from the one stored at build time the window is rebuilt; otherwise only the
        texts are refreshed.
        """
        a = st["ask"]
        return (a and a["mode"], bool(a and a["new"]), last_read() is not None, st["foreign"] is not None,
                any(settings[k] for k in KEEPS), settings["grid"], len(data["shops"]))

    def extra_h():
        """Height of the optional parts: the Overwrite bar, the "Which shop?" question (taller while a new
        name is typed) and the best stops block (not in the grid view).
        """
        a = st["ask"]
        over = Kit.GAP + OVER_H if st["foreign"] is not None else 0
        return (over + ((Kit.GAP + ASK_H + (NAME_H if a["new"] else 0)) if a else 0) +
                (0 if settings["grid"] else Kit.GAP + STOPS_H))

    def fixed_h(n=1):
        """Height of the window without its resizable rows; n is the number of grid rows."""
        body = ROW_H + n * ROW_H if settings["grid"] else len(ORDER) * ROW_H
        return 2 * Kit.MARGIN + 30 + Kit.GAP + 30 + body + 6 + Kit.GAP + LINE_H + extra_h()

    def grid_cols():
        """Pixel widths of the shop name column and of a price cell in the grid."""
        return Kit.text_w(GRID_NAME) + 8, Kit.text_w(GRID_CELL) + 8

    def min_size():
        """Smallest (width, height) the window can have in the current view."""
        if not settings["grid"]:
            return W, fixed_h()
        nw, cw = grid_cols()
        return max(W, 2 * Kit.MARGIN + 16 + nw + len(ORDER) * cw), fixed_h(1)

    def trend(sid, code, row):
        """Price trend of one grid cell: "^" if it rose, "v" if it fell, empty if equal or no earlier read.

        Compares with the newest history row older than this read.
        """
        h = data["hist"].get((sid, code))
        prev = [r for r in h["rows"] if r[0] < row[2]] if h else []
        if not prev:
            return ""
        return "^" if row[0] > prev[-1][1] else "v" if row[0] < prev[-1][1] else ""

    def draw_ask(g, store, c, M, y, IW, a):
        """Draw the "Which shop?" section: the drop-down of shops (plus New shop), the name box when New
        shop is picked and the Skip / Cancel and OK buttons.

        The first button reads Skip for a pending read (the read is dropped) and Cancel when only
        changing the shop of the last vendor.
        """
        Kit.add_section(g, M, y, IW, ASK_H + (NAME_H if a["new"] else 0))
        x = M + IW - 8
        cancel = ("Skip", "Drop this read") if a["mode"] == "read" else ("Cancel", "Keep this vendor's shop")
        for key, art, cap, tip in (("ask_skip", Kit.ART_CLOSE) + cancel,
                                   ("ask_ok", Kit.ART_OK, "OK", "Link this vendor to the picked shop")):
            x -= 35 + Kit.text_w(cap)
            Kit.art_button(g, store, key, art, x, y + 6, cap, tip, on_click=queue(key))
            x -= 10
        Kit.add_label(g, "Which shop?", M + 8, y + 10)
        dx = M + 16 + Kit.text_w("Which shop?")
        ids = c["ask_ids"] = shop_ids()
        names = [shop_name(sid) for sid in ids] + [NEW_SHOP]
        if a["new"]:
            Kit.add_label(g, "Name:", M + 8, y + ASK_H + 2)
            tb = Kit.add_textbox(g, "", dx, y + ASK_H, x - dx, numbers=False)
            c["ask_name"] = Kit.with_tip(tb, "Name of the new shop (up to %d letters)" % NAME_MAX)
        dd = G.CreateDropDown(x - dx, names, max(0, min(a["pick"], len(ids))))
        dd.SetPos(dx, y + 6)
        g.Add(dd)
        c["ask_dd"] = Kit.with_tip(dd, "Shop this vendor is in")

    def draw_over(g, store, M, y, IW):
        """Draw the Overwrite bar shown when the picked book holds other writing."""
        Kit.add_section(g, M, y, IW, OVER_H)
        x = M + IW - 8 - 35 - Kit.text_w("Overwrite")
        Kit.art_button(g, store, "overwrite", Kit.ART_OK, x, y + 6, "Overwrite",
                       "Write the prices over this book's text (this book only)", on_click=queue("overwrite"))
        Kit.add_label(g, Kit.fit("The book holds other writing", x - M - 18), M + 8, y + 10, Kit.HUE_BAD)

    def draw_grid(g, c, M, y, IW, sh, n):
        """Draw the grid section: shop name column, one column per reagent and n empty rows to fill."""
        Kit.add_section(g, M, y, IW, sh, GRID_TITLE)
        nw, cw = grid_cols()
        cw = max(cw, (IW - 16 - nw) // len(ORDER))
        x0 = M + 8 + nw
        c["name_w"] = nw - 8
        c["cell_w"] = cw - 4
        for i, code in enumerate(ORDER):
            Kit.add_label(g, code, x0 + i * cw, y + 30, Kit.HUE_TITLE)
        c["grid"] = [(Kit.add_label(g, "", M + 8, y + 30 + (j + 1) * ROW_H),
                      [Kit.add_label(g, "", x0 + i * cw, y + 30 + (j + 1) * ROW_H) for i in range(len(ORDER))])
                     for j in range(n)]

    def build_window():
        """Build the whole window from the current state, then refresh it.

        The window takes a slot in its zone when it has one (rows then follow the zone's height) and
        caps the grid at GRID_MAX shops. Layout: title row with the Buy list and View buttons, the
        cheapest list or the grid, the status line with Change, the "Which shop?" question, best stops
        and the Overwrite bar. Client tick.
        """
        mw, mh = min_size()
        z = wnd.zone_slot(mw, mh)
        grid = settings["grid"]
        n = 0
        if grid:
            own = max(1, min(GRID_MAX, len(data["shops"])))
            n = min(GRID_MAX, wnd.rows(ROW_H, fixed_h(0), own)) if z else own
            mh = fixed_h(n)
        w, h = z if z else (mw, mh)
        g, store, c = wnd.begin(w, h)
        c["shape"] = shape()
        if not st["minimized"]:
            # The Buy list button uses press_buy so that Alt+click can start Follow (R5) instead of opening
            # the list.
            wnd.frame(g, extra=[("buy", Kit.ART_PLAY, "Buy list", BUY_TIP, press_buy),
                                ("view", Kit.ART_PAGE, "View: grid" if grid else "View: cheapest", VIEW_TIP,
                                 queue("view"))])
            M = Kit.MARGIN
            IW = w - 2 * M
            y = M + 30 + Kit.GAP
            a = st["ask"]
            listed = c["shape"][4]
            tail = Kit.GAP + LINE_H + extra_h()
            if grid:
                draw_grid(g, c, M, y, IW, h - M - tail - y, n)
            else:
                Kit.add_section(g, M, y, IW, h - M - tail - y, "CHEAPEST")
                nx = M + 34
                px = nx + max(Kit.text_w(Kit.REAGENTS[k][0]) for k in ORDER) + 10
                bx = px + Kit.text_w("9999") + 10
                sx = bx + (Kit.text_w("buy 9999") + 10 if listed else 0)
                ax = M + IW - 8 - Kit.text_w("59 min ago")
                c["shop_w"] = ax - 8 - sx
                c["rows"] = []
                for i, code in enumerate(ORDER):
                    ry = y + 30 + i * ROW_H
                    name, graphic = Kit.REAGENTS[code]
                    pic = G.CreateGumpItemPic(graphic, 20, 20)
                    pic.SetPos(M + 8, ry - 2)
                    Kit.inert(pic)
                    g.Add(pic)
                    Kit.add_label(g, name, nx, ry)
                    # The buy column exists only when a shopping list is set.
                    c["rows"].append((code, Kit.add_label(g, "", px, ry), Kit.add_label(g, "", sx, ry),
                                      Kit.add_label(g, "", ax, ry, Kit.HUE_INFO),
                                      Kit.add_label(g, "", bx, ry, Kit.HUE_INFO) if listed else None))
            ys = h - M - tail + Kit.GAP
            Kit.add_section(g, M, ys, IW, LINE_H)
            c["line_w"] = IW - 16
            if a is None and last_read() is not None:
                bx = M + IW - 8 - 35 - Kit.text_w("Change")
                c["line_w"] = bx - 6 - M - 8
                Kit.art_button(g, store, "change", Kit.ART_PAGE, bx, ys + 4, "Change",
                               "Pick another shop for the last vendor read", on_click=queue("change"))
            c["line"] = Kit.add_label(g, "", M + 8, ys + 9, Kit.HUE_INFO)
            ys += LINE_H + Kit.GAP
            if a is not None:
                draw_ask(g, store, c, M, ys, IW, a)
                ys += ASK_H + (NAME_H if a["new"] else 0) + Kit.GAP
            if not grid:
                Kit.add_section(g, M, ys, IW, STOPS_H, "BEST STOPS")
                c["stops_w"] = IW - 16
                c["stops"] = [Kit.add_label(g, "", M + 8, ys + 30 + i * ROW_H, Kit.HUE_INFO) for i in range(STOPS + 1)]
                ys += STOPS_H + Kit.GAP
            if st["foreign"] is not None:
                draw_over(g, store, M, ys, IW)
        wnd.end(g)
        refresh()

    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=MINI, icon=TRAY_ICON, cleanup=cleanup)

    def fill_rows(c, prices, pool, hv, want, now):
        """Fill the cheapest list rows with text and colours.

        Without an open buy list each row shows the cheapest price, its shop and its age (grey when
        older than Old after). With one open, each row shows this vendor's price (green when it ties the
        best elsewhere or beats it) and the best other shop. hv is the here_view result, want how many
        to buy.
        """
        best = cheapest(dict((s, p) for s, p in pool.items() if s != hv[0]) if hv else pool)
        every = cheapest(prices)
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
                Kit.set_text(ls, Kit.fit("best %d %s" % (hit[1][0], shop_name(hit[0])) if hit else "no other shop",
                                         c["shop_w"]), Kit.HUE_INFO)
                Kit.set_text(la, Kit.ago(now - hit[1][2], AGE) if hit else "", Kit.HUE_INFO)
                continue
            if hit is None:
                Kit.set_text(lp, "-", Kit.HUE_INFO)
                Kit.set_text(ls, "Only old prices" if code in every else "No price yet", Kit.HUE_INFO)
                Kit.set_text(la, "")
                continue
            sid, row = hit
            hue = Kit.HUE_INFO if now - row[2] > olds else Kit.HUE_TEXT
            Kit.set_text(lp, str(row[0]), hue)
            Kit.set_text(ls, Kit.fit(shop_name(sid), c["shop_w"]), hue)
            Kit.set_text(la, Kit.ago(now - row[2], AGE), Kit.HUE_INFO)

    def fill_grid(c, prices, pool, now):
        """Fill the grid cells: price, trend and stock per shop and reagent.

        The cheapest of each column is green, an old price grey, a dash means not listed. When there are
        more shops than rows the last row says how many are left out.
        """
        best = cheapest(pool)
        ids = shop_ids()
        rows = c["grid"]
        more = len(ids) - len(rows) + 1
        olds = settings["old"] * DAY
        for j, (ln, cells) in enumerate(rows):
            sid = ids[j] if j < len(ids) and (more <= 1 or j < len(rows) - 1) else None
            sp = prices.get(sid)
            if sid is None:
                Kit.set_text(ln, "+%d more shops" % more if j < len(ids) else "", Kit.HUE_INFO)
            else:
                Kit.set_text(ln, Kit.fit(shop_name(sid), c["name_w"]), Kit.HUE_INFO if sp is None else Kit.HUE_TEXT)
            for code, lbl in zip(ORDER, cells):
                row = sp.get(code) if sp else None
                if row is None:
                    Kit.set_text(lbl, "-" if sp is not None else "", Kit.HUE_INFO)
                    continue
                old = now - row[2] > olds
                low = code in best and row[0] <= best[code][1][0]
                Kit.set_text(lbl, Kit.fit("%d%s (%d)" % (row[0], trend(sid, code, row), row[1]), c["cell_w"]),
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
            text = "read %s %s" % (shop_name(shop_of(last)), Kit.ago(now - data["reads"][last]["t"], AGE))
        if st["foreign"] is not None:
            text = "book holds other writing; Restore to overwrite"
        if st["ask"] is not None:
            text = "which shop? Restore to pick"
        if "status" in c:
            Kit.set_text(c["status"], "%s: %s" % (TITLE, text))
        elif "line" in c:
            prices = shop_prices()
            pool = shop_prices(now)
            hv = here_view()
            want, listed, need, ranked = ranking(pool)
            if "grid" in c:
                fill_grid(c, prices, pool, now)
            else:
                fill_rows(c, prices, pool, hv, want, now)
            if st["ask"] is not None:
                line = "Which shop is this vendor in? Pick it below"
            elif last is None:
                line = "No reads yet: open a reagent vendor's buy list"
            else:
                line = "Last %s" % text
            Kit.set_text(c["line"], Kit.fit(line, c["line_w"]), Kit.HUE_INFO)
            if "stops" not in c:
                return
            rows = [cost_line(pool, hv, want, listed, need)] + [
                "%d %s %s%s" % (i + 1, shop_name(r[3]), commas(r[1]), ": " + lack_text(r) if r[0] else "")
                for i, r in enumerate(ranked)]
            if need and not ranked:
                rows.append("No prices yet")
            for i, lbl in enumerate(c["stops"]):
                r = ranked[i - 1] if 0 < i <= len(ranked) else None
                Kit.set_text(lbl, Kit.fit(rows[i] if i < len(rows) else "", c["stops_w"]),
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

    def link(serial, sid, spot, picked=False):
        """Link a vendor to a shop and remember where the vendor stands.

        When the player picked the shop it also remembers that spot for the shop, so later vendors
        close to it are placed without asking.
        """
        old = data["vendors"].get(serial) or {"spot": None, "tail": []}
        data["vendors"][serial] = {"shop": sid, "spot": spot or old["spot"], "tail": old["tail"]}
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

        Links the vendor, replaces its read, adds history rows, queues the log lines and, when the
        journal line is on, says which reagents this shop is cheapest for. Raises the book version so
        the book is written again. picked is True when the player chose the shop.
        """
        serial, t = pend["serial"], pend["t"]
        link(serial, sid, pend["spot"], picked)
        old = data["reads"].get(serial) or {"tail": []}
        data["reads"][serial] = {"t": t, "p": dict(pend["p"]), "tail": old["tail"]}
        mark("R|%X" % serial)
        for code, (price, stock) in pend["p"].items():
            add_hist(sid, code, (t, price, stock))
        log_read(pend, sid)
        if settings["say"]:
            pool = shop_prices(time.time())
            best = cheapest(pool)
            here = pool.get(sid, {})
            won = [k for k in ORDER if k in here and here[k][0] == best[k][1][0]]
            say("%s read%s." % (shop_name(sid), "; cheapest for " + ", ".join(won) if won else ""), Kit.HUE_GOOD)
        st["bookver"] += 1
        show()

    def log_read(pend, sid):
        """Queue the csv log lines of a read, one per reagent (price empty and stock 0 when not listed).

        Names with a comma or quote are quoted. The queue keeps at most LOG_MAX lines.
        """
        name = shop_name(sid)
        when = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pend["t"]))
        q = st["logq"]
        if "," in name or '"' in name:
            name = '"%s"' % name.replace('"', '""')
        q.extend("%s,%s,%s,%s,%d" % (when, name, Kit.REAGENTS[k][0], pend["p"][k][0] if k in pend["p"] else "",
                                     pend["p"][k][1] if k in pend["p"] else 0) for k in ORDER)
        if len(q) > LOG_MAX:
            del q[:-LOG_MAX]

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

        A read identical to the stored one within REREAD_GAP seconds is ignored. The vendor's spot is
        taken from the mobile. A vendor with a known shop is stored at once; else the nearest known shop
        within Shop distance; else the window asks "Which shop?".
        """
        old = data["reads"].get(serial)
        if old is not None and now - old["t"] < REREAD_GAP and old["p"] == got:
            return
        mob = API.FindMobile(serial)
        spot = (int(API.GetMap()), int(mob.X), int(mob.Y)) if mob else None
        pend = {"serial": serial, "t": int(now), "p": got, "spot": spot}
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
        filled in yet is waited for, and a vendor with no reagents and no shop is ignored. While the
        same list stays open a change of the backpack asks for a new count of the pack. While a shop
        question for a read is open, nothing else is read.
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
            show()
        elif st["here"] is not None:
            st["here"] = None
            show()

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
        stops with what each lacks. Pages 3 to 18: one shop each with when it was read and its prices
        in pairs (full names, short codes when too wide). Unused lines and pages are blank.
        """
        prices = shop_prices()
        pool = shop_prices(now)
        best = cheapest(pool)
        every = cheapest(prices)
        old = settings["old"] * DAY
        seen = {}
        for serial, rd in data["reads"].items():
            sid = shop_of(serial)
            if sid is not None:
                seen[sid] = max(seen.get(sid, 0), rd["t"])

        def cost(row):
            """Price text for a row, with an asterisk when its read is older than Old after."""
            return "%d%s" % (row[0], "*" if now - row[2] > old else "")

        pages = [[fit_line("%s %s " % (code, cost(best[code][1])), shop_name(best[code][0])) if code in best
                  else "%s - (old)" % code if code in every else "%s - (no read)" % code for code in ORDER]]
        want, listed, need, ranked = ranking(pool)
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

        Pending typed names are applied first. A shop question for the removed shop's vendor is closed.
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
        for serial in [v for v, e in data["vendors"].items() if e["shop"] == sid]:
            del data["vendors"][serial]
            mark("V|%X" % serial)
            if data["reads"].pop(serial, None) is not None:
                mark("R|%X" % serial)
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
        loads it. Creates the lock that guards the log file.
        """
        import _thread
        st.update({"shutting": False, "docked": False, "queue": [], "loaded": False, "seen": None, "check_at": 0.0,
                   "aged_at": 0.0, "save_at": 0.0, "ask": None, "load_fails": 0, "book": None, "foreign": None,
                   "ok_books": set(), "picking": None, "minimized": wnd.start_min(), "jobs": [], "have": None,
                   "here": None, "hooked": None, "menu": False, "followed": None, "hk_at": 0.0, "pv": None,
                   "logq": [], "log_at": 0.0, "log_fails": 0, "log_lock": _thread.allocate_lock()})
        data.update({"shops": {}, "vendors": {}, "reads": {}, "hist": {}, "dirty": {}, "marks": 0})
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
        ages every AGE_EVERY seconds.
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

    def _thread_tick():
        """Script thread tick: run queued jobs (pack count, buy list menu), write the log and save or
        load the data file.

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
        if now < st["save_at"]:
            return
        if not st["loaded"]:
            load_data()
        elif data["dirty"]:
            save_data()

    def _thread_wanted():
        """True when the script thread has work: jobs, log lines waiting or data to load or save."""
        now = time.time()
        return bool(st["jobs"]) or bool(st["logq"]) and now >= st["log_at"] or (
            not st["loaded"] or bool(data["dirty"])) and now >= st["save_at"]

    def _stop():
        """Module stop: save settings and data, flush the log, release the hotkey and Follow, close
        the window.
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
        cleanup.close()

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": page_closed,
            "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("prices", "Reagent Prices", "Reagent prices and a price book", _module_prices, 0.25, category="The world")
