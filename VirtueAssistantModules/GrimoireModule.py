def _module_grimoire():
    KEY = "grimoire"; TITLE = "Grimoire"; SPELLBOOK_GRAPHICS = [0x0EFA]
    TRAVEL_TYPES = {"charge": 0, "recall": 3, "gate":   4, "sacred": 5,}; DEFAULT_TRAVEL = "recall"
    TRAVEL_METHODS = ("recall", "gate", "charge", "recall_scroll", "gate_scroll", "sacred")
    TRAVEL_SPELL = {"recall": "Recall", "gate": "Gate Travel", "sacred": "Sacred Journey"}; LOW_CHARGES = 3
    SEARCH_MAX = 40; FAVS_MAX = SEARCH_MAX; SEARCH_EVERY = 0.15; MANA_EVERY = 0.5
    STAR_ON, STAR_OFF = "#F0C040", "#6A6A6A"; TAB_FAVS = 1; RECALL_SCROLL = 0x1F4C; GATE_SCROLL   = 0x1F60
    SCROLL_CAST_TIMEOUT = 12; RUNE_CAST_CLAIM = 5
    CAST_FAIL_TEXTS = ("fizzles", "not yet recovered", "more reagents",
                       "insufficient mana", "concentration is disturbed")
    PREBUILD_EVERY     = 0.4; CAST_CLAIM         = 5.0
    NO_TARGET_SPELLS = frozenset("Reactive Armor|Protection|Magic Reflection|Incognito|Create Food|Earthquake|"
                                 "Summon Creature|Air Elemental|Earth Elemental|Fire Elemental|Water Elemental|"
                                 "Summon Daemon".split("|"))
    CAST_DEFER         = 1.5; CAST_HOLD          = 4.0; DEFAULT_W, DEFAULT_H = 920, 950; MIN_W, MIN_H         = 700, 220
    SIDE_W               = 160; SCALE_MIN, SCALE_MAX = 60, 150; TITLE_H              = 54; LINK_CMD = "Grimoire_cmd"
    LINK_STATE = "Grimoire_state"; DEFAULT_OPACITY      = 95; SPELL_ICON           = 66; ART_FRAME    = Kit.WINDOW_BG
    GEM          = Kit.ART_PLAY[0]; GEM_ON       = Kit.ART_PLAY[1]; CIRCLE_ART   = 0x08B1; COL_HEAD    = "#E8C84A"
    COL_TEXT    = "#ECECEC"; COL_DIM     = "#9C9C9C"; COL_MUTED   = "#6E6E6E"; COL_EMPTY   = "#E04848"
    COL_ROW     = "#C8B070"; ROW_A = 0.05
    TEXT_HUES = {COL_TEXT: Kit.HUE_TEXT, COL_HEAD: Kit.HUE_TITLE, COL_DIM: Kit.HUE_INFO,
                 COL_MUTED: Kit.HUE_INFO, COL_EMPTY: Kit.HUE_BAD}
    gump = None
    SPELL_DESC = ("Lowers the target's Dexterity for a time.|Conjures a random piece of food into your pack.|Lowers "
                  "the target's Intelligence for a time.|Restores a small amount of the target's health.|Strikes the "
                  "target with a minor bolt of magic.|Lets the target see clearly in darkness.|Wards you with armor "
                  "that soaks up melee damage.|Lowers the target's Strength for a time.|Raises the target's Dexterity "
                  "for a time.|Raises the target's Intelligence for a time.|Attempts to neutralize poison in the "
                  "target.|Damages the target; strongest at close range.|Traps a container to explode when opened.|"
                  "Disarms a magical trap on a container.|Temporarily raises your armor rating.|Raises the target's "
                  "Strength for a time.|Raises the target's Strength, Dexterity and Intelligence.|Hurls a ball of fire "
                  "at the target.|Magically seals a container shut.|Poisons the target.|Uses or opens an object from a "
                  "distance.|Instantly moves you to a visible location.|Opens a magically locked container.|Raises a "
                  "temporary wall of stone.|Cures poison in the target and those nearby.|Raises the armor rating of "
                  "everyone around you.|Lowers the target's Strength, Dexterity and Intelligence.|Creates a wall of "
                  "flame that burns those who cross it.|Restores a large amount of the target's health.|Calls a bolt "
                  "of lightning down on the target.|Drains mana from the target.|Teleports you to the location marked "
                  "on a rune.|Summons whirling blades that attack nearby creatures.|Destroys a magical field.|"
                  "Disguises your appearance and name for a time.|Turns harmful spells back upon their caster.|Damages "
                  "the target based on your superior intellect.|Freezes the target in place for a time.|Creates a wall "
                  "of poisonous gas.|Summons a random creature to fight for you.|Banishes a summoned creature.|Strikes "
                  "the target with a powerful bolt of energy.|Engulfs the target in a fiery explosion.|Makes the "
                  "target invisible for a time.|Marks a recall rune with your current location.|Curses everyone in an "
                  "area.|Creates a wall that paralyzes those who touch it.|Reveals hidden creatures and players "
                  "nearby.|Lightning strikes everyone around the target.|Creates an impassable wall of energy.|Engulfs "
                  "the target in a column of fire.|Opens a moongate to a rune's location that others can use.|Steals "
                  "the target's mana and gives it to you.|Banishes all summoned creatures in an area.|Rains fire on "
                  "everyone around the target.|Transforms you into another creature.|Shakes the ground, damaging "
                  "everyone around you.|Summons a vortex of energy that attacks your foes.|Brings a ghost back to "
                  "life.|Summons an air elemental to serve you.|Summons a daemon to serve you.|Summons an earth "
                  "elemental to serve you.|Summons a fire elemental to serve you.|Summons a water elemental to serve "
                  "you.").split("|")
    REAGENT_FIX = {"Feeblemind": "NS GI", "Cunning": "NS MR", "Resurrection": "BM GI GA"}
    CIRCLES = [(o + " Circle", [(n, SPELL_DESC[c * 8 + i], REAGENT_FIX.get(n, r))
                                for i, (n, r) in enumerate(Kit.MAGERY[c * 8:c * 8 + 8])])
               for c, o in enumerate(("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"))]
    REAGENTS = dict(Kit.REAGENTS, SS=("Spider's Silk", 0x0F8D))
    REAGENT_ORDER = ["BP", "BM", "GA", "GI", "MR", "NS", "SA", "SS"]; RUNE_HEAD_SIZE  = 16; RUNE_TITLE_SIZE = 24
    RUNE_METHODS = [("charge", "Charge", "Recall using one of the book's charges"),
                    ("recall", "Recall", "Cast Recall on this rune"), ("gate", "Gate", "Cast Gate Travel to this rune"),
                    ("recall_scroll", "Recall scroll", "Read a Recall scroll on this rune"),
                    ("gate_scroll", "Gate scroll", "Read a Gate Travel scroll on this rune")]
    REG_SLOT = 86; REG_PIC  = 60; st = {"minimized": False}; spellbook_serial = 0; known_spells = None; runebooks = []
    rune_cache = {}; book_charges = {}; bg_reads = []; bg = {"hold": 0.0}; gump_id = 0x554B87F3
    lists = {"ver": 0, "dest_ver": -1, "dests": []}
    favs = {"list": [], "keys": set(), "last": None, "owner": None, "save": False, "save_last": False}; fav_ui = {}
    charge_seen = {}; charge_news = []
    def new_layer(hidden=False):
        return {"ctrls": [], "tops": [], "counts": [], "spells": [], "stars": {}, "hidden": hidden}
    frame = new_layer(); pages = {}; tgt = frame; row_bgs = {}; tab_marks = {}; tab_parts = {}
    click_state = {"key": None, "t": 0.0, "selected": None}; say = Kit.sayer(TITLE)
    def norm(s): s = re.sub(r"[^a-z]", "", (s or "").lower()); return s.replace("summon", "") if "elemental" in s else s
    def items_in_pack(fresh=False): return HOST.pack_items(deep=True, max_age=0.0 if fresh else 0.5)
    def held_items():
        out = [API.FindLayer("OneHanded"), API.FindLayer("TwoHanded")]
        out += list(API.ItemsInContainer(API.Player.Serial) or ()); seen, items, pack = set(), [], API.Backpack
        for it in out:
            if it and it.Serial not in seen and it.Serial != pack: seen.add(it.Serial); items.append(it)
        return items
    def load_rb_types():
        types = set()
        for part in Kit.get_var("Grimoire_RunebookTypes").split(","):
            try: g, h = part.split(":"); types.add((int(g, 16), int(h, 16)))
            except ValueError: pass
        return types
    rb_types = load_rb_types(); rb_seen = set()
    def is_runebook(it): return is_runebook_v(it.Graphic, it.Hue, it.Name)
    def is_runebook_v(g, h, name):
        if (g, h) in rb_types: return True
        name = (name or "").lower()
        if "rune" in name and "book" in name: return True
        if "spellbook" in name: return False
        if g in SPELLBOOK_GRAPHICS and h == 0x0461: return True
        return g == 0x22C5
    def is_spellbook(it): return it.Graphic in SPELLBOOK_GRAPHICS and not is_runebook(it)
    def find_spellbook():
        books = [it for it in held_items() + items_in_pack() if is_spellbook(it)]
        for b in books:
            if list(API.GetSpellsInSpellbook(b.Serial) or ()): return b.Serial
        return books[0].Serial if books else 0
    def close_spellbook_window(serial):
        closed = False
        try:
            for g in list(Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))):
                try:
                    if (g.LocalSerial == serial and "Spellbook" in g.GetType().Name and not g.IsDisposed):
                        g.Dispose(); closed = True
                except Exception: pass
        except Exception: pass
        return closed
    def spells_key(): return "spells_%08X" % int(API.Player.Serial)
    def load_known_spells(force=False):
        if not spellbook_serial: return None
        names = list(API.GetSpellsInSpellbook(spellbook_serial) or [])
        if not names and not force:
            cached = set(n for n in load_value(spells_key()).split(",") if n)
            if cached: return cached
        if not names:
            API.UseObject(spellbook_serial); deadline = time.time() + 2.0
            while time.time() < deadline and HOST.idle(0.05):
                names = list(API.GetSpellsInSpellbook(spellbook_serial) or [])
                if names: break
            deadline = time.time() + 1.0
            while time.time() < deadline and not HOST.aborting():
                if Kit.on_client(lambda: close_spellbook_window(spellbook_serial)): break
                HOST.idle(0.05)
        if not names: return None
        known = set(norm(n) for n in names); save_value(spells_key(), ",".join(sorted(known))); return known
    SUPPLY_GRAPHICS = set([g for _, g in REAGENTS.values()] + [RECALL_SCROLL, GATE_SCROLL])
    def supply_counts():
        items = items_in_pack(); memo = None
        if HOST.in_hop:
            memo = (HOST.pass_id, len(items))
            if _supply["key"] == memo: return dict(_supply["totals"])
        totals = dict((g, 0) for g in SUPPLY_GRAPHICS)
        for it in items:
            g = it.Graphic
            if g in totals: totals[g] += max(1, it.Amount or 0)
        if memo is not None: _supply.update({"key": memo, "totals": dict(totals)})
        return totals
    _supply = {"key": None, "totals": None}
    def count_text(n): return "{:,}".format(n)
    def count_entry(graphic, lbl, n, owned=True):
        return [graphic, lbl, count_text(n), TEXT_HUES[COL_TEXT if owned else COL_MUTED],
                TEXT_HUES[COL_EMPTY if owned else COL_MUTED]]
    def scroll_flags(totals): return (totals.get(RECALL_SCROLL, 0) > 0, totals.get(GATE_SCROLL, 0) > 0)
    def refresh_counts():
        if not frame["counts"] and not any(pg["counts"] for pg in pages.values()): return
        totals = supply_counts(); changed = totals != loop["totals"]; loop["totals"] = totals
        entries = (frame["counts"] + [e for pg in pages.values() for e in pg["counts"]]) if changed else []
        for entry in entries:
            graphic, lbl, last = entry[0], entry[1], entry[2]; n = totals.get(graphic, 0); text = count_text(n)
            if text == last: continue
            if (n == 0) != (last == "0"): lbl.Hue = entry[3] if n else entry[4]
            set_label_text(lbl, text); entry[2] = text
        if changed: refresh_castable()
        flags = scroll_flags(totals); shown = page_key(st["tab"])
        for key, pg in list(pages.items()):
            if pg.get("scrolls") is not None and pg["scrolls"] != flags and not st["dirty"]:
                if key == shown: build_page(key, False)
                else: clear(pages.pop(key)["ctrls"])
    BOOKISH = set([0x0EFA, 0x22C5, 0x0FEF, 0x0FF0, 0x0FF1, 0x0FF2, 0x0FF3, 0x0FF4,
                   0x0FBD, 0x0FBE, 0x1C11, 0x1C13, 0x2252, 0x2253, 0x238C, 0x23A0, 0x2D50])
    def report_books():
        books = [it for it in held_items() + items_in_pack() if it.Graphic in BOOKISH
                 or "book" in (it.Name or "").lower()]
        if not books: say("no books in your pack or hands.", Kit.HUE_BAD); return
        say("books you carry (graphic / hue / name / kind):", Kit.HUE_INFO)
        for it in books:
            kind = "runebook" if is_runebook(it) else ("spellbook" if is_spellbook(it) else "?")
            say("0x%04X / 0x%04X / %s (%s)." % (it.Graphic, it.Hue, it.Name or "no name", kind), Kit.HUE_INFO)
    def register_runebook():
        say("target one of your runebooks.", Kit.HUE_INFO); token = object(); st["pick"] = token
        def done(serial):
            if st["pick"] is not token: return
            st["pick"] = None; st["queue"].insert(0, ("registered", serial))
        HOST.pick_target(15, done)
    def registered(serial):
        if not serial: say("cancelled.", Kit.HUE_INFO); return False
        it = API.FindItem(serial)
        if not it: say("that isn't an item.", Kit.HUE_BAD); return False
        rb_types.add((it.Graphic, it.Hue))
        Kit.put_var("Grimoire_RunebookTypes", ",".join("%X:%X" % t for t in sorted(rb_types)))
        say("runebooks are graphic 0x%04X, hue 0x%04X; saved." % (it.Graphic, it.Hue), Kit.HUE_GOOD); return True
    def _book_vals(items):
        out = []
        for it in items:
            try: g, h, n = it.Graphic, it.Hue, it.Name
            except Exception: continue
            out.append((it.Serial, g, h, n, is_runebook_v(g, h, n)))
        return out
    def find_runebooks():
        found, seen_titles = [], {}; pack = _book_vals(items_in_pack(fresh=True))
        rb_seen.update((g, h) for s, g, h, n, rb in pack if rb and n); got = set()
        for s, g, h, n, rb in _book_vals(held_items()) + pack:
            book = rb or (not n and (g, h) in rb_seen)
            if not book or int(s) in got: continue
            got.add(int(s)); title = (n or "").strip() or "Runebook"; title = title[:1].upper() + title[1:]
            seen_titles[title] = seen_titles.get(title, 0) + 1
            if seen_titles[title] > 1: title = "%s %d" % (title, seen_titles[title])
            found.append({"serial": int(s), "title": title})
        return found
    def file_lines(raw): return str(raw or "").replace("\r", "").replace("\x00", "").split("\n")
    def parser_selftest():
        out = {}
        try:
            out["is_cmd"] = Kit.gump_is_cmd("croppedtext 305 60 115 17 81 17")
            out["text_is_text"] = not Kit.gump_is_cmd("Page 2 Boss"); lines, cmds = Kit.gump_parse("Shame Bankpage 0")
            out["split_merged"] = (lines, cmds); out["lines"] = len(Kit.gump_parse("a\nb\nc\npage 0")[0])
        except Exception as ex: out["error"] = str(ex)
        return out
    JUNK_TEXT = re.compile(r"^(empty|\(indescript\)|charges?:?|max charges:?|rename( book)?|drop rune|set default|"
        r"recall.*|gate travel.*|sacred journey.*|use charge.*|next|prev(ious)?|okay|cancel|"
        r"felucca|trammel|ilshenar|malas|tokuno)$", re.I)
    COORDS = re.compile(r"\d+\s*[o\u00b0]\s*\d+'?\s*[NSEW]", re.I)
    TEXT_ARG = {"croppedtext": (7, 6), "text": (5, 4), "htmlgump": (6, 5)}
    def gump_elements(raw):
        lines, cmds = Kit.gump_parse(raw); page, buttons, labels = 0, [], []
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "page": page = int(t[1])
                elif k == "button" and len(t) >= 8:
                    if int(t[5]) == 1: buttons.append((page, int(t[1]), int(t[2]), int(t[7])))
                elif k in TEXT_ARG and len(t) >= TEXT_ARG[k][0]:
                    labels.append((page, int(t[1]), int(t[2]), Kit.strip_html(lines[int(t[TEXT_ARG[k][1]])])))
            except (ValueError, IndexError): continue
        return lines, buttons, labels
    def looks_like_destination(text):
        t = text.strip()
        if not t or JUNK_TEXT.match(t) or COORDS.search(t): return False
        return not re.match(r"^[\d\s/:.,-]+$", t)
    parse_stats = {}
    def extract_destinations(raw):
        lines, cmds = Kit.gump_parse(raw); parse_stats.clear()
        parse_stats.update({"text_lines": len(lines), "commands": len(cmds)})
        if cmds: parse_stats["last_command"] = " ".join(cmds[-1])
        else: tail = file_lines(raw); parse_stats["last_line_repr"] = repr(tail[-2] if len(tail) > 1 else tail[-1])
        seen, pending = {}, None
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "button" and len(t) >= 8 and t[5] == "1":
                    bid = int(t[7]); pending = bid if bid >= 2 and (bid - 2) % 6 == 0 else None
                elif k in ("croppedtext", "text") and pending is not None:
                    name = Kit.strip_html(lines[int(t[-1])]); slot = (pending - 2) // 6
                    if slot not in seen: seen[slot] = (name, pending)
                    pending = None
                else: pending = None
            except Exception as ex: parse_stats["error"] = str(ex); pending = None
        parse_stats["sequential_pairs"] = len(seen)
        dests = [{"name": n, "slot": sl, "button": bid} for sl, (n, bid) in seen.items() if n and n.lower() != "empty"]
        if dests: return sorted(dests, key=lambda d: d["name"].lower())
        lines, buttons, labels = gump_elements(raw)
        parse_stats.update({"buttons": len(buttons), "labels": len(labels)})
        def pair(btns):
            out = {}
            for (bp, bx, by, bid) in sorted(btns):
                if bid in out: continue
                best = None
                for (lp, lx, ly, text) in labels:
                    dx, dy = lx - bx, abs(ly - by)
                    if lp != bp or dy > 12 or dx == 0: continue
                    if 0 < dx <= 60: score = dx
                    elif -150 <= dx < 0: score = 100 - dx
                    else: continue
                    if best is None or score < best[0]: best = (score, text, bp)
                if best and looks_like_destination(best[1]): out[bid] = (best[1], best[2])
            return out
        std = pair([b for b in buttons if b[3] >= 2 and (b[3] - 2) % 6 == 0]); dests = []
        for bid, (name, _) in std.items():
            slot = (bid - 2) // 6
            if not any(d["slot"] == slot for d in dests): dests.append({"name": name, "slot": slot, "button": bid})
        if not dests:
            paired = pair(buttons); by_page = {}
            for bid, (name, pg) in paired.items(): by_page.setdefault(pg, []).append((name, bid))
            if by_page:
                best_page = max(sorted(by_page), key=lambda pg: len(by_page[pg]))
                for name, bid in by_page[best_page]: dests.append({"name": name, "slot": None, "button": bid})
        return sorted(dests, key=lambda d: d["name"].lower())
    CHARGES_TEXT = re.compile(r"^(max(imum)?\s*)?charges?\s*:?\s*(\d+)?\s*(/\s*(\d+))?$", re.I)
    def extract_charges(raw):
        lines, cmds = Kit.gump_parse(raw); found, want, nums = {}, None, []; page = 0
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "page": page = int(t[1]); continue
                if k in ("xmfhtmlgump", "xmfhtmlgumpcolor", "xmfhtmltok") and len(t) >= 6:
                    cl = int(t[5])
                    if cl == 1011296: want = "cur"
                    elif cl == 1011297: want = "max"
                    continue
                if k not in TEXT_ARG or len(t) < TEXT_ARG[k][0]: continue
                x, y, text = int(t[1]), int(t[2]), lines[int(t[TEXT_ARG[k][1]])]
            except (ValueError, IndexError): continue
            text = Kit.strip_html(text)
            if Kit.gump_is_int(text):
                if want and want not in found: found[want] = int(text); want = None
                else: nums.append((page, x, y, int(text)))
                continue
            m = CHARGES_TEXT.match(text)
            if m:
                key = "max" if m.group(1) else "cur"
                if m.group(3):
                    found.setdefault(key, int(m.group(3)))
                    if m.group(5): found.setdefault("max", int(m.group(5)))
                else: want = key
        if not found and len(nums) >= 2:
            (p1, x1, y1, a), (p2, x2, y2, b) = nums[0], nums[1]
            if p1 == p2 and abs(y1 - y2) <= 4 and x2 > x1 and a <= b: found = {"cur": a, "max": b}
        return found.get("cur"), found.get("max")
    def esc(s):
        return (str(s).replace("%", "%25").replace("|", "%7C").replace(";", "%3B")
                .replace("\t", "%09").replace("\n", "%0A").replace("\r", ""))
    def unesc(s):
        return (s.replace("%0A", "\n").replace("%09", "\t").replace("%3B", ";")
                .replace("%7C", "|").replace("%25", "%"))
    def hex_encode(s): return "".join(["%04X" % ord(ch) for ch in s])
    def hex_decode(h):
        try: return "".join([chr(int(h[i:i + 4], 16)) for i in range(0, len(h) - 3, 4)])
        except ValueError: return ""
    def opt_int(s): return int(s) if Kit.gump_is_int(s) else None
    def write_file(path, text):
        try: import System; System.IO.File.WriteAllText(path, text)
        except Exception: f = open(path, "w"); f.write(text); f.close()
    SAVE_FILE = "Grimoire_saved.txt"; saved = {"data": None, "warned": False, "dirty": set()}
    def saved_data():
        if saved["data"] is None:
            saved["data"] = {}; text = ""; path = Kit.data_path(SAVE_FILE)
            try:
                import System
                if System.IO.File.Exists(path): text = System.IO.File.ReadAllText(path)
            except Exception:
                try: f = open(path, "r"); text = f.read(); f.close()
                except Exception: text = ""
            for line in file_lines(text):
                if "\t" in line: k, v = line.split("\t", 1); saved["data"][k] = v
        return saved["data"]
    def save_value(key, value):
        data = saved_data()
        if data.get(key) == value: return
        data[key] = value; saved["dirty"].add(key)
    def flush_saved():
        if not saved["dirty"]: return
        keys, saved["dirty"] = saved["dirty"], set(); data = saved_data()
        text = "\n".join([k + "\t" + data[k] for k in sorted(data)]) + "\n"; path = Kit.data_path(SAVE_FILE)
        try: write_file(path, text); return
        except Exception as ex:
            if not saved["warned"]: say("couldn't save to %s (%s)." % (path, ex), Kit.HUE_BAD); saved["warned"] = True
        for key in sorted(keys):
            try: API.SavePersistentVar("Grimoire_H_" + key, hex_encode(data[key]), API.PersistentVar.Char)
            except Exception:
                if not saved["warned"]:
                    say("couldn't save the runebook lists; they are read again next time.", Kit.HUE_BAD)
                    saved["warned"] = True
    def load_value(key):
        v = saved_data().get(key)
        if v: return v
        h = Kit.get_var("Grimoire_H_" + key); return hex_decode(h) if h else ""
    def book_key(serial): return "book_%08X" % int(serial)
    def opt_str(v): return "" if v is None else str(v)
    def save_book(serial):
        dests = rune_cache.get(serial)
        if dests is None: return
        cur, mx = book_charges.get(serial, (None, None)); parts = ["v1", opt_str(cur), opt_str(mx)]
        parts += ["|".join([esc(d["name"]), opt_str(d["slot"]), opt_str(d["button"]),
                            str(d.get("rune") or "")]) for d in dests]
        save_value(book_key(serial), ";".join(parts))
    def load_book(serial):
        parts = load_value(book_key(serial)).split(";")
        if len(parts) < 3 or parts[0] != "v1": return False
        dests = []
        for p in parts[3:]:
            f = p.split("|")
            if len(f) != 4: continue
            d = {"name": unesc(f[0]), "slot": opt_int(f[1]), "button": opt_int(f[2])}
            if opt_int(f[3]): d["rune"] = opt_int(f[3])
            dests.append(d)
        rune_cache[serial] = dests; book_charges[serial] = (opt_int(parts[1]), opt_int(parts[2])); return True
    def store_book(serial, dests, charges):
        old = (rune_cache.get(serial, "none"), book_charges.get(serial))
        if rune_cache.get(serial) and (dests is None or (not dests and serial in rune_errors)): return False
        rune_cache[serial] = dests
        if charges is not None: book_charges[serial] = charges; charge_news.append(serial)
        if dests is not None: save_book(serial)
        changed = old != (rune_cache.get(serial), book_charges.get(serial))
        if changed: rekey_favs(serial); lists["ver"] += 1
        return changed
    def resolve(serial, index, name=None, taken=None):
        lst = rune_cache.get(serial)
        if not lst: return None
        n = len(lst)
        if 0 <= index < n and (name is None or lst[index]["name"] == name) and (taken is None or index not in taken):
            return index
        if name is None: return None
        hits = [(abs(i - index), i) for i in range(n) if lst[i]["name"] == name and (taken is None or i not in taken)]
        return min(hits)[1] if hits else None
    def fav_keys_now():
        keys, seen, lst = set(), set(), []
        for f in favs["list"]:
            k = (f[0], f[1]) if f[1] >= 0 else (f[0], -1, f[2])
            if k in seen: continue
            seen.add(k); lst.append(f)
            if f[1] >= 0: keys.add(k)
        if len(lst) != len(favs["list"]): favs["list"] = lst; favs["save"] = True
        favs["keys"] = keys
    def rekey_favs(serial):
        moved = False; taken = set()
        mine = sorted([f for f in favs["list"] if f[0] == serial], key=lambda f: (f[1] < 0, f[1]))
        for f in mine:
            i = resolve(serial, f[1], f[2], taken)
            if i is None:
                if f[1] != -1: f[1] = -1; moved = True
                continue
            taken.add(i)
            if i != f[1]: f[1] = i; moved = True
        if moved: fav_keys_now(); favs["save"] = True
        last = favs["last"]
        if last is not None and last[0] == serial:
            i = resolve(serial, last[1], last[2])
            if i is not None and i != last[1]: favs["last"] = (serial, i, last[2], last[3]); favs["save_last"] = True
    def load_favs():
        who = "%08X" % int(API.Player.Serial)
        if who == favs["owner"]: return
        if favs["save"] or favs["save_last"]: save_favs()
        lst = []; parts = load_value("favs_" + who).split(";")
        if parts and parts[0] == "v1":
            for p in parts[1:]:
                f = p.split("|")
                if len(f) != 3: continue
                try: lst.append([int(f[0], 16), int(f[1]), unesc(f[2])])
                except ValueError: continue
        last = None; parts = load_value("last_" + who).split(";")
        if len(parts) == 2 and parts[0] == "v1":
            f = parts[1].split("|")
            try:
                if len(f) == 4 and f[3] in TRAVEL_METHODS: last = (int(f[0], 16), int(f[1]), unesc(f[2]), f[3])
            except ValueError: last = None
        favs.update({"list": lst[:FAVS_MAX], "last": last, "owner": who, "save": False, "save_last": False})
        fav_keys_now(); lists["ver"] += 1
    def save_favs():
        who = favs["owner"]
        if who is None: favs["save"] = favs["save_last"] = False; return
        if favs["save"]:
            favs["save"] = False
            save_value("favs_" + who, ";".join(["v1"] + ["%08X|%d|%s" % (f[0], f[1], esc(f[2]))
                                                         for f in list(favs["list"])]))
        if favs["save_last"]:
            favs["save_last"] = False; last = favs["last"]
            if last is not None:
                save_value("last_" + who, "v1;%08X|%d|%s|%s" % (last[0], last[1], esc(last[2]), last[3]))
    def toggle_fav(serial, index, name):
        key = (serial, index)
        if key in favs["keys"]: favs["list"] = [f for f in favs["list"] if (f[0], f[1]) != key]; on = False
        else:
            if len(favs["list"]) >= FAVS_MAX:
                say("Favourites is full (%d); take a star off first." % FAVS_MAX, Kit.HUE_BAD); return
            favs["list"].append([serial, index, name]); on = True
        fav_keys_now(); favs["save"] = True; lists["ver"] += 1; return on
    def note_trip(serial, dest, method):
        idx = next((i for i, d in enumerate(rune_cache.get(serial) or []) if d is dest), None)
        if idx is None: idx = resolve(serial, 0, dest.get("name"))
        if idx is None: return
        favs["last"] = (serial, idx, dest.get("name") or "", method); favs["save_last"] = True; lists["ver"] += 1
    rune_errors = {}; dump = {"books": set()}
    def dump_due(): return not dump["written"] or dump["armed"]
    def write_dump(text):
        if not dump_due(): return None
        dump["written"], dump["armed"] = True, False; path = Kit.data_path("Grimoire_runebook_dump.txt")
        try: write_file(path, text)
        except Exception as ex: say("couldn't save the runebook details (%s)." % ex, Kit.HUE_BAD); return None
        say("saved the runebook details to %s." % path, Kit.HUE_INFO); return path
    def dumped(serial, path):
        if path:
            old, dump["books"] = dump["books"], set([serial])
            for s in old:
                if s != serial: Kit.on_client(lambda s=s: drop_page(s) if s in pages else None)
    def describe_items(container):
        return Kit.on_client(lambda: ["  0x%08X  graphic 0x%04X  hue 0x%04X  amount %d  name '%s'"
            % (it.Serial, it.Graphic, it.Hue, it.Amount or 0, it.Name or "")
            for it in list(API.ItemsInContainer(container) or [])])
    def open_book(serial):
        nonlocal gump_id
        if gump_id and API.HasGump(gump_id): API.CloseGump(gump_id); HOST.idle(0.1)
        before = API.HasGump(); API.ConfigNextGump(serial=gump_id, isVisible=False); API.UseObject(serial)
        def look():
            gid = API.HasGump()
            if gid and (gid == gump_id or gid != before): return ("gump", gid)
            book = API.FindItem(serial); return ("container", None) if book and book.GetContainerGump() else None
        result = (None, "double-clicking the book opened nothing within 3 seconds"); deadline = time.time() + 3.0
        try:
            while time.time() < deadline and HOST.idle(0.05):
                seen = Kit.on_client(look)
                if seen is not None: result = seen; break
        finally: API.ConfigNextGump()
        if (result[0] is None and Kit.on_client(lambda: len(list(API.ItemsInContainer(serial) or [])))):
            result = ("container", None)
        if result[0] == "gump": gump_id = result[1]
        return result
    def rune_label(rune_serial):
        def item_name(): it = API.FindItem(rune_serial); return ((it.Name if it else "") or "").strip()
        name = Kit.on_client(item_name)
        if not name or name.lower() in ("recall rune", "a recall rune", "rune"):
            try:
                rd = journal_from_now(); clicked = time.time(); API.ClickObject(rune_serial); deadline = clicked + 1.0
                own = name.lower(); plain, plain_by = None, 0.0
                while time.time() < deadline and HOST.idle(0.1):
                    best = None
                    for ln in rd.new():
                        who = (ln.name or "").lower(); txt = (ln.text or "").strip()
                        if not txt or (who and who != own) or va_line(txt): continue
                        if "rune" in ln.low: best = txt; break
                        if plain is None: plain, plain_by = txt, time.time() + 0.3
                    if best is not None: name = best; break
                    if plain is not None and time.time() >= plain_by: name = plain; break
                else:
                    if plain is not None: name = plain
            except Exception: pass
        return re.sub(r"^(a |an )?(marked )?recall rune( for| to)?\s*", "", name, flags=re.I).strip()
    def read_container_book(serial):
        dests = []; runes = Kit.on_client(lambda: [it.Serial for it in list(API.ItemsInContainer(serial) or [])])
        for rune in runes or []:
            name = rune_label(rune)
            if not name or "unmarked" in name.lower(): continue
            dests.append({"name": name, "slot": None, "button": None, "rune": rune})
        def close():
            book = API.FindItem(serial); g = book.GetContainerGump() if book else None
            if g: g.Dispose()
        Kit.on_client(close); return sorted(dests, key=lambda d: d["name"].lower())
    def gump_text(gid):
        def read(): g = API.GetGump(gid); return (g.PacketGumpText or "") if g else ""
        return Kit.on_client(read)
    def read_runebook(serial):
        rune_errors.pop(serial, None); kind, gid = open_book(serial)
        if kind == "container":
            dests = read_container_book(serial)
            if not dests:
                rune_errors[serial] = "The book opened like a bag, but no named runes were inside."
                if dump_due():
                    dumped(serial, write_dump("Runebook 0x%08X opened as a CONTAINER\n\n" % serial +
                                              "\n".join(describe_items(serial))))
            return dests, None
        if kind is None:
            rune_errors[serial] = "Couldn't open it: " + gid + "."
            if dump_due():
                dumped(serial, write_dump("Runebook 0x%08X: %s\nLast server gump: 0x%08X\nItems " "inside:\n%s"
                                          % (serial, gid, API.HasGump(), "\n".join(describe_items(serial))
                                             or "  (none known)")))
            return None, None
        raw = gump_text(gid)
        if not raw: HOST.idle(0.1); raw = gump_text(gid)
        API.CloseGump(gid); dests = extract_destinations(raw) if raw else []
        if not dests:
            rune_errors.setdefault(serial, "The book's window didn't match any known layout.")
            if dump_due():
                lines, buttons, _ = gump_elements(raw) if raw else ([], [], [])
                parse_stats["selftest"] = parser_selftest()
                dumped(serial, write_dump("Runebook 0x%08X  gump 0x%08X  (%d texts, %d " "buttons)\nparser: %r\n\n%s"
                                          % (serial, gid, len(lines), len(buttons), parse_stats,
                                             raw or "(empty PacketGumpText)")))
            return dests, None
        return dests, extract_charges(raw)
    def note_open_gump(book_serial, gid):
        raw = gump_text(gid)
        if not raw: return
        dests = extract_destinations(raw)
        if dests and store_book(book_serial, dests, extract_charges(raw)): Kit.on_client(lambda: drop_page(book_serial))
    def fresh_dest(serial, dest):
        same = [d for d in (rune_cache.get(serial) or ())
                if d.get("name") == dest.get("name") and d.get("slot") is not None]
        for d in same:
            if d["slot"] == dest["slot"]: return d
        return same[0] if same else None
    def book_gump(book_serial):
        kind, gid = open_book(book_serial)
        if kind != "gump": say("the runebook did not open.", Kit.HUE_BAD); return None
        note_open_gump(book_serial, gid); HOST.idle(0.1); return gid
    def rune_gone(gid): API.CloseGump(gid); say("that rune isn't in the book any more; nothing was used.", Kit.HUE_BAD)
    TRAVEL_FAIL_TEXTS = CAST_FAIL_TEXTS + ("already casting", "not allowed to travel", "recall from this",
                                           "gate from this", "travel from this", "location is blocked",
                                           "too encumbered", "heat of battle", "doth not appear to work",
                                           "is not marked", "not yet marked")
    def item_amount(it): return max(1, int(it.Amount or 0))
    def trip_look(serials):
        def look():
            n = sum(item_amount(it) for it in map(API.FindItem, serials) if it)
            return bool(API.HasTarget("any")), n, (int(API.Player.X), int(API.Player.Y))
        return Kit.on_client(look)
    def cursor_up_refused():
        if API.HasTarget("any"):
            say("a target cursor is up; finish it or press Esc first.", Kit.HUE_INFO); return True
        return False
    def travel_by_scroll(book_serial, dest, method):
        graphic = GATE_SCROLL if method == "gate_scroll" else RECALL_SCROLL
        spell = "Gate Travel" if method == "gate_scroll" else "Recall"; since = journal_from_now(); me = player_name()
        found = Kit.on_client(lambda: next(((it.Serial, item_amount(it)) for it in items_in_pack()
                                            if it.Graphic == graphic), None))
        if not found: say("you have no %s scrolls." % spell, Kit.HUE_BAD); return
        scroll, before = found; target = dest.get("rune")
        if not target:
            if dest["slot"] is None: say("scrolls need a standard runebook layout.", Kit.HUE_BAD); return
            gid = book_gump(book_serial)
            if gid is None: return
            dest = fresh_dest(book_serial, dest)
            if dest is None: return rune_gone(gid)
            API.ConfigNextGump(serial=gid, isVisible=False); API.ReplyGump(2 + dest["slot"] * 6 + 2, gid)
            deadline = time.time() + 2.0
            while time.time() < deadline and HOST.idle(0.1):
                if API.HasGump(gid): break
            API.ConfigNextGump(); API.CloseGump(gid)
            if not HOST.idle(0.3): return
            target = book_serial
        if not wait_cursor_free(): return
        if cursor_up_refused(): return
        HOST.claim_cursor(KEY, SCROLL_CAST_TIMEOUT + 1.0)
        try:
            start = player_xy(); API.CancelPreTarget(); API.PreTarget(target, "neutral"); API.UseObject(scroll)
            deadline = time.time() + SCROLL_CAST_TIMEOUT
            while time.time() < deadline and HOST.idle(0.1):
                up, left, now_xy = trip_look((scroll,))
                if up:
                    HOST.idle(0.15)
                    if API.HasTarget("any") and not cursor_taken(): API.Target(target)
                    return
                if left < before or failed_since(since, me) or moved_far(start, now_xy): break
        finally: API.CancelPreTarget(); HOST.release_cursor(KEY)
    def cursor_taken(): return HOST.cursor_busy(KEY) is not None
    def wait_cursor_free():
        until = time.time() + 3.0
        while cursor_taken() and time.time() < until:
            if not HOST.idle(0.1): return False
        return True
    def player_xy(): return Kit.on_client(lambda: (int(API.Player.X), int(API.Player.Y)))
    def player_name(): return Kit.on_client(lambda: API.Player.Name) or ""
    def moved_far(start, now):
        return start is not None and now is not None and max(abs(now[0] - start[0]), abs(now[1] - start[1])) > 30
    def journal_from_now(): Journal.update(True); return Journal.Reader()
    _va = {"titles": None}
    def va_line(text):
        i = text.find(": ")
        if i <= 0 or i > 60: return False
        titles = _va["titles"]
        if titles is None:
            titles = set(["Virtue Assistant", "Grimoire"])
            for sl in HOST.slots:
                titles.add(sl.title)
                for p in sl.parts: titles.add(p[1]); titles.add("%s > %s" % (sl.title, p[1]))
            _va["titles"] = titles
        return text[:i] in titles
    def failure_in(lines, texts, me):
        for ln in lines:
            name = ln.name or ""
            if name and name != "System" and name != me: continue
            low = ln.low
            for f in texts:
                if f in low:
                    if not va_line(ln.text or ""): return True
                    break
        return False
    def failed_since(rd, me=""): return failure_in(rd.new(), TRAVEL_FAIL_TEXTS, me)
    def travel(book_serial, dest, method):
        if cursor_up_refused(): return
        if method in ("recall_scroll", "gate_scroll"): travel_by_scroll(book_serial, dest, method); return
        if dest.get("rune"):
            spell = TRAVEL_SPELL.get(method, "Recall")
            if not wait_cursor_free(): return
            if cursor_up_refused(): return
            HOST.claim_cursor(KEY, RUNE_CAST_CLAIM)
            try:
                since, start, me = journal_from_now(), player_xy(), player_name(); pearl = REAGENTS["BP"][1]
                stacks = Kit.on_client(lambda: [(it.Serial, item_amount(it)) for it in items_in_pack(True)
                                                if it.Graphic == pearl]) if spell in ("Recall", "Gate Travel") else None
                serials = tuple(s for s, _n in stacks or ()); before = sum(n for _s, n in stacks or ())
                API.CancelPreTarget(); API.PreTarget(dest["rune"], "neutral"); API.CastSpell(spell)
                deadline = time.time() + RUNE_CAST_CLAIM
                while time.time() < deadline and HOST.idle(0.1):
                    up, left, now_xy = trip_look(serials)
                    if up: HOST.idle(0.15); break
                    if before and left < before: break
                    if failed_since(since, me) or moved_far(start, now_xy): break
            finally: API.CancelPreTarget(); HOST.release_cursor(KEY)
            return
        gid = book_gump(book_serial)
        if gid is None: return
        if dest["slot"] is not None:
            dest = fresh_dest(book_serial, dest)
            if dest is None: return rune_gone(gid)
            API.ReplyGump(2 + dest["slot"] * 6 + TRAVEL_TYPES[method], gid)
        else: API.ReplyGump(dest["button"], gid)
        if (method == "charge" or dest["slot"] is None) and book_serial not in bg_reads: bg_reads.append(book_serial)
    view = {"scale": 1.0}
    def sc(v): return int(round(v * view["scale"]))
    def on_window(parent, ctrl):
        if parent is gump:
            tgt["tops"].append(ctrl)
            if tgt["hidden"]: ctrl.IsVisible = False
    def show_layer(layer, shown):
        for ctrl in layer["tops"]: ctrl.IsVisible = shown
        layer["hidden"] = not shown
    def put(parent, ctrl, track): on_window(parent, ctrl); parent.Add(ctrl); track.append(ctrl); return ctrl
    def box(parent, x, y, w, h, color, alpha, track):
        b = G.CreateGumpColorBox(alpha, color); b.SetRect(sc(x), sc(y), max(1, sc(w)), max(1, sc(h)))
        return put(parent, b, track)
    def label(parent, text, x, y, size, color, track, width=0, align="left", smooth=False):
        hue = TEXT_HUES.get(color)
        if hue is not None and not smooth and not (width and align == "left"):
            l = G.CreateGumpLabel(text, hue); l.SetAcceptMouseInput(False); place_uo(l, x, y, size, width, align)
            return put(parent, l, track)
        size = max(6, sc(size))
        if width: l = G.CreateGumpTTFLabel(text, size, color, aligned=align, maxWidth=sc(width))
        else: l = G.CreateGumpTTFLabel(text, size, color)
        l.SetPos(sc(x), sc(y)); l.SetAcceptMouseInput(False); return put(parent, l, track)
    _uo_meta = {}
    def place_uo(l, x, y, size, width, align):
        lw = int(l.GetWidth()) or 7 * len(l.Text or ""); lh = int(l.GetHeight()) or 16; X = sc(x)
        if width and align == "center": X += max(0, (sc(width) - lw) // 2)
        elif width and align == "right": X += max(0, sc(width) - lw)
        Y = sc(y) + max(0, (int(sc(size) * 1.3) - lh) // 2); l.SetPos(X, Y)
        if width and align != "left":
            if len(_uo_meta) > 3000:
                for k in [k for k in _uo_meta if k.IsDisposed]: del _uo_meta[k]
            _uo_meta[l] = (x, y, size, width, align)
    def set_label_text(l, text):
        l.Text = text; m = _uo_meta.get(l)
        if m is not None: place_uo(l, m[0], m[1], m[2], m[3], m[4])
    def item_pic(parent, graphic, x, y, size, track):
        p = G.CreateGumpItemPic(graphic, sc(size), sc(size)); p.SetPos(sc(x), sc(y)); p.SetAcceptMouseInput(False)
        return put(parent, p, track)
    def star(parent, x, y, on, track):
        color = STAR_ON if on else STAR_OFF; parts = []
        for rx, ry, rw, rh in ((6, 0, 2, 4), (0, 4, 14, 2), (3, 6, 8, 3), (2, 9, 3, 3), (9, 9, 3, 3)):
            b = box(parent, x + rx, y + ry, rw, rh, color, 1.0, track); b.SetAcceptMouseInput(False); parts.append(b)
        return parts
    _star_rgb = dict((on, tuple(int(col[i:i + 2], 16) for i in (1, 3, 5))) for on, col in ((True, STAR_ON),
                                                                                           (False, STAR_OFF)))
    def recolor_star(parts, on):
        r, g_, b_ = _star_rgb[bool(on)]
        for p in parts: p.SetBaseColor(r, g_, b_, 255)
    def on_click(ctrl, fn): G.AddControlOnClick(ctrl, fn)
    _dbl = {"ok": None}
    def hook_double_click(api_ctrl, fn):
        if _dbl["ok"] is False: return False
        _dbl["ok"] = Kit.hook_double(api_ctrl, fn, queue=False)
        if not _dbl["ok"]:
            say("double-clicks can't be caught on this client; click a row, then click it again to use it.",
                Kit.HUE_BAD)
        return _dbl["ok"]
    def make_row_click(key, action):
        def cb():
            now = time.time(); prev = click_state["selected"]
            if prev is not None and prev != key and prev in row_bgs: row_bgs[prev].SetAlpha(ROW_A)
            if key in row_bgs: row_bgs[key].SetAlpha(0.20)
            click_state["selected"] = key
            if _dbl["ok"] is False and click_state["key"] == key and now - click_state["t"] <= 3.0:
                click_state["key"], click_state["t"] = None, 0.0; st["queue"].append(stamped(action, now))
            else: click_state["key"], click_state["t"] = key, now
        return cb
    def stamped(action, now=None):
        if action[0] == "cast": return action + (now or time.time(),)
        if action[0] in ("travel", "favgo"): return ("pressed", now or time.time(), action)
        return action
    def bind_row(bg, key, action):
        on_click(bg, make_row_click(key, action)); hook_double_click(bg, queue_stamped(action))
    def go_circle(i):
        if i != st["circle"] or st["tab"] != "spells": switch_page("spells", lambda: st.update({"circle": i}))
    queue_action = Kit.queuer(st)
    def queue_stamped(action):
        def cb(): st["queue"].append(stamped(action))
        return cb
    def queue_ui(action):
        def cb():
            if action not in st["ui_queue"]: st["ui_queue"].append(action)
        return cb
    def load_int(name, default):
        try: return int(Kit.get_var("Grimoire_" + name, str(default)))
        except Exception: return default
    def save_int(name, value): Kit.put_var("Grimoire_" + name, str(int(value)))
    win = {"w": DEFAULT_W, "h": DEFAULT_H, "opacity": DEFAULT_OPACITY}; pending_scale = {"value": None, "t": 0.0}
    def load_window_prefs():
        view["scale"] = min(SCALE_MAX, max(SCALE_MIN, load_int("Scale", 100))) / 100.0
        win["w"] = max(sc(MIN_W), load_int("W", sc(DEFAULT_W))); win["h"] = max(sc(MIN_H), load_int("H", sc(DEFAULT_H)))
        win["opacity"] = min(100, max(0, load_int("Opacity", DEFAULT_OPACITY))); fit_screen()
    def fit_screen():
        if fitst["own"] is not None: return
        W, H = Kit.screen()
        if H > 0: win["h"] = max(MIN_H * SCALE_MIN // 100, min(win["h"], H))
        if W > 0: win["w"] = max(MIN_W * SCALE_MIN // 100, min(win["w"], W))
    def LW(): return max(MIN_W, int(win["w"] / view["scale"]))
    def LH(): return max(MIN_H, int(win["h"] / view["scale"]))
    bg_box = {"parts": []}
    def on_resized():
        if st["minimized"]: return
        win["w"], win["h"] = gump.GetWidth(), gump.GetHeight(); loop["size_dirty"] = True; st["dirty"] = True
        loop["settle"] = time.time() + 0.3
    def save_size():
        loop["size_dirty"] = False
        if fitst["own"] is not None: return
        for k, v in (("W", win["w"]), ("H", win["h"])): save_int(k, v)
    def create_window():
        nonlocal gump; fit_screen(); px, py = load_int("X", -1), load_int("Y", -1)
        if px >= 0:
            px, py = Kit.adapt(px, max(0, py), win["w"], win["h"]); px, py = Kit.clamp(px, py, win["w"], win["h"])
            px, py = max(0, px), max(0, py)
        gump = G.CreateModernGump(px if px >= 0 else 100, py if py >= 0 else 60, win["w"], win["h"],
                                  True, MIN_W * SCALE_MIN // 100, MIN_H * SCALE_MIN // 100, on_resized)
        gump.SetAlpha(0)
        if px < 0: gump.CenterXInViewPort(); gump.CenterYInViewPort()
    def clear(track):
        for c in track: _uo_meta.pop(c, None); c.Dispose()
        del track[:]
    _art_sizes = {}
    def art_size(graphic):
        if graphic not in _art_sizes:
            p = G.CreateGumpPic(graphic, 0, 0, 0); _art_sizes[graphic] = (int(p.GetWidth()), int(p.GetHeight()))
            p.Dispose()
        return _art_sizes[graphic]
    def pic_px(parent, graphic, X, Y, W, H, track, mouse=False, hue=0):
        p = G.CreateGumpPic(graphic, X, Y, hue); p.SetWidth(max(1, W)); p.SetHeight(max(1, H))
        if not mouse: p.SetAcceptMouseInput(False)
        return put(parent, p, track)
    def tiled_px(parent, graphic, X, Y, W, H, track):
        t = G.CreateTiledGumpPic(graphic, max(1, W), max(1, H)); t.SetRect(X, Y, max(1, W), max(1, H))
        t.SetAcceptMouseInput(False); return put(parent, t, track)
    def stone(parent, x, y, w, h, track, alpha=1.0):
        X0, Y0, X3, Y3 = sc(x), sc(y), sc(x + w), sc(y + h); lw, th = art_size(ART_FRAME)
        rw, bh = art_size(ART_FRAME + 8); lw, rw = min(lw, (X3 - X0) // 2), min(rw, (X3 - X0) // 2)
        th, bh = min(th, (Y3 - Y0) // 2), min(bh, (Y3 - Y0) // 2); xs = [X0, X0 + lw, X3 - rw, X3]
        ys = [Y0, Y0 + th, Y3 - bh, Y3]; parts = []
        for i in [4, 0, 1, 2, 3, 5, 6, 7, 8]:
            cx, cy = i % 3, i // 3; W, H = xs[cx + 1] - xs[cx], ys[cy + 1] - ys[cy]
            if W <= 0 or H <= 0: continue
            if i in (0, 2, 6, 8): parts.append(pic_px(parent, ART_FRAME + i, xs[cx], ys[cy], W, H, track))
            else: parts.append(tiled_px(parent, ART_FRAME + i, xs[cx], ys[cy], W, H, track))
        for p in parts: p.SetAlpha(alpha)
        return [(p, 1.0) for p in parts]
    def parchment(parent, x, y, w, h, track, alpha=1.0):
        p = tiled_px(parent, Kit.SECTION_TILE, sc(x), sc(y), sc(w), sc(h), track); p.SetAlpha(alpha * Kit.SECTION_ALPHA)
        return [(p, Kit.SECTION_ALPHA)]
    def corner_knots(w, h, track):
        cw, ch = art_size(Kit.CORNER_ART); W, H = sc(w), sc(h)
        return [pic_px(gump, Kit.CORNER_ART, X, Y, cw, ch, track)
                for X, Y in ((0, 0), (W - cw, 0), (0, H - ch), (W - cw, H - ch))]
    _ttf_widths = {}
    def text_w(text): return int(round(Kit.text_px(text) / view["scale"]))
    def fit(text, room, size=None):
        if size is None: return Kit.fit(text, sc(room))
        if ttf_w(text, size) <= room: return text
        lo, hi = 2, len(text) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ttf_w(text[:mid] + "..", size) <= room: lo = mid
            else: hi = mid - 1
        return text[:lo].rstrip() + ".."
    def ttf_w(text, size):
        key = (text, size, view["scale"])
        if key not in _ttf_widths:
            if len(_ttf_widths) >= 4000: _ttf_widths.clear()
            l = G.CreateGumpTTFLabel(text, max(6, sc(size)), COL_TEXT); px = int(l.GetWidth() or 0); l.Dispose()
            _ttf_widths[key] = px or int(0.55 * size * len(text))
        return int(round(_ttf_widths[key] / view["scale"]))
    def art_w(art): return int(round(art_size(art[0])[0] / view["scale"]))
    def button(x, y, w, h, text, tooltip, fn, size=14, parent=None, art=Kit.ART_PLAY):
        parent = parent or gump; c = tgt["ctrls"]
        gw, gh = art_size(art[0]); b = G.CreateGumpButton("", 0, art[0], art[1], art[2])
        b.SetPos(sc(x), sc(y) + max(0, (sc(h) - gh) // 2)); put(parent, b, c); on_click(b, fn); Kit.with_tip(b, tooltip)
        if text:
            lx = x + int(round(gw / view["scale"])) + 4
            label(parent, text, lx, y + (h - size) // 2 - 1, size, COL_TEXT, c)
            hit = box(parent, lx, y, max(4, x + w - lx), h, COL_ROW, 0.0, c); on_click(hit, fn)
            Kit.with_tip(hit, tooltip)
        return b
    def min_click():
        if Kit.zone_up(KEY) and not st["minimized"]: return
        HOST.dock_want_set(KEY, False); toggle_min()
    def fold_to_bar():
        if Kit.zone_up(KEY): return
        HOST.dock_want_set(KEY, True)
        if not st["minimized"]: toggle_min()
        if HOST.bar_alive(): set_docked(True)
        else: HOST.dock_note(TITLE)
    def toggle_min():
        st["minimized"] = not st["minimized"]
        if st["minimized"]: gump.SetResizable(False); gump.SetHeight(sc(TITLE_H))
        else: gump.SetHeight(win["h"]); gump.SetResizable(True)
        set_docked(False); save_int("Min", 1 if st["minimized"] else 0); st["dirty"] = True
    def save_window_pos():
        x, y = int(gump.GetX()), int(gump.GetY()); loop["last_pos"] = (x, y)
        for k, v in (("X", x), ("Y", y)): save_int(k, v)
    def set_docked(on):
        on = bool(on)
        if on == st["docked"]: return
        st["docked"] = on; gump.IsVisible = not on
    def link_tick():
        now = time.time()
        if now < st.get("link_next", 0.0): return
        st["link_next"] = now + 0.1
        if st.pop("to_bar", False): fold_to_bar()
        cmd = API.GetSharedVar(LINK_CMD)
        if cmd:
            API.RemoveSharedVar(LINK_CMD); cmd = str(cmd)
            if cmd == "show" and (st["minimized"] or st["docked"]):
                HOST.dock_want_set(KEY, False)
                if st["minimized"]: toggle_min()
                set_docked(False)
            elif cmd == "dock" and not st["docked"]: fold_to_bar()
        if st["docked"]:
            if not HOST.bar_alive(): set_docked(False)
        elif st["minimized"] and now >= st.get("wish_next", 0.0):
            st["wish_next"] = now + 0.25
            if HOST.dock_wanted(KEY) and HOST.bar_alive(): set_docked(True)
        elif not st["minimized"] and now >= st.get("wish_next", 0.0):
            st["wish_next"] = now + 1.0
            if HOST.dock_wanted(KEY): HOST.dock_want_set(KEY, False)
        ls = "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")
        if ls != st["link_state"]: st["link_state"] = ls; API.SetSharedVar(LINK_STATE, ls)
    def on_opacity(value):
        win["opacity"] = int(value)
        for p, factor in bg_box["parts"]: p.SetAlpha(win["opacity"] / 100.0 * factor)
        save_int("Opacity", win["opacity"])
    def on_scale(value): pending_scale["value"] = int(value); pending_scale["t"] = time.time()
    def size_gump():
        gump.SetWidth(win["w"]); gump.SetHeight(sc(TITLE_H) if st["minimized"] else win["h"]); st["dirty"] = True
    def save_scale(new, w, h):
        for k, v in (("Scale", int(round(new * 100))), ("W", w), ("H", h)): save_int(k, v)
    def rescale(new, save):
        if abs(new - view["scale"]) < 0.001: return
        ratio = new / view["scale"]; view["scale"] = new
        win["w"], win["h"] = int(round(win["w"] * ratio)), int(round(win["h"] * ratio))
        own_w, own_h = win["w"], win["h"]; fit_screen(); size_gump()
        if save: save_scale(new, own_w, own_h)
    def apply_scale():
        value = pending_scale["value"]; pending_scale["value"] = None
        new = min(SCALE_MAX, max(SCALE_MIN, value)) / 100.0
        if fitst["own"] is None: rescale(new, True); return
        if abs(new - fitst["own"][0]) < 0.001: return
        own_w = int(round(fitst["own"][1] * new / fitst["own"][0]))
        own_h = int(round(fitst["own"][2] * new / fitst["own"][0])); rescale(new, False)
        fitst["own"] = (new, own_w, own_h); save_scale(new, own_w, own_h)
        if fitst["told"] is not None: st["ui_queue"].append(("fit",) + fitst["told"])
    fitst = {"own": None, "told": None}
    def layout_fit(w, h, mode): fitst["told"] = (w, h) if w else None; st["ui_queue"].append(("fit", w, h))
    def run_fit(w, h):
        if not w:
            own, fitst["own"] = fitst["own"], None
            if own is not None: view["scale"] = own[0]; win["w"], win["h"] = own[1], own[2]; fit_screen(); size_gump()
            return
        if fitst["own"] is None: fitst["own"] = (view["scale"], win["w"], win["h"])
        w, h = int(w), int(h)
        if st["minimized"]: h = win["h"]
        if (win["w"], win["h"]) != (w, h): win["w"], win["h"] = w, h; size_gump()
    BOTTOM_H = 48
    def build_chrome():
        w = LW(); h = TITLE_H if st["minimized"] else LH(); c = tgt["ctrls"]; op = win["opacity"] / 100.0
        bg_box["parts"] = stone(gump, 0, 0, w, h, c, op); frame = [p for p, _f in bg_box["parts"]]
        bg_box["parts"] += parchment(gump, 12, 12, w - 24, 30, c, op)
        if not st["minimized"]:
            frame += corner_knots(w, h, c); bg_box["parts"] += parchment(gump, 12, h - 40, w - 24, 28, c, op)
        Kit._frame_parts[gump] = frame; label(gump, "GRIMOIRE", 42, 18, 14, COL_HEAD, c)
        left = w - 12 - 44 - 20 - (0 if st["minimized"] else Kit.DOCK_DX + 106 + 98)
        c.append(Kit.title_catcher(gump, sc(12), sc(12), sc(left - 16), sc(30), queue_ui(("min_click",)),
                                   key="grimoire:mini" if st["minimized"] else "grimoire"))
        x = w - 12 - 44; zoned = Kit.zone_up(KEY)
        if not zoned:
            button(x, 15, 30, 24, "", Kit.CLOSE_TIP % TITLE, queue_ui(("close",)), art=Kit.ART_CLOSE); x -= 20
            button(x, 15, 16, 24, "", Kit.RESTORE_TIP if st["minimized"] else Kit.MIN_TIP, queue_ui(("min_click",)),
                   art=Kit.ART_RESTORE if st["minimized"] else Kit.ART_MIN)
        if not st["minimized"]:
            if not zoned:
                x -= Kit.DOCK_DX
                button(x, 15, 16, 24, "", Kit.DOCK_TIP, lambda: st.__setitem__("to_bar", True), art=Kit.ART_DOCK)
            x -= 106
            button(x, 15, 100, 24, "Settings", Kit.SETTINGS_TIP % TITLE, queue_ui(("settings",)), art=Kit.ART_PAGE)
            x -= 98
            button(x, 15, 92, 24, "Refresh", "Find your spellbook and runebooks again and reread every runebook",
                   queue_action(("refresh",)), art=Kit.ART_OK)
        return 50
    def content_right(): return LW() - SIDE_W - 20
    def is_book_key(key): return key not in ("spells", "favs", "+add") and not isinstance(key, tuple)
    def book_low(serial): cur = book_charges.get(serial, (None, None))[0]; return cur is not None and cur < LOW_CHARGES
    def tab_tip(key, title, short):
        tip = title if short != title else None
        if is_book_key(key) and book_low(key):
            cur = book_charges[key][0]; tip = "%s: %s left (low)" % (title, Kit.count(cur, "charge"))
        return tip
    def tab_button(key, x, y, w, h, text, tooltip, title=None):
        c = tgt["ctrls"]; on = st["tab"] == key; color = COL_EMPTY if is_book_key(key) and book_low(key) else COL_TEXT
        gw, gh = art_size(GEM); gx, gy = sc(x), sc(y) + max(0, (sc(h) - gh) // 2)
        pic_px(gump, GEM, gx, gy, gw, gh, c); mark = pic_px(gump, GEM_ON, gx, gy, gw, gh, c)
        mark.SetAlpha(1.0 if on else 0.0)
        lbl = label(gump, text, x + int(round(gw / view["scale"])) + 4, y + (h - 14) // 2 - 1, 14, color, c)
        b = box(gump, x, y, w, h, COL_ROW, 0.0, c); fn = queue_switch(key); on_click(b, fn); on_click(mark, fn)
        if tooltip: b.SetTooltip(tooltip); mark.SetTooltip(tooltip)
        tab_marks[key] = mark
        if is_book_key(key): tab_parts[key] = (lbl, b, mark, title or text, text, color == COL_EMPTY)
    def recolor_tab(serial):
        parts = tab_parts.get(serial); low = book_low(serial)
        if parts is None or parts[5] == low: return
        lbl, b, mark, title, short, _ = parts; lbl.Hue = TEXT_HUES[COL_EMPTY if low else COL_TEXT]
        tab_parts[serial] = (lbl, b, mark, title, short, low); tip = tab_tip(serial, title, short) or title
        b.SetTooltip(tip); mark.SetTooltip(tip)
    def queue_switch(key):
        def cb(): st["switch"] = key
        return cb
    def build_tabs(top):
        tabs = [("spells", "Spellbook")] + ([("favs", "Favourites")] if runebooks else []) + \
            [(b["serial"], b["title"]) for b in runebooks]
        right = content_right(); row_h = 28; places, x, y = [], 20, top + 4; aw = art_w(Kit.ART_OK)
        for key, title in tabs:
            short = title if len(title) < 18 else title[:16] + ".."; w = max(90, aw + 4 + text_w(short) + 14)
            if x + w > right - 4: x, y = 20, y + row_h
            places.append((key, title, short, x, y, w)); x += w + 6
        if st["scanned"]:
            title = "Add runebook..."; w = max(90, aw + 4 + text_w(title) + 14); ax = right - 4 - w
            if x > ax: y += row_h
            places.append(("+add", title, title, ax, y, w))
        tabs_bottom = y + row_h + 2; op = win["opacity"] / 100.0
        bg_box["parts"] += parchment(gump, 12, top, right - 12, tabs_bottom - top, tgt["ctrls"], op)
        for key, title, short, x, y, w in places:
            if key == "+add":
                button(x, y, w, 24, short, "Target an unlisted runebook; books of its kind are found from then on",
                       queue_action(("register",)), art=Kit.ART_OK)
            elif key == "favs":
                tab_button(key, x, y, w, 24, short, "Starred destinations, last trip and a search of every runebook")
            else: tab_button(key, x, y, w, 24, short, tab_tip(key, title, short), title)
        top = tabs_bottom + Kit.GAP
        bg_box["parts"] += parchment(gump, 12, top, right - 12, LH() - BOTTOM_H - top, tgt["ctrls"], op)
        st["content_top"] = top + 4; return top + 4
    def scroll_area(x, y, w, h):
        sa = G.CreateGumpScrollArea(sc(x), sc(y), sc(w), sc(max(40, h))); tgt["ctrls"].append(sa); return sa
    def attach(ctrl): on_window(gump, ctrl); gump.Add(ctrl)
    def build_supplies(top):
        c = tgt["ctrls"]; x0 = LW() - SIDE_W - 12; bottom = LH() - BOTTOM_H
        bg_box["parts"] += parchment(gump, x0, top, SIDE_W, bottom - top, c, win["opacity"] / 100.0)
        label(gump, "Supplies", x0, top + 8, 15, COL_HEAD, c, width=SIDE_W, align="center")
        rows = [REAGENTS[a] for a in REAGENT_ORDER]
        rows += [None, ("Recall scroll", RECALL_SCROLL), ("Gate scroll", GATE_SCROLL)]; rh, pic = 40, 34
        need = sum(10 if r is None else rh for r in rows); y0 = top + 32
        if y0 + need <= bottom: parent, ox, oy, sa = gump, x0, y0, None
        else: sa = scroll_area(x0 + 2, y0, SIDE_W - 2, bottom - y0 - 4); parent, ox, oy = sa, 0, 0
        totals = supply_counts(); y = oy
        for r in rows:
            if r is None:
                box(parent, ox + 10, y + 4, SIDE_W - 20 - (16 if sa else 0), 1, COL_DIM, 0.6, c); y += 10; continue
            name, graphic = r; item_pic(parent, graphic, ox + 8, y + (rh - pic) // 2, pic, c)
            n = totals.get(graphic, 0)
            cnt = label(parent, count_text(n), ox + 48, y + 3, 15, COL_TEXT if n else COL_EMPTY, c)
            tgt["counts"].append(count_entry(graphic, cnt, n))
            label(parent, fit(name, SIDE_W - 52 - (16 if sa else 0)), ox + 48, y + 21, 12, COL_TEXT, c); y += rh
        if sa is not None: attach(sa)
    def build_spell_page(top, circle):
        c = tgt["ctrls"]; right = content_right(); x = 22; cw, ch = art_size(CIRCLE_ART); w = max(1, cw * 30 // ch)
        for i in range(8):
            p = pic_px(gump, CIRCLE_ART + i, sc(x), sc(top + 2), sc(w), sc(30), c, mouse=True)
            if circle != i: p.SetAlpha(0.45)
            on_click(p, queue_ui(("circle", i))); p.SetTooltip(CIRCLES[i][0]); x += w + 6
        title, spells = CIRCLES[circle]; label(gump, title, x + 10, top + 6, 18, COL_HEAD, c); top += 38
        if not spellbook_serial:
            label(gump, "No spellbook in your pack or hands. Carry one, then click Refresh.",
                  22, top + 4, 14, COL_DIM, c)
            return
        sa = scroll_area(16, top, right - 20, LH() - top - BOTTOM_H - 4); rh = 100; totals = supply_counts()
        base = circle * 8; row_w = right - 34; text_x = SPELL_ICON + 18; reg_x0 = row_w - 4 * REG_SLOT - 6
        mana = loop["mana"]
        for i, (name, desc, regs) in enumerate(spells):
            y = i * rh; owned = known_spells is None or norm(name) in known_spells; key = ("spell", name)
            bg = box(sa, 0, y, row_w, rh - 4, COL_ROW, ROW_A, c); row_bgs[key] = bg
            entry = [name, [REAGENTS[a][1] for a in regs.split()], SPELL_MANA[circle], None, None, bg, None]
            if owned: entry[6] = cast_state(entry, totals, mana)
            dim = owned and entry[6][0]
            icon = entry[4] = pic_px(sa, 0x08C0 + base + i, sc(8), sc(y + (rh - 4 - SPELL_ICON) // 2), sc(SPELL_ICON),
                                     sc(SPELL_ICON), c, hue=0 if owned else 0x3B2)
            if dim: icon.SetAlpha(DIM_ICON)
            entry[3] = label(sa, name, text_x, y + 14, 17, (COL_DIM if dim else COL_TEXT) if owned else COL_MUTED, c)
            label(sa, desc if owned else desc + "  (not in your book)", text_x, y + 38, 13,
                  COL_DIM if owned else COL_MUTED, c, width=max(120, reg_x0 - text_x - 8))
            reg_list = regs.split(); sx = row_w - len(reg_list) * REG_SLOT - 6
            for abbr in reg_list:
                full, graphic = REAGENTS[abbr]
                pic = item_pic(sa, graphic, sx + (REG_SLOT - REG_PIC) // 2, y + 2, REG_PIC, c)
                if not owned: pic.SetAlpha(0.4)
                n = totals.get(graphic, 0)
                cnt = label(sa, count_text(n), sx, y + REG_PIC + 3, 13,
                            (COL_TEXT if n else COL_EMPTY) if owned else COL_MUTED, c, width=REG_SLOT, align="center")
                tgt["counts"].append(count_entry(graphic, cnt, n, owned))
                label(sa, full, sx, y + REG_PIC + 20, 11, COL_DIM if owned else COL_MUTED, c,
                      width=REG_SLOT, align="center")
                sx += REG_SLOT
            if owned: bind_row(bg, key, ("cast", name)); bg.SetTooltip(cast_tip(entry)); tgt["spells"].append(entry)
        attach(sa)
    DIM_ICON = 0.45; REG_NAMES = dict((g_, n) for n, g_ in REAGENTS.values()); SPELL_MANA = Kit.SPELL_MANA
    def cast_state(entry, totals, mana):
        for g_ in entry[1]:
            if totals.get(g_, 0) <= 0: return (True, "Out of " + REG_NAMES.get(g_, "a reagent"))
        if mana is not None and mana < entry[2]: return (True, "Not enough mana (needs %d)" % entry[2])
        return (False, "")
    def cast_tip(entry):
        tip = "Double-click to cast " + entry[0]
        if entry[6] is not None and entry[6][0]: tip += "\n" + entry[6][1]
        return tip
    def refresh_castable():
        totals = loop["totals"]
        if totals is None: return
        mana = loop["mana"]
        for pg in list(pages.values()):
            for e in pg["spells"]:
                now = cast_state(e, totals, mana)
                if now == e[6]: continue
                e[6] = now; dim = now[0]; e[3].Hue = TEXT_HUES[COL_DIM if dim else COL_TEXT]
                e[4].SetAlpha(DIM_ICON if dim else 1.0); e[5].SetTooltip(cast_tip(e))
    def mana_tick(now):
        if (now < loop["next_mana"] and loop["next_mana"] - now <= MANA_EVERY) \
                or st["tab"] != "spells" or st["minimized"] or st["docked"]:
            return
        loop["next_mana"] = now + MANA_EVERY
        mana = int(API.Player.Mana); tier = sum(1 for m in SPELL_MANA if m <= mana); loop["mana"] = mana
        if tier != loop["tier"]: loop["tier"] = tier; refresh_castable()
    def charges_text(serial):
        cur, mx = book_charges.get(serial, (None, None))
        if cur is None: return None, 1
        if mx is None: return "Charges: %d" % cur, cur
        return "Charges: %d / %d" % (cur, mx), cur
    def build_rune_page(top, serial):
        c = tgt["ctrls"]; right = content_right(); book = next((b for b in runebooks if b["serial"] == serial), None)
        if book is None:
            if serial == st["tab"]: st["switch"] = "spells"
            return
        label(gump, book["title"], 22, top + 2, RUNE_TITLE_SIZE, COL_HEAD, c, smooth=True)
        button(right - 104, top + 4, 96, 26, "Re-read", "Read this runebook again",
               queue_ui(("reread", serial)), size=15, art=Kit.ART_PAGE)
        if serial not in rune_cache:
            label(gump, "Reading this runebook", 22, top + 36, 14, COL_DIM, c)
            if serial in bg_reads: bg_reads.remove(serial)
            if ("read", serial) not in st["queue"]: st["queue"].append(("read", serial))
            return
        text, charges = charges_text(serial)
        if text:
            label(gump, text, right - 340, top + 6, 20, COL_HEAD if charges and not book_low(serial) else COL_EMPTY, c,
                  width=226, align="right", smooth=True)
        dests = rune_cache[serial]
        if dests is None or (not dests and serial in rune_errors):
            msg = rune_errors.get(serial, "Couldn't read this runebook.")
            label(gump, msg, 22, top + 36, 14, COL_EMPTY, c, width=right - 26)
            label(gump, "Details saved to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder; send "
                        "that file, then click Refresh." if serial in dump["books"] else
                  "Click Re-read to save this book's details to Grimoire_runebook_dump.txt in "
                  "the VirtueAssistantSettings folder.", 22, top + 62, 12, COL_DIM, c, width=right - 26)
            return
        if not dests:
            label(gump, "No runes in this runebook. Add some, then click Re-read.", 22, top + 36, 14, COL_DIM, c)
            return
        totals = supply_counts(); tgt["scrolls"] = scroll_flags(totals)
        have_of = {"recall_scroll": totals.get(RECALL_SCROLL, 0),
                   "gate_scroll": totals.get(GATE_SCROLL, 0), "charge": charges}
        charges_known = book_charges.get(serial, (None, None))[0] is not None; n = len(dests)
        any_std = any(d["slot"] is not None for d in dests); any_btn = any_std or any(d.get("rune") for d in dests)
        label(gump, "%s; double-click a name to %s there" %
              (Kit.count(n, "destination"), DEFAULT_TRAVEL), 22, top + 36, RUNE_HEAD_SIZE, COL_DIM, c, smooth=True)
        aw = art_w(Kit.ART_PLAY); methods = []
        if any_btn:
            for m, head, tip in RUNE_METHODS:
                if m == "charge" and not any_std: continue
                methods.append((m, head, tip, max(aw + 12, ttf_w(head, RUNE_HEAD_SIZE) + 12)))
        block_w = sum(m[3] for m in methods); head_y = top + 62; list_y = head_y + 26; row_w = right - 34
        unit_min = 200 + block_w + 16; ncols = max(1, min(n, row_w // unit_min)); unit_w = row_w // ncols
        name_w = unit_w - block_w - 20; rows = (n + ncols - 1) // ncols; avail_h = LH() - list_y - BOTTOM_H - 4
        rh = max(36, min(54, avail_h // max(1, rows))); name_size = max(16, int((rh - 4) * 0.72))
        line_h = int(name_size * 1.3)
        for col in range(ncols):
            hx = 16 + col * unit_w + name_w + 16
            label(gump, "Destination", 16 + col * unit_w + 30, head_y, RUNE_HEAD_SIZE, COL_HEAD, c, smooth=True)
            for m, head, tip, cw in methods:
                col_color = COL_HEAD if have_of.get(m, 1) else COL_EMPTY
                label(gump, head, hx, head_y, RUNE_HEAD_SIZE, col_color, c, width=cw, align="center", smooth=True)
                hx += cw
        box(gump, 18, head_y + 23, row_w - 4, 1, COL_DIM, 0.5, c); sa = scroll_area(16, list_y, right - 20, avail_h)
        stars = tgt["stars"]
        for i, dest in enumerate(dests):
            col, r = divmod(i, rows); x0, y = col * unit_w, r * rh; key = ("rune", serial, dest["button"], dest["name"])
            bg = box(sa, x0, y, unit_w - 6, rh - 4, COL_ROW, ROW_A, c); row_bgs[key] = bg
            standard = dest["slot"] is not None; rune_bag = bool(dest.get("rune"))
            bind_row(bg, key, ("travel", serial, dest, default_method(dest)))
            bg.SetTooltip("Double-click to %s to %s" % (DEFAULT_TRAVEL, dest["name"]))
            stars[i] = star(sa, x0 + 8, y + max(0, (rh - 4 - 14) // 2), (serial, i) in favs["keys"], c)
            hit = box(sa, x0 + 2, y, 26, rh - 4, COL_ROW, 0.0, c)
            on_click(hit, queue_ui(("star", serial, i, dest["name"]))); hit.SetTooltip(STAR_TIP)
            ty = y + max(0, (rh - 4 - line_h) // 2)
            if not (standard or rune_bag):
                label(sa, fit(dest["name"], unit_w - 46, name_size), x0 + 30, ty, name_size, COL_TEXT, c, smooth=True)
                continue
            label(sa, fit(dest["name"], name_w - 24, name_size), x0 + 30, ty, name_size, COL_TEXT, c, smooth=True)
            bx = x0 + name_w + 16
            for m, head, tip, cw in methods:
                if m == "charge" and not standard: bx += cw; continue
                have = have_of.get(m, 1); full_tip = tip
                if m in ("recall_scroll", "gate_scroll"): full_tip += " (%d carried)" % have
                elif m == "charge" and charges_known: full_tip += " (%d left)" % have
                b = button(bx + (cw - aw) // 2, y + 2, aw, rh - 8, "", full_tip,
                           queue_stamped(("travel", serial, dest, m)), parent=sa)
                if not have: b.SetAlpha(0.35)
                bx += cw
        attach(sa)
    def default_method(dest): return DEFAULT_TRAVEL if dest["slot"] is not None or dest.get("rune") else "charge"
    STAR_TIP = "Add to Favourites (click again to remove)"
    METHOD_VERB = {"recall": "recall", "gate": "gate", "charge": "recall (a charge)",
                   "recall_scroll": "recall (a scroll)", "gate_scroll": "gate (a scroll)",
                   "sacred": "travel (Sacred Journey)"}
    def build_fav_page(top):
        c = tgt["ctrls"]; right = content_right()
        label(gump, "Favourites", 22, top + 2, RUNE_TITLE_SIZE, COL_HEAD, c, smooth=True); sw = 220; sx = right - 8 - sw
        cap = "Search:"; label(gump, cap, sx - 10 - text_w(cap), top + 8, 14, COL_TEXT, c)
        tiled_px(gump, Kit.FIELD_TILE, sc(sx) - 2, sc(top + 4) - 1, sc(sw) + 4, 24, c)
        tb = G.CreateGumpTextBox(fav_ui["text"], sc(sw), 22, False, 16); tb.SetPos(sc(sx), sc(top + 4))
        Kit.with_tip(tb, "Search every runebook you carry by rune or book name (empty: your Favourites)")
        put(gump, tb, c); info = label(gump, "", 22, top + 38, 14, COL_DIM, c); list_y = top + 62; row_w = right - 34
        sa = scroll_area(16, list_y, right - 20, LH() - list_y - BOTTOM_H - 4)
        fav_ui.update({"layer": tgt, "tb": tb, "info": info, "sa": sa, "pool": [], "seen": None, "ver": -1,
                       "row_w": row_w, "name_w": max(120, int(row_w * 0.55)), "info_w": right - 30})
        fav_render(building=True); attach(sa)
    def fav_rows():
        titles = dict((b["serial"], b["title"]) for b in runebooks); order = [b["serial"] for b in runebooks]
        if not order: return [], "No runebooks in your pack or hands."
        q = fav_ui["text"].strip().lower(); rows = []
        if q:
            words = q.split(); more = False
            for s in order:
                lst = rune_cache.get(s) or (); tl = titles[s].lower()
                for i in range(len(lst)):
                    hay = lst[i]["name"].lower() + "  " + tl
                    if all(wd in hay for wd in words):
                        if len(rows) >= SEARCH_MAX: more = True; break
                        rows.append((s, i, lst[i]["name"], titles[s], None, False))
                if more: break
            if more: return rows, "More than %d found; type more letters." % SEARCH_MAX
            if rows:
                return rows, "%s found; double-click one to %s there" % (
                    Kit.count(len(rows), "destination"), DEFAULT_TRAVEL)
            return rows, "No rune or runebook name has '%s' in it." % fav_ui["text"].strip()
        last = favs["last"]
        if last is not None and last[0] in titles:
            i = resolve(last[0], last[1], last[2])
            if i is not None: rows.append((last[0], i, last[2], titles[last[0]], last[3], True))
        by_book = {}
        for f in favs["list"]: by_book.setdefault(f[0], []).append(f)
        away = 0
        for s in list(by_book):
            if s not in titles: away += len(by_book.pop(s))
        n = 0
        for s in order:
            for f in sorted(by_book.get(s, ()), key=lambda f: f[1]):
                i = resolve(s, f[1], f[2])
                if i is None: away += 1; continue
                rows.append((s, i, f[2], titles[s], None, False)); n += 1
        if n:
            info = "%s; double-click one to %s there, or type above to search" % (
                Kit.count(n, "favourite"), DEFAULT_TRAVEL)
        else: info = "Click a destination's star on a runebook page to list it here."
        if away: info += "  (%d not in the books you carry)" % away
        return rows[:SEARCH_MAX + 1], info
    def fav_render(building=False):
        ui = fav_ui; layer = ui["layer"]
        if layer is None or (pages.get("favs") is not layer and not building): ui["layer"] = None; return
        rows, info = fav_rows(); ui["ver"], ui["seen"] = lists["ver"], ui["text"]
        Kit.set_text(ui["info"], fit(info, ui["info_w"]), TEXT_HUES[COL_DIM]); pool = ui["pool"]
        for i in range(len(rows)):
            if i >= len(pool): pool.append(new_fav_slot(i, rows[i]))
            fav_assign(pool[i], rows[i])
        for i in range(len(rows), len(pool)): fav_assign(pool[i], None)
    def new_fav_slot(i, row):
        ui = fav_ui; sa, track, rh = ui["sa"], ui["layer"]["ctrls"], 30; y = i * rh
        slot = {"i": i, "a": None, "prev": None, "at": 0.0, "tip": None, "shown": True}
        slot["bg"] = box(sa, 0, y, ui["row_w"], rh - 4, COL_ROW, ROW_A, track); row_bgs[("fav", i)] = slot["bg"]
        slot["on"] = (row[0], row[1]) in favs["keys"]
        slot["star"] = star(sa, 8, y + (rh - 4 - 14) // 2, slot["on"], track)
        slot["hit"] = box(sa, 2, y, 26, rh - 4, COL_ROW, 0.0, track); slot["hit"].SetTooltip(STAR_TIP)
        slot["name"] = label(sa, "", 32, y + (rh - 4 - 14) // 2 - 2, 14, COL_TEXT, track)
        slot["book"] = label(sa, "", 32 + ui["name_w"] + 10, y + (rh - 4 - 14) // 2 - 2, 14, COL_DIM, track)
        on_click(slot["hit"], fav_cb(slot, lambda a: queue_ui(("star", a[0], a[1], a[2]))()))
        on_click(slot["bg"], fav_cb(slot, lambda a: make_row_click(("fav", slot["i"]), ("favgo",) + a)()))
        hook_double_click(slot["bg"], fav_cb(slot, lambda a: st["queue"].append(stamped(("favgo",) + a)))); return slot
    def fav_show(slot, shown):
        slot["shown"] = shown
        for ctl in [slot["bg"], slot["hit"], slot["name"], slot["book"]] + slot["star"]: ctl.IsVisible = shown
    def fav_assign(slot, row):
        if row is None:
            if slot["a"] is not None: slot["prev"], slot["at"], slot["a"] = slot["a"], time.time(), None
            if slot["shown"]: fav_show(slot, False)
            return
        a = (row[0], row[1], row[2], row[4], row[5])
        if slot["a"] != a: slot["prev"], slot["at"], slot["a"] = slot["a"], time.time(), a
        if not slot["shown"]: fav_show(slot, True)
        ui = fav_ui
        Kit.set_text(slot["name"], fit(("Last: " if row[5] else "") + row[2], ui["name_w"] - 4), TEXT_HUES[COL_TEXT])
        book = row[3] + ((", " + METHOD_VERB.get(row[4], row[4])) if row[4] else "")
        Kit.set_text(slot["book"], fit(book, ui["row_w"] - ui["name_w"] - 46), TEXT_HUES[COL_DIM])
        on = (row[0], row[1]) in favs["keys"]
        if on != slot["on"]: recolor_star(slot["star"], on); slot["on"] = on
        lst = rune_cache.get(row[0]) or ()
        m = row[4] or (default_method(lst[row[1]]) if row[1] < len(lst) else DEFAULT_TRAVEL)
        tip = "Double-click to %s to %s (%s)" % (METHOD_VERB.get(m, m), row[2], row[3])
        if tip != slot["tip"]: slot["tip"] = tip; Kit.with_tip(slot["bg"], tip)
    def fav_cb(slot, go):
        def cb():
            a = slot["prev"] if slot["prev"] is not None and time.time() - slot["at"] < 0.15 else slot["a"]
            if a is not None: go(a)
        return cb
    def fav_tick(now):
        ui = fav_ui
        if ui["layer"] is None: return
        if pages.get("favs") is not ui["layer"]: ui["layer"] = None; return
        if st["tab"] != "favs" or st["minimized"] or st["docked"]: return
        if now >= ui["next"] or ui["next"] - now > SEARCH_EVERY:
            ui["next"] = now + SEARCH_EVERY; ui["text"] = str(ui["tb"].Text or "")
        if ui["text"] != ui["seen"] or ui["ver"] != lists["ver"]: fav_render()
    def fav_travel(act):
        serial, index, name, method = act[1], act[2], act[3], act[4]; i = resolve(serial, index, name)
        if i is None: say("%s isn't in that runebook any more." % name, Kit.HUE_BAD); return None
        dest = rune_cache[serial][i]; return ("travel", serial, dest, method or default_method(dest))
    def page_key(tab): return ("spells", st["circle"]) if tab == "spells" else tab
    def build_page(key, hidden):
        nonlocal tgt; old = pages.pop(key, None); pg = tgt = new_layer(hidden)
        try:
            if isinstance(key, tuple): build_spell_page(st["content_top"], key[1])
            elif key == "favs": build_fav_page(st["content_top"])
            else: build_rune_page(st["content_top"], key)
        finally: tgt = frame
        pages[key] = pg
        if old is not None: clear(old["ctrls"])
        return pg
    def drop_page(key):
        if st["minimized"] or st["dirty"]:
            if key in pages: clear(pages.pop(key)["ctrls"])
            return
        build_page(key, key != page_key(st["tab"]))
    def all_page_keys():
        keys = [("spells", i) for i in range(len(CIRCLES))]
        if runebooks: keys.append("favs")
        keys += [b["serial"] for b in runebooks if b["serial"] in rune_cache]; return keys
    def switch_page(tab, change=None):
        prev = page_key(st["tab"])
        if change: change()
        st["tab"] = tab; save_int("Tab", 0 if tab == "spells" else (TAB_FAVS if tab == "favs" else tab))
        save_int("Circle", st["circle"])
        if tab == "spells": loop["next_mana"] = 0.0
        key = page_key(tab)
        if key == prev and key in pages and not pages[key]["hidden"]: return
        click_state["selected"] = None
        if prev in pages: show_layer(pages[prev], False)
        if key in pages: show_layer(pages[key], True)
        else: build_page(key, False)
    def switch_tab(key):
        for k, mark in tab_marks.items(): mark.SetAlpha(1.0 if k == key else 0.0)
        switch_page(key)
    def prebuild_next():
        if st["minimized"]: return False
        missing = [k for k in all_page_keys() if k not in pages]
        if missing: build_page(missing[0], missing[0] != page_key(st["tab"]))
        loop["next_prebuild"] = time.time() + PREBUILD_EVERY; return bool(missing)
    def rebuild():
        old = frame["ctrls"][:]
        for k in ("ctrls", "tops", "counts"): del frame[k][:]
        old_pages = list(pages.values())
        for d in (pages, row_bgs, tab_marks): d.clear()
        click_state["selected"] = None; st["dirty"] = False; top = build_chrome()
        if not st["minimized"]:
            build_supplies(top); build_tabs(top); label(gump, st["status"], 30, LH() - 35, 12, COL_DIM, frame["ctrls"])
            build_page(page_key(st["tab"]), False); loop["next_prebuild"] = time.time() + PREBUILD_EVERY
        clear(old)
        for pg in old_pages: clear(pg["ctrls"])
    def scan_all(full=False, bags=True):
        nonlocal spellbook_serial, known_spells; saved_data(); load_favs()
        spellbook_serial = Kit.on_client(find_spellbook); known_spells = load_known_spells(force=full)
        Kit.on_client(lambda: scan_books(full, bags))
    def scan_books(full, bags):
        nonlocal runebooks; runebooks = find_runebooks(); del bg_reads[:]
        for b in runebooks:
            s = b["serial"]; have = s in rune_cache or load_book(s)
            if full or not have: bg_reads.append(s)
            if have and s not in charge_seen: charge_seen[s] = book_charges.get(s, (None, None))[0]
            if have and rune_cache.get(s): rekey_favs(s)
        lists["ver"] += 1; want = st.pop("want_tab", None)
        if want and (any(b["serial"] == want for b in runebooks) or (want == TAB_FAVS and runebooks)):
            st["tab"] = "favs" if want == TAB_FAVS else want
        if st["tab"] in bg_reads: bg_reads.remove(st["tab"]); bg_reads.insert(0, st["tab"])
        if (st["tab"] == "favs" and not runebooks) or (st["tab"] not in ("favs", "spells")
                                                       and not any(b["serial"] == st["tab"] for b in runebooks)):
            st["tab"] = "spells"
        count = ("All spells shown" if known_spells is None else "%d spells known" % len(known_spells))
        st["status"] = "%s, %s" % (count if spellbook_serial else "No spellbook", Kit.count(len(runebooks), "runebook"))
        if not runebooks and bags and (full or not st["reported"]): report_books(); st["reported"] = True
        st["scanned"] = True; st["dirty"] = True
    def read_and_store(serial):
        dests, charges = read_runebook(serial)
        if store_book(serial, dests, charges): Kit.on_client(lambda: drop_page(serial))
    def on_close(): st["closed"] = True
    CONFIG_PAGE = (("WINDOW", (
        ("slider", "opacity", "Background opacity:", "How solid the stone and black backdrop are (0-100, 0 = "
         "see-through)", 0, 100),
        ("slider", "scale", "Scale:", "Size of everything in the window (%d-%d%%, applied when the slider stops)"
         % (SCALE_MIN, SCALE_MAX), SCALE_MIN, SCALE_MAX),
        ("note", "Drag a window corner to resize.", {"ndy": 2})), {"sh": 124}),)
    CONFIG_OPTS = {"top": 34, "fh": 30, "ldy": 0, "sdy": 4, "lw": 178, "sw": 200, "ugap": 12, "vfmt": "%d%%"}
    page_vals = {"opacity": DEFAULT_OPACITY, "scale": 100, "loaded": False}
    def page_change(old, new):
        if new["opacity"] != old["opacity"]: on_opacity(new["opacity"])
        if new["scale"] != old["scale"]:
            on_scale(new["scale"])
            if not Kit.is_open(gump): apply_scale()
    cfg = Kit.Page(page_vals, CONFIG_PAGE, None, page_change, CONFIG_OPTS)
    def build_config(g, x, y, w):
        if not page_vals["loaded"] and not Kit.is_open(gump): page_vals["loaded"] = True; load_window_prefs()
        page_vals.update({"opacity": win["opacity"], "scale": int(round(view["scale"] * 100))}); cfg.build(g, x, y, w)
    loop = {}; trip = {}; jobs = []; cast = {"rd": None, "me": ""}; cleanup = Kit.Cleanup()
    def reset_state():
        nonlocal tgt
        st.update({"tab": "spells", "circle": 0, "dirty": True, "closed": False, "queue": [("scan",)], "ui_queue": [],
                   "status": "Reading your books", "minimized": False, "switch": None, "content_top": 0,
                   "shutting": False, "scanned": False, "reported": False, "docked": False, "link_state": None,
                   "pick": None})
        for k in ("ctrls", "tops", "counts"): del frame[k][:]
        for d in (pages, row_bgs, tab_marks, tab_parts, _uo_meta, charge_seen, rb_seen): d.clear()
        for lst in (jobs, bg_reads, charge_news): del lst[:]
        tgt = frame; bg_box["parts"] = []
        loop.update({"next_count": 0.0, "next_prebuild": 0.0, "last_pos": (None, None), "held": None, "totals": None,
                     "settle": 0.0, "size_dirty": False, "mana": None, "tier": None, "next_mana": 0.0})
        trip["busy"], trip["at"] = False, 0.0
        fav_ui.update({"layer": None, "tb": None, "info": None, "sa": None, "pool": [],
                       "text": "", "seen": None, "ver": -1, "next": 0.0})
        lists["ver"] += 1; lists["dest_ver"] = -1; cast.update({"wait": None, "claim": 0.0, "seen": False, "next": 0.0})
        dump.update({"written": False, "armed": False}); rb_types.clear(); rb_types.update(load_rb_types())
    def layout_state():
        if st["closed"] or st["shutting"] or not Kit.is_open(gump): return None
        return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")
    def _start():
        reset_state(); fitst["own"] = None; load_window_prefs()
        st["circle"] = max(0, min(len(CIRCLES) - 1, load_int("Circle", 0))); st["want_tab"] = load_int("Tab", 0) or None
        create_window(); G.AddControlOnDisposed(gump, on_close); G.AddGump(gump); Kit.on_moved(gump, save_window_pos)
        HOST.layout_add(KEY, lambda: gump, TITLE, {"fit": layout_fit, "state": layout_state, "exact": True})
        cleanup.add(HOST.layout_remove, KEY); fitst["own"], fitst["told"] = None, None
        if load_int("Min", 0) == 1 or HOST.dock_wanted(KEY): toggle_min()
        API.RemoveSharedVar(LINK_CMD); link_tick()
        HOST.alert_kind("grimoire.charges", "Runebook low on charges", 0x1EA)
        for name, fn in SERVICES.items(): cleanup.service(name, fn)
    def run_ui_action(act):
        kind = act[0]
        if kind == "min_click": min_click()
        elif kind == "circle":
            i = act[1]
            if ("spells", i) in pages and not st["dirty"]: go_circle(i)
            else: st["switch"] = ("spells", i)
        elif kind == "settings": HOST.show_settings(KEY)
        elif kind == "fit": run_fit(act[1], act[2])
        elif kind == "close": Kit.dispose(gump)
        elif kind == "reread": dump["armed"] = True; st["queue"].append(("read", act[1]))
        elif kind == "star":
            serial, i = act[1], act[2]; on = toggle_fav(serial, i, act[3])
            if on is None: return
            pg = pages.get(serial); parts = pg["stars"].get(i) if pg is not None else None
            if parts is not None: recolor_star(parts, on)
    def start_cast(name):
        now = time.time()
        if name in NO_TARGET_SPELLS: API.CastSpell(name); bg["hold"] = now + CAST_HOLD; return
        HOST.claim_cursor(KEY, CAST_CLAIM)
        cast.update({"claim": now + CAST_CLAIM, "seen": False, "next": now + 0.1, "rd": Journal.reader(),
                     "me": player_name()})
        API.CastSpell(name); bg["hold"] = now + CAST_HOLD
    def end_cast(): cast["claim"], cast["rd"] = 0.0, None; HOST.release_cursor(KEY)
    def watch_cast(now):
        if now >= cast["claim"]: end_cast(); return
        if now < cast["next"]: return
        cast["next"] = now + 0.1
        if API.HasTarget(): cast["seen"] = True
        elif cast["seen"] or failure_in(cast["rd"].new(), CAST_FAIL_TEXTS, cast["me"]): end_cast()
    def cursor_up_now(now):
        if API.HasTarget("any"): bg["cursor_next"] = now + 0.25; return True
        return False
    def _tick():
        if st["closed"]:
            if not st["shutting"]: HOST.disable(KEY)
            return
        now = time.time()
        if pending_scale["value"] is not None and now - pending_scale["t"] >= 0.4: apply_scale()
        link_tick()
        while st["ui_queue"]:
            run_ui_action(st["ui_queue"].pop(0))
            if st["closed"]: return
        if now >= loop["settle"]:
            if loop["size_dirty"]: save_size()
            if st["dirty"]: rebuild()
        if st["switch"] is not None:
            key, st["switch"] = st["switch"], None
            if isinstance(key, tuple): go_circle(key[1])
            else: switch_tab(key)
            if st["dirty"]: rebuild()
        if charge_news: charges_tick()
        if cast["claim"]: watch_cast(now)
        if cast["wait"] is not None:
            name, until = cast["wait"]
            if not cursor_taken(): cast["wait"] = None; start_cast(name)
            elif now >= until:
                cast["wait"] = None; say("%s was not cast; the target cursor stayed in use." % name, Kit.HUE_BAD)
        if jobs: pass
        elif st["queue"]:
            act = st["queue"].pop(0)
            if act[0] == "pressed":
                if 0 <= now - act[1] <= 3.0: act = act[2]
                else:
                    say("trip not made; Grimoire was busy with a runebook. Press it again.", Kit.HUE_INFO)
                    act = ("dropped",)
            kind = act[0]
            if kind == "cast":
                if len(act) > 2 and now - act[2] > CAST_DEFER:
                    say("%s was not cast; Grimoire was busy with a runebook." % act[1], Kit.HUE_INFO)
                elif cast["wait"] is not None: pass
                elif cursor_taken():
                    cast["wait"] = (act[1], now + CAST_DEFER)
                    say("target cursor in use; %s is cast once it is free." % act[1], Kit.HUE_INFO)
                else: start_cast(act[1])
            elif kind == "read":
                if act[1] in bg_reads: bg_reads.remove(act[1])
                if now < bg["hold"] or st["pick"] is not None or cast["claim"] \
                        or cast["wait"] is not None or cursor_taken() or API.HasTarget("any"):
                    bg_reads.insert(0, act[1])
                else: jobs.append(act)
            elif kind in ("travel", "scan", "rescan", "refresh"):
                if kind == "refresh": dump["armed"] = True
                jobs.append(act)
            elif kind == "favgo":
                job = fav_travel(act)
                if job is not None: jobs.append(job)
            elif kind == "register": register_runebook()
            elif kind == "registered":
                if registered(act[1]): st["queue"].insert(0, ("scan",))
        elif bg_reads and now >= bg["hold"] and st["pick"] is None \
                and cast["claim"] == 0.0 and cast["wait"] is None and not cursor_taken() \
                and now >= bg.get("cursor_next", 0.0) and not cursor_up_now(now):
            jobs.append(("read", bg_reads.pop(0)))
        if not jobs and not st["dirty"] and st["switch"] is None and now >= loop["next_prebuild"]: prebuild_next()
        if st["closed"]: return
        if now >= loop["next_count"]: refresh_counts(); watch_hands(); loop["next_count"] = time.time() + 1.5
        mana_tick(now); fav_tick(now)
    def charges_tick():
        while charge_news:
            serial = charge_news.pop(0); cur = book_charges.get(serial, (None, None))[0]; prev = charge_seen.get(serial)
            charge_seen[serial] = cur; low = book_low(serial); was_low = prev is not None and prev < LOW_CHARGES
            if low and not was_low:
                title = next((b["title"] for b in runebooks if b["serial"] == serial), "A runebook")
                left = "%s left" % Kit.count(cur, "charge")
                HOST.alert("grimoire.charges", "%s: %s" % (title, left), who=serial)
            recolor_tab(serial)
    def travel_pending():
        return (trip["busy"] or time.time() - trip["at"] < 2.0 or any(a[0] == "travel" for a in jobs)
                or any(a[0] in ("travel", "favgo") or (a[0] == "pressed" and a[2][0] in ("travel", "favgo"))
                       for a in st["queue"]))
    def svc_travel(book_serial, rune_index, method, name=None):
        if st["shutting"] or st["closed"]: return False
        if method not in TRAVEL_METHODS: say("no way to travel called '%s'." % method, Kit.HUE_BAD); return False
        try: serial, index = int(book_serial), int(rune_index)
        except (TypeError, ValueError): return False
        if not st["scanned"]:
            say("still finding your runebooks; try again shortly.", Kit.HUE_INFO); return False
        title = next((b["title"] for b in runebooks if b["serial"] == serial), None)
        if title is None: say("that runebook isn't in your pack or hands.", Kit.HUE_BAD); return False
        try: dest = rune_cache[serial][resolve(serial, index, name)]
        except (KeyError, IndexError, TypeError): dest = None
        if dest is None: say("%s isn't in %s any more." % (name or "that rune", title), Kit.HUE_BAD); return False
        if method == "charge" and dest.get("rune"):
            say("%s has no charges to use; pick Recall instead." % title, Kit.HUE_BAD); return False
        if method in ("gate", "sacred") and dest.get("slot") is None and not dest.get("rune"):
            say("%s has its own layout; only its rune's own button works there, not %s."
                % (title, "Gate Travel" if method == "gate" else "Sacred Journey"), Kit.HUE_BAD)
            return False
        if travel_pending(): say("a trip is already on its way.", Kit.HUE_INFO); return False
        st["queue"].append(("travel", serial, dest, method)); return True
    def svc_destinations():
        if lists["dest_ver"] != lists["ver"]:
            lists["dests"] = [{"book": b["serial"], "book_name": b["title"], "index": i, "name": d["name"],
                               "charges": book_charges.get(b["serial"], (None, None))[0]}
                              for b in runebooks for i, d in enumerate(rune_cache.get(b["serial"]) or ())]
            lists["dest_ver"] = lists["ver"]
        return list(lists["dests"])
    def svc_book_charges():
        if lists.get("chg_ver") != lists["ver"]:
            lists["charges"] = dict((b["serial"], book_charges.get(b["serial"], (None, None))[0]) for b in runebooks
                                    if rune_cache.get(b["serial"]))
            lists["chg_ver"] = lists["ver"]
        return lists["charges"]
    SERVICES = {"grimoire.travel": svc_travel, "grimoire.destinations": svc_destinations,
                "grimoire.book_charges": svc_book_charges}
    def _thread_tick():
        try: _thread_work()
        finally: flush_saved()
    def thread_wanted(): return bool(jobs or favs["save"] or favs["save_last"] or saved["dirty"])
    def _thread_work():
        if st["closed"]: return
        if favs["save"] or favs["save_last"]: save_favs()
        if not jobs: return
        act = jobs[0]; kind = act[0]
        if kind == "travel": trip["busy"], trip["at"] = True, time.time()
        jobs.pop(0)
        if kind == "travel":
            try: note_trip(act[1], act[2], act[3]); save_favs(); travel(act[1], act[2], act[3])
            finally: trip["busy"] = False
            bg["hold"] = time.time() + 6.0
        elif kind == "read":
            if API.HasTarget("any"):
                if act[1] in bg_reads: bg_reads.remove(act[1])
                bg_reads.insert(0, act[1]); return
            read_and_store(act[1]); bg["hold"] = max(bg["hold"], time.time() + 0.55)
        else: scan_all(full=kind == "refresh", bags=kind != "rescan")
    _hand_names = {}
    def _held_book(it, look_names):
        g = it.Graphic
        if g in BOOKISH: return True
        h = it.Hue
        if (g, h) in rb_types: return True
        key = (it.Serial, g, h); hit = None if look_names else _hand_names.get(key)
        if hit is None:
            n = it.Name; hit = is_runebook_v(g, h, n)
            if n:
                if len(_hand_names) > 200: _hand_names.clear()
                _hand_names[key] = hit
        return hit
    def watch_hands():
        loop["hand_looks"] = n = loop.get("hand_looks", 0) + 1; look_names = n % 10 == 0
        held = sorted(it.Serial for it in held_items() if _held_book(it, look_names))
        if loop["held"] is not None and held != loop["held"] and ("rescan",) not in st["queue"]:
            st["queue"].append(("rescan",))
        loop["held"] = held
    def _stop():
        st["shutting"] = True; cleanup.close(); save_favs(); flush_saved(); st["docked"], st["link_state"] = False, None
        API.SetSharedVar(LINK_STATE, "off"); HOST.release_cursor(KEY)
        cast.update({"wait": None, "claim": 0.0, "seen": False, "rd": None})
        def keep_place():
            if Kit.is_open(gump): save_window_pos(); return True
            return False
        placed = Kit.on_client(keep_place)
        if not placed and loop["last_pos"][0] is not None:
            for k, v in zip(("X", "Y"), loop["last_pos"]): save_int(k, v)
        if loop["size_dirty"]: save_size()
        if Kit.is_open(gump): Kit.dispose(gump)
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "thread_tick": _thread_tick,
              "thread_wanted": thread_wanted, "config_height": cfg.height, "build_config": build_config,
              "poll_config": cfg.poll, "config_closed": cfg.closed}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("grimoire", "Grimoire", "Spellbook, runebooks and reagents", _module_grimoire, 0.05, category="Your things")
