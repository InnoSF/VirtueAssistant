# =============================================================================
# Virtue Assistant - TazUO Legion Script Manager (Python), shard In Mani Ylem
#
# The mother script. It holds the Virtue Assistant window (the Modules and Settings tabs), the
# shared look and helpers every window is built with (Kit), window snapping, the layout of zones
# round the game area, profiles, alerts, the guard-zone and hostile-near holds, and the main loop
# (HOST). Every module is its own file in the VirtueAssistantModules folder beside this script. A
# module file is run inside this script's namespace, so it sees everything defined here (API, G,
# safe, Client, Kit, HOST ...), and its last lines register it with the host (HOST.add). A module file
# cannot run on its own.
#
# Modules (files in the VirtueAssistantModules folder):
#
#    ActionBarModule.py       Action Bar       cells for items, spells, skills and windows, with hotkeys
#    CharacterHudModule.py    Character HUD    frames, timers and bars for you and your pets
#    InventoryModule.py       Inventory        bags, paperdoll, storage, restock and supplies
#    GrimoireModule.py        Grimoire         spellbook, runebooks and reagents
#    WorldMapModule.py        World Map        pings, corpse, dig and dry spots, traps, on the map
#    UltimaTrackerModule.py   Ultima Tracker   friends, foes and neutrals near you
#    SocialModule.py          Social           friends, party, guild and profile
#    SkillsModule.py          Skills           skills, training and AFK alarms
#    PropertyButlerModule.py  Property Butler  house sweeps, visitors, eject and ban
#    MetersModule.py          Meters           damage, healing, loot and gold meters
#    MongotchiModule.py       Mongotchi        a pet mongbat to raise and dress up
#
# Five of the modules are made of parts: a part is one feature with its own box under the module's
# row on the Modules tab, and a part that is off costs nothing. The Modules tab search also finds
# the older module names. Every saved setting, window place, list and file keeps its key, so nothing
# is lost moving between versions.
#
# A file taken out of the folder leaves that module out. A new file whose name ends in Module.py,
# dropped in the folder, is loaded too, after the ones above. Any other folder beside this script
# whose name starts with VirtueAssistant and ends with Modules is loaded the same way.
#
# Everything Virtue Assistant saves to disk (lists, layouts, exports, profiles) is kept in the
# VirtueAssistantSettings folder beside this script (Kit.data_path), made on the first start.
# Per-character values (window places, which modules are on) are kept with Kit.get_var / put_var.
#
# Every window uses the client's own gump art (the stone frame, the black sections, the UO font in
# client hues and the standard gump buttons); the art ids are in the Kit class. Every window snaps
# to the others when dragged and moves with the window it snapped to. A window can be minimized to
# its own small form or folded into the Action Bar's tray. Hotkeys never fire while the player is
# typing in any text field (Client.typing).
#
# Profiles are a copy of one character's whole setup that any other character can load: the
# modules' settings and window places, which modules are on, the Bags layout and TazUO's own
# settings. Things tied to one character's own items stay with that character.
#
# Layout of this file, top to bottom: constants, the small client helpers (Client, Typing, Follow),
# Kit, then the engines (Fill, Alerts, Guard, Snap, Layout, Profiles), the Host and its windows, and
# the module loader at the bottom.
# =============================================================================
import API
import math
import os
import re
import struct
import time
# The app name shown in titles and journal lines, and the version the patch notes and the
# What's new window go by. The script file is named after the version.
APP_NAME = "Virtue Assistant"
APP_VERSION = "2.7.0.38"
# The folder of module files, beside this script.
MODULE_DIR = "VirtueAssistantModules"
# The folder every saved file goes in, beside this script (Kit.data_dir).
SETTINGS_DIR = "VirtueAssistantSettings"
SETTINGS_KEY = "VirtueAssistant_settings"
VA_ALONE = "VA_ALONE" in globals() and "_VA_INNER" not in globals()
START_AT = (globals().get("_VA_INNER") or [time.time()])[0]
# Shared-variable key the suite keeps fresh once a second, so another script can tell it is running.
ALIVE_KEY = "VirtueAssistant_alive"
START_KEY = "VirtueAssistant_starting"
# Per-character key (one per module) holding the parts a module had on when run alone.
ALONE_PARTS = "VirtueAssistant_alone_parts_%s"
# Seconds between passes of the main loop.
HOST_TICK = 0.02
# Seconds between looks at the script's own windows.
UI_TICK = 0.05
# Seconds between those looks once the player has been idle for UI_IDLE_AFTER seconds.
UI_IDLE = 0.12
UI_IDLE_AFTER = 2.0
# Pixels between the lines of the screen grid.
GRID_DEFAULT = 32
# Pixels within which a let-go window snaps to a screen anchor.
SNAP_ANCHOR = 40
# Seconds between looks for a window that is off the screen (the keeper pass).
KEEP_EVERY = 0.5
# Seconds between full keeper passes when nothing has changed in between.
KEEP_SWEEP = 2.0
# Folder, inside the settings folder, that holds the saved profiles.
PROFILE_DIR = "VirtueAssistantProfiles"
# Per-character key: which profile this character follows.
PROFILE_STATE_KEY = "VirtueAssistant_profile"
# Longest profile name, in characters.
PROFILE_NAME_MAX = 32
# Seconds: the same alert (key plus who, or key plus text) shows at most this often.
ALERT_RATE = 10.0
# Seconds a warn or info banner stays up; an alarm waits for a click.
ALERT_HOLD = 8.0
# Seconds between two alert sounds, so a burst plays them in turn.
ALERT_SOUND_GAP = 0.4
# Seconds between the flashes of an alarm banner.
ALERT_FLASH = 0.5
# Sounds offered on Settings > Alerts: (name, client sound id). Id 0 is silent.
ALERT_SOUNDS = (("Silent", 0), ("Chime", 0x1EA), ("Harp note", 0x3D0), ("Lever", 0x04A), ("Whistle", 0x335),
    ("Yell", 0x338), ("War drum", 0x2E7), ("Trap snap", 0x1EF), ("Boom", 0x307), ("Recall", 0x1FC),
    ("Heal tone", 0x202), ("Bird", 0x017), ("Smack", 0x3B2), ("Harm", 0x1F1), ("Cure", 0x1E0))
# Lower-case journal lines that mean the player has entered or left a guarded town.
GUARD_IN_TEXTS = ("you are now under the protection of the town guards",)
GUARD_OUT_TEXTS = ("you have left the protection of the town guards",
                   "beware! you have left the protection of the town guards")
# Optional hand-filled guard areas, (facet, x1, y1, x2, y2, name). Used only while the guard state
# is not known yet. Empty until the town bounds are filled in.
GUARD_AREAS = ()
# Tiles: a saved guard state counts while the player stands this close to where it was seen.
GUARD_SPOT = 3
# Tiles: a hostile this close holds every loop that acts by itself (R3: one fight test, shared).
FOE_RANGE = 12
# Seconds between two looks at the mobiles around the player (shared by every loop).
FOE_EVERY = 1.0
# Notoriety values (API.Notoriety) that always count as hostile: enemy and murderer.
FOE_NOTO = (5, 6)
# Notoriety values that count as hostile only in war mode: grey (attackable) and criminal.
FOE_WAR_NOTO = (3, 4)
# Seconds a loop stays held after the player's hit points dropped.
HURT_SECS = 10.0
# A module that raises this many errors within ERROR_SECS is switched off.
MAX_MODULE_ERRORS = 25
# Window of seconds in which a module's errors are counted.
ERROR_SECS = 60.0
# Longest time, in seconds, a loop may wait for a server gump it is expecting.
GUMP_EXPECT_MAX = 30.0
# Hue of the journal lines that report an attack on the player.
ATTACK_HUE = 0x22
# Seconds within which a second press on the same target confirms a harmful action in a guard zone.
HARM_SECS = 3.0
# Seconds under which a second press counts as the same press and does not confirm.
HARM_DOUBLE = 0.6
# Notoriety names (blue, green, odd targets) that need that second press in a guard zone.
HARM_NOTO = ("innocent", "ally", "odd")
# The wait reason each hold shows in status lines and the journal.
HOLD_TEXT = {"dead": "you are dead", "war": "war mode", "hurt": "you took damage", "foe": "a hostile is near",
    "item": "you are moving an item", "alarm": "an alarm needs you", "guard": "guard zone",
    "unknown": "Guard zone not known yet: cross a town's guard line once", "attacked": "you are being attacked",}
# Headings of the Modules tab, in this order (the category given to HOST.add). Any other heading
# comes after them, by name.
CATEGORY_ORDER = ("On screen", "Your things", "The world", "Skills and home", "Extras", "Other")
# Seconds after the last key in the Modules search box before the list is filtered.
SEARCH_SETTLE = 0.3
# Per-account key: the version whose What's new window was last shown.
WHATS_NEW_KEY = "VirtueAssistant_seen_version"


def whats_new():
    """The What's new lines of this version, from the _WhatsNew helper file in the first module folder.

    Returns a tuple of lines, or an empty tuple when there is no module folder or the file is missing
    or broken. The helper is read fresh each time (dropped from sys.modules first) and holds nothing
    but text. Script thread.
    """
    import sys
    d = module_folders()
    if not d:
        return ()
    if d[0] not in sys.path:
        sys.path.insert(0, d[0])
    sys.modules.pop("_WhatsNew", None)
    try:
        import _WhatsNew
        return tuple(_WhatsNew.WHATS_NEW)
    except Exception:
        return ()


class _Gumps(object):
    """API.Gumps with three changes every window gets: right-click closing is turned off on each gump it
    adds, each gump takes part in snapping and the layout, and the controls made during start-up are
    counted for the start-up timing. A module is turned off from the Modules list or its own X button,
    never by a stray right-click on one of its windows.
    """
    def __init__(self, inner):
        """Keep the real API.Gumps object that every other call is passed on to.

        made counts the Create* calls while start-up is being timed; it becomes None when the timing ends.
        """
        self._inner = inner
        self.made = 0

    def __getattr__(self, name):
        """Pass any other attribute through to API.Gumps.

        While start-up is timed, each Create* function is wrapped so its calls are counted in made.
        """
        # Found once, then stored as a plain attribute: later G.Create* calls skip __getattr__ and the
        # .NET member lookup.
        v = getattr(self._inner, name)
        if self.made is not None and name.startswith("Create"):
            v = self._counted(v)
        self.__dict__[name] = v
        return v

    def _counted(self, fn):
        """Wrap a Create* function so each call adds one to made, for as long as the timing runs."""
        def run(*args, **kw):
            """Count the call (only while made is not None), then make the control."""
            if self.made is not None:
                self.made += 1
            return fn(*args, **kw)

        return run

    def AddControlOnClick(self, ctrl, fn):
        """Register a click handler on a control, and poke the host after it ran so the module acts on the
        click on the very next pass instead of its next due tick.
        """
        key = HOST.click_key()

        def run(*args):
            """Run the handler, then wake the host whether it succeeded or failed."""
            HOST.pressed_at = time.time()
            try:
                fn(*args)
            finally:
                HOST.poke(key)

        self._inner.AddControlOnClick(ctrl, run)

    def AddGump(self, g):
        """Add a gump to the screen: right-click closing off, size pinned where the window was given one,
        and registered with the snapping and the layout.
        """
        # A script window is closed only from its X button or the module list.
        Kit.set(g, "CanCloseWithRightClick", False)
        Kit.set(Kit._raw_gump(g), "CanCloseWithRightClick", False)
        p = Kit._pend.get(g)
        # A window given a size keeps it (or one already converted to scrolling): the client's own auto
        # size would otherwise change it on its first update.
        if (p is not None and p[2] and p[3]) or g in Kit._scrolled:
            Kit.pin_size(g)
        r = self._inner.AddGump(g)
        Kit.stir()
        # Quiet: a failure in the snapping or layout bookkeeping must never stop the window from showing.
        with Kit.quiet:
            SNAP.add(g)
            if LAYOUT.loaded:
                # A new window: the layout fits it on its next look, not up to KEEP_EVERY seconds later.
                LAYOUT.fresh_adds.add(g)
        return r


# The one gump interface the whole suite uses.
G = _Gumps(API.Gumps)


def safe(fn, default=None):
    """Call fn() and return its result, or default if it raises.

    Every module leans on this, so it stays as small as Python allows. The mother's own per-pass code
    uses plain try / except instead, to avoid building a lambda on every call.
    """
    try:
        return fn()
    except Exception:
        return default


class Client(object):
    """The few things scripts cannot ask TazUO for through API: the mouse's double-click timer and the
    Alt, Shift and Ctrl keys, found by name among the client's loaded assemblies, plus the hop onto
    the client thread. Works whatever the assembly is called.
    """
    # Set once Client.find has looked for the mouse and keyboard members.
    looked = False
    # (get, set) of Mouse.LastLeftButtonClickTime, or None when this build has no such member.
    mouse = None
    # Key name ("alt", "shift", "ctrl") to the function that reads whether it is held.
    keys = {}
    # A click time meaning the last click was long ago (0 and the maximum mean a double-click).
    NO_CLICK_TIME = 1
    # Full type name to Type, or (None, time of the miss). A scan of every loaded assembly is slow, so
    # lookups are remembered; a miss is retried at most every TYPE_RETRY seconds.
    _types = {}
    # The client's own assembly; False means not looked for yet.
    _client_asm = False
    # Seconds before a type that was not found is looked for again (an assembly may load later).
    TYPE_RETRY = 30.0

    @staticmethod
    def _type(name):
        """Find a .NET type by full name, from the client's own assembly first, then every loaded one.

        Returns the Type or None. Misses are cached for TYPE_RETRY seconds.
        """
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
                    # Kept with the other measured client data, so a later start in the same process skips the lookup.
                    Client._client_asm = Kit._measure["asm"] = API.GetType().Assembly
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
    def flags(static=False, public=True):
        """BindingFlags for reflection: static or instance members, always non-public too, and public ones
        unless public is False.
        """
        from System.Reflection import BindingFlags
        return ((BindingFlags.Static if static else BindingFlags.Instance) | BindingFlags.NonPublic |
                (BindingFlags.Public if public else BindingFlags.Default))

    @staticmethod
    def _member(t, name):
        """Return (get, set) functions for a static property or field of a .NET type, or None if it has
        neither. The setter converts the value to the member's type.
        """
        import System
        flags = Client.flags(True)
        p = t.GetProperty(name, flags)
        if p is not None:
            return (lambda: p.GetValue(None, None),
                    lambda v: p.SetValue(None, System.Convert.ChangeType(v, p.PropertyType), None))
        f = t.GetField(name, flags)
        if f is not None:
            return (lambda: f.GetValue(None), lambda v: f.SetValue(None, System.Convert.ChangeType(v, f.FieldType)))
        return None

    @staticmethod
    def find():
        """Look once for the client's mouse click timer and the Alt, Shift and Ctrl key readers.

        Fills Client.mouse and Client.keys; a reader that cannot be read on this build is left out.
        """
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
            for key, name in (("alt", "Alt"), ("shift", "Shift"), ("ctrl", "Ctrl")):
                # Quiet: a missing key reader just leaves that key out.
                with Kit.quiet:
                    m = Client._member(kb, name)
                    bool(m[0]())
                    Client.keys[key] = m[0]

    @staticmethod
    def second_click_swallowed():
        """Clear the client's last-click time so the next click is reported to script handlers.

        The client turns a second click within its double-click time into a double-click and never
        reports it to script click handlers, so a double-click would arrive as one click. Returns True
        if the second click had already come and gone (swallowed) before this click was handled.
        """
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
        """True while keys go into a text field (chat line or any text box), when hotkeys must not act.
        See Typing.
        """
        return bool(safe(Typing.now, False))

    @staticmethod
    def key_held(which):
        """True or False for whether the key ("alt", "shift" or "ctrl") is held; None when this build has no
        reader for it.
        """
        if not Client.looked:
            Client.find()
        fn = Client.keys.get(which)
        if fn is None:
            return None
        try:
            return bool(fn())
        except Exception:
            return False

    # The client's MainThreadQueue type, found once by _find_mtq.
    MTQ = None
    # Set once _find_mtq has looked.
    mtq_looked = False
    # The way of calling into the client thread that this IronPython build accepts (_pick_main_call).
    main_call = None
    main_cached = False

    @staticmethod
    def _find_mtq():
        """Find ClassicUO.Game.Managers.MainThreadQueue once. Returns the type or None.

        A type found is also kept in the measured client data, so a later start in the same process does
        not look again.
        """
        if Client.mtq_looked:
            return Client.MTQ
        Client.mtq_looked = True
        try:
            import clr
            clr.AddReference(API.GetType().Assembly)
            from ClassicUO.Game.Managers import MainThreadQueue
            Client.MTQ = Kit._measure["mtq"] = MainThreadQueue
        except Exception:
            Client.MTQ = None
        return Client.MTQ

    @staticmethod
    def on_client_thread():
        """True when this code already runs on the client's thread.

        Asked of the client every time, because other threads may call this too.
        """
        MTQ = Client.MTQ if Client.mtq_looked else Client._find_mtq()
        if MTQ is None:
            return False
        try:
            return bool(MTQ.IsMainThread)
        except Exception:
            return False

    @staticmethod
    def _pick_main_call():
        """Pick the way into the client thread that this build accepts. Returns a function taking a callable,
        or None when none works.

        A form that worked in an earlier start of this process is only built (Client.main_cached is set),
        with no probe hop; if building it fails, the probing below runs as usual. Otherwise each form is
        tried in turn once and the first that runs is remembered in the measured client data. The generic
        method and the delegate type are bound here, once, instead of on every hop.
        """
        from System import Func
        MTQ = Client.MTQ
        F = Func[object]

        def generic_of():
            """Build the variant that calls the generic InvokeOnMainThread method."""
            inv = MTQ.InvokeOnMainThread[object]

            def generic(run):
                """Hand run to the client thread through the generic method."""
                inv(F(run))

            return generic

        def inferred_of():
            """Build the variant that lets IronPython infer the generic method's type."""
            def inferred(run):
                """Hand run to the client thread, type inferred."""
                MTQ.InvokeOnMainThread(F(run))

            return inferred

        def with_event_of():
            """Build the variant that queues an action and waits for a flag."""
            from System import Action
            from System.Threading import ManualResetEventSlim

            def with_event(run):
                """Queue run on the client thread and wait up to five seconds for it to finish."""
                done = ManualResetEventSlim(False)

                def wrapped():
                    """Run the call, then release the waiting thread whether it succeeded or failed."""
                    try:
                        run()
                    finally:
                        done.Set()

                MTQ.EnqueueAction(Action(wrapped))
                # A stalled client thread is not "ok": the caller is told with _HopTimeout.
                if not done.Wait(5000):
                    raise _HopTimeout("the client thread didn't answer in 5 s")

            return with_event

        makes = (generic_of, inferred_of, with_event_of)
        at = Kit._measure.get("main_call")
        Client.main_cached = False
        if at in (0, 1, 2):
            try:
                candidate = makes[at]()
                Client.main_cached = True
                return candidate
            except Exception:
                Kit._measure.pop("main_call", None)
        for at, make in enumerate(makes):
            probe = {}

            def run_probe():
                """The probe each variant is tried with: it only has to run."""
                probe["ok"] = True

            try:
                candidate = make()
                candidate(run_probe)
            except Exception:
                continue
            if probe.get("ok"):
                Kit._measure["main_call"] = at
                return candidate
        return None

    @staticmethod
    def post(fn):
        """Queue fn on the client thread without waiting for it, so the script thread can carry on at once.

        Needs Client.MTQ to have been found (_find_mtq); callers check that first.
        """
        from System import Action
        Client.MTQ.EnqueueAction(Action(fn))

    @staticmethod
    def on_main_ex(fn):
        """Run fn on the client thread and report how it went.

        Returns ("ok", result) when fn ran there, ("err", message) when it ran there and raised, or
        ("no", None) when the hop cannot be made. On "err" the exception is kept in Client.exc and its
        text in Client.error. Called on the client thread, fn runs in place. When the hop cannot be queued
        and the call form came from the measured client data, that form is dropped so the next call picks
        one again.
        """
        # Cleared first so a stale exception is never read after a success.
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
        # Queued but not run yet: never run it here as well.
        except _HopTimeout as ex:
            Client.error = str(ex)
            return "err", Client.error
        except Exception as ex:
            Client.error = str(ex)
            if Client.main_cached:
                Client.main_call = None
                Client.main_cached = False
                Kit._measure.pop("main_call", None)
            return "no", None
        if hop.e is not None:
            Client.error, Client.exc = hop.e, hop.x
            return "err", hop.e
        return "ok", hop.v

    # Text of the last error from on_main_ex.
    error = ""
    # The last exception raised inside on_main_ex.
    exc = None


class _HopTimeout(Exception):
    """The client thread took a queued hop but had not run it within the wait."""
    pass


class _Hop(object):
    """One call carried to the client thread by Client.on_main_ex: the function and what came back (value,
    error text, exception). One small object per hop instead of a closure and a dict.
    """
    __slots__ = ("fn", "v", "e", "x")

    def __init__(self, fn):
        """Remember the function; the result slots start empty."""
        self.fn, self.v, self.e, self.x = fn, None, None, None

    def run(self):
        """Run the function on the client thread and keep its value, or its error text and exception."""
        try:
            self.v = self.fn()
        except Exception as ex:
            self.e = str(getattr(ex, "InnerException", None) or ex)
            self.x = ex
        except:
            self.e = "unknown error"


class Typing(object):
    """Is a key the player presses meant for a text field rather than a hotkey?

    The client itself runs its macros only while keyboard focus rests on the chat line and the chat
    line is not open for typing. Virtue Assistant's hotkeys follow the same rule for every field
    anywhere on screen: the chat line once open (Enter), any text box of any window (own settings
    fields, client search and rename boxes, Legion's editor and other Myra windows), and anything
    already typed on the chat line. Read live from the client's UIManager by reflection, so it is
    current at the moment of the key press. Every module asks Client.typing() (or HOST.typing())
    before acting on a key.
    """
    # Set once _find has looked for the two client types.
    looked = False
    # ClassicUO.Game.Managers.UIManager (static).
    uim = None
    # ClassicUO.Configuration.ProfileManager (static).
    prof = None
    # (Type, member, static) to (PropertyInfo or FieldInfo, is a property) or None; keyed by the Type
    # itself, so a lookup is one dict hit.
    _members = {}
    # BindingFlags for (instance, static) members, made once.
    _flags = None
    # The profile object's Type, read once.
    _prof_t = None
    # The system chat control's Type, read once.
    _chat_t = None
    # [pass id, answer] of the last Typing.now inside a client hop.
    _now_memo = [-1, False]

    @staticmethod
    def _find():
        """Look once for the UIManager and ProfileManager types."""
        if Typing.looked:
            return
        Typing.looked = True
        Typing.uim = Client._type("ClassicUO.Game.Managers.UIManager")
        Typing.prof = Client._type("ClassicUO.Configuration.ProfileManager")

    @staticmethod
    def _lookup(t, name, static):
        """Find the member name of type t, most derived class first. Returns (member, is_property) or None.

        Interface properties are tried last for instances.
        """
        if Typing._flags is None:
            from System.Reflection import BindingFlags
            base = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly
            Typing._flags = (base | BindingFlags.Instance, base | BindingFlags.Static)
        flags = Typing._flags[1 if static else 0]
        m, prop, tt = None, False, t
        # Most derived first, so there is no ambiguity.
        while tt is not None and m is None:
            try:
                m = tt.GetProperty(name, flags)
            except Exception:
                m = None
            if m is not None:
                prop = True
            else:
                m = tt.GetField(name, flags)
            tt = tt.BaseType
        # An interface property (the client's IGui).
        if m is None and not static:
            for it in t.GetInterfaces():
                m = it.GetProperty(name)
                if m is not None:
                    prop = True
                    break
        return (m, prop) if m is not None else None

    @staticmethod
    def _get(obj, name, t=None, default=None):
        """Read a property or field of a .NET object by reflection (obj None means static on t).

        Returns default when the member is missing or the read fails. The member lookup is cached.
        """
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
        """True when a and b are the same client object (neither None)."""
        return a is not None and b is not None and bool(Kit._same()(a, b))

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
    def hop(memo, fn):
        """Run fn, or reuse its answer within one pass of the host's client hop.

        memo is a [pass id, value] list owned by the caller. Nothing moves during a hop, so the answer
        stays true for the pass; outside a hop (a hotkey on the script thread) fn always runs.
        """
        try:
            h = HOST
            pid = h.pass_id if h.in_hop else None
        except Exception:
            pid = None
        if pid is not None and memo[0] == pid:
            return memo[1]
        v = fn()
        if pid is not None:
            memo[0] = pid
            memo[1] = v
        return v

    @staticmethod
    def now():
        """True while a key would go into a text field (see the class note). Kept for the pass inside a
        client hop; a hotkey on the script thread always reads it fresh.
        """
        return Typing.hop(Typing._now_memo, Typing._now)

    @staticmethod
    def _now():
        """Work out whether a key would go into a text field, reading the client's UI state."""
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
        # Focus on some other text field counts as typing, unless that field is gone, hidden or read-only
        # (then the client hands focus back).
        if focus is not None and not Typing._same(focus, chat_tb) \
                and not bool(Typing._get(focus, "IsDisposed", default=False)) \
                and bool(Typing._get(focus, "IsVisible", default=True)) \
                and bool(Typing._get(focus, "AcceptKeyboardInput", default=True)):
            return True
        if chat is None:
            return False
        # Without a readable profile the chat line is taken to activate after Enter, the client's default.
        after_enter = True
        if Typing.prof is not None:
            cur = Typing._get(None, "CurrentProfile", Typing.prof)
            if cur is not None:
                v = Typing._get(cur, "ActivateChatAfterEnter", Typing._ptype(cur))
                after_enter = True if v is None else bool(v)
        if after_enter and bool(Typing._get(chat, "IsActive", Typing._chat_t, default=False)):
            # The chat line is open (Enter pressed).
            return True
        text = Typing._get(chat_tb, "Text") if chat_tb is not None else None
        # Something already typed on the chat line.
        return text is not None and len(str(text)) > 0

    @staticmethod
    def release():
        """Hand keyboard focus back to the chat line, the way a click on the game world does, so hotkeys
        work again.

        Runs on the client thread (it hops there if called from the script thread).
        """
        # The pass's kept answer is no longer true.
        Typing._now_memo[0] = -1

        def run():
            """Ask the UIManager to restore chat focus, or focus the chat text box directly."""
            Typing._find()
            uim = Typing.uim
            if uim is None:
                return
            try:
                m = uim.GetMethod("RestoreSystemChatFocus", Client.flags(True))
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
            Client.on_main_ex(run)


class Follow(object):
    """Alt+click auto-follow, the same in every module.

    Any health bar, frame or row for another mobile, and any button that acts on one, can be
    Alt+clicked to auto-follow that mobile with TazUO's own auto-follow; Alt+click the same one again
    to stop. Every module uses this helper, so they all agree on who is followed. In the click
    handler (read Alt AT the click, the key may be up by the next tick) only queue it, then call
    Follow.toggle(serial, TITLE) from tick(). Follow.current() is read from the client itself, so it
    is right even after the client stopped following (the player walked away, the mobile left view)
    or the player Alt+clicked a mobile in the game world.
    """
    # Who this script last asked the client to follow.
    serial = None
    # The ways to read the Alt key, best first (made by _find).
    readers = None
    # Key names tried through API.IsKeyPressed when no reader exists.
    ALT_NAMES = ("ALT", "LALT", "RALT", "LEFTALT", "RIGHTALT", "MENU", "LMENU", "RMENU")
    # SDL's KMOD_ALT mask.
    SDL_ALT = 0x0300

    @staticmethod
    def _find():
        """Build the list of Alt-key readers once: the client's Keyboard.Alt member, its Keyboard type, and
        SDL's modifier state.
        """
        if Follow.readers is not None:
            return
        r = []
        try:
            import clr
            for asm in ("ClassicUO", "ClassicUO.Client", "TazUO", "FNA", "SDL2-CS", "SDL3-CS"):
                safe(lambda: clr.AddReference(asm))
        except Exception:
            pass
        Client.find()
        if "alt" in Client.keys:
            r.append(lambda: Client.key_held("alt"))
        try:
            from ClassicUO.Input import Keyboard
            # The client's own Keyboard.Alt, by reflection.
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
        # A reader exists and says Alt is up: believe it. The IsKeyPressed loop below is for builds with no
        # reader at all (each call there is a frame-wait, which is slow inside a click handler).
        if Follow.readers:
            return False
        for k in Follow.ALT_NAMES:
            if safe(lambda: API.IsKeyPressed(k), False):
                return True
        return False

    # [pass id, serial] of the last Follow.current inside a client hop.
    _memo = [-1, None]

    @staticmethod
    def current():
        """Serial the client is auto-following, or None. Kept for the pass inside a client hop; start and
        stop drop it.
        """
        return Typing.hop(Follow._memo, Follow._current)

    @staticmethod
    def _current():
        """Read the client's FollowingMode and FollowingTarget, falling back to the serial last asked for."""
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
        # No readable profile: trust the last serial only while that mobile is still in view.
        if Follow.serial is not None and API.FindMobile(Follow.serial) is None:
            Follow.serial = None
        return Follow.serial

    @staticmethod
    def start(serial, who=APP_NAME):
        """Auto-follow the mobile with this serial. Returns True when the follow was started.

        Refuses (with a journal line naming who) for no serial, yourself, a mobile out of sight, or a
        client error.
        """
        serial = int(serial or 0)
        if not serial:
            return False
        me = int(safe(lambda: API.Player.Serial, 0) or 0)
        if serial == me:
            API.SysMsg("%s: you can't follow yourself." % who, Kit.HUE_INFO)
            return False
        if API.FindMobile(serial) is None:
            API.SysMsg("%s: can't follow them, they are out of sight." % who, Kit.HUE_BAD)
            return False
        try:
            API.AutoFollow(serial)
        except Exception as ex:
            API.SysMsg("%s: couldn't auto-follow (%s)." % (who, ex), Kit.HUE_BAD)
            return False
        Follow.serial = serial
        # The client's answer changes now: drop the pass's kept one.
        Follow._memo[0] = -1
        API.HeadMsg("* following *", serial, 0x44)
        return True

    @staticmethod
    def stop(who=APP_NAME):
        """Stop auto-following and show a head message over the mobile that was followed."""
        s = Follow.serial
        Follow._memo[0] = -1
        API.CancelAutoFollow()
        Follow.serial = None
        if s:
            API.HeadMsg("* stopped following *", s, 0x35)

    @staticmethod
    def toggle(serial, who=APP_NAME):
        """Alt+click action: follow this mobile, or stop if it is already followed. Returns True when a
        follow started. Call from tick(), not from inside the click handler.
        """
        serial = int(serial or 0)
        if serial and Follow.current() == serial:
            Follow.stop(who)
            return False
        return Follow.start(serial, who)


class Kit(object):
    """The shared native look and the helpers every window of every module is built from.

    Stone frame of the crafting gump, translucent sections, the UO font in client hues, client
    checkboxes and gump-art buttons, plus the windowing rules (below), saved per-character values,
    text measuring, gump parsing, data files and the settings-page and window builders (Form, Page,
    Cleanup, Window). The look (classic, dark, parchment or high contrast; Kit.LOOKS, Kit.set_look),
    the text scale (Kit.tscale) and the compact rows flag (Kit.compact) are class values the host
    sets from the saved interface choices. Everything is a static method on the class, so a module
    calls Kit.something with no setup.

    What is measured from the client (text widths, picture sizes, reflected members) is kept for the
    life of the client process by Kit.measure_bind, so a script started again in the same client does
    not measure it twice.

    The window rules every window of every module and of this script follows:
    1. A window is always wholly on screen: place it with Kit.place, never a bare SetRect. The keeper
       (Snap.keep) moves back whatever still ends up off screen. A window taller than the screen
       scrolls (Kit.scroll_fit); one in a layout zone is cut to its slot the same way.
    2. Every window remembers its place and state per character (Kit.load_pos, save_pos, load_min,
       save_min). A place saved on another screen size is adapted (Kit.adapt).
    3. One anchor convention: the nine screen anchors (Kit.ANCHORS) are placed by Kit.anchor_pos and
       recognised by Kit.anchor_at, and windows snap flush to one another within SNAP_DIST.
    """
    # Art ids of the stone window frame: the crafting gump's nine pieces start here.
    WINDOW_BG     = 5054
    # Centre piece of that frame (plain stone).
    STONE_TILE    = 5058
    # Black tile the crafting gump fills its sections with.
    SECTION_TILE  = 2624
    # How see-through the black sections are in the current look.
    SECTION_ALPHA = 0.8
    # Tile drawn solid behind text boxes.
    FIELD_TILE    = 2624
    # Knot ornament on the frame's corners (0 turns it off).
    CORNER_ART    = 10460
    # Gump-art buttons are (normal, pressed, hover) art ids: right arrow.
    ART_PLAY    = (4005, 4007, 4006)
    # X / cancel.
    ART_CLOSE   = (4017, 4019, 4018)
    # Hue of the frame art, hue of the corner knots and section alpha in the dark look (Kit.set_look).
    DARK_HUE = 1899
    DARK_CORNER_HUE = 2305
    DARK_SECTION_ALPHA = 0.95
    LIGHT_SECTION_ALPHA = 0.8
    PARCH_HUE = 2960
    PARCH_CORNER_HUE = 1260
    PARCH_SECTION_HUE = 1845
    PARCH_SECTION_ALPHA = 0.9
    CONTRAST_HUE = 1175
    CONTRAST_SECTION_ALPHA = 1.0
    LOOKS = {"classic": (0, 0, 0, LIGHT_SECTION_ALPHA), "dark": (DARK_HUE, DARK_CORNER_HUE, 0, DARK_SECTION_ALPHA),
             "parchment": (PARCH_HUE, PARCH_CORNER_HUE, PARCH_SECTION_HUE, PARCH_SECTION_ALPHA),
             "contrast": (CONTRAST_HUE, CONTRAST_HUE, 0, CONTRAST_SECTION_ALPHA)}
    LOOK_ORDER = ("classic", "dark", "parchment", "contrast")
    LOOK_NAMES = {"classic": "Classic", "dark": "Dark", "parchment": "Parchment", "contrast": "High contrast"}
    TEXT_SIZES = (100, 115, 130, 150)
    SECTION_HUE = 0
    tscale = 1.0
    compact = cblind = streamer = False
    # Art ids of the gold edge pieces (horizontal, vertical) and its thickness in pixels (gold_box).
    GOLD_H = 2700
    GOLD_V = 2701
    GOLD_T = 3
    _hues = {}
    _look = "classic"
    # Window key to its Kit.Window, for the windows that use it.
    _wins = {}
    _behind = set()
    # Check mark.
    ART_OK      = (4023, 4025, 4024)
    # Page / scroll.
    ART_PAGE    = (4011, 4013, 4012)
    # Small down arrow: Minimize.
    ART_MIN     = (253, 252, 253)
    # Small up arrow: Restore.
    ART_RESTORE = (251, 250, 251)
    # Gold down triangle: Fold into the Action Bar.
    ART_DOCK    = (5602, 5606, 5602)
    # Small round gem button for a window's simple buttons.
    ART_CIRCLE  = (2117, 2118, 2118)
    # The fold button sits DOCK_DX pixels left of the Minimize arrow and DOCK_DY lower (the triangle
    # is 16 pixels tall, the arrow 21).
    DOCK_DX, DOCK_DY = 20, 2
    # Tooltips of the standard title buttons.
    DOCK_TIP = "Fold into the Action Bar's tray"
    MIN_TIP = "Minimize (or double-click the title)"
    RESTORE_TIP = "Restore"
    SETTINGS_TIP = "Open %s settings"
    CLOSE_TIP = "Close %s (turns it off)"
    DOUBLE_TIP = "Double-click: minimize or restore"
    # Health bar line art: the client's own status bar pieces (red, blue, poison).
    LINE_RED, LINE_BLUE, LINE_POISON = 0x0805, 0x0806, 0x0808
    # Client hues for titles, text, good news, bad news and information.
    HUE_TITLE = 53
    HUE_TEXT  = 1153
    HUE_GOOD  = 68
    HUE_BAD   = 33
    HUE_INFO  = 946
    # Stone frame visible round the sections, in pixels.
    MARGIN = 12
    # Stone visible between sections, in pixels (it acts as the border).
    GAP    = 8
    # Graphic to (width, height), as measured by pic_size.
    _sizes = {}
    # The measured client data of this process: the entry measure_bind binds, holding the "bad" flag,
    # the client assembly and queue type, the way into the client thread, the render scale and the
    # missing-member list.
    _measure = {}
    MEASURE_CAP = 6000

    @staticmethod
    def on_client(fn, fallback=True):
        """Run fn in one hop on the client thread, where every script call runs in place.

        This is the way to build or redraw a whole window: a call that returns a value waits for the
        client's next update pass, one round trip each, unless it already runs on the client thread.
        Returns fn's result. When the hop cannot be made, fn runs here instead if fallback is set (else
        None comes back). fn must not wait (no HOST.idle, no API.Pause): on the client thread a wait is
        a freeze.
        """
        how, v = Client.on_main_ex(fn)
        if how == "ok":
            return v
        # fn ran there and failed: report it, do not run it again.
        if how == "err":
            raise Client.exc if isinstance(Client.exc, Exception) else Exception(Client.error)
        return fn() if fallback else None

    # Cached client size and when it was read.
    _screen = {"wh": (0, 0), "at": 0.0}

    @staticmethod
    def screen():
        """(width, height) of the client window in the pixels gumps are placed in.

        The client window's pixels divided by the UI scale (render_scale), re-read at most once a second.
        """
        now = time.time()
        if now - Kit._screen["at"] >= 1.0:
            Kit._screen["at"] = now
            try:
                b = API.GetClientBounds()
                wh = (int(b.Width), int(b.Height))
            except Exception:
                wh = None
            if wh and wh[0] > 0 and wh[1] > 0:
                # Gumps are placed in logical pixels.
                s = Kit.render_scale()
                if abs(s - 1.0) > 0.001:
                    wh = (int(round(wh[0] / s)), int(round(wh[1] / s)))
                Kit._screen["wh"] = wh
        return Kit._screen["wh"]

    _scale = {"fn": None, "looked": False}

    @staticmethod
    def render_scale():
        """The client's UI scale, 1.0 when it has none or cannot be read.

        A gump's X, Y and size are logical pixels, the client window's pixels divided by this scale, so
        screen() gives the same pixels as the gumps use. The scale is read by reflection from the client's
        Game.RenderScale property, because the client class is internal to the client. The two reflected
        members are kept in the measured client data; a failed read drops them.
        """
        st = Kit._scale
        if not st["looked"]:
            st["looked"] = True
            try:
                gp, rp = Kit._measure.get("scale") or (None, None)
                if rp is None:
                    t = Client._type("ClassicUO.Client")
                    gp = t.GetProperty("Game", Client.flags(True))
                    game = gp.GetValue(None, None)
                    rp = game.GetType().GetProperty("RenderScale", Client.flags())
                    float(rp.GetValue(game, None))
                    Kit._measure["scale"] = (gp, rp)
                st["fn"] = lambda: float(rp.GetValue(gp.GetValue(None, None), None))
            except Exception:
                st["fn"] = None
        fn = st["fn"]
        if fn is None:
            return 1.0
        try:
            s = fn()
            # Anything outside a sane range is treated as no scale.
            return s if 0.25 <= s <= 4.0 else 1.0
        except Exception:
            Kit._measure.pop("scale", None)
            return 1.0

    # The nine screen anchors: corners, edge midpoints, centre.
    ANCHORS = ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR")
    # Per-character key: the screen size the saved places were made for.
    SCREEN_KEY = "VirtueAssistant_screen"
    # (width, height) read from that key at start (see adapt).
    _pos_screen = None

    @staticmethod
    def clamp(x, y, w, h):
        """(x, y) moved the least so a w x h window is wholly on screen.

        A window bigger than the screen keeps whichever edge the place asked for: its left (top) edge
        when x (y) is at or past 0, else its right (bottom) edge, so a very wide bar can be dragged to
        reach either end and never ends up with both ends off the screen.
        """
        W, H = Kit.screen()
        x, y, w, h = int(x or 0), int(y or 0), int(w or 0), int(h or 0)
        if W > 0:
            x = max(0, min(x, W - w)) if w <= W else max(W - w, min(x, 0))
        if H > 0:
            y = max(0, min(y, H - h)) if h <= H else max(H - h, min(y, 0))
        return x, y

    # Window to the list of controls that make up its stone frame.
    _frame_parts = {}
    # Window to what it was last asked to be, while the client has not applied it: SetRect and SetPos
    # are queued by the client and land on a later frame, while GetX and GetWidth answer at once. A
    # window just made reads 0, 0, 0 x 0 and a window just moved reads its old place. Kit.rect answers
    # with the asked-for place until the client has applied it.
    _pend = {}
    # Seconds a request is believed before the client's own answer is taken again.
    PEND_FOR = 1.0
    churn = 0
    churn_at = 0.0

    @staticmethod
    def stir():
        """Note that a window was added, moved, resized or disposed.

        Counts it in churn and stamps churn_at, which Host.settle_tick reads: start-up is not settled until
        the windows have been quiet for a moment.
        """
        Kit.churn += 1
        Kit.churn_at = time.time()

    @staticmethod
    def note_rect(g, x, y, w=None, h=None):
        """Record that window g was asked to be at (x, y), and w x h when given, until the client applies it.

        Kit.rect then answers with that. A request that really changes the place or size also calls
        Kit.stir. Never raises: a window that cannot be tracked is ignored.
        """
        if g is None:
            return
        try:
            r = None
            if Kit._pend:
                # Drop a request that landed or expired first.
                r = Kit.rect(g)
            old = Kit._pend.get(g)
            if w is None and old is not None:
                # A move after a resize that has not landed yet keeps the asked-for size.
                w, h = old[2], old[3]
            if old is not None:
                # The client's own word from before both requests.
                was = old[5]
            elif r is not None:
                # The client's word, just read above.
                was = r
            else:
                was = (int(g.GetX()), int(g.GetY()), int(g.GetWidth() or 0), int(g.GetHeight() or 0))
            n = (int(x), int(y), None if w is None else int(w), None if h is None else int(h))
            b = old or was
            if b[0:2] != n[0:2] or (n[2] is not None and (b[2], b[3]) != n[2:4]):
                Kit.stir()
            Kit._pend[g] = n + (time.time(), was)
        except Exception:
            # Not a window it can keep track of.
            pass

    @staticmethod
    def rect(g):
        """(x, y, w, h) of window g: what it was last asked to be while the client has not applied it, else
        what the client says. None when it cannot be read.
        """
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
                # Landed, or the client moved it since (a drag, a fit of its own), or it never will: from here on
                # the client's word is taken.
                if (x, y, w, h) == (p[0], p[1], pw, ph) or (x, y, w, h) != p[5] or time.time() - p[4] > Kit.PEND_FOR:
                    del pend[g]
                else:
                    return p[0], p[1], pw, ph
        return x, y, w, h

    @staticmethod
    def pos(g):
        """(x, y) of window g as Kit.rect has it, using two client reads instead of four when no request for
        it is waiting to land. None when it cannot be read.
        """
        if Kit._pend and g in Kit._pend:
            r = Kit.rect(g)
            return None if r is None else (r[0], r[1])
        try:
            return int(g.GetX()), int(g.GetY())
        except Exception:
            return None

    @staticmethod
    def prune_pending():
        """Drop requests that landed long ago or whose window closed. Called by the keeper."""
        # Windows never seen by the snapping would pile up here.
        if len(Kit._pinned) > 400:
            Kit._pinned = set(g for g in Kit._pinned if Kit.is_open(g))
        if not Kit._pend:
            return
        now = time.time()
        for g in [g for g, p in Kit._pend.items() if now - p[4] > Kit.PEND_FOR]:
            Kit._pend.pop(g, None)

    @staticmethod
    def place(g, x, y, w, h, head=None, max_h=None):
        """Place window g on screen, always, and return the (x, y) used.

        A window the layout has fitted to its slot in a zone (Fill) stays the slot's size wherever and
        however big its module places it: (w, h) is noted as the window's own size and the slot is kept.
        head is the height of the fixed title part when the window scrolls; max_h is a lower height limit
        than the screen's (the slot of a zone).
        """
        rec = Fill.recs.get(g) if Fill.recs else None
        if rec is not None and rec["slot"] is not None:
            rec["nat"], rec["size"] = (int(w or 0), int(h or 0)), None
            sx, sy, sw, sh = rec["slot"]
            if Kit.on_client(lambda: Fill.fit(g, sx, sy, sw, sh, rec["mode"]), fallback=False) is not None:
                return sx, sy
            # Could not be fitted: placed as it comes.
            Fill.recs.pop(g, None)
        return Kit._place_raw(g, x, y, w, h, head, max_h)

    @staticmethod
    def _place_raw(g, x, y, w, h, head=None, max_h=None):
        """Kit.place without the zone fit (Fill places with this). Returns the (x, y) the window was set at.

        A window taller than the screen (or than max_h) is not shown half off it: it is cut to that height
        and its body scrolls, with a scrollbar down its right side and the title row staying put
        (Kit.scroll_fit). head is the height of that fixed top part in the window's pixels (default: the
        standard title section). A window parked at the screen's left tab keeps that parked x. The size
        set here is pinned, so the keeper does not undo it.
        """
        w, h = int(w or 0), int(h or 0)
        H = Kit.screen()[1]
        limit = H if not max_h else min(H, int(max_h))
        if limit > 0 and (h > limit or g in Kit._scrolled):
            # The slot (or None), not the screen height, is what scroll_fit keeps as its cap, so a taller
            # client window lets the window grow back.
            fit = Kit.scroll_fit(g, w, h, head, int(max_h) if max_h else None)
            if fit is not None:
                w, h = fit
        off = g in Kit._behind or int(x or 0) <= TAB_X // 2
        x, y = Kit.clamp(x, y, w, h)
        if off:
            x = TAB_X
        g.SetRect(x, y, w, h)
        # Read back as asked until it lands.
        Kit.note_rect(g, x, y, w, h)
        if g not in Kit._pinned:
            # The size set here stays its size.
            Kit.pin_size(g)
        return x, y

    # Windows whose auto size is off.
    _pinned = set()

    @staticmethod
    def pin_size(g, raw=None):
        """Turn the client's auto size off for window g, so the size this script gives it stays.

        TazUO makes a script window with WantUpdateSize on: on its first update the client sets its width
        and height to the far edge of its visible children and turns the flag off. A window whose frame is
        hidden before that came out short of its slot, so a window given a size keeps it. Returns True
        when the flag is off. A plain property set, safe on any thread.
        """
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

    # Width of the band added to a scrolling window for the client's scrollbar (the scrollbar gump is
    # 15 pixels wide).
    SCROLL_BAND = 15
    # Window to the frame pieces add_window_frame drew.
    _frames = {}
    # Window to how it was converted to a scrolling window (see scroll_fit).
    _scrolled = {}
    # Look up a window's conversion record with Kit.scroll_info.
    scroll_info = _scrolled.get
    # How a raw control's rect is read on this build.
    _rawmode = {}

    @staticmethod
    def scroll_fit(g, w, h, head=None, limit=None):
        """Turn window g (w x h, taller than the screen) into a scrolling window of the screen's height, or
        bring one already converted up to date with a new size.

        A window taller than the screen is cut to its height, everything under the title row is moved
        into a client scroll area covering the body, and the client's own scrollbar runs down the right
        side in a band SCROLL_BAND pixels wide. The controls keep their coordinates (the area sits at 0,
        0), so a module that moves or reads its controls later sees no change; controls added later are
        swept into the area by the keeper (scroll_sweep). The frame is drawn again for the new size, an
        opaque stone band behind the title row keeps scrolled content from showing or clicking through,
        and the title row is drawn last, on top.

        head is the fixed top height; limit is the height to cut to instead of the screen's (a zone
        slot). Returns (width, height) of the window, or None when it could not be done, in which case
        the caller places the window as it is.
        """
        try:
            H = Kit.screen()[1]
            if limit:
                H = min(H, int(limit))
            info = Kit._scrolled.get(g)
            if info is not None and info["w"] == w and info["h"] == h and info["H"] == H:
                return info["w2"], info["hv"]
            if head is None:
                head = info["head"] if info is not None else Kit.MARGIN + 30 + Kit.GAP
            out = Kit.on_client(lambda: Kit._scroll_build(g, w, h, int(head), H), fallback=False)
            if out is not None:
                Kit._scrolled[g]["lim"] = int(limit) if limit else None
            return out
        except Exception:
            return None

    @staticmethod
    def _raw_rect(c):
        """(x, y, w, h) of a client control, or None.

        The client's X, Y, Width and Height are ref properties, which not every IronPython reads the same
        way, so the way that works here is found once and kept in _rawmode.
        """
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
        """The client's own Gump behind a script window, or None."""
        try:
            raw = g.Gump
            if raw is not None:
                return raw
        except Exception:
            pass
        return Kit.client_control(g)

    @staticmethod
    def _children(raw):
        """The client control's children in draw order, as a list copy."""
        kids = raw.Children
        return [kids[i] for i in range(int(kids.Count))]

    @staticmethod
    def _scroll_build(g, w, h, head, H):
        """Convert window g to a scrolling window, or re-fit a converted one, on the client thread.

        Returns (w2, hv), the new width and visible height, or None, in which case the window is as it
        was. Nothing is changed until every control's place has been read; after that a failure puts the
        frame back (_scroll_undo).
        """
        M = Kit.MARGIN
        # Every queued Add and SetRect in place first.
        if not Kit.flush():
            return None
        raw = Kit._raw_gump(g)
        if raw is None:
            return None
        hv = min(h, H)
        head = max(0, min(head, hv - M - 40))
        w2 = w + Kit.SCROLL_BAND
        # The client puts its scrollbar 14 pixels from the right.
        area_w = w - M + 14
        area_h = hv - M
        info = Kit._scrolled.get(g)
        if info is not None:
            return Kit._scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head)
        fr = Kit._frames.get(g)
        corners = fr["corners"] if fr else True
        mouse = fr["mouse"] if fr else True
        old_frame = list(fr["pieces"]) if fr else []
        kids, content, header, fixed = [], [], [], []
        skip = [pr for pr in map(Kit.client_control, old_frame) if pr is not None]
        same = Kit._same()
        for c in Kit._children(raw):
            try:
                if c.IsDisposed:
                    continue
            except Exception:
                continue
            if any(same(c, s) for s in skip):
                continue
            # A control whose place cannot be read: give up.
            r = Kit._raw_rect(c)
            if r is None:
                return None
            kids.append(c)
            cy, ch = r[1], r[3]
            # A full-height background of the module's own.
            if cy <= 0 and ch >= h - 2:
                fixed.append(c)
            # The title row (and anything across its edge).
            elif cy < head:
                header.append(c)
            else:
                content.append(c)
        # A first conversion starts here: the old frame is replaced.
        Kit._frames.pop(g, None)
        for p in old_frame:
            Kit.dispose(p)
        frame = area = band = None
        try:
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h)
            # Under everything.
            frame = Kit._scroll_frame(g, w2, hv, corners, mouse)
            if not Kit.flush():
                raise Exception("queue")
            for c in fixed:
                # To the end of the list: right after the frame.
                c.Parent = raw
            g.Add(area)
            if not Kit.flush():
                raise Exception("queue")
            area_raw = Kit.client_control(area)
            if area_raw is None:
                raise Exception("no area")
            for c in content:
                # Into the scroll area, same coordinates.
                c.Parent = area_raw
            band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush():
                raise Exception("queue")
            for c in header:
                # Last of all: drawn over the band.
                c.Parent = raw
        except Exception:
            Kit._scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band)
            return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse)
        return w2, hv

    @staticmethod
    def _scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head):
        """Re-fit a converted window to another size: the frame and band are drawn again and the content
        moves into a scroll area of the new size.

        The client's scrollbar keeps the hit boxes it was made with, so it is made anew rather than
        resized. Returns (w2, hv) or None.
        """
        frame = area = band = None
        moved = False
        try:
            for p in info["frame"] + info["band"]:
                Kit.dispose(p)
            old_area, old_raw = info["area"], info["area_raw"]
            header = [c for c in info["header"] if not c.IsDisposed]
            fixed = [c for c in info["fixed"] if not c.IsDisposed]
            corners, mouse = info["corners"], info["mouse"]
            frame = Kit._scroll_frame(g, w2, hv, corners, mouse)
            if not Kit.flush():
                raise Exception("queue")
            for c in fixed:
                c.Parent = raw
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h)
            g.Add(area)
            if not Kit.flush():
                raise Exception("queue")
            area_raw = Kit.client_control(area)
            if area_raw is None:
                raise Exception("no area")
            kids = Kit._children(old_raw)
            # The first child is the old scrollbar.
            for c in kids[1:]:
                try:
                    if not c.IsDisposed:
                        c.Parent = area_raw
                except Exception:
                    pass
            Kit.dispose(old_area)
            moved = True
            band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush():
                raise Exception("queue")
            for c in header:
                c.Parent = raw
        except Exception:
            if moved:
                info.update(area=area, area_raw=area_raw)
            else:
                Kit.dispose(area)
            info.update(frame=frame or [], band=band or [], known=None, skip_raw=None)
            return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse)
        return w2, hv

    @staticmethod
    def _scroll_frame(g, w2, hv, corners, mouse):
        """The frame of a scrolling window: the nine-piece stone frame and the two knots on the right.

        The knots sit under the scrollbar, which covers their middle (as the sections cover the left
        knots' middle), so a strip of each shows on the border. Returns the controls drawn.
        """
        return Kit._add_corners(g, Kit._frame_pieces(g, w2, hv, False, mouse), w2, hv, corners, mouse)

    @staticmethod
    def _add_corners(g, out, right, hv, corners, mouse):
        """Add the corner knots to a frame, on the left (right is None) or at the given right edge.
        Returns out with the knots appended.
        """
        cw, ch = Kit.pic_size(Kit.CORNER_ART) if corners and Kit.CORNER_ART else (0, 0)
        if cw and ch:
            for cy in (0, hv - ch):
                p = Kit.add_pic(g, Kit.CORNER_ART, 0 if right is None else right - cw, cy, mouse=mouse)
                if p is not None:
                    out.append(p)
                    Kit._note_frame_part(g, p)
        return out

    @staticmethod
    def _scroll_band(g, w, w2, hv, head, corners, mouse):
        """The band behind the title row of a scrolling window, and the two left knots over it.

        Opaque stone (the frame's own tile, from the same origin, so there is no seam) that takes the
        mouse, so nothing scrolled under the title can be seen or clicked. Returns the controls drawn.
        """
        M = Kit.MARGIN
        band = []
        bl = Kit.pic_size(Kit.WINDOW_BG + 3)[0] or M
        bt = Kit.pic_size(Kit.WINDOW_BG + 1)[1] or M
        t = Kit.add_tiled(g, Kit.STONE_TILE, bl, bt, w - M - bl, head - bt)
        if t is not None:
            t.SetAcceptMouseInput(True)
            # Takes the mouse, and can be used to drag the window.
            t.CanMove = True
            band.append(t)
        return Kit._add_corners(g, band, None, hv, corners, mouse)

    @staticmethod
    def _note_frame_part(g, p):
        """Note that control p is part of window g's stone frame, drawn after the frame itself, so the one
        frame hides it with the rest.
        """
        parts = Kit._frame_parts.get(g)
        if parts is not None:
            parts.append(p)

    @staticmethod
    def _scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse):
        """Record how window g was converted to a scrolling window, so later calls can refit and sweep it."""
        Kit._scrolled[g] = {"w": w, "h": h, "H": H, "w2": w2, "hv": hv, "head": head, "raw": raw, "area": area,
                            "area_raw": area_raw, "frame": frame, "band": band, "header": header, "fixed": fixed,
                            "n": Kit._live_count(raw), "corners": corners, "mouse": mouse}
        Kit._prune(Kit._scrolled)

    @staticmethod
    def _scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band):
        """Undo a conversion that failed half way: the window as it was, its frame drawn again at its own
        size and its controls put back after it in the same order.
        """
        for p in (frame or []) + (band or []):
            Kit.dispose(p)
        Kit.dispose(area)
        # Quiet: a failure here must not hide the window.
        with Kit.quiet:
            pieces = Kit._frame_pieces(g, w, h, corners, mouse)
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}
            Kit.flush()
            # After the frame again, in the same order.
            for c in kids:
                c.Parent = raw

    @staticmethod
    def _live_count(raw):
        """How many children a client control has that are not disposed (a disposed one stays in the list
        until the control's next update). -1 when it cannot be read.
        """
        n = 0
        try:
            kids = raw.Children
            for i in range(int(kids.Count)):
                if not kids[i].IsDisposed:
                    n += 1
        except Exception:
            return -1
        return n

    # Bound once to System.Object.ReferenceEquals.
    _same_fn = None

    @staticmethod
    def _same():
        """Return a function (a, b) that says whether two are the same client object."""
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
        """Keeper pass for scrolling windows, on the client thread: put controls a module added after the
        conversion into the scroll area, and fit a window again when the client's height changed.

        Controls under the title row stay where they are. Windows that closed are forgotten. A cheap
        child-count read comes first; the child-by-child count runs only when it changed, and every
        SWEEP_FULL seconds.
        """
        if not Kit._scrolled:
            return
        gone, stalled = [], False
        H = Kit.screen()[1]
        for g, info in list(Kit._scrolled.items()):
            if not Kit.is_open(g):
                gone.append(g)
                continue
            raw = info["raw"]
            lim = info.get("lim")
            want = min(H, lim) if lim else H
            # The client window changed height: fit again.
            if H > 0 and info["H"] != want:
                try:
                    fit = Kit._scroll_build(g, info["w"], info["h"], info["head"], want)
                    if fit is not None:
                        info = Kit._scrolled.get(g) or info
                        info["lim"] = lim
                        x, y = Kit.clamp(int(g.GetX()), int(g.GetY()), fit[0], fit[1])
                        if g in Kit._behind:
                            x = TAB_X
                        g.SetRect(x, y, fit[0], fit[1])
                        Kit.moved_by_code(g)
                except Exception:
                    pass
                continue
            try:
                cnt = int(raw.Children.Count)
            except Exception:
                cnt = -1
            now = time.time()
            # The child count is unchanged and a full look is not due yet: nothing to do.
            if cnt >= 0 and cnt == info.get("cnt") and 0 <= info.get("full_at", 0.0) - now:
                continue
            info["cnt"] = cnt
            info["full_at"] = now + Kit.SWEEP_FULL
            n = Kit._live_count(raw)
            if n < 0 or n == info["n"]:
                continue
            if stalled or not Kit.flush():
                # The queue could not be flushed: look at it again next sweep.
                info["cnt"], stalled = None, True
                continue
            try:
                kids = Kit._children(raw)
            except Exception:
                info["cnt"] = None
                continue
            known = info.get("known")
            if known is None:
                # One set of the window's own pieces, kept: a set lookup per child instead of a ReferenceEquals
                # call against every piece.
                known = info["known"] = set([info["area_raw"]] + info["header"] + info["fixed"] + [
                    kr for kr in map(Kit.client_control, info["frame"] + info["band"]) if kr is not None])
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
    def attach(follower, leader):
        """Tell the snapping that follower is placed beside leader by the module itself (a tray beside a bar,
        a grid under a title bar). It never snaps on its own, and the keeper keeps the two on screen as
        one, moving both.
        """
        SNAP.attach(follower, leader)

    @staticmethod
    def detach(follower):
        """Release a follower: a free window again, snapping as any other."""
        SNAP.detach(follower)

    @staticmethod
    def no_snap(g):
        """Window g takes no part in snapping: it stays exactly where it is dropped, follows nothing and
        nothing snaps on to it, but the keeper still keeps it on screen and on_moved still tells its
        module.
        """
        SNAP.exempt(g)

    @staticmethod
    def anchor_pos(name, w, h):
        """(x, y) of a w x h window on the screen anchor name (one of ANCHORS), or (None, None) without a
        screen or a name. A window wider or taller than the screen keeps its left or top edge on.
        """
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
        """The screen anchor a w x h window at (x, y) sits on, or an empty string for none.

        It sits on an anchor when it is within slack pixels of it on both axes.
        """
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return ""
        col = "L" if abs(x) <= slack else "R" if abs(x + w - W) <= slack else \
            "C" if abs(x - (W - w) // 2) <= slack else None
        row = "T" if abs(y) <= slack else "B" if abs(y + h - H) <= slack else \
            "C" if abs(y - (H - h) // 2) <= slack else None
        if col is None or row is None:
            return ""
        # "TC" becomes "T" and "CC" becomes "C".
        return (row + col).replace("C", "") or "C"

    @staticmethod
    def anchor_targets(w, h):
        """List of (x, y) where a w x h window sits on each anchor, in ANCHORS order (top row first, left to
        right); an empty list without a screen.
        """
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return []
        return [Kit.anchor_pos(n, w, h) for n in Kit.ANCHORS]

    @staticmethod
    def remap_axis(p, s, S, S2):
        """Position p of a window s long on a screen S long, moved to a screen S2 long.

        It keeps its distance from the edge or the centre it is nearest (the third of the screen its
        middle is in), and sits exactly on the anchor when it was exactly on it.
        """
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
        """A saved window place moved to the screen of today.

        It moves with the anchor it was nearest on the screen it was saved on (read from SCREEN_KEY), then,
        when a size is given, is kept wholly on screen. Returns (x, y).
        """
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
        """At start: read the screen size the saved places belong to from SCREEN_KEY."""
        try:
            w, h = Kit.get_var(Kit.SCREEN_KEY).split(",")
            Kit._pos_screen = (int(w), int(h))
        except Exception:
            Kit._pos_screen = None

    @staticmethod
    def note_screen(wh=None):
        """From here on the saved places belong to this screen size (called once the windows have been placed
        on it). Writes SCREEN_KEY when the size changed.
        """
        wh = wh or Kit.screen()
        if wh and wh[0] > 0 and wh[1] > 0 and wh != Kit._pos_screen:
            Kit._pos_screen = wh
            Kit.put_var(Kit.SCREEN_KEY, "%d,%d" % wh)

    @staticmethod
    def pic_size(graphic):
        """Pixel size (width, height) of a gump graphic, measured from the client and cached. (0, 0) when it
        cannot be measured.
        """
        wh = Kit._sizes.get(graphic)
        if wh is None:
            w = h = 0
            try:
                p = G.CreateGumpPic(graphic)
                w, h = int(p.GetWidth() or 0), int(p.GetHeight() or 0)
                Kit.dispose(p)
            except Exception:
                # A failed measure marks the kept client data as bad, so the next start measures afresh.
                Kit._measure["bad"] = True
            wh = Kit._sizes[graphic] = (w, h)
        return wh

    @staticmethod
    def dark():
        """True when the current look is a dark one (dark or high contrast)."""
        return Kit._look in ("dark", "contrast")

    @staticmethod
    def look():
        """The name of the current look."""
        return Kit._look

    @staticmethod
    def set_look(name):
        """Switch the shared look by name (an unknown name gives classic).

        Sets the frame piece hues and the section hue and alpha from Kit.LOOKS. It only changes the
        values; Kit.retint repaints frames already drawn.
        """
        name = name if name in Kit.LOOKS else "classic"
        fh, kh, sh, sa = Kit.LOOKS[name]
        art = [(Kit.WINDOW_BG + i, fh) for i in range(9)] + [(Kit.CORNER_ART, kh), (Kit.SECTION_TILE, sh)]
        Kit._hues = dict(p for p in art if p[1])
        Kit._look, Kit.SECTION_HUE, Kit.SECTION_ALPHA = name, sh, sa

    @staticmethod
    def tsize(px):
        """A pixel size scaled by the interface text size (Kit.tscale), as a whole number."""
        return int(round(px * Kit.tscale))

    @staticmethod
    def pitch(h):
        """A row height in pixels, trimmed by 4 (never under 20) when compact rows are on."""
        # Rows of 20 or less are left alone so they never become too small to click.
        return max(20, h - 4) if Kit.compact and h > 20 else h

    @staticmethod
    def look_hue(graphic, hue=0):
        """The hue for an art id: the given hue, else the current look's tint, else 0."""
        return hue or Kit._hues.get(graphic, 0)

    @staticmethod
    def retint():
        """Tint every drawn frame piece again for the current look."""
        for parts in list(Kit._frame_parts.values()):
            for p in parts:
                # Quiet: a disposed piece is skipped.
                with Kit.quiet:
                    p.Hue = Kit._hues.get(int(p.Graphic), 0)

    @staticmethod
    def add_pic(g, graphic, x, y, hue=0, mouse=True):
        """Add a gump picture to window g at (x, y) and return it, or None on failure.

        With mouse False clicks go through to the window under it. The current look's hue is applied unless
        a hue is given.
        """
        try:
            hue = hue or Kit._hues.get(graphic, 0)
            p = G.CreateGumpPic(graphic, x, y, hue) if hue else G.CreateGumpPic(graphic, x, y)
            p.SetPos(x, y)
            # Clicks go through to the window under it.
            if not mouse:
                p.SetAcceptMouseInput(False)
            g.Add(p)
            return p
        except Exception:
            return None

    @staticmethod
    def add_tiled(g, graphic, x, y, w, h, alpha=None, fallback="#101010", hue=0):
        """Add a tiled picture w x h to window g and return it (None when w or h is not positive).

        The look's hue is applied unless a hue is given. Falls back to a flat colour box when the art
        cannot be made. Never takes the mouse.
        """
        if w <= 0 or h <= 0:
            return None
        hue = hue or Kit._hues.get(graphic, 0)
        try:
            t = (G.CreateTiledGumpPic(graphic, w, h, hue) if hue else G.CreateTiledGumpPic(graphic, w, h))
        except Exception:
            t = G.CreateGumpColorBox(alpha if alpha is not None else 1.0, fallback)
        t.SetRect(x, y, w, h)
        if alpha is not None:
            t.SetAlpha(alpha)
        t.SetAcceptMouseInput(False)
        g.Add(t)
        return t

    @staticmethod
    def inert(ctrl):
        """Turn mouse input off on a drawn control (a label, box or picture) and return it, so the control
        never takes a click meant for the window. Used while building windows.
        """
        ctrl.SetAcceptMouseInput(False)
        return ctrl

    @staticmethod
    def add_box(g, x, y, w, h, alpha=0.5, color="#FFFFFF"):
        """A flat translucent rectangle (grid lines, markers); never takes the mouse. None when w or h is not
        positive.
        """
        if w <= 0 or h <= 0:
            return None
        b = G.CreateGumpColorBox(alpha, color)
        b.SetRect(x, y, w, h)
        b.SetAcceptMouseInput(False)
        g.Add(b)
        return b

    @staticmethod
    def add_resizepic(g, base, x, y, w, h, mouse=True):
        """Draw a nine-piece UO background (like a server gump's AddBackground) and return the controls drawn.

        The nine sizes are measured once per art; when they cannot be measured only the centre is drawn.
        """
        # The nine sizes, once per art.
        s = Kit._rp_sizes.get(base)
        if s is None:
            s = [Kit.pic_size(base + i) for i in range(9)]
            if not all(p[0] > 0 and p[1] > 0 for p in s):
                # Cannot measure: centre only.
                return [Kit.add_tiled(g, base + 4, x, y, w, h)]
            Kit._rp_sizes[base] = s
        tl, t, tr, l, c, r, bl, b, br = s
        out = [Kit.add_tiled(g, base + 4, x + l[0], y + t[1], w - l[0] - r[0], h - t[1] - b[1]),
            Kit.add_tiled(g, base + 1, x + tl[0], y, w - tl[0] - tr[0], t[1]),
            Kit.add_tiled(g, base + 7, x + bl[0], y + h - b[1], w - bl[0] - br[0], b[1]),
            Kit.add_tiled(g, base + 3, x, y + tl[1], l[0], h - tl[1] - bl[1]),
            Kit.add_tiled(g, base + 5, x + w - r[0], y + tr[1], r[0], h - tr[1] - br[1]),
            Kit.add_pic(g, base + 0, x, y, mouse=mouse), Kit.add_pic(g, base + 2, x + w - tr[0], y, mouse=mouse),
            Kit.add_pic(g, base + 6, x, y + h - bl[1], mouse=mouse),
            Kit.add_pic(g, base + 8, x + w - br[0], y + h - br[1], mouse=mouse)]
        return [p for p in out if p is not None]

    @staticmethod
    def gold_box(g, x, y, w, h, t=GOLD_T):
        """A gold-edged black box: tiled black fill with a gold border t pixels thick. Returns the controls."""
        out = [Kit.add_tiled(g, Kit.SECTION_TILE, x + t, y + t, w - 2 * t, h - 2 * t)]
        for art, bx, by, bw, bh in ((Kit.GOLD_H, x, y, w, t), (Kit.GOLD_H, x, y + h - t, w, t),
                                    (Kit.GOLD_V, x, y, t, h), (Kit.GOLD_V, x + w - t, y, t, h)):
            out.append(Kit.add_tiled(g, art, bx, by, bw, bh))
        return [p for p in out if p is not None]

    @staticmethod
    def _frame_pieces(g, w, h, corners=True, mouse=True):
        """The stone frame's controls: the nine-piece frame and, with corners, the knot on each corner.
        Returns them.
        """
        out = Kit.add_resizepic(g, Kit.WINDOW_BG, 0, 0, w, h, mouse)
        if corners and Kit.CORNER_ART:
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch:
                for cx, cy in ((0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)):
                    p = Kit.add_pic(g, Kit.CORNER_ART, cx, cy, mouse=mouse)
                    if p is not None:
                        out.append(p)
        # Kept so the one frame can hide or re-fit them; a page canvas has no frame to keep.
        if type(g) is not PageCanvas:
            try:
                Kit._prune(Kit._frame_parts)
                Kit._frame_parts[g] = [p for p in out if p is not None]
            except TypeError:
                pass
        return out

    _frame_want = {}

    @staticmethod
    def frame_show(g, on):
        """Show or hide window g's stone frame (the one frame of a zoned window), and remember the wish."""
        Kit._prune(Kit._frame_want, 32)
        Kit._frame_want[g] = bool(on)
        # A window in the seam bookkeeping has its frame handled there.
        if g in Seam.bare or g in Seam.recs:
            return
        for p in Kit._frame_parts.get(g) or ():
            Kit.set(p, "IsVisible", bool(on))

    @staticmethod
    def frame_fit(g, w, h):
        """Move and size window g's frame pieces for a new w x h without drawing them again.

        Returns False when the pieces cannot be fitted (no frame noted, a scrolling window, or the piece
        count differs), so the caller draws the frame again.
        """
        fr = Kit._frames.get(g)
        s = Kit._rp_sizes.get(Kit.WINDOW_BG)
        if fr is None or s is None or g in Kit._scrolled:
            return False
        tl, t, tr, l, _, r, bl, b, br = s
        cw, ch = Kit.pic_size(Kit.CORNER_ART) if fr["corners"] and Kit.CORNER_ART else (0, 0)
        rects = [(l[0], t[1], w - l[0] - r[0], h - t[1] - b[1]), (tl[0], 0, w - tl[0] - tr[0], t[1]),
                 (bl[0], h - b[1], w - bl[0] - br[0], b[1]), (0, tl[1], l[0], h - tl[1] - bl[1]),
                 (w - r[0], tr[1], r[0], h - tr[1] - br[1]), (0, 0), (w - tr[0], 0), (0, h - bl[1]),
                 (w - br[0], h - br[1])]
        if cw and ch:
            rects += [(0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)]
        if len(fr["pieces"]) != len(rects):
            return False
        for p, rect in zip(fr["pieces"], rects):
            if len(rect) == 4:
                p.SetRect(*rect)
            else:
                p.SetPos(*rect)
        return True

    @staticmethod
    def add_window_frame(g, w, h, corners=True, mouse=True):
        """Draw the stone frame of window g.

        mouse False lets clicks on it reach the window itself (a resizable window is resized by dragging
        its corners). The pieces are noted until the window is placed, so a window taller than the screen
        can have its frame drawn again at the size it gets (Kit.place, scroll_fit); the note goes when the
        window does.
        """
        pieces = Kit._frame_pieces(g, w, h, corners, mouse)
        if type(g) is not PageCanvas:
            Kit._prune(Kit._frames, 32)
            # Closed windows: let their notes go.
            if len(Kit._frames) > 48:
                Kit._frames.clear()
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}

    @staticmethod
    def add_section(g, x, y, w, h, title=None, alpha=None):
        """A translucent black block like each part of the crafting gump, with an optional title in its
        top-left corner. Returns the block.
        """
        # A settings page being laid out: it only records the section.
        if type(g) is PageCanvas:
            g.sections.append((x, y, w, h))
        t = Kit.add_tiled(g, Kit.SECTION_TILE, x, y, w, h, Kit.SECTION_ALPHA if alpha is None else alpha)
        if title:
            Kit.add_label(g, title, x + 8, y + 6, Kit.HUE_TITLE)
        return t

    @staticmethod
    def add_label(g, text, x, y, hue=None):
        """Add a text label at (x, y) in the client's UO font and return it. hue defaults to the text hue."""
        lbl = G.CreateGumpLabel(text, Kit.HUE_TEXT if hue is None else hue)
        lbl.SetPos(x, y)
        g.Add(lbl)
        return lbl

    @staticmethod
    def add_check(g, text, x, y, checked=False, tooltip=None):
        """Add a client checkbox with its caption and return it."""
        # Client checkbox art.
        cb = G.CreateGumpCheckbox(text, Kit.HUE_TEXT, checked)
        cb.SetPos(x, y)
        Kit.with_tip(cb, tooltip)
        g.Add(cb)
        return cb

    @staticmethod
    def add_textbox(g, text, x, y, w=60, numbers=True, font=16):
        """A text field on its tile. numbers makes it numbers-only; font is its font size.

        A window that lays itself out at a scale k and then calls Kit.scale_window passes round(16 * k),
        since the client never scales a field's text (the field's box itself is scaled with the rest).
        """
        Kit.add_tiled(g, Kit.FIELD_TILE, x - 2, y - 1, w + 4, 24)
        tb = G.CreateGumpTextBox(text, w, 22, False, font)
        tb.SetPos(x, y)
        if numbers:
            tb.NumbersOnly = True
        g.Add(tb)
        return tb

    @staticmethod
    def add_slider(g, x, y, w, lo, hi, value):
        """Add a slider from lo to hi at the given value and return it."""
        s = G.CreateSlider(w, lo, hi, int(value), x, y, True)
        g.Add(s)
        return s

    # Set once a click handler has run: clicks do arrive on this build.
    clicks_seen = False

    @staticmethod
    def on_click(ctrl, fn):
        """Hook a click handler that also gets the second click of a double-click.

        fn is called with no arguments, again when the client had swallowed the second click. Every click
        pokes the host, so the window's module (and the settings window) act on it on the very next pass
        instead of their next due tick.
        """
        key = HOST.click_key()

        def handler(*args):
            """Run fn, and again when a second click was swallowed; wake the host afterwards."""
            Kit.clicks_seen = True
            twice = Client.second_click_swallowed()
            try:
                fn()
            finally:
                try:
                    # Replay the click the client kept.
                    if twice:
                        fn()
                finally:
                    HOST.poke(key)

        G.AddControlOnClick(ctrl, handler)

    # Title strip key to (time of its last click, window position) for double-click timing.
    _dbl = {}
    # Double-clicks the client reported itself, waiting for the module's next tick.
    pending = []
    # Key to the time it last ran (see once).
    _fired = {}

    @staticmethod
    def _prune(d, cap=64):
        """Drop the closed windows from a dict keyed by window once it holds more than cap entries."""
        if len(d) > cap:
            for k in [k for k in d if not Kit.is_open(k)]:
                d.pop(k, None)

    @staticmethod
    def _forget_old(d, now, age=5.0):
        """Keep a key-to-time dict (_fired, _dbl) small: a key is often id(window) and every rebuilt window
        brings a new one, while only the last few seconds matter.
        """
        if len(d) > 64:
            for k in [k for k, v in d.items() if now - (v[0] if type(v) is tuple else v) > age]:
                d.pop(k, None)

    # Seconds in which a second click counts as the second half of a double-click.
    TWICE = 0.15

    @staticmethod
    def once(fn, key, gap=0.6):
        """Return a function that runs fn, ignoring a repeat within gap seconds for the same key.

        One double-click can be seen both by our own timing and by the client's own event.
        """
        def run():
            """Run fn unless the same key ran less than gap seconds ago."""
            now = time.time()
            if now - Kit._fired.get(key, 0.0) < gap:
                return
            Kit._fired[key] = now
            Kit._forget_old(Kit._fired, now)
            fn()

        return run

    @staticmethod
    def hook_mouse(api_ctrl, fn, queue=True, event="MouseDoubleClick", button="Left"):
        """Hook a client mouse event (a double-click by default) on a script control, on the client thread.

        fn is queued for the module's next tick when queue is set (else called at once). The handler marks
        the event handled and pokes the host. Returns True when the hook was made. The event type, its
        delegate type and add method are found once per control type.
        """
        try:
            import clr
            import System
            ctrl = Kit.client_control(api_ctrl)
            t0 = ctrl.GetType()
            name = (str(t0.FullName), event)
            found = Kit._dbl_events.get(name)
            if found is None:
                flags = Client.flags()
                t, ev = t0, None
                while t is not None and ev is None:
                    ev = t.GetEvent(event, flags)
                    t = t.BaseType
                found = (ev, clr.GetPythonType(ev.EventHandlerType), ev.GetAddMethod(True))
                if len(Kit._dbl_events) > 64:
                    Kit._dbl_events.clear()
                Kit._dbl_events[name] = found
            ev, delegate_type, add = found

            def handler(sender, e):
                """Handle the mouse event for the chosen button only."""
                try:
                    if str(e.Button) == button:
                        if queue:
                            Kit.pending.append(fn)
                        else:
                            fn()
                        e.Result = True
                        HOST.pressed_at = time.time()
                        HOST.poke()
                except Exception:
                    pass

            add.Invoke(ctrl, System.Array[object]([delegate_type(handler)]))
            return True
        except Exception:
            return False

    # The name some modules call it by.
    hook_double = hook_mouse
    # Control type name and event to (event, delegate type, add method).
    _dbl_events = {}

    @staticmethod
    def on_moved(g, fn):
        """Call fn each time the player has moved window g and let go of it (and when g moved because a
        window it is snapped to was dragged). Use it to save the window's position right away.
        """
        SNAP.on_moved(g, fn)

    @staticmethod
    def moved_by_code(g):
        """Tell the snapping that window g was just placed by code (a tray put beside its bar, a grid under a
        title bar). Without it, on a client where the mouse button cannot be read, every such move counts
        as a drag. Call it right after the move.
        """
        SNAP.moved_by_code(g)
        Kit.stir()

    @staticmethod
    def title_catcher(g, x, y, w, h, fn, key=None):
        """An invisible, draggable strip over a title: double-click it to run fn (minimize or restore).

        A drag also ends in a click, so the window must not have moved between the two clicks. key
        separates the debounce of different strips. Returns the strip. Where the client reports a
        double-click itself, that event is hooked too.
        """
        key = key or id(g)
        once = Kit.once(fn, key)

        def fn():
            """Run the double-click action unless it is the end of a drag."""
            # A click that ended a drag (or came while one is on) is no half of a double-click: a window dragged
            # on to its zone must not be minimized or folded by the click that lets it go.
            if Kit.just_dragged(g):
                Kit._dbl.pop(key, None)
                return
            once()

        def clicked():
            """Time the clicks on the strip: two within 0.7 s, on a window that did not move, make a double-click."""
            now = time.time()
            # See fn above.
            if Kit.just_dragged(g):
                Kit._dbl.pop(key, None)
                return
            pos = (g.GetX(), g.GetY())
            last = Kit._dbl.get(key)
            if last and now - last[0] <= 0.7 and abs(pos[0] - last[1][0]) <= 3 and abs(pos[1] - last[1][1]) <= 3:
                Kit._dbl.pop(key, None)
                fn()
            else:
                Kit._dbl[key] = (now, pos)
                Kit._forget_old(Kit._dbl, now)

        c = Kit.catcher(g, x, y, w, h, clicked, Kit.DOUBLE_TIP, movable=True)
        if Client.mouse is None:
            Kit.hook_double(c, fn)
        return c

    # Seconds after a drag ends in which a click is its own and not a click.
    DRAG_QUIET = 0.4

    @staticmethod
    def just_dragged(g):
        """True while window g is being dragged, or was let go DRAG_QUIET seconds ago or less: a click on it
        is then the end of the drag, not a click.
        """
        try:
            if g in SNAP.drag or g in SNAP.dragged:
                return True
            t = SNAP.drag_end.get(g)
            return t is not None and time.time() - t < Kit.DRAG_QUIET
        except Exception:
            return False

    @staticmethod
    def catcher(g, x, y, w, h, fn, tooltip=None, movable=False):
        """An invisible click target over (x, y, w, h) with an optional tooltip; movable makes it draggable."""
        c = G.CreateGumpColorBox(0.01, "#000000")
        c.SetRect(x, y, w, h)
        Kit.on_click(c, fn)
        Kit.with_tip(c, tooltip)
        if movable:
            c.CanMove = True
        g.Add(c)
        return c

    @staticmethod
    def art_button(g, store, key, art, x, y, label=None, tooltip=None, hue=None, on_click=None):
        """A gump-art button, optionally with a clickable label to its right. Returns the label if there is
        one, else the button.

        store is the (buttons, clicks) pair of the window it belongs to; key names the button in it.
        Clicks are either polled with was_clicked() or handed to on_click. Every button can take a hotkey
        (see Binds), and the hotkey is shown in its tooltip.
        """
        bdict, cdict = store
        b = G.CreateGumpButton("", Kit.HUE_TEXT, art[0], art[1], art[2])
        b.SetPos(x, y)
        g.Add(b)
        bdict[key] = b
        cdict[key] = False
        # Every button can take a hotkey: see Binds.
        bid = Binds.note(store, key, on_click, b, tooltip)

        def clicked(*args):
            """Record the click for polling and call on_click."""
            cdict[key] = True
            if on_click is not None:
                on_click()

        click = Binds.wrap(bid, clicked)
        Kit.on_click(b, click)
        combo = Binds.saved.get(bid)
        if combo:
            tooltip = (tooltip + " " if tooltip else "") + "(hotkey: %s)" % combo
        Kit.with_tip(b, tooltip)
        if label:
            bw, bh = Kit.pic_size(art[0])
            lbl = Kit.add_label(g, label, x + (bw or 30) + 5, y + max(((bh or 22) - 16) // 2, 0), hue)
            lbl.SetAcceptMouseInput(True)
            Kit.on_click(lbl, click)
            return lbl
        return b

    @staticmethod
    def closed(win, key="g"):
        """True (and the window is closed) when the window's Close button was clicked."""
        if not Kit.was_clicked(win["store"], "close"):
            return False
        Kit.dispose(win[key])
        return True

    @staticmethod
    def weight_bar(g, c, bx, by, bw, centre=0):
        """Draw a weight bar: a red track with hidden ok, warn and red fills, kept in c for weight_show.
        centre is the row height to centre the bar in.
        """
        lw, lh = Kit.pic_size(Kit.LINE_RED)
        fh = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or lh or 9))
        if centre:
            by += max(0, (centre - fh) // 2)
        if lw > 0:
            Kit.add_tiled(g, Kit.LINE_RED, bx, by, bw, fh, hue=946)
        else:
            Kit.add_tiled(g, Kit.SECTION_TILE, bx, by, bw, fh, 1.0)
        fills = {}
        for kind, art, hue in (("ok", Kit.LINE_POISON, 0), ("warn", Kit.LINE_BLUE, 0x0035), ("red", Kit.LINE_RED, 0)):
            f = Kit.add_tiled(g, art, bx, by, 1, fh, hue=hue)
            if f is not None:
                f.IsVisible = False
                fills[kind] = f
        c["wfills"] = fills
        c["wbar_w"] = bw

    @staticmethod
    def weight_level(frac, bw):
        """(fill kind, width) for a weight fraction and bar width: ok below 85 per cent, warn from 85, red
        from 95. (None, 0) for a negative fraction (no reading).
        """
        if frac < 0:
            return None, 0
        kind = "red" if frac >= 0.95 else "warn" if frac >= 0.85 else "ok"
        return kind, max(1, min(bw, int(round(bw * min(1.0, frac)))))

    @staticmethod
    def weight_show(fills, kind, width):
        """Show the fill of the given kind at the given width and hide the others."""
        for k, f in fills.items():
            try:
                if k == kind:
                    Kit.ui_w(f, width)
                f.IsVisible = k == kind
            except Exception:
                pass

    _hooks = {}

    @staticmethod
    def hook_once(holder, key, *pairs):
        """Hook client events once per holder key, remembering them for unhook.

        Each pair is (event name, handler). The client's API.Events methods are named On plus the event
        name, so a bare name gets the On prefix here, the same rule unhook uses. holder[key] marks that
        they are hooked; the owner is the current module, so unhook(owner) can undo them.
        """
        if holder[key]:
            return
        holder[key] = True
        owner = HOST.owner_key()
        for event, fn in pairs:
            try:
                getattr(API.Events, event if event.startswith("On") else "On" + event)(fn)
            except Exception:
                continue
            Kit._hooks.setdefault(owner, []).append((event, fn, holder, key))

    @staticmethod
    def unhook(owner):
        """Unregister every client event a module hooked with hook_once, on the client thread, and clear its
        hooked marks. A hook that fails to unregister is kept for another try.
        """
        recs = Kit._hooks.pop(owner, None)
        if not recs:
            return

        def run():
            """Unregister each recorded event handler."""
            for rec in recs:
                event, fn, holder, key = rec
                try:
                    getattr(API.Events, "Unregister" + (event if event.startswith("On") else "On" + event))(fn)
                except Exception:
                    Kit._hooks.setdefault(owner, []).append(rec)
                    continue
                holder[key] = False

        # Quiet: nothing to do if the client refuses.
        with Kit.quiet:
            Kit.on_client(run)

    @staticmethod
    def was_clicked(store, key):
        """True once after a click on the button key of a window's store.

        The click handler's note is enough once handlers are known to run (clicks_seen); until then the
        client's own HasBeenClicked flag is asked as well.
        """
        cdict = store[1]
        hit = cdict.get(key, False)
        if hit:
            cdict[key] = False
        # The usual case: the handler's note is enough.
        if Kit.clicks_seen:
            return hit
        # Until a click handler has run, ask the client.
        ctl = store[0].get(key)
        if ctl is not None:
            try:
                hit = ctl.HasBeenClicked() or hit
            except Exception:
                pass
        return hit

    # What each label shows, as last set: label to [text, hue]. Keyed by the label itself, not id(),
    # which is a slow lookup for a client object and can be reused.
    _texts = {}
    # Labels of closed windows are let go once the dict passes this size; the size then grows with the
    # number still open, so the sweep stays rare.
    _texts_cap = 3000
    # A sweep was put off until the next client pass.
    _texts_sweep = False
    # The labels being swept.
    _texts_list = None
    # Where the sweep is in that list.
    _texts_at = 0
    # Labels checked per client pass.
    TEXTS_SLICE = 400

    @staticmethod
    def set_text(lbl, text, hue=None):
        """Change a label only when needed. Returns True if the text changed.

        What a label shows is remembered here, so nothing is read back from the client after the first
        look (a read waits for the client, a write does not). hue is applied only when given and changed.
        """
        try:
            e = Kit._texts.get(lbl)
        # Unhashable stand-in: not remembered.
        except TypeError:
            e = [None, None]
        if e is None:
            e = Kit._texts[lbl] = [None, None]
            if len(Kit._texts) > Kit._texts_cap:
                Kit._prune_texts()
        changed = e[0] != text
        if changed:
            e[0] = text
            try:
                lbl.Text = text
            except Exception:
                try:
                    lbl.SetText(text)
                except Exception:
                    pass
        if hue is not None and e[1] != hue:
            e[1] = hue
            try:
                lbl.Hue = hue
            except Exception:
                pass
        return changed

    @staticmethod
    def _prune_texts():
        """Drop the labels of closed windows from the text memory, a slice per client pass."""
        # Every IsDisposed read off the client thread is a frame-wait (thousands of them stall the script
        # thread): let the dict grow a little and sweep it on the next client pass instead.
        if not Client.on_client_thread():
            Kit._texts_cap = len(Kit._texts) + 500
            Kit._texts_sweep = True
            return
        # Swept in slices of TEXTS_SLICE labels per client pass (thousands of IsDisposed reads in one frame
        # were a hitch); the cap grows meanwhile.
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

    # Pixel widths of texts, measured once each.
    _widths = {}
    # Script control type to its Control PropertyInfo.
    _ctl_prop = {}
    # Art base to its nine measured sizes (add_resizepic).
    _rp_sizes = {}
    # Seconds between full child counts of a scrolling window at the least (scroll_sweep).
    SWEEP_FULL = 5.0
    # Texts made on the fly would otherwise pile up for the whole session; past this the cache starts over.
    WIDTHS_MAX = 4000

    @staticmethod
    def text_w(text):
        """Pixel width of text in the client's label font, measured once with a label and cached.

        Falls back to eight pixels a character when it cannot be measured.
        """
        px = Kit._widths.get(text)
        if px is None:
            px = 0
            try:
                l = G.CreateGumpLabel(text, Kit.HUE_TEXT)
                px = int(l.GetWidth() or 0)
                Kit.dispose(l)
            except Exception:
                # A failed measure marks the kept client data as bad, so the next start measures afresh.
                Kit._measure["bad"] = True
            px = px or 8 * len(text)
            if len(Kit._widths) >= Kit.WIDTHS_MAX:
                # The long, one-off texts go first; the short ones (letters, captions, numbers) are the ones asked
                # for again and again.
                wd = Kit._widths
                for k in [k for k in wd if len(k) > 12]:
                    del wd[k]
                if len(wd) >= Kit.WIDTHS_MAX // 2:
                    wd.clear()
            Kit._widths[text] = px
        return px

    _wraps = {}

    @staticmethod
    def wrap(text, width):
        """text split into lines no wider than width, cached.

        With letter widths that add up (text_px) a line's width is carried along, so no label is made for
        any candidate line, and the breaks are the same as the measured ones.
        """
        ck = (text, width)
        got = Kit._wraps.get(ck)
        if got is None:
            if len(Kit._wraps) > 600:
                Kit._wraps.clear()
            got = Kit._wraps[ck] = tuple(Kit._wrap_raw(text, width))
        return list(got)

    @staticmethod
    def _wrap_raw(text, width):
        """Split text into lines no wider than width by greedy word fit; at least one line comes back."""
        lines = []
        words = text.split()
        if words and Kit._px["ok"] is None:
            # The one-time font check.
            Kit.text_px("")
        if Kit._px["ok"]:
            pad, cw = Kit._px["pad"], Kit._px_ch
            sp = cw.get(" ")
            if sp is None:
                sp = Kit._ch_w(" ")
            cur = 0
            for word in words:
                # Its letters.
                ww = Kit.text_px(word) - pad
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

    # Text widths as a sum of letter widths: the client's label font has no kerning, so the width of a
    # text is a constant plus the width of each of its letters. Once a letter is known (one measurement)
    # every text made of known letters costs no label at all. Checked once against a measured reference
    # text; if this client's font does not add up, text_px falls back to text_w.
    _px = {"ok": None, "pad": 0}
    # Letter to its measured width.
    _px_ch = {}
    # The reference text the letter-width check measures.
    PX_REF = "Total 120.0 / 700.0 (+5.2) Session ~1h 05m: Magery, Str"

    @staticmethod
    def _ch_w(ch):
        """Width of one letter, measured as the difference two labels make, and remembered."""
        w = Kit.text_w("x" + ch + "x") - Kit.text_w("xx")
        Kit._px_ch[ch] = w
        return w

    @staticmethod
    def text_px(text):
        """Pixel width of text in the label font: the sum of its letters' widths when the font adds up (no
        label made for a text of known letters), else Kit.text_w.
        """
        px = Kit._px
        if px["ok"] is None:
            try:
                px["pad"] = 2 * Kit.text_w("x") - Kit.text_w("xx")
                ref = Kit.PX_REF
                px["ok"] = Kit.text_w(ref) == px["pad"] + sum(Kit._ch_w(ch) for ch in ref)
            except Exception:
                px["ok"] = False
                # A failed measure marks the kept client data as bad, so the next start measures afresh.
                Kit._measure["bad"] = True
        if not px["ok"]:
            return Kit.text_w(text)
        w, cw = px["pad"], Kit._px_ch
        for ch in text:
            x = cw.get(ch)
            w += Kit._ch_w(ch) if x is None else x
        return w

    @staticmethod
    def measure_bind():
        """Bind the measured client data to the entry kept for this process, once, before anything measures.

        The entry sits on the sys module under (app version, process id), so it outlives a Stop of the
        script and a Play in the same client, and is one entry only. Each cache (text widths, letter widths,
        picture sizes, reflected members, client types, texture parts) is the same dict object as the one in
        the entry; a missing or oversized one is replaced by a fresh dict. An entry flagged bad is started
        over. Also restores the client assembly and the queue type from it. Script thread; a failure is
        caught by the caller.
        """
        import sys
        key = (APP_VERSION, os.getpid())
        st = sys.__dict__.get("_VA_MEASURE")
        e = st.get(key) if type(st) is dict else None
        if type(e) is not dict or e.get("bad") is not False:
            e = {"bad": False}
            sys._VA_MEASURE = {key: e}
        for cls, name in ((Kit, "_widths"), (Kit, "_px_ch"), (Kit, "_px"), (Kit, "_sizes"), (Kit, "_rp_sizes"),
                          (Kit, "_ctl_prop"), (Client, "_types"), (Typing, "_members"), (Tz, "_types"), (Tz, "_found"),
                          (Tex, "parts")):
            k = cls.__name__ + "." + name
            d = e.get(k)
            if type(d) is not dict or len(d) > Kit.MEASURE_CAP:
                d = e[k] = cls.__dict__[name]
            setattr(cls, name, d)
        if e.get("asm") is not None:
            Client._client_asm = e["asm"]
        if e.get("mtq") is not None:
            Client.MTQ, Client.mtq_looked = e["mtq"], True
        Tex.ok = True if Tex.parts.get("ok") is True else None
        Kit._measure = e

    @staticmethod
    def fit(text, width, tail=".."):
        """text cut short, with tail after it, when it is wider than width pixels in the label font.

        Uses letter widths when the font adds up, else the longest fitting start found by halving: a few
        labels, not one per letter.
        """
        text = str(text or "")
        if len(text) * 9 <= width or Kit.text_px(text) <= width:
            return text
        # Letters add up: take them off one by one.
        if Kit._px["ok"]:
            w, cw = Kit.text_px(text + tail), Kit._px_ch
            while text and w > width:
                w -= cw.get(text[-1], 0)
                text = text[:-1]
            return text.rstrip() + tail
        # text[:lo] is kept even if it does not fit.
        lo, hi = 1, len(text) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if Kit.text_w(text[:mid] + tail) <= width:
                lo = mid
            else:
                hi = mid - 1
        return text[:lo].rstrip() + tail

    # The commands of a server gump's layout (PacketGumpText): TazUO keeps a gump's text lines, one a
    # line, then the commands, one a line (the last text line and the first command share a line). The
    # parser below lives here so a fix lands once for every module. Basic string operations only:
    # IronPython disagreed with CPython on fancier versions.
    GUMP_CMDS = ("page", "button", "buttontileart", "checkertrans", "croppedtext", "gumppic", "gumppictiled",
                 "gumppichued", "gumppicphued", "htmlgump", "xmfhtmlgump", "xmfhtmlgumpcolor", "xmfhtmltok", "noclose",
                 "nodispose", "nomove", "noresize", "group", "endgroup", "radio", "checkbox", "resizepic", "text",
                 "textentry", "textentrylimited", "tilepic", "tilepichue", "tooltip", "itemproperty", "mastergump",
                 "picinpic", "picinpichued", "picinpicphued", "togglelimitgumpscale", "maparea")
    _gump_cmds = frozenset(GUMP_CMDS)
    _cliloc_cache = {}

    @staticmethod
    def gump_is_int(a):
        """True for a (possibly negative) whole number."""
        a = str(a)
        if a.startswith("-"):
            a = a[1:]
        return len(a) > 0 and a.isdigit()

    @staticmethod
    def _gump_arg_ok(a):
        """A command argument: an integer, a #cliloc, a name=value option (gumppic's hue=N or class=Name) or
        an @text@ argument.
        """
        if Kit.gump_is_int(a):
            return True
        if a.startswith("#"):
            return Kit.gump_is_int(a[1:])
        if "=" in a:
            return a.split("=", 1)[0].isalnum()
        return a.startswith("@") or a.endswith("@")

    @staticmethod
    def gump_is_cmd(line):
        """Is this line a gump command?

        Its first word must be a command AND every other token an integer, a #cliloc or part of an @text@
        argument: a text line that merely starts with such a word ("Page 2 Boss", "Text me", "Group
        leader") is text.
        """
        words = str(line).strip().split()
        if not words or words[0].lower() not in Kit._gump_cmds:
            return False
        # Inside an @...@ argument with spaces.
        inside = False
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
        """The last text line and the first command arrive glued together: pull them apart. Returns (text,
        command) or (text, None).
        """
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
        """Split a gump's PacketGumpText into (text lines, command token lists).

        Trailing blank lines are dropped, then lines from the end that parse as commands are taken as the
        command block; the line before it may hold the last text line glued to the first command, which
        _gump_split_merged pulls apart.
        """
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
            # The last text line was empty.
            if first is None:
                lines, cmds = parts[:j] + [""], parts[j:]
            else:
                lines, cmds = parts[:j - 1] + [tail], [first] + parts[j:]
        return lines, [c.split() for c in cmds]

    # Compiled once.
    _HTML_RE = re.compile(r"<[^>]*>")

    @staticmethod
    def strip_html(s):
        """text with HTML tags and non-breaking spaces removed, stripped."""
        return Kit._HTML_RE.sub("", str(s or "")).replace("&nbsp;", " ").strip()

    @staticmethod
    def cliloc_text(n, clilocs=None):
        """The client's text of cliloc number n.

        The caller's own table (clilocs, number to text) is asked first, then API.GetClilocString when
        the build has it (remembered, the cache restarts past 500 entries), else the text "#n".
        """
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

    # Per gump command: (least tokens, text index, cliloc index, background index, sized) - where in
    # the command each part sits, for gump_cells.
    _CELLS = {"htmlgump": (8, 5, None, 6, 1), "xmfhtmlgump": (8, None, 5, 6, 1), "xmfhtmlgumpcolor": (8, None, 5, 6, 1),
              "xmfhtmltok": (9, None, 8, 5, 1), "text": (5, 4, None, None, 0), "croppedtext": (7, 6, None, None, 1)}

    @staticmethod
    def gump_cells(raw, clilocs=None):
        """The texts of a gump and its reply buttons.

        Returns (cells, buttons). A cell is {"x", "y", "w", "h", "text", "raw", "cliloc", "bg"} with the
        text's HTML stripped and raw as sent; buttons are [(x, y, id)] for reply buttons. Text controls
        read are htmlgump (text index), xmfhtmlgump and xmfhtmlgumpcolor (cliloc), xmfhtmltok (cliloc
        plus arguments), and text and croppedtext (text index). clilocs is an own number-to-text table
        looked at before the client's (see cliloc_text). A malformed command is skipped.
        """
        lines, cmds = Kit.gump_parse(raw)
        cells, buttons = [], []
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "button" and len(t) >= 8:
                    if int(t[5]) == 1:
                        buttons.append((int(t[1]), int(t[2]), int(t[7])))
                    continue
                r = Kit._CELLS.get(k)
                if r is None or len(t) < r[0]:
                    continue
                li, ci, bi, sized = r[1:]
                src = "" if li is None else lines[int(t[li])]
                cl = 0 if ci is None else int(str(t[ci]).replace("#", ""))
                cells.append({"x": int(t[1]), "y": int(t[2]), "w": int(t[3]) if sized else 0,
                              "h": int(t[4]) if sized else 0, "raw": src,
                              "text": Kit.strip_html(src) if ci is None else Kit.cliloc_text(cl, clilocs),
                              "cliloc": cl, "bg": bi is not None and int(t[bi]) != 0})
            except (ValueError, IndexError):
                continue
        return cells, buttons

    @staticmethod
    def dispose(ctrl):
        """Dispose a client control, ignoring None and any failure.

        Disposing a window that snaps (a member of SNAP) counts as window activity (Kit.stir).
        """
        if ctrl is not None:
            if ctrl in SNAP.members:
                Kit.stir()
            try:
                ctrl.Dispose()
            except Exception:
                pass

    @staticmethod
    def is_open(g):
        """True when g exists and is not disposed."""
        if g is None:
            return False
        try:
            return not g.IsDisposed
        except Exception:
            return False

    # Cache of the per-character values read or written.
    _vars = {}

    @staticmethod
    def get_var(key, default=""):
        """A per-character saved string, or default when unset or unreadable.

        Read from the persistent variables once, then served from a cache (cleared past 3000 entries).
        """
        v = Kit._vars.get(key)
        if v is None:
            try:
                v = str(API.GetPersistentVar(key, "", API.PersistentVar.Char) or "")
            except Exception:
                return str(default)
            if len(Kit._vars) > 3000:
                Kit._vars.clear()
            Kit._vars[key] = v
        return v or str(default)

    @staticmethod
    def put_var(key, value, loud=False):
        """Save a per-character string, skipping the write when it is unchanged.

        loud lets a failure to save raise; otherwise it is ignored. The cache takes the new value.
        """
        v = str(value)
        if Kit._vars.get(key) == v:
            return
        Kit._vars.pop(key, None)
        if loud:
            API.SavePersistentVar(key, value, API.PersistentVar.Char)
        else:
            with Kit.quiet:
                API.SavePersistentVar(key, value, API.PersistentVar.Char)
                Kit._vars[key] = v
            return
        Kit._vars[key] = v

    # The settings folder, worked out once.
    _data_dir = [None]
    # Files older layouts kept beside the script, moved into the settings folder once by data_setup.
    # The pattern includes a save's temporary copy ("name.tmp", "name.pid.tmp").
    DATA_MOVE = re.compile(r"^(_ultima_tracker_data\.txt|_lookout_feed\.txt|_unified_bag_\d+\.cfg"
                           r"|_storage_index_[^\\/]+?\.txt|_swing_timer_\d+\.txt"
                           r"|Skills_[0-9A-F]{8}\.txt|SkillBags_[0-9A-F]{8}_rule\d+\.txt"
                           r"|Meters_[0-9A-F]{8}\.txt|Grimoire_saved\.txt" r"|Grimoire_runebook_dump\.txt)"
                           r"(\.\d+)?(\.tmp)?$")
    # Grimoire's files were kept in LegionScripts itself, wherever this script was.
    DATA_MOVE_ROOT = re.compile(r"^(Grimoire_saved\.txt|Grimoire_runebook_dump\.txt)$")

    @staticmethod
    def script_dir():
        """The folder this script runs from, an empty string when it cannot be told.

        When the path points into a module folder (a name ending in Modules), its parent is used.
        """
        base = str(API.ScriptPath or "").rstrip("/\\")
        if base and os.path.isfile(base):
            base = os.path.dirname(base)
        if base.endswith("Modules"):
            base = os.path.dirname(base)
        return base or safe(Kit._legion_root, "")

    @staticmethod
    def _legion_root():
        """The LegionScripts folder under the client's base directory."""
        import System
        return os.path.join(str(System.AppDomain.CurrentDomain.BaseDirectory), "LegionScripts")

    @staticmethod
    def data_dir():
        """The VirtueAssistantSettings folder beside this script, worked out once. data_setup makes it at
        start; if it could not be made the script's own folder is used.
        """
        d = Kit._data_dir[0]
        if d is None:
            base = Kit.script_dir()
            d = Kit._data_dir[0] = os.path.join(base, SETTINGS_DIR) if base else SETTINGS_DIR
        return d

    @staticmethod
    def data_path(name):
        """Where the data file name lives, in the settings folder. No disk work: call it anywhere."""
        return os.path.join(Kit.data_dir(), name)

    @staticmethod
    def write_safe(path, text, enc="utf-8", tail=None):
        """Write a file so a crash or a second client never leaves it half written. Returns True.

        The text (or bytes) goes to a temporary file named after this process and thread, tail() may
        return extra bytes to append, then the file replaces the target; if the replace fails three times
        the old file is renamed aside and restored when the rename fails too. A failure removes the
        temporary file and raises. A non-empty write is remembered in _seen for read_merge.
        """
        try:
            import _thread
            tmp = "%s.%d.%d.tmp" % (path, os.getpid(), _thread.get_ident())
        except Exception:
            tmp = "%s.%d.tmp" % (path, id(text))
        import io
        try:
            if isinstance(text, bytes):
                with io.open(tmp, "wb") as f:
                    f.write(text)
            else:
                with io.open(tmp, "w", encoding=enc, newline="") as f:
                    f.write(text)
            more = tail() if tail is not None else None
            if more:
                with io.open(tmp, "ab") as f:
                    f.write(more)
        except Exception:
            safe(lambda: os.remove(tmp))
            raise
        done = False
        for _ in range(3):
            try:
                os.replace(tmp, path)
                done = True
                break
            except Exception:
                pass
        if not done:
            bak = tmp + ".bak"
            had = os.path.exists(path)
            try:
                if had:
                    os.rename(path, bak)
                os.rename(tmp, path)
            except Exception:
                if had and os.path.exists(bak):
                    if os.path.exists(path):
                        safe(lambda: os.remove(bak))
                    else:
                        safe(lambda: os.rename(bak, path))
                safe(lambda: os.remove(tmp))
                raise
            if had:
                safe(lambda: os.remove(bak))
        if text:
            Kit._seen.add(os.path.normcase(os.path.abspath(path)))
        return True

    # Files this process has written or read non-empty, by normalised path.
    _seen = set()
    # Path to the time it was first found missing.
    _gone = {}
    # Seconds a file that was seen before and has vanished is waited for.
    MISS_WAIT = 5.0

    @staticmethod
    def read_merge(path):
        """Read a file for a read-merge-write save.

        Returns "" for a file that never existed, the text otherwise, and None when it cannot be read or
        when a file seen earlier is missing: another client may be replacing it, so for MISS_WAIT seconds
        the caller must not write. After that the file is taken as gone.
        """
        key = os.path.normcase(os.path.abspath(path))
        if not os.path.exists(path):
            if key not in Kit._seen:
                return ""
            now = time.time()
            t = Kit._gone.setdefault(key, now)
            if now - t < Kit.MISS_WAIT:
                return None
            Kit._seen.discard(key)
            Kit._gone.pop(key, None)
            return ""
        Kit._gone.pop(key, None)
        text = Kit.read_safe(path)
        if text:
            Kit._seen.add(key)
        return text

    @staticmethod
    def read_safe(path, missing=""):
        """The text of a file read as UTF-8 (a BOM is dropped). The missing value when there is no file;
        None when it cannot be read.
        """
        try:
            if not os.path.exists(path):
                return missing
            import io
            with io.open(path, "r", encoding="utf-8-sig") as f:
                return f.read()
        except Exception:
            return None

    @staticmethod
    def merge_text(text, entries, key_of, sep="\n"):
        """Merge entries into delimited text. Returns (joined text, list of entries).

        Entries already in the text are kept in order; one whose key (key_of(entry)) is in entries is
        replaced in place, a new key is appended, and an entry of None deletes the key. Blank entries are
        dropped and a repeated key in the text keeps its last line.
        """
        out, at = [], {}
        for e in (text or "").split(sep):
            e = e.rstrip("\r")
            if not e.strip():
                continue
            k = key_of(e)
            if k is not None and k in at:
                out[at[k]] = e
                continue
            if k is not None:
                at[k] = len(out)
            out.append(e)
        for k, e in entries.items():
            if k in at:
                out[at[k]] = e
            elif e is not None:
                at[k] = len(out)
                out.append(e)
        out = [e for e in out if e is not None]
        return sep.join(out), out

    @staticmethod
    def merge_save(path, entries, key_of, sep="\n"):
        """Read-merge-write a shared data file: entries (key to line, None to delete) are merged into what
        is on disk and the file is written again.

        Returns the merged list, or None when the file could not be read safely (nothing is written then,
        see read_merge). Two clients saving the same file keep each other's entries.
        """
        text = Kit.read_merge(path)
        if text is None:
            return None
        merged, out = Kit.merge_text(text, entries, key_of, sep)
        Kit.write_safe(path, merged + sep if out else "")
        return out

    @staticmethod
    def data_setup():
        """Once at start, on the script's thread, before any module loads: bind the measured client data
        (measure_bind), make the settings folder and move into it the files an older layout left beside this
        script (Grimoire's from LegionScripts) and the profiles folder.

        A file already in the folder is never written over; the older copy stays where it is. One journal
        line says how many files moved, and one when some could not.
        """
        safe(Kit.measure_bind)
        base, d = Kit.script_dir(), Kit.data_dir()
        try:
            if not os.path.isdir(d):
                os.makedirs(d)
        except Exception as ex:
            # Files stay beside the script.
            Kit._data_dir[0] = base or ""
            Kit.say("couldn't make the %s folder (%s); saving beside the script." % (SETTINGS_DIR, ex), Kit.HUE_BAD)
            return
        moved, failed = 0, 0
        places = [(base, Kit.DATA_MOVE)] if base else []
        root = safe(Kit._legion_root, "")
        norm = lambda p: os.path.normcase(os.path.abspath(p)) if p else ""
        if root and norm(root) != norm(base):
            places.append((root, Kit.DATA_MOVE_ROOT))
        for place, pat in places:
            try:
                names = os.listdir(place)
            except Exception:
                continue
            for n in names:
                if not pat.match(n):
                    continue
                src, dst = os.path.join(place, n), os.path.join(d, n)
                try:
                    if not os.path.isfile(src) or os.path.exists(dst):
                        continue
                    os.rename(src, dst)
                    moved += 1
                except Exception:
                    failed += 1
        if base:
            src, dst = os.path.join(base, PROFILE_DIR), os.path.join(d, PROFILE_DIR)
            try:
                if os.path.isdir(src) and not os.path.exists(dst):
                    os.rename(src, dst)
                    moved += 1
            except Exception:
                failed += 1
        if moved:
            Kit.say("moved %s into the %s folder." % (Kit.count(moved, "saved file"), SETTINGS_DIR), Kit.HUE_INFO)
        if failed:
            Kit.say("couldn't move %s into the %s folder (open in another client?)." % (
                Kit.count(failed, "saved file"), SETTINGS_DIR), Kit.HUE_BAD)

    @staticmethod
    def load_pos(key, default=(200, 200), size=None):
        """A window place saved with save_pos, as (x, y) adapted to the screen of today (Kit.adapt).

        With size=(w, h) it is also kept wholly on screen. default is used when nothing is saved.
        """
        try:
            x, y = Kit.get_var(key, "%d,%d" % default).split(",")
            x, y = int(x), int(y)
        except Exception:
            x, y = default
        w, h = size if size else (0, 0)
        return Kit.adapt(x, y, w, h)

    @staticmethod
    def load_min(key):
        """Was the window minimized when last saved? (see save_min)"""
        return Kit.get_var(key, "0") == "1"

    @staticmethod
    def save_min(key, minimized):
        """Remember whether the window is minimized, saved the moment it changes."""
        Kit.put_var(key, "1" if minimized else "0")

    @staticmethod
    def save_pos(key, g):
        """Save window g's place under key as "x,y", unless g is closed, held by the layout in a zone, or
        parked at the screen's left tab (a parked window keeps its last real place).
        """
        if Kit.is_open(g) and g not in LAYOUT.held and g.GetX() > TAB_X // 2:
            Kit.put_var(key, "%d,%d" % (g.GetX(), g.GetY()))

    @staticmethod
    def queuer(st):
        """Make the queue for a module's window: st["queue"] is the list the module's tick drains.

        Returns queue(action, dup=False), which gives a click handler that adds action to st["queue"] (once
        unless dup) so clicks never do the work themselves. queue.add(action, dup, front, cap, key) adds
        directly; it skips an action already queued, or a full queue (cap), puts it first with front, and
        pokes the host when called outside a host pass.
        """
        def add(action, dup=False, front=False, cap=None, key=None):
            """Add an action to the queue, wake the host when needed, and say whether it was added."""
            q = st["queue"]
            if not dup and action in q or cap is not None and len(q) >= cap:
                return False
            if front:
                q.insert(0, action)
            else:
                q.append(action)
            if key is not None and (HOST.draining or not HOST.in_hop):
                HOST.poke(key)
            return True

        def queue(action, dup=False):
            """Return a click handler that queues action."""
            key = HOST.click_key()

            def handler(*args):
                """Queue the action on a click."""
                add(action, dup, key=key)

            return handler

        queue.add = add
        return queue

    @staticmethod
    def disposer(key, st, win):
        """Make on_disposed(g): a window g going away turns module key off.

        Not when the module replaced the window itself (win["g"] moved on) or is shutting down
        (st["shutting"]).
        """
        def on_disposed(g):
            """Return the handler for window g's disposal."""
            def handler(*args):
                """Turn the module off when its current window was disposed from outside."""
                if win["g"] is g and not st["shutting"]:
                    win["g"] = None
                    HOST.disable(key)

            return handler

        return on_disposed

    # Pixels between the title and the first button, between two captioned buttons, and between two
    # buttons drawn without captions.
    TITLE_GAP = 6
    CAP_GAP = 10
    BARE_GAP = 4

    @staticmethod
    def caption_tip(caption, tip):
        """A button's tooltip when its caption cannot be shown: the caption first, then the tooltip
        (Settings: open the Bags settings page).
        """
        tip = str(tip or "")
        if not tip:
            return caption
        return "%s: %s%s" % (caption, tip[:1].lower(), tip[1:])

    @staticmethod
    def title_plan(w, title, buttons, after=None):
        """Work out how a title row fits w pixels.

        Returns (captions shown, show the after label, the title as drawn, x of every button from the
        right, leftmost x). buttons is [(caption, ...)] from the right, left of Settings' place. The
        captions go first (each button then drawn as its art alone, from the right), then the grey label
        after the title, then the title itself is cut with Kit.fit.
        """
        M = Kit.MARGIN
        # Settings' right end (its caption's end).
        right = w - M - 84 - Kit.DOCK_DX
        t0 = M + 30
        caps_w = [35 + Kit.text_w(b[0]) for b in buttons]

        def xs(with_caps):
            """The x of each button from the right, with or without captions."""
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
        # A row narrower than its buttons: the leftmost go, never off the window.
        while pos and pos[-1] < M + 4:
            pos.pop()
        left = pos[-1] if pos else right
        room = left - Kit.TITLE_GAP - t0
        # No room for even a cut title.
        T = title.upper() if tw <= room else "" if room < Kit.text_w("W..") else Kit.fit(title.upper(), room)
        return False, False, T, pos, left

    @staticmethod
    def title_bar(g, store, w, title, key, on_min, on_dock, on_settings=None, close_tip=None, extra=None, after=None):
        """The title section of a full window: the upper-case title, a double-click strip, then (right to
        left) Close, Minimize, Fold into the Action Bar and, with on_settings, Settings.

        Returns the x where the buttons start, for more buttons to the left of them. close_tip is the
        Close tooltip when Kit.CLOSE_TIP is not right. extra is [(key, art, caption, tooltip, on_click)]
        buttons left of Settings, right to left; after is a grey label right after the title (a count such
        as "BAGS  8"). The row fits its width (Kit.title_plan): when the captions do not all fit, every
        captioned button is drawn without its caption and its tooltip starts with the caption; still too
        tight, the title is cut and its whole text goes on the strip's tooltip.
        """
        M = Kit.MARGIN
        Kit.add_section(g, M, M, w - 2 * M, 30)
        buttons = []
        if on_settings is not None:
            buttons.append(("Settings", "settings", Kit.ART_PAGE, Kit.SETTINGS_TIP % title, on_settings))
        for b in (extra or ()):
            buttons.append((b[2], b[0], b[1], b[3], b[4]))
        # A window in a zone is always up: no Minimize, Close or fold arrow and no double-click; its own
        # buttons move right into their room.
        zoned = Kit.zone_up(key)
        shift = (84 + Kit.DOCK_DX - 10) if zoned else 0
        caps, show_after, shown, pos, left = Kit.title_plan(w + shift, title, buttons, after)
        Kit.add_label(g, shown, M + 30, M + 7, Kit.HUE_TITLE)
        if show_after:
            Kit.add_label(g, after, M + 30 + Kit.text_w(shown) + 8, M + 7, Kit.HUE_INFO)
        # Dragged in Arrange mode; nothing to double-click.
        if zoned:
            strip = Kit.catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, lambda *a: None, None, movable=True)
        else:
            strip = Kit.title_catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, on_min, key=key)
        # Cut: the whole title goes on the strip's tooltip.
        if shown != title.upper():
            Kit.with_tip(strip, title if zoned else "%s. %s" % (title, Kit.DOUBLE_TIP))
        for (cap, bkey, art, tip, fn), x in zip(buttons, pos):
            Kit.art_button(g, store, bkey, art, x, M + 4, cap if caps else None,
                           tip if caps else Kit.caption_tip(cap, tip), on_click=fn)
        if not zoned:
            Kit.dock_button(g, store, w - M - 74, M + 7, on_click=on_dock)
            Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP, on_click=on_min)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None,
                           close_tip or Kit.CLOSE_TIP % title)
        return pos[-1] if pos else w - M - 84 - Kit.DOCK_DX + shift

    @staticmethod
    def zone_up(key):
        """True when window key sits in a layout zone: it is always up, at the slot's size."""
        return bool(HOST.layout_holds(key))

    # The client's Mouse.Position getter; False when it is not available.
    _mouse = [None]

    @staticmethod
    def mouse_pos():
        """(x, y) of the mouse in gump pixels, or None when the client will not say. Client thread."""
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
            # The space the client hit-tests gumps in.
            return int(p.X), int(p.Y)
        except Exception:
            return None

    @staticmethod
    def mini_bar(g, store, w, h, title, key, on_restore, text="", hue=None, close_tip=None):
        """A minimized window: a small stone bar with one section, a label (returned), a double-click strip,
        and the Restore and Close buttons.
        """
        Kit.add_window_frame(g, w, h, corners=False)
        Kit.add_section(g, 8, 8, w - 16, h - 16)
        lbl = Kit.add_label(g, text, 18, 15, Kit.HUE_INFO if hue is None else hue)
        # Its own double-click key: sharing the full window's key would let the debounce after a
        # double-click that minimized swallow the restoring double-click.
        Kit.title_catcher(g, 8, 8, w - 70, h - 16, on_restore, key=str(key) + ":mini")
        Kit.art_button(g, store, "restore", Kit.ART_RESTORE, w - 60, 15, None, Kit.RESTORE_TIP, on_click=on_restore)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - 44, 12, None, close_tip or Kit.CLOSE_TIP % title)
        return lbl

    @staticmethod
    def dock_button(g, store, x_min, y_min, on_click=None, key="tobar"):
        """The Fold into the Action Bar button, placed DOCK_DX pixels left of a Minimize arrow drawn at
        (x_min, y_min). Its click should end in HOST.dock_to_bar(module key) on the module's tick.
        """
        return Kit.art_button(g, store, key, Kit.ART_DOCK, x_min - Kit.DOCK_DX,
                              y_min + Kit.DOCK_DY, None, Kit.DOCK_TIP, on_click=on_click)

    @staticmethod
    def dock_hooks(title, icon, st, win, redraw, fit=None):
        """Build the dock-registry hooks (see Host.dock_add) for a module whose window is win["g"] and whose
        "minimized", "docked" and "shutting" flags are in st.

        redraw() rebuilds the window on the module's next pass. "minimize" is the window's own minimized
        form (not folded), used by HOST.dock_to_bar while the Action Bar is not on screen. For the
        layout's zone fill: fit is fn(w, h, mode) and says the module lays the window out itself for its
        slot in a zone, w x h pixels; it is called with (None, None, None) when the window is freed, runs
        on the client thread in the keeper's pass, and must record and queue a rebuild, never wait. A
        module that then makes the window exactly w x h adds hooks["exact"] = True; without it the layout
        fits the rest (Fill), as it does every window without "fit". hooks["fill"] is "grid" or "frame"
        (see Fill).
        """
        def state():
            """The window's state for the dock: "docked", "minimized", "open", or None with no window or when
            shutting down.
            """
            if win["g"] is None or st["shutting"]:
                return None
            return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")

        def to(docked, minimized):
            """Return a function that sets the docked and minimized flags and redraws."""
            def f():
                """Set the flags and redraw."""
                st["docked"], st["minimized"] = docked, minimized
                redraw()

            return f

        def undock():
            """Show the window again from the Action Bar's tray."""
            st["docked"] = False
            redraw()

        hooks = {"title": title, "icon": icon, "state": state, "show": to(False, False), "dock": to(True, True),
                 "undock": undock, "minimize": to(False, True), "gump": lambda: win["g"], "redraw": redraw}
        if fit is not None:
            hooks["fit"] = fit
        return hooks

    @staticmethod
    def add_front(g, hidden=False):
        """Add gump g to the screen in front of the other windows and return what G.AddGump returns.

        The client's queued control changes are run first (Kit.flush), so the gump is added with its
        controls in place. hidden starts it invisible. Client thread.
        """
        Kit.flush()
        if hidden:
            g.IsVisible = False
        return G.AddGump(g)

    _stack = {"off": False}

    @staticmethod
    def replace_gump(old, g, hidden=False):
        """Add the rebuilt window g and give it the old window's place in the stacking order.

        old is the window being replaced (it is disposed by the caller afterwards). When old is still open,
        g is moved in the client's gump list to sit directly in front of it, so a rebuilt window does not
        jump to the top of the other windows. Does nothing extra when the start-up order setting is off
        (Host.ORDER_OFF in HOST.tz_off), off the client thread, or after the first failure to reach the
        client's list. Returns what Kit.add_front returns.
        """
        r = Kit.add_front(g, hidden)
        st = Kit._stack
        if st["off"] or Host.ORDER_OFF in HOST.tz_off or not Kit.is_open(old) or not Client.on_client_thread():
            return r
        try:
            ro, rn = Kit._raw_gump(old), Kit._raw_gump(g)
            if ro is None or rn is None:
                return r
            uim = Tz.T("ClassicUO.Game.Managers.UIManager")
            gumps = Tz.get(None, "Gumps", uim)
            same = Kit._same()
        except Exception:
            st["off"] = True
            return r
        try:
            # The client keeps its windows in a linked list with the topmost first: take the new window out and
            # put it back just in front of the old one.
            node, new, at, n = gumps.First, None, None, 0
            while node is not None and n < 2000 and (new is None or at is None):
                v = node.Value
                if new is None and same(v, rn):
                    new = node
                elif at is None and same(v, ro):
                    at = node
                node = node.Next
                n += 1
            if new is None or at is None or (new.Next is not None and same(new.Next.Value, ro)):
                return r
            gumps.Remove(new)
            try:
                gumps.AddBefore(at, new)
            except Exception:
                gumps.AddFirst(new)
            # Tell the client the list changed and which window is on top, or it keeps using its old order.
            Tz.put(None, "_gumpsStructureVersion", int(Tz.get(None, "_gumpsStructureVersion", uim)) + 1, uim)
            Tz.put(None, "TopMostControl", gumps.First.Value, uim)
        except Exception:
            pass
        return r

    @staticmethod
    def flush():
        """Run the client's queued control changes now. Client thread only.

        SetPos, SetRect and Add on a control are queued by the client and run on a later frame, while
        GetX and GetY answer at once, so anything that reads a freshly made control's place or children
        must call this first. True when the queue is empty afterwards.
        """
        MTQ = Client._find_mtq()
        if MTQ is None or not Client.on_client_thread():
            return False
        try:
            n = 0
            while int(MTQ.Count) > 0 and n < 500:
                # Each call processes a slice of queued work; the loop is bounded.
                MTQ.ProcessQueue()
                n += 1
            return int(MTQ.Count) == 0
        except Exception:
            return False

    @staticmethod
    def client_control(api_ctrl):
        """The client's own control behind a script control, or None.

        The Control property is looked up once per script control type (a type's members do not change
        while the game runs).
        """
        try:
            pt = type(api_ctrl)
            cache = Kit._ctl_prop
            prop = cache.get(pt, False)
            if prop is False:
                prop = None
                import clr
                flags = Client.flags()
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
        """(controls to leave alone, the scroll area) of a window the scroll conversion touched.

        Its new frame and band pieces, the scroll area and the client's own scrollbar inside it were made
        at the size the window has, and are never scaled; the area's other children (the window's body)
        are.
        """
        info = Kit._scrolled.get(g)
        if info is None:
            return [], None
        # Resolved once per conversion.
        base = info.get("skip_raw")
        if base is None:
            base = [pr for pr in map(Kit.client_control, info["frame"] + info["band"]) if pr is not None]
            info["skip_raw"] = base
        skip = list(base)
        area = info["area_raw"]
        try:
            kids = area.Children
            if int(kids.Count) > 0:
                # The client's scrollbar.
                skip.append(kids[0])
        except Exception:
            pass
        return skip, area

    @staticmethod
    def walk(g, fn, root=None):
        """Call fn on every control inside window g, depth first, starting under root (default: the
        window's own client control).

        fn(control) may return False to skip that control's children. Returns True when the walk ran,
        False when the window has no client control or the tree could not be read. Client thread.
        """
        root = Kit.client_control(g) if root is None else root
        if root is None:
            return False

        def tree(c):
            """Visit one control, then its children (unless fn said to skip them)."""
            if fn(c) is False:
                return
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
    def scale_window(g, scale):
        """Draw everything in window g at scale (1.0 is as built), using the client's own control scaling
        (the one its paperdoll and skills windows use) on every control and what is inside it.

        The window's own size is set by the caller. Call it on a freshly built window; calling it again
        scales only the controls added since (a control already at that scale is left alone), and the
        pieces of a scroll conversion are never touched. True if it worked.
        """
        if abs(scale - 1.0) < 0.001:
            return True
        root = Kit.client_control(g)
        # The controls are added by the queue.
        if root is None or not Kit.flush():
            return False
        skip, area = Kit._scroll_skip(g)
        same = Kit._same()

        def one(c):
            """Scale one control: skip the scroll conversion's own pieces and its scroll area, scale the rest."""
            if skip and any(same(c, k) for k in skip):
                return False
            if area is None or not same(c, area):
                # Tiled pictures must scale their texture too, or the tile pattern stays at the old size.
                if str(c.GetType().Name) == "GumpPicTiled":
                    Kit.set(c, "ScaleTiledTexture", True)
                c.ApplyScale(scale, True, True, False)

        return Kit.walk(g, one, root)

    @staticmethod
    def ui_pos(c, x, y):
        """Move a control after the window was drawn.

        A window in a zone is fitted to its slot (Fill), so its controls are not where the module put
        them. A module that moves or resizes a control after drawing it uses these ui_* helpers, which pass
        the change through the window's fit and set it as it is when the window is not fitted. ui_y reads
        back the place the module gave.
        """
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, x=x, y=y)):
            c.SetPos(int(x), int(y))

    @staticmethod
    def ui_rect(c, x, y, w, h):
        """Place and size a control through the window's fit."""
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, x, y, w, h)):
            c.SetRect(int(x), int(y), int(w), int(h))

    @staticmethod
    def ui_w(c, w):
        """Set a control's width through the window's fit."""
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, w=w)):
            c.SetWidth(int(w))

    @staticmethod
    def ui_size(c, w, h):
        """Set a control's width and height through the window's fit."""
        if c is None:
            return
        if not (Fill.recs and Fill.change(c, w=w, h=h)):
            c.SetWidth(int(w))
            c.SetHeight(int(h))

    @staticmethod
    def ui_y(c):
        """The y of a control as its module gave it (before any zone fit), else the client's."""
        own = Fill.own(c) if Fill.recs else None
        return own[1] if own is not None else c.GetY()

    SPELL_WORDS, MAGERY, CAST_DELAY_OTHER = {}, [], {}
    # The spell table, built once when the class is made from one compact string: spells are separated
    # by semicolons and each is "words,name,reagents,kind" for Magery (reagent abbreviations, and kind
    # heal, cure or cure+ for the spells Meters counts as healing and cures), or "words,name,seconds,
    # kind" for the other schools (cast seconds). Magery is listed circle by circle, eight spells each.
    for _r in ("uus jux,Clumsy,BM NS,;in mani ylem,Create Food,GA GI MR,;rel wis,Feeblemind,GI NS,;"
               "in mani,Heal,GA GI SS,heal;in por ylem,Magic Arrow,SA,;in lor,Night Sight,SS SA,;"
               "flam sanct,Reactive Armor,GA SS SA,;des mani,Weaken,GA NS,;ex uus,Agility,BM MR,;"
               "uus wis,Cunning,MR NS,;an nox,Cure,GA GI,cure;an mani,Harm,NS SS,;in jux,Magic Trap,GA SS SA,;"
               "an jux,Magic Untrap,BM SA,;uus sanct,Protection,GA GI SA,;uus mani,Strength,MR NS,;"
               "rel sanct,Bless,GA MR,;vas flam,Fireball,BP,;an por,Magic Lock,BM GA SA,;in nox,Poison,NS,;"
               "ort por ylem,Telekinesis,BM MR,;rel por,Teleport,BM MR,;ex por,Unlock,BM SA,;"
               "in sanct ylem,Wall of Stone,BM GA,;vas an nox,Arch Cure,GA GI MR,cure+;"
               "vas uus sanct,Arch Protection,GA GI MR SA,;des sanct,Curse,GA NS SA,;in flam grav,Fire Field,BP SS SA,;"
               "in vas mani,Greater Heal,GA GI MR SS,heal;por ort grav,Lightning,MR SA,;ort rel,Mana Drain,BP MR SS,;"
               "kal ort por,Recall,BP BM MR,;in jux hur ylem,Blade Spirits,BP MR NS,;an grav,Dispel Field,BP GA SS SA,;"
               "kal in ex,Incognito,BM GA NS,;in jux sanct,Magic Reflection,GA MR SS,;"
               "por corp wis,Mind Blast,BP MR NS SA,;an ex por,Paralyze,GA MR SS,;in nox grav,Poison Field,BP NS SS,;"
               "kal xen,Summon Creature,BM MR SS,;an ort,Dispel,GA MR SA,;corp por,Energy Bolt,BP NS,;"
               "vas ort flam,Explosion,BM MR,;an lor xen,Invisibility,BM NS,;kal por ylem,Mark,BP BM MR,;"
               "vas des sanct,Mass Curse,GA MR NS SA,;in ex grav,Paralyze Field,BP GI SS,;wis quas,Reveal,BM SA,;"
               "vas ort grav,Chain Lightning,BP BM MR SA,;in sanct grav,Energy Field,BP MR SS SA,;"
               "kal vas flam,Flamestrike,SS SA,;vas rel por,Gate Travel,BP MR SA,;ort sanct,Mana Vampire,BP BM MR SS,;"
               "vas an ort,Mass Dispel,BP GA MR SA,;flam kal des ylem,Meteor Swarm,BM MR SS SA,;"
               "vas ylem rel,Polymorph,BM MR SS,;in vas por,Earthquake,BM GI MR SA,;"
               "vas corp por,Energy Vortex,BP BM MR NS,;an corp,Resurrection,BM GA GI,;"
               "kal vas xen hur,Air Elemental,BM MR SS,;kal vas xen corp,Summon Daemon,BM MR SS SA,;"
               "kal vas xen ylem,Earth Elemental,BM MR SS,;kal vas xen flam,Fire Elemental,BM MR SS SA,;"
               "kal vas xen an flam,Water Elemental,BM MR SS,;expor flamus,Cleanse by Fire,1.0,cure;"
               "obsu vulni,Close Wounds,1.5,heal;consecrus arma,Consecrate Weapon,0.5,;dispiro malas,Dispel Evil,0.25,;"
               "divinum furis,Divine Fury,1.0,;forul solum,Enemy of One,0.5,;augus luminos,Holy Light,1.75,;"
               "dium prostra,Noble Sacrifice,1.5,;extermo vomica,Remove Curse,1.5,;sanctum viatas,Sacred Journey,1.5,;"
               "uus corp,Animate Dead,1.75,;in jux mani xen,Blood Oath,1.5,;in agle corp ylem,Corpse Skin,1.5,;"
               "an sanct gra char,Curse Weapon,1.0,;pas tym an sanct,Evil Omen,1.0,;"
               "rel xen vas bal,Horrific Beast,2.0,;rel xen corp ort,Lich Form,2.0,;wis an ben,Mind Rot,1.5,;"
               "in sar,Pain Spike,1.25,;in vas nox,Poison Strike,2.0,;in bal nox,Strangle,2.0,;"
               "kal xen bal,Summon Familiar,2.0,;rel xen an sanct,Vampiric Embrace,2.0,;"
               "kal xen bal beh,Vengeful Spirit,2.0,;kal vas an flam,Wither,1.5,;rel xen um,Wraith Form,2.0,;"
               "ort corp grav,Exorcism,2.0,").split(";"):
        # words, name, reagents or cast seconds, kind.
        _w, _n, _x, _t = _r.split(",")
        SPELL_WORDS[_w] = (_n, _t or None)
        # A reagent list starts with a letter; a cast time with a digit.
        if _x[0] > "9":
            MAGERY.append((_n, _x))
        else:
            CAST_DELAY_OTHER[_n] = float(_x)
    MAGERY = tuple(MAGERY)
    # The loop's names are not kept on the class.
    del _r, _w, _n, _x, _t
    # Reagent abbreviation to (name, item graphic).
    REAGENTS = {"BP": ("Black Pearl", 0x0F7A), "BM": ("Blood Moss", 0x0F7B), "GA": ("Garlic", 0x0F84),
                "GI": ("Ginseng", 0x0F85), "MR": ("Mandrake Root", 0x0F86), "NS": ("Nightshade", 0x0F88),
                "SS": ("Spiders' Silk", 0x0F8D), "SA": ("Sulfurous Ash", 0x0F8C)}
    # Mana per circle, first to eighth. Classic (pre-AoS) values.
    SPELL_MANA = (4, 6, 9, 11, 14, 20, 40, 50)
    # Seconds of casting before the target cursor per circle: 0.5 plus 0.25 for each circle above the
    # first. Recall, Gate and the eighth-circle summons are slower still.
    CAST_DELAY = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25)
    # Seconds added to every Magery cast time on In Mani Ylem.
    CAST_EXTRA = 0.5
    # Spell name (lower case) to spell_info's answer, built on first use.
    _spells = {}

    @staticmethod
    def spell_info(name):
        """Information about a spell by name (any case). Returns (circle 1-8, reagent abbreviations, mana,
        cast seconds) for a Magery spell, (0, (), 0, seconds) for a known spell of another school, or
        None.
        """
        if not Kit._spells:
            for n, secs in Kit.CAST_DELAY_OTHER.items():
                Kit._spells[n.lower()] = (0, (), 0, secs)
            for i, (n, regs) in enumerate(Kit.MAGERY):
                c = i // 8 + 1
                Kit._spells[n.lower()] = (c, tuple(regs.split()), Kit.SPELL_MANA[c - 1],
                                          Kit.CAST_DELAY[c - 1] + Kit.CAST_EXTRA)
        return Kit._spells.get(str(name or "").strip().lower())

    # Eight points of the compass, starting east and going clockwise on screen.
    COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")
    # Facet numbers to names.
    FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")

    @staticmethod
    def compass(dx, dy, names=None):
        """The compass point of (dx, dy) in game tiles, an empty string when both are 0. names replaces the
        default points.
        """
        if not dx and not dy:
            return ""
        return (names or Kit.COMPASS)[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]

    @staticmethod
    def held_item():
        """The serial of the item on the cursor (0: none, or the client cannot say). Kept for the pass inside
        a client hop.
        """
        pid = HOST.pass_id if HOST.in_hop else None
        if pid is not None and Kit._held[0] == pid:
            return Kit._held[1]
        try:
            v = int(API.GetHeldItem() or 0)
        except Exception:
            v = 0
        if pid is not None:
            Kit._held[0], Kit._held[1] = pid, v
        return v

    # [pass id, serial] of the last read inside a hop.
    _held = [-1, 0]

    @staticmethod
    def find_item(serial):
        """API.FindItem(serial), or None (no serial, or the client cannot say)."""
        if not serial:
            return None
        try:
            return API.FindItem(serial)
        except Exception:
            return None

    @staticmethod
    def top_of(serial):
        """Follow an item up through its containers. Returns (serial of the outermost item, serial of the
        mobile that carries it or 0).

        At most ten containers are climbed. An item the client does not know comes back as itself with 0.
        """
        s = int(serial or 0)
        for _ in range(10):
            it = Kit.find_item(s)
            if it is None:
                return s, 0
            try:
                c = int(it.Container or 0)
            except Exception:
                c = 0
            if not c or c == 0xFFFFFFFF:
                return s, 0
            # A container serial below this is a mobile: the item is worn or held.
            if c < 0x40000000:
                return s, c
            s = c
        return s, 0

    @staticmethod
    def in_pack(serial):
        """True when the item is inside the player's backpack, at any depth."""
        pack = int(API.Backpack or 0)
        return bool(pack) and bool(serial) and Kit.top_of(serial)[0] == pack

    @staticmethod
    def where_text(dx, dy, here="under you", names=None):
        """Where (dx, dy) tiles away is: "312 tiles NE", "1 tile S", or here when it is under the player."""
        d = max(abs(int(dx)), abs(int(dy)))
        if d == 0:
            return here
        return "%s %s" % (Kit.count(d, "tile"), Kit.compass(dx, dy, names))

    @staticmethod
    def count(n, word, many=None):
        """n with its noun, "1 tile" or "2 tiles"; many gives an irregular plural."""
        return "%d %s" % (n, word if n == 1 else many or word + "s")

    @staticmethod
    def facet_name(m):
        """The name of a facet number, "?" when it is not a number, "facet n" when it is unknown."""
        try:
            m = int(m)
        except Exception:
            return "?"
        return Kit.FACETS[m] if 0 <= m < len(Kit.FACETS) else "facet %d" % m

    # Time units for ago: (limit in seconds, divisor, format). A limit of 0 is the last row. The short
    # form drops minutes under an hour, and the words form gives "just now" and "Nm ago".
    AGO = ((60, 1, "%ds"), (3600, 60, "%dm"), (0, 3600, "%dh %dm"))
    AGO_SHORT = ((60, 1, "%ds"), (3600, 60, "%dm"), (0, 3600, "%dh"))
    AGO_WORDS = ((60, 1, "just now"), (3600, 60, "%dm ago"), (86400, 3600, "%dh ago"), (0, 86400, "%dd ago"))

    @staticmethod
    def ago(secs, units=None):
        """A number of seconds as "45s", "6m" or "2h 14m" (never negative); units picks another table."""
        secs = max(0, int(secs))
        for limit, div, fmt in units or Kit.AGO:
            if not limit or secs < limit:
                break
        n = fmt.count("%")
        if n == 0:
            return fmt
        return fmt % (secs // div) if n == 1 else fmt % (secs // div, secs % div // 60)

    @staticmethod
    def read_int(ctrl, default, lo=None, hi=None):
        """The integer in a text box (its Text), clamped to [lo, hi]; default when it is empty or not a number."""
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
        """A "k=v;k2=v2" settings string as a dict (keys and values stripped)."""
        out = {}
        for part in str(text or "").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                out[k.strip()] = v.strip()
        return out

    B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    B64_REV = dict((ch, i) for i, ch in enumerate(B64))

    @staticmethod
    def b64(data):
        """Encode a list of byte values (a multiple of 3 long) as URL-safe base64 text without padding
        characters (alphabet Kit.B64). Used for the layout share code.
        """
        out = []
        B64 = Kit.B64
        for i in range(0, len(data), 3):
            n = (data[i] << 16) | (data[i + 1] << 8) | data[i + 2]
            out += [B64[(n >> 18) & 63], B64[(n >> 12) & 63], B64[(n >> 6) & 63], B64[n & 63]]
        return "".join(out)

    @staticmethod
    def unb64(s):
        """Decode Kit.b64 text (a multiple of 4 long) back to a list of byte values."""
        data = []
        B64_REV = Kit.B64_REV
        for i in range(0, len(s), 4):
            n = 0
            for ch in s[i:i + 4]:
                n = (n << 6) | B64_REV[ch]
            data += [(n >> 16) & 255, (n >> 8) & 255, n & 255]
        return data

    @staticmethod
    def checksum(data):
        """A 16-bit checksum of a list of byte values, used to catch a mistyped layout share code."""
        s = 7
        for i, b in enumerate(data):
            s = (s * 31 + b + i) & 0xFFFF
        return s

    @staticmethod
    def kv_load(key, sep, into, nums=None, strs=()):
        """Load a saved "k=v" list (parts split by sep, from the per-character value key) into the dict into.

        Keys in nums are whole numbers clamped to their (low, high); keys in strs are kept as text; any
        other key already in into is a flag stored as "1" or "0". Unknown keys are ignored.
        """
        nums = nums or {}
        for part in Kit.get_var(key).split(sep):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            k, v = k.strip(), v.strip()
            if k in nums:
                try:
                    into[k] = max(nums[k][0], min(nums[k][1], int(v)))
                except ValueError:
                    pass
            elif k in strs:
                into[k] = v
            elif k in into:
                into[k] = v == "1"

    @staticmethod
    def kv_save(key, sep, vals, order, nums=None, strs=()):
        """Save the values in order as a "k=v" list under the per-character value key (the inverse of
        kv_load): numbers and text as they are, flags as "1" or "0".
        """
        nums = nums or {}
        Kit.put_var(key, sep.join("%s=%s" % (k, vals[k] if k in nums or k in strs else ("1" if vals[k] else "0"))
                                  for k in order))

    @staticmethod
    def with_tip(ctrl, text):
        """Give a control a tooltip when there is text. Returns the control."""
        if text:
            try:
                ctrl.SetTooltip(text)
            except Exception:
                pass
        return ctrl

    @staticmethod
    def sayer(title, gate=None, key=None):
        """Make a say(text, hue) function that prints a journal line "title: text".

        When gate and key are given it says nothing while gate[key] is false (a module's own "talk" flag).
        """
        def say(text, hue=None):
            """Print one journal line prefixed with the module's title, if allowed."""
            if gate is None or gate[key]:
                API.SysMsg("%s: %s" % (title, text), Kit.HUE_INFO if hue is None else hue)

        return say

    @staticmethod
    def basics(st, title):
        """The three helpers most modules start with: (Cleanup, queue, say) for a window state and title."""
        return Kit.Cleanup(), Kit.queuer(st), Kit.sayer(title)

    @staticmethod
    def dd_index(dd, default):
        """The selected index of a dropdown, default when it cannot be read."""
        try:
            return int(dd.GetSelectedIndex())
        except Exception:
            return default

    @staticmethod
    def drop_arrow(st, arrow_id):
        """Remove the tracking arrow of a module (st["arrow"]) when it has one up."""
        if st["arrow"] is not None:
            st["arrow"] = None
            API.TrackingArrow(-1, -1, arrow_id)

    @staticmethod
    def say(text, hue=None):
        """Print one journal line prefixed with the app name, in the information hue unless given."""
        API.SysMsg(APP_NAME + ": " + str(text), Kit.HUE_INFO if hue is None else hue)

    @staticmethod
    def win_action(action, st, key, title, build, min_key=None):
        """Do the standard title-button actions a module's tick receives. Returns True when handled.

        Settings opens the module's settings page; toggle_min flips minimized (clears docked, forgets the
        tray entry, saves the choice under min_key) and rebuilds; to_bar folds the window into the Action
        Bar; redraw rebuilds.
        """
        if action == "settings":
            HOST.show_settings(key)
        elif action == "toggle_min":
            st["minimized"], st["docked"] = not st["minimized"], False
            HOST.dock_forget(key)
            if min_key:
                Kit.save_min(min_key, st["minimized"])
            build()
        elif action == "to_bar":
            HOST.dock_to_bar(key, title)
        elif action == "redraw":
            build()
        else:
            return False
        return True

    @staticmethod
    def show_window(g, x, y, w, h, lock_key, hidden, on_disposed, moved, into=None, parts=None, max_h=None, old=None):
        """Place and show a freshly built window and return the (x, y) it was placed at.

        The window is placed on screen (max_h is the zone slot's height), counted as built for the
        start-up settling when lock_key is given, made immovable when the layout locks it, its parts are
        merged into the module's window dict, an on_disposed handler and a moved handler are attached, and
        it is added in front through Kit.replace_gump (old is the window it replaces) and hidden when
        hidden is set (folded into the Action Bar).
        """
        xy = Kit.place(g, x, y, w, h, None, max_h)
        if lock_key is not None:
            HOST.built(lock_key)
        if lock_key is not None and HOST.layout_locked(lock_key):
            g.CanMove = False
        if into is not None:
            into.update(parts)
        if on_disposed is not None:
            G.AddControlOnDisposed(g, on_disposed)
        Kit.replace_gump(old, g, hidden)
        if moved is not None:
            Kit.on_moved(g, moved)
        return xy

    @staticmethod
    def row_set(row, val, now):
        """Keep a row's value with the one before it and when it changed.

        val is a tuple whose first item is what the row stands for (a serial); row_clicker uses the
        previous value for a moment after a change.
        """
        cur = row.get("val")
        if (cur[0] if cur else None) != (val[0] if val else None):
            row["prev"], row["val"], row["changed"] = cur or None, val, now

    @staticmethod
    def row_clicker(row, queue, kind, grace=0.15, follow=True):
        """Make the click handler of a list row that acts on what the row shows.

        A row's content can change between the player's look and the click, so for grace seconds after a
        change the click acts on the previous value. Alt+click follows the mobile (when follow is set);
        any other click queues (kind, ...value).
        """
        def handler(*args):
            """Act on the row's value as the player saw it."""
            v = row.get("prev")
            if not (v and time.time() - row.get("changed", 0.0) < grace):
                v = row.get("val")
            if not v or not v[0]:
                return
            if follow and Follow.alt_held():
                queue(("follow", v[0]))()
            else:
                queue((kind,) + tuple(v))()

        return handler

    @staticmethod
    def buttons(g, store, x, y, rows, gap=20):
        """Lay out a row of art buttons left to right. rows are (key, art, caption, tooltip, on_click, hue)
        with the last two optional. Returns the x after the last button.
        """
        for b in rows:
            Kit.art_button(g, store, b[0], b[1], x, y, b[2], b[3], b[5] if len(b) > 5 else None,
                           b[4] if len(b) > 4 else None)
            x += 35 + Kit.text_w(b[2]) + gap
        return x

    class Form(object):
        """A declarative form for a settings page.

        A page is a list of sections (title, rows, options); the rows are check boxes, number fields, text
        fields, sliders, notes, button rows and custom rows, drawn in order with the standard spacing.
        Row forms: ("check", key, caption, tip), ("num", key, label, tip, unit, low, high), ("text", key,
        label, tip), ("slider", key, label, tip, low, high), ("note", text), ("buttons", [buttons]),
        ("custom", height, fn(form, x, y)) and ("gap", height); a dict as a row's last item overrides the
        options for that row. Created without a gump (g None) it only measures its height. read() takes the
        values back from the controls. A row whose setting is new in this release, or the one the settings
        search found, gets a small tag drawn after it (Form._tag).
        """
        # Default spacing and sizes: title row, bottom padding, row heights for check, field, note and
        # buttons, left inset, label offset, label-to-field gap, field-to-unit gap, number field width,
        # slider width, slider and note and button offsets, button gap, number format.
        OPTS = {"top": 30, "pad": 10, "ch": 26, "fh": 28, "nh": 20, "bh": 28, "dx": 12, "ldy": 3, "lgap": 10,
                "ugap": 8, "fw": 50, "sw": 140, "sdy": 2, "ndy": 0, "bdy": -2, "bgap": 20, "fmt": "%d"}
        # Which option holds the row height of each row kind.
        STEP = {"check": "ch", "note": "nh", "buttons": "bh", "num": "fh", "text": "fh", "slider": "fh"}
        COMPACT = {"ch": 22, "fh": 24, "bh": 26, "top": 28, "pad": 6}
        # Row kinds that have a label and a field.
        FIELDS = ("num", "text", "slider")
        sink = mark = fresh = page = None
        BOX_W = 20
        FOUND = "<- found"
        NEW = "new"

        def __init__(self, g, x, y, w, vals, page=(), store=None, **opts):
            """Lay out the page's sections at (x, y) width w, starting from the saved values vals."""
            self.g, self.x, self.y, self.w, self.vals, self.opts = g, x, y, w, vals, opts
            self.top, self.c, self.store, self.specs = y, {}, store or ({}, {}), []
            for sec in page:
                self.section(*sec)

        @property
        def h(self):
            """The height of what was drawn so far, without the last gap."""
            return max(0, self.y - self.top - Kit.GAP)

        @staticmethod
        def height(page, w=0, **opts):
            """The height a page would have at width w, without drawing it."""
            return Kit.Form(None, 0, 0, w, {}, page, **opts).h

        def _o(self, sec, r=None):
            """The options for a section or one of its rows: the defaults, the compact set when compact rows are
            on, then the form's, then the section's, then the row's own dict.
            """
            o = dict(Kit.Form.OPTS)
            if Kit.compact:
                o.update(Kit.Form.COMPACT)
            o.update(self.opts)
            o.update(sec)
            if r and type(r[-1]) is dict:
                o.update(r[-1])
            return o

        @staticmethod
        def _step(r, o):
            """The vertical room a row takes; a row marked stay takes none."""
            if o.get("stay"):
                return 0
            if r[0] in ("gap", "custom"):
                return r[1]
            return o["h"] if "h" in o else o[Kit.Form.STEP[r[0]]]

        def section(self, title, rows, sec=None):
            """Draw one section (a black block with its title) and its rows, and move y below it.

            A fixed section height can be given as sh; otherwise it is the title row, the rows and the padding.
            Field labels line up on the widest label when the section asks for align. When the settings
            search is collecting rows (Form.sink), the section is also recorded with the part that draws it.
            """
            if Kit.Form.sink is not None:
                Kit.Form.sink.append((HOST.cur_part, title, rows))
            sec = sec or {}
            so, opts = self._o(sec), [self._o(sec, r) for r in rows]
            sh = sec.get("sh") or so["top"] + sum(Kit.Form._step(r, o) for r, o in zip(rows, opts)) + so["pad"]
            x, ry, g = self.x, self.y + so["top"], self.g
            if g is not None:
                Kit.add_section(g, x, self.y, self.w, sh, title)
            self.y += sh + Kit.GAP
            if g is None:
                return
            lw = max([Kit.text_w(r[2]) for r in rows if r[0] in Kit.Form.FIELDS] or [0])
            for r, o in zip(rows, opts):
                self._row(g, r, o, x, ry, o.get("lw", lw if o.get("align") else None))
                ry += Kit.Form._step(r, o)

        @staticmethod
        def _tag(r):
            """The small tag for a row: "<- found" for the row the settings search jumped to, "new" for a
            setting added in this release that the player has not looked at yet, else None.

            Gaps and custom rows never carry a tag; notes can only be marked as found. r is the row tuple.
            """
            F = Kit.Form
            if F.page is None or r[0] in ("gap", "custom"):
                return None
            pk = HOST.cur_part
            keys = [b[0] for b in r[1]] if r[0] == "buttons" else [r[1]]
            if F.mark is not None and F.mark[0] == pk and F.mark[1] in keys:
                return F.FOUND
            pre = F.page + "." + (pk + "." if pk else "")
            if r[0] != "note" and F.fresh and any(pre + str(k) in F.fresh for k in keys):
                return F.NEW
            return None

        def _row(self, g, r, o, sx, y, lw):
            """Draw one row of a section, and the row's tag (Form._tag) after its last control when it has one."""
            kind, c, x = r[0], self.c, sx + o["dx"]
            k = r[1] if kind in Kit.Form.FIELDS or kind == "check" else None
            tag = Kit.Form._tag(r)
            end = None
            if kind == "check":
                c[k] = Kit.add_check(g, r[2], x, y, self.vals[k], r[3])
                self.specs.append((r, o))
                end = x + Kit.Form.BOX_W + (Kit.text_w(r[2]) if tag else 0)
            elif kind == "note":
                lbl = Kit.add_label(g, r[1], x, y + o["ndy"], o.get("hue", Kit.HUE_INFO))
                if o.get("key"):
                    c[o["key"]] = lbl
                end = x + (Kit.text_w(r[1]) if tag else 0)
            elif kind == "buttons":
                end = Kit.buttons(g, self.store, x, y + o["bdy"], [b[:5] for b in r[1]], o["bgap"]) - o["bgap"]
            elif kind == "custom":
                r[2](self, sx, y)
            elif kind in Kit.Form.FIELDS:
                lbl = Kit.add_label(g, r[2], x, y + o["ldy"])
                fx = x + (Kit.text_w(r[2]) if lw is None else lw) + o["lgap"]
                tip = r[3]
                if kind == "num":
                    if tip and not tip.endswith(")"):
                        tip += " (%d-%d)" % (r[5], r[6])
                    c[k] = Kit.add_textbox(g, o["fmt"] % self.vals[k], fx, y, o["fw"])
                    end = fx + o["fw"]
                    if r[4]:
                        Kit.add_label(g, r[4], fx + o["fw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                        end += o["ugap"] + (Kit.text_w(r[4]) if tag else 0)
                elif kind == "text":
                    tw = (o.get("tw") or self.w - (fx - sx) - 16) - (Kit.text_w(tag) + 6 if tag else 0)
                    c[k] = Kit.add_textbox(g, self.vals[k], fx, y, tw, numbers=False)
                    end = fx + tw
                else:
                    c[k] = Kit.add_slider(g, fx, y + o["sdy"], o["sw"], r[4], r[5], self.vals[k])
                    end = fx + o["sw"]
                    if o.get("vfmt") or o.get("unit"):
                        lt = o["vfmt"] % self.vals[k] if o.get("vfmt") else o["unit"]
                        c[k + "_lbl"] = Kit.add_label(g, lt, fx + o["sw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                        end += o["ugap"] + (Kit.text_w(lt) if tag else 0)
                Kit.with_tip(c[k], tip)
                if o.get("ltip"):
                    Kit.with_tip(lbl, tip)
                self.specs.append((r, o))
            if tag and end is not None:
                dy = {"check": 2, "note": o["ndy"], "buttons": o["bdy"] + 3}.get(kind, o["ldy"])
                Kit.add_label(g, tag, min(end + 6, sx + self.w - 4 - Kit.text_w(tag)), y + dy, Kit.HUE_TITLE)

        def read(self, strict=False, empty=None):
            """Read the controls back into a copy of the values.

            Checks are True or False, numbers are read and clamped to their range (a value out of range falls
            back to the old one), text is stripped (empty falls back to empty[key] or an empty string) and a
            slider is clamped. A control that cannot be read keeps its old value, or raises when strict. A
            slider's value label is updated.
            """
            out = dict(self.vals)
            for r, o in self.specs:
                kind, k = r[0], r[1]
                try:
                    ctrl = self.c[k]
                    if kind == "check":
                        v = bool(ctrl.IsChecked)
                    elif kind == "num":
                        v = Kit.read_int(ctrl, out[k], *((r[5], r[6]) if o.get("clamp", True) else ()))
                        v = o.get("cast", int)(v if r[5] <= v <= r[6] else out[k])
                    elif kind == "text":
                        v = str(ctrl.Text or "").strip() or (empty or {}).get(k, "")
                    else:
                        v = max(r[4], min(r[5], int(ctrl.Value)))
                except Exception:
                    if strict:
                        raise
                    continue
                out[k] = v
                if kind == "slider" and o.get("vfmt"):
                    Kit.set_text(self.c[k + "_lbl"], o["vfmt"] % v)
            return out

    class Page(object):
        """A settings page bound to the values it edits: a form, its saving and its reaction to a change.

        table is the rows (or a function of the width); save() runs when a value changed and on_change(old,
        new) after it; clicks(form) is polled for button rows; adjust(form, new) may alter the read values
        before they are compared; every limits how often fields are read (seconds) and final reads them
        once more when the page closes.
        """
        def __init__(self, vals, table, save=None, on_change=None, opts=None, strict=False, empty=None, adjust=None,
                     clicks=None, every=0.0, final=False):
            """Remember the page's values, rows and callbacks; nothing is drawn yet."""
            self.vals, self.table, self.save, self.on_change, self.opts = vals, table, save, on_change, opts or {}
            self.strict, self.empty, self.adjust, self.clicks, self.every = strict, empty, adjust, clicks, every
            self.f, self.unread, self.at, self.final, self.force = None, False, 0.0, final, False

        def rows(self, w):
            """The rows at width w."""
            return self.table(w) if callable(self.table) else self.table

        def height(self, w):
            """The height the page takes at width w."""
            return Kit.Form.height(self.rows(w), w, **self.opts)

        def build(self, g, x, y, w):
            """Draw the page into g at (x, y) with width w and return the form."""
            self.unread, self.at = False, 0.0
            self.f = Kit.Form(g, x, y, w, self.vals, self.rows(w), **self.opts)
            return self.f

        def poll(self, force=False):
            """Read the fields and react to a change: update the values, save and call on_change.

            Skipped (and marked unread) when called again before every seconds passed, unless forced. A form
            that cannot be read is dropped.
            """
            f = self.f
            if f is None:
                return
            if self.clicks is not None:
                self.clicks(f)
                if self.f is not f:
                    return
            if self.every:
                now = time.time()
                if not force and now < self.at:
                    self.unread = True
                    return
                self.at, self.unread = now + self.every, False
            try:
                new = f.read(self.strict, self.empty)
            except Exception:
                self.f = None
                return
            self.force = force
            if self.adjust is not None:
                self.adjust(f, new)
            if new == self.vals:
                return
            old = dict(self.vals)
            self.vals.update(new)
            if self.save is not None:
                self.save()
            if self.on_change is not None:
                self.on_change(old, self.vals)

        def closed(self):
            """The page was closed: read the fields once more if they have changed since the last poll, then let
            go of the form.
            """
            if (self.unread or self.final) and self.f is not None:
                self.poll(True)
            self.f, self.unread = None, False

    class Cleanup(object):
        """The jobs a module undoes when it stops, run last-in first-out."""
        def __init__(self):
            """Start with no jobs."""
            self.jobs = []

        def add(self, fn, *args):
            """Add a job: fn(*args) is called at close. Returns fn."""
            self.jobs.append((fn, args))
            return fn

        def service(self, name, fn):
            """Register a named host service and remove it again at close. Returns fn."""
            HOST.services[name] = fn
            self.jobs.append((Kit.Cleanup.drop, (name, fn)))
            return fn

        @staticmethod
        def drop(name, fn):
            """Remove a registered service, only when it is still this function."""
            if HOST.services.get(name) is fn:
                HOST.services.pop(name, None)

        def close(self):
            """Run every job, last added first, ignoring failures."""
            jobs = self.jobs
            while jobs:
                fn, args = jobs.pop()
                with Kit.quiet:
                    fn(*args)

    class Window(object):
        """The standard window of a module: one window drawn by build(), with its place and minimized state
        remembered, its title bar, frame and dock entry.

        key is the module's key; st is its state dict (queue, minimized, docked, shutting) and win the dict
        that holds the window (under gkey); pos_key and min_key are the saved-value keys of its place and
        minimized state; mini is the (w, h) of the minimized form; cleanup is the module's Kit.Cleanup (the
        window closes with it); owner makes closing the window turn the module off. The module calls
        begin(), draws, then end().
        """
        def __init__(self, key, title, st, win, build, pos_key, min_key=None, default=(200, 200), mini=None,
                     icon=None, cleanup=None, gkey="g", names=("c", "store"), lock=True, owner=True, close_tip=None,
                     clear=None, docked_min=False):
            """Remember the settings and make the module's click queue."""
            self.key, self.title, self.st, self.win, self.build, self.pos_key = key, title, st, win, build, pos_key
            self.min_key, self.default, self.mini, self.icon, self.cleanup = min_key, default, mini, icon, cleanup
            self.gkey, self.names, self.lock, self.owner, self.close_tip = gkey, names, lock, owner, close_tip
            self.clear, self.docked_min, self.slot, self.held, self.old = clear or {}, docked_min, None, False, None
            self.queue = Kit.queuer(st) if st is not None else None
            self.x = self.y = self.w = self.h = 0
            self.c, self.store, self.fade = {}, ({}, {}), True

        def minimized(self):
            """True when the module's state says the window is minimized."""
            return self.st is not None and bool(self.st["minimized"])

        def start_min(self):
            """True when the window should start minimized: the dock wanted it, or its saved minimized flag."""
            return bool(HOST.dock_wanted(self.key) or (self.min_key and Kit.load_min(self.min_key)))

        def begin(self, w, h, default=None, resize=None):
            """Start a rebuild: open a fresh gump, remembering the old window to drop once the new one is up.

            The size is the minimized form's when minimized. The place is the old window's, else the layout's
            planned slot, else the saved one (adapted to the screen). Returns (gump, store, controls); a
            minimized window already has its bar.
            """
            if self.queue is not None:
                Kit._wins[self.key] = self
            if Kit.is_open(self.old) and self.old is not self.win.get(self.gkey):
                Kit.dispose(self.old)
            old = self.win.get(self.gkey)
            mini = self.minimized()
            if mini and self.mini:
                w, h = self.mini
            self.w, self.h = w, h
            p = None if Kit.is_open(old) or mini or not LAYOUT.planned else LAYOUT.plan_at(self.key)
            if Kit.is_open(old):
                self.x, self.y = old.GetX(), old.GetY()
            elif p is not None:
                self.x, self.y = int(p[0]), int(p[1])
            else:
                self.x, self.y = Kit.load_pos(self.pos_key, default or self.default, (w, h))
            self.old, self.win[self.gkey] = old, None
            if self.cleanup is not None and not self.held:
                self.held = True
                self.cleanup.add(self.release)
            if resize is not None and not mini:
                self.x, self.y = Kit.clamp(self.x, self.y, w, h)
                g = G.CreateModernGump(self.x, self.y, w, h, True, resize[0], resize[1], resize[2])
                g.SetAlpha(0)
            else:
                g = G.CreateGump(True, True)
            self.c, self.store = {}, ({}, {})
            if mini:
                self.c["status"] = Kit.mini_bar(g, self.store, w, h, self.title, self.key, self.queue("toggle_min"),
                                                close_tip=self.close_tip)
            return g, self.store, self.c

        def frame(self, g, w=None, h=None, extra=None, after=None, settings=True, mouse=True, corners=True):
            """Draw the standard frame and title bar and return the x where the title buttons start."""
            w = self.w if w is None else w
            q = self.queue
            Kit.add_window_frame(g, w, self.h if h is None else h, corners, mouse)
            return Kit.title_bar(g, self.store, w, self.title, self.key, q("toggle_min"), q("to_bar"),
                                 q("settings") if settings else None, self.close_tip, extra, after)

        def end(self, g, parts=None, w=None, h=None, max_h=None):
            """Show the new window and drop the old one. Returns the (x, y) it was placed at.

            The window is placed and registered through Kit.show_window; a window the layout holds in a zone
            is moved to its slot and fitted at once. A minimized window that the Action Bar will fold into its
            tray is marked docked from the start. parts are added to the window dict with the controls and the
            button store under the names given. The fade service is woken so a faded window comes back when it
            is rebuilt.
            """
            st, parts = self.st, dict(parts or {})
            parts[self.gkey] = g
            if not self.lock:
                HOST.built(self.key)
            if st is not None and st.get("minimized") and st.get("docked") is False and HOST.dock_soon(self.key):
                st["docked"] = True
            for name, v in zip(self.names or (), (self.c, self.store)):
                parts[name] = v
            xy = Kit.show_window(g, self.x, self.y, self.w if w is None else w, self.h if h is None else h,
                                 self.key if self.lock else None, st is not None and st["minimized"] and st["docked"],
                                 self.disposed(g), self.save_pos, self.win, parts, max_h, self.old)
            slot = LAYOUT.spot(self.key) if LAYOUT.seamless and LAYOUT.holds(self.key) else None
            if slot is not None and xy is not None and (xy[0], xy[1]) != (slot[0], slot[1]):
                g.SetPos(int(slot[0]), int(slot[1]))
                Kit.note_rect(g, slot[0], slot[1])
                Kit.moved_by_code(g)
                xy = (slot[0], slot[1])
            if slot is not None and xy is not None:
                LAYOUT._hold(g, self.key)
                LAYOUT.fit_now(self.key, g)
            if FADE.on:
                FADE.wake(self.key)
            old, self.old = self.old, None
            Kit.dispose(old)
            return xy

        def disposed(self, g):
            """Make the handler for window g being disposed from outside: clear the window and, for an owner,
            turn the module off, unless the window was replaced or the module is shutting down.
            """
            def handler(*args):
                """Clear the window entries and turn the module off when this window went away by itself."""
                win = self.win
                if win.get(self.gkey) is not g or (self.owner and self.st["shutting"]):
                    return
                win[self.gkey] = None
                win.update(self.clear)
                if self.owner:
                    HOST.disable(self.key)

            return handler

        def save_pos(self):
            """Save the window's place."""
            Kit.save_pos(self.pos_key, self.win.get(self.gkey))

        def close(self):
            """Close the window for good: drop any older one, save its place and minimized flag, and dispose it."""
            if Kit.is_open(self.old) and self.old is not self.win.get(self.gkey):
                Kit.dispose(self.old)
            st = self.st
            self.save_pos()
            if self.min_key and st is not None:
                Kit.save_min(self.min_key, st["minimized"] and not (self.docked_min and st["docked"]))
            g, self.win[self.gkey] = self.win.get(self.gkey), None
            self.win.update(self.clear)
            Kit.dispose(g)

        def release(self):
            """Cleanup job: release the hold and close the window."""
            self.held = False
            self.close()

        def action(self, action):
            """Do a standard title-button action (see Kit.win_action). Returns True when handled."""
            return Kit.win_action(action, self.st, self.key, self.title, self.build, self.min_key)

        def fit(self, w, h, mode):
            """The layout's fit hook: record the slot size (None when freed) and redraw when it changed, or when
            the mode is again.
            """
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != self._slot or (mode == "again" and new is not None):
                self.slot = new
                self.queue("redraw")()

        @property
        def slot(self):
            """The (width, height) of the zone slot this window was given, or None.

            When no fit has told the window yet and the layout has a plan, the planned slot is taken (once), so
            the first draw already has the size.
            """
            s = self._slot
            if s is None and LAYOUT.planned and not self.told and self.st is not None and not self.st["minimized"]:
                p = LAYOUT.plan_at(self.key)
                if p is not None:
                    s = self._slot = (int(p[2]), int(p[3]))
                    self.told = True
            return s

        @slot.setter
        def slot(self, v):
            """Set the zone slot size; a value that is not None also marks the window as told, so the layout's
            plan is not asked again.
            """
            self._slot = v
            self.told = v is not None or self.__dict__.get("told", False)

        def zone_slot(self, mw, mh):
            """The zone slot (width, height) this window should fill, or None to keep its own size.

            None when its zone is not up, the window is minimised, or the slot is narrower than mw or shorter
            than mh (a slot too small for the window is ignored). Client thread, while building the window.
            """
            z = self.slot if Kit.zone_up(self.key) and not self.st["minimized"] else None
            return z if z is not None and z[0] >= mw and z[1] >= mh else None

        def rows(self, row_h, fixed_h, own_n, min_n=1):
            """How many rows of row_h pixels fit the window's zone slot under fixed_h pixels of other content,
            at least min_n; own_n when it is not in a zone.
            """
            if self.slot is None or not HOST.layout_holds(self.key):
                return own_n
            return max(min_n, int(self.slot[1] - fixed_h) // max(1, int(row_h)))

        def dock(self, fit=False, **extra):
            """Register the window with the host's dock registry through Kit.dock_hooks (fit is True to use
            this window's fit hook, or a function) and add the removal to the cleanup. Returns the hooks.
            """
            hooks = Kit.dock_hooks(self.title, self.icon, self.st, self.win, self.queue("redraw"),
                                   self.fit if fit is True else (fit or None))
            hooks.update(extra)
            HOST.dock_add(self.key, hooks)
            if self.cleanup is not None:
                self.cleanup.add(HOST.dock_remove, self.key)
            return hooks

    class _Quiet(object):
        """Context manager that swallows any Exception raised inside its with block."""
        def __enter__(self):
            """Enter the block; nothing to set up."""
            return self

        def __exit__(self, kind, value, tb):
            """Leave the block: return True (suppress) when an Exception subclass was raised, else False."""
            return kind is not None and issubclass(kind, Exception)

    quiet = _Quiet()
    _notos = {}
    NOTO_ORDER = ("unknown", "innocent", "ally", "gray", "criminal", "enemy", "murderer", "invulnerable")
    CB_RGB = {"innocent": (0, 114, 178), "ally": (86, 180, 233), "gray": (153, 153, 153), "criminal": (153, 153, 153),
              "enemy": (230, 159, 0), "murderer": (213, 94, 0), "invulnerable": (240, 228, 66)}
    CB_HUE = {"innocent": 1266, "ally": 1060, "gray": 2958, "criminal": 2958, "enemy": 1174, "murderer": 1100,
              "invulnerable": 1568}
    NOTO_MARKS = {"murderer": "R", "criminal": "C", "gray": "C", "enemy": "O", "ally": "A", "invulnerable": "I"}
    VEILS = {"me": "You", "guild": "(hidden)", "xy": "(hidden)", "place": "(hidden)"}
    B36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @staticmethod
    def noto_name(mob):
        """Return the lower-case notoriety name of a mobile, or unknown when it cannot be read."""
        try:
            v = mob.Notoriety
        except Exception:
            return "unknown"
        return Kit.noto_of(v)

    @staticmethod
    def noto_of(v):
        """Turn a notoriety value into its lower-case name, cached per value so the hot path does no string
        work.
        """
        try:
            return Kit._notos[v]
        except KeyError:
            pass
        except Exception:
            # A value that cannot be hashed is converted without caching.
            return str(v).split(".")[-1].lower()
        n = Kit._notos[v] = str(v).split(".")[-1].lower()
        return n

    @staticmethod
    def _noto_key(noto):
        """Turn a notoriety (a client number, a key string or a client enum value) into one of the keys of
        Kit.NOTO_ORDER; "unknown" for a number out of range.
        """
        if type(noto) is int:
            return Kit.NOTO_ORDER[noto] if 0 <= noto < len(Kit.NOTO_ORDER) else "unknown"
        return noto if isinstance(noto, str) else Kit.noto_of(noto)

    @staticmethod
    def cb_rgb(noto, default=None):
        """The colour-blind safe (r, g, b) of a notoriety, or default when colour-blind marks are off or the
        notoriety has none.
        """
        return Kit.CB_RGB.get(Kit._noto_key(noto), default) if Kit.cblind else default

    @staticmethod
    def cb_hex(noto, default=None):
        """Kit.cb_rgb as a "#RRGGBB" string, or default when there is no colour-blind colour."""
        c = Kit.cb_rgb(noto)
        return default if c is None else "#%02X%02X%02X" % c

    @staticmethod
    def cb_hue(noto, default=0):
        """The colour-blind safe client hue for a notoriety, or default when the marks are off."""
        return Kit.CB_HUE.get(Kit._noto_key(noto), default) if Kit.cblind else default

    @staticmethod
    def noto_mark(noto):
        """The one-letter mark for a notoriety (shown beside a name so colour is not the only cue), or an
        empty string when colour-blind marks are off or the notoriety has none.
        """
        return Kit.NOTO_MARKS.get(Kit._noto_key(noto), "") if Kit.cblind else ""

    @staticmethod
    def hp_mark(poisoned=False, paralysed=False, mortal=False):
        """Letters for a health bar's state when colour-blind marks are on: P poisoned, Z paralysed, M mortal.
        Empty text when the marks are off.
        """
        if not Kit.cblind:
            return ""
        return ("P" if poisoned else "") + ("Z" if paralysed else "") + ("M" if mortal else "")

    @staticmethod
    def veil(kind, text, serial=0):
        """Hide private text while streamer mode is on, and give it back unchanged otherwise.

        kind says what the text is: "name" becomes "Player" and three base 36 digits of the serial, so
        the same person keeps the same stand-in; any other kind becomes its fixed word from Kit.VEILS, or
        "(hidden)". Never raises.
        """
        if not Kit.streamer:
            return text
        if kind != "name":
            return Kit.VEILS.get(kind, "(hidden)")
        try:
            s = int(serial or 0)
        except (TypeError, ValueError):
            s = 0
        if s <= 0:
            return "Player"
        d = ""
        for _ in range(3):
            d = Kit.B36[s % 36] + d
            s //= 36
            if not s:
                break
        return "Player " + d

    @staticmethod
    def set(obj, attr, value):
        """Set an attribute on a client object and ignore any failure (a disposed or read-only control)."""
        try:
            setattr(obj, attr, value)
        except Exception:
            pass


class Fill(object):
    """Fits an open gump into a slot of a different size (the layout and dock zones).

    It records every child control of the gump with its natural rectangle, then stretches background
    pieces and slides the other controls so the content fills the slot. When the slot is smaller than
    the
    gump the content is scaled down (and a scroll band is used if it still does not fit). All of it
    runs on the client tick through the client's own API control wrappers.
    """
    ROW_H = 72
    MIN_EDGE = 20
    MIN_BG = 40
    FILL_MIN_K = 0.6
    FIELD_T = "TTFTextInputField"
    recs = {}
    by_raw = {}
    w2r = {}
    _api_t = [None]
    broken = False

    @staticmethod
    def _axis(n, N, M, ivals, mode):
        """Build the piecewise-linear map for one axis, from natural size n to slot size N.

        ivals are the background spans that may stretch. Spans are merged, the extra length N - n is
        shared
        between them in proportion to their length, and the result is a list of (natural, new) points.
        Returns None when the slot is no larger than the gump. In grid mode the whole inner area
        stretches.
        """
        n, N = float(max(1, n)), float(max(1, N))
        E = N - n
        if E < 0.5:
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
        """Evaluate an axis map m at the natural coordinate v by linear interpolation (identity past the
        ends).
        """
        if m is None or v <= m[0][0]:
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
        """Work out the new rectangle (x, y, w, h) of one recorded control for the record's slot and scale.

        Entry layout: kind (s stretch, p place), x, y, w, h, anchor background, last rectangle, frame
        flag,
        role (field or back), partner control, slack. Stretch pieces follow both axis maps; placed pieces
        keep their size and move with the map point of their centre (or of their background edge in anchor
        mode). The result is clamped inside the slot.
        """
        kind, x, y, w, h, bg = e[:6]
        role = e[8] if len(e) > 8 else None
        # A back piece is the box drawn behind a text field: it follows its field so the two stay glued.
        if role == "back":
            pe = rec["ent"].get(e[9])
            if pe is not None:
                fr = Fill._xform(rec, pe)
                return fr[0] - 2, fr[1] - 1, fr[2] + 4, fr[3] + (h - pe[4])
        k = rec.get("k", 1.0)
        h0 = h
        if k != 1.0:
            # When the gump is scaled down, positions and widths scale; a text field keeps as much height as the
            # space around it allows, so typing stays readable.
            x, y, w = x * k, y * k, w * k
            if role == "field":
                slack = e[10] if len(e) > 10 else None
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
            x0, x1 = ev(fx, x), ev(fx, x + w)
            # Tall backgrounds stretch on both axes; short ones (rows, title strip) only keep their centre.
            if h0 >= Fill.MIN_EDGE and (h0 > Fill.ROW_H or rec["rows"]) and not Fill.title_strip(e[2], e[4]):
                y0, y1 = ev(fy, y), ev(fy, y + h)
            else:
                c = ev(fy, y + h / 2.0)
                y0, y1 = c - h / 2.0, c + h / 2.0
            x0 = max(0, min(N - 1, int(round(x0))))
            y0 = max(0, min(Hn - 1, int(round(y0))))
            x1, y1 = min(N, int(round(x1))), min(Hn, int(round(y1)))
            return x0, y0, max(1, x1 - x0), max(1, y1 - y0)
        mode = rec["mode"]
        if bg is not None:
            bx, by, bw, bh = bg
            if mode == "frame":
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
        # A control with no background in frame mode is simply centred in the slot.
        elif mode == "frame" and not e[7]:
            nx = x + (N - rec["nat"][0] * k) / 2.0
            ny = y + (Hn - rec["nat"][1] * k) / 2.0
        else:
            nx = ev(fx, x + w / 2.0) - w / 2.0
            ny = ev(fy, y + h / 2.0) - h / 2.0
        nx = max(0, min(int(round(nx)), N - w)) if w < N else 0
        ny = max(0, min(int(round(ny)), Hn - h)) if h < Hn else 0
        return nx, ny, w, h

    @staticmethod
    def raw_of(c):
        """Return the client-side raw control behind a Legion control wrapper, cached; None if unavailable.

        The cache is dropped when it grows past 4000 entries.
        """
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
        """Move or resize a raw client control through the API control type (SetPos or SetRect).

        pos_only moves without resizing. Returns True on success; on any failure marks Fill as broken, so
        the fitter switches itself off instead of failing every tick.
        """
        t = Fill._api_t[0]
        if t is None:
            return False
        try:
            wraps = Fill._wraps
            # Wrappers are cached per raw control; the caches are cleared when they grow too large.
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
            Fill.broken = True
            return False

    _wraps = {}
    _mk = None

    @staticmethod
    def _find_api_type(g):
        """Find the client's ApiUiBaseControl type from a gump wrapper's class chain and remember it.

        Returns True once the type is known.
        """
        if Fill._api_t[0] is not None:
            return True
        with Kit.quiet:
            import clr
            t = clr.GetClrType(type(g))
            while t is not None:
                if str(t.Name) == "ApiUiBaseControl":
                    Fill._api_t[0] = t
                    return True
                t = t.BaseType
        return False

    @staticmethod
    def _scan(rec, kids, skip, k_now=1.0):
        """Record the controls of kids that are not yet known (skipping those in skip and the catchers).

        Each new control becomes an entry in rec["ent"] and in Fill.by_raw, classed as a stretching piece
        (backgrounds, tiles, scroll areas, red, blue and poison lines) or a placed piece. Returns the list
        of
        (control, entry) added. k_now is the scale to apply to them straight away.
        """
        ents = rec["ent"]
        same = Kit._same()
        new = []
        for c in kids:
            try:
                if c.IsDisposed or c in ents or c in Seam.catchers:
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
            # The coloured line pictures are drawn as stretching rules.
            if tn == "GumpPic":
                with Kit.quiet:
                    if int(c.Graphic) in (Kit.LINE_RED, Kit.LINE_BLUE, Kit.LINE_POISON):
                        kind = "s"
            # A near-transparent narrow blend control is a spacer, not a background.
            if kind == "s" and tn == "AlphaBlendControl" and r[2] < Fill.MIN_BG:
                with Kit.quiet:
                    if float(c.Alpha) < 0.05:
                        kind = "p"
            e = [kind, r[0], r[1], r[2], r[3], None, tuple(r), c in rec["frame"],
                 "field" if tn == Fill.FIELD_T else None, None, None]
            ents[c] = e
            Fill.by_raw[c] = (rec, e)
            new.append((c, e))
            if tn == "ScrollArea":
                rec["nested"] = True
            if k_now != 1.0:
                Fill._scale_one(rec, c, k_now)
        if new:
            Fill._pair_fields(rec)
        return new

    @staticmethod
    def _pair_fields(rec):
        """Pair each text field with the box drawn behind it and measure the free space around the field.

        The back piece follows its field; slack is the smallest vertical gap to a neighbouring control,
        and
        tells the transform how much a field may grow when the gump is scaled.
        """
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
                    continue
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
        """Return every descendant control of c (walk with an explicit stack, no recursion)."""
        out = []
        try:
            stack = list(Kit._children(c))
        except Exception:
            return out
        while stack:
            d = stack.pop()
            out.append(d)
            with Kit.quiet:
                stack.extend(Kit._children(d))
        return out

    @staticmethod
    def _scale_one(rec, c, k):
        """Apply the internal scale k to a control and to all of its descendants, resizing the descendants.

        Their own natural rectangles are remembered in rec["desc"] so unfit can put them back.
        """
        try:
            if abs(k - 1.0) > 0.001 and str(c.GetType().Name) == "GumpPicTiled":
                c.ScaleTiledTexture = True
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

    STRETCH = ("GumpPicTiled", "AlphaBlendControl", "ScrollArea", "ResizePic", "SimpleProgressBar")

    @staticmethod
    def _bgs(rec):
        """List the rectangles of the stretching background pieces that are neither the frame nor a back
        piece.

        Pieces that are too small, that cover the whole gump, or that touch the top or bottom edge are
        left out.
        """
        nw, nh = rec["nat"]
        out = []
        frame = rec["frame"]
        for c, e in rec["ent"].items():
            if e[0] != "s" or c in frame or e[8] == "back":
                continue
            x, y, w, h = e[1], e[2], e[3], e[4]
            if w < Fill.MIN_BG or h < Fill.MIN_EDGE:
                continue
            if w >= nw - 8 and h >= nh - 8:
                continue
            if y < 2 or y + h > nh - 2:
                continue
            out.append((x, y, w, h))
        return out

    @staticmethod
    def title_strip(y, h):
        """True when a rectangle at y with height h is the title strip (the top band of a gump)."""
        return y <= Kit.MARGIN + 2 and h <= 31

    @staticmethod
    def _maps(rec):
        """Build the two axis maps and the background list of a record, then anchor every placed piece."""
        nw, nh = rec["nat"]
        N, Hn = rec["size"]
        k = rec.get("k", 1.0)
        M = Kit.MARGIN * k
        bgs = Fill._bgs(rec)
        tall = [b for b in bgs if b[3] > Fill.ROW_H]
        rec["rows"] = not tall
        rec["fx"] = Fill._axis(nw * k, N, M, [(b[0] * k, (b[0] + b[2]) * k) for b in bgs], rec["mode"])
        rec["fy"] = Fill._axis(nh * k, Hn, M, [(b[1] * k, (b[1] + b[3]) * k) for b in (tall or bgs)
                                               if not Fill.title_strip(b[1], b[3])], rec["mode"])
        rec["bgs"] = bgs
        for e in rec["ent"].values():
            Fill._anchor(e, bgs)

    @staticmethod
    def _anchor(e, bgs):
        """Give a placed entry the smallest background that holds its centre (stored in the anchor slot)."""
        if e[0] == "s":
            return
        cx, cy = e[1] + e[3] / 2.0, e[2] + e[4] / 2.0
        best = None
        for x, y, w, h in bgs:
            if (x <= cx <= x + w and y <= cy <= y + h and (best is None or w * h < best[2] * best[3])):
                best = (x, y, w, h)
        e[5] = best

    @staticmethod
    def _apply(rec, pairs=None):
        """Move every recorded control (or only pairs) to its transformed rectangle.

        Controls that were disposed are dropped from the caches. A control is only touched when its
        rectangle changed; a pure move uses the cheaper SetPos.
        """
        for c, e in (list(rec["ent"].items()) if pairs is None else pairs):
            try:
                if c.IsDisposed:
                    rec["ent"].pop(c, None)
                    Fill.by_raw.pop(c, None)
                    Fill._wraps.pop(c, None)
                    continue
            except Exception:
                continue
            r = Fill._xform(rec, e)
            if r != e[6] and Fill._set(c, r, e[0] == "p" and rec.get("k", 1.0) == 1.0 and (r[2], r[3]) == (e[3], e[4])):
                e[6] = r

    @staticmethod
    def fit(g, x, y, W, H, mode="anchor"):
        """Fit gump g to the slot x, y, W, H and place it there.

        mode is anchor, grid or frame and decides how pieces follow the stretch. Returns None when the
        fitter cannot work (broken, no API type, nothing flushed), False when nothing needed changing, and
        True when the gump was resized or moved. Runs on the client tick; a full child sweep is only done
        now and then, otherwise the child counts are compared.
        """
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
                   "placed": None, "scroll": False, "bgs": [], "frame": set(), "k": 1.0, "desc": {}, "nested": False,
                   "head0": (info["head"] if info is not None else None) or (Kit.MARGIN + 30 + Kit.GAP)}
            fr = Kit._frames.get(g)
            rec["frame"].update(pr for pr in map(Kit.client_control, fr["pieces"] if fr else ()) if pr is not None)
            Fill.recs[g] = rec
        # The gump changed natural size by itself (for example a page switch): learn the new size.
        elif rec["placed"] is not None and info is None:
            r = Snap.rect(g)
            if r is not None and (r[2], r[3]) != rec["placed"][2:]:
                rec["nat"] = (r[2], r[3])
                rec["size"] = None
        rec["mode"] = mode
        skip, area = Kit._scroll_skip(g)
        try:
            cnt = (int(raw.Children.Count), int(area.Children.Count) if area is not None else 0)
        except Exception:
            cnt = None
        now = time.time()
        # The cheap child count must match and the periodic full sweep must not be due, else recount.
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
        nw, nh = rec["nat"]
        band = Kit.SCROLL_BAND
        conv = g in Kit._scrolled
        # A gump that already scrolls (converted) only shrinks to fit; a plain one may also start scrolling.
        if conv:
            Wb = W - band
            k = 1.0 if (Wb >= nw and H >= nh) else min(1.0, Wb / float(nw), max(Fill.FILL_MIN_K, H / float(nh)))
            scroll = nh * k > H + 1
        else:
            k, scroll = Fill.scale_for(nw, nh, W, H, rec["nested"])
        size = (W - band, int(round(nh * k)) if scroll else H) if scroll or conv else (W, H)
        if abs(k - rec["k"]) > 0.0005:
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
        if r is not None and (r[0], r[1], r[2], r[3]) == (TAB_X if g in Kit._behind else x, y, W, H) and not new \
                and rec["placed"] is not None:
            return False
        if scroll or conv:
            head = int(round(rec["head0"] * k))
            Kit._place_raw(g, x, y, size[0], size[1], head, H)
        else:
            Kit._place_raw(g, x, y, W, H, None, None)
        r = Snap.rect(g)
        rec["placed"] = (x, y, r[2], r[3]) if r is not None else (x, y, W, H)
        rec["slot"] = (x, y, W, H)
        return True

    @staticmethod
    def scale_for(nw, nh, W, H, nested=False):
        """Return (scale, scrolls) for a gump of natural size nw, nh in a slot W, H.

        The scale never goes below FILL_MIN_K for height; below that the gump scrolls instead. A gump with
        nested scroll areas shrinks both ways and never scrolls.
        """
        nw, nh = float(max(1, nw)), float(max(1, nh))
        if W >= nw and H >= nh:
            return 1.0, False
        if nested:
            return min(1.0, W / nw, H / nh), False
        k = min(1.0, W / nw, max(Fill.FILL_MIN_K, H / nh))
        if nh * k > H + 1:
            k = min(1.0, (W - Kit.SCROLL_BAND) / nw, max(Fill.FILL_MIN_K, H / nh))
            return k, nh * k > H + 1
        return k, False

    @staticmethod
    def unfit(g):
        """Undo a fit: put every control back to its natural rectangle and scale, and restore the gump size.

        Returns False when the gump was not fitted.
        """
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
            Fill._wraps.pop(c, None)
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
        """Map a point (rf) that sat beside rectangle r to the matching point beside the new rectangle nr.

        Returns (x, y). Used to keep a neighbour's relative offset when a gump is resized.
        """
        def one(f0, f1, a0, a1, b0, b1):
            """Map one axis: keep the distance to the edge the point is nearest, else keep the offset to the
            start.
            """
            if f0 >= a1:
                return b1 + (f0 - a1)
            if f1 <= a0:
                return b0 - (a0 - f0)
            return f0 + (b0 - a0)

        return (one(rf[0], rf[0] + rf[2], r[0], r[0] + r[2], nr[0], nr[0] + nr[2]),
                one(rf[1], rf[1] + rf[3], r[1], r[1] + r[3], nr[1], nr[1] + nr[3]))

    @staticmethod
    def prune():
        """Forget records of gumps that are no longer open, and rebuild by_raw if it grew past 20000 entries."""
        if not Fill.recs:
            return
        for g in [g for g in Fill.recs if not Kit.is_open(g)]:
            rec = Fill.recs.pop(g)
            for c in rec["ent"]:
                Fill.by_raw.pop(c, None)
                Fill._wraps.pop(c, None)
        if len(Fill.by_raw) > 20000:
            Fill.by_raw.clear()
            for rec in Fill.recs.values():
                for c, e in rec["ent"].items():
                    Fill.by_raw[c] = (rec, e)

    @staticmethod
    def entry(c):
        """Return the (record, entry) that holds control c, or None when c is not fitted."""
        return Fill.by_raw.get(Fill.raw_of(c)) if Fill.recs else None

    @staticmethod
    def change(c, x=None, y=None, w=None, h=None):
        """Change the natural x, y, w or h of a fitted control and place it by the current transform.

        Returns False when the control is not fitted or the record has no size yet.
        """
        hit = Fill.entry(c)
        if hit is None:
            return False
        rec, e = hit
        for i, v in ((1, x), (2, y), (3, w), (4, h)):
            if v is not None:
                e[i] = int(v)
        if rec["size"] is None:
            return False
        if e[0] == "p" and (x is not None or y is not None):
            Fill._anchor(e, rec["bgs"])
        r = Fill._xform(rec, e)
        try:
            if e[0] == "p" and w is None and h is None:
                c.SetPos(r[0], r[1])
            else:
                c.SetRect(r[0], r[1], r[2], r[3])
            e[6] = r
        except Exception:
            return False
        return True

    @staticmethod
    def own(c):
        """Return the natural (x, y, w, h) of a fitted control, or None when it is not fitted."""
        hit = Fill.entry(c)
        return None if hit is None else tuple(hit[1][1:5])


class PageCanvas(object):
    """Stand-in for a gump while a settings page is built: it records every control added.

    Pages call Add on this canvas; the controls are kept in ctrls so the page can be moved or removed
    later, and everything else is passed through to the real gump when there is one.
    """
    def __init__(self, inner):
        """Wrap the real gump (or None) in inner and start with empty control and section lists."""
        self._inner = inner
        self.ctrls = []
        self.sections = []

    def Add(self, ctrl, *args):
        """Remember the control, then add it to the real gump if there is one and return it."""
        self.ctrls.append(ctrl)
        if self._inner is not None:
            return self._inner.Add(ctrl, *args)
        return ctrl

    def __getattr__(self, name):
        """Pass every other attribute to the wrapped gump; raise AttributeError when there is none."""
        if self._inner is None:
            raise AttributeError(name)
        return getattr(self._inner, name)


class Alerts(object):
    """The shared alert centre: one list of alert kinds, a banner, sounds and map pings for every module.

    Modules register a kind and raise alerts. Each alert goes to the system message line, to the alert
    history, to a sound queue, to a banner window and optionally to a map ping. The player's choices
    (mute, banner, quiet time, per-kind on/off and sound) are saved under KEY and the history under
    LOG_KEY. While quiet time is on, alerts are kept in the history only: no sound and no banner.
    Runs on the client tick; tick does the timed work.
    """
    KEY = "VirtueAssistant_alerts"
    POS_KEY = "VirtueAssistant_alert_pos"
    W, H = 420, 46
    LEVELS = {"info": Kit.HUE_INFO, "warn": Kit.HUE_TITLE, "alarm": Kit.HUE_BAD}
    TEST_KEY = "va.test"
    LOG_KEY = "VirtueAssistant_alert_log"
    LOG_CAP = 50
    LOG_EVERY = 60.0
    LOG_CUT = 160
    QUIET_MAX = 1440
    QUIET_ALARM = 30.0

    def __init__(self):
        """Create the empty tables and flags; nothing is loaded until the first use."""
        self.kinds = {}
        self.order = []
        self.choice = {}
        self.banner_on = True
        self.mute = self.loaded = self.busy = self.shown = self.alarm = self.flash_on = self.clicked = False
        self.last = {}
        self.pending = []
        self.sounds = []
        self.pings = []
        self.sound_at = self.hide_at = self.flash_at = self.moved_at = 0.0
        self.g = self.pos = None
        self.c = {}
        self.count = 0
        self.hue = Kit.HUE_TITLE
        self.line = ""
        self.tw = self.W - 36
        self.scale = 1.0
        self.log = []
        self.log_ver = 0
        self.log_due = False
        self.log_at = 0.0
        self.quiet_until = 0
        self.bw = 30
        self.store = ({}, {})
        self.alarm_until = 0.0
        self.line_who = ("", 0)

    def load(self):
        """Read the saved choices and the history.

        KEY holds mute, banner, quiet (the time quiet ends) and one kind.<key>=on,sound entry per kind.
        LOG_KEY holds one history line per row, fields separated by a tilde: time, level, quiet flag, text,
        name and serial. Rows that do not parse are dropped and only the newest LOG_CAP are kept.
        """
        self.loaded = True
        self.choice = {}
        self.mute, self.banner_on = False, True
        self.quiet_until = 0
        for k, v in Kit.codec_load(Kit.get_var(self.KEY)).items():
            if k == "mute":
                self.mute = v == "1"
            elif k == "banner":
                self.banner_on = v != "0"
            elif k == "quiet":
                try:
                    self.quiet_until = int(v)
                except ValueError:
                    self.quiet_until = 0
            elif k.startswith("kind."):
                bits = v.split(",")
                try:
                    snd = int(bits[1]) if len(bits) > 1 and bits[1] != "" else None
                except ValueError:
                    snd = None
                self.choice[k[5:]] = [bits[0] != "0", snd]
        log = []
        for ln in Kit.get_var(self.LOG_KEY).split("\n"):
            b = ln.split("~", 5)
            if len(b) < 4:
                continue
            try:
                t, ser = float(b[0]), int(b[5]) if len(b) > 5 and b[5] else 0
            except ValueError:
                continue
            log.append((t, b[1], b[3], "", b[2] == "q", b[4] if len(b) > 4 else "", ser))
        self.log = log[-self.LOG_CAP:]
        self.log_ver += 1
        self.log_due = False

    def save(self):
        """Write mute, banner, every per-kind choice and the quiet end time back to KEY as one semicolon list."""
        parts = ["mute=%d" % (1 if self.mute else 0), "banner=%d" % (1 if self.banner_on else 0)]
        for k in sorted(self.choice):
            on, snd = self.choice[k]
            parts.append("kind.%s=%d,%s" % (k, 1 if on else 0, "" if snd is None else int(snd)))
        parts.append("quiet=%d" % int(self.quiet_until))
        Kit.put_var(self.KEY, ";".join(parts))

    @staticmethod
    def _clip(s, n):
        """Make text safe for one history field: the tilde and line breaks become spaces, cut to n characters."""
        return re.sub(r"[~\r\n]", " ", str(s))[:n]

    @staticmethod
    def veiled(line, name, serial=0):
        """Replace the name in an alert line with its streamer mode stand-in (Kit.veil) when streamer mode is
        on. Only whole words match, so a name inside a longer word is left alone.
        """
        if not Kit.streamer or not name or name not in line:
            return line
        v = Kit.veil("name", name, serial)
        return re.sub(r"(?<!\w)%s(?!\w)" % re.escape(name), lambda m: v, line)

    @staticmethod
    def with_quiet(text, mine):
        """Join two saved alert lists for a profile: everything in text except its quiet entry, plus the quiet
        entry of mine (the one this character has now), so loading a profile never changes quiet time.
        """
        keep = [p for p in str(text or "").split(";") if p.strip() and not p.strip().startswith("quiet=")]
        return ";".join(keep + [p for p in str(mine or "").split(";") if p.strip().startswith("quiet=")][-1:])

    def shown_line(self):
        """The banner line as it is shown, with streamer mode applied."""
        return Alerts.veiled(self.line, *self.line_who)

    def save_log(self, now):
        """Write the alert history to LOG_KEY, one row per alert, and schedule the next save LOG_EVERY seconds
        on. Fields are cut to keep the saved value small.
        """
        self.log_due = False
        self.log_at = now + self.LOG_EVERY
        c = Alerts._clip
        rows = ("%d~%s~%s~%s~%s~%d" % (int(t), c(lv, 8), "q" if q else "", c(line, self.LOG_CUT), c(who, 40), ser)
                for t, lv, line, _k, q, who, ser in list(self.log))
        Kit.put_var(self.LOG_KEY, "\n".join(rows))

    def quiet_on(self, now=None):
        """True while quiet time is on: an end time in the future that is no more than QUIET_MAX minutes
        away (a clock that jumped is not trusted). now defaults to the current time.
        """
        if not self.loaded:
            self.load()
        left = self.quiet_until - (time.time() if now is None else now)
        return 0 < left <= 60 * self.QUIET_MAX

    def quiet(self, minutes=30):
        """Start quiet time for the given minutes (1 to QUIET_MAX): drop queued sounds and banners, save,
        refresh the settings page and say when it ends in the system line.
        """
        if not self.loaded:
            self.load()
        m = max(1, min(self.QUIET_MAX, int(minutes)))
        self.quiet_until = int(time.time() + 60 * m)
        self.sounds, self.pending = [], []
        self.save()
        HOST.refresh_settings(ALERTS_PAGE)
        API.SysMsg("Alerts: quiet until %s." % time.strftime("%H:%M", time.localtime(self.quiet_until)), Kit.HUE_INFO)

    def resume(self):
        """End quiet time at once, save, refresh the settings page and say so in the system line."""
        if not self.loaded:
            self.load()
        self.quiet_until = 0
        self.save()
        HOST.refresh_settings(ALERTS_PAGE)
        API.SysMsg("Alerts: back on.", Kit.HUE_INFO)

    def quiet_alarm(self, now=None):
        """True for QUIET_ALARM seconds after an alarm came in during quiet time, so the host can still show
        that something urgent happened. now defaults to the current time.
        """
        left = self.alarm_until - (time.time() if now is None else now)
        return 0 < left <= self.QUIET_ALARM

    def toggle_quiet(self):
        """Start quiet time for 30 minutes, or end it when it is on (the hotkey and launcher action)."""
        if self.quiet_on():
            self.resume()
        else:
            self.quiet(30)

    def setting(self, key):
        """Return (on, sound id) for a kind: the saved choice, else on with the kind's own default sound."""
        if not self.loaded:
            self.load()
        k = self.kinds.get(key)
        ch = self.choice.get(key)
        on = ch[0] if ch is not None else True
        snd = ch[1] if ch is not None and ch[1] is not None else (k["sound"] if k else 0)
        return on, int(snd or 0)

    def choose(self, key, on=None, sound=None):
        """Change the on/off flag and/or the sound of a kind and save when something changed."""
        cur = self.setting(key)
        new = [cur[0] if on is None else bool(on), cur[1] if sound is None else int(sound)]
        if new != list(cur) or key not in self.choice:
            self.choice[key] = new
            self.save()

    def kind(self, key, label, sound=None, owner=None):
        """Register or update an alert kind (label, default sound, owner) and return its key.

        The settings page is refreshed when the kind is new or changed, except for the built-in test kind.
        """
        key = str(key)
        k = self.kinds.get(key)
        new = {"label": str(label or key), "sound": int(sound or 0), "owner": str(owner or APP_NAME)}
        if k is None:
            self.order.append(key)
        if new != k:
            self.kinds[key] = new
            if key != self.TEST_KEY:
                HOST.refresh_settings(ALERTS_PAGE)
        return key

    def raise_(self, key, text, level="warn", sound=None, ping=None, who=None, owner=None, name=None, serial=None):
        """Raise an alert and return True, or False when the kind is off or the alert repeats too soon.

        key is the kind, text the message, level one of info, warn or alarm (the colour; alarm also flashes
        the banner until clicked). who tells apart alerts of one kind for the repeat limit (default: the
        text). name and serial say which player the alert is about, for streamer mode. The message goes to
        the system line and the history; a sound is played or queued and a banner is queued, unless quiet
        time is on (history only); an optional map ping (x, y) is queued for the pings service.
        """
        if not self.loaded:
            self.load()
        key = str(key)
        k = self.kinds.get(key)
        # A kind that was never registered is created on the fly, so a module may raise without setup.
        if k is None:
            self.kind(key, key, sound, owner)
            k = self.kinds[key]
        on, snd = self.setting(key)
        if not on:
            return False
        now = time.time()
        rk = (key, str(who) if who is not None else str(text))
        t = self.last.get(rk)
        # Same kind and same subject repeat at most once every ALERT_RATE seconds. A clock that went
        # backwards also lets the alert through.
        if t is not None and 0 <= now - t < ALERT_RATE:
            return False
        # Keep the repeat table small: drop entries that have expired.
        if len(self.last) > 200:
            cut = now - ALERT_RATE
            for old in [x for x, tt in self.last.items() if tt < cut or tt > now]:
                del self.last[old]
        self.last[rk] = now
        who_t = k["owner"]
        text = str(text)
        # The owner name leads the line unless the text already starts with it.
        line = text if text.startswith(who_t + ":") else "%s: %s" % (who_t, text)
        nm = str(name) if name else who if isinstance(who, str) and len(who) > 1 else ""
        try:
            ser = int((0 if isinstance(who, str) else who) if serial is None else serial) or 0
        except (TypeError, ValueError):
            ser = 0
        hue = self.LEVELS.get(level, Kit.HUE_TITLE)
        API.SysMsg(Alerts.veiled(line, nm, ser), hue)
        quiet = self.quiet_on(now)
        self.log.append((now, str(level), line, key, quiet, nm, ser))
        if len(self.log) > self.LOG_CAP:
            del self.log[:-self.LOG_CAP]
        self.log_ver += 1
        self.log_due = True
        if quiet and level == "alarm":
            self.alarm_until = now + self.QUIET_ALARM
        # A sound given in the call wins over the saved one; a sound of 0 means silent.
        sid = (int(sound) if sound else snd) if snd else 0
        if sid and not self.mute and not quiet and len(self.sounds) < 4:
            if not self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP:
                self._play(sid, now)
            else:
                self.sounds.append(sid)
        if self.banner_on and not quiet:
            self.pending.append((line, hue, level == "alarm", nm, ser))
            if len(self.pending) > 50:
                del self.pending[:-50]
        if ping is not None and len(self.pings) < 8:
            safe(lambda: self.pings.append([int(ping[0]), int(ping[1]), now + 10.0]))
        self.busy = True
        return True

    def _play(self, sid, now):
        """Play sound sid now and note the time, for the gap between sounds."""
        self.sound_at = now
        API.PlaySound(int(sid))

    def tick(self, now):
        """Drive the queued sounds, map pings and banner; client tick, only while there is work (busy).

        Saves the history when it is due. Plays the next queued sound once the gap has passed, sends the
        oldest ping through the pings service (dropping it when sent, expired or the service is missing),
        shows queued banner lines and watches the banner that is up.
        """
        if self.log_due and not 0 <= self.log_at - now <= self.LOG_EVERY:
            self.save_log(now)
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
                    done = bool(fn(x, y))
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
        """Show the newest queued line on the banner, counting the others as +N more.

        Builds the banner window when it is not open, makes it visible and restarts the hold and flash
        timers. items are (line, hue, alarm, name, serial) rows.
        """
        if not self.banner_on:
            return
        line, hue, alarm, nm, ser = items[-1]
        if self.shown and Kit.is_open(self.g):
            self.count += len(items)
            self.alarm = self.alarm or any(it[2] for it in items)
        else:
            self.count = len(items) - 1
            self.alarm = any(it[2] for it in items)
        self.line, self.hue, self.line_who = line, hue, (nm, ser)
        if not Kit.is_open(self.g):
            self._build()
        if self.g is None:
            return
        self._label()
        if not self.shown:
            Kit.set(self.g, "IsVisible", True)
            self.shown = True
            self.clicked = False
            self.pos = Snap.pos(self.g)
        self.hide_at = now + ALERT_HOLD
        self.flash_at = now + ALERT_FLASH
        self.flash_on = True

    def _label(self):
        """Put the banner text on its label, shortened to fit beside the +N more label, with streamer mode
        applied to the line.
        """
        c = self.c
        more = ("+%d more" % self.count) if self.count > 0 else ""
        mw = Kit.text_px(more) if more else 0
        bw = self.bw + 6
        tw = self.W - 36 - bw - ((mw + 8) if more else 0)
        self.tw = tw
        Kit.set_text(c["text"], Kit.fit(self.shown_line(), tw), self.hue)
        Kit.set_text(c["more"], more, Kit.HUE_INFO)
        if more:
            s = self.scale
            c["more"].SetPos(int(round((self.W - 18 - bw - mw) * s)), int(round(15 * s)))

    def _watch(self, now):
        """Keep the banner alive: notice a move or a click, flash an alarm, hide a normal alert after its hold
        time.
        """
        g = self.g
        if not Kit.is_open(g):
            self.shown, self.g = False, None
            return
        p = Snap.pos(g)
        if p != self.pos:
            if self.pos is not None:
                self.moved_at = now
            self.pos = p
        # A click that came with a drag (the window moved just now) is a move, not a dismiss.
        if self.clicked:
            self.clicked = False
            if not 0 <= now - self.moved_at <= 0.35:
                self.dismiss()
                return
        if self.alarm:
            if not 0 < self.flash_at - now <= ALERT_FLASH:
                self.flash_at = now + ALERT_FLASH
                self.flash_on = not self.flash_on
                Kit.set_text(self.c["text"], Kit.fit(self.shown_line(), self.tw), Kit.HUE_BAD
                             if self.flash_on else Kit.HUE_TEXT)
        elif not 0 < self.hide_at - now <= ALERT_HOLD:
            self.dismiss()

    def dismiss(self):
        """Hide the banner and clear its counters."""
        self.shown, self.count, self.alarm = False, 0, False
        g = self.g
        if Kit.is_open(g):
            Kit.set(g, "IsVisible", False)

    def _click(self):
        """Click handler of the banner catcher: note the click for the next watch and wake the tick."""
        self.clicked = True
        self.busy = True

    def _build(self):
        """Create the banner window (hidden at first) at its saved position, or near the top centre of the
        screen, at the interface text scale.

        The catcher over the whole window turns clicks into dismiss and lets the window be dragged. A
        button on its right opens the alert history.
        """
        W, H, s = self.W, self.H, Kit.tscale
        WS, HS = int(round(W * s)), int(round(H * s))
        sw = Kit.screen()[0] or 1024
        x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 60), (WS, HS))
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H, corners=False)
        Kit.add_section(g, 8, 8, W - 16, H - 16)
        c = {"text": Kit.add_label(g, "", 18, 15, Kit.HUE_TITLE),
             "more": Kit.add_label(g, "", W - 60, 15, Kit.HUE_INFO)}
        Kit.catcher(g, 0, 0, W, H, self._click, "Click to dismiss; drag to move", movable=True)
        bw, bh = Kit.pic_size(Kit.ART_PAGE[0])
        self.bw, bh = bw or 30, bh or 22
        self.store = ({}, {})
        Binds.scoped("va.banner", Kit.art_button, g, self.store, "history", Kit.ART_PAGE, W - 12 - self.bw,
                     (H - bh) // 2, None, "Show the last 50 alerts", None, lambda: HOST.alert_log.open())
        self.scale = s if Kit.scale_window(g, s) else 1.0
        if self.scale == 1.0:
            WS, HS = W, H
        Kit.show_window(g, x, y, WS, HS, None, False, None, lambda: Kit.save_pos(self.POS_KEY, self.g))
        self.g, self.c = g, c
        self.shown = False

    def rebuild(self):
        """Draw the banner again after a look or text size change, keeping its place and whether it was
        showing.
        """
        g = self.g
        up = self.shown and Kit.is_open(g)
        if g is None:
            return
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        self.g = None
        Kit.dispose(g)
        self.shown = False
        if not up:
            return
        self._build()
        if self.g is None:
            return
        self._label()
        Kit.set(self.g, "IsVisible", True)
        self.shown = True
        self.pos = Snap.pos(self.g)

    def close(self):
        """Close the banner window, save its place and the history, and drop everything still queued."""
        if self.log_due:
            self.save_log(time.time())
        g, self.g = self.g, None
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)
        self.shown = False
        self.pending, self.sounds, self.pings = [], [], []
        self.busy = False


class AlertLog(object):
    """The alert history window: the newest 50 alerts as lines coloured by level, newest first, with the
    time of day. Opened from the banner, the Alerts settings page or the launcher; client tick.
    """
    W = 600
    ROW = 20
    POS_KEY = "VirtueAssistant_alert_log_pos"
    EVERY = 1.0
    TITLE = "ALERT HISTORY"

    def __init__(self):
        """Start closed."""
        self.g = None
        self.store = ({}, {})
        self.ver = -1
        self.next = 0.0
        self.want = 0.0

    def open(self):
        """Ask for the window to open on the next client tick. Repeated asks within 2 seconds are ignored."""
        now = time.time()
        if 0 <= now - self.want < 2.0:
            return
        self.want = now
        Kit.pending.append(self._open)
        HOST.poke()

    def _open(self):
        """Open the window on the client tick (or draw it again when it is already up), loading the history
        first when it has not been read.
        """
        self.want = 0.0
        if not ALERTS.loaded:
            ALERTS.load()
        if Kit.is_open(self.g):
            self.rebuild()
        else:
            Binds.scoped("va.alertlog", self._build)

    def rows(self):
        """Build the window's lines from the history as (text, hue) pairs, newest first. A quiet alert is
        marked "(quiet)" and drawn in the information colour; names follow streamer mode.
        """
        out = []
        tw = self.W - 2 * Kit.MARGIN - 24
        for t, level, line, _key, quiet, who, ser in reversed(list(ALERTS.log)):
            line = Alerts.veiled(line, who, ser)
            head = time.strftime("%H:%M", time.localtime(t)) + "  "
            tail = "  (quiet)" if quiet else ""
            text = head + Kit.fit(line, tw - Kit.text_w(head) - Kit.text_w(tail)) + tail
            out.append((text, Kit.HUE_INFO if quiet else Alerts.LEVELS.get(level, Kit.HUE_TITLE)))
        return out

    def _build(self):
        """Draw the window: title section, close button and one label per history line, scaled to the text
        size, placed at its saved position (or near the top centre) and added in front of the other windows.
        """
        M, W, s = Kit.MARGIN, self.W, Kit.tscale
        rows = self.rows()
        self.store = ({}, {})
        self.ver = ALERTS.log_ver
        self.next = time.time() + self.EVERY
        h_body = 16 + self.ROW * max(1, len(rows))
        H = M + 30 + Kit.GAP + h_body + M
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, self.TITLE, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close")
        yb = M + 30 + Kit.GAP
        Kit.add_section(g, M, yb, W - 2 * M, h_body)
        if not rows:
            Kit.add_label(g, "No alerts yet.", M + 12, yb + 8, Kit.HUE_INFO)
        for i, (text, hue) in enumerate(rows):
            Kit.add_label(g, text, M + 12, yb + 8 + self.ROW * i, hue)
        sc = s if Kit.scale_window(g, s) else 1.0
        WS, HS = int(round(W * sc)), int(round(H * sc))
        sw = Kit.screen()[0] or 1024
        x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 80), (WS, HS))
        Kit.place(g, x, y, WS, HS, int(round((M + 30 + Kit.GAP) * sc)))
        Kit.add_front(g)
        Kit.on_moved(g, lambda: Kit.save_pos(self.POS_KEY, self.g))
        self.g = g

    def rebuild(self):
        """Close the drawn window (saving its place) and draw it again from the current history."""
        g, self.g = self.g, None
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)
        Binds.scoped("va.alertlog", self._build)

    def poll(self, now):
        """Called each UI pass while the window is open: close it when the player closed it or clicked close,
        and redraw it when the history changed, at most once per EVERY seconds.
        """
        g = self.g
        if g is None:
            return
        if not Kit.is_open(g) or Kit.was_clicked(self.store, "close"):
            self.close()
            return
        if self.ver != ALERTS.log_ver and not 0 <= self.next - now <= self.EVERY:
            self.rebuild()

    def close(self):
        """Close the window and save its place."""
        g, self.g = self.g, None
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)


class Guard(object):
    """Remembers whether the player is inside a town guard zone, for modules that must not harm there.

    The journal tells when the guards' protection is entered or left; the last answer and place are
    saved under KEY so that a restart in the same spot still knows. Known guard areas also answer.
    """
    KEY = "VirtueAssistant_guard"
    EVERY = 0.25
    # The client's message numbers (Cliloc.enu) for the same four guard lines, mapped to the English text
    # they stand for, so a line in other words still counts (Journal.said).
    NUMS = {500112: GUARD_IN_TEXTS[0], 500114: GUARD_IN_TEXTS[0], 500113: GUARD_OUT_TEXTS[0],
            500115: GUARD_OUT_TEXTS[1]}

    def __init__(self):
        """Start with no known state and an empty answer cache."""
        self.state = self.rd = self.saved = None
        self.next = 0.0
        self.cache = (0.0, None, None)

    def tick(self, now):
        """Read new journal lines for the guard messages and update the state; client tick, every EVERY
        seconds at most.

        A change of state is saved with the player's position.
        """
        if now < self.next and self.next - now <= self.EVERY:
            return
        self.next = now + self.EVERY
        if self.rd is None:
            self.rd = Journal.reader()
            self.rd.last = 0
        for ln in self.rd.new():
            low = Journal.said(ln, self.NUMS)
            if "protection of the town guards" not in low:
                continue
            # Only system lines count; a line spoken by a player carries a name.
            if ln.name and ln.name.lower() != "system":
                continue
            new = False if low.startswith(GUARD_OUT_TEXTS) else True if low.startswith(GUARD_IN_TEXTS) else None
            if new is not None and new != self.state:
                self.state = new
                self.cache = (0.0, None, None)
                self._save(new)

    @staticmethod
    def _where():
        """Return the player's (x, y, map) or None when the player cannot be read."""
        try:
            p = HOST.me()
            return int(p.X), int(p.Y), int(API.GetMap())
        except Exception:
            return None

    def _save(self, state):
        """Save the guard state and the place where it was seen under KEY as state,x,y,map."""
        w = self._where()
        if w is None or not (w[0] or w[1]):
            return
        self.saved = (state, w[0], w[1], w[2])
        Kit.put_var(self.KEY, "%d,%d,%d,%d" % (1 if state else 0, w[0], w[1], w[2]))

    def store(self):
        """Save the current state with the current place, if a state is known."""
        if self.state is not None:
            self._save(self.state)

    def _look(self):
        """Return (guarded, area name) for the player's place, cached for a second.

        A known guard area gives True and its name. Otherwise, with no journal answer yet, the saved state
        is
        used when the player stands within GUARD_SPOT tiles of where it was saved on the same map.
        """
        now = time.time()
        if now < self.cache[0] <= now + 1.0:
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
                if s[0] is not None and s[3] == m and abs(s[1] - x) <= GUARD_SPOT and abs(s[2] - y) <= GUARD_SPOT:
                    state = s[0]
        self.cache = (now + 1.0, state, name)
        return state, name

    def guarded(self):
        """True or False when it is known whether the player is under guard protection, None when not known."""
        if self.state is not None:
            return self.state
        return self._look()[0]

    def area(self):
        """Name of the guard area the player is standing in, or None."""
        return self._look()[1]


class _Page(object):
    """Base class of a settings page of the mother script (Alerts and Keys)."""
    def __init__(self):
        """Start with no controls and an empty click store."""
        self.c = None
        self.store = ({}, {})

    def closed(self):
        """Called when the settings window closes: forget the controls."""
        self.c = None

    def api(self):
        """Return the settings page hooks (height, build, poll and closed) the settings window calls."""
        return {"config_height": self.height, "build_config": self.build,
                "poll_config": self.poll, "config_closed": self.closed}


class AlertsPage(_Page):
    """Settings page listing every alert kind with its on/off box and sound, plus the mute, banner, quiet
    time and history controls.
    """
    def kinds(self):
        """Alert kinds to list, without the test kind."""
        return [k for k in ALERTS.order if k != Alerts.TEST_KEY]

    QUIET_CAPS = ("Quiet 30 min", "Resume")

    def table(self, w):
        """Return the form table for the page at width w: the global options, then the per-kind section.

        The quiet button reads Quiet 30 min or Resume, and a note beside it says when quiet time ends.
        """
        q = ALERTS.quiet_on()
        qx = 12 + 35 + max(Kit.text_w(c) for c in self.QUIET_CAPS) + 20 + 35
        qx += Kit.text_w("History") + 20
        note = ("Quiet until %s" % time.strftime("%H:%M", time.localtime(ALERTS.quiet_until))) if q else ""
        quiet = (("quiet", Kit.ART_PLAY, self.QUIET_CAPS[1], "Turn alert sounds and banners back on") if q else
                 ("quiet", Kit.ART_PLAY, self.QUIET_CAPS[0], "No alert sounds or banners for 30 minutes; journal "
                  "lines and the history stay"))
        return (("ALERTS  (every module's warnings)", (("check", "mute", "Mute every alert sound",
                     "No alert sounds; banners and journal lines stay", {"stay": True}),
                    ("check", "banner", "Show the banner", "Show alerts in a banner (click to dismiss, drag to move)",
                     {"dx": 242}), ("buttons", (("test", Kit.ART_PLAY, "Test alert",
                                  "Raise a test alert"),), {"bdy": 4, "stay": True}),
                    ("note", "The same alert repeats at most every %d s." % int(ALERT_RATE), {"dx": 172, "ndy": 7}),
                    ("buttons", (quiet, ("history", Kit.ART_PAGE, "History", "Show the last 50 alerts")),
                     {"bdy": 4, "stay": True}), ("note", note, {"dx": qx, "ndy": 7})),
                 {"top": 32, "sh": 118}), (Kit.fit("ALERT KINDS  (from modules on this session)", w - 16),
                 (("custom", 0, self._kinds),), {"sh": 40 + 28 * max(1, len(self.kinds()))}))

    def height(self, w):
        """Height of the page at width w."""
        return Kit.Form.height(self.table(w), w)

    def build(self, g, x, y, w):
        """Build the page into gump g at x, y, w from the form table; loads the saved choices first and
        remembers whether quiet time was on, so poll can redraw when it changes.
        """
        if not ALERTS.loaded:
            ALERTS.load()
        self.store = ({}, {})
        self.quiet_drawn = ALERTS.quiet_on()
        self.c = Kit.Form(g, x, y, w, {"mute": ALERTS.mute, "banner": ALERTS.banner_on}, self.table(w), self.store).c

    def _kinds(self, f, x, y):
        """Custom section: one row per alert kind (check box, owner, play button and sound drop-down).

        The drop-downs are added after the rows so they sit on top of the other controls.
        """
        g, w, c, kinds = f.g, f.w, f.c, self.kinds()
        c.update(rows=[], dd=[])
        if not kinds:
            Kit.add_label(g, "No alerts yet: turn on a module that has some.", x + 12, y + 6, Kit.HUE_INFO)
        dd_w = 150
        x_dd = x + w - 12 - 30 - 8 - dd_w
        later = []
        for i, key in enumerate(kinds):
            k = ALERTS.kinds[key]
            on, snd = ALERTS.setting(key)
            ry = y + 4 + 28 * i
            label = Kit.fit(k["label"], 196)
            cb = Kit.add_check(g, label, x + 12, ry, on, "Raise the %s alert" % k["label"])
            Kit.add_label(g, Kit.fit(k["owner"], x_dd - 8 - (x + 236)), x + 236, ry + 2, Kit.HUE_INFO)
            Kit.art_button(g, self.store, "play%d" % i, Kit.ART_PLAY, x + w - 12 - 30, ry - 2,
                           None, "Play this alert's sound")
            ids = [sid for _, sid in ALERT_SOUNDS]
            names = [n for n, _ in ALERT_SOUNDS]
            if snd not in ids:
                ids.append(snd)
                names.append("Sound 0x%X" % snd)
            later.append((key, ids, names, ids.index(snd), x_dd, ry))
            c["rows"].append((key, cb))
        for key, ids, names, idx, dx, dy in later:
            dd = G.CreateDropDown(dd_w, names, idx)
            dd.SetPos(dx, dy)
            g.Add(dd)
            Kit.with_tip(dd, "This alert's sound")
            c["dd"].append((key, dd, ids, idx))

    def poll(self):
        """Apply what the player changed on the page; called while the page is open.

        Writes mute, banner and per-kind boxes and sounds back to the alert centre, plays a sound when its
        button is clicked, raises a test alert when the test button is clicked, starts or ends quiet time,
        opens the history window, and redraws the page when quiet time starts or ends by itself.
        """
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
        if Kit.was_clicked(self.store, "test"):
            ALERTS.kind(Alerts.TEST_KEY, "Test", 0x1EA, APP_NAME)
            ALERTS.last.pop((Alerts.TEST_KEY, "test"), None)
            ALERTS.raise_(Alerts.TEST_KEY, "This is how an alert looks and sounds.", "warn", who="test")
        if Kit.was_clicked(self.store, "quiet"):
            ALERTS.toggle_quiet()
        if Kit.was_clicked(self.store, "history"):
            HOST.alert_log.open()
        q = ALERTS.quiet_on()
        if q != self.quiet_drawn:
            self.quiet_drawn = q
            HOST.refresh_settings(ALERTS_PAGE)
        for n, row in enumerate(c["dd"]):
            key, dd, ids, idx = row
            i = Kit.dd_index(dd, idx)
            if i != idx and 0 <= i < len(ids):
                idx = i
                c["dd"][n] = (key, dd, ids, i)
                ALERTS.choose(key, sound=ids[i])
            if Kit.was_clicked(self.store, "play%d" % n) and ids[idx]:
                API.PlaySound(int(ids[idx]))


class BackupPage(_Page):
    """Settings page for the backups of this character: Back up now, a drop-down of the saved backups and
    Restore.

    A backup is a folder holding every Virtue Assistant setting of this character, its unified bag
    layout and an info file. The KEEP newest are kept. One is made by hand, one before a restore and
    one the first time a new version starts. Restore asks twice (ARM seconds to confirm).
    """
    KEEP = 10
    ARM = 3.0
    DIR = "Backups"
    VER_KEY = "VirtueAssistant_backup_ver"
    AUTO = "before %s"
    SKIP = ("VirtueAssistant_starting", "VirtueAssistant_backup_ver")

    def __init__(self):
        """Start with no backup list read, nothing picked and nothing armed."""
        _Page.__init__(self)
        self.items = None
        self.sel = 0
        self.armed = (None, 0.0)
        self.pick = None

    def table(self, w):
        """The form table for the page: one section with the two buttons, the backup drop-down and a note
        saying where the files are. w is not used.
        """
        return (("BACKUPS  (this character)", (
            ("buttons", (("backup_now", Kit.ART_OK, "Back up now", "Save every Virtue Assistant setting of this "
                          "character now (the 10 newest are kept)"),
                         ("restore", Kit.ART_PLAY, "Restore", "Put the picked backup back (press twice; the "
                          "settings of now are backed up first)"))),
            ("custom", 30, self._list), ("note", "In the VirtueAssistantSettings folder, Backups")), {}),)

    def height(self, w):
        """Height of the page at width w."""
        return Kit.Form.height(self.table(w), w)

    def build(self, g, x, y, w):
        """Build the page into gump g at x, y, w from the form table."""
        self.store = ({}, {})
        self.c = Kit.Form(g, x, y, w, {}, self.table(w), self.store).c

    def _list(self, f, x, y):
        """Custom row: the drop-down of backups, keeping the picked one selected when the list is redrawn.
        Shows a waiting or empty line when there is nothing to pick.
        """
        items = self.items or []
        names = [lbl for _, lbl in items]
        if not names:
            names = ["Reading the backups" if self.items is None else "No backups yet"]
        at = [i for i, it in enumerate(items) if it[0] == self.pick]
        self.sel = at[0] if at else max(0, min(self.sel, len(names) - 1))
        dd = G.CreateDropDown(min(380, f.w - 24), names, self.sel)
        dd.SetPos(x + 12, y + 2)
        f.g.Add(dd)
        Kit.with_tip(dd, "The backup that Restore puts back")
        f.c["dd"] = dd

    def poll(self):
        """Take the drop-down pick, and handle the two buttons; called while the page is open.

        Back up now asks the host for a backup. Restore needs two clicks on the same backup within ARM
        seconds; the first one only arms it, so a stray click cannot overwrite settings.
        """
        c = self.c
        if c is None:
            return
        dd = c.get("dd")
        items = self.items or []
        if dd is not None:
            self.sel = Kit.dd_index(dd, self.sel)
        if 0 <= self.sel < len(items):
            self.pick = items[self.sel][0]
        if Kit.was_clicked(self.store, "backup_now"):
            self.ask(("backup", "by hand"))
        if not Kit.was_clicked(self.store, "restore"):
            return
        if not items:
            API.SysMsg("Backups: there is no backup to restore yet.", Kit.HUE_BAD)
            return
        name = items[max(0, min(self.sel, len(items) - 1))][0]
        now = time.time()
        a = self.armed
        if a[0] == name and 0 <= a[1] - now <= self.ARM:
            self.armed = (None, 0.0)
            self.ask(("restore", name))
            return
        self.armed = (name, now + self.ARM)
        API.SysMsg("Backups: press Restore again to confirm.", Kit.HUE_INFO)

    @staticmethod
    def ask(req):
        """Hand a backup or restore request to the host, which does it on the main loop (never inside a
        module tick). req is ("backup", why) or ("restore", name). Refused with a message while another
        request is waiting.
        """
        if HOST.profile_req is not None:
            API.SysMsg("Backups: busy saving; try again.", Kit.HUE_BAD)
            return
        HOST.profile_req = req
        HOST.poke()

    @staticmethod
    def base():
        """The folder that holds this character's backups: the Backups data folder plus the character serial
        in hex. Raises when the character is not in the world yet.
        """
        serial = safe(lambda: int(API.Player.Serial), 0)
        if not serial:
            raise Exception("the character isn't in the world yet")
        return os.path.join(Kit.data_path(BackupPage.DIR), "%08X" % serial)

    @staticmethod
    def names():
        """The backup names of this character, oldest first. A folder still being written (.saving) or
        without its info file does not count.
        """
        base = BackupPage.base()
        if not os.path.isdir(base):
            return []
        return sorted(n for n in os.listdir(base) if not n.endswith(".saving")
                      and os.path.isfile(os.path.join(base, n, "info.txt")))

    @staticmethod
    def info(name):
        """The info file of a backup read as a dict (saved time, version, why)."""
        text = Kit.read_safe(os.path.join(BackupPage.base(), name, "info.txt"), None) or ""
        return dict((k.strip(), v.strip()) for k, v in (ln.split("=", 1) for ln in text.splitlines() if "=" in ln))

    @staticmethod
    def label(name):
        """The text the drop-down shows for a backup: its date and time of day, taken from the folder name."""
        return "%s %s" % (name[:10], name[11:16].replace("-", ":"))

    def scan(self):
        """Read the backups from disk into items as (name, text) pairs, newest first, with the reason in
        brackets.
        """
        out = []
        for n in reversed(self.names()):
            why = self.info(n).get("why", "")
            out.append((n, self.label(n) + ("  (%s)" % why if why else "")))
        self.items = out

    @staticmethod
    def snapshot(prefs):
        """Collect the settings a backup holds, as a dict of key to text.

        Every Virtue Assistant setting of this character, the module settings keys included, except the
        session only ones and the backup's own bookkeeping. prefs is the host settings text, which is
        stored under SETTINGS_KEY because the host may not have saved it yet.
        """
        found = Profiles.char_vars()
        mods = set(s.key for s in HOST.slots)
        extra = tuple(set(k[:-8] for k in found if k.endswith("_settings") and k[:-9].lower() in mods))
        skip = set(Profiles.SESSION_VARS + BackupPage.SKIP + (PROFILE_STATE_KEY,))
        va = dict((k, v) for k, v in found.items() if k not in skip and k.startswith(Profiles.VA_KEYS + extra))
        va[SETTINGS_KEY] = prefs
        return va

    @staticmethod
    def _drop(path):
        """Delete a backup folder and the files in it."""
        for n in os.listdir(path):
            os.remove(os.path.join(path, n))
        os.rmdir(path)

    @staticmethod
    def read_vars(path):
        """Read the settings of a backup folder from its va_vars.txt."""
        return Profiles.parse_vars(Kit.read_safe(os.path.join(path, "va_vars.txt"), None) or "")

    @staticmethod
    def early():
        """Take the snapshot for the first start of a new version, before the host and the modules have
        changed anything, so the backup holds the settings as the older version left them. Returns
        (settings, bag layout text), or None when this version already made its backup or reading failed.
        """
        if Kit.get_var(BackupPage.VER_KEY) == APP_VERSION:
            return None
        bag = safe(Profiles.bag_path)
        return safe(lambda: (BackupPage.snapshot(Kit.get_var(SETTINGS_KEY)), Kit.read_safe(bag, None) if bag else None))

    def make(self, why, prefs, keep=None, early=None):
        """Write a backup and return (its name, how many settings it holds).

        why goes in the info file. prefs is the host settings text. keep is a backup that must survive the
        pruning, early is the pair from BackupPage.early (used instead of a fresh snapshot). The files are
        written into a .saving folder, read back and compared, and only then renamed into place, so a
        failed write leaves no half backup. Two backups in one second get a -NN suffix. Anything over KEEP
        is deleted, oldest first. Raises when the read-back differs. Script thread.
        """
        base = self.base()
        t = time.time()
        stem = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(t))
        if not os.path.isdir(base):
            os.makedirs(base)
        top = -1
        for n in os.listdir(base):
            if n.endswith(".saving"):
                safe(lambda: self._drop(os.path.join(base, n)))
                continue
            rest = n[len(stem):] if n.startswith(stem) else None
            if rest == "":
                top = max(top, 0)
            elif rest and rest[0] == "-" and rest[1:].isdigit():
                top = max(top, int(rest[1:]))
        name = stem if top < 0 else "%s-%02d" % (stem, top + 1)
        final = os.path.join(base, name)
        tmp = final + ".saving"
        os.makedirs(tmp)
        va = early[0] if early else self.snapshot(prefs)
        Profiles._write(os.path.join(tmp, "va_vars.txt"),
                        "".join("%s\t%s\n" % (Profiles._esc(k), Profiles._esc(va[k])) for k in sorted(va)))
        bag = Profiles.bag_path()
        text = early[1] if early else Kit.read_safe(bag, None) if bag else None
        if text is not None:
            Profiles._write(os.path.join(tmp, "unified_bag.cfg"), text)
        Profiles._write(os.path.join(tmp, "info.txt"), "saved=%d\nversion=%s\nwhy=%s\n" % (int(t), APP_VERSION, why))
        if self.read_vars(tmp) != va:
            safe(lambda: self._drop(tmp))
            raise Exception("the backup doesn't read back the same; try again")
        os.rename(tmp, final)
        names = self.names()
        extra = len(names) - self.KEEP
        for n in names:
            if extra <= 0:
                break
            if n != keep and n != name:
                safe(lambda: self._drop(os.path.join(base, n)))
                extra -= 1
        return name, len(va)

    def read(self, name):
        """Read a backup: returns (settings dict, bag layout text or None). Raises when the backup is gone."""
        path = os.path.join(self.base(), name)
        if not os.path.isfile(os.path.join(path, "info.txt")):
            raise Exception("that backup is gone")
        return self.read_vars(path), Kit.read_safe(os.path.join(path, "unified_bag.cfg"), None)

    @staticmethod
    def apply(va, lay, gone=()):
        """Put a backup back: write its settings, blank those in gone (settings this character has now that
        the backup does not hold), wait for them to land and restore the bag layout, keeping the lines
        that belong to this character only. Returns False when some writes were still pending. Script
        thread.
        """
        for k in sorted(va):
            Kit.put_var(k, va[k])
        for k in sorted(set(gone) - set(va)):
            Kit.put_var(k, "")
        ok = PROFILES.wait_vars(va)
        bag = Profiles.bag_path()
        own = Profiles.BAG_OWN
        cur = Kit.read_safe(bag) if lay is not None and bag else None
        if cur is not None:
            keep = [l for l in lay.splitlines() if l.strip() and not l.startswith(own)]
            Profiles._write(bag, "\n".join(keep + [l for l in cur.splitlines() if l.startswith(own)]))
        return ok


def _norm_key(k):
    """Normalise a key combination: upper case, modifiers in the order CTRL, SHIFT, ALT, then one key."""
    parts = [p for p in str(k or "").strip().upper().replace(" ", "").split("+") if p]
    keys = [p[5:] if p.startswith("SDLK_") else p for p in parts if p not in ("CTRL", "SHIFT", "ALT")]
    return "+".join([m for m in ("CTRL", "SHIFT", "ALT") if m in parts] + keys[-1:])


class Binds(object):
    """Lets the player bind a keyboard key to any button of a window.

    Every button built through the form kit is registered with an id (owner and key). In Settings the
    player arms binding, clicks a button and presses a key; later the key acts as a click on that
    button.
    Bindings are saved as id=combo pairs under VAR and the keys are registered with the host.
    """
    VAR = "VirtueAssistant_binds"
    REPEAT = 0.6
    ARM_SECS = 20.0
    REG_CAP = 5000
    armed_until = 0.0
    reg = {}
    saved = {}
    last = {}
    hooked = set()
    armed = False
    picked = None
    answer = None
    loaded = False
    scope = None
    OWNER = "Button binds"
    IDS_VAR = "VirtueAssistant_binds_ids"

    @staticmethod
    def scoped(name, fn, *args):
        """Run fn with Binds.scope set to name (the owner of buttons built meanwhile), then restore it."""
        was = Binds.scope
        Binds.scope = name
        try:
            return fn(*args)
        finally:
            Binds.scope = was

    @staticmethod
    def note(store, key, on_click, ctl, tip):
        """Register a button under an id made of its owner and key and return the id.

        The registry is cleared if it passes REG_CAP entries.
        """
        owner = Binds.scope or HOST.cur_owner
        if owner is None:
            cur = HOST.current()
            owner = cur.key if cur is not None else "va"
        bid = "%s|%s" % (owner, key)
        if len(Binds.reg) >= Binds.REG_CAP:
            Binds.reg.clear()
        Binds.reg[bid] = (store, key, on_click)
        return bid

    @staticmethod
    def wrap(bid, handler):
        """Wrap a button handler: while binding is armed (and not timed out) a click picks the button instead
        of acting.
        """
        def click(*args):
            """Click handler used in place of the real one."""
            if Binds.armed:
                Binds.armed = False
                if time.time() <= Binds.armed_until:
                    Binds.pick(bid)
                    return
            handler(*args)

        return click

    @staticmethod
    def load():
        """Load the saved bindings and hook their keys; once per session, after the player is known."""
        if Binds.loaded or not safe(lambda: API.Player):
            return
        Binds.loaded = True
        # Ids from before each window had its own owner name cannot be matched; they are dropped once and
        # the
        # player is told.
        fresh = str(Kit.get_var(Binds.IDS_VAR, "") or "") != "2"
        dropped = 0
        for part in str(Kit.get_var(Binds.VAR, "") or "").split(";"):
            if "=" in part:
                bid, combo = part.rsplit("=", 1)
                if fresh and bid.split("|", 1)[0] in ("va", "interface"):
                    dropped += 1
                    continue
                combo = _norm_key(combo)
                if bid and combo:
                    Binds.saved[bid] = combo
                    Binds.hook(combo)
        if fresh:
            Kit.put_var(Binds.IDS_VAR, "2")
            if dropped:
                Binds.save()
                Kit.say("%s cleared (each window has its own now); bind them again in Settings > Hotkeys."
                        % Kit.count(dropped, "button key"), Kit.HUE_INFO)

    @staticmethod
    def save():
        """Save every binding to VAR as id=combo pairs."""
        Kit.put_var(Binds.VAR, ";".join("%s=%s" % kv for kv in sorted(Binds.saved.items())))

    @staticmethod
    def hook(combo):
        """Register the combo with the host hotkey table; remember it only if the host took it."""
        if HOST.hotkey_on(combo, Binds.OWNER, lambda: Binds.fire(combo), "a button") is not False:
            Binds.hooked.add(combo)

    @staticmethod
    def unhook(combo):
        """Release the combo from the host."""
        Binds.hooked.discard(combo)
        HOST.hotkey_off(combo, Binds.OWNER)

    @staticmethod
    def fire(combo):
        """Hotkey handler: act as a click on the button bound to combo.

        A repeat within REPEAT seconds is ignored (key auto-repeat). The click flag is set in the button's
        store, the main loop is woken and the button's own click callback runs.
        """
        now = time.time()
        was = Binds.last.get(combo)
        Binds.last[combo] = now
        if was is not None and 0 <= now - was < Binds.REPEAT:
            return
        for bid, c in Binds.saved.items():
            if c == combo:
                r = Binds.reg.get(bid)
                if r is None:
                    return
                store, key, on_click = r
                store[1][key] = True
                HOST.poke()
                if on_click is not None:
                    on_click()
                return

    @staticmethod
    def arm(on=True):
        """Arm or disarm binding mode; arming lasts ARM_SECS seconds and tells the player what to do."""
        Binds.armed = bool(on)
        if on:
            Binds.armed_until = time.time() + Binds.ARM_SECS
            Kit.say("click a button to bind within %d s (Esc on the key window cancels)."
                       % int(Binds.ARM_SECS), Kit.HUE_INFO)

    @staticmethod
    def pick(bid):
        """Start asking for a key for button bid, on a background thread so the client keeps running."""
        Binds.armed = False
        Binds.picked = bid
        Binds.answer = None
        import System

        def ask():
            """Thread body: ask the client for a key press (30 s) and store the answer, empty on failure or Esc."""
            try:
                Binds.answer = str(API.RequestHotkey("Press the key for this button", 30) or "")
            except Exception:
                Binds.answer = ""

        t = System.Threading.Thread(System.Threading.ThreadStart(ask))
        t.IsBackground = True
        t.Start()

    @staticmethod
    def tick():
        """Finish a binding when the key answer has arrived; client tick.

        Refuses a key already used by another owner, replaces the old key of the button, saves and
        refreshes
        the Keys page.
        """
        if Binds.answer is None:
            return
        combo, Binds.answer = _norm_key(Binds.answer), None
        bid, Binds.picked = Binds.picked, None
        if bid is None or not combo:
            return
        taken = next((row[1] for row in KeysPage.rows()
                      if row[0] == combo and not (row[1] == Binds.OWNER and Binds.saved.get(bid) == combo)), None)
        if taken is not None:
            Kit.say("%s is already %s's key; pick another." % (combo, taken), Kit.HUE_BAD)
            return
        old = Binds.saved.get(bid)
        if old and old != combo:
            Binds.unhook(old)
        Binds.saved[bid] = combo
        Binds.hook(combo)
        Binds.save()
        Kit.say("%s bound." % combo, Kit.HUE_GOOD)
        HOST.refresh_settings(KEYS_PAGE)

    @staticmethod
    def clear():
        """Remove every binding and save the empty list."""
        for combo in set(Binds.saved.values()) | Binds.hooked:
            Binds.unhook(combo)
        Binds.saved.clear()
        Binds.save()


class KeysPage(_Page):
    """Settings page that lists every registered hotkey, owner and purpose, and marks keys used twice."""
    ROW = 24

    @staticmethod
    def rows():
        """Collect every known hotkey as (combo, owner, what, clash), sorted by key.

        Sources are the host hotkey list, keys owned without a description and each module's hotkeys
        service. clash is True when the same combo appears more than once.
        """
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
        """Height of the page: header space plus one row per hotkey."""
        return 64 + self.ROW * max(1, len(self.rows()))

    def build(self, g, x, y, w):
        """Build the hotkey list into gump g at x, y, w.

        Draws the section, the Refresh, Clear binds and Bind a button buttons, a line counting keys bound
        twice and one row per hotkey; a clashing key is shown in red.
        """
        self.store = ({}, {})
        rows = self.rows()
        h = 64 + self.ROW * max(1, len(rows))
        Kit.add_section(g, x, y, w, h, "HOTKEYS  (every key Virtue Assistant listens to)")
        rx = x + w + 4
        for key, art, cap, dy, tip in (("refresh", Kit.ART_PAGE, "Refresh", 4, "Read the hotkeys again"),
                ("bind_clear", Kit.ART_CLOSE, "Clear binds", 28, "Unbind every button"),
                ("bind", Kit.ART_PLAY, "Bind a button", 28, "Click this, then a button in any window, then a key")):
            rx -= 16 + 35 + Kit.text_w(cap)
            Kit.art_button(g, self.store, key, art, rx, y + dy, cap, tip)
        clashes = len(set(r[0] for r in rows if r[3]))
        Kit.add_label(g, ("%s bound twice (shown in red)" % Kit.count(clashes, "key"))
                      if clashes else "No key is bound twice.", x + 12, y + 32,
                      Kit.HUE_BAD if clashes else Kit.HUE_INFO)
        if not rows:
            Kit.add_label(g, "No module that is on has a hotkey.", x + 12, y + 56, Kit.HUE_INFO)
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
        """Handle the page buttons: refresh the list, arm button binding or clear every binding."""
        if self.c is not None and Kit.was_clicked(self.store, "refresh"):
            HOST.refresh_settings(KEYS_PAGE)
        if self.c is not None and Kit.was_clicked(self.store, "bind"):
            Binds.arm(True)
        if self.c is not None and Kit.was_clicked(self.store, "bind_clear"):
            Binds.clear()
            HOST.refresh_settings(KEYS_PAGE)


ALERTS_PAGE, KEYS_PAGE, BACKUP_PAGE = "va.alerts", "va.keys", "va.backups"


class WhatsNew(object):
    """The what's-new window: shown once per version, from the text of the patch notes. It also keeps
    which new settings of this version the player has already looked at, so the settings pages can
    mark the ones that are still new.
    """
    W = 520
    SEEN_KEY = "VirtueAssistant_new_seen"
    seen_keys = None
    # The settings added in this version, by key; the settings pages mark them until they have been seen.
    NEW_KEYS = ("prices.pick_book", "prices.book_open", "prices.book_head", "prices.keep_SS", "prices.keep_NS",
                "prices.keep_BP", "prices.keep_GA", "prices.keep_SA", "prices.keep_BM", "prices.keep_GI",
                "prices.keep_MR", "prices.say", "prices.skip_old", "prices.dist", "prices.old", "prices.hk")

    def __init__(self):
        """Start closed with no text loaded."""
        self.g = None
        self.store = ({}, {})
        self.text = None

    @staticmethod
    def seen():
        """The set of new setting keys already seen this version, read from SEEN_KEY on first use (a list
        saved by another version counts as empty).
        """
        if WhatsNew.seen_keys is None:
            ver, _, keys = Kit.get_var(WhatsNew.SEEN_KEY, "").partition(":")
            WhatsNew.seen_keys = set(k for k in keys.split(",") if k) if ver == APP_VERSION else set()
        return WhatsNew.seen_keys

    @staticmethod
    def unseen(page=None):
        """The new setting keys not seen yet; with page, only those under that page key."""
        seen = WhatsNew.seen()
        pre = None if page is None else page + "."
        return set(k for k in WhatsNew.NEW_KEYS if k not in seen and (pre is None or k.startswith(pre)))

    @staticmethod
    def see(keys):
        """Record these keys as seen and save the list with the version."""
        seen = WhatsNew.seen()
        new = set(keys) - seen
        if new:
            seen.update(new)
            Kit.put_var(WhatsNew.SEEN_KEY, "%s:%s" % (APP_VERSION, ",".join(sorted(seen))))

    def due(self):
        """True when there is a what's-new text and this account has not yet seen it for this version."""
        if self.text is None:
            self.text = whats_new()
        if not self.text:
            return False
        try:
            seen = API.GetPersistentVar(WHATS_NEW_KEY, "", API.PersistentVar.Account)
        except Exception:
            return False
        return str(seen or "") != APP_VERSION

    def open(self):
        """Open the window on the client tick when it is due."""
        if self.due():
            Kit.on_client(lambda: Binds.scoped("va.news", self._build))

    def show(self):
        """Open the window now, whether or not it is due, when there is text. Returns False when there is
        nothing to show.
        """
        if self.text is None:
            self.text = whats_new()
        if not self.text:
            return False
        if not Kit.is_open(self.g):
            Kit.on_client(lambda: Binds.scoped("va.news", self._build))
        return True

    def _build(self):
        """Build and show the window: title bar, close button and the wrapped text, centred in the upper part
        of the screen and added in front of the other windows.
        """
        M, W = Kit.MARGIN, self.W
        lines = []
        for para in self.text:
            lines += Kit.wrap(para, W - 2 * M - 24) or [""]
        h_body = 16 + 20 * len(lines)
        H = M + 30 + Kit.GAP + h_body + M
        self.store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, "WHAT'S NEW IN %s %s" % (APP_NAME.upper(), APP_VERSION), M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close (shown once per version)")
        yb = M + 30 + Kit.GAP
        Kit.add_section(g, M, yb, W - 2 * M, h_body)
        for i, line in enumerate(lines):
            Kit.add_label(g, line, M + 12, yb + 8 + 20 * i, Kit.HUE_TEXT)
        sw, sh = Kit.screen()
        Kit.place(g, max(0, ((sw or 1024) - W) // 2), max(0, ((sh or 768) - H) // 3), W, H)
        Kit.add_front(g)
        self.g = g

    def poll(self):
        """Close the window when the player closes it or clicks the close button; client tick."""
        g = self.g
        if g is None:
            return
        if not Kit.is_open(g) or Kit.was_clicked(self.store, "close"):
            self.close(True)

    def close(self, seen=False):
        """Close the window; when seen is True, save the current version as seen on the account."""
        g, self.g = self.g, None
        Kit.dispose(g)
        if seen:
            API.SavePersistentVar(WHATS_NEW_KEY, APP_VERSION, API.PersistentVar.Account)


class ModuleSlot(object):
    """One entry of the host's module table: a module's description, state and counters.

    The module's own api (its hooks) is put in api once its file is loaded. Fields cover the on/off
    state, the run state, timing (next_due, and the busy records load and part_load), the errors seen,
    the category and the parts (optional sub-features) the player may switch on one by one.
    """
    def __init__(self, key, title, desc, factory, interval):
        """Create a slot for module key with its title, description, factory and default interval, off and
        not loaded.

        load is the module's busy record and part_load maps each of its running parts to theirs: both are
        lists [decayed ms sum, last time, slowest tick] kept by Host.busy_add. shipped marks a module that
        is one of the published files, and folded is whether its parts list is folded in the settings.
        """
        self.key = key
        self.title = title
        self.desc = desc
        self.factory = factory
        self.interval = interval
        self.api = self.lazy = self.broken = self.iv_fn = self.thread_want = None
        self.enabled = self.default_on = self.running = self.busy = self.pending_stop = False
        self.thread_due = self.on_client = self.has_thread = False
        self.category = "Other"
        self.next_due = 0.0
        self.errors = set()
        self.error_times = {}
        self.load = [0.0, 0.0, 0.0]
        self.part_load = {}
        self.start_tok = None
        self.page_err_at = 0.0
        self.shipped = False
        self.parts = self.aliases = ()
        self.parts_on = {}
        self.parts_running = set()
        self.folded = True

    def part(self, key):
        """Return the part tuple with this key, or None."""
        for p in self.parts:
            if p[0] == key:
                return p
        return None

    def parts_wanted(self):
        """Return the keys of the parts the player has switched on."""
        return [p[0] for p in self.parts if self.parts_on.get(p[0])]

    def part_title(self, key):
        """Return the display title of a part as module title > part title; the module title when it is
        unknown.
        """
        p = self.part(key)
        return "%s > %s" % (self.title, p[1]) if p is not None else self.title


class PartView(object):
    """A part of a module seen as if it were a module of its own (key, title, state), for the host's
    tables.
    """
    def __init__(self, key, slot, part):
        """Remember the slot and part, and copy the title and category from them."""
        self.key = key
        self.slot = slot
        self.part = part
        self.title = slot.part_title(part)
        self.category = slot.category

    @property
    def running(self):
        """True while the module runs and this part is among its running parts."""
        return bool(self.slot.running and self.part in self.slot.parts_running)

    @property
    def enabled(self):
        """True when the module is on and this part is switched on."""
        return bool(self.slot.enabled and self.slot.parts_on.get(self.part))

    @property
    def api(self):
        """The module's api hooks."""
        return self.slot.api

    @property
    def lazy(self):
        """The module's lazy loader state."""
        return self.slot.lazy

    @property
    def broken(self):
        """The module's broken flag."""
        return self.slot.broken


class _KeyMap(dict):
    """Dictionary of slots by key that also answers for part keys, built on demand as PartView objects."""
    def __init__(self, host):
        """Keep the host to ask for part keys."""
        dict.__init__(self)
        self.host = host

    def view(self, key):
        """Return a PartView for a part key, or None when the key names no part."""
        slot, part = self.host.resolve(key)
        return PartView(key, slot, part) if part is not None else None

    def __contains__(self, key):
        """True for a slot key or for a part key."""
        return dict.__contains__(self, key) or self.view(key) is not None

    def get(self, key, default=None):
        """Return the slot (or the part view) for key, else default."""
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        v = self.view(key)
        return v if v is not None else default

    def __getitem__(self, key):
        """Return the slot (or the part view) for key; raise KeyError when there is none."""
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        v = self.view(key)
        if v is None:
            raise KeyError(key)
        return v


def _error_where():
    """Return the file and line of the innermost frame of the exception being handled, as text for an
    error message.

    Module files give the file name and line; other code gives only the line; empty when unknown.
    """
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
    """One journal line, with its text, lower-case text, speaker name, hue, client time ticks, time seen,
    text type and the client message number (num, 0 until Journal.pair finds one).
    """
    __slots__ = ("seq", "text", "low", "name", "hue", "ticks", "at", "kind", "num")

    def __init__(self, seq, text, name, hue, ticks, at, kind):
        """Store the fields and the lower-case copy of the text used for matching."""
        self.seq, self.text, self.low, self.name = seq, text, text.lower(), name
        self.hue, self.ticks, self.at, self.kind, self.num = hue, ticks, at, kind, 0


class Journal(object):
    """Shared reader of the client journal: read once per pass, then every module reads from the same
    copy.

    New entries are given a sequence number. Each module holds a Reader that remembers the last number
    it saw, so no module misses a line and none sees one twice. Lines are kept for KEEP seconds.
    The client's message event (OnClilocMessageReceived) is hooked once; its records in clis (at most
    CLI_CAP, kept CLI_AGE seconds) give journal lines their message number.
    """
    KEEP = 60.0
    MAX_BACK = 30.0
    lines = []
    seen = {}
    seq = 0
    read_at = 0.0
    pass_id = -1
    zero_seen = False
    clis = []
    CLI_CAP = 64
    CLI_AGE = 5.0
    hook = {"on": False}
    ATTACK_RE = re.compile(r"\*?\s*(.+?)\s+is attacking you", re.IGNORECASE)

    class Reader(object):
        """A cursor over the journal: gives each caller the lines added since its last call."""
        __slots__ = ("last",)

        def __init__(self):
            """Start at the newest line, so only later lines are returned."""
            self.last = Journal.seq

        def new(self, read=True):
            """Return the lines added since the last call, oldest first.

            read=False skips the journal update (used when the caller has just updated it).
            """
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
        """Update the journal and return a new Reader starting after the newest line."""
        Journal.update()
        return Journal.Reader()

    @staticmethod
    def update(force=False):
        """Read the client journal and append the lines not seen before; at most once per host pass unless
        force.

        Entries are matched by (time ticks, text, name). Entries with no time stamp (ticks 0) cannot be
        matched that way, so they are counted and only the surplus over what is already kept is added.
        Lines older than KEEP seconds are dropped with their match keys. Client tick. The first read (and
        the first after the hook's owner stops) hooks the message event and drops any stale records.
        """
        pid = HOST.pass_id
        if pid == Journal.pass_id and not force:
            return
        Journal.pass_id = pid
        now = time.time()
        if not Journal.hook["on"]:
            del Journal.clis[:]
            Kit.hook_once(Journal.hook, "on", ("OnClilocMessageReceived", Journal.on_cliloc))
        # Look back as far as the last read (plus a second), never more than MAX_BACK seconds.
        back = min(Journal.MAX_BACK, max(1.0, now - Journal.read_at + 1.0)) if Journal.read_at else Journal.MAX_BACK
        Journal.read_at = now
        try:
            entries = list(API.GetJournalEntries(back) or [])
        except Exception:
            entries = []
        seen, fresh, zero, stopped, i = Journal.seen, [], [], False, len(entries) - 1
        while i >= 0:
            e = entries[i]
            i -= 1
            pos = i
            try:
                text = str(e.Text or "")
                if not text:
                    continue
                try:
                    ticks = int(e.Time.Ticks)
                except Exception:
                    ticks = 0
                key = (ticks, text, str(e.Name or ""))
                if ticks == 0:
                    zero.append((key, e, pos))
                    Journal.zero_seen = True
                    continue
                # Newest first: stop at the first known entry, but keep reading while stamp-less entries are still
                # being found.
                if stopped or key in seen:
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
            kept = {}
            ws = now - back
            for ln in reversed(Journal.lines):
                if ln.at < ws:
                    break
                if ln.ticks == 0:
                    k = (0, ln.text, ln.name)
                    kept[k] = kept.get(k, 0) + 1
            rank = {}
            for key, e, pos in zero:
                r = rank.get(key, 0)
                rank[key] = r + 1
                if r < total[key] - kept.get(key, 0):
                    fresh.append((key, e, pos))
            fresh.sort(key=lambda t: t[2])
        else:
            fresh.reverse()
        added = {}
        for key, e, pos in fresh:
            if key[0] != 0:
                if key in added:
                    continue
                added[key] = 1
            try:
                Journal.seq += 1
                seen[key] = Journal.seq
                Journal.lines.append(JLine(Journal.seq, key[1], key[2], int(e.Hue or 0), key[0], now,
                                           str(e.TextType or "")))
            except Exception:
                continue
        # Give the new lines their message numbers before any reader sees them.
        if Journal.clis:
            Journal.pair(now)
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
    def on_cliloc(e):
        """Script event: a client message by number arrived. Only stores (number, text, time) in clis, capped
        at CLI_CAP; the journal read pairs it with its line.
        """
        try:
            Journal.clis.append((int(e.Cliloc), str(e.Text or ""), time.time()))
        except Exception:
            return
        if len(Journal.clis) > Journal.CLI_CAP:
            del Journal.clis[:-Journal.CLI_CAP]

    @staticmethod
    def pair(now):
        """Give each stored message record's number to the newest numberless journal line with the same text
        from the last CLI_AGE seconds.

        A record whose line has not been read yet waits (the event can come before the line); one older
        than CLI_AGE is dropped. A line takes at most one number, so it can never match twice.
        """
        recs, Journal.clis = Journal.clis, []
        keep = []
        for rec in recs:
            num, text, t = rec
            hit = False
            for ln in reversed(Journal.lines):
                if ln.at < t - Journal.CLI_AGE:
                    break
                if not ln.num and ln.text == text:
                    ln.num = num
                    hit = True
                    break
            if not hit and now - t < Journal.CLI_AGE:
                keep.append(rec)
        if keep:
            Journal.clis[:0] = keep[-Journal.CLI_CAP:]

    @staticmethod
    def said(ln, nums):
        """The text to match a journal line by: when its message number is in nums and the line's own words
        lack that text (another language, the client's wording changed), the mapped English text;
        otherwise the line's lower-case text, so English lines match exactly as before.
        """
        t = nums.get(ln.num) if ln.num else None
        return ln.low if t is None or t in ln.low else t

    @staticmethod
    def since(t):
        """Return the journal lines added at or after time t, oldest first."""
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
        """Return the journal lines of the last secs seconds."""
        return Journal.since(time.time() - secs)

    @staticmethod
    def find(t, texts):
        """Return the newest line since time t that contains any of texts (case ignored), or None."""
        if isinstance(texts, str):
            texts = (texts,)
        low = [x.lower() for x in texts]
        for ln in Journal.since(t):
            for x in low:
                if x in ln.low:
                    return ln
        return None


class Picker(object):
    """Asks the player for a target on the client tick, so a module never blocks its thread on a cursor.

    Each request is a job with a timeout and a callback that gets the serial (0 when cancelled, timed
    out or lost). A new request cancels the older ones. Where the client's target manager cannot be
    reached, the job is run later in blocking mode by run_blocking.
    """
    jobs = []
    cuo = None
    neutral = None
    looked = False
    CURSOR_TARGET = 6983686

    @staticmethod
    def _tm():
        """Find the client's target manager once and return it, or None."""
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
        try:
            return Picker.cuo.Game.UO.World.TargetManager
        except Exception:
            return None

    @staticmethod
    def ask(timeout, fn, owner=None):
        """Ask for a target: fn(serial) is called after the player picks, cancels or time runs out (timeout
        seconds).

        owner tells whose request it is (default: the module running now) so a stopping module can drop
        it.
        """
        for j in Picker.jobs:
            j["cancel"] = True
        if owner is None:
            owner = HOST.owner_key()
        Picker.jobs.append({"t": float(timeout), "fn": fn, "until": 0.0, "d": None,
                            "got": None, "block": False, "cancel": False, "owner": owner})
        HOST.poke()

    @staticmethod
    def due():
        """True when a job still needs the tick (not yet started, or an answer is waiting)."""
        for j in Picker.jobs:
            if j["d"] is None or j["got"] is not None:
                return True
        return False

    @staticmethod
    def _done(j, serial):
        """Finish job j: take it off the list and call its callback with the serial; an error is shown in the
        system line.
        """
        if j in Picker.jobs:
            Picker.jobs.remove(j)
        try:
            j["fn"](int(serial or 0))
        except Exception as ex:
            Kit.say("target error: %s%s" % (ex, _error_where()), Kit.HUE_BAD)

    @staticmethod
    def tick():
        """Advance every job: start targeting, collect an answer, or cancel on timeout or when replaced;
        client tick.
        """
        if not Picker.jobs:
            return
        tm = Picker._tm()
        for j in list(Picker.jobs):
            if j["block"]:
                continue
            if j["d"] is None:
                if j["cancel"]:
                    Picker._done(j, 0)
                    continue
                if tm is None:
                    j["block"] = True
                    continue
                try:
                    from System import Action

                    def got(obj, j=j):
                        """Client callback with the chosen object; stores its serial (0 for none) in the job."""
                        try:
                            j["got"] = (int(obj.Serial or 0) if obj is not None else 0)
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
                Picker._done(j, 0)
            elif j["cancel"] or time.time() >= j["until"]:
                try:
                    tm.CancelTarget()
                except Exception:
                    pass
                Picker._done(j, 0)

    @staticmethod
    def drop(owner=None):
        """Drop the jobs of owner (every job when owner is None), cancel the cursor if it is theirs, call
        their callbacks with 0.
        """
        mine = [j for j in Picker.jobs if owner is None or j.get("owner") == owner]
        if not mine:
            return
        for j in mine:
            Picker.jobs.remove(j)
        tm = Picker._tm()
        up = [j["d"] for j in mine if j["d"] is not None and j["got"] is None]
        if tm is not None and up:
            def take_down():
                """Cancel the targeting cursor of each dropped job, on the client tick."""
                for d in up:
                    if tm.IsCurrentTargetingAction(d):
                        tm.CancelTarget()

            safe(lambda: Kit.on_client(take_down, fallback=False))
        for j in mine:
            Picker._done(j, 0)

    @staticmethod
    def run_blocking():
        """Run the jobs that could not use the target manager with the API's own blocking request; script
        thread.
        """
        for j in [j for j in Picker.jobs if j["block"]]:
            Picker.jobs.remove(j)
            serial = 0 if j["cancel"] else int(safe(lambda: API.RequestTarget(j["t"]), 0) or 0)
            Picker._done(j, serial)


def _first(e):
    """Return the first element of e (sort key)."""
    return e[0]


class _Memo(object):
    """Wrapper that caches attribute reads of a client object, for the mobile and item objects of one
    pass.

    Every attribute is read from the raw object once and kept; writing an attribute writes through and
    forgets the cached value. int() gives the serial.
    """
    def __init__(self, raw):
        """Hold the raw object."""
        self.__dict__["raw"] = raw

    def __getattr__(self, name):
        """Read the attribute from the raw object and keep it."""
        v = getattr(self.__dict__["raw"], name)
        self.__dict__[name] = v
        return v

    def __setattr__(self, name, value):
        """Write through to the raw object and forget the cached copy."""
        setattr(self.__dict__["raw"], name, value)
        self.__dict__.pop(name, None)

    def __int__(self):
        """Return the serial of the raw object."""
        return int(self.__dict__["raw"].Serial)


class Host(object):
    """The host: owns the module table, the main loop, the shared services and the saved settings.

    Modules are loaded into slots and driven from here. The client tick runs the pass that gives each
    running module its turn; script threads run modules that need them. The host also keeps the caches
    shared by every module (the player, mobiles, backpack), hotkeys, docks and layout, fight and
    cursor guards, services and saved preferences, the start-up timing list and the split timers, the
    settling of start-up (when the windows have stopped changing), the start mark and the safe-start
    window, and the check that warns about TazUO settings the shard rules forbid. It also applies the
    look settings, runs the backups and the alert history window, and sits in front of the profile and
    backup requests. At start it caches the mother script and the module files' compiled code and
    compiles module files ahead while the client builds windows. Modules reach it as HOST.
    """
    def __init__(self):
        """Create the empty tables, caches and flags, and the built-in Alerts, Hotkeys and Backups settings
        pages.

        boot starts the start-up timing list with the time spent before the host existed. split holds the
        split timers of start-up (None once start-up is over). compile_hit says the last compiled call
        used the cache; texts holds module file text read ahead of its load and ahead_ms the compile time
        spent ahead per file; ahead_off stops the compile-ahead. held_on and held_parts name the modules
        and parts that are switched off for this session only but stay saved as on. marked says this run
        set the start mark; ask_g and ask_store belong to the safe-start window. settled_at is when
        start-up settled (None while booting); settle_seen, settle_from, settle_capped, settle_holds and
        builds are the settling bookkeeping, and bar_dead says the Action Bar failed to start. tz_at is
        when the TazUO settings check runs next, tz_off holds its key when a client name it reads is
        missing, and tz_told the settings already warned about this session. early_backup holds the
        snapshot taken before anything loads, for the backup of a new version.
        """
        self.slots = []
        self.by_key = _KeyMap(self)
        self.old_map = {}
        # boot is a list of (phase, seconds). The first phase is everything the mother script did before the
        # host was made, measured from START_AT, the mother's first lines. It is set to None once the
        # start-up line has been dealt with, which stops further timing.
        self.boot = [("code", time.time() - START_AT)]
        # boot_at is the time the last phase ended.
        self.boot_at = time.time()
        # boot_load adds up the module compile times, which are taken out of the final first build phase so
        # they are not counted twice.
        self.boot_load = 0.0
        self.cur_part = self.cur_owner = self.config = self.hub = self.grid = self.profile_req = self.alone = None
        self.hurt_hp = self._me = self._want_raw = self.attack_rd = None
        self.stack = []
        self.harm_conf = (None, 0, 0.0)
        self.quitting = self.shut = self.ui_busy = self.poked = self.prefs_frozen = False
        self.in_hop = self.pass_poked = self.pass_all = self.poke_user = self.draining = False
        self.alive_at = 0.0
        self.poke_keys = set()
        self.pass_keys = self.NO_KEYS
        self.off_q = []
        self._stop_fi = None
        self.look = self.LOOKAHEAD
        import _thread
        self._drain_lk = _thread.allocate_lock()
        self.ui_next = self.dock_next = self._claim_len = self.hurt_until = self.input_at = 0.0
        self.attacked_until = self.prefs_at = self.pressed_at = 0.0
        self.hurt_who = 0
        self.prefs_due = False
        self.docks = []
        self.services = {}
        self.hotkeys_owned = {}
        self.prefs = {}
        self.cursor_claim = (None, 0.0)
        self.hk_fns = {}
        self.hk_wait = {}
        self.gump_exp = {}
        self.services["gump.expect"] = self.gump_expect
        self.foe_seen = (0.0, None)
        self.client_idles = self.pass_id = 0
        self._me_pid = self._mob_pid = self._one_pid = -1
        self._mob_list = ()
        self._one = {}
        self._pack = {}
        self._mob_at = 0.0
        self._pack_v = 0
        self._pack_keys = set()
        self._pack_hook = {"on": False}
        self._pack_fn = self._pack_event
        self.active = []
        self.client_run = []
        self._pass_fn = self._client_pass
        self._want_set = frozenset()
        self.told, self._zone_held, self._zone_was_d, self._zone_bring = set(), set(), None, {}
        self.load_jobs = []
        self.hotkey_list = []
        self.pages = []
        self.held_on = set()
        self.held_parts = set()
        self.marked = False
        self.ask_g = None
        self.ask_store = ({}, {})
        self.settled_at = self.boot_line = None
        self.settle_seen = 0.0
        self.settle_capped = False
        self.builds = {}
        self.settle_from = None
        self.settle_holds = []
        self.split = {}
        self.compile_hit = False
        self.bar_dead = self.ahead_off = False
        self.texts = {}
        self.ahead_ms = {}
        self.tz_at = 0.0
        self.tz_off = set()
        self.tz_told = set()
        self.backups = BackupPage()
        self.alert_log = AlertLog()
        self.launcher = None
        self.early_backup = None
        for key, title, page in ((ALERTS_PAGE, "Alerts", AlertsPage()), (KEYS_PAGE, "Hotkeys", KeysPage()),
                                 (BACKUP_PAGE, "Backups", self.backups)):
            s = ModuleSlot(key, title, "", None, 1.0)
            s.api = page.api()
            self.pages.append(s)
        self.whats_new = WhatsNew()
        self.services["alerts.history"] = self.alert_log.open
        self.services["alerts.quiet"] = ALERTS.toggle_quiet

    def _tell(self, msg):
        """Show a message in the system line once (the same message is not repeated until the list resets)."""
        if msg in self.told:
            return
        if len(self.told) > 50:
            self.told.clear()
        self.told.add(msg)
        API.SysMsg(msg, Kit.HUE_BAD)

    def _refresh_active(self):
        """Rebuild the lists of running modules and of those that run on the client tick."""
        act = [s for s in self.slots if s.running]
        self.active = act
        self.client_run = [s for s in act if s.on_client]

    NO_KEYS = frozenset()

    def poke(self, key=None, user=True):
        """Ask for another pass of the main loop soon.

        key limits the pass to one module (and its family); None means all. user is True when it comes
        from the player's own input, which also speeds the settings window up. While a drain is running
        the
        request is held for the pass after it.
        """
        if self.draining:
            if key is None:
                self.pass_all = self.pass_poked = True
            else:
                self.pass_keys = self.pass_keys | frozenset((key, key.partition(".")[0]))
            if user:
                self.pass_poked = True
                self.input_at = time.time()
            if user or key is None:
                self.ui_next = 0.0
            return
        if key is None:
            self.poked = True
        else:
            ks = self.poke_keys
            ks.add(key)
            ks.add(key.partition(".")[0])
        if user:
            self.poke_user = True
            self.input_at = time.time()

    def click_key(self):
        """Return the key of the module being run now, or None."""
        cur = self.current()
        return cur.key if cur is not None else None

    INPUT_FAST = 1.0
    PAGE_EVERY = 0.25

    def poll_due(self, gate, every=None):
        """Say whether a window poll is due now.

        gate is the caller's own time gate; every is its wanted period. A poll is due when there are no
        mouse click records yet, when the player is giving input (fast mode) or when the mouse is pressed.
        Used so idle windows cost almost nothing.
        """
        now = time.time()
        if every is not None and every <= UI_TICK:
            return True
        if not Kit.clicks_seen:
            return True
        # Fast mode: the player gave input in the last second, or the caller's own gate is far in the
        # future.
        fast = now - self.input_at <= self.INPUT_FAST or 0 <= gate[0] - now > 2.0
        if not fast:
            # Otherwise look at the mouse button and the chat typing state, so a click or typing is answered at
            # once.
            p = SNAP.pressed()
            if p is not False:
                if p:
                    self.input_at = now
                fast = True
            else:
                fast = Client.typing()
        if fast or now >= gate[0]:
            gate[0] = now + (every if every is not None else self.PAGE_EVERY)
            return True
        return False

    def alert_kind(self, key, label, default_sound=None):
        """Register an alert kind for the module running now (its title is the owner); returns the key."""
        s = self.current()
        return ALERTS.kind(key, label, default_sound, s.title if s is not None else APP_NAME)

    def alert(self, key, text, level="warn", sound=None, ping=None, who=None, name=None, serial=None):
        """Raise an alert for the module running now; see Alerts.raise_ for the arguments. name and serial
        tell streamer mode whose name is in the text. Wakes the fade service for that module. Returns True
        when it was raised.
        """
        s = self.current()
        if FADE.on and s is not None:
            FADE.wake(s.key)
        return ALERTS.raise_(key, text, level, sound, ping, who, s.title if s is not None else APP_NAME, name, serial)

    def guarded(self):
        """True or False when the guard state is known, None when not."""
        return GUARD.guarded()

    def guard_area(self):
        """Name of the guard area the player stands in, or None."""
        return GUARD.area()

    def hotkey_note(self, combo, owner, what=""):
        """Record that owner uses combo (shown on the Keys page) without registering a handler.

        what says what the key does. An older entry of the same key and owner is replaced.
        """
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list if not (_norm_key(e[0]) == k and e[1] == owner)]
        self.hotkey_list.append((k, str(owner), str(what or "")))
        if k not in self.hotkeys_owned:
            self.hotkeys_owned[k] = str(owner)

    def hotkey_on(self, combo, owner, fn, what=""):
        """Register a handler fn for the key combo on behalf of owner.

        Returns True when taken, False when the combo is empty or the client refused it, and None when
        another owner already holds it (this one is queued and gets the key when the holder lets go).
        """
        k, owner = _norm_key(combo), str(owner)
        if not k:
            return False
        cur = self.current()
        ent = (owner, fn, cur.key if cur is not None else None, str(what or ""))
        held = self.hk_fns.get(k)
        if held is not None and held[0] != owner:
            wait = [w for w in self.hk_wait.get(k, ()) if w[0] != owner]
            wait.append(ent)
            self.hk_wait[k] = wait
            Kit.say("%s is already %s's key; %s can't use it until that lets it go." % (k, held[0], owner), Kit.HUE_BAD)
            return None
        if held is None:
            try:
                API.OnHotKey(k, self._hk_fire(k))
            except Exception:
                return False
        self._hk_take(k, ent)
        return True

    def _hk_take(self, k, ent):
        """Make ent the holder of key k and record it for the Keys page."""
        self.hk_fns[k] = ent
        self.hotkey_note(k, ent[0], ent[3])
        self.hotkeys_owned[k] = ent[0]

    def _hk_fire(self, k):
        """Return the callback given to the client for key k: it runs whichever handler holds the key at that
        moment.
        """
        def fired(*args):
            """Client callback for the key: run the current holder's handler, if any."""
            self.pressed_at = time.time()
            ent = self.hk_fns.get(k)
            if ent is not None:
                ent[1]()

        return fired

    def hotkey_off(self, combo, owner):
        """Release the combo for owner: leave the queue, and hand the key to the next waiting owner or
        unregister it.
        """
        k, owner = _norm_key(combo), str(owner)
        held = self.hk_fns.get(k)
        wait = [w for w in self.hk_wait.get(k, ()) if w[0] != owner]
        if wait:
            self.hk_wait[k] = wait
        else:
            self.hk_wait.pop(k, None)
        self.hotkey_drop(k, owner)
        if held is None or held[0] != owner:
            return
        if wait:
            nxt = wait.pop(0)
            if not wait:
                self.hk_wait.pop(k, None)
            self._hk_take(k, nxt)
            Kit.say("%s is %s's key now." % (k, nxt[0]), Kit.HUE_INFO)
            return
        self.hk_fns.pop(k, None)
        with Kit.quiet:
            API.OnHotKey(k)

    def hotkey_drop(self, combo, owner=None):
        """Remove a key from the Keys page list (only owner's entry when owner is given) and fix who is shown
        as holder.
        """
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list
                            if not (_norm_key(e[0]) == k and (owner is None or e[1] == owner))]
        left = [e[1] for e in self.hotkey_list if _norm_key(e[0]) == k]
        cur = self.hotkeys_owned.get(k)
        if cur is None or owner is None or cur == str(owner):
            if left:
                self.hotkeys_owned[k] = left[0]
            else:
                self.hotkeys_owned.pop(k, None)

    def page_slot(self, key):
        """Return the slot (module or built-in settings page) that a settings page key stands for, or None."""
        s = self.resolve(key)[0]
        if s is None:
            return next((p for p in self.pages if p.key == key), None)
        return s

    def resolve(self, key):
        """Turn a key into (slot, part key): a module key gives (slot, None), a part key gives both, else
        (None, None).
        """
        s = dict.get(self.by_key, key)
        if s is not None:
            return s, None
        m = self.old_map.get(key)
        if m is None and "." in str(key):
            m = str(key).split(".", 1)
        if m is not None:
            s = dict.get(self.by_key, m[0])
            if s is not None and s.part(m[1]) is not None:
                return s, m[1]
        return None, None

    def _note_parts(self, s, default_on, category, parts, aliases):
        """Store the module's default state, category, parts and aliases on its slot.

        Old part keys listed on a part are remembered so saved settings and windows using them still
        resolve.
        """
        s.default_on = bool(default_on)
        s.category = str(category or "Other")
        s.parts = tuple(tuple(p) for p in (parts or ()))
        s.aliases = tuple(str(a) for a in (aliases or ()))
        for p in s.parts:
            for old in (p[4] if len(p) > 4 else ()):
                self.old_map[str(old)] = (s.key, p[0])
            if p[0] not in s.parts_on:
                s.parts_on[p[0]] = False

    def part_on(self, part, module=None):
        """True when part of module (default: the module running now) is switched on."""
        if module is None:
            cur = self.current()
            module = cur.key if cur is not None else None
        s = dict.get(self.by_key, module)
        return bool(s is not None and s.parts_on.get(part))

    def owner_key(self):
        """Return the key a window or request belongs to: the running part's owner for a module with parts,
        else the module key.
        """
        cur = self.current()
        if cur is None:
            return None
        if self.cur_owner is not None and cur.parts:
            return self.cur_owner
        return cur.key

    def _parts_fill(self, s):
        """When a module has parts but none is on, switch on its default parts (or its first).

        A part held off for this session (held_parts) is never chosen as a default.
        """
        if s.parts and not s.parts_wanted():
            for p in [p[0] for p in s.parts if p[3] and (s.key, p[0]) not in self.held_parts] or [s.parts[0][0]]:
                s.parts_on[p] = True

    def _part_notify(self, s):
        """Tell a running module which parts are now wanted, through its parts hook on the client tick."""
        if not s.running or s.api is None or not s.api.get("parts"):
            return
        was = s.busy
        self._enter(s)
        try:
            want = set(s.parts_wanted())
            Kit.on_client(lambda: s.api["parts"](want))
        except Exception as ex:
            self.report(s, ex)
        finally:
            self._leave(s)
            s.busy = was

    def part_set(self, module, part, on):
        """Switch a part of a module on or off, as the player's own choice.

        Any choice makes the part no longer held, so it is saved as the player set it. Switching a part on
        also turns the module on; switching off the last one turns the module off. Otherwise the
        preferences are saved and the module is told. The settings page is refreshed.
        """
        s = dict.get(self.by_key, module)
        if s is None or s.part(part) is None:
            return
        on = bool(on)
        self.held_parts.discard((s.key, part))
        if s.parts_on.get(part) == on:
            if on and not s.enabled:
                self.enable(module)
            return
        s.parts_on[part] = on
        if not on:
            s.error_times.pop(part, None)
        if on and not s.enabled:
            self.enable(module)
        elif not on and not s.parts_wanted():
            self.disable(module)
        else:
            self.save_prefs()
            self._part_notify(s)
        self.refresh_settings(module)

    def alarm_up(self):
        """True while an alarm banner is on screen, or for a short while after an alarm came in during quiet
        time.
        """
        return bool(ALERTS.shown and ALERTS.alarm) or ALERTS.quiet_alarm()

    def typing(self):
        """True while the player is typing in the client (a chat or other text box has focus)."""
        return Client.typing()

    def release_typing(self):
        """Let go of the typing hold taken for the client."""
        Typing.release()

    def grid_size(self):
        """Grid spacing in pixels from the saved preference, kept between 8 and 512."""
        return max(8, min(512, self.pref_int("grid", GRID_DEFAULT)))

    def grid_shown(self):
        """True when the alignment grid is on screen."""
        return self.grid is not None and self.grid.shown

    def grid_toggle(self):
        """Switch the alignment grid on or off, remember it and return whether it is shown now."""
        if self.grid is not None:
            self.grid.toggle()
            self.prefs["grid_on"] = "1" if self.grid_shown() else "0"
            self.save_prefs()
        return self.grid_shown()

    def set_look(self, name):
        """Choose the look (classic, dark, parchment or high contrast; an unknown name gives classic), save it
        and redraw every window in it. Called from the settings page.
        """
        name = name if name in Kit.LOOKS else "classic"
        self.prefs["look"] = name
        self.prefs["dark"] = "1" if name in ("dark", "contrast") else "0"
        self.save_prefs()
        Kit.set_look(name)
        self.restyle("Look: %s." % Kit.LOOK_NAMES[name])

    SWITCHES = {"compact": "Compact rows", "cblind": "Colour-blind marks", "streamer": "Streamer mode"}

    def set_switch(self, key, value):
        """Change one interface switch and redraw: key is tsize (text size percent, one of Kit.TEXT_SIZES),
        compact, cblind or streamer (value is on or off). Saves the choice, sets the matching Kit value,
        says what changed in the system line and ignores any other key.
        """
        if key == "tsize":
            v = int(value) if int(value) in Kit.TEXT_SIZES else 100
            self.prefs[key] = str(v)
            Kit.tscale = v / 100.0
            note = "Text size: %d%%." % v
        elif key in self.SWITCHES:
            on = bool(value)
            self.prefs[key] = "1" if on else "0"
            note = "%s %s." % (self.SWITCHES[key], "on" if on else "off")
            if key == "compact":
                Kit.compact = on
            elif key == "cblind":
                Kit.cblind = on
            else:
                Kit.streamer = on
        else:
            return
        self.save_prefs()
        self.restyle(note)

    def _apply_style(self):
        """Set Kit's look, text scale and the compact, colour-blind and streamer switches from the saved
        interface choices, and load the fade settings. A saved look that disagrees with the saved dark flag
        falls back to dark or classic, which keeps settings saved by an older version meaning the same.
        """
        look, dark = self.prefs.get("look", ""), self.pref_int("dark", 0) == 1
        if look not in Kit.LOOKS or dark != (look in ("dark", "contrast")):
            look = "dark" if dark else "classic"
        Kit.set_look(look)
        ts = self.pref_int("tsize", 100)
        Kit.tscale = (ts if ts in Kit.TEXT_SIZES else 100) / 100.0
        Kit.compact, Kit.cblind = self.pref_int("compact", 0) == 1, self.pref_int("cblind", 0) == 1
        Kit.streamer = self.pref_int("streamer", 0) == 1
        FADE.load(self)

    def restyle(self, note=None):
        """Redraw everything in the current look or scale: retint the frames, rebuild every open module window
        and dock, run the look services of the modules, refresh the settings and layout pages and rebuild
        the alert banner. note is shown in the system line. Client tick or main loop.
        """
        FADE.reset()
        Kit.retint()
        for k, d in list(self.docks):
            try:
                s = d["state"]() if d.get("redraw") is not None else None
            except Exception:
                s = None
            if s in ("open", "minimized"):
                safe(d["redraw"])
        for w in list(Kit._wins.values()):
            if Kit.is_open(w.win.get(w.gkey)):
                w.queue.add("redraw")
        for name, fn in list(self.services.items()):
            if name.startswith("look."):
                safe(fn)
        self.refresh_settings(LAYOUT_OWNER)
        c = self.config
        if c is not None and c.mode == "alone":
            c.refresh()
        elif c is not None:
            c.measured.clear()
            if c.mode == "full":
                c.prof_redraw = True
        safe(ALERTS.rebuild)
        self.poke()
        if self.alert_log.g is not None:
            self.alert_log.open()
        if self.launcher is not None and self.launcher.g is not None:
            Kit.pending.append(self.launcher.rebuild)
        if note:
            Kit.say(note, Kit.HUE_GOOD)

    def dock_wanted(self, key):
        """True when the module window key is wanted in the action bar tray."""
        return key in self._dock_want()

    def _dock_want(self):
        """Return the set of wanted dock keys from the saved preference, parsed again only when the text
        changed.
        """
        raw = self.prefs.get("dock_want", "") or ""
        if raw != self._want_raw:
            self._want_raw = raw
            self._want_set = frozenset(k for k in str(raw).split(",") if k)
        return self._want_set

    def dock_want_set(self, key, on):
        """Add or remove key in the saved list of wanted docks and save."""
        want = self._dock_want()
        if bool(on) == (key in want):
            return
        self.prefs["dock_want"] = ",".join(sorted(want | {key} if on else want - {key}))
        self.save_prefs()

    def dock_forget(self, key):
        """Stop wanting key in the tray."""
        self.dock_want_set(key, False)

    def gump_expect(self, gid, secs=5.0):
        """Service gump.expect: note that a gump with this id is about to open, for up to secs seconds
        (capped).
        """
        gid = int(gid or 0)
        if not gid:
            return
        now = time.time()
        exp = dict((k, t) for k, t in list(self.gump_exp.items()) if 0 < t - now <= GUMP_EXPECT_MAX)
        exp[gid] = now + max(0.0, min(float(secs), GUMP_EXPECT_MAX))
        self.gump_exp = exp

    def gump_expected(self, gid, now):
        """True when a gump with this id was announced and the time has not run out."""
        t = self.gump_exp.get(gid)
        return t is not None and 0 < t - now <= GUMP_EXPECT_MAX

    def dock_to_bar(self, key, title=None):
        """Dock a window into the Action Bar tray.

        Returns True when the bar is up; if not, the window is only minimised and the player is told. It
        does nothing for a window held by a layout zone.
        """
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
        """Tell the player that a window is minimised until the Action Bar opens."""
        API.SysMsg("%s: minimized until the Action Bar opens; then it folds into its tray." % title, Kit.HUE_INFO)

    def dock_add(self, key, hooks):
        """Register a window's dock hooks under key, replacing an older entry; windows with a gump also join
        the layout.

        While booting, a window a zone holds is remembered in _zone_held.
        """
        self.dock_remove(key)
        self.docks.append((key, hooks))
        if self.booting() and LAYOUT.holds(key):
            self._zone_held.add(key)
        gump = hooks.get("gump")
        if gump is not None:
            self.layout_add(key, gump, hooks.get("title"), hooks)

    def dock_remove(self, key):
        """Remove a window's dock hooks and its layout entry."""
        self.docks = [d for d in self.docks if d[0] != key]
        self.layout_remove(key)

    def layout_add(self, key, get_gump, title=None, hooks=None):
        """Add a window to the layout, owned by the module and part running now, and fit it at once."""
        cur = self.current()
        owner = (cur.key, self.cur_part if cur.parts else None) if cur is not None else None
        LAYOUT.add(key, get_gump, title, hooks, owner)
        LAYOUT.fit_added(key)

    def layout_remove(self, key):
        """Remove a window from the layout."""
        LAYOUT.remove(key)

    def layout_slot(self, key):
        """Return the (w, h) the layout zone gives the window, or None when no zone holds it.

        The size the window was last told wins, then the slot it was placed in, then the planned slot.
        """
        key = str(key)
        if not LAYOUT.holds(key):
            return None
        rec = LAYOUT.fitted.get(key)
        if rec is not None and rec.get("told") is not None:
            return rec["told"]
        slot = LAYOUT.placed.get(key) or LAYOUT.plan_at(key)
        return (slot[2], slot[3]) if slot is not None else None

    def layout_rect(self, key):
        """Return the zone rectangle (x, y, w, h) of the window, or None when no zone holds it."""
        key = str(key)
        if not LAYOUT.holds(key):
            return None
        slot = LAYOUT.spot(key)
        return tuple(slot) if slot is not None else None

    def layout_holds(self, key):
        """True when a layout zone holds the window."""
        return LAYOUT.holds(key)

    def layout_need(self, key, w=None, h=None):
        """Tell the layout the size a window needs (w and h, either may be None)."""
        LAYOUT.need(key, w, h)

    def layout_base(self, key):
        """Return the base size of the zone that holds the window."""
        return LAYOUT.zone_base(key)

    def layout_locked(self, key):
        """True when the window is locked in its zone."""
        return LAYOUT.locked(key)

    def layout_arrange(self, on=None):
        """Turn the layout arrange mode on or off (toggle when on is None)."""
        LAYOUT.set_arrange((not LAYOUT.arrange) if on is None else on)

    def layout_arranging(self):
        """True while the layout arrange mode is on."""
        return LAYOUT.arrange

    def layout_in_use(self):
        """True when the layout has windows assigned to zones and is switched on."""
        return bool(LAYOUT.assign) and LAYOUT.enabled

    def layout_pair(self, top_key, bottom_key):
        """Put the window bottom_key below top_key in the layout."""
        return LAYOUT.pair_below(top_key, bottom_key)

    def layout_refit(self):
        """Mark every layout slot to be fitted again on the next pass."""
        LAYOUT.dirty = LAYOUT.fresh = True

    @staticmethod
    def suite_alive():
        """True when another Virtue Assistant on this client has shown it is alive in the last three seconds."""
        try:
            return time.time() - float(API.GetSharedVar(ALIVE_KEY) or 0) < 3.0
        except Exception:
            return False

    def bar_alive(self):
        """True when the Action Bar is running (shared alive stamp fresh); always False in stand-alone mode."""
        if VA_ALONE:
            return False
        try:
            alive = float(API.GetSharedVar(ConfigWindow.LINK_ALIVE) or 0)
        except Exception:
            alive = 0.0
        return time.time() - alive <= ConfigWindow.LINK_STALE

    def bar_on(self):
        """True when the Action Bar module is on, loaded without a failure and has not failed to start. Always
        False in stand-alone mode.
        """
        s = dict.get(self.by_key, "actionbar")
        return not VA_ALONE and s is not None and bool(s.enabled) and not s.broken and not self.bar_dead

    def bar_soon(self):
        """True when the Action Bar is running now, or is on and start-up has not settled yet."""
        return self.bar_alive() or (self.booting() and self.bar_on())

    def dock_soon(self, key):
        """True when window key is wanted in the tray, no zone holds it and the Action Bar is up or coming, so
        it can be built folded into its tray from the start.
        """
        return key in self._dock_want() and not LAYOUT.holds(key) and self.bar_on() and (
            self.booting() or self.bar_alive())

    def dock_tick(self):
        """Fold or unfold windows to match the tray list, and drive key binds; client tick, every 0.25 s at
        most.

        A window that is wanted in the tray and minimised is docked when the bar is up; docked windows
        are undocked when the bar is gone (not while the bar is still starting). Windows held by a zone are
        left to the layout. While start-up has not settled it runs on every pass.
        """
        now = time.time()
        if now < self.dock_next and self.dock_next - now <= 0.25 and self.settled_at is not None:
            return
        self.dock_next = now + 0.25
        Binds.load()
        Binds.tick()
        want = self._dock_want()
        fold, unfold = [], []
        self.zone_up_tick()
        for k, d in self.docks:
            if LAYOUT.holds(k):
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
        elif not (self.booting() and self.bar_on()):
            for d in unfold:
                safe(d.get("undock"))

    ZONE_WAS_VAR = "Layout_zone_was"

    def _zone_was(self):
        """Return the saved table of windows that were docked or minimised before a zone took them, loading
        it once.
        """
        d = self._zone_was_d
        if d is None:
            d = self._zone_was_d = dict(p.split("=", 1) for p in Kit.get_var(self.ZONE_WAS_VAR).split(",") if "=" in p)
        return d

    def _zone_was_save(self):
        """Save the table of previous window states to its saved variable."""
        Kit.put_var(self.ZONE_WAS_VAR, ",".join("%s=%s" % kv for kv in sorted(self._zone_was_d.items())))

    def zone_up_tick(self):
        """Bring windows up when a layout zone takes them and put them back when it lets go; client tick,
        from dock_tick.

        The earlier state (docked or minimised) is saved so it survives a restart. A held window that is
        not open is shown again no more than every two seconds, and not while arranging.
        """
        if VA_ALONE:
            return
        held, was = self._zone_held, self._zone_was()
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
            if on and s is None and not LAYOUT.arrange and time.time() >= self._zone_bring.get(k, 0.0):
                fn = d.get("show") or d.get("on")
                if fn is not None:
                    self._zone_bring[k] = time.time() + 2.0
                    safe(fn)
            if changed and d.get("redraw") is not None and s != "docked":
                safe(d.get("redraw"))

    TWICE = "%s: %s loaded twice (module key \"%s\"); skipped the second copy."
    COMPILE_CAP = 64

    def compiled(self, text, path):
        """Return the compiled code of the module file at path, from a cache when its text is unchanged.

        The cache is kept on the sys module, which outlives a run of the script, so starting the script
        again skips the compile. An entry is used only when its text matches exactly. Entries of another
        install folder are dropped, and the cache is emptied at COMPILE_CAP entries. A cache failure
        only means a fresh compile. compile_hit says whether the last call came from the cache.
        """
        c = None
        self.compile_hit = False
        try:
            import sys
            c = sys.__dict__.get("_COMPILED")
            if not isinstance(c, dict):
                c = {}
                sys._COMPILED = c
            e = c.get(path)
            if type(e) is tuple and len(e) == 3 and e[0] == len(text) and type(e[1]) is str and e[1] == text:
                if type(e[2]) is type(self.compiled.__func__.__code__):
                    self.compile_hit = True
                    return e[2]
        except Exception:
            c = c if type(c) is dict else None
        code = compile(text, path, "exec")
        try:
            if c is not None:
                if path not in c:
                    root = os.path.normcase(os.path.dirname(os.path.dirname(path)))
                    for k in [k for k in c if os.path.normcase(os.path.dirname(os.path.dirname(str(k)))) != root]:
                        c.pop(k, None)
                    if len(c) >= self.COMPILE_CAP:
                        c.clear()
                c[path] = (len(text), text, code)
        except Exception:
            pass
        return code

    SELF_KEY = "_VA_INNER"

    def self_run(self, g):
        """Make the mother script run from its own cached compile. Returns True when the caller must stop.

        g is the script's globals. Called from the tail of the mother. On the outer run it reads the
        script file, takes its code from the entry kept on sys (path, length, text, code; used only when
        all three match) or compiles the text with the import API line left out, and runs that code in the
        same globals with a marker in them; that inner run reaches this call, finds the marker and returns
        False so it carries on starting the suite. Later starts of the script in this client then skip
        parsing and compiling the large file. Returns True once the inner run has done the work, and also
        when a stop was asked; False when the caller itself should go on, which is the case for the inner
        copy, when the file cannot be read or the TazUO setting for the module cache is off, and when an
        earlier inner run failed (the entry then holds no code). The read and compile times go to the split
        timers.
        """
        box = g.get(self.SELF_KEY)
        if box is not None:
            box[1] = True
            for k, ms in box[2]:
                self.split_add(k, ms)
            return False
        import sys
        keep = None
        try:
            path = str(g.get("__file__") or os.path.join(str(API.ScriptPath), str(API.ScriptName)))
            t0 = time.time()
            text = _read_text(path)
            t1 = time.time()
            e = sys.__dict__.get("_VA_SELF")
            same = type(e) is tuple and len(e) == 4 and e[0] == path and e[1] == len(text) and type(e[2]) is str \
                and e[2] == text
            if same and e[3] is None:
                return False
            if same and type(e[3]) is type(self.compiled.__func__.__code__):
                code, kind = e[3], "hit"
            elif safe(self.no_cache, False):
                return False
            else:
                sys._VA_SELF = None
                kind = "compile"
                code = compile(re.sub(r"(?m)^import API$", "", text.replace("\r\n", "\n")), path, "exec")
                sys._VA_SELF = (path, len(text), text, code)
            keep = dict(g)
            ms = (time.time() - t1) * 1000.0
            box = [START_AT, False, [("read:mother", (t1 - t0) * 1000.0), (kind + ":mother", ms)]]
            g[self.SELF_KEY] = box
            exec(code, g)
        except Exception:
            if box is not None and box[1]:
                raise
        finally:
            g.pop(self.SELF_KEY, None)
        if box is not None and box[1]:
            return True
        stop = bool(safe(lambda: API.StopRequested, False))
        if keep is not None:
            g.clear()
            g.update(keep)
            if not stop:
                sys._VA_SELF = (path, len(text), text, None)
        return stop

    @staticmethod
    def no_cache():
        """True when TazUO has its script module cache switched off, in which case the mother does not cache
        itself. Raises when the setting cannot be read; callers wrap it in safe.
        """
        t = Tz.T("ClassicUO.LegionScripting.LegionScripting")
        return bool(Tz.get(None, "LScriptSettings", t).DisableModuleCache)

    def add(self, key, title, desc, factory, interval, default_on=False, category=None, parts=(), aliases=()):
        """Register a module with the host and build its api.

        Returns the slot. A key already loaded for real is reported and skipped; a lazy slot is filled in.
        parts and aliases describe optional sub-features and older keys. In stand-alone mode the first
        module is started alone. A module whose factory fails is marked broken, and the player is told
        unless the script is stopping.
        """
        s = dict.get(self.by_key, key)
        if s is not None and s.lazy is not None:
            s.lazy = None
            s.title, s.desc, s.factory, s.interval = title, desc, factory, interval
            self._note_parts(s, default_on, category, parts, aliases)
        elif s is not None:
            API.SysMsg(self.TWICE % (APP_NAME, title, key), Kit.HUE_BAD)
            return s
        else:
            s = ModuleSlot(key, title, desc, factory, interval)
            self._note_parts(s, default_on, category, parts, aliases)
            self.slots.append(s)
            self.by_key[key] = s
        try:
            s.api = factory()
        except Exception as ex:
            s.broken = str(ex) + _error_where()
            if not self.stopping():
                Kit.say("couldn't load %s (%s)." % (title, s.broken), Kit.HUE_BAD)
        self._arm(s)
        if VA_ALONE and self.alone is None:
            self.run_alone(s)
        return s

    @staticmethod
    def _arm(s):
        """Cache from the module's api which hooks it has (client tick, interval, thread tick, thread
        wanted).
        """
        api = s.api
        s.on_client = bool(api and api.get("client_tick"))
        s.iv_fn = api.get("interval") if api else None
        s.has_thread = bool(api) and "thread_tick" in api
        s.thread_want = api.get("thread_wanted") if api else None

    def add_lazy(self, key, title, desc, path, interval, default_on=False, category=None, parts=(), aliases=()):
        """Register a module whose file is read later, from path, on first use; returns the slot."""
        if dict.__contains__(self.by_key, key):
            return dict.__getitem__(self.by_key, key)
        s = ModuleSlot(key, title, desc, None, interval)
        self._note_parts(s, default_on, category, parts, aliases)
        s.lazy = path
        self.slots.append(s)
        self.by_key[key] = s
        return s

    def request_load(self, s):
        """Queue a lazy module to be loaded on the next idle pass. Returns False when it is not lazy."""
        if s is None or s.lazy is None:
            return False
        if s not in self.load_jobs:
            self.load_jobs.append(s)
        self.poke()
        return True

    def _run_load_jobs(self):
        """Load the queued modules and start those that are on, in start rank order; a module that fails to
        load is switched off and remembered.

        With two or more modules queued, compile_ahead may load and start some of them while the others
        are still being compiled. The rest are loaded here, then all of those are started together.
        """
        if not self.load_jobs or self.stack:
            return
        jobs, self.load_jobs, todo = self.load_jobs, [], []
        jobs, owed, rank = self.compile_ahead(jobs)
        for s in jobs:
            if self.stopping():
                break
            if self._load_job(s):
                todo.append(s)
        todo.sort(key=lambda s: rank[s.key] if s.key in rank else self._start_rank(s))
        self.start_all(todo)
        if owed and not todo:
            safe(lambda: Kit.on_client(self._starts_done))

    def _load_job(self, s):
        """Load module s (switching it off and remembering that when its file fails to load) and tell the
        settings window it loaded. Returns True when it is on and should now be started.
        """
        ok = self.load(s)
        if not ok and s.enabled and not self.stopping():
            s.enabled = False
            self.held_on.add(s.key)
            self.save_prefs()
        if self.config is not None:
            self.config.loaded(s.key)
        return ok and s.enabled and not s.running and not s.pending_stop

    AHEAD_WAIT = 5.0

    def compile_ahead(self, jobs):
        """Load and start the queued modules with their compiling overlapped with the client thread's work.

        Returns (the jobs not handled, whether the final start-up call is still owed, start ranks by key).
        Any failure turns the overlap off (ahead_off) and leaves all the jobs to the caller.
        """
        done, box = [], {"owed": False, "rank": {}}
        try:
            self._ahead(jobs, done, box)
        except Exception:
            self.ahead_off = True
        return [s for s in jobs if s not in done], box["owed"], box["rank"]

    def _ahead(self, jobs, done, box):
        """Load modules in start rank order, starting each while the remaining cold files compile.

        Does nothing once start-up has settled, with fewer than two jobs, on the client thread, or when
        every file is already compiled in the cache. A module is loaded and started with its start hops
        posted to the client thread; during each hop this thread compiles the next cold file (ahead).
        Modules that load once nothing is left to compile are collected and started together at the end.
        done collects the modules handled here; box gets the ranks used and whether _starts_done is owed
        (start_all is called with last False until the final group).
        """
        if self.settled_at is not None or len(jobs) < 2 or self._poster() is None:
            return
        import sys
        c = sys.__dict__.get("_COMPILED")
        c = c if type(c) is dict else {}
        texts = self.texts

        def warm(path):
            """True when the file at path is already in the compile cache with text of the length read."""
            e = c.get(path)
            return type(e) is tuple and len(e) == 3 and e[0] == len(texts.get(path) or "")

        rank = dict((s.key, self._start_rank(s)) for s in jobs)
        order = sorted(jobs, key=lambda s: rank[s.key])
        cold = [s for s in order if s.lazy is not None and not warm(s.lazy)]
        if not cold:
            return
        box["rank"] = rank
        self.ahead_off = False
        left = lambda: [x for x in cold if x.lazy is not None and x.lazy not in self.ahead_ms]

        def ahead(busy):
            """Compile the next module file that has not been compiled, again and again, while busy() is true.

            Runs on the script thread during a client hop. The text is read once and kept in texts; the time
            spent goes to ahead_ms so load can report it. A failure turns the overlap off.
            """
            while busy() and not self.ahead_off:
                todo = left()
                if not todo:
                    break
                path = todo[0].lazy
                try:
                    text = texts.get(path)
                    if text is None:
                        text = _read_text(path)
                        texts[path] = text
                    t0 = time.time()
                    self.compiled(text, path)
                    self.ahead_ms[path] = time.time() - t0
                except Exception:
                    self.ahead_off = True

        tail = []
        for s in order:
            if self.stopping() or self.ahead_off:
                return
            bar = self.bar_on()
            go = self._load_job(s)
            # A module that put the Action Bar up or took it down changes which modules fold into its tray, so
            # the ranks are recomputed without that last wait and the overlap stops.
            if self.bar_on() != bar:
                self.ahead_off = True
                box["rank"] = dict((k, 2 if r == 3 else r) for k, r in rank.items())
                if not go:
                    done.append(s)
                return
            if go and (tail or not left()):
                tail.append(s)
                continue
            if go:
                box["owed"] = True
                self.start_all((s,), ahead, False)
            done.append(s)
        if tail:
            box["owed"] = False
            self.start_all(tail)
            done.extend(tail)

    def _poster(self):
        """Return Client.post, or None when the client thread cannot be queued to, or this code is already on
        it.
        """
        if (Client.MTQ if Client.mtq_looked else Client._find_mtq()) is None or Client.on_client_thread():
            return None
        return Client.post

    def _hop(self, fn, ahead):
        """Run fn on the client thread while the script thread runs ahead(busy) meanwhile. Returns fn's result.

        Without ahead, or when it is turned off or the queue is unreachable, this is Kit.on_client. fn is
        posted without waiting; ahead is called with a function that stays true until the hop is finished
        or, if the client has not begun it, until AHEAD_WAIT seconds have passed. If the client never
        began within that time the hop is cancelled (a late run does nothing) and fn runs through
        Kit.on_client instead. The result, or the error, is passed back as Kit.on_client would.
        """
        post = None if ahead is None or self.ahead_off else self._poster()
        if post is None:
            return Kit.on_client(fn)
        import _thread
        lk, began, done = _thread.allocate_lock(), _thread.allocate_lock(), _thread.allocate_lock()
        began.acquire()
        done.acquire()
        hop = _Hop(fn)
        box = {"go": None}
        t0 = time.time()

        def run():
            """Runs on the client thread: begin fn once, unless it was cancelled, then signal that it finished."""
            with lk:
                if box["go"] is not None:
                    return
                box["go"] = True
            began.release()
            try:
                hop.run()
            finally:
                done.release()

        try:
            post(run)
        except Exception:
            self.ahead_off = True
            return Kit.on_client(fn)
        try:
            ahead(lambda: done.locked() and (box["go"] is not None or time.time() - t0 < self.AHEAD_WAIT))
        except Exception:
            self.ahead_off = True
        if not began.acquire(True, max(0.0, self.AHEAD_WAIT - (time.time() - t0))):
            with lk:
                late = box["go"] is None
                box["go"] = box["go"] or False
            if late:
                self.ahead_off = True
                return Kit.on_client(fn)
        done.acquire()
        if hop.e is not None:
            raise hop.x if isinstance(hop.x, Exception) else Exception(hop.e)
        return hop.v

    def _start_rank(self, s):
        """Sort key for starting modules: the layout owner first, then the Action Bar, then ordinary modules,
        and last the ones that will fold into the Action Bar's tray (so the bar is up when they start).
        """
        if s.key == LAYOUT_OWNER:
            return 0
        if s.key == "actionbar":
            return 1
        return 3 if self.dock_soon(s.key) else 2

    def load(self, s):
        """Load a lazy module now: compile and run its file in this namespace.

        The compile goes through Host.compiled. The file registers itself with the host. When it does
        not, or fails, the slot is marked broken with the message and line, and the player is told. The
        text may have been read, and the file compiled, ahead of this call. The read, compile (or cache
        hit) and run times go to the split timers under the module's key. While start-up timing runs, the
        time taken is added to the boot list under the module's title. Returns True when the module has
        an api.
        """
        if s is None:
            return False
        if s.lazy is not None:
            path = s.lazy
            t0 = time.time()
            pre = self.ahead_ms.pop(path, None)
            try:
                text = self.texts.pop(path, None) or _read_text(path)
                t1 = time.time()
                code = self.compiled(text, path)
                hit, t2 = self.compile_hit, time.time()
                exec(code, globals())
                t3 = time.time()
                hit = hit and pre is None
                if s.lazy is not None:
                    raise Exception("the file's HOST.add line didn't run")
                for n, a, b in (("read", t0, t1), ("hit" if hit else "compile", t1, t2 if pre is None else t1 + pre),
                                ("exec", t2, t3)):
                    self.split_add(n + ":" + s.key, (b - a) * 1000.0)
            except Exception as ex:
                s.lazy = None
                line = getattr(ex, "lineno", None)
                where = (" (%s line %s)" % (os.path.basename(path), line)) if line else _error_where()
                s.api, s.broken = None, "%s%s" % (getattr(ex, "msg", None) or ex, where)
                if not self.stopping():
                    Kit.say("couldn't load %s (%s)." % (s.title, s.broken), Kit.HUE_BAD)
            if self.boot is not None:
                d = time.time() - t0
                self.boot.append((s.title, d))
                self.boot_load += d
        return s.api is not None

    def boot_mark(self, name):
        """Close a start-up phase called name: add it to the boot list with the time since the last phase.

        Does nothing once start-up timing has finished.
        """
        if self.boot is not None:
            t = time.time()
            self.boot.append((name, t - self.boot_at))
            self.boot_at = t

    def boot_done(self):
        """End start-up timing and, only when the main setting startup is 1 and the suite is not running
        alone, keep one journal line with the total and each phase.

        Called by run_due once the module load jobs are done. The last phase, first build, is the time
        since the final mark less the module compile times already listed. This is also the moment the
        backup list is read and the backup for a new version is requested (backup_start). The line is
        printed by settle_report, at once when start-up has already settled.
        """
        # Setting boot to None above makes this a one-shot, whether or not the line is printed.
        boot, self.boot = self.boot, None
        t = time.time()
        if self.alone is None:
            self.backup_start()
        if self.alone is None and self.pref_int("startup", 0) == 1:
            boot.append(("first build", max(0.0, t - self.boot_at - self.boot_load)))
            self.boot_line = "start-up took %.1f s (%s)" % (t - START_AT, ", ".join("%s %d ms" % (n, d * 1000)
                                                                                  for n, d in boot))
        if self.settled_at is not None:
            self.settle_report()

    def built(self, key):
        """Count a build of window key while start-up has not settled (at most 200 different keys), for the
        settling report.
        """
        b = self.builds
        if self.settled_at is None and (key in b or len(b) < 200):
            b[key] = b.get(key, 0) + 1

    def settle_tick(self, now):
        """Decide whether start-up has settled; called every pass of the main loop until it has.

        Start-up is busy while the load list, the layout, the hub, the settings window or any hold from
        settle_hold still has work, and for SETTLE_QUIET seconds (SETTLE_QUIET_HOLD while a hold is open)
        after the last such work or window change (Kit.churn_at). It is also declared settled after
        SETTLE_CAP seconds, unless the safe-start window is waiting for the player. When settled it drops
        the read-ahead module texts, prints the report and brings the Script Manager window to the front.
        In stand-alone mode it settles at once and ends the split timers.
        """
        if self.alone is not None:
            self.settled_at = now
            self.split_end()
            return
        cfg, hub, lay = self.config, self.hub, LAYOUT
        if (self.boot is not None or self.load_jobs or (lay.enabled and lay.loaded and (
                lay.dirty or lay.fresh or lay.fresh_adds or lay.seam_wait)) or (hub is not None and hub.dirty)
                or (cfg is not None and (cfg.request is not None or cfg.request_tab is not None or (
                    cfg.mode == "full" and (cfg.redraw_req or cfg.prof_redraw))))
                or any(safe(fn, False) for fn in self.settle_holds)):
            self.settle_seen = now
        capped = self.ask_g is None and now - (self.settle_from or START_AT) >= self.SETTLE_CAP
        quiet = self.SETTLE_QUIET_HOLD if self.settle_holds else self.SETTLE_QUIET
        if not capped and now - max(self.settle_seen, Kit.churn_at) < quiet:
            return
        if not capped and safe(lay.plan_prune, False):
            self.settle_seen = now
            return
        self.settled_at, self.settle_capped = now, capped
        del self.settle_holds[:]
        self.texts.clear()
        self.ahead_ms.clear()
        self.settle_report()
        safe(lambda: Kit.on_client(self.front_script_manager))

    def booting(self):
        """True while start-up has not settled."""
        return self.settled_at is None

    def settle_hold(self, fn):
        """Keep start-up unsettled while fn() returns true; used by a module with work still to finish
        (at most 32 holds, dropped once settled).
        """
        if self.settled_at is None and len(self.settle_holds) < 32:
            self.settle_holds.append(fn)

    def split_add(self, key, ms):
        """Record a split timer: key to milliseconds (or a count), while the timers run and fewer than
        SPLIT_CAP keys are held.
        """
        sp = self.split
        if sp is not None and (key in sp or len(sp) < self.SPLIT_CAP):
            sp[key] = ms

    def split_at(self, name):
        """Record how long after the start of the script the current module (or the named part) was ready."""
        s = self.current()
        self.split_add("at:" + (name if s is None else s.title), (time.time() - START_AT) * 1000.0)

    def split_end(self):
        """End the split timers: drop the list and give the raw Create* calls back to G, so nothing is
        counted or wrapped any more.
        """
        self.split = None
        G.made = None
        for k in [k for k in G.__dict__ if k.startswith("Create")]:
            G.__dict__.pop(k, None)

    def split_line(self, sp):
        """Build the start-up splits line the report prints from the timers sp.

        It adds up read, compile (cache hits included, with their count) and set-up times of the module
        files, the number of start steps with the longest one and the controls it made, and the times
        parts reported they were ready.
        """
        tot = dict((n, 0.0) for n in ("read", "compile", "hit", "exec"))
        marks = []
        for k, v in sp.items():
            n = k.split(":", 1)
            if len(n) == 2 and n[0] in tot:
                tot[n[0]] += v
            elif len(n) == 2 and n[0] == "at":
                marks.append((v, n[1]))
        hops = int(sp.get("hops", 0))
        top = max([(sp.get("hop %d" % i, 0.0), i) for i in range(1, hops + 1)]
                  or [(0.0, 0)])
        text = "Splits: read %d ms, compiled %d ms (%d cached), set up %d ms; started in %s (longest %d ms, %s)" % (
            tot["read"], tot["compile"] + tot["hit"], len([k for k in sp if k.startswith("hit:")]), tot["exec"],
            Kit.count(hops, "step"), top[0], Kit.count(int(sp.get("hop %d controls" % top[1], 0)), "control"))
        return text + "".join("; %s ready at %.1f s" % (n, v / 1000.0) for v, n in sorted(marks)) + "."

    @staticmethod
    def front_script_manager():
        """Put the client's Script Manager window on top of the other windows, so it is not buried by the
        windows built at start-up. Client thread. Does nothing when the start-up order setting is off.
        """
        if Host.ORDER_OFF in HOST.tz_off:
            return
        uim = Tz.T("ClassicUO.Game.Managers.UIManager")
        node = Tz.get(None, "Gumps", uim).First
        n = 0
        while node is not None and n < 2000:
            v = node.Value
            if str(v.GetType().Name) == "ScriptManagerWindow" and not v.IsDisposed:
                Tz.call(None, "MakeTopMostGump", [v], uim)
                return
            node = node.Next
            n += 1

    def settle_report(self):
        """Print the start-up line (with when it settled) and up to two more lines, once.

        The second line counts the window builds while settling, names the windows built more than once,
        and lists when the main window was built and why, and what was ignored before any input. The
        third is the splits line (split_line), printed when the timers held anything. The timers end here
        once start-up timing is over. Nothing is printed when no line was kept (start-up timing is off) or
        when running alone.
        """
        line, self.boot_line, sp = self.boot_line, None, self.split
        if self.boot is None:
            self.split_end()
        if line is None or self.alone is not None:
            return
        end = ("not settled after %d s" % self.SETTLE_CAP) if self.settle_capped else \
            ("settled at %.1f s" % (self.settled_at - START_AT))
        Kit.say("%s; %s." % (line, end), Kit.HUE_INFO)
        names = sorted((-n, APP_NAME if k == ConfigWindow.DOCK_KEY else safe(lambda: LAYOUT.title_of(k), k))
                       for k, n in self.builds.items() if n > 1)
        text = "Settling: " + Kit.count(sum(self.builds.values()), "window build")
        if names:
            text += " (%s)" % ", ".join("%s %d" % (t, -n) for n, t in names[:6])
        log = self.config.why_log if self.config is not None else []
        if log:
            text += ", main window built at " + ", ".join("%.1f s (%s)" % (t - START_AT, self.why_text(w))
                                                          for t, w in log[-3:])
        stale = self.config.stale_log if self.config is not None else []
        if stale:
            text += ", ignored before any input: " + ", ".join("%s at %.1f s" % (
            self.why_text(w), t - START_AT) for t, w in stale[-3:])
        Kit.say(text + ".", Kit.HUE_INFO)
        if sp:
            Kit.say(self.split_line(sp), Kit.HUE_INFO)

    WHY_WORDS = {"link": "Settings link", "gear": "gear click", "redraw": "refresh"}

    def why_text(self, why):
        """Turn a reason a main window was built (kind or kind:argument) into words for the report."""
        kind, _, arg = str(why).partition(":")
        s = dict.get(self.by_key, arg) if arg else None
        if kind == "request":
            return "%s settings" % (s.title if s is not None else arg)
        if kind == "tab":
            return "%s tab" % arg.capitalize()
        return self.WHY_WORDS.get(kind, kind)

    def current(self):
        """Return the slot of the module being run now, or None."""
        return self.stack[-1] if self.stack else None

    def stopping(self):
        """True when the script is being stopped, by the host or by the client."""
        if self.quitting:
            return True
        try:
            return bool(API.StopRequested)
        except Exception:
            return True

    def aborting(self):
        """True when whatever is running should end now: the script stops, a second client-thread wait, or
        the module is stopping or off.
        """
        if self.stopping():
            return True
        if self.client_idles > 1 and Client.on_client_thread():
            return True
        s = self.current()
        return s is not None and (s.pending_stop or not s.enabled)

    def idle(self, seconds):
        """Wait seconds without blocking the host.

        On the client thread it only notes the call (one is allowed) and returns at once. On a script
        thread it keeps the host drained until the time is up. Returns False when the wait was cut short
        by a stop request.
        """
        if Client.on_client_thread():
            self.client_idles += 1
            return self.client_idles <= 1 and not self.aborting()
        end = time.time() + max(0.0, seconds)
        while not API.StopRequested:
            if self.aborting():
                return False
            self.drain()
            self.run_due()
            if self.aborting():
                return False
            rem = end - time.time()
            # A clock that jumped (forward or back) ends the wait instead of sleeping the wrong time.
            if rem <= 0 or rem > seconds + 1.0:
                return True
            API.Pause(min(HOST_TICK, rem))
        return False

    def _enter(self, s):
        """Mark module s as running code and push it on the stack of modules being run."""
        s.busy = True
        self.stack.append(s)

    def _leave(self, s):
        """Take s off the stack of running modules and mark it idle."""
        stack = self.stack
        if stack and stack[-1] is s:
            stack.pop()
        elif s in stack:
            stack.remove(s)
        s.busy = False

    def report(self, s, ex, what=None, part=None):
        """Report an error of a module in the system line (each distinct message once) and count it.

        what names the failing part of the module; part its part key. The message carries the file and
        line.
        """
        msg = str(ex) + _error_where()
        if msg not in s.errors:
            s.errors.add(msg)
            Kit.say("%s error (still running): %s" % (what or s.title, msg), Kit.HUE_BAD)
        self.count_error(s, what, part)

    def count_error(self, s, what=None, part=None, page=False):
        """Count an error against a module or one of its parts.

        Errors older than ERROR_SECS are discarded; when MAX_MODULE_ERRORS remain, the module (or that
        part) is told off and switched off. page=True counts at most one error a second, for window code.
        """
        now = time.time()
        if page:
            if 0 <= now - s.page_err_at < 1.0:
                return
            s.page_err_at = now
        seen = [t for t in s.error_times.get(part, ()) if 0 <= now - t < ERROR_SECS]
        seen.append(now)
        s.error_times[part] = seen
        if len(seen) < MAX_MODULE_ERRORS or not s.enabled:
            return
        s.error_times.pop(part, None)
        Kit.say("%s kept failing and was switched off." % (what or s.title), Kit.HUE_BAD)
        if part is not None and s.parts and s.parts_on.get(part):
            self.part_set(s.key, part, False)
        else:
            self.disable(s.key)

    def start(self, s):
        """Start module s: mark it running and run its start hook on the client tick.

        Same as start_all for one module. A start that is overtaken by a stop undoes itself, and a failure
        to start switches the module off and saves that.
        """
        self.start_all((s,))

    def start_all(self, slots, ahead=None, last=True):
        """Start several modules together, hopping to the client thread as few times as possible.

        Each module is prepared first (_start_prep), then the start hooks run in slices on the client tick
        (_start_hop), through _hop so that compile-ahead work can run meanwhile when ahead is given. last
        False leaves out the final _starts_done call, because more starts follow. A module whose start
        never ran because the hop failed is queued to load again. The results are then settled one by one
        (_start_end).
        """
        runs = [r for r in (self._start_prep(s) for s in slots) if r is not None]
        n = len(runs)
        pos = {"i": 0}
        while pos["i"] < n and not self.stopping():
            i = pos["i"]
            try:
                self._hop(lambda: self._start_hop(runs, pos, n, last), ahead)
            except Exception as ex:
                msg = str(ex) + _error_where()
                pos["gone"] = True
                hit = False
                for r in runs[i:]:
                    with r["lk"]:
                        began, ended = r["began"], r["ended"]
                    if ended or r["err"] is not None:
                        continue
                    if began or not hit:
                        r["err"] = msg
                        hit = True
                    else:
                        r["again"] = True
                pos["i"] = n
        for j, r in enumerate(runs):
            if r["again"] or j >= pos["i"]:
                with r["lk"]:
                    r["s"].start_tok = None
                    r["s"].running = False
        for r in runs:
            self._start_end(r)
        again = [r["s"] for r in runs if r["again"] and r["s"] not in self.load_jobs]
        if again and not self.stopping():
            self.load_jobs[:0] = again

    def _start_prep(self, s):
        """Prepare the start of module s and return its run record, or None when it is running, the script is
        stopping or it will not load.

        The record holds the lock, the flags began and ended, the error, and the undo and go functions the
        client tick uses. The start token makes a start that is overtaken by a stop undo itself.
        """
        if s.running or self.stopping() or not self.load(s):
            return None
        s.errors, s.error_times = set(), {}
        s.pending_stop = False
        tok = s.start_tok = object()
        import _thread
        lk = _thread.allocate_lock()
        run = {"s": s, "lk": lk, "began": False, "ended": False, "undone": False, "err": None, "again": False}

        def undo():
            """Run the module's stop hook and release its claims, once only."""
            with lk:
                if run["undone"]:
                    return
                run["undone"] = True
            safe(lambda: s.api["stop"]())
            safe(lambda: self._unclaim(s))

        def go():
            """Run the module's start hook on the client tick, unless a stop overtook it, and undo the start when
            one did meanwhile.
            """
            with lk:
                if s.start_tok is not tok or not s.running or run["began"]:
                    return
                run["began"] = True
            try:
                s.api["start"]()
            finally:
                with lk:
                    run["ended"] = True
                    late = s.start_tok is not tok or not s.running
                if late:
                    undo()

        run["undo"], run["go"] = undo, go
        if s.key == "actionbar":
            self.bar_dead = False
        try:
            s.running = True
            self._arm(s)
            self._refresh_active()
        except Exception as ex:
            run["err"] = str(ex) + _error_where()
        return run

    def _start_hop(self, runs, pos, n, last=True):
        """One client-tick slice of starting: start modules in turn until START_HOP seconds are used, so one
        tick is never held up long.

        While the split timers run, the slice's length and the controls created in it are recorded.
        """
        t0, m0 = time.time(), G.made
        while pos["i"] < n and not pos.get("gone"):
            r = runs[pos["i"]]
            pos["i"] += 1
            self._start_go(r)
            if time.time() - t0 >= self.START_HOP:
                break
        if pos["i"] >= n and not pos.get("gone") and last:
            self._starts_done()
        sp = self.split
        if sp is not None and m0 is not None:
            h = sp["hops"] = sp.get("hops", 0) + 1
            self.split_add("hop %d" % h, (time.time() - t0) * 1000.0)
            self.split_add("hop %d controls" % h, (G.made or m0) - m0)

    def _start_go(self, r):
        """Start one module of the run list on the client tick, recording its error. A failed or dead Action
        Bar is noted in bar_dead.
        """
        s = r["s"]
        if r["err"] is None:
            self._enter(s)
            self.client_idles = 0
            try:
                r["go"]()
            except Exception as ex:
                r["err"] = str(getattr(ex, "InnerException", None) or ex) + _error_where()
            finally:
                self._leave(s)
        if s.key == "actionbar" and (r["err"] is not None or not self.bar_alive()):
            self.bar_dead = True

    def _starts_done(self):
        """After the last start: when the Action Bar did not come up, sync the tray list and run the dock
        pass so windows folded for it open again.
        """
        cfg = self.config
        if self.bar_dead and self.alone is None and cfg is not None:
            safe(cfg.dock_sync)
            safe(self.dock_tick)

    def _start_end(self, r):
        """Finish one start on the script thread: on an error release the module, say so, undo the start and
        switch it off (saved); then refresh the active list and make the module due.

        When the script is stopping, an error is neither said nor saved, because a stop explains it.
        """
        s = r["s"]
        if r["err"] is not None:
            with r["lk"]:
                s.start_tok = None
                s.running = False
                busy = r["began"] and not r["ended"]
            stop = self.stopping()
            if not stop:
                Kit.say("couldn't start %s (%s)." % (s.title, r["err"]), Kit.HUE_BAD)
            if not busy:
                r["undo"]()
            if not stop:
                s.enabled = False
                self.save_prefs()
        self._refresh_active()
        s.next_due = 0.0

    def _stop(self, s):
        """Stop module s now: release its claims, run its stop hook and mark it not running."""
        s.pending_stop = False
        if not s.running:
            return
        self._unclaim(s)
        self._enter(s)
        try:
            s.api["stop"]()
        except Exception:
            pass
        finally:
            s.running = False
            self._leave(s)
            self._refresh_active()

    def _unclaim(self, s):
        """Release everything a stopping module holds: target requests, the cursor claim, hotkeys and key
        hooks.

        Hotkeys it held pass to the next owner waiting for them.
        """
        olds = [s.key] + [old for p in s.parts for old in p[4]]
        for k in olds + [p[0] for p in s.parts]:
            Picker.drop(k)
        if self.cursor_claim[0] in olds:
            self.cursor_claim = (None, 0.0)
        for k, wait in list(self.hk_wait.items()):
            for w in [w for w in wait if w[2] == s.key]:
                self.hotkey_off(k, w[0])
        for k, ent in list(self.hk_fns.items()):
            if ent[2] == s.key:
                self.hotkey_off(k, ent[0])
        pre = s.key + "."
        for owner in list(Kit._hooks):
            if owner in olds or str(owner).startswith(pre):
                Kit.unhook(owner)

    def tick(self, s, hook="tick"):
        """Run one hook (tick by default, or thread_tick) of module s, timing it.

        Errors are reported and counted, never raised. The time of each call is added to the module's
        load record, which feeds the stats (busiest parts, slowest lately). After a tick the next due time
        and whether the thread hook is wanted are asked from the module. A stop requested while the
        module was busy is carried out afterwards.
        """
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
            Host.busy_add(s.load, (t1 - t0) * 1000.0, t1)
        if hook == "tick":
            s.next_due = t1 + Host._ask(s.iv_fn, s.interval)
            s.thread_due = s.has_thread and Host._ask(s.thread_want, True, bool)
        if s.pending_stop:
            self._stop(s)

    BUSY_T = 10.0

    @staticmethod
    def busy_add(ld, ms, t1):
        """Add one tick of ms milliseconds, ending at time t1, to the load record ld.

        ld is [decayed ms sum, last time, slowest tick]. The sum decays with a time constant of BUSY_T
        (10 s), so sum / BUSY_T is the busy milliseconds per second. The slowest tick decays by 2% per
        tick, so it shows the worst time lately. Runs on whichever thread ran the tick.
        """
        d = ld[1] - t1
        # The sum only decays when time has passed; a clock that jumped back adds no decay.
        ld[0] = (ld[0] * math.exp(d / Host.BUSY_T) if d < 0.0 else ld[0]) + ms
        ld[1] = t1
        w = ld[2] * 0.98
        ld[2] = ms if ms > w else w

    @staticmethod
    def busy_share(ld, now):
        """Return the busy milliseconds per second of load record ld, read at time now.

        The stored sum is decayed to now first, so a module that has gone quiet fades away.
        """
        d = ld[1] - now
        return (ld[0] * math.exp(d / Host.BUSY_T) if d < 0.0 else ld[0]) / Host.BUSY_T

    @staticmethod
    def _ask(fn, default, cast=None):
        """Call a module hook fn for a value (the default when it is missing or fails); cast converts the
        result.
        """
        if fn is None:
            return default
        try:
            v = fn()
            return cast(v) if cast else (v or default)
        except Exception:
            return default

    def enable(self, key):
        """Switch a module (or a part, when key names one) on, save it and start it.

        A lazy module that is not loaded yet is loaded on the next idle pass when called from the client
        thread.
        """
        s, part = self.resolve(key)
        if s is None:
            return
        if self.off_q:
            self.off_q = [e for e in self.off_q if e[1:] != (s.key, part)]
        if part is not None:
            self.part_set(s.key, part, True)
            return
        self._parts_fill(s)
        if s.lazy is not None and Client.on_client_thread():
            s.enabled = True
            self.save_prefs()
            self.request_load(s)
            return
        if not self.load(s):
            return
        s.enabled = True
        if s.running and s.pending_stop:
            s.pending_stop = False
        self.save_prefs()
        self.start(s)

    def show_settings(self, key):
        """Open the settings window at the page of module key."""
        if self.config is not None:
            self.config.show_settings(key)

    def refresh_settings(self, key):
        """Redraw the settings page of a module (or a part's module)."""
        if self.config is not None:
            s, _part = self.resolve(key)
            self.config.refresh(s.key if s is not None else key)

    def disable(self, key):
        """Switch a module (or a part) off and save it.

        During a drain the request is queued. A running module is stopped at once when not busy, otherwise
        as soon as its tick ends. A module with parts called from one of its own parts turns that part
        off.
        """
        s, part = self.resolve(key)
        if s is None:
            return
        if self.shut or self.stopping():
            return
        if self.draining:
            self.off_q.append((key, s.key, part))
            return
        if part is None and s.parts and self.cur_part is not None and self.current() is s \
                and s.parts_on.get(self.cur_part):
            part = self.cur_part
        if part is not None:
            self.part_set(s.key, part, False)
            return
        self.held_on.discard(s.key)
        s.enabled = False
        self.save_prefs()
        if s.running:
            s.pending_stop = True
            if not s.busy:
                self._stop(s)

    def run_due(self):
        """One pass of the main loop: handle a profile request, run the client pass, then tick modules that
        are due.

        Client-tick modules run inside the client pass. Script-thread modules are ticked here when poked,
        named by a poke key, or due by their interval (also when the clock jumped back). The TazUO settings
        check runs here when due, on the script thread and never inside a module tick. Thread hooks run
        when wanted. Blocking target requests and queued module loads are handled last. When the load
        jobs are all done, start-up timing is closed with boot_done, and the start mark is cleared once
        every running module has ticked at least once.
        """
        if self.shut:
            return
        if self.profile_req is not None and not self.stack:
            req, self.profile_req = self.profile_req, None
            self.profile_job(req)
            return
        poked, self.poked = self.poked, False
        self.pass_id += 1
        keys, user = self.poke_keys, self.poke_user
        if keys:
            self.poke_keys = set()
        else:
            keys = self.NO_KEYS
        self.poke_user = False
        self.pass_keys = keys
        if poked or user:
            self.ui_next = 0.0
        now = time.time()
        if self.prefs_due:
            self.prefs_flush()
        if now >= self.tz_at:
            self.tz_warn()
        if poked or keys or self._client_due(now):
            self.pass_poked, self.pass_all = poked or user, poked
            try:
                Kit.on_client(self._pass_fn)
            except Exception as ex:
                if not self.stopping():
                    self._tell("%s: pass error: %s" % (APP_NAME, ex))
            poked, keys = self.pass_all, self.pass_keys
            if self.stopping():
                return
            if self.off_q:
                q, self.off_q = self.off_q, []
                for e in q:
                    self.disable(e[0])
            now = time.time()
        if Picker.jobs:
            Picker.run_blocking()
        for s in self.active:
            if s.pending_stop:
                if s.busy:
                    continue
                self._stop(s)
            elif s.busy or not s.running:
                continue
            # A clock that went back more than CLOCK_BACK seconds makes the module due at once.
            elif not s.on_client and (poked or s.key in keys or now >= s.next_due
                                      or s.next_due - now > self.CLOCK_BACK):
                self.tick(s)
            elif s.thread_due:
                s.thread_due = False
                self.tick(s, "thread_tick")
            else:
                continue
            if self.stopping():
                return
            self.drain()
        if self.load_jobs and not self.stack:
            self._run_load_jobs()
        elif self.boot is not None and not self.load_jobs and self.ask_g is None:
            self.boot_done()
        # The start mark stays set while the safe-start window waits, while modules are still loading and
        # until each running module has ticked once (a tick sets next_due). A start that hangs or crashes
        # before this point leaves the mark for the next start to find.
        elif self.marked and self.ask_g is None and not self.load_jobs and all(s.next_due > 0.0 for s in self.active):
            self.unmark()
        cfg = self.config
        if cfg is not None and cfg.prof_stale and not self.stack:
            cfg.refresh_profiles()

    LOOKAHEAD = HOST_TICK + 0.035
    CLOCK_BACK = 60.0
    EARLY = 0.008
    MOB_AGE = 0.1
    PACK_CAP = 6000
    PREFS_EVERY = 1.0
    SETTLE_QUIET = 0.25
    SETTLE_QUIET_HOLD = 0.5
    SETTLE_CAP = 30.0
    START_HOP = 0.05
    SPLIT_CAP = 300
    ORDER_OFF = "start-up_order"

    def _client_due(self, now):
        """True when the client pass is needed now: the UI is due, a target job or window work is waiting, or
        a client module is about to be due.
        """
        if now >= self.ui_next or Picker.jobs or (Kit.pending and self.config is not None):
            return True
        if self.ui_next - now > UI_TICK and SNAP.pressed():
            self.ui_next = now
            return True
        if self.ui_next - now > 1.0:
            self.ui_next = now
            return True
        soon = now + self.look
        for s in self.client_run:
            if soon >= s.next_due:
                return True
            if s.next_due - now > self.CLOCK_BACK:
                s.next_due = now
                return True
        return False

    def drain(self, hop=False):
        """Run the callbacks that the client has queued for this script (API.ProcessCallbacks).

        Only one thread drains at a time. With hop=True the host is marked as draining so pokes made by
        callbacks are held for the next pass.
        """
        lk = self._drain_lk
        if not lk.acquire(False):
            return
        try:
            if hop:
                self.draining = True
            API.ProcessCallbacks()
        except Exception:
            pass
        finally:
            if hop:
                self.draining = False
            lk.release()

    FRAME_MIN = 1.0 / 60
    NAP_MIN = 0.002

    def nap(self, began):
        """Return how long the loop sleeps before the next pass.

        Short (up to a frame) when input, a poke or a target request is waiting, else HOST_TICK. Also sets
        how far ahead the loop looks for a due client module.
        """
        now = time.time()
        if (self.poked or self.poke_keys or self.poke_user or (Kit.pending and self.config is not None)
                or Picker.due() or 0 <= now - self.input_at <= self.INPUT_FAST):
            self.look = self.EARLY
            return max(self.NAP_MIN, self.FRAME_MIN - max(0.0, now - began))
        self.look = self.LOOKAHEAD
        return HOST_TICK

    def _stop_free(self):
        """True when the API shows its stop is not yet scheduled, read by reflection (False when it cannot be
        read).
        """
        f = self._stop_fi
        if f is None:
            try:
                from System.Reflection import BindingFlags
                f = API.GetType().GetField("_onStopScheduled", BindingFlags.NonPublic | BindingFlags.Instance)
            except Exception:
                f = None
            f = self._stop_fi = f or False
        if f is False:
            return False
        try:
            return not f.GetValue(API)
        except Exception:
            return False

    def _drop_offs(self):
        """Apply the queued switch-offs without stopping anything, during shutdown."""
        q, self.off_q = self.off_q, []
        for e in q:
            s = dict.get(self.by_key, e[1])
            if s is None:
                continue
            if e[2] is not None:
                s.parts_on[e[2]] = False
            if e[2] is None or not s.parts_wanted():
                s.enabled = False
                self.held_on.discard(s.key)

    def _client_pass(self, poked=None):
        """The client-thread pass: runs the shared per-pass work and the client-tick modules.

        Drains callbacks, sweeps cached texts, builds the UI, samples health, ticks target jobs, ticks
        every due client module, then the UI and the alert tick. Errors of the pass are shown, not raised.
        """
        self.in_hop = True
        try:
            self.client_idles = 0
            if self._stop_free():
                self.drain(True)
            if self.stopping():
                return
            if poked is None:
                poked = self.pass_all
            keys = self.pass_keys
            offs = set(e[1] for e in self.off_q if e[2] is None) if self.off_q else ()
            if Kit._texts_sweep:
                Kit._prune_texts()
            self.ui_pending()
            self.fight_sample(time.time())
            if Picker.jobs:
                try:
                    Picker.tick()
                except Exception as ex:
                    self._tell("%s: target cursor error: %s" % (APP_NAME, ex))
            now = time.time()
            for s in self.client_run:
                if s.running and not s.busy and not s.pending_stop and s.key not in offs and (poked or s.key in keys
                        or now + self.EARLY >= s.next_due or s.next_due - now > self.CLOCK_BACK):
                    self.tick(s)
                    if self.stopping():
                        return
            self.ui_tick()
            if ALERTS.pending:
                try:
                    ALERTS.tick(time.time())
                except Exception as ex:
                    self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
        finally:
            self.in_hop = False

    def claim_cursor(self, key, seconds):
        """Claim the target cursor for module key for the given seconds."""
        self._claim_len = max(0.0, seconds)
        self.cursor_claim = (key, time.time() + self._claim_len)

    def release_cursor(self, key):
        """Release the cursor claim if key holds it."""
        if self.cursor_claim[0] == key:
            self.cursor_claim = (None, 0.0)

    def cursor_busy(self, key=None):
        """Return who is using the target cursor (pick for a target request, or the claiming module), else
        None.
        """
        if Picker.jobs:
            return "pick"
        owner, until = self.cursor_claim
        return owner if owner is not None and owner != key and \
            0 < until - time.time() <= self._claim_len + 0.05 else None

    def cursor_ok(self, key, kind="any"):
        """True when module key may use the cursor and the client has a target of the given kind waiting."""
        if self.cursor_busy(key) is not None:
            return False
        try:
            return bool(API.HasTarget(kind))
        except Exception:
            return False

    def harm_ok(self, serial, key, title, harmful=None, again="press again to confirm", odd=False, now=None):
        """Guard check before a harmful action on a target in a guard zone; True means go ahead.

        Outside a guard zone, or against a target that is not blue or green, it is True. Otherwise the
        player must press the same action again within a window after a pause (HARM_DOUBLE to HARM_SECS)
        to confirm, and a warning is shown in the system line and over the target. harmful is the cursor
        kind when already known; odd is for a target that should be a mobile.
        """
        if harmful is None:
            try:
                harmful = bool(API.HasTarget("harmful"))
            except Exception:
                harmful = False
        if not harmful:
            return True
        gz = self.guarded()
        if gz is False:
            return True
        try:
            m = API.FindMobile(serial) if serial else None
        except Exception:
            m = None
        noto = Kit.noto_name(m) if m is not None else ("odd" if odd and serial else "unknown")
        if noto not in HARM_NOTO:
            return True
        now = time.time() if now is None else now
        c = self.harm_conf
        if c[0] == key and c[1] == serial:
            age = now - c[2]
            if 0 <= age < HARM_DOUBLE:
                return False
            if 0 <= age <= HARM_SECS:
                self.harm_conf = (None, 0, 0.0)
                return True
        self.harm_conf = (key, serial, now)
        try:
            name = str(m.Name or "") if m is not None else ""
        except Exception:
            name = ""
        who = "%s is %s" % (name or "they", "green" if noto == "ally" else "blue") if m is not None else \
            "your target is not a mobile"
        API.SysMsg("%s: %s and you %s in a guard zone: %s." % (title, who, "are" if gz else "may be", again),
                   Kit.HUE_BAD)
        if m is not None:
            API.HeadMsg("* %s *" % again, serial, 0x22)
        return False

    def guard_hold(self):
        """Return guard when the player is in a guard zone, unknown when it is not known, else None."""
        try:
            g = GUARD.guarded()
        except Exception:
            g = None
        return "guard" if g is True else "unknown" if g is None else None

    def foe_near(self):
        """Return the name of a hostile mobile near the player, or None; cached for FOE_EVERY seconds.

        Looks at the mobiles within FOE_RANGE on the client thread; war-mode players of the listed
        notoriety also count. The player and renamable pets are skipped.
        """
        now = time.time()
        at, name = self.foe_seen
        if 0 <= at - now <= FOE_EVERY:
            return name

        def look():
            """Client-thread job that scans the mobiles and returns the first foe's name (or a question mark)."""
            try:
                me = int(self.me().Serial)
            except Exception:
                me = 0
            try:
                for m in self.mobiles(FOE_RANGE):
                    try:
                        if int(m.Serial) == me or m.IsRenamable:
                            continue
                        n = int(m.Notoriety)
                        if n in FOE_NOTO or (n in FOE_WAR_NOTO and m.InWarMode):
                            return str(m.Name or "") or "?"
                    except Exception:
                        continue
            except Exception:
                pass
            return None

        try:
            name = Kit.on_client(look)
        except Exception:
            name = None
        self.foe_seen = (now + FOE_EVERY, name)
        return name

    def fight_sample(self, now):
        """Note a drop in the player's hit points, so fight_hold knows the player was hurt just now; once per
        pass.
        """
        try:
            p = self.me()
            who = int(p.Serial)
            hits = int(p.Hits)
        except Exception:
            return
        if who != self.hurt_who:
            self.hurt_hp = None
            self.hurt_who = who
        if self.hurt_hp is not None and hits < self.hurt_hp:
            self.hurt_until = now + HURT_SECS
        self.hurt_hp = hits

    def fight_hold(self, now=None):
        """Return why a module should hold off now, or None: dead, war, hurt, attacked, foe, item (in hand)
        or alarm.

        Hurt and attacked last HURT_SECS seconds after the hit points fell or the journal said someone is
        attacking. A module uses this before it takes a free action. Client tick.
        """
        if now is None:
            now = time.time()
        dead = war = False
        try:
            p = self.me()
            dead = bool(p.IsDead)
            war = bool(p.InWarMode)
        except Exception:
            pass
        if dead:
            return "dead"
        if war:
            return "war"
        if self.attack_rd is None:
            self.attack_rd = Journal.reader()
        else:
            for ln in self.attack_rd.new():
                if ln.hue == ATTACK_HUE and str(ln.kind).upper() != "CLIENT" and Journal.ATTACK_RE.search(ln.text):
                    self.attacked_until = max(self.attacked_until, min(ln.at, now) + HURT_SECS)
        if 0 < self.hurt_until - now <= HURT_SECS:
            return "hurt"
        if 0 < self.attacked_until - now <= HURT_SECS:
            return "attacked"
        if self.foe_near():
            return "foe"
        if Kit.held_item():
            return "item"
        up = self.services.get("attention.up")
        if up is not None and safe(up):
            return "alarm"
        return None

    def me(self):
        """Return the player, wrapped to cache attribute reads; None when there is no player.

        Inside a client pass the same wrapper is reused for the whole pass.
        """
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
        """Return the list of (distance, mobile) for every mobile the client knows, cached for the pass.

        Outside a client pass the list is reused for MOB_AGE seconds. Each mobile is wrapped in a cache
        and
        its distance is read once. Inside a pass the wrappers are also indexed by serial for mobile().
        """
        if self._mob_pid == self.pass_id and (self.in_hop or time.time() - self._mob_at <= self.MOB_AGE):
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
        self._mob_pid, self._mob_list, self._mob_at = self.pass_id, out, time.time()
        return out

    def mobiles(self, distance=None):
        """Return the mobiles, or only those within distance tiles."""
        lst = self._mob_scan()
        if distance is None:
            return [e[1] for e in lst]
        return [m for d, m in lst if d <= distance]

    def mobile(self, serial):
        """Return the mobile with this serial (cached wrapper), or None when it is unknown."""
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
        """Return the items of the backpack (deep: the whole tree; else the top level), cached.

        The list is reused within a pass, or for max_age seconds when given. A copy is returned. When
        change tracking is on, the serials of the pack are remembered so item events can invalidate the
        cache.
        """
        k = bool(deep)
        now = time.time()
        ent = self._pack.get(k)
        if ent is not None and ((self.in_hop and ent[0] == self.pass_id)
                                or (max_age > 0 and 0 <= now - ent[1] <= max_age)):
            return list(ent[2])
        bp = API.Backpack
        lst = list((API.FindTypeAll(0xFFFFFFFF, bp) if k else API.ItemsInContainer(bp, False)) or []) if bp else []
        if bp and self._pack_hook["on"]:
            try:
                ks = set(int(i.Serial) for i in lst)
                ks.add(int(bp))
            except Exception:
                ks = set()
            if not k and len(self._pack_keys) <= self.PACK_CAP:
                ks |= self._pack_keys
            self._pack_keys = ks if len(ks) <= self.PACK_CAP else set([int(bp)])
        self._pack[k] = (self.pass_id if self.in_hop else -1, now, lst)
        return list(lst)

    def pack_dirty(self):
        """Forget the cached backpack lists."""
        self._pack.clear()

    def pack_ver(self):
        """Return a counter that goes up whenever the backpack changes; the first call starts the item
        tracking.
        """
        Kit.hook_once(self._pack_hook, "on", ("OnItemCreated", self._pack_fn), ("OnItemUpdated", self._pack_fn))
        return self._pack_v

    def _pack_event(self, *args):
        """Item created or updated event: when it is in the backpack, bump the counter and drop the cached
        lists.
        """
        keys = self._pack_keys
        for a in args:
            try:
                s, c = int(a.Serial), int(a.Container)
            except Exception:
                continue
            if c in keys or s in keys:
                self._pack_v += 1
                self._pack.clear()
            return

    def pick_target(self, timeout, on_done, owner=None):
        """Ask the player for a target without blocking; on_done(serial) runs on the client tick (see
        Picker.ask).
        """
        Picker.ask(timeout, on_done, owner)

    def ui_pending(self):
        """Run the window work queued by other threads (Kit.pending) on the client thread."""
        if self.ui_busy or self.config is None or not Kit.pending:
            return
        self.ui_busy = True
        try:
            while Kit.pending:
                lst, Kit.pending = Kit.pending, []
                for fn in lst:
                    safe(fn)
        finally:
            self.ui_busy = False

    def ui_tick(self):
        """Per-pass window work: settings window, shared alive stamp, hub, docks, grid, alerts, alert history,
        guard, what's new, the launcher and the safe-start window.

        Runs at UI_TICK; slows down to UI_IDLE after UI_IDLE_AFTER seconds without input, unless a mouse
        button is held or the layout is arranging. Errors are shown once, never raised.
        """
        self.ui_pending()
        if self.ui_busy or self.config is None:
            return
        self.ui_busy = True
        try:
            now = time.time()
            if now >= self.ui_next:
                boot = self.settled_at is None
                self.ui_next = now + (0.0 if boot else UI_TICK)
                self.config.poll()
                if not VA_ALONE and now >= self.alive_at:
                    self.alive_at = now + 1.0
                    API.SetSharedVar(ALIVE_KEY, str(now))
                if self.hub is not None:
                    self.hub.poll()
                self.dock_tick()
                SNAP.tick()
                if FADE.on:
                    try:
                        FADE.tick(now)
                    except Exception as ex:
                        self._tell("%s: fade error: %s%s" % (APP_NAME, ex, _error_where()))
                if now - self.input_at > UI_IDLE_AFTER and not (boot or SNAP.down or LAYOUT.arrange):
                    self.ui_next = now + UI_IDLE
                if self.grid is not None:
                    self.grid.tick()
                try:
                    ALERTS.tick(now)
                except Exception as ex:
                    self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
                try:
                    GUARD.tick(now)
                except Exception as ex:
                    self._tell("%s: guard-zone error: %s%s" % (APP_NAME, ex, _error_where()))
                if self.whats_new.g is not None:
                    self.whats_new.poll()
                if self.alert_log.g is not None:
                    self.alert_log.poll(now)
                if self.launcher is not None and self.launcher.g is not None:
                    self.launcher.poll(now)
                if self.ask_g is not None:
                    self.ask_poll()
        except Exception as ex:
            msg = "%s: settings window error: %s%s" % (APP_NAME, ex, _error_where())
            if not self.stopping():
                self._tell(msg)
        finally:
            self.ui_busy = False

    def load_prefs(self):
        """Load the saved settings and set each module's state.

        A module that is on by default is switched on once (the seen list). Modules saved as on but not
        loadable are kept in held_on so a missing file does not lose the choice. Held parts from an
        earlier load are forgotten here; tz_check holds them again when needed. The look and interface
        switches are applied (_apply_style).
        """
        prefs = self.prefs = Kit.codec_load(Kit.get_var(SETTINGS_KEY))
        on = [k for k in prefs.get("modules", "").split(",") if k]
        seen = set(k for k in prefs.get("seen", "").split(",") if k)
        was = prefs.get("seen", "")
        changed = self._migrate_parts(prefs, on, seen)
        held = self.held_on = set()
        self.held_parts = set()
        for s in self.slots:
            if s.default_on and s.key not in seen:
                on.append(s.key)
                seen.add(s.key)
                self._parts_fill(s)
            s.enabled = s.key in on and (s.api is not None or s.lazy is not None)
            if s.key in on and not s.enabled:
                held.add(s.key)
            if s.enabled:
                self._parts_fill(s)
        prefs["seen"] = ",".join(sorted(seen))
        self._apply_style()
        if prefs["seen"] != was or changed:
            self.save_prefs()

    def _migrate_parts(self, prefs, on, seen):
        """Work out which parts of each module are on from the saved lists; return True when something
        changed.

        Settings saved before parts existed are converted from the old module keys. A part that is new in
        this release and marked default is switched on once for a player who already used the module.
        """
        def by_module(key):
            """Return {module key: set of part keys} from a saved list of module.part items."""
            out = {}
            for item in prefs.get(key, "").split(","):
                if "." in item:
                    mk, pk = item.split(".", 1)
                    out.setdefault(mk, set()).add(pk)
            return out

        saved, saved_off = by_module("parts"), by_module("parts_off")
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
                for p in s.parts:
                    s.parts_on[p[0]] = p[0] in off
                continue
            if mine is not None and not fresh:
                for p in s.parts:
                    s.parts_on[p[0]] = p[0] in mine
                    if len(p) > 5 and p[5] and p[0] not in mine and p[3]:
                        new_seen = str(Kit.get_var("VirtueAssistant_new_parts", "") or "").split(",")
                        if p[0] not in new_seen:
                            if not VA_ALONE:
                                Kit.put_var("VirtueAssistant_new_parts", ",".join([x for x in new_seen if x] + [p[0]]))
                            s.parts_on[p[0]] = True
                            changed = True
            else:
                olds = [k for p in s.parts for k in p[4]]
                had_old = any(k in on_set for k in olds) or (s.key in on_set and not olds)
                for p in s.parts:
                    if p[4]:
                        s.parts_on[p[0]] = any(k in on_set for k in p[4])
                    elif mine is not None:
                        s.parts_on[p[0]] = p[0] in mine
                    else:
                        s.parts_on[p[0]] = bool(p[3]) and not had_old and s.key not in on_set
                if s.key in on_set:
                    self._parts_fill(s)
                changed = True
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
        """Read an integer preference; the default when missing or not a number."""
        try:
            return int(self.prefs.get(key, default))
        except Exception:
            return default

    def save_prefs(self, now=False):
        """Build the saved settings text from the module and part states and save it.

        Returns the text. Saves are spaced PREFS_EVERY seconds apart unless now is True; a skipped save
        sets prefs_due for prefs_flush. Does nothing while prefs_frozen (profile load). A module or part
        held off for this session (held_on, held_parts) is still saved as on, so the hold lasts only this
        run. The settings windows are given the values to keep their own copies.
        """
        if self.config is not None:
            self.config.box_hit = True
        if self.prefs_frozen:
            return None
        mods, parts, off = [], [], []
        for s in self.slots:
            if not s.enabled and s.key not in self.held_on:
                for p in s.parts:
                    if s.parts_on.get(p[0]) or (s.key, p[0]) in self.held_parts:
                        off.append("%s.%s" % (s.key, p[0]))
                continue
            mods.append(s.key)
            for p in s.parts:
                if s.parts_on.get(p[0]) or (s.key, p[0]) in self.held_parts:
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
        t = time.time()
        if not now and t < self.prefs_at:
            self.prefs_due = True
            return data
        self.prefs_due = False
        self.prefs_at = t + self.PREFS_EVERY
        Kit.put_var(SETTINGS_KEY, data)
        return data

    def prefs_flush(self, force=False):
        """Write a pending settings save when its time has come (or at once when forced)."""
        if self.prefs_due and not self.prefs_frozen and (force or time.time() >= self.prefs_at):
            self.save_prefs(True)

    def profile_job(self, req):
        """Do a profile or backup request on the main loop; a failure is shown in the system line.

        req is (kind, name): save, load or fav for profiles, backup or restore for backups. The settings
        window's profile list is refreshed afterwards, except after a load or restore, which rebuild the
        windows themselves.
        """
        kind, name = req
        try:
            getattr(self, "_profile_" + kind)(name)
        except Exception as ex:
            what = {"fav": "set the favourite profile", "backup": "save the backup",
                    "restore": "restore the backup"}.get(kind, kind + " the profile")
            Kit.say("couldn't %s (%s%s)." % (what, Tz.why(ex), _error_where()), Kit.HUE_BAD)
        if kind not in ("load", "restore") and self.config is not None and not self.stopping():
            self.config.refresh_profiles()
            if self.config.mode == "full":
                self.config.prof_redraw = False
                self.config.redraw()

    def _profile_save(self, name):
        """Save the current settings and every module's saved variables as a profile.

        Raises when the name is empty. A favourite profile is also set as the client's default for new
        characters.
        """
        name = PROFILES.clean(name)
        if not name:
            raise Exception("type a name for the profile in the box")
        Kit.say('saving profile "%s".' % name, Kit.HUE_INFO)
        data = self.save_prefs(True)
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
        """Load a profile: stop the modules, close the windows, replace the saved variables, then start
        again.

        The work is done by _reload; the result is reported in the system line.
        """
        if PROFILES.info(name) is None:
            raise Exception('there is no profile "%s"' % name)
        Kit.say('loading profile "%s".' % name, Kit.HUE_INFO)
        result = self._reload(lambda: PROFILES.apply(name, "fav" if name == PROFILES.favorite() else "pick"), name)
        PROFILES.report(name, "loaded", *result)

    def _reload(self, apply, sel=None):
        """Stop everything, run apply (which replaces the saved settings) and start everything again; shared
        by loading a profile and restoring a backup. Returns what apply returned.

        The pending settings and the alert history are written first, and saving is frozen meanwhile. The
        settings window and hub are rebuilt, key binds, alerts, guard memory and layout are reloaded, each
        module's api is built again, and every enabled module is started. The client check (tz_check) runs
        again after the settings are loaded, so a module the client cannot support stays held. sel is the
        profile to show picked in the settings window afterwards.
        """
        self.prefs_flush(True)
        self.prefs_frozen = True
        if ALERTS.log_due:
            ALERTS.save_log(time.time())
        try:
            if self.config is not None:
                safe(self.config.close)
            for s in self.slots:
                if s.running:
                    self._stop(s)
            if self.hub is not None:
                safe(self.hub.close)
            Kit._vars.clear()
            result = apply()
            for c in set(Binds.saved.values()) | Binds.hooked:
                Binds.unhook(c)
            Binds.saved.clear()
            Binds.loaded = False
            self._zone_was_d = None
            Kit._vars.clear()
            ALERTS.load()
            WhatsNew.seen_keys = None
            GUARD.saved = None
            Kit.read_screen()
            Binds.load()
            for s in self.slots:
                if s.api is not None and s.lazy is None and s.factory is not None:
                    try:
                        s.api = s.factory()
                        s.broken = None
                    except Exception as ex:
                        s.api, s.broken = None, str(ex) + _error_where()
                        Kit.say("couldn't load %s (%s)." % (s.title, s.broken), Kit.HUE_BAD)
            self.load_prefs()
            self.tz_check()
            LAYOUT.load()
        finally:
            self.prefs_frozen = False
            self.config = ConfigWindow(self)
            if sel is not None:
                self.config.prof_sel = sel
            self.config.open()
            self.hub = HubWindow(self)
            if self.grid is not None:
                safe(self.grid.show if self.pref_int("grid_on", 0) == 1 else self.grid.hide)
            for s in self.slots:
                if s.enabled:
                    self.start(s)
            Kit.note_screen()
        return result

    def backup_start(self):
        """Read the backup list for the Backups page, and ask for a backup when this version has not made
        one yet. Called once when start-up timing ends, and not in the alone mode.
        """
        try:
            self.backups.scan()
        except Exception:
            self.backups.items = []
        self.refresh_settings(BACKUP_PAGE)
        if Kit.get_var(BackupPage.VER_KEY) != APP_VERSION and self.profile_req is None:
            self.profile_req = ("backup", BackupPage.AUTO % APP_VERSION)

    def _profile_backup(self, why, keep=None):
        """Make a backup (request kind backup): save the history and settings, write the backup, remember
        that this version has its backup when it was the automatic one, refresh the list and say how many
        settings it holds. keep names a backup to spare from pruning.
        """
        if ALERTS.log_due:
            ALERTS.save_log(time.time())
        auto = why == BackupPage.AUTO % APP_VERSION
        name, n = self.backups.make(why, self.save_prefs(True), keep, self.early_backup if auto else None)
        if auto:
            Kit.put_var(BackupPage.VER_KEY, APP_VERSION)
            self.early_backup = None
        self.backups.scan()
        self.refresh_settings(BACKUP_PAGE)
        API.SysMsg("Backups: saved %s (%s)." % (Kit.count(n, "setting"), BackupPage.label(name)), Kit.HUE_GOOD)

    def _profile_restore(self, name):
        """Restore a backup (request kind restore): back the present settings up first (named so in the
        list), then put the picked backup back through _reload, refresh the list and report. Raises when
        the backup is empty. Says so when some settings were still saving.
        """
        va, lay = self.backups.read(name)
        if not va:
            raise Exception("that backup is empty")
        self._profile_backup("before restore", name)
        gone = list(BackupPage.snapshot(""))
        API.SysMsg("Backups: restoring %s." % BackupPage.label(name), Kit.HUE_INFO)
        ok = self._reload(lambda: BackupPage.apply(va, lay, gone))
        self.backups.scan()
        self.refresh_settings(BACKUP_PAGE)
        API.SysMsg("Backups: restored %s from %s." % (Kit.count(len(va), "setting"), BackupPage.label(name)),
                   Kit.HUE_GOOD)
        if not ok:
            API.SysMsg("Backups: some settings were still saving; restart Virtue Assistant if a module looks "
                       "unchanged.", Kit.HUE_BAD)

    def _profile_fav(self, name):
        """Make a profile the favourite, or take the star off when it already is; sets the client default
        too.
        """
        if PROFILES.info(name) is None:
            raise Exception("save a profile first, then star it")
        if PROFILES.favorite() == name:
            PROFILES.set_favorite("")
            safe(lambda: PROFILES.set_client_default(None))
            Kit.say('"%s" is no longer the favourite profile.' % name, Kit.HUE_INFO)
            return
        PROFILES.set_favorite(name)
        note = ""
        try:
            PROFILES.set_client_default(name)
        except Exception as ex:
            note = " (TazUO's default for new characters wasn't set: %s)" % Tz.why(ex)
        Kit.say('"%s" is the favourite profile: characters that haven\'t loaded another get it at start.%s'
                   % (name, note), Kit.HUE_GOOD)

    def hold(self, s, part=None):
        """Hold a module, or one part of it, off for this session without changing what is saved.

        With a part, the part is switched off and remembered in held_parts; the module itself is held only
        when no other part is wanted. A held module is disabled, remembered in held_on and stopped on the
        next pass (pending_stop). Does nothing for a part that is already off.
        """
        if part is not None:
            # Only a part that is on can be held; one the player left off stays as it is.
            if not s.parts_on.get(part):
                return
            s.parts_on[part] = False
            self.held_parts.add((s.key, part))
            # The module is held only when it has no other part wanted.
            if s.parts_wanted():
                return
        if s.enabled:
            s.enabled = False
            self.held_on.add(s.key)
            s.pending_stop = s.running

    TZ_GONE = "TazUO changed %s; %s %s off until the next Virtue Assistant."

    def tz_check(self):
        """Check the client against the Tz.NEED table and hold what cannot work, at start and after a profile load.

        Prints one journal line per missing client name, naming the modules or parts it affects, and holds
        them off for this session through hold. A key with an underscore is not a module or part: it is
        only a phrase for the journal line. Such keys are kept in tz_off, so code that has no fallback of
        its own (the TazUO settings check) can stop itself. Also makes the settings check run on the next
        pass. Runs on the script thread, after the settings are loaded.
        """
        self.tz_at = 0.0
        self.tz_off = set()
        for name, keys in safe(Tz.missing, ()):
            titles = []
            for key in keys:
                s, part = self.resolve(key)
                # Keys that name no module or part are skipped unless they hold an underscore.
                if s is None and "_" not in key:
                    continue
                t = key.replace("_", " ") if s is None else s.part_title(part)
                if t not in titles:
                    titles.append(t)
                if s is not None:
                    self.hold(s, part)
                else:
                    self.tz_off.add(key)
            if titles:
                Kit.say(self.TZ_GONE % (name, ", ".join(titles), "are" if len(titles) > 1 else "is"), Kit.HUE_BAD)

    TZ_KEY = "TazUO_settings_check"
    TZ_EVERY = 60.0
    TZ_LINE = "TazUO's \"%s\" is on; %s. Switch it off in %s."
    TZ_RULE = "it %s by itself, which this shard's rules don't allow"
    TZ_AL = "Legion Assistant > Agents > Auto Loot"
    TZ_SOON = 5.0
    # The four TazUO settings that act by themselves against the shard rules: auto loot (R2), auto loot of
    # human corpses (R6, looting other players' corpses flags the looter criminal), the scavenger (R2) and
    # automatic doors (R4, Auto Doors stays removed). Each row is the Profile property, the label TazUO's
    # own window shows, the rule in plain words and where the switch is.
    TZ_SETS = (("EnableAutoLoot", "Enable Auto Loot", TZ_RULE % "loots", TZ_AL),
               ("AutoLootHumanCorpses", "Auto Loot Human Corpses",
                "it loots players' corpses by itself, which can flag you criminal", TZ_AL),
               ("EnableScavenger", "Enable Scavenger", TZ_RULE % "picks up items",
                "Legion Assistant > Agents > Scavenger"))

    def tz_warn(self):
        """Warn once per session about each TazUO setting that breaks the shard rules; never change one.

        Runs from run_due on the script thread: at start, after a profile load and then every TZ_EVERY
        seconds, so a setting switched on later still gets its one line. Silent while a module runs alone,
        when the player ticked the tz_quiet main setting (System Stats page) or when tz_check found a client
        name this check reads missing. With no TazUO profile yet it looks again after TZ_SOON seconds.
        """
        self.tz_at = time.time() + self.TZ_EVERY
        if self.alone is not None or self.TZ_KEY in self.tz_off or self.pref_int("tz_quiet", 0) == 1:
            return
        on = safe(self.tz_on, ())
        if on is None:
            self.tz_at = time.time() + self.TZ_SOON
            return
        for name, label, why, where in self.TZ_SETS:
            if name in on and name not in self.tz_told:
                self.tz_told.add(name)
                Kit.say(self.TZ_LINE % (label, why, where), Kit.HUE_BAD)

    def tz_on(self):
        """Read which of the TZ_SETS settings are on in TazUO's current profile, by reflection.

        Returns a set of property names, or None while no profile is loaded. Human corpses count only while
        auto loot itself is on. The scavenger counts only once its list has loaded and holds entries, since
        TazUO ships it switched on with an empty list. A failed scavenger read leaves only that one out.
        """
        cur = Tz.get(None, "CurrentProfile", Tz.T("ClassicUO.Configuration.ProfileManager"))
        if cur is None:
            return None
        on = set(sp[0] for sp in self.TZ_SETS if bool(Tz.get(cur, sp[0])))
        if "EnableAutoLoot" not in on:
            on.discard("AutoLootHumanCorpses")
        if "EnableScavenger" in on:
            on.discard("EnableScavenger")
            with Kit.quiet:
                sm = Tz.get(None, "Instance", Tz.T("ClassicUO.Game.Managers.ScavengerManager"))
                if bool(Tz.get(sm, "IsLoaded")) and int(Tz.get(sm, "ScavengerEntries").Count) > 0:
                    on.add("EnableScavenger")
        return on

    def mark_start(self):
        """Set the per-character start mark and return whether it was already set.

        A mark found set means the last start never finished. The key is kept out of profiles (OWN_VARS).
        """
        was = Kit.get_var(START_KEY) == "1"
        Kit.put_var(START_KEY, "1")
        self.marked = True
        return was

    def unmark(self, stop=False):
        """Clear the start mark once start-up is judged finished.

        With stop True (the script is ending) the mark is cleared only when the player asked for the stop
        (API.StopRequested); a stop after a crash leaves it set. It is never cleared while the safe-start
        window is waiting for an answer.
        """
        if self.marked and self.ask_g is None and (not stop or safe(lambda: bool(API.StopRequested), False)):
            self.marked = False
            Kit.put_var(START_KEY, "")

    def start_on(self):
        """Queue every enabled module to be loaded and started by the main loop.

        While start-up has not settled, it notes when queuing began (for the settle cap) and plans the
        layout first. The layout owner is queued first.
        """
        if self.settled_at is None:
            self.settle_from = self.settle_from or time.time()
            safe(LAYOUT.plan)
        self.load_jobs.extend(sorted((s for s in self.slots if s.enabled and s not in self.load_jobs),
                                     key=lambda s: s.key != LAYOUT_OWNER))

    SAFE_ASK = "Virtue Assistant didn't finish starting last time. Start with every module off?"
    SAFE_DONE = "every module is off for now; tick them on one at a time on the Modules tab (%s)."
    SAFE_BUTTONS = (("normal", Kit.ART_PLAY, "Start normally", "Turn on the modules you had on"),
                    ("safe", Kit.ART_PLAY, "Start safely", "Keep every module off for now"))

    def ask_open(self):
        """Open the safe-start window and return whether it is showing.

        Returns False when the settings window does not exist yet. The window is built on the client tick
        under its own key-bind scope.
        """
        if self.config is None:
            return False
        with Kit.quiet:
            Kit.on_client(lambda: Binds.scoped("va.safe", self._ask_build))
        return self.ask_g is not None

    def _ask_build(self):
        """Build the small SAFE START window: the question and the Start normally and Start safely buttons.

        Runs on the client tick. The window is centred horizontally and sits a third of the way down the
        screen.
        """
        M, W = Kit.MARGIN, 420
        lines = Kit.wrap(self.SAFE_ASK, W - 2 * M - 24)
        n = len(lines)
        h = 48 + 20 * n
        yb = M + 30 + Kit.GAP
        H = yb + h + M
        self.ask_store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, "SAFE START", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.add_section(g, M, yb, W - 2 * M, h)
        for i, line in enumerate(lines):
            Kit.add_label(g, line, M + 12, yb + 8 + 20 * i, Kit.HUE_TEXT)
        Kit.buttons(g, self.ask_store, M + 12, yb + 14 + 20 * n, self.SAFE_BUTTONS)
        sw, sh = Kit.screen()
        Kit.place(g, max(0, ((sw or 1024) - W) // 2), max(0, ((sh or 768) - H) // 3), W, H)
        Kit.add_front(g)
        self.ask_g = g

    def ask_poll(self):
        """Poll the safe-start window and act on a click or on its being closed.

        Start safely holds every module for this session, and the journal lists the ones that were on so
        the player can tick them on again one at a time on the Modules tab. Start normally, or closing the
        window, keeps the saved modules. Either way the enabled modules are then queued to load. Called
        from ui_tick.
        """
        st = self.ask_store
        safe_on = Kit.was_clicked(st, "safe")
        if not (safe_on or Kit.was_clicked(st, "normal") or not Kit.is_open(self.ask_g)):
            return
        g, self.ask_g = self.ask_g, None
        Kit.dispose(g)
        if safe_on:
            names = [s.title for s in self.slots if s.enabled]
            for s in self.slots:
                self.hold(s)
            Kit.say(self.SAFE_DONE % (", ".join(names) or "none"), Kit.HUE_INFO)
        self.start_on()
        self.poke()

    def run(self):
        """Start the full suite: find the client, load settings, build the windows, then run the main loop.

        Sets the start mark first and checks the client for missing members (tz_check). Takes the early
        backup snapshot before the settings are loaded. The windows built on the client thread (the main
        window, Ultima Tracker, the start line, What's new) are made in one hop, _front_hop. Modules are
        queued to load at once, unless the last start left its mark set, in which case the safe-start
        window decides. Window build errors are shown, not fatal.
        """
        ask = self.mark_start()
        Client.find()
        if Client.mouse is None:
            Kit.say("no client mouse timer; double-clicks use the client's own event.", Kit.HUE_INFO)
        self.early_backup = BackupPage.early()
        self.load_prefs()
        ALERTS.load()
        self.tz_check()
        Kit.read_screen()
        LAYOUT.load()
        SNAP.on_drop(LAYOUT.dropped)
        API.OnStop(self.shutdown)
        self.grid = Grid(self)
        self.launcher = Launcher(self)
        self.services["launcher.open"] = self.launcher.toggle
        why = None
        try:
            self.config = ConfigWindow(self)
            self.config.refresh_profiles()
        except Exception as ex:
            why = ex
        safe(self.whats_new.due)
        self._front_hop(ask, why)
        # Last start-up phase before the loop; the time after it is reported as the first build.
        self.boot_mark("main window")
        self.loop()

    def _front_hop(self, ask, why):
        """Build the first windows in one hop to the client thread; if no hop is possible, build them here.

        Raises the error that happened on the client thread. ask and why are the safe-start flag and the
        error from building the main window object, passed on to _front.
        """
        how, v = Client.on_main_ex(lambda: self._front(ask, why))
        if how == "no":
            self._front(ask, why)
        elif how == "err" and Client.exc is not None:
            raise Client.exc

    def _front(self, ask, why):
        """Open the main window and the other first windows, then start the modules, on the client thread.

        why is an error raised while the main window object was made; it is reported like one raised
        while opening the window, and a gear button is built so the player can still reach the settings.
        Makes the Ultima Tracker window, shows the grid when on, says which modules are on, and publishes
        the alive mark. Binds and the modules start unless the safe-start window asks first. Opens the
        What's new window last.
        """
        try:
            if why is not None:
                raise why
            self.config.open(True)
        except Exception as ex:
            self._tell("%s: couldn't build the window: %s%s" % (APP_NAME, ex, _error_where()))
            if self.config is None:
                self.config = safe(lambda: ConfigWindow(self))
            if self.config is not None:
                safe(lambda: self.config.build_gear(self.config.gx, self.config.gy))
        try:
            self.hub = HubWindow(self)
        except Exception as ex:
            self._tell("%s: couldn't make the Ultima Tracker window: %s%s" % (APP_NAME, ex, _error_where()))
        if self.pref_int("grid_on", 0) == 1:
            safe(self.grid.show)
        names = [s.title for s in self.slots if s.enabled]
        API.SysMsg("%s %s running. %s" % (APP_NAME, APP_VERSION, ("On: " + ", ".join(names) + ".") if names else
                   "Tick a module on the Modules tab."), Kit.HUE_GOOD)
        API.SetSharedVar(ALIVE_KEY, str(time.time()))
        Binds.load()
        if not ask or not self.ask_open():
            self.start_on()
        Kit.note_screen()
        try:
            self.whats_new.open()
        except Exception as ex:
            self._tell("%s: couldn't make the What's new window: %s" % (APP_NAME, ex))

    def run_alone(self, s):
        """Run one module on its own, without the rest of the suite (stand-alone mode).

        Does nothing but tell the player when the suite is already running. The settings are not saved
        (frozen) and the module gets a small settings page of its own.
        """
        if self.suite_alive():
            API.SysMsg("%s: %s is running; use %s there." % (s.title, APP_NAME, s.title), Kit.HUE_BAD)
            return
        self.alone, self.prefs_frozen = s, True
        Client.find()
        self.load_prefs()
        Kit.read_screen()
        API.OnStop(self.shutdown)
        self.config = AlonePage(s)
        self.hub = safe(lambda: HubWindow(self))
        on = Kit.get_var(ALONE_PARTS % s.key, "")
        if s.parts and on:
            s.parts_on = dict((p[0], p[0] in on.split(",")) for p in s.parts)
        API.SysMsg("%s: running alone, without the rest of %s." % (s.title, APP_NAME), Kit.HUE_GOOD)
        Binds.load()
        self.enable(s.key)
        self.loop()

    def loop(self):
        """The main loop: drain callbacks, run what is due and sleep until the next pass, until the script
        stops.

        Errors of a pass are shown and the loop goes on. shutdown always runs at the end.
        """
        try:
            while not self.stopping() and (self.alone is None or self.alone.enabled):
                began = time.time()
                self.drain()
                try:
                    self.run_due()
                    if self.settled_at is None:
                        self.settle_tick(time.time())
                except Exception as ex:
                    if self.stopping():
                        break
                    self._tell("%s: main loop error: %s%s" % (APP_NAME, ex, _error_where()))
                API.Pause(self.nap(began))
        finally:
            self.shutdown()

    def shutdown(self):
        """Stop everything in order: modules, windows, layout, saved settings, then print the stopped line.

        Safe to call twice (it runs once); also registered with the client's stop hook. The start mark is
        cleared first, and only for a stop the player asked for. The alert history is saved with the
        banner closing.
        """
        if self.shut:
            return
        self.shut = self.quitting = True
        safe(Picker.drop)
        self.unmark(True)
        if self.off_q:
            self._drop_offs()
        if not VA_ALONE:
            safe(lambda: Kit.on_client(LAYOUT.game_view_restore))
            safe(lambda: LAYOUT.set_arrange(False, tell=False))
            safe(lambda: Kit.on_client(LAYOUT._tabs_off))
            safe(LAYOUT.situ_park)
            safe(lambda: Kit.on_client(lambda: [cw.free() for cw in list(ClientWin.found.values()) + [
                LAYOUT.journal_held] if cw is not None]))
        if self.config is not None:
            safe(lambda: self.save_prefs(True))
            safe(self.config.close)
        else:
            safe(lambda: self.prefs_flush(True))
        for s in reversed(self.slots):
            if s.running:
                try:
                    self._stop(s)
                except Exception:
                    s.running = False
        self._refresh_active()
        if self.hub is not None:
            safe(self.hub.close)
        if self.launcher is not None:
            safe(self.launcher.close)
        for fn in (self.alert_log.close, ALERTS.close, self.whats_new.close, GUARD.store, Kit.note_screen,
                   lambda: Kit.dispose(self.ask_g), lambda: Kit.unhook(None)):
            safe(fn)
        if self.grid is not None:
            safe(self.grid.hide)
        safe(lambda: API.SysMsg("%s stopped." % APP_NAME, Kit.HUE_INFO))


class PartSet(object):
    """Runs a module's optional parts (small features the player ticks on or off) inside one module slot.

    Each part is a factory returning a hooks dict (start, tick, stop, thread_tick, thread_wanted,
    interval, build_config, config_height, poll_config, config_closed). The set starts and stops parts
    to match what the slot wants, ticks the running ones on their own intervals, and stacks their
    config sections in the module's settings page. Hooks of the whole set come from hooks().
    """
    OFF_LINE = "%s is off: tick it under PARTS to see its settings."

    def __init__(self, key, title, parts, shared=None):
        """Builds the set for module key from parts, a list of (part key, factory, interval, owner).
        The optional owner names the part's hook owner (default module.part); shared holds extra module
        hooks (tick, stop, thread_tick, thread_wanted) run alongside the set's own.
        """
        self.key = key
        self.specs = [[sp[0], sp[1], float(sp[2]), sp[3] if len(sp) > 3 else None] for sp in parts]
        self._owner = {sp[0]: sp[3] or ("%s.%s" % (key, sp[0])) for sp in self.specs}
        self._iv = {sp[0]: sp[2] for sp in self.specs}
        self._fns = {}
        self.api = {}
        self.running = []
        self.due = {}
        self.thread_due = {}
        # want holds a part list that arrived while a part call was running; it is applied after that call.
        self.want = self._slot = None
        self.busy = 0
        self.stopping = False
        self.load = {}
        self.shared = shared or {}

    def slot(self):
        """Returns the module slot this set belongs to, found once in HOST.by_key and cached."""
        if self._slot is None:
            self._slot = dict.get(HOST.by_key, self.key)
        return self._slot

    def owner(self, pk):
        """Returns the hook owner name for part pk, used to release its hooks, cursor and pickers."""
        return self._owner.get(pk, pk)

    def part_api(self, pk):
        """Returns the hooks dict of part pk, building it once from its factory (None if pk is unknown).
        A factory that raises is reported to the player and counts as an empty part.
        Also caches the part's interval and thread flags so the tick loop needs no dict lookups per call.
        """
        api = self.api.get(pk)
        if api is None:
            for sp in self.specs:
                if sp[0] == pk:
                    # The current part and owner are set while the factory runs so hooks it registers are attributed.
                    HOST.cur_part, HOST.cur_owner = pk, self.owner(pk)
                    try:
                        api = sp[1]()
                    except Exception as ex:
                        api = {}
                        s = self.slot()
                        if s is not None:
                            HOST.report(s, ex, s.part_title(pk), pk)
                    finally:
                        HOST.cur_part = HOST.cur_owner = None
                    self.api[pk] = api
                    self._fns[pk] = ((api.get("interval"), "thread_tick" in api,
                                      api.get("thread_wanted")) if api else (None, False, None))
                    break
        return api

    def _call(self, pk, hook, *args):
        """Calls hook of part pk with args and returns its result, or None if it has no such hook.
        Errors are reported against the module (unless the script is stopping) and never propagate.
        The part is marked current while it runs, and busy stops reconcile from changing the list mid-call.
        """
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
        """Copies the running part keys to the slot so the module and its settings page see them."""
        s = self.slot()
        if s is not None:
            s.parts_running = set(self.running)

    def start_part(self, pk):
        """Starts part pk: builds its hooks, marks it running, makes it due now and calls its start hook.

        Does nothing if it already runs or the set is stopping; a part with no hooks is dropped. Gives the
        part a load record and shares the set's records with the slot as part_load.
        """
        if pk in self.running or self.stopping:
            return
        api = self.part_api(pk)
        if not api:
            self.api.pop(pk, None)
            return
        if pk not in self.load:
            self.load[pk] = [0.0, 0.0, 0.0]
        self.running.append(pk)
        self._sync_slot()
        self.due[pk] = 0.0
        self.thread_due[pk] = False
        s = self.slot()
        if s is not None:
            s.next_due = 0.0
            s.part_load = self.load
        self._call(pk, "start")

    def stop_part(self, pk):
        """Stops part pk: drops its pickers, releases its cursor, calls its stop hook and unhooks its owner."""
        if pk not in self.running:
            return
        self.running.remove(pk)
        self._sync_slot()
        owner = self.owner(pk)
        Picker.drop(owner)
        HOST.release_cursor(owner)
        self._call(pk, "stop")
        Kit.unhook(owner)

    def wanted(self):
        """Returns the set of part keys the player has ticked for this module."""
        s = self.slot()
        return set(s.parts_wanted()) if s is not None else set()

    def reconcile(self, want=None):
        """Starts and stops parts so the running list matches want (default: the ticked parts).
        If a part call is in progress the change is only remembered and applied after it finishes.
        Parts start in declared order and stop in reverse.
        """
        if want is None:
            want = self.wanted()
        if self.busy:
            self.want = set(want)
            return
        self.want = None
        for sp in self.specs:
            pk = sp[0]
            if pk in want and pk not in self.running:
                self.start_part(pk)
        for pk in list(reversed(self.running)):
            if pk not in want:
                self.stop_part(pk)

    def _start(self):
        """Start hook of the set: clears the stopping flag and starts the wanted parts."""
        self.stopping = False
        self.reconcile()

    # Placeholder for a part without hooks: no interval, no thread work.
    _NOFN = (None, False, None)

    def _tick(self):
        """Client tick: runs the tick hook of every part that is due, then applies any waiting part change.

        A part is due on its schedule, when the pass was poked, when a pass key names it, when the clock
        ran back, or slightly early (Host.EARLY) so ticks do not slip a whole pass. Each call is timed
        and added to the part's load record.
        """
        now = time.time()
        poked = HOST.pass_poked
        running = self.running
        due = self.due
        load = self.load
        keys = HOST.pass_keys if self.key in HOST.pass_keys else None
        for pk in list(running):
            if pk not in running:
                continue
            d = due.get(pk, 0.0)
            if poked or now + Host.EARLY >= d or d - now > Host.CLOCK_BACK or (
                    keys is not None and self.key + "." + pk in keys):
                # One pair of time.time() calls times the part; the end time also anchors the next due time.
                t0 = time.time()
                self._call(pk, "tick")
                t1 = time.time()
                Host.busy_add(load[pk], (t1 - t0) * 1000.0, t1)
                nxt, has_thread, want = self._fns.get(pk, self._NOFN)
                due[pk] = t1 + Host._ask(nxt, self._iv.get(pk, 0.1))
                self.thread_due[pk] = has_thread and Host._ask(want, True, bool)
        if self.want is not None and not self.busy:
            self.reconcile(self.want)

    def _thread_wanted(self):
        """Tells the host whether any part (or a waiting part change) needs the script thread."""
        if self.want is not None:
            return True
        td = self.thread_due
        for pk in self.running:
            if td.get(pk):
                return True
        return False

    def _thread_tick(self):
        """Script thread: runs thread_tick for each part that asked for it, timing each call into the part's
        load record, then applies a waiting part change.
        """
        for pk in list(self.running):
            if self.thread_due.get(pk) and pk in self.running:
                self.thread_due[pk] = False
                t0 = time.time()
                self._call(pk, "thread_tick")
                t1 = time.time()
                Host.busy_add(self.load[pk], (t1 - t0) * 1000.0, t1)
        if self.want is not None and not self.busy:
            self.reconcile(self.want)

    def _interval(self):
        """Returns the seconds until the earliest part is due, between 0.002 and 30 (1.0 with none running)."""
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
        """Stop hook of the set: marks it stopping and stops every part, last started first."""
        self.stopping = True
        self.want = None
        for pk in list(reversed(self.running)):
            self.stop_part(pk)

    HEAD_H = 28

    def _config_height(self, w):
        """Returns the height of the stacked part sections for width w: a header per part plus the content
        height of each running part that has one. At least 40.
        """
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
        """Draws the stacked part sections into gump g at x, y with width w.
        A running part gets its title in capitals and its own build_config content; a part that is off
        shows a one-line hint to tick it.
        """
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
                Kit.add_label(g, Kit.fit(self.OFF_LINE % title, w - 24), x + 12, y + 7, Kit.HUE_INFO)
            elif s is not None and s.part(pk) and len(s.part(pk)) > 2 and s.part(pk)[2]:
                tx = x + 8 + Kit.text_w(title.upper()) + 14
                Kit.add_label(g, Kit.fit(s.part(pk)[2], max(20, x + w - 12 - tx)), tx, y + 6, Kit.HUE_INFO)
            y += self.HEAD_H
            if on and api and api.get("build_config"):
                y += Kit.GAP
                hh = self._call(pk, "config_height", w) if api.get("config_height") else 0
                self._call(pk, "build_config", g, x, y, w)
                y += max(0, int(hh or 0))

    def _poll_config(self):
        """Settings page poll: lets each running part poll its config controls."""
        for pk in list(self.running):
            self._call(pk, "poll_config")

    def _config_closed(self):
        """Settings page closed: tells each part that has a config_closed hook."""
        for pk in self.specs:
            api = self.api.get(pk[0])
            if api and api.get("config_closed"):
                self._call(pk[0], "config_closed")

    def hooks(self):
        """Returns the hooks dict that registers this set with the host.
        With shared hooks, the shared tick, stop, thread_tick and thread_wanted are wrapped so the set and
        the module code both run (stop always runs both).
        """
        h = {"start": self._start, "tick": self._tick, "stop": self._stop, "client_tick": True,
             "thread_tick": self._thread_tick, "thread_wanted": self._thread_wanted, "interval": self._interval,
             "parts": self.reconcile, "config_height": self._config_height, "build_config": self._build_config,
             "poll_config": self._poll_config, "config_closed": self._config_closed}
        sh = self.shared
        if not sh:
            return h

        def tick():
            """Runs the set's tick and then the shared module tick."""
            self._tick()
            sh["tick"]()

        def stop():
            """Stops the set, then always runs the shared stop."""
            try:
                self._stop()
            finally:
                sh["stop"]()

        def thread_tick():
            """Runs the set's thread tick and then the shared one."""
            self._thread_tick()
            sh["thread_tick"]()

        def thread_wanted():
            """True when the shared code or any part wants the script thread."""
            return bool(sh["thread_wanted"]()) or self._thread_wanted()

        wrap = {"tick": tick, "stop": stop, "thread_tick": thread_tick, "thread_wanted": thread_wanted}
        h.update((k, wrap[k]) for k in sh)
        return h


class Tz(object):
    """Reflection helpers for reading and writing TazUO internals that Legion's API does not expose.

    Lookups are cached in _found so repeated calls cost one dictionary hit. NEED lists what Virtue
    Assistant reads this way, so a client that lacks one of them can be found at start.
    """
    _types = {}
    _MISS = object()
    # Each row is (client type, member names separated by spaces, modules or parts that need it). An
    # empty member list asks only for the type. A part is written module.part; a key with an
    # underscore is only text for the journal line. A client member read by reflection needs a row.
    NEED = (("LegionScripting.LegionAPI", "_onStopScheduled", "early_event_handling"),
        ("LegionScripting.LegionAPI", "World", "actionbar meters social"),
        ("Game.GameActions", "", "actionbar social skills.window"), ("Game.GameActions", "DropItem", "inventory.bags"),
        ("Game.GameActions", "Equip QueueEquipSwap", "inventory.paperdoll"),
        ("Game.Managers.UIManager", "Gumps", "actionbar grimoire interface hud inventory.bags skills.window social"),
        ("Game.Managers.UIManager", "ContainerScale", "inventory.bags"),
        ("Game.Managers.UIManager", "KeyboardFocusControl _gumpsStructureVersion SystemChat", "interface"),
        ("Game.Managers.UIManager", "MakeTopMostGump", "hud skills.window"),
        ("Game.Managers.UIManager", "Gumps MakeTopMostGump _gumpsStructureVersion TopMostControl", "start-up_order"),
        ("Game.Managers.UIManager", "Add", "skills.window"),
        ("Game.Managers.UIManager", "IsMouseOverWorld", "worldmap.pings"),
        ("Game.Managers.MacroManager", "GetAllMacros SetMacroToExecute Update FindMacro", "actionbar"),
        ("Game.Managers.MacroObject", "Items", "actionbar"), ("Game.Managers.MacroObject", "", "social"),
        ("Common.Enums.MacroType", "", "actionbar social"), ("Common.Enums.MacroSubType", "", "actionbar social"),
        ("LegionScripting.LegionScripting", "LoadedScripts", "actionbar"),
        ("Input.Keyboard", "KeyDownEvent KeyUpEvent", "actionbar"),
        ("Input.Mouse", "CancelDoubleClick", "inventory.bags"),
        ("Input.Mouse", "Position MClickPosition MButtonPressed", "worldmap.pings"),
        ("Game.World", "Macros", "actionbar social"), ("Game.World", "Instance Get TargetManager", "hud.frames"),
        ("Game.World", "TargetManager", "meters"),
        ("Game.World", "Instance Player SkillsGroupManager", "skills.window"), ("Game.World", "Party Player", "social"),
        ("Game.Managers.TargetManager", "LastAttack", "hud.frames meters"),
        ("Client", "Game", "hud.frames inventory.bags inventory.paperdoll social"),
        ("GameController", "UO", "hud.frames inventory.bags inventory.paperdoll social"),
        ("UltimaOnline", "Animations FileManager", "hud.frames"),
        ("UltimaOnline", "GameCursor", "inventory.bags inventory.paperdoll"), ("UltimaOnline", "World", "social"),
        ("Game.GameCursor", "ItemHold", "inventory.bags"),
        ("Game.ItemHold", "Enabled IsFixedPosition Serial Graphic Hue Container MouseOffset DisplayedGraphic",
         "inventory.bags"), ("Configuration.ProfileManager", "CurrentProfile",
         "hud.frames inventory.bags inventory.storage TazUO_settings_check"),
        ("Configuration.Profile", "EnableAutoLoot AutoLootHumanCorpses EnableScavenger", "TazUO_settings_check"),
        ("Game.Managers.ScavengerManager", "Instance IsLoaded ScavengerEntries", "TazUO_settings_check"),
        ("Configuration.Profile", "OpenHealthBarForLastAttack", "hud.frames"),
        ("Configuration.Profile", "Username ServerName", "inventory.storage"),
        ("Game.UI.Gumps.BaseHealthBarGump", "LastAttackBar", "hud.frames"),
        ("Game.GameObjects.Mobile", "GetGroupForAnimation", "hud.frames"),
        ("Game.GameObjects.Mobile", "IsCovered", "inventory.paperdoll"), ("Renderer.SpriteInfo", "", "hud.frames"),
        ("Time", "Ticks", "hud.timers"),
        ("Game.UI.Controls.Control", "SetHitTestOffset _bounds Location", "inventory.bags"),
        ("Game.UI.Controls.Control", "_bounds Location", "interface inventory.paperdoll"),
        ("Game.UI.Gumps.ContainerGump", "_data _gumpPicContainer _hitBox", "inventory.bags"),
        ("Assets.TileDataLoader", "_staticData", "inventory.bags"), ("Game.Data.Layer", "", "inventory.paperdoll"),
        ("Game.UI.Controls.PaperDollInteractable", "GetAnimID", "inventory.paperdoll"),
        ("Game.Managers.EventSink", "OnEntityDamage", "meters"), ("Game.GameObjects.Entity", "", "meters"),
        ("Game.Data.Lock", "", "skills.window"), ("Game.Data.Skill", "Lock", "skills.window"),
        ("Game.GameObjects.PlayerMobile", "Skills", "skills.window"),
        ("Game.GameObjects.PlayerMobile", "Serial", "social"),
        ("Game.Managers.SkillsGroupManager", "Groups", "skills.window"),
        ("Game.Managers.SkillsGroup", "", "skills.window"),
        ("Game.UI.Gumps.SkillButtonGump", "SkillID", "skills.window"),
        ("Game.Managers.FriendsListManager", "Instance", "social"),
        ("Game.Managers.PartyManager", "Leader Inviter CanLoot Members", "social"),
        ("Game.UI.Gumps.IgnoreManagerGump", "", "social"), ("Network.AsyncNetClient", "Socket", "social sysstats"),
        ("Network.AsyncNetClient", "Statistics", "sysstats"), ("Network.NetClientExt", "Send_PartyDecline", "social"),
        ("CUOEnviroment", "CurrentRefreshRate", "sysstats"), ("CUOEnviroment", "ExecutablePath", "worldmap"),
        ("Game.Managers.EnhancedMap.EnhancedMapManager", "Instance IsConnected Config Reconnect _client",
         "worldmap.pings"), ("Game.SelectedObject", "Object", "worldmap.pings"),
        ("Game.UI.Gumps.WorldViewportGump", "Instance ResizeGameWindow SetGameWindowPosition", "interface"),
        ("Game.UI.Gumps.SystemChatControl", "IsDisposed ParentX ParentY TextBoxControl", "interface"),
        ("Game.UI.Controls.TTFTextInputField", "EnterPressed", "launcher_Enter_key"),)

    @staticmethod
    def missing():
        """Return the client types and members that are missing, with the keys each one affects.

        The result is a sorted list of (name, keys), or an empty tuple when the client types cannot be
        reached at all, so a script that is not inside the client holds nothing. Each row is looked up
        once per client process; the result is kept in the measured client data. No API calls are made.
        Runs on the script thread at start.
        """
        got = Kit._measure.get("tz_missing")
        if got is None:
            if Client._type("ClassicUO.Client") is None:
                return ()
            fl = Tz._flags(True) | Tz._flags(False)
            out = {}
            for tn, names, keys in Tz.NEED:
                t = Client._type("ClassicUO." + tn)
                short = tn.split(".")[-1]
                for gone in [short] if t is None else [short + "." + n for n in names.split() if not Tz.has(t, n, fl)]:
                    out.setdefault(gone, []).extend(keys.split())
            got = Kit._measure["tz_missing"] = tuple((k, tuple(v)) for k, v in sorted(out.items()))
        return [(k, list(v)) for k, v in got]

    @staticmethod
    def has(t, name, fl):
        """Return True when type t, or one of its base types, declares a member called name.

        fl are the binding flags from _flags.
        """
        while t is not None:
            if t.GetMember(name, fl).Length:
                return True
            t = t.BaseType
        return False

    @staticmethod
    def T(name):
        """Returns the .NET type called name, cached; raises a plain-English error when this TazUO build lacks it."""
        t = Tz._types.get(name)
        if t is None:
            t = Client._type(name)
            if t is None:
                raise Exception("this TazUO build has no %s" % name.split(".")[-1])
            Tz._types[name] = t
        return t

    @staticmethod
    def get(obj, name, t=None):
        """Reads field or property name from obj (or the static type t when obj is None); raises if unreadable."""
        v = Typing._get(obj, name, t, Tz._MISS)
        if v is Tz._MISS:
            raise Exception("can't read %s" % name)
        return v

    @staticmethod
    def _flags(static):
        """Returns reflection binding flags for public and private members declared on the type itself,
        static or instance.
        """
        from System.Reflection import BindingFlags
        return BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly | \
            (BindingFlags.Static if static else BindingFlags.Instance)

    _found = {}

    @staticmethod
    def put(obj, name, value, t=None):
        """Writes value to property or field name of obj (static when obj is None), searching base types.
        The member found is cached. Raises if nothing writable has that name.
        """
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
    def call(obj, name, args=(), t=None, opt=False):
        """Calls method name on obj (static when obj is None) with args and returns its result.
        A method is picked by name and argument count (generic methods are skipped); with opt, trailing
        optional parameters may be left out and are filled with their defaults. Cached per signature.
        """
        import System
        t = t if t is not None else obj.GetType()
        args = list(args)
        n = len(args)
        ck = ("call", t, name, n, obj is None, opt)
        hit = Tz._found.get(ck, Tz._MISS)
        if hit is Tz._MISS:
            hit = None
            flags = Tz._flags(obj is None)
            tt = t
            while tt is not None and hit is None:
                for mm in tt.GetMethods(flags):
                    if mm.Name != name or mm.IsGenericMethodDefinition:
                        continue
                    ps = list(mm.GetParameters())
                    if len(ps) == n or opt and len(ps) > n and all(p.IsOptional for p in ps[n:]):
                        hit = (mm, [p.DefaultValue for p in ps[n:]])
                        break
                tt = tt.BaseType
            Tz._found[ck] = hit
        if hit is None:
            raise Exception("can't call %s.%s" % (t.Name, name))
        return hit[0].Invoke(obj, System.Array[object](args + hit[1]))

    @staticmethod
    def load_json(path, typeinfo, t):
        """Loads a TazUO JSON settings file at path through the client's own ConfigurationResolver,
        using typeinfo for the type t. Raises a plain-English error if that loader is missing.
        """
        import System
        cr = Tz.T("ClassicUO.Configuration.ConfigurationResolver")
        for m in cr.GetMethods(Tz._flags(True)):
            if m.Name == "Load" and m.IsGenericMethodDefinition and m.GetParameters().Length == 2:
                g = m.MakeGenericMethod(System.Array[System.Type]([t]))
                return g.Invoke(None, System.Array[object]([path, typeinfo]))
        raise Exception("can't read TazUO settings files")

    @staticmethod
    def copy_props(src, dst, skip=()):
        """Copies every writable public property from src to dst (same type), for restoring client options.
        Skips names in skip, serial properties, JsonIgnore ones and read-only ones; converts enums and
        numbers when a direct set fails. Returns (changed, failed) counts.
        """
        import System
        from System.Reflection import BindingFlags
        changed = failed = 0
        for p in dst.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance):
            name = str(p.Name)
            if name in skip or name.endswith("Serial"):
                continue
            if not p.CanRead or not p.CanWrite or p.GetIndexParameters().Length or p.GetSetMethod(False) is None:
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
                except Exception:
                    pt = p.PropertyType
                    v = System.Enum.ToObject(pt, v) if pt.IsEnum else System.Convert.ChangeType(v, pt)
                    p.SetValue(dst, v, None)
                changed += 1
            except Exception:
                failed += 1
        return changed, failed

    @staticmethod
    def windows(type_names):
        """Returns the open client windows whose type name is in type_names."""
        gumps = Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))
        return [g for g in list(gumps) if str(g.GetType().Name) in type_names]

    @staticmethod
    def why(ex):
        """Returns the innermost error message of a .NET or Python exception as plain text."""
        e = getattr(ex, "clsException", None) or ex
        while getattr(e, "InnerException", None) is not None:
            e = e.InnerException
        return str(getattr(e, "Message", None) or e)


class Profiles(object):
    """Saves and restores the player's profiles: a named copy of every Virtue Assistant setting of this
    character plus the TazUO client's own settings files and the unified bag layout.

    A profile is a folder under the profile directory holding profile.txt (name, saved stamp, character,
    version), va_vars.txt (tab separated settings, escaped), unified_bag.cfg and a tazuo folder of
    client files. Saving writes to a .saving folder first and swaps it in, so a failed save keeps the
    old copy. The start mark is never carried, nor the alert history, the seen list or the backup
    version, which belong to one character. The quiet time of the alerts is never changed by a profile.
    """
    # Client option names that belong to the character or session and are never copied between characters.
    PROFILE_SKIP = ("Username", "ServerName", "CharacterName", "Serial", "LastLoaded", "FollowingTarget")
    # Bag layout lines that belong to this character only; they are kept when a profile is applied.
    BAG_OWN = ("slot.", "trapsel=", "trapextra=")
    # Settings keys that end in a serial are tied to one item or character and are not saved.
    SERIAL_KEY = re.compile(r"_[0-9A-Fa-f]{8}$")
    # Prefixes of every setting key that Virtue Assistant owns and a profile may carry.
    VA_KEYS = ("ActionBar_", "Attention_", "BandageAgent", "Character_", "CombatBars_", "CorpseRun_", "EMPings.",
               "Grimoire_", "Harvest_", "Interface_", "Layout_", "Lookout_", "Meters_", "Mongotchi_", "Pets_",
               "PropertyButler_", "Restock_", "SkillBags_", "Skills_", "Social_", "SpellTimers_", "StorageIndex_",
               "SwingTimer_", "swingtimer_", "SystemStats_", "TrapHL_", "TreasureHunter_", "UltimaTracker_",
               "UnifiedBag_", "UnitFrames_", "VirtueAssistant_", "WorldMap_", "ReagentPrices_")
    # Settings that hold this character's own lists and history; they stay out of profiles.
    OWN_VARS = ("CorpseRun_corpse", "SkillBags_rules", "SkillBags_done", "UnitFrames_tracked", "Social_names",
                "TreasureHunter_maps", "Restock_settings", "PropertyButler_visits", "SpellTimers_active",
                "VirtueAssistant_starting", "VirtueAssistant_new_seen", "VirtueAssistant_alert_log",
                "VirtueAssistant_backup_ver", "ReagentPrices_book")
    # A value no real setting holds, used to tell a missing setting from an empty one.
    MISSING = "\x01VA-missing"

    def __init__(self):
        """Sets the profile directory path under the data folder."""
        self.base = os.path.join(Kit.data_dir(), PROFILE_DIR)

    @staticmethod
    def _read(path):
        """Returns the text of the file at path, or None if the path is empty or unreadable."""
        return Kit.read_safe(path, None) if path else None

    @staticmethod
    def _write(path, text):
        """Writes text to the file at path through the safe writer."""
        Kit.write_safe(path, text)

    @staticmethod
    def _esc(s):
        """Escapes backslash, tab, carriage return and newline so a value fits one tab separated line."""
        return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r") .replace("\n", "\\n")

    @staticmethod
    def _unesc(s):
        """Reverses _esc."""
        un = {"t": "\t", "r": "\r", "n": "\n"}
        return re.sub(r"\\(.)", lambda m: un.get(m.group(1), m.group(1)), s, flags=re.S)

    # Windows device names that cannot be folder names.
    RESERVED = frozenset(["CON", "PRN", "AUX", "NUL", "CLOCK$"] + ["COM%d" % i for i in range(1, 10)]
                         + ["LPT%d" % i for i in range(1, 10)])

    @staticmethod
    def clean(name):
        """Returns name made safe for a folder: bad characters become dashes, edges trimmed, length capped.
        Returns an empty string for a reserved Windows device name.
        """
        name = re.sub(r'[\\/:*?"<>|\t\r\n]+', "-", str(name or ""))
        name = name.strip(" .-")[:PROFILE_NAME_MAX].strip(" .-")
        # The .old and .saving endings belong to the save swap, so a player's name may not end that way.
        if name.lower().endswith((".old", ".saving")):
            dot = name.rfind(".")
            name = (name[:dot] + "-" + name[dot + 1:])[:PROFILE_NAME_MAX]
        if name.split(".")[0].upper() in Profiles.RESERVED:
            return ""
        return name

    def folder(self, name):
        """Returns the folder path of profile name."""
        return os.path.join(self.base, name)

    def names(self):
        """Returns the saved profile names, sorted without regard to case. A folder counts only if it has a
        profile.txt and is not a .saving or .old leftover.
        """
        import System
        out = []
        with Kit.quiet:
            if System.IO.Directory.Exists(self.base):
                for d in System.IO.Directory.GetDirectories(self.base):
                    n = str(System.IO.Path.GetFileName(d))
                    if n.endswith(".saving") or n.endswith(".old"):
                        continue
                    if System.IO.File.Exists(os.path.join(str(d), "profile.txt")):
                        out.append(n)
        return sorted(out, key=lambda s: s.lower())

    def info(self, name):
        """Returns the profile.txt fields of profile name as a dict, or None if it does not exist."""
        text = self._read(os.path.join(self.folder(name), "profile.txt")) if name else None
        if text is None:
            return None
        pairs = (line.split("=", 1) for line in text.splitlines() if "=" in line)
        return dict((k.strip(), v.strip()) for k, v in pairs)

    def favorite(self):
        """Returns the favourite profile name (applied on login), or an empty string if none or it is gone."""
        name = (self._read(os.path.join(self.base, "_favorite.txt")) or "").strip()
        return name if name and self.info(name) is not None else ""

    def set_favorite(self, name):
        """Stores name as the favourite profile (empty clears it)."""
        if not os.path.isdir(self.base):
            os.makedirs(self.base)
        self._write(os.path.join(self.base, "_favorite.txt"), name or "")

    def state(self):
        """Returns (mode, name, stamp): which profile this character last had applied and how, kept in the
        character's own settings so startup can tell whether it is already current.
        """
        p = Kit.get_var(PROFILE_STATE_KEY).split("|")
        return (p[0], p[1], p[2]) if len(p) >= 3 else ("", "", "")

    def set_state(self, mode, name, stamp):
        """Records the applied profile: mode ("pick" or "fav"), its name and its saved stamp."""
        Kit.put_var(PROFILE_STATE_KEY, "%s|%s|%s" % (mode, name, stamp))

    # Settings that only describe the current session and are never saved in a profile.
    SESSION_VARS = ("Layout_gameview_own", "Layout_gameview_lock", "Layout_zone_was", "VirtueAssistant_reclaim_undo")

    def keep_var(self, key, extra=()):
        """True if setting key belongs in a profile: a Virtue Assistant key that is not the profile state,
        serial based, session only, or one of the character's own lists. extra adds module prefixes.
        """
        if key == PROFILE_STATE_KEY or self.SERIAL_KEY.search(key) or key in self.SESSION_VARS:
            return False
        if key in self.OWN_VARS or key.startswith(("Grimoire_H_", "Layout_client_locked_")):
            return False
        return key.startswith(self.VA_KEYS + tuple(extra))

    def profile_vars(self, found):
        """Returns the part of found (a dict of all settings) that goes into a profile.
        Modules with a saved settings key count as Virtue Assistant keys. The alert settings are kept
        without their quiet time entry.
        """
        mods = set(s.key for s in HOST.slots)
        extra = tuple(set(k[:-8] for k in found if k.endswith("_settings") and k[:-9].lower() in mods))
        va = dict((k, v) for k, v in found.items() if self.keep_var(k, extra))
        if Alerts.KEY in va:
            va[Alerts.KEY] = Alerts.with_quiet(va[Alerts.KEY], "")
        return va

    @staticmethod
    def char_vars():
        """Returns every persistent variable of the current character as a dict of text.
        Reflection is needed because the API reads one variable at a time. Raises if the list cannot be read.
        """
        import System
        t = Tz.T("ClassicUO.LegionScripting.PersistentVars")
        for m in t.GetMethods():
            if m.Name == "GetAllVars" and m.GetParameters().Length == 1:
                scope = System.Enum.Parse(m.GetParameters()[0].ParameterType, "Char")
                d = m.Invoke(None, System.Array[object]([scope]))
                return dict((str(kv.Key), "" if kv.Value is None else str(kv.Value)) for kv in d)
        raise Exception("can't list this character's saved settings")

    @staticmethod
    def parse_vars(text):
        """Reads the text of a va_vars.txt (one setting per line, key and value separated by a tab, both
        escaped) into a dict. Lines without a tab and empty keys are skipped.
        """
        out = {}
        for line in text.split("\n"):
            if "\t" in line:
                k, v = line.split("\t", 1)
                k = Profiles._unesc(k)
                if k:
                    out[k] = Profiles._unesc(v.rstrip("\r"))
        return out

    def read_vars(self, name):
        """Reads the saved settings of profile name from its va_vars.txt and returns those that belong in it."""
        return self.profile_vars(self.parse_vars(self._read(os.path.join(self.folder(name), "va_vars.txt")) or ""))

    def wait_vars(self, wanted, timeout=5.0):
        """Waits up to timeout seconds until every setting in wanted reads back with its new value.
        Returns True if all arrived. Runs on the script thread (it pauses between polls).
        """
        left = dict(wanted)
        end = time.time() + timeout
        while left and not API.StopRequested:
            for k in list(left):
                # Writes to persistent variables land asynchronously, so each one is polled until it matches.
                got = safe(lambda: API.GetPersistentVar(k, self.MISSING, API.PersistentVar.Char))
                if got is not None and str(got) == left[k]:
                    del left[k]
            if not left or time.time() > end:
                break
            API.Pause(0.05)
        return not left

    @staticmethod
    def bag_path():
        """Returns the path of this character's unified bag file, or None while the player is unknown."""
        serial = safe(lambda: int(API.Player.Serial), 0)
        if not serial:
            return None
        return Kit.data_path("_unified_bag_%d.cfg" % serial)

    @staticmethod
    def client_files():
        """Returns the table of TazUO settings files a profile carries, one row per file:
        (file name, player wording, flush function, reload function).
        Flush makes the client write the file out before it is copied; reload makes it read a copied-in
        file again. Runs on the client thread (reflection into the client).
        """
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
            """Clears the auto loot manager's loaded flag and loads its file again."""
            a = inst(MGR + "AutoLootManager")
            Tz.put(a, "_loaded", False)
            Tz.call(a, "Load")

        def infobar_reload():
            """Reloads the info bar file and resets any open info bar windows."""
            Tz.call(Tz.get(world(), "InfoBars"), "Load")
            for gump in Tz.windows(("InfoBarGump",)):
                safe(lambda: Tz.call(gump, "ResetItems"))

        def buysell_flush():
            """Unloads and loads the buy and sell agent so its in-memory lists are written and re-read."""
            static(MGR + "BuySellAgent", "Unload")
            static(MGR + "BuySellAgent", "Load")

        return (("cooldownbars.json", "cooldown bars", lambda: Tz.call(current(CFG + "CooldownBarsConfig"), "Save"),
             lambda: static(CFG + "CooldownBarsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_highlights.json", "grid highlights", lambda: Tz.call(current(CFG + "GridHighlightsConfig"), "Save"),
             lambda: static(CFG + "GridHighlightsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_container_bands.json", "container bands",
             lambda: Tz.call(current(CFG + "GridContainerBandsConfig"), "Save"),
             lambda: static(CFG + "GridContainerBandsConfig", "LoadForProfile", (path(),))),
            ("screen_decorations.json", "screen effects", lambda: Tz.call(current(SD), "Save"),
             lambda: static(SD, "LoadForProfile", (path(),))), ("tooltip_overrides.json", "tooltip overrides",
             lambda: Tz.call(Tz.get(current(CFG + "TooltipOverridesConfig"), "Char"), "Save"),
             lambda: static(CFG + "TooltipOverridesConfig", "Load")), ("nameoverhead.xml", "name plates",
             lambda: static(MGR + "NameOverHeadManager", "Save"), lambda: static(MGR + "NameOverHeadManager", "Load")),
            ("infobar.xml", "info bar", lambda: Tz.call(Tz.get(world(), "InfoBars"), "Save"), infobar_reload),
            ("AutoLoot.json", "auto loot", lambda: Tz.call(inst(MGR + "AutoLootManager"), "Save"), autoloot_reload),
            ("OrganizerConfig.json", "organizer", lambda: Tz.call(inst(MGR + "OrganizerAgent"), "Save"),
             lambda: static(MGR + "OrganizerAgent", "Load")), ("journal_filters.json", "journal filter",
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Save", (False,)),
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Load")),
            ("BuyAgentConfig.json", "auto buy", buysell_flush, lambda: static(MGR + "BuySellAgent", "Load")),
            ("SellAgentConfig.json", "auto sell", lambda: None, lambda: static(MGR + "BuySellAgent", "Load")),
            ("macros.xml", "macros", lambda: Tz.call(Tz.get(world(), "Macros"), "Save", (None,)),
             lambda: Tz.call(Tz.get(world(), "Macros"), "Load")), ("hotkeys.json", "hotkeys",
             lambda: static(MGR + "Hotkeys.HotKeys", "Save"), lambda: static(MGR + "Hotkeys.HotKeys", "Load")),)

    @staticmethod
    def _profile_type():
        """Returns the client's ProfileManager type and the current profile object."""
        PM = Tz.T("ClassicUO.Configuration.ProfileManager")
        return PM, Tz.get(None, "CurrentProfile", PM)

    def _client_export(self, dest):
        """Client thread: asks the client to save its options and every settings file, and lists which files
        to copy into dest. Returns (saved, failed, pairs) where pairs holds (source, target, wording).
        """
        import System
        F = System.IO.File
        PM, cur = self._profile_type()
        src = str(Tz.get(None, "ProfilePath", PM))
        saved, failed, pairs = [], [], []
        try:
            Tz.call(cur, "Save")
            pairs.append((os.path.join(src, "profile.json"), os.path.join(dest, "profile.json"), "options"))
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
        """Loads the client options file at path and copies its values onto the current profile.
        Identity options (PROFILE_SKIP) are kept. Saves the profile, then re-applies vsync and the
        container scale so they take effect at once. Returns (changed, failed) counts.
        """
        import System
        PM, cur = self._profile_type()
        ctx = Tz.get(None, "DefaultToUse", Tz.T("ClassicUO.Configuration.ProfileJsonContext"))
        src = Tz.load_json(path, Tz.get(ctx, "Profile"), cur.GetType())
        if src is None:
            raise Exception("its profile.json can't be read")
        changed, failed = Tz.copy_props(src, cur, self.PROFILE_SKIP)
        Tz.call(cur, "Save")
        safe(lambda: Tz.call(Tz.get(None, "Game", Tz.T("ClassicUO.Client")), "SetVSync", (Tz.get(cur, "EnableVSync"),)))
        safe(lambda: Tz.put(None, "ContainerScale", System.Single(int(Tz.get(cur, "ContainersScale")) / 100.0),
                            Tz.T("ClassicUO.Game.Managers.UIManager")))
        return changed, failed

    def _client_import(self, srcdir):
        """Client thread: puts the saved client files from srcdir into the live client profile.
        Closes the client's options windows first so they cannot overwrite the result. Each file is
        copied and reloaded; if that fails the previous file is restored. Returns (done, failed) lists.
        """
        import System
        F = System.IO.File
        done, failed = [], []
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
                    failed.append(Kit.count(bad, "option"))
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
                with Kit.quiet:
                    if old is not None:
                        F.WriteAllBytes(target, old)
                    elif F.Exists(target):
                        F.Delete(target)
                    reload()
        return done, failed

    def set_client_default(self, name):
        """Makes profile name the client's default for new characters by copying its options and macros over
        default.json and macros.xml, or restores the originals when name is empty.
        The first change keeps a .va-backup copy (or a .va-none marker when there was no file) so it can
        be undone.
        """
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
                if not F.Exists(bak) and not F.Exists(none):
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

    @staticmethod
    def _on_client(fn):
        """Runs fn on the client thread and returns its (done, failed) result.
        A failure or an unreachable client becomes a failed entry instead of an error.
        """
        try:
            res = Kit.on_client(fn, fallback=False)
        except Exception as ex:
            res = ([], ["TazUO settings (%s)" % Tz.why(ex)])
        return res or ([], ["TazUO settings (couldn't reach the client)"])

    def save(self, name, prefs_data):
        """Saves the current settings as profile name and returns (stamp, count, saved, failed).
        prefs_data is the module window layout text stored with it.
        Writes everything into a .saving folder, swaps it in over the old one, and reads the result back;
        raises if it does not match what was meant to be saved.
        """
        import System
        D = System.IO.Directory
        final = self.folder(name)
        tmp, old = final + ".saving", final + ".old"
        if D.Exists(tmp):
            D.Delete(tmp, True)
        D.CreateDirectory(os.path.join(tmp, "tazuo"))
        stamp = "%d" % int(time.time())
        va = self.profile_vars(self.char_vars())
        va[SETTINGS_KEY] = prefs_data
        self._write(os.path.join(tmp, "va_vars.txt"),
                    "".join("%s\t%s\n" % (self._esc(k), self._esc(va[k])) for k in sorted(va)))
        bag = self.bag_path()
        text = self._read(bag) if bag else None
        # The bag layout is saved without the character-only lines.
        if text is not None:
            lay = [l for l in text.splitlines() if l.strip() and not l.startswith(self.BAG_OWN)]
            self._write(os.path.join(tmp, "unified_bag.cfg"), "\n".join(lay))
        res = self._on_client(lambda: self._client_export(os.path.join(tmp, "tazuo")))
        saved, failed = list(res[0]), list(res[1])
        F = System.IO.File
        for src, dst, what in (res[2] if len(res) > 2 else ()):
            try:
                F.Copy(src, dst, True)
                saved.append(what)
            except Exception as ex:
                failed.append("%s (%s)" % (what, Tz.why(ex)))
        who = safe(lambda: str(API.Player.Name), "") or ""
        self._write(os.path.join(tmp, "profile.txt"),
                    "name=%s\nsaved=%s\nfrom=%s\nversion=%s\n" % (name, stamp, who, APP_VERSION))
        # Swap in the new folder; if the move fails the old copy is moved back so nothing is lost.
        if D.Exists(old):
            D.Delete(old, True)
        if D.Exists(final):
            D.Move(final, old)
        try:
            D.Move(tmp, final)
        except Exception:
            if D.Exists(old) and not D.Exists(final):
                safe(lambda: D.Move(old, final))
            raise
        if D.Exists(old):
            D.Delete(old, True)
        if self.read_vars(name) != va or (self.info(name) or {}).get("saved") != stamp:
            raise Exception("the saved copy doesn't read back the same; try again")
        return stamp, len(va), saved, failed

    def apply(self, name, mode):
        """Applies profile name: writes its settings, waits for them to land, restores the bag layout (keeping
        this character's own lines) and loads the client files. mode is "pick" or "fav" for the state record.
        The character's own quiet time for the alerts is kept. Returns (count, all_landed, done, failed).
        Script thread.
        """
        info = self.info(name)
        if info is None:
            raise Exception('there is no profile "%s"' % name)
        folder = self.folder(name)
        va = self.read_vars(name)
        if Alerts.KEY in va:
            va[Alerts.KEY] = Alerts.with_quiet(va[Alerts.KEY], Kit.get_var(Alerts.KEY))
        for k in sorted(va):
            Kit.put_var(k, va[k])
        ok = self.wait_vars(va)
        lay = self._read(os.path.join(folder, "unified_bag.cfg"))
        bag = self.bag_path()
        cur = Kit.read_safe(bag) if lay is not None and bag else None
        if cur is not None:
            own = [l for l in cur.splitlines() if l.startswith(self.BAG_OWN)]
            self._write(bag, "\n".join([l for l in lay.splitlines() if l.strip()] + own))
        done, failed = self._on_client(lambda: self._client_import(os.path.join(folder, "tazuo")))
        if lay is not None and bag and cur is None:
            failed = list(failed) + ["bag layout (couldn't read the bag file)"]
        self.set_state(mode, name, info.get("saved", ""))
        return len(va), ok, done, failed

    def report(self, name, verb, n, ok, done, failed):
        """Tells the player in the game's chat what was done by a save or apply, listing anything that failed."""
        Kit.say('profile "%s" %s: %d Virtue Assistant settings; TazUO: %s.'
                   % (name, verb, n, ", ".join(done) or "nothing"), Kit.HUE_GOOD)
        if not ok:
            Kit.say("some settings were still saving; restart Virtue Assistant if a module looks unchanged.",
                    Kit.HUE_BAD)
        if failed:
            Kit.say("not done: %s." % "; ".join(failed), Kit.HUE_BAD)

    def startup(self):
        """On login, applies the favourite profile unless this character already has it, or has a different
        one the player chose by hand.
        """
        fav = self.favorite()
        if not fav:
            return
        stamp = (self.info(fav) or {}).get("saved", "")
        mode, name, had = self.state()
        if mode == "pick" and name != fav and self.info(name) is not None:
            return
        if name == fav and had == stamp:
            return
        self.report(fav, "(the favourite) put on this character", *self.apply(fav, "fav"))


class ConfigWindow(object):
    """The main Virtue Assistant window: a title row, the profile row and a body with a Modules tab (tick
    modules and their parts on or off) and a Settings tab (one page per module, or a search over every
    option).

    It is drawn as a modern gump scaled by the player's chosen percentage, laid out in columns that
    fill the window, and can fold to a small gear icon or dock into the action bar. Everything is
    rebuilt on the client thread; poll() runs on the script thread and reads clicks and ticked boxes
    that the draw code stored. The action bar talks to it through shared variables (LINK_*), and the
    Quick Launcher (Launcher) reads its option index.
    """
    W = 640
    GEAR = 52
    TABS = (("modules", "Modules"), ("settings", "Settings"))
    DOCK_KEY = "va"
    # Shared variable names of the link to the action bar: commands in, state out, its alive stamp.
    LINK_CMD = "VirtueAssistant_cmd"
    LINK_STATE = "VirtueAssistant_state"
    LINK_ALIVE = "ActionBar_alive"
    LINK_STALE = 10.0
    LINK_ENABLE = "VirtueAssistant_enable"

    def __init__(self, host):
        """Reads the saved place, tab, page, size and scale from the host's preferences, sets up the module
        search, option search and option index state, and clears the shared command variables left over
        from an earlier run. The window itself opens in open().
        """
        self.host = host
        self.g = self.mode = self._pp_key = self.shown_page = self.request = self.request_tab = None
        self.lag_lbl = self.dirty = self.gear_pos = self.body = self.head = None
        self.link_state = self.prof_sel = self.prof_cache = self.prof_shown = None
        self.loading = self.stale_page = self.search_tb = self.search_text = None
        self.gear_clicked = self.closing = self.docked = self.prof_stale = self.prof_redraw = False
        self.box_hit = self.redraw_req = self.search_focus = self.find_prof = False
        self.gear_look = self.lag_next = self.gear_moved = self.link_next = self.box_next = self.search_at = 0.0
        self.resize_at = 0.0
        self.store = ({}, {})
        self.seen = {}
        self._pp_gate = [0.0]
        self._fld_gate = [0.0]
        self._fld_due = True
        self.opt_search = ""
        self.opt_index = {}
        self.opt_ver = 0
        self.opt_open = False
        self.opt_wait = self.opt_mark = self.opt_lbl = self.opt_drawn = self.fresh_view = None
        self.opt_hits = (None, None)
        self.hit_keys = []
        self.why, self.why_log, self.stale_log = None, [], []
        self.from_xy = None
        # Saved positions are pulled back on screen if the screen is smaller than when they were saved.
        self.x, self.y = Kit.adapt(host.pref_int("cfg_x", 140), host.pref_int("cfg_y", 80), self.W, self.MIN_H)
        self.gx, self.gy = Kit.adapt(host.pref_int("gear_x", self.x),
                                     host.pref_int("gear_y", self.y), self.GEAR, self.GEAR)
        self.minimized = host.pref_int("cfg_min", 0) == 1 or host.dock_wanted(self.DOCK_KEY)
        self.tab = host.prefs.get("cfg_tab", "modules")
        if self.tab not in ("modules", "settings"):
            self.tab = "modules"
        self.page = host.prefs.get("cfg_page", "")
        SNAP.enabled = host.pref_int("snap", 1) == 1
        self.reported = set()
        self.page_keys = []
        self.box_list = []
        self.part_boxes = []
        self.fold_keys = []
        self.measured = {}
        self.mod_search = ""
        self._prof_reset()
        sh = Kit.screen()[1]
        self.lim_w = max(self.W, host.pref_int("cfg_w", self.W))
        self.lim_h = max(self.MIN_H, host.pref_int("cfg_h", (sh - 60) if sh > 400 else 1000))
        self.scale = max(50, min(200, host.pref_int("cfg_scale", 100))) / 100.0
        self.size = (0, 0)
        for var in (self.LINK_CMD, self.LINK_ENABLE):
            API.RemoveSharedVar(var)

    # Pixel boxes that draw the favourite star: (x, y, width, height) in a 16 by 16 square.
    STAR_RECTS = ((7, 1, 1, 2), (6, 3, 3, 3), (1, 6, 13, 2), (4, 8, 7, 3), (3, 11, 3, 3), (9, 11, 3, 3))
    STAR_ON, STAR_OFF = (240, 192, 64), (106, 106, 106)
    PROF_H = 34
    PROF_DD_W = 196

    def _prof_reset(self):
        """Forgets the profile row's controls so the next build starts them fresh."""
        self.prof_dd = self.prof_dd_args = self.prof_tb = self.prof_seen = None
        self.prof_names = []
        self.prof_fav = ""
        self.prof_stars = []
        self.prof_star_hit = False

    @staticmethod
    def _cap_w(art, text):
        """Returns the width of a button made of art plus a caption."""
        return (Kit.pic_size(art[0])[0] or 30) + 5 + Kit.text_w(text)

    def refresh_profiles(self):
        """Reads the profile names, favourite and applied profile into the cache (or the error that stopped
        it). If the visible row would now differ, asks for a redraw.
        """
        self.prof_stale = False
        P = PROFILES
        try:
            data = ("ok", P.names(), P.favorite(), P.state()[1])
        except Exception as ex:
            data = ("err", ex)
        self.prof_cache = data
        if self.prof_shown is not None and self._prof_key(data) != self.prof_shown and self.mode == "full":
            self.prof_redraw = True

    @staticmethod
    def _prof_key(data):
        """Returns a key that changes whenever the profile row would need redrawing."""
        return ("ok", data[1], data[2]) if data[0] == "ok" else ("err", str(data[1]))

    def _build_profiles(self, g, x, y, w):
        """Draws the profile row into g at x, y with width w: the favourite star, Load and Save buttons and
        the name box. When the title row has no room for the Find button it is added at the end of this
        row instead (find_prof). The drop down itself is added later by _add_profile_list so it sits on top.
        Raises the stored error if the profiles could not be read; the caller shows it as a message.
        """
        data = self.prof_cache
        if data is None:
            self.refresh_profiles()
            data = self.prof_cache
        self.prof_shown = self._prof_key(data)
        self.prof_stale = True
        if data[0] != "ok":
            raise data[1]
        names, fav, cur = data[1], data[2], data[3]
        sel = self.prof_sel if self.prof_sel in names else None
        if sel is None:
            sel = cur if cur in names else (fav if fav in names else (names[0] if names else None))
        self.prof_sel, self.prof_names, self.prof_fav = sel, names, fav
        H = self.PROF_H
        Kit.add_section(g, x, y, w, H)
        xs = x + 12 + self.PROF_DD_W + 10
        ys = y + (H - 16) // 2
        off = "#%02X%02X%02X" % self.STAR_OFF
        boxes = [Kit.add_box(g, xs + rx, ys + ry, rw, rh, 1.0, off) for rx, ry, rw, rh in self.STAR_RECTS]
        self.prof_stars = [b for b in boxes if b is not None]
        Kit.catcher(g, xs - 3, ys - 3, 22, 22, self._star_click,
                    "Favourite: characters that haven't loaded another profile get it (click again to clear)")
        xb = xs + 28
        for key, art, cap, gap, tip in (("p_load", Kit.ART_PLAY, "Load", 14, "Load the picked profile here"),
                ("p_save", Kit.ART_OK, "Save", 6, "Save this setup under the typed name, or over the picked profile")):
            Kit.art_button(g, self.store, key, art, xb, y + 6, cap, tip)
            xb += self._cap_w(art, cap) + gap
        Kit.add_label(g, "as", xb, y + 9, Kit.HUE_INFO)
        xf = xb + Kit.text_w("as") + 8
        fw = (Kit.pic_size(Kit.ART_PAGE[0])[0] or 30) + 8 if self.find_prof else 0
        self.prof_tb = Kit.with_tip(Kit.add_textbox(g, "", xf, y + 6, max(60, x + w - 12 - xf - fw), numbers=False),
                                    "New profile name (empty: save over the picked one)")
        items = [n + ("  (favourite)" if n == fav else "") for n in names] or ["(no profiles saved yet)"]
        self.prof_dd_args = (x + 12, y + 7, self.PROF_DD_W, items, names.index(sel) if sel in names else 0)

    def _add_profile_list(self, g):
        """Adds the profile drop down on top of the other controls and keeps the player's pick when the
        window is rebuilt.
        """
        if self.prof_dd_args is None:
            return
        old = self.prof_dd
        dx, dy, dw, items, idx = self.prof_dd_args
        if old is not None:
            i = Kit.dd_index(old, None)
            Kit.dispose(old)
            if i is not None and 0 <= i < len(self.prof_names):
                self.prof_sel = self.prof_names[i]
        if self.prof_sel in self.prof_names:
            idx = self.prof_names.index(self.prof_sel)
        dd = G.CreateDropDown(dw, items, idx)
        dd.SetPos(dx, dy)
        g.Add(dd)
        self.prof_dd = Kit.with_tip(dd, "Saved profiles: pick one to load or save over")
        self.prof_seen = idx
        self._show_star()

    def _prof_picked(self):
        """Returns the picked profile name, or None if nothing valid is picked."""
        return self.prof_sel if self.prof_sel in self.prof_names else None

    def _show_star(self):
        """Colours the star gold when the picked profile is the favourite, grey otherwise."""
        p = self._prof_picked()
        r, g, b = self.STAR_ON if bool(p) and p == self.prof_fav else self.STAR_OFF
        for box in self.prof_stars:
            with Kit.quiet:
                box.SetBaseColor(r, g, b, 255)

    def _star_click(self):
        """Click handler of the star; the poll sees the flag."""
        self.prof_star_hit = True

    def _poll_profiles(self):
        """Script thread: follows the drop down, and turns a click on the star, Load or Save into a profile
        request for the host to run (only one at a time).
        Save uses the typed name, or overwrites the picked profile when the box is empty.
        """
        if self.prof_dd is not None and self._fld_due:
            i = Kit.dd_index(self.prof_dd, None)
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
            return
        picked = self._prof_picked()
        if save:
            typed = str(safe(lambda: self.prof_tb.Text, "") or "").strip()
            name = PROFILES.clean(typed) if typed else picked
            if not name:
                Kit.say("type a profile name beside Save.", Kit.HUE_BAD)
                return
            self.host.profile_req = ("save", name)
        elif not picked:
            Kit.say("save a profile first (type a name beside Save).", Kit.HUE_BAD)
        elif load:
            self.host.profile_req = ("load", picked)
        else:
            self.host.profile_req = ("fav", picked)

    def settings_slots(self):
        """Returns the slots that have a settings page (modules and standalone pages)."""
        return [s for s in self.host.slots if s.lazy is not None or (s.api is not None and s.api.get("build_config"))] \
            + list(self.host.pages)

    def open(self, launch=False):
        """Opens the window as the gear icon or in full, as last left.

        Script thread. launch is True when the player starts the script: the window then opens as the gear
        (and asks the action bar to dock it when the bar is on) instead of in full.
        """
        if self.prof_cache is None:
            self.refresh_profiles()
        if launch and self.host.bar_on():
            self.host.dock_want_set(self.DOCK_KEY, True)
        if self.minimized or launch:
            self.build_gear(self.gx, self.gy)
        else:
            self.build_full(self.x, self.y, "start")

    def build_full(self, x, y, why="redraw"):
        """Builds the full window at x, y on the client thread."""
        self.why = why
        Kit.on_client(lambda: self._build_full(x, y))

    def _replace(self, g, mode, x, y, w, h, head=None, hidden=False):
        """Puts the new gump g in place of the old one: positions it on screen, adds it, hooks its move
        event, then disposes the previous gump so there is never a gap on screen.
        """
        old, same = self.g, self.mode == mode
        x, y = Kit.place(g, x, y, w, h, head)
        if mode == "gear":
            self.gx, self.gy = x, y
        else:
            self.x, self.y = x, y
        self.g, self.mode = g, mode
        Kit.replace_gump(old if same else None, g, hidden)
        Kit.on_moved(g, self._moved)
        self.host.built(self.DOCK_KEY)
        if mode == "gear":
            g.SetInScreen()
        Kit.dispose(old)

    def _note_pos(self):
        """Copies the live window position into the saved one. Returns False if it cannot be read."""
        x, y = self.pos()
        if x is None or y is None:
            return False
        if self.mode == "gear":
            self.gx, self.gy = x, y
        elif self.mode == "full":
            self.x, self.y = x, y
        return True

    def _moved(self):
        """Move event: remembers the new place and saves it."""
        if self._note_pos():
            self.host.save_prefs()

    def _settings_error(self, s, what, ex):
        """Reports an error of a settings page once per distinct message and counts it against the module."""
        msg = "%s: %s settings %s error: %s%s" % (APP_NAME, s.title, what, ex, _error_where())
        if msg not in self.reported:
            self.reported.add(msg)
            API.SysMsg(msg, Kit.HUE_BAD)
        self.host.count_error(s, page=True)

    def _leave_page(self):
        """Called when the settings page on show is left or rebuilt: lets it poll one last time (unless it
        is already stale) and then close, so its edits are kept.
        """
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

    # Column width is the window width less the margins; MIN_W and MIN_H bound the resize.
    COL_W = W - 2 * Kit.MARGIN
    MIN_W = W
    MIN_H = 200
    SETTLE = 0.35
    SCALES = (70, 80, 90, 100, 110, 125, 150)
    ART_LESS = (5401, 5401, 5401)
    ART_MORE = (5402, 5402, 5402)
    HELP_LINES = ("Tick a module to turn it on; closing its window turns it off. Settings are on the Settings tab.",
                  "Drag a corner to resize; - and + scale the window.",
                  "Zones, layout and snapping: Settings > Interface.")
    BROKEN = "couldn't load: see the journal"
    LAG_SAMPLE = "12 modules on; slowest lately: Ultima Tracker, 999 ms"

    def _context(self):
        """Decides which slots, pages and page to draw. Returns (slots, pages, page).
        A lazy page that is not loaded yet is requested from the script thread and the window shows a
        loading note until loaded() arrives. A page that fails to load falls back to the first that works.
        """
        host = self.host
        pages = self.settings_slots()
        page = None
        if self.tab == "settings" and pages:
            page = host.page_slot(self.page)
            if page not in pages:
                page = pages[0]
                self.page = page.key
            if page.lazy is not None and Client.on_client_thread():
                host.request_load(page)
                self.loading = page
                return host.slots, pages, None
            if not host.load(page) or not page.api.get("build_config"):
                pages = self.settings_slots()
                page = pages[0] if pages and host.load(pages[0]) and pages[0].api.get("build_config") else None
                if page is not None:
                    self.page = page.key
        self.loading = None
        return host.slots, pages, page

    def _body_y(self):
        """Returns the y where the body starts, below the title and profile rows."""
        return Kit.MARGIN + 34 + Kit.GAP + self.PROF_H + Kit.GAP

    def _pack(self, units, n, limit):
        """Packs units into n columns of height limit. Returns a list of placements
        (unit, column, top, first row, last row, height), or None if they do not fit.
        A unit with rows can be split between columns at row boundaries, repeating its head.
        """
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
        """Finds the smallest column height at which units fit in n columns by bisection and returns that
        packing.
        """
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
        """Chooses how many columns fit the screen and the player's size limit, and returns the packing
        of units for column width CW.
        """
        M, GAP = Kit.MARGIN, Kit.GAP
        lim_w = self.lim_w
        sw = Kit.screen()[0]
        if sw:
            lim_w = min(lim_w, max(self.MIN_W, int(sw / self.scale) - 10))
        n = max(1, (lim_w - 2 * M + GAP) // (CW + GAP))
        if sw:
            n = max(1, min(n, (int(sw / self.scale) - 2 * M + GAP) // (CW + GAP)))
        limit = max(40, self.lim_h - self._body_y() - M)
        placed = self._pack(units, n, limit)
        if placed is None:
            placed = self._fit(units, n)
        return placed

    @staticmethod
    def _matches(s, q):
        """Returns (hit, part keys) telling whether slot s matches the search text q (lower case).
        Matches title, description, old names, then parts by title and description, and last the
        words of a part's settings.
        """
        if not q:
            return True, []
        hit = q in s.title.lower() or q in (s.desc or "").lower() or any(q in a.lower() for a in s.aliases)
        parts = [p[0] for p in s.parts if q in p[1].lower() or q in (p[2] or "").lower()]
        if not parts:
            parts = [p[0] for p in s.parts if any(q in str(o).lower() for o in p[4])]
        return hit or bool(parts), parts

    def _mod_rows(self, slots, CW):
        """Builds the rows of the module list for width CW, grouped by category and filtered by the search.
        A row is a category head, a module (with its description wrapped), one of its parts or a
        no-match note. Parts show unless the module is folded (a search match unfolds them).
        """
        q = self.mod_search.strip().lower()
        groups, order, found = {}, [], {}
        for s in slots:
            hit, parts = self._matches(s, q)
            if not hit:
                continue
            found[s.key] = parts
            cat = s.category or "Other"
            if cat not in groups:
                groups[cat] = []
                order.append(cat)
            groups[cat].append(s)
        cats = [c for c in CATEGORY_ORDER if c in groups] + sorted(c for c in order if c not in CATEGORY_ORDER)
        rows = []
        for cat in cats:
            rows.append(("head", cat))
            for s in groups[cat]:
                broken = s.api is None and s.lazy is None
                rows.append(("mod", s, broken, Kit.wrap(self.BROKEN if broken else s.desc, CW - 212)))
                if s.parts and not broken and (not s.folded or found.get(s.key)):
                    for p in s.parts:
                        rows.append(("part", s, p, Kit.wrap(p[2] or "", CW - 248), p[0] in found.get(s.key, ())))
        if not rows:
            rows.append(("none", 'No module matches "%s".' % self.mod_search.strip()))
        return rows

    @staticmethod
    def _row_h(r):
        """Returns the pixel height of a module list row."""
        if r[0] in ("mod", "part"):
            return Kit.pitch(26) + 20 * (len(r[3]) - 1)
        return Kit.pitch(24)

    def _units_modules(self, slots):
        """Returns the layout units of the Modules tab (the list and the help block) and the column width."""
        CW = self.COL_W
        rows = self._mod_rows(slots, CW)
        lines = [l for para in self.HELP_LINES for l in Kit.wrap(para, CW - 42)]
        h_opts = 8 + 22 * len(lines) + 24
        units = [{"rows": [self._row_h(r) for r in rows], "head": 34, "tail": 4,
                  "draw": lambda g, x, y, h, i, j: self._draw_mods(g, x, y, CW, h, rows[i:j], i == 0)}, {"h": h_opts,
                  "draw": lambda g, x, y, h, i, j: self._draw_opts(g, x, y, CW, h, lines)}]
        return units, CW

    PAGE_MAX_W = 1100

    def _measure_page(self, page, x0, y0, CW):
        """Measures a settings page without showing it: builds it onto a canvas with no gump, reads where its
        sections and widest control end, and removes the controls again.
        Returns ([section rectangles], width needed) or None if the page fails.
        Results are cached by page, width and what is switched on; the cache is cleared past 64 entries.
        Runs on the client thread.
        """
        try:
            hp = int(page.api["config_height"](CW))
        except Exception:
            hp = None
        ck = (page.key, CW, hp, bool(page.running), tuple(p[0] for p in page.parts if page.parts_on.get(p[0])))
        if ck in self.measured:
            return self.measured[ck]
        measure = PageCanvas(None)
        out = None
        try:
            page.api["build_config"](measure, x0, y0, CW)
            if Kit.flush():
                right = x0 + CW
                for c in measure.ctrls:
                    r = safe(lambda: int(c.GetX()) + int(c.GetWidth()), None)
                    if r is not None and r != x0 + CW:
                        right = max(right, r + 4)
                out = ([tuple(int(v) for v in r) for r in measure.sections], right - x0)
        except Exception:
            out = None
        finally:
            # The page's close hook runs so anything it opened for the dry run is released.
            if page.api.get("config_closed"):
                safe(page.api["config_closed"])
            for c in measure.ctrls:
                Kit.dispose(c)
        if len(self.measured) > 64:
            self.measured.clear()
        if page not in self.host.pages:
            self.measured[ck] = out
        return out

    def forget_measure(self, key):
        """Drops the cached measurements of one page."""
        for ck in [ck for ck in self.measured if ck[0] == key]:
            self.measured.pop(ck, None)

    def loaded(self, key):
        """Called when a lazy page has finished loading: drops its measurement and its search index entry (the
        page is indexed again from its real content), and redraws if it is the page being waited for.
        """
        self.forget_measure(key)
        self._forget_index(key)
        if self.opt_wait is not None and self.opt_wait.key == key:
            self.opt_wait = None
        if self.loading is not None and self.loading.key == key:
            self.redraw_req = True

    OPT_TIP = "Type words to find an option on any settings page"
    OPT_CAP = 4000
    OPT_MAX = 30
    READING = "Reading settings: %d of %d pages"

    def _pick_unit(self, pages, CW, lit):
        """Returns the layout unit that holds the page picker: one button per settings page, in rows, with a
        (new) tag beside pages that have settings the player has not seen. The first slice also carries the
        option Search box. lit(s) says which page is current (shown in the title colour).
        """
        slot = 35 + max([Kit.text_w(s.title) for s in pages] or [80]) + 12
        per = max(1, 1 + (CW - 30 - slot) // 196)
        self.page_keys = [("page_" + s.key, s.key) for s in pages]
        n = (len(pages) + per - 1) // per
        news = set(s.key for s in pages if WhatsNew.unseen(s.key))

        def draw_pick(g, x, y, h, i, j):
            """Draws the page buttons and the Search box inside their section; i and j are the first and last row
            of buttons this slice holds when the picker is split between columns.
            """
            Kit.add_section(g, x, y, CW, h, "SETTINGS  (pick a page)" if i == 0 else "SETTINGS  (continued)")
            if i == 0:
                self._search_box(g, x + CW - 12 - self.SEARCH_W, y, self.opt_search, self.OPT_TIP)
            ly = max(((Kit.pic_size(Kit.ART_PAGE[0])[1] or 22) - 16) // 2, 0)
            for k, s in enumerate(pages):
                r = k // per
                bx, by = x + 30 + (k % per) * 196, y + 32 + (r - i) * 28
                if not i <= r < j:
                    continue
                Kit.art_button(g, self.store, "page_" + s.key, Kit.ART_PAGE, bx, by, s.title,
                               "Show %s settings" % s.title, Kit.HUE_TITLE if lit(s) else Kit.HUE_TEXT)
                if s.key in news:
                    Kit.add_label(g, Kit.Form.NEW, bx + self._cap_w(Kit.ART_PAGE, s.title) + 6, by + ly, Kit.HUE_INFO)

        return {"rows": [28] * n, "head": 34, "tail": 4, "draw": draw_pick}

    def _search_box(self, g, xs, y, text, tip):
        """Adds the Search label and text box with its left edge at xs, and forgets the text last read from
        a box so poll sees the new one fresh.
        """
        Kit.add_label(g, "Search", xs - 8 - Kit.text_w("Search"), y + 7, Kit.HUE_INFO)
        self.search_tb = Kit.with_tip(Kit.add_textbox(g, text, xs, y + 5, self.SEARCH_W, numbers=False), tip)
        self.search_text = None

    def _forget_index(self, key):
        """Drops the search index entries of settings page key so the page is read again, and bumps the index
        version so cached search hits are recomputed.
        """
        if self.opt_index.pop(key, None) is not None:
            self.opt_ver += 1

    def _index_page(self, s):
        """Builds the search index entries of settings page s: the page, each of its parts and every option the
        page lists.

        Each entry is (page key, part key or None, section name, kind, caption, tip, key to mark). The
        options are found by calling the page's config_height hook while Kit.Form.sink collects the form
        rows it describes, so the page is never drawn. Repeats and options without a caption are left out.
        """
        out = [(s.key, None, "", "page", s.title, s.desc or "", None)]
        out += [(s.key, p[0], "", "part", p[1], p[2] or "", None) for p in s.parts]
        # Calling config_height makes the form helpers record each section and its rows into Form.sink, so
        # a page's options are listed without drawing it.
        sink = Kit.Form.sink = []
        try:
            s.api["config_height"](self.COL_W)
        except Exception:
            pass
        finally:
            Kit.Form.sink = None
        for pk, title, rows in sink:
            sec = str(title or "").split("  ")[0]
            for r in rows:
                if r[0] == "buttons":
                    out += [(s.key, pk, sec, "button", str(b[2] or ""), str(b[3] or ""), b[0]) for b in r[1]]
                elif r[0] == "note":
                    out.append((s.key, pk, sec, "note", str(r[1]), "", r[1]))
                elif r[0] == "check" or r[0] in Kit.Form.FIELDS:
                    out.append((s.key, pk, sec, r[0], str(r[2]), str(r[3] or ""), r[1]))
        keep, seen = [], set()
        for e in out:
            # Entries without a caption are dropped, except the page and its parts.
            if e not in seen and (e[3] in ("page", "part") or e[4].strip()):
                seen.add(e)
                keep.append(e)
        return keep

    def _index_tick(self):
        """Script thread, a step of the background reading of every settings page into opt_index: indexes one
        page that is already loaded, or asks the host to load one lazy page and waits for it. Returns True
        when a page was indexed. The index as a whole is limited to OPT_CAP entries.
        """
        idx = self.opt_index
        todo = [s for s in self.settings_slots() if s.key not in idx]
        if not todo:
            return False
        s = next((p for p in todo if p.lazy is None), None)
        if s is None:
            if self.opt_wait is not todo[0]:
                self.opt_wait = todo[0]
                self.host.request_load(todo[0])
            return False
        n = sum(len(v) for v in idx.values())
        # The index is capped so a huge settings tree cannot grow it without limit.
        idx[s.key] = self._index_page(s)[:max(0, self.OPT_CAP - n)]
        self.opt_ver += 1
        return True

    def _opt_hits(self):
        """Returns the index entries that match the option search words, best first and at most OPT_MAX of
        them. Every word has to match an entry; the result is cached until the text or the index changes.
        """
        ck = (self.opt_search.lower(), self.opt_ver)
        if self.opt_hits[0] == ck:
            return self.opt_hits[1]
        words = ck[0].split()
        found = []
        for pi, s in enumerate(self.settings_slots()):
            for n, e in enumerate(self.opt_index.get(s.key, ())):
                p = s.part(e[1]) if e[1] else None
                cap, tip = e[4].lower(), e[5].lower()
                head = " ".join((e[2], s.title, p[1] if p else "")).lower()
                score = 0
                for w in words:
                    # A word counts most in the caption, less in the page or section head and least in the tip. Every
                    # word must match somewhere or the entry is left out.
                    pts = 3 if w in cap else 2 if w in head else 1 if w in tip else 0
                    if not pts:
                        score = 0
                        break
                    score += pts
                if score:
                    found.append((-score, pi, n, e))
        found.sort(key=lambda f: f[:3])
        hits = [f[3] for f in found[:self.OPT_MAX]]
        self.opt_hits = (ck, hits)
        return hits

    def _poll_index(self):
        """Script thread: carries on reading pages for the option search and, once all are read and the text
        has settled, redraws the window with the hits. Returns True when it asked for a redraw.
        """
        changed = self._index_tick()
        pages = self.settings_slots()
        done = sum(1 for s in pages if s.key in self.opt_index)
        if not pages:
            return False
        if done < len(pages):
            if changed and self.opt_lbl is not None:
                Kit.set_text(self.opt_lbl, self.READING % (done, len(pages)))
            return False
        # Wait while the player is still typing (search_at is set), and skip the redraw when these hits are
        # already on screen.
        if self.search_at or self._opt_hits() == self.opt_drawn:
            return False
        self.search_focus = True
        self.redraw()
        return True

    def _hit_text(self, e):
        """Returns the line shown for search hit e: the page title, then the section and the caption."""
        s = self.host.page_slot(e[0])
        title = s.title if s is not None else e[0]
        cap = e[4].rstrip(":")
        if e[3] == "page":
            return title
        if e[3] == "part" or not e[2]:
            return "%s > %s" % (title, cap)
        return "%s > %s: %s" % (title, e[2], cap)

    def _found_unit(self, pages, CW):
        """Returns the layout unit that lists the option search hits (or a reading-progress note while the
        pages are still being indexed, or a no-match note), one button per hit.
        """
        done = sum(1 for s in pages if s.key in self.opt_index)
        hits = self._opt_hits() if done == len(pages) else None
        self.opt_drawn = hits
        rows = hits or [None]
        note = self.READING % (done, len(pages)) if hits is None else 'No option matches "%s".' % self.opt_search

        def draw_found(g, x, y, h, i, j):
            """Draws the FOUND section: the progress or no-match note, or one button per hit that opens the
            option's page with the option marked.
            """
            Kit.add_section(g, x, y, CW, h, "FOUND  (click one to open it)" if i == 0 else "FOUND  (continued)")
            for r in range(i, j):
                e, ry = rows[r], y + 32 + (r - i) * 28
                if e is None:
                    self.opt_lbl = Kit.add_label(g, Kit.fit(note, CW - 24), x + 12, ry + 3, Kit.HUE_INFO)
                    continue
                bkey, text = "hit_%d" % r, self._hit_text(e)
                self.hit_keys.append((bkey, e))
                Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 30, ry, Kit.fit(text, CW - 77),
                               e[5] or "Open %s" % text)

        return {"rows": [28] * len(rows), "head": 34, "tail": 4, "draw": draw_found}

    def _fresh(self, key):
        """Returns the settings of page key that the player has not seen yet (the (new) tags), read once and
        kept while that page is drawn.
        """
        fv = self.fresh_view
        if fv is None or fv[0] != key:
            fv = self.fresh_view = (key, WhatsNew.unseen(key))
        return fv[1]

    def _units_loading(self, pages, title):
        """Returns the units shown while a lazy page loads: the picker and a loading note."""
        CW = self.COL_W

        def draw_note(g, x, y, h, i, j):
            """Draws the loading note."""
            Kit.add_section(g, x, y, CW, h)
            Kit.add_label(g, "Loading %s settings" % title, x + 12, y + 12, Kit.HUE_INFO)

        return [self._pick_unit(pages, CW, lambda s: s.title == title), {"h": 40, "draw": draw_note}], CW

    def _units_settings(self, pages, page, x0, y0):
        """Returns the layout units of a settings page: picker, the parts box, the windows box and the page
        itself cut into bands, plus the column width (wider for a page that needs it).
        """
        CW = self.COL_W
        rects = None
        m = self._measure_page(page, x0, y0, CW)
        if m is not None:
            rects, need = m
            if need > CW:
                CW = min(self.PAGE_MAX_W, need)
                m = self._measure_page(page, x0, y0, CW)
                rects = m[0] if m is not None else None
        units = [self._pick_unit(pages, CW, lambda s: s is page)]
        if page.parts:
            units.append({"h": 34 + 26 * len(page.parts) + 6,
                          "draw": lambda g, x, y, h, i, j: self._draw_parts(g, x, y, CW, h, page)})
        wins = LAYOUT.windows_of(page.key) if LAYOUT.enabled else ()
        if wins:
            units.append({"h": 34 + 26 * len(wins) + 6, "draw": lambda g, x, y, h, i,
                          j: self._draw_windows(g, x, y, CW, h, wins)})
        try:
            h_page = max(40, int(page.api["config_height"](CW)))
        except Exception as ex:
            self._settings_error(page, "layout", ex)
            h_page = 40
        bands = (self._bands(rects, y0, h_page) if rects else None) or [(0, h_page)]
        state = {"at": {}}

        def band_draw(b):
            """Returns a draw function for band b. The last band draws the whole page and moves each band's
            controls to where the layout placed that band.
            """
            def draw(g, x, y, h, i, j):
                """Records where band b was placed; the last one draws the page."""
                state["at"][b] = (x, y)
                if b == len(bands) - 1:
                    self._draw_page(g, page, x0, y0, CW, bands, state["at"])

            return draw

        for b, (top, bottom) in enumerate(bands):
            units.append({"h": bottom - top, "draw": band_draw(b)})
        return units, CW

    @staticmethod
    def _bands(rects, y0, h_page):
        """Returns (top, bottom) bands of a page from the rectangles of its sections, ignoring sections that
        sit inside another and joining ones that overlap vertically. Bands let a tall page flow over
        columns.
        """
        rects = sorted(set(rects), key=lambda r: (r[1], r[0]))
        top_level = [r for r in rects if not any(o != r and o[0] <= r[0] and o[1] <= r[1] and r[0] + r[2] <= o[0] + o[2]
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
        """Draws the settings page onto the body canvas, marking the option the player picked from the search
        and tagging unseen settings as new, then moves the controls of each band to where the layout placed
        that band. A page that raises is shown as an unavailable note and reported.
        """
        canvas = PageCanvas(g)
        F = Kit.Form
        m = self.opt_mark
        F.page, F.fresh = page.key, self._fresh(page.key)
        F.mark = (m[1], m[2]) if m is not None and m[0] == page.key and m[3] != "part" else None
        try:
            page.api["build_config"](canvas, x0, y0, CW)
        except Exception as ex:
            self._settings_error(page, "window", ex)
            Kit.add_section(g, x0, y0, CW, 40)
            Kit.add_label(g, "Settings unavailable: %s" % ex, x0 + 12, y0 + 12, Kit.HUE_BAD)
        finally:
            F.page = F.fresh = F.mark = None
        WhatsNew.see(self._fresh(page.key))
        self.shown_page = page.key
        moves = []
        for b, (top, bottom) in enumerate(bands):
            px, py = at.get(b, (x0, y0 + top))
            moves.append((top, px - x0, py - (y0 + top)))
        if all(dx == 0 and dy == 0 for t, dx, dy in moves):
            return
        if not Kit.flush():
            return
        for c in canvas.ctrls:
            try:
                cx, cy = int(c.GetX()), int(c.GetY())
            except Exception:
                continue
            rel = cy - y0
            dx, dy = moves[0][1], moves[0][2]
            for top, mx, my in moves:
                if rel >= top:
                    dx, dy = mx, my
            if dx or dy:
                safe(lambda: c.SetPos(cx + dx, cy + dy))

    SEARCH_W = 150

    def _draw_parts(self, g, x, y, w, h, s):
        """Draws the PARTS box of a page: one tick box and description per part, with a found marker beside
        the part the search picked and a (new) tag beside parts the player has not seen.
        """
        Kit.add_section(g, x, y, w, h, "PARTS  (tick a part to turn it on)")
        ry = y + 32
        m = self.opt_mark
        fresh = self._fresh(s.key)
        for p in s.parts:
            self._part_box(g, s, p, x + 12, ry)
            hit = m is not None and m[3] == "part" and m[:2] == (s.key, p[0])
            tag = Kit.Form.FOUND if hit else Kit.Form.NEW if "%s.%s" % (s.key, p[0]) in fresh else None
            d = Kit.fit(p[2] or "", w - 236 - (Kit.text_w(tag) + 6 if tag else 0))
            Kit.add_label(g, d, x + 224, ry + 2, Kit.HUE_INFO)
            if tag:
                Kit.add_label(g, tag, x + 224 + Kit.text_w(d) + 6, ry + 2, Kit.HUE_TITLE)
            ry += 26

    def _part_box(self, g, s, p, x, ry):
        """Adds the tick box of part p and records it so poll can see when it changes."""
        on = bool(s.parts_on.get(p[0]))
        cb = Kit.add_check(g, p[1], x, ry, on, "%s: %s" % (s.title, p[2] or p[1]))
        self._hook_box(cb)
        self.part_boxes.append((s, p[0], cb))
        self.seen["%s.%s" % (s.key, p[0])] = on

    ZONE_TIP = "Click: next zone (free: stays where you put it; Settings > Interface lists them all)"

    def _draw_windows(self, g, x, y, w, h, wins):
        """Draws the WINDOWS box: for each window of the module a button naming its zone."""
        Kit.add_section(g, x, y, w, h, "WINDOWS  (the zone each sits in)")
        zones = LAYOUT.zone_choices()
        ry = y + 32
        for key, title in wins:
            Kit.add_label(g, Kit.fit(title, 200), x + 12, ry + 3)
            zid = LAYOUT.zone_of(key)
            cap = "Zone: " + ((zid[5:] if zid.startswith("Zone ") else zid) if zid else "free")
            bkey = "zone_" + key
            Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 224, ry - 2, cap, self.ZONE_TIP)
            self.zone_keys.append((bkey, key, zones))
            ry += 26

    FOLD_TIP = "Show its parts"
    UNFOLD_TIP = "Hide its parts"
    MOD_TIP = "Type part of a name or feature to list matching modules (old names work)"

    def _draw_mods(self, g, x, y, w, h, rows, first):
        """Draws a slice of the module list (the head, the Search box on the first slice and the rows).
        Module rows get a tick box, a fold arrow when the module has parts and the description;
        part rows are indented with a (new) tag or a found marker from the search.
        """
        Kit.add_section(g, x, y, w, h, "MODULES  (tick a module to turn it on)" if first else "MODULES  (continued)")
        if first:
            self._search_box(g, x + w - 12 - self.SEARCH_W, y, self.mod_search, self.MOD_TIP)
        ry = y + 32
        news = WhatsNew.unseen()
        for row in rows:
            if row[0] == "part":
                s, p, lines, hit = row[1], row[2], row[3], row[4]
                self._part_box(g, s, p, x + 36, ry)
                xd = x + 236
                for k, line in enumerate(lines):
                    Kit.add_label(g, line, xd, ry + 2 + 20 * k, Kit.HUE_INFO)
                tag = Kit.Form.FOUND if hit else (Kit.Form.NEW if "%s.%s" % (s.key, p[0]) in news else "")
                if tag:
                    tw = Kit.text_w(lines[0]) if lines else 0
                    Kit.add_label(g, tag, min(xd + tw + 10, x + w - 12 - Kit.text_w(tag)), ry + 2,
                                  Kit.HUE_TITLE if hit else Kit.HUE_INFO)
            elif row[0] != "mod":
                Kit.add_label(g, row[1].upper() if row[0] == "head" else row[1], x + 12, ry + 3,
                              Kit.HUE_TITLE if row[0] == "head" else Kit.HUE_INFO)
            else:
                s, broken, lines = row[1], row[2], row[3]
                if broken:
                    Kit.add_label(g, s.title, x + 36, ry + 2, Kit.HUE_INFO)
                else:
                    cb = Kit.add_check(g, s.title, x + 12, ry, s.enabled, s.desc)
                    self._hook_box(cb)
                    self.box_list.append((s, None, cb))
                    self.seen[s.key] = s.enabled
                    if s.parts:
                        arrow = ">" if s.folded else "v"
                        Kit.add_label(g, arrow, x + 184, ry + 2, Kit.HUE_TITLE)
                        Kit.catcher(g, x + 178, ry, 18, 22, self._fold_click(s.key),
                                    self.FOLD_TIP if s.folded else self.UNFOLD_TIP)
                        self.fold_keys.append(("fold_" + s.key, s.key))
                for k, line in enumerate(lines):
                    Kit.add_label(g, line, x + 200, ry + 2 + 20 * k, Kit.HUE_BAD if broken else Kit.HUE_INFO)
            ry += self._row_h(row)

    def _fold_click(self, key):
        """Returns the click handler of a module's fold arrow; it raises the flag poll() reads and pokes the
        host.
        """
        store = self.store

        def hit():
            """Click handler: records that the fold arrow of this module was hit."""
            Kit.clicks_seen = True
            store[1]["fold_" + key] = True
            HOST.poke()

        return hit

    def _draw_opts(self, g, x, y, w, h, lines):
        """Draws the help block and an empty line for the lag report."""
        Kit.add_section(g, x, y, w, h)
        ly = y + 8
        for line in lines:
            Kit.add_label(g, line, x + 30, ly, Kit.HUE_INFO)
            ly += 22
        self.lag_lbl = Kit.add_label(g, "", x + 30, ly, Kit.HUE_INFO)
        self.lag_next = 0.0

    def _on_resized(self, *args):
        """Resize event: fades the window while it is being dragged. The rebuild waits until it settles."""
        first = not self.resize_at
        self.resize_at = time.time()
        g = self.g
        if first and self.mode == "full" and Kit.is_open(g):
            g.SetAlpha(0.55)

    def _relayout(self):
        """Rebuilds the window for its new size once the player has finished resizing it, and saves the size."""
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
        """Steps the window scale up or down through SCALES (d is 1, -1 or 0 to return to 100%)."""
        pcts = list(self.SCALES)
        cur = int(round(self.scale * 100))
        i = min(range(len(pcts)), key=lambda k: abs(pcts[k] - cur))
        i = max(0, min(len(pcts) - 1, i + d)) if d else pcts.index(100)
        if pcts[i] != cur:
            self.scale = pcts[i] / 100.0
            self.redraw()

    def _reset(self):
        """Clears the per-build state before a rebuild, leaving the shown page first: the stored clicks and
        keys of the old controls, the search box and the profile row's controls.
        """
        self._leave_page()
        self.search_tb, self.search_text, self.search_at = None, None, 0.0
        self.store = ({}, {})
        self.page_keys, self.box_list, self.zone_keys, self.hit_keys = [], [], [], []
        self.lag_lbl = self.opt_lbl = None
        self._prof_reset()

    def _plan(self):
        """Works out the layout for the current tab: the page, units, column width, placements and the
        window's total width and height. With a search typed on the Settings tab the units are the page
        picker and the list of hits instead of a page.
        """
        slots, pages, page = self._context()
        M, GAP = Kit.MARGIN, Kit.GAP
        y_body = self._body_y()
        if self.tab == "settings" and pages and self.opt_search and not self.opt_open:
            CW, page, self.fresh_view = self.COL_W, None, None
            units = [self._pick_unit(pages, CW, lambda s: False), self._found_unit(pages, CW)]
        elif self.tab == "settings" and page is not None:
            units, CW = self._units_settings(pages, page, M, y_body)
        elif self.tab == "settings" and self.loading is not None and pages:
            units, CW = self._units_loading(pages, self.loading.title)
        else:
            units, CW = self._units_modules(slots)
            self.fresh_view = None
        placed = self._flow(units, CW)
        n_cols = 1 + max([p[1] for p in placed] or [0])
        W = 2 * M + n_cols * CW + (n_cols - 1) * GAP
        H = y_body + max([p[2] + p[5] for p in placed] or [40]) + M
        return page, units, CW, placed, W, H

    def _draw_body(self, g, units, CW, placed):
        """Calls each unit's draw function in order onto one canvas and returns the canvas."""
        body = PageCanvas(g)
        y_body = self._body_y()
        for u, col, top, i, j, h in sorted(placed, key=lambda p: p[0]):
            units[u]["draw"](body, Kit.MARGIN + col * (CW + Kit.GAP), y_body + top, h, i, j)
        return body

    def _build_full(self, x, y):
        """Builds the full window at x, y: frame, title row with tabs, scale, Find and dock buttons, profile
        row and body, scaled by the player's percentage. A search box that had keyboard focus gets it
        back so typing is not interrupted. Client thread.
        """
        if self.host.settled_at is None and len(self.why_log) < 10:
            self.why_log.append((time.time(), self.why))
        self._reset()
        self.seen, self.resize_at = {}, 0.0
        self.part_boxes, self.fold_keys = [], []
        M, GAP = Kit.MARGIN, Kit.GAP
        L = M
        page, units, CW, placed, W, H = self._plan()
        y_title = M
        y_prof = y_title + 34 + GAP
        y_body = self._body_y()
        IW = W - 2 * M
        S = self.scale
        # The gump is created at the scaled size, then Kit.scale_window scales its contents to match.
        WS, HS = int(round(W * S)), int(round(H * S))
        g = G.CreateModernGump(x, y, WS, HS, True, int(self.MIN_W * S), int(self.MIN_H * S), self._on_resized)
        g.SetAlpha(0)
        Kit.add_window_frame(g, W, H, mouse=False)
        Kit.add_section(g, L, y_title, IW, 34)
        Kit.add_label(g, "VIRTUE ASSISTANT", L + 30, y_title + 9, Kit.HUE_TITLE)
        xv = L + 30 + Kit.text_w("VIRTUE ASSISTANT") + 12
        Kit.add_label(g, "v" + APP_VERSION, xv, y_title + 9, Kit.HUE_INFO)
        xt = xv + Kit.text_w("v" + APP_VERSION) + 16
        Kit.title_catcher(g, L, y_title, xt - 6 - L, 34, lambda: self.store[1].__setitem__("min", True), key="va")
        for key, text in self.TABS:
            on = key == self.tab
            Kit.art_button(g, self.store, "tab_" + key, Kit.ART_PAGE, xt, y_title + 6, text,
                           "Show the %s tab" % text, Kit.HUE_TITLE if on else Kit.HUE_INFO)
            xt += self._cap_w(Kit.ART_PAGE, text) + 16
        pct = "%d%%" % int(round(S * 100))
        xp = W - M - 74 - Kit.DOCK_DX - 8 - 16
        Kit.art_button(g, self.store, "scale_up", self.ART_MORE, xp, y_title + 9, None, "Larger window and text")
        xl = xp - 6 - Kit.text_w(pct)
        Kit.add_label(g, pct, xl, y_title + 9, Kit.HUE_TEXT)
        Kit.catcher(g, xl - 2, y_title + 6, Kit.text_w(pct) + 4, 22,
                    lambda: self.store[1].__setitem__("scale_reset", True), "Scale (click: 100%)")
        Kit.art_button(g, self.store, "scale_down", self.ART_LESS, xl - 6 - 16, y_title + 9,
                       None, "Smaller window and text")
        Kit.dock_button(g, self.store, W - M - 74, y_title + 9)
        Kit.art_button(g, self.store, "min", Kit.ART_MIN, W - M - 74, y_title + 9, None,
                       "Minimize to the gear (or double-click the title)")
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, y_title + 6,
                       None, "Close Virtue Assistant (stops every module)")
        self.find_prof = False
        lt = self.host.launcher
        lim = xl - 6 - 16 - 8
        fw, aw = self._cap_w(Kit.ART_PAGE, "Find"), Kit.pic_size(Kit.ART_PAGE[0])[0] or 30
        if lt is not None and xt + fw <= lim:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, lim - fw, y_title + 6, "Find", Launcher.TIP,
                           Kit.HUE_INFO, lt.toggle)
        elif lt is not None and xt + aw <= lim:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, lim - aw, y_title + 6, None,
                           Kit.caption_tip("Find", Launcher.TIP), None, lt.toggle)
        else:
            self.find_prof = lt is not None
        try:
            self._build_profiles(g, L, y_prof, IW)
        except Exception as ex:
            self.prof_dd_args = None
            Kit.add_label(g, "Profiles unavailable: %s" % ex, L + 12, y_prof + 9, Kit.HUE_BAD)
        if self.find_prof:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, L + IW - 12 - aw, y_prof + 6, None,
                           Kit.caption_tip("Find", Launcher.TIP), None, lt.toggle)
        keys = frozenset(self.store[0])
        body = self._draw_body(g, units, CW, placed)
        self._add_profile_list(g)
        # If the client cannot scale the window it falls back to 100% rather than draw a broken window.
        if not Kit.scale_window(g, S) and S != 1.0:
            self.scale, S, WS, HS = 1.0, 1.0, W, H
            Kit.say("can't scale the window; it stays at 100%.", Kit.HUE_BAD)
        if self.mode != "full":
            jx = LAYOUT.beside_journal(x, y, WS, HS)
            self.from_xy = (x, y, jx)
            x = jx
        self._replace(g, "full", x, y, WS, HS, int(round(y_body * S)))
        fit = Kit.scroll_info(g)
        self.size = (fit["w2"], fit["hv"]) if fit else (WS, HS)
        self.minimized = False
        self.dirty = None
        self.body, self.head = body, (g, W, self.tab, (Kit.look(), Kit.compact), keys)
        # The search box keeps keyboard focus across a rebuild so typing is not interrupted.
        if self.search_focus:
            self.search_focus = False
            tb = self.search_tb
            if tb is not None:
                cc = Kit.client_control(tb)
                if cc is not None and Kit.flush():
                    safe(lambda: cc.SetKeyboardFocus())

    def build_gear(self, x, y):
        """Builds the small gear icon window at x, y (the minimised state). Hidden while docked in the bar."""
        self._reset()
        self.fresh_view = None
        S = self.GEAR
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, S, S, corners=False)
        Kit.add_section(g, 7, 7, S - 14, S - 14)
        p = G.CreateGumpItemPic(0x1053, S - 18, S - 18)
        p.SetPos(9, 9)
        p.SetAcceptMouseInput(False)
        g.Add(p)
        Kit.catcher(g, 0, 0, S, S, self._gear_click, "%s: click to open, drag to move" % APP_NAME, movable=True)
        self.gear_clicked, self.gear_pos, self.gear_moved = False, None, 0.0
        self.docked = self.host.dock_wanted(self.DOCK_KEY) and self.host.bar_soon()
        self._replace(g, "gear", x, y, S, S, hidden=self.docked)
        self.minimized = True

    def fold_to_bar(self):
        """Hands the window to the action bar: folds it and tells the player if the bar is not running."""
        self.host.dock_want_set(self.DOCK_KEY, True)
        if self.mode == "full":
            self.fold()
        if not self.host.bar_alive():
            self.host.dock_note(APP_NAME)

    def _show_gear(self, shown):
        """Shows or hides the gear icon."""
        g = self.g
        if self.mode == "gear" and Kit.is_open(g):
            g.IsVisible = bool(shown)
            Kit.stir()

    def link_tick(self):
        """Script thread, about ten times a second: takes commands and module enable requests from the action
        bar through shared variables, keeps the gear hidden or shown to match the dock state, and publishes
        the state (docked, gear or open).

        A show command is ignored while the script is still starting and the player has not pressed
        anything (see _stale), so a request left over from an earlier run does not pop the window open.
        """
        now = time.time()
        if now < self.link_next and self.link_next - now <= 0.1:
            return
        self.link_next = now + 0.1
        key = self._take_shared(self.LINK_ENABLE)
        if key:
            self.host.enable(str(key))
        cmd = self._take_shared(self.LINK_CMD)
        if cmd:
            cmd = str(cmd)
            if cmd == "show" and self.mode != "full":
                if not self._stale("link"):
                    self.unfold("link")
            elif cmd == "dock" and self.mode == "full":
                self.fold_to_bar()
            elif cmd == "modules":
                self.request_tab = "modules"
        self.dock_sync()
        state = ("docked" if self.docked else "gear") if self.mode == "gear" else "open"
        if state != self.link_state:
            self.link_state = state
            API.SetSharedVar(self.LINK_STATE, state)

    def dock_sync(self):
        """Hides the gear icon when the window is wanted in the action bar and the bar is up or about to be,
        and shows it again when that stops. Does nothing unless the window is the gear.
        """
        want = self.host.dock_wanted(self.DOCK_KEY)
        if self.mode == "gear" and (self.docked or want):
            hide = want and self.host.bar_soon()
            if hide != self.docked:
                self.docked = hide
                self._show_gear(not hide)

    @staticmethod
    def _take_shared(name):
        """Returns the value of shared variable name and clears it, so each command is seen once.
        None if the variable cannot be read.
        """
        try:
            v = API.GetSharedVar(name)
        except Exception:
            return None
        if v:
            API.RemoveSharedVar(name)
        return v

    def _gear_click(self):
        """Click handler of the gear icon; poll() checks the flag."""
        self.gear_clicked = True

    def _unpressed(self):
        """True while the script is still starting and no hotkey has been pressed yet."""
        return self.host.booting() and self.host.pressed_at <= 0

    def _stale(self, why):
        """True when a request to open the window should be ignored because the script is still starting and
        nothing was pressed. The first few refused requests are kept (stale_log) with the reason why, for
        the start-up report.
        """
        h = self.host
        if not h.booting() or h.pressed_at > 0:
            return False
        if len(self.stale_log) < 10:
            self.stale_log.append((time.time(), why))
        return True

    def pos(self):
        """Returns the window's (x, y) on screen; either is None if it cannot be read."""
        g = self.g
        return safe(lambda: int(g.GetX())), safe(lambda: int(g.GetY()))

    def store_prefs(self, prefs):
        """Writes the window's place, size limits, scale, tab, page and snap setting into prefs (strings)."""
        if Client.on_client_thread():
            self._note_pos()
        for k, v in (("cfg_x", self.x), ("cfg_y", self.y), ("cfg_w", self.lim_w), ("cfg_h", self.lim_h),
                     ("cfg_scale", int(round(self.scale * 100))), ("gear_x", self.gx), ("gear_y", self.gy)):
            prefs[k] = str(v)
        prefs["cfg_min"] = "1" if self.minimized else "0"
        prefs["cfg_tab"], prefs["cfg_page"] = self.tab, self.page or ""
        prefs["snap"] = "1" if SNAP.enabled else "0"

    def fold(self):
        """Folds the full window to the gear icon at the same place."""
        x, y = self.pos()
        f, self.from_xy = self.from_xy, None
        if x is not None:
            self.x, self.y = x, y
        self.gx, self.gy = (f[0], f[1]) if f is not None and f[0] != f[2] == self.x else (self.x, self.y)
        self.build_gear(self.gx, self.gy)
        self.host.save_prefs()

    def unfold(self, why="redraw"):
        """Opens the full window from the gear icon, where the gear sat, and clears the dock request."""
        x, y = self.pos()
        if x is not None:
            self.gx, self.gy = x, y
        self.docked = False
        self.host.dock_forget(self.DOCK_KEY)
        self.build_full(self.gx, self.gy, why)
        self.host.save_prefs()

    def redraw(self, why="redraw"):
        """Rebuilds the full window in place (or opens it if it is the gear) and saves the preferences."""
        if self.mode != "full":
            self.unfold(why)
            return
        x, y = self.pos()
        if x is not None:
            self.x, self.y = x, y
        self.build_full(self.x, self.y, why)
        self.host.save_prefs()

    def _switch_page(self, key):
        """Shows settings page key and swaps the body of the window, rebuilding everything if a quick swap is
        not possible.
        """
        self.page = key
        x, y = self.pos()
        if x is not None:
            self.x, self.y = x, y
        Kit.on_client(self._swap_body)
        self.host.save_prefs()

    def _swap_body(self):
        """Client thread: swaps only the body when the window frame can stay as it is (same tab, theme and
        scale, nothing scrolled or filled, no resize pending, profile row unchanged). Otherwise does a full
        rebuild.
        """
        g, head = self.g, self.head
        done = False
        # A page switch is the hot case when browsing settings, so the frame is kept when it can be.
        if head is not None and head[0] is g and Kit.is_open(g) and self.tab == head[2] == "settings" \
                and head[3] == (Kit.look(), Kit.compact) and self.scale == 1.0 and g not in Kit._scrolled \
                and g not in Fill.recs and not self.resize_at and self.prof_cache is not None \
                and self._prof_key(self.prof_cache) == self.prof_shown:
            try:
                done = self._fast_body(g, head[1], head[4])
            except Exception as ex:
                self.host._tell("%s: settings window error: %s%s" % (APP_NAME, ex, _error_where()))
        if not done:
            self.why = "redraw"
            self._build_full(self.x, self.y)

    def _fast_body(self, g, W0, keys):
        """Redraws just the body for the current page at the existing window. Returns False when the new
        layout needs a different window size or the frame cannot be fitted, so the caller does a full build.
        """
        self._leave_page()
        self.page_keys, self.zone_keys, self.part_boxes, self.seen = [], [], [], {}
        page, units, CW, placed, W, H = self._plan()
        if page is None or W != W0 or H > Kit.screen()[1] > 0 or not Kit.frame_fit(g, W, H):
            return False
        store, texts, w2r = self.store, Kit._texts, Fill.w2r
        # The old body controls are disposed and their cached text and fill entries dropped so they do not leak.
        for c in self.body.ctrls:
            Kit.dispose(c)
            texts.pop(c, None)
            w2r.pop(c, None)
        for k in [k for k in store[0] if k not in keys]:
            store[0].pop(k, None)
            store[1].pop(k, None)
        self.body = self._draw_body(g, units, CW, placed)
        self._add_profile_list(g)
        self.x, self.y = Kit.place(g, self.x, self.y, W, H)
        Kit.moved_by_code(g)
        self.size, self.dirty = (W, H), None
        return True

    def show_settings(self, key):
        """Asks the window to open the settings page of module key on the next poll."""
        self.request = key

    def refresh(self, key):
        """Marks module key's settings page as stale: its cached measure and search index entry are dropped
        and, if the page is on show, it redraws.
        """
        self.forget_measure(key)
        self._forget_index(key)
        if self.shown_page == key:
            self.dirty = self.stale_page = key

    def close(self):
        """Closes the window and tells the action bar the state is off."""
        self.closing = True
        self._leave_page()
        g, self.g = self.g, None
        Kit.dispose(g)
        self.docked, self.link_state = False, None
        API.SetSharedVar(self.LINK_STATE, "off")

    def poll(self):
        """Script thread poll of the window, run every pass.
        Rebuilds the gump if the player closed it, takes action bar commands, handles page and tab
        requests, then in order: the gear icon, redraw requests, settled resizes, button clicks, the profile
        row, search box typing, the option index, the lag line, ticked boxes (at most BOX_EVERY apart unless
        a click was seen) and the shown page's own poll_config. Each step that rebuilds the window ends
        the pass.
        """
        if self.closing:
            return
        if not Kit.is_open(self.g):
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
            if self.mode == "full" or not self._unpressed():
                self.redraw("request:%s" % key)
            return
        if self.request_tab is not None:
            tab, self.request_tab = self.request_tab, None
            if tab in ("modules", "settings"):
                self.tab = tab
            if self.mode == "full" or not self._unpressed():
                self.redraw("tab:%s" % tab)
            return
        if self.mode == "gear":
            now = time.time()
            # The gear position is read at most twice a second so a click can be told from the end of a drag.
            if not self.docked and (self.gear_clicked or self.gear_pos is None or now >= self.gear_look
                                    or SNAP.pressed() is not False):
                self.gear_look = now + 0.5
                p = self.pos()
                if p != self.gear_pos:
                    if self.gear_pos is not None:
                        self.gear_moved = now
                    self.gear_pos = p
            if self.gear_clicked:
                self.gear_clicked = False
                if now - self.gear_moved > 0.35 and not self._stale("gear"):
                    self.unfold("gear")
            return
        if self.prof_redraw:
            self.prof_redraw = False
            self.redraw()
            return
        if self.redraw_req:
            self.redraw_req = False
            if self.tab == "settings":
                self.redraw()
                return
        if self.resize_at and time.time() - self.resize_at >= self.SETTLE and not SNAP.pressed():
            self.resize_at = 0.0
            self._relayout()
            return
        if self._poll_buttons():
            return
        self._fld_due = self.host.poll_due(self._fld_gate)
        self._poll_profiles()
        if self.search_tb is not None and self._fld_due and self._poll_search():
            return
        if self.tab == "settings" and self.opt_search and not self.opt_open and self._fld_due:
            if self._poll_index():
                return
        # The lag line is refreshed once a second.
        if self.lag_lbl is not None and time.time() >= self.lag_next:
            self.lag_next = time.time() + 1.0
            running = self.host.active
            if running:
                worst = max(running, key=lambda s: s.load[2])
                text = "%d modules on; slowest lately: %s, %d ms" % (len(running), worst.title, worst.load[2])
            else:
                text = "No modules on"
            Kit.set_text(self.lag_lbl, text)
        now = time.time()
        if self.box_hit or now >= self.box_next or not Kit.clicks_seen:
            self.box_hit = False
            self.box_next = now + self.BOX_EVERY
            if self._poll_boxes():
                return
        s = self.host.page_slot(self.shown_page) if self.shown_page is not None else None
        if self.stale_page is not None and self.stale_page == self.shown_page:
            s = None
        if s is not None and s.api is not None and s.api.get("poll_config"):
            if self._pp_key != self.shown_page:
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
        """Watches the search box. After the text has settled for SEARCH_SETTLE seconds it filters the module
        list (Modules tab) or the option search (Settings tab) by it and redraws, keeping focus in the box.
        Returns True when it redrew.
        """
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
            q = t.strip()
            opt = self.tab == "settings"
            if q.lower() != (self.opt_search if opt else self.mod_search).strip().lower():
                if not opt:
                    self.mod_search = q
                else:
                    self.opt_search, self.opt_open = q, False
                if opt and not q:
                    self.opt_mark = None
                self.search_focus = True
                self.redraw()
                return True
        return False

    BOX_EVERY = 1.0

    def _hook_box(self, cb):
        """Hooks a tick box so a click wakes the host at once instead of waiting for the next box poll."""
        if cb is None:
            return

        def hit(*args):
            """Click handler: flags that a box was hit and pokes the host."""
            Kit.clicks_seen = True
            self.box_hit = True
            HOST.poke()

        G.AddControlOnClick(cb, hit)

    def _poll_boxes(self):
        """Compares each tick box with what was last seen and turns modules and parts on or off to match.
        A box that disagrees with the real state is put back. Returns True when the window was rebuilt
        or closed in the process.
        """
        seen = self.seen
        for s, pk, cb in self.box_list + self.part_boxes:
            sk, cur = (s.key, s.enabled) if pk is None else ("%s.%s" % (s.key, pk), bool(s.parts_on.get(pk)))
            try:
                v = bool(cb.IsChecked)
            except Exception:
                v = cur
            if v != seen.get(sk):
                seen[sk] = v
                if pk is not None:
                    self.host.part_set(s.key, pk, v)
                if pk is not None and v:
                    WhatsNew.see((sk,))
                elif v:
                    self.host.enable(s.key)
                else:
                    self.host.disable(s.key)
                if not Kit.is_open(self.g) or self.mode != "full":
                    return True
            elif v != cur:
                safe(lambda: cb.SetIsChecked(cur))
                seen[sk] = cur
        return False

    def _poll_buttons(self):
        """Handles the stored button clicks: close, minimise, dock, scale, tab, page, search hit, fold and
        zone buttons. A search hit opens its page with the option marked. Returns True when one was
        handled and the window changed.
        """
        store = self.store
        if Kit.clicks_seen and True not in store[1].values():
            return False
        if Kit.was_clicked(store, "close"):
            self.host.save_prefs()
            self.host.quitting = True
            return True
        if Kit.was_clicked(store, "min"):
            self.host.dock_forget(self.DOCK_KEY)
            self.fold()
            return True
        if Kit.was_clicked(store, "tobar"):
            self.fold_to_bar()
            return True
        Kit.was_clicked(store, "find")
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
                self.opt_open, self.opt_mark = bool(self.opt_search), None
                self._switch_page(key)
                return True
        for bkey, e in self.hit_keys:
            if Kit.was_clicked(store, bkey):
                self.opt_open, self.opt_mark = True, (e[0], e[1], e[6] if e[6] is not None else e[4], e[3])
                self._switch_page(e[0])
                return True
        for bkey, key in self.fold_keys:
            if Kit.was_clicked(store, bkey):
                s = dict.get(self.host.by_key, key)
                if s is not None:
                    s.folded = not s.folded
                self.redraw()
                return True
        for bkey, key, zones in self.zone_keys:
            if Kit.was_clicked(store, bkey):
                cur = LAYOUT.zone_of(key)
                i = zones.index(cur) if cur in zones else 0
                nxt = zones[(i + 1) % len(zones)] if zones else None
                # A zone that is the world map's is skipped for other windows when there are more than two zones.
                mz = LAYOUT._map_zone()
                if nxt is not None and key != "worldmap" and nxt == mz and len(zones) > 2:
                    nxt = zones[(i + 2) % len(zones)]
                LAYOUT.assign_to(key, nxt)
                self.redraw()
                return True
        return False


class AlonePage(object):
    """The settings window of one module when it runs by itself, without the full suite.
    It shows the module's parts as tick boxes and its own settings page in a small window.
    Stops itself if the whole suite starts.
    """
    W = 460
    prof_stale = False
    mode = "alone"

    def __init__(self, s):
        """Creates the window object for module slot s."""
        self.s, self.want, self.dirty, self.parts, self.check_at = s, False, False, None, 0.0
        self.st = {"minimized": False, "shutting": False, "docked": False, "queue": []}
        self.win = {"g": None, "c": {}, "store": ({}, {})}
        self.wnd = Kit.Window(s.key + "_alone", s.title + " settings", self.st, self.win, self.build,
                              "VirtueAssistant_alone_pos", mini=(260, 46), lock=False, owner=False,
                              close_tip="Close these settings")

    def __getattr__(self, name):
        """Any other member read returns a function that does nothing, so the host can call this page like a
        ConfigWindow.
        """
        return lambda *args, **kw: None

    def api(self):
        """Returns the module's hooks if it has a settings page, else None."""
        return self.s.api if self.s.api and self.s.api.get("build_config") else None

    def show_settings(self, key):
        """Opens the window (the key is ignored, there is one page)."""
        self.want, self.st["minimized"] = True, False

    def refresh(self, key=None):
        """Marks the page for a rebuild."""
        self.dirty = True

    def rows(self):
        """Returns the form rows for the PARTS box, or an empty tuple for a module without parts."""
        return (("PARTS", [("check", p[0], p[1], p[2]) for p in self.s.parts]),) if self.s.parts else ()

    def build(self):
        """Builds the window: a form of tick boxes for the parts above the module's own settings page.
        The window height comes from the page's config_height hook. Client thread.
        """
        api, M = self.api(), Kit.MARGIN
        w = self.W - 2 * M
        top = M + 30 + Kit.GAP
        self.parts = None
        ph = Kit.Form.height(self.rows(), w)
        ph += Kit.GAP if ph else 0
        g, store, c = self.wnd.begin(self.W, top + ph + int(api["config_height"](w) or 0) + M)
        if not self.st["minimized"]:
            self.wnd.frame(g, settings=False)
            self.parts = Kit.Form(g, M, top, w, dict(self.s.parts_on), self.rows())
            api["build_config"](g, M, top + ph, w)
        self.wnd.end(g)

    def poll_parts(self):
        """Reads the part tick boxes and turns parts on or off in the host. At least one part must stay
        ticked (closing the window is how to turn the module off). The choice is saved in a persistent
        variable so it survives a restart.
        """
        s = self.s
        new = self.parts.read()
        changed = [k for k in new if s.parts_on.get(k) != new[k]]
        if changed and s.parts and not any(new.get(p[0], s.parts_on.get(p[0])) for p in s.parts):
            self.dirty = True
            API.SysMsg("%s: keep one part ticked; close the window to turn it off." % s.title, Kit.HUE_INFO)
            return
        for k in changed:
            HOST.part_set(s.key, k, new[k])
        if changed:
            Kit.put_var(ALONE_PARTS % s.key, ",".join(s.parts_wanted()))
            self.dirty = True

    def poll(self):
        """Script thread: stops this copy if the full suite has started, runs queued window actions,
        rebuilds when asked, closes on the close button and otherwise runs the page's poll_config.
        """
        now = time.time()
        # The suite check is made every two seconds, not every pass.
        if now >= self.check_at:
            self.check_at = now + 2.0
            if HOST.suite_alive():
                API.SysMsg("%s: %s started, so this copy stops." % (self.s.title, APP_NAME), Kit.HUE_INFO)
                HOST.disable(self.s.key)
                return
        if self.api() is None:
            return
        q = self.st["queue"]
        while q:
            action = q.pop(0)
            if action != "to_bar":
                self.wnd.action(action)
        if self.want or (self.dirty and self.win["g"] is not None):
            self.want = self.dirty = False
            self.build()
        if self.win["g"] is None:
            return
        if Kit.was_clicked(self.win["store"], "close"):
            self.close()
        elif not self.st["minimized"]:
            if self.parts is not None:
                self.poll_parts()
            try:
                self.s.api["poll_config"]()
            except Exception as ex:
                HOST._tell("%s: settings error: %s" % (self.s.title, ex))
                HOST.count_error(self.s, page=True)

    def close(self):
        """Closes the window after letting the page save through its config_closed hook."""
        if self.win["g"] is None:
            return
        if self.api().get("config_closed"):
            self.s.api["config_closed"]()
        self.wnd.close()


class HubWindow(object):
    """The shared window that holds the small tracker sections modules add (Ultima Tracker and similar).

    Sections are added and removed by their module; each brings height, build, poll and closed hooks.
    The window can minimise, dock into the action bar, or sit in a layout zone. Closing it turns the
    modules behind its sections off.
    """
    W = 372
    MINI_W, MINI_H = 240, 46

    def __init__(self, host):
        """Reads the saved place and minimised state and registers the window with the host's dock list."""
        self.host = host
        self.g = None
        self.H = 0
        self.sections = []
        self.stores = {}
        self.store = ({}, {})
        self.x, self.y = Kit.adapt(host.pref_int("hub_x", 100), host.pref_int("hub_y", 100), self.W, self.MINI_H)
        self.minimized = host.pref_int("hub_min", 0) == 1 or host.dock_wanted("hub")
        self.docked = self.dirty = self.closing = False
        self._gates = {}
        self.docked = self.minimized and host.dock_soon("hub")
        host.dock_add("hub", {"title": "Ultima Tracker", "icon": 0x1057, "always": True,
                              "state": self.state, "show": self.show, "dock": self.dock,
                              "undock": self.undock, "minimize": self.minimize, "on": self.open_modules,
                              "gump": lambda: self.g, "redraw": self.refresh})

    def add(self, key, title, hooks):
        """Adds a section (replacing one with the same key) and asks for a rebuild."""
        self.remove(key)
        self.sections.append((key, title, hooks))
        self.dirty = True

    def remove(self, key):
        """Removes a section; closes the window when it was the last one, else asks for a rebuild."""
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
        """Asks for a rebuild on the next poll."""
        self.dirty = True

    def title(self):
        """Returns the window title: the section's own title if there is only one, else Ultima Tracker."""
        return self.sections[0][1] if len(self.sections) == 1 else "Ultima Tracker"

    def state(self):
        """Returns "docked", "minimized" or "open", or None when nothing is showing."""
        if not self.sections or self.g is None:
            return None
        return "docked" if self.docked else ("minimized" if self.minimized else "open")

    def show(self):
        """Dock hook: shows the window normally."""
        self.docked = self.minimized = False
        self.dirty = True

    def dock(self):
        """Dock hook: folds the window into the action bar."""
        if not self.sections:
            return
        self.minimized = self.docked = True
        self.dirty = True

    def undock(self):
        """Dock hook: brings the window back out of the bar."""
        if self.docked:
            self.docked = False
            self._visible(True)

    def minimize(self):
        """Dock hook: minimises the window."""
        if not self.sections:
            return
        self.minimized, self.docked = True, False
        self.dirty = True

    def toggle_min(self):
        """Toggles between minimised and full (the title bar click)."""
        self.minimized = not self.minimized
        self.docked = False
        self.host.dock_forget("hub")
        self.dirty = True

    def open_modules(self):
        """Dock hook: asks the main window to show its Modules tab."""
        if self.host.config is not None:
            self.host.config.request_tab = "modules"

    def _visible(self, on):
        """Shows or hides the gump without destroying it."""
        g = self.g
        if Kit.is_open(g):
            Kit.set(g, "IsVisible", bool(on))

    def _pos(self):
        """Remembers the window's position, unless a layout zone is holding it."""
        g = self.g
        if Kit.is_open(g) and not self.host.layout_holds("hub"):
            with Kit.quiet:
                self.x, self.y = int(g.GetX()), int(g.GetY())

    def _leave(self):
        """Lets every section poll one last time and tell it is closing, then forgets their stores."""
        for key, title, hooks in self.sections:
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"):
                safe(lambda: hooks["poll"](st_))
            if key in self.stores and hooks.get("closed"):
                safe(hooks["closed"])
        self.stores = {}

    def _close_window(self):
        """Closes the window and drops its gump."""
        self._pos()
        self._leave()
        g, self.g = self.g, None
        Kit.dispose(g)
        self.docked = False

    def _part_of(self, key):
        """Returns (module key, part key) for a section key, mapping an old section name to the module and part
        that replaced it; a plain module key gives (key, None).
        """
        m = self.host.old_map.get(key)
        if m is not None and dict.get(self.host.by_key, m[0]) is not None:
            return m
        return key, None

    def _off(self, key):
        """Turns off the module or part a section belongs to."""
        mk, pk = self._part_of(key)
        self.host.disable(("%s.%s" % (mk, pk)) if pk is not None else key)

    def _error(self, key, ex):
        """Reports error ex of a section against its module."""
        mk, pk = self._part_of(key)
        s = dict.get(self.host.by_key, mk)
        if s is not None:
            self.host.report(s, ex, None, pk)

    def build(self):
        """Builds the window on the client thread with the hub's key bindings scoped."""
        Kit.on_client(lambda: Binds.scoped("va.hub", self._build))

    def _build(self):
        """Draws the window: minimised (a small bar), or the title row and every section stacked in order.
        A section that fails to build shows its error in red and is reported. A window held by a layout
        zone takes the zone's position and title bar. Client thread.
        """
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
        held = self.host.layout_holds("hub")
        close_tip = "Close %s (turns %s off; the Modules tab turns %s back on)" % (
            self.title(), "them" if len(self.sections) > 1 else "it", "them" if len(self.sections) > 1 else "it")
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
            heights = [max(20, int(safe(lambda: hooks["height"](IW), 40) or 40)) for key, t, hooks in self.sections]
            h = M + 30 + GAP + sum(heights) + GAP * (len(heights) - 1) + M
            Kit.add_window_frame(g, w, h, corners=False)
            if held:
                Kit.title_bar(g, store, w, self.title(), "hub", None, None)
            else:
                Kit.add_section(g, M, M, IW, 30)
                Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
                Kit.title_catcher(g, M, M, IW - 70 - Kit.DOCK_DX, 30, self.toggle_min, key="hub")
                Kit.dock_button(g, store, w - M - 66, M + 7)
                Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 66, M + 7, None, Kit.MIN_TIP)
                Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 44, M + 4, None, close_tip)
            y = M + 30 + GAP
            for (key, t, hooks), sh in zip(self.sections, heights):
                st_ = self.stores[key] = ({}, {})
                try:
                    Binds.scoped(key, hooks["build"], g, M, y, IW, st_)
                except Exception as ex:
                    Kit.add_section(g, M, y, IW, sh)
                    Kit.add_label(g, "%s: %s" % (t, ex), M + 10, y + 10, Kit.HUE_BAD)
                    self._error(key, ex)
                y += sh + GAP
        if held:
            xy = LAYOUT.spot("hub") or (self.x, self.y)
            g.SetPos(int(xy[0]), int(xy[1]))
        else:
            self.x, self.y = Kit.place(g, self.x, self.y, w, h)
        self.H = h
        self.g, self.store = g, store
        G.AddControlOnDisposed(g, lambda *a: self._disposed(g))
        Kit.replace_gump(old, g, self.docked)
        if not held:
            g.SetInScreen()
        Kit.on_moved(g, self._moved)
        Kit.dispose(old)

    def _moved(self):
        """Move event: remembers the new place and saves it."""
        self._pos()
        self.host.save_prefs()

    def _disposed(self, g):
        """The player closed the gump: tells every section it closed and turns each one off."""
        if self.g is g and not self.closing:
            self.g = None
            self.stores = {}
            for key, t, hooks in list(self.sections):
                safe(hooks.get("closed", lambda: None))
                self._off(key)

    def store_prefs(self, prefs):
        """Writes the window's place and minimised state into prefs."""
        if Client.on_client_thread():
            self._pos()
        prefs["hub_x"], prefs["hub_y"] = str(self.x), str(self.y)
        prefs["hub_min"] = "1" if self.minimized else "0"

    def close(self):
        """Closes the window for good (used when the script stops)."""
        self.closing = True
        self._close_window()

    def poll(self):
        """Script thread poll: rebuilds when asked, handles the close, minimise and dock buttons, and
        gives each section its poll hook when it is due. A failing section is reported and the rest go on.
        """
        if self.closing:
            return
        if self.dirty:
            self.build()
            if self.sections and self.host.pref_int("hub_min", 0) != int(self.minimized):
                self.host.save_prefs()
        g = self.g
        if g is None:
            return
        if not Kit.is_open(g):
            self.g = None
            return
        if Kit.clicks_seen and True not in self.store[1].values():
            pass
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
            return
        for key, t, hooks in list(self.sections):
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"):
                gate = self._gates.get(key)
                if gate is None:
                    gate = self._gates[key] = [0.0]
                if not self.host.poll_due(gate, hooks.get("poll_every")):
                    continue
                try:
                    hooks["poll"](st_)
                except Exception as ex:
                    self._error(key, ex)


class Launcher(object):
    """The Quick Launcher: a small window with a text box that finds Grimoire runes, Action Bar cells and
    outfits, windows, window layouts, settings options and a few commands as the player types, and runs
    the one picked (Enter runs the top row, a click runs that row).

    The window is built on the client thread and polled from the script thread by the host. Other
    modules are reached only through the host's services table, so a module that is off simply gives
    no rows. The last runs of the session are kept in recent.
    """
    W = 560
    ROWS = 8
    ROW = 28
    SETTLE = 0.15
    RECENT = 5
    POS_KEY = "VirtueAssistant_launcher_pos"
    ONCE = "va.launcher.run"
    GAP = 0.6
    SOON = "too soon after the last run; press again."
    TITLE = "QUICK LAUNCHER"
    TIP = "Quick launcher: find a rune, cell, window or option"
    NAME = "Quick Launcher"
    ENTER_OFF = "launcher_Enter_key"
    ORDER = ("rune", "cell", "window", "layout", "option", "command")
    FIELD_TIP = "Type words to find something; Enter runs the top row"
    HINT = "Type to find a rune, cell, window, layout, option or command"
    RUN = "Enter runs the top row; click a row to run it"
    CLICK = "Click a row to run it"

    def __init__(self, host):
        """Sets up empty state. toggle and go are debounced entry points (Kit.once), so a repeated hotkey or
        click inside the short guard time is ignored.
        """
        self.host = host
        self.g = self.tb = self.ver = self.pick = None
        self.store = ({}, {})
        self.rows = []
        self.recent = []
        self.text = self.shown = self.status = ""
        self.typed_at = 0.0
        self.enter = self.hooked = False
        self.toggle = Kit.once(self._toggle_req, "va.launcher", 0.4)
        self.go = Kit.once(self._go, self.ONCE, self.GAP)

    def _toggle_req(self):
        """Called from a hotkey or button on any thread: queues the toggle for the client thread and wakes the
        host.
        """
        Kit.pending.append(self._toggle)
        self.host.poke()

    def _toggle(self):
        """Client thread: closes the launcher if it is open, otherwise starts it with an empty box and builds
        the window.
        """
        if Kit.is_open(self.g):
            self.close()
            return
        self.text = self.shown = ""
        self.typed_at = 0.0
        self.enter = False
        self.ver = None
        self.rows, self.status = self.find("")
        Binds.scoped("va.launcher", self._build)

    @staticmethod
    def score(words, text, extra=""):
        """Returns how well text matches every word in words, or 0 if any word is missing. A word scores 3
        when a word of the text starts with it, 2 when it is found inside the text and 1 when it is found
        only in extra. The scores are added.
        """
        low = text.lower()
        starts = low.replace("(", " ").replace(">", " ").split()
        more = extra.lower()
        total = 0
        for w in words:
            pts = 3 if any(s.startswith(w) for s in starts) else 2 if w in low else 1 if w in more else 0
            if not pts:
                return 0
            total += pts
        return total

    def zones_on(self):
        """Returns True when the Interface module (owner of window layouts) is running."""
        s = dict.get(self.host.by_key, LAYOUT_OWNER)
        return s is not None and s.running

    def windows(self):
        """Returns the windows the launcher can show, as ((module key, dock keys), title). A module without
        parts is one entry; a module with parts gives one entry per part. The dock keys are the names the
        host's dock records may know the window by, tried in order.
        """
        out = []
        slots = [s for s in self.host.slots if s.api is not None or s.lazy is not None]
        mine = [p[0] for s in slots for p in s.parts]
        for s in slots:
            if not s.parts:
                out.append(((s.key, (s.key,)), s.title))
                continue
            for p in s.parts:
                key = "%s.%s" % (s.key, p[0])
                docks = tuple(p[4][:1]) if len(p) > 4 else ()
                # A part may be known to the dock table by its own key, by the module and part key, or by the bare
                # part key when no other module uses that name.
                docks += (key,) + ((p[0],) if mine.count(p[0]) == 1 and p[0] not in self.host.by_key else ())
                out.append(((key, docks), s.part_title(p[0])))
        return out

    def commands(self):
        """Returns the commands the launcher offers as (key, caption) pairs; the quiet command changes its
        caption while alerts are quiet.
        """
        return (("history", "Alert history"),
                ("quiet", "Resume alerts" if ALERTS.quiet_on() else "Quiet alerts for 30 minutes"),
                ("backup", "Back up settings now"), ("settings", "Settings"), ("news", "What's new"))

    def options(self, words):
        """Returns ([(index entry, text)], all pages read) for the options whose page, section, caption or
        tip contains every word. Reads the window's option index, so it has nothing until the settings
        pages have been indexed; the flag says whether every page has been.
        """
        c = self.host.config
        if c is None or c.mode == "alone":
            return [], True
        pages = c.settings_slots()
        out = []
        for s in pages:
            for e in c.opt_index.get(s.key, ()):
                hay = " ".join((s.title, e[2], e[4], e[5], "option")).lower()
                if e[3] != "note" and all(w in hay for w in words):
                    out.append((e, c._hit_text(e)))
        return out, all(s.key in c.opt_index for s in pages)

    def ask(self, name, q, n=None):
        """Calls the host service name with query q and at most n rows (ROWS by default). Returns its list, or
        an empty tuple when the module is off or the call fails.
        """
        fn = self.host.services.get(name)
        return (safe(lambda: fn(q, n or self.ROWS), None) or ()) if fn is not None else ()

    def find(self, q):
        """Returns (rows, status line) for the query q. A row is (label, kind, data, tip), at most ROWS of
        them, best score first, then kind in ORDER, then the order found. An empty query gives the recent
        runs, or a hint when there are none.

        Runes and cells come from their modules' own search, so they are kept even when the label scores
        nothing; every other kind must match every word.
        """
        words = str(q or "").lower().split()
        if not words:
            if self.recent:
                return list(self.recent), "Your last runs this session"
            return [], self.HINT
        found = []

        def add(label, kind, data, tip, extra="", pre=False):
            """Adds one candidate row when it scores for the words (or when pre is True, the source having matched
            already).
            """
            # A row from a module's own search keeps a score of at least one per word even if its label does not
            # match.
            sc = self.score(words, label, extra) or (len(words) if pre else 0)
            if sc:
                found.append((-sc, self.ORDER.index(kind), len(found), (label, kind, data, tip)))

        for label, tok in self.ask("grimoire.find", q):
            add("Rune: " + label, "rune", tok, "Travel to %s" % label, "rune", True)
        for label, ref, kind in self.ask("actionbar.find", q):
            head = "Outfit" if kind == "outfit" else "Cell"
            add("%s: %s" % (head, label), "cell", (ref, label), "Use %s" % label, "cell " + kind, True)
        for key, title in self.windows():
            s = self.host.by_key.get(key[0])
            on = s is not None and s.running
            add("Window: " + title, "window", key, ("Show %s" if on else "Turn %s on") % title, "window")
        if self.zones_on():
            for name in [LAYOUT_DEFAULT, LAYOUT_MIRRORED] + list(LAYOUT.layout_names()):
                add("Layout: " + name, "layout", name, 'Use the window layout "%s"' % name, "layout")
        opts, done = self.options(words)
        for e, text in opts:
            add("Option: " + text, "option", e, e[5] or "Open %s" % text, e[5] + " option")
        for key, cap in self.commands():
            add(cap, "command", key, cap, "command")
        found.sort(key=lambda f: f[:3])
        rows = [f[3] for f in found[:self.ROWS]]
        if not done:
            return rows, "Still reading settings pages; options appear as they are read"
        if not rows:
            return rows, 'Nothing matches "%s"' % str(q).strip()
        return rows, self.RUN

    def _build(self):
        """Client thread: builds the launcher window for the current rows and status, replaces the old one in
        the same place (or centres a new one at the saved or default spot), and puts the text caret back.
        """
        M, W, GAP = Kit.MARGIN, self.W, Kit.GAP
        s = Kit.tscale
        RH = Kit.pitch(self.ROW)
        rows = self.rows
        old = self.g
        store = ({}, {})
        yb = M + 30 + GAP
        yr = yb + 44
        caret = self._caret()
        h_body = 44 + RH * len(rows) + 28
        H = yb + h_body + M
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H)
        Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, self.TITLE, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close")
        Kit.add_section(g, M, yb, W - 2 * M, h_body)
        tb = Kit.add_textbox(g, self.text, M + 12, yb + 10, W - 2 * M - 24, numbers=False)
        self.hooked = self._hook(tb)
        Kit.with_tip(tb, self.FIELD_TIP if self.hooked else self.FIELD_TIP.split(";")[0])
        for i, r in enumerate(rows):
            Kit.art_button(g, store, "run%d" % i, Kit.ART_PLAY, M + 12, yr + RH * i, Kit.fit(r[0], W - 2 * M - 70),
                           r[3])
        text = self.status if self.hooked or self.status != self.RUN else self.CLICK
        Kit.add_label(g, Kit.fit(text, W - 2 * M - 24), M + 12, yr + RH * len(rows) + 4, Kit.HUE_INFO)
        sc = s if Kit.scale_window(g, s) else 1.0
        WS, HS = int(round(W * sc)), int(round(H * sc))
        if Kit.is_open(old):
            x, y = int(old.GetX()), int(old.GetY())
        else:
            sw = Kit.screen()[0] or 1024
            x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 120), (WS, HS))
        Kit.place(g, x, y, WS, HS, int(round(yb * sc)))
        Kit.add_front(g)
        Kit.on_moved(g, lambda: Kit.save_pos(self.POS_KEY, self.g))
        self.g, self.tb, self.store = g, tb, store
        Kit.dispose(old)
        safe(tb.SetFocus)
        self._put_caret(tb, caret)

    def _caret(self):
        """Returns the caret position of the text box if it can be read, else None."""
        with Kit.quiet:
            n = int(self.tb.CaretIndex)
            if 0 <= n < len(self.text):
                return n
        return None

    @staticmethod
    def _put_caret(tb, n):
        """Puts the caret of text box tb back at n (nothing when n is None)."""
        if n is None:
            return
        with Kit.quiet:
            Kit.client_control(tb).TextBox.CaretIndex = n

    def _hook(self, tb):
        """Hooks the box's Enter key by reflection on the client control, so Enter can run the top row.
        Returns False if it is switched off for this character or the control has no such event; the
        status line then tells the player to click a row.
        """
        if self.ENTER_OFF in self.host.tz_off:
            return False
        try:
            # The client's text box exposes Enter only as an event on its control, so the handler is attached
            # by reflection.
            import clr
            import System
            c = Kit.client_control(tb)
            ev = c.GetType().GetEvent("EnterPressed")
            h = clr.GetPythonType(ev.EventHandlerType)(self._enter_hit)
            ev.GetAddMethod(True).Invoke(c, System.Array[object]([h]))
            return True
        except Exception:
            return False

    def _enter_hit(self, sender=None, e=None):
        """Enter handler: sets the flag poll reads and wakes the host."""
        self.enter = True
        self.host.poke()

    def rebuild(self):
        """Saves the window's place and builds it again, for new rows or a new status line."""
        if Kit.is_open(self.g):
            Kit.save_pos(self.POS_KEY, self.g)
            Binds.scoped("va.launcher", self._build)

    def poll(self, now):
        """Script thread, every pass while the window is open: closes it when the player did, reads the typed
        text, runs Enter or a clicked row, and searches again once typing has paused for SETTLE seconds or
        the option index has grown. The window is rebuilt only when the rows or status changed.
        """
        if not Kit.is_open(self.g) or Kit.was_clicked(self.store, "close"):
            self.close()
            return
        try:
            t = str(self.tb.Text or "")
        except Exception:
            t = self.text
        if t != self.text:
            self.text, self.typed_at = t, now
        if self.enter:
            self.enter = False
            self.rows, self.status = self.find(self.text)
            self.shown = self.text
            if self.rows:
                self.run(0, True)
            else:
                self.rebuild()
            return
        for i in range(len(self.rows)):
            if Kit.was_clicked(self.store, "run%d" % i):
                self.run(i)
                return
        c = self.host.config
        words = self.text.split()
        if words and c is not None and c.mode != "alone":
            safe(c._index_tick)
        ver = c.opt_ver if c is not None and c.mode != "alone" else 0
        if (self.text != self.shown and now - self.typed_at >= self.SETTLE) or (words and ver != self.ver):
            rows, status = self.find(self.text)
            self.shown, self.ver = self.text, ver
            if rows != self.rows or status != self.status:
                self.rows, self.status = rows, status
                self.rebuild()

    def run(self, i, enter=False):
        """Runs row i of the list. Refused with a message when the last run was under GAP seconds ago.
        enter says the row was chosen with Enter. The window closes first, then the run goes through go.
        """
        if not 0 <= i < len(self.rows):
            return
        # A second run inside GAP seconds is refused (Kit._fired holds the last run's time).
        if 0.0 <= time.time() - Kit._fired.get(self.ONCE, 0.0) < self.GAP:
            self.say(self.SOON)
            return
        self.pick = (self.rows[i], enter)
        self.close()
        self.go()

    def _go(self):
        """Runs the picked row according to its kind and keeps it in recent when it worked. Returns whether it
        did. A module that is off, or a cell that has changed since it was listed, is refused with a
        message.
        """
        row, enter = self.pick
        label, kind, data = row[0], row[1], row[2]
        sv = self.host.services
        ok = False
        if kind == "rune":
            fn = sv.get("grimoire.go")
            ok = fn is not None and bool(fn(data))
            if fn is None:
                self.say("Grimoire is off.")
        elif kind == "cell":
            fn = sv.get("actionbar.use")
            ref, cap = data
            name = cap.rsplit("  (", 1)[0]
            if fn is None:
                self.say("the Action Bar is off.")
            # Cells can change while the list is open, so the cell is looked up again by name and refused if it
            # is gone.
            elif (cap, ref) not in [r[:2] for r in self.ask("actionbar.find", name, 200)]:
                self.say("%s is no longer on the Action Bar." % name)
            else:
                if enter:
                    # Enter can only arm the harmful-cursor confirm, never confirm it, so the pending confirm is
                    # cleared.
                    self.host.harm_conf = (None, 0, 0.0)
                ok = bool(fn(ref))
        elif kind == "window":
            ok = self._window(data)
        elif kind == "layout":
            ok = self.zones_on()
            if ok:
                LAYOUT.use_windows(data)
            else:
                self.say("window layouts need the Interface module on.")
        elif kind == "option":
            ok = self._option(data)
        else:
            ok = self._command(data)
        if ok:
            self.recent = [row] + [r for r in self.recent if r[1:3] != row[1:3]]
            del self.recent[self.RECENT:]
        return ok

    def say(self, text):
        """Prints one launcher line to the journal in the warning colour."""
        API.SysMsg("%s: %s" % (self.NAME, text), Kit.HUE_BAD)

    def _window(self, key):
        """Shows or turns on the window of key = (module key, dock keys). A module that is off is turned on;
        a window that is closed is shown through its dock record. Returns False when the module is gone.
        """
        part, keys = key
        s = self.host.by_key.get(part)
        docks = dict(self.host.docks)
        if s is None:
            self.say("that window is no longer loaded.")
            return False
        dk = next((k for k in keys if k in docks), keys[0])
        if not s.running:
            self.host.dock_forget(dk)
            self.host.enable(part)
            return True
        d = docks.get(dk)
        if d is not None and safe(d.get("state")) != "open":
            safe(d.get("show"))
            self.host.dock_forget(dk)
        return True

    def _option(self, e):
        """Opens the settings page of option entry e with the option marked, through the main window.
        Returns False when there is no full window or the page is gone.
        """
        c = self.host.config
        if c is None or c.mode == "alone" or self.host.page_slot(e[0]) is None:
            return False
        c.opt_open, c.opt_mark = True, (e[0], e[1], e[6] if e[6] is not None else e[4], e[3])
        c.show_settings(e[0])
        return True

    def _command(self, key):
        """Runs a launcher command: alert history, quiet alerts, a settings backup, the Settings tab or the
        what's new window. Returns False if it could not run.
        """
        h = self.host
        if key == "history":
            h.alert_log.open()
        elif key == "quiet":
            ALERTS.toggle_quiet()
        elif key == "backup":
            BackupPage.ask(("backup", "by hand"))
        elif key == "settings":
            if h.config is None:
                return False
            h.config.request_tab = "settings"
        elif key == "news":
            return h.whats_new.show()
        return True

    def close(self):
        """Closes the window, saving where it stood."""
        g, self.g, self.tb = self.g, None, None
        self.enter = False
        if Kit.is_open(g):
            Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)
        self.store = ({}, {})


SNAP_DIST = 16
SNAP_SETTLE = 0.25
SNAP_EVERY = 0.08
SNAP_PRUNE = 2.0


class Snap(object):
    """Watches every Virtue Assistant window for dragging and keeps them tidy on screen.

    When a window is dropped near another it snaps to its edge or corner and becomes linked to it, so
    dragging the leader carries the followers. It also snaps to screen edges, anchors and the grid,
    keeps windows on screen after a resolution change, and tells the layout code (LAYOUT) about drops.
    tick() runs from the script thread; windows are read and moved through Kit helpers.
    """
    def __init__(self):
        """Sets up empty tracking tables. Snapping is on by default."""
        self.gumps = []
        self.members = set()
        self.last = None
        self.drag = {}
        self.links = {}
        self.button = None
        # The player's snap setting is applied by the settings window.
        self.enabled = True
        self.next = 0.0
        self.prune_at = 0.0
        self.moved_cb = {}
        self.moved = set()
        self.attached = {}
        self._fmap = None
        self.no_snap = set()
        self.keep_at = 0.0
        self.screen = None
        self.by_code = {}
        self.dragged = set()
        self.droppers = []
        self.drag_end = {}
        self.drag_key = {}
        self.drag_rect = {}
        self.lost = {}
        self.down = True
        self.sweep_at = 0.0
        self.keep_sig = None

    def add(self, g):
        """Starts tracking gump g (once)."""
        if g is not None and g not in self.members:
            self.members.add(g)
            self.gumps.append(g)

    def on_moved(self, g, fn):
        """Registers gump g and a function called after the player moves it."""
        if g is None:
            return
        if g not in self.attached:
            self.add(g)
        self.moved_cb[g] = fn

    def on_drop(self, fn):
        """Registers a function called with the gump after a drag ends (or with None, key and rect when the
        dragged gump vanished mid drag).
        """
        if fn not in self.droppers:
            self.droppers.append(fn)

    def _tell_moved(self):
        """Tells the owners of moved gumps that they moved, and the drop listeners which gump was dropped.
        A gump that was dragged and then closed is reported by its layout key and last rectangle instead.
        """
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
            self.drag_end[g] = now
        # Drag end times are only needed briefly; old ones are pruned once the table grows.
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
                    except Exception:
                        pass
                continue
            if keys.get(g) is not None and rects.get(g) is not None:
                lost[g] = (keys[g], rects[g])
        done = set()
        for g, (key, r) in lost.items():
            if key in done:
                continue
            done.add(key)
            for fn in self.droppers:
                try:
                    fn(None, key=key, rect=r)
                except Exception:
                    pass

    def moved_by_code(self, g):
        """Records that code (not the player) moved gump g, so the new place is not mistaken for a drag."""
        if g is None:
            return
        p = self.pos(g)
        if self.last is not None and p is not None:
            self.last[g] = p
        self.drag.pop(g, None)
        self.moved.discard(g)
        self.by_code[g] = time.time()

    def skip_gump(self, g, keep_fresh=False):
        """Stops tracking gump g for snapping and following. keep_fresh leaves its new-window layout entry alone."""
        if not keep_fresh:
            LAYOUT.fresh_adds.discard(g)
        if g in self.members:
            self.members.discard(g)
            self.gumps.remove(g)

    def exempt(self, g):
        """Excludes gump g from snapping: it neither snaps nor is snapped to, and links to it are dropped."""
        if g is None:
            return
        self.add(g)
        self.no_snap.add(g)
        self.links.pop(g, None)
        for f, l in list(self.links.items()):
            if l is g:
                self.links.pop(f, None)

    def attach(self, follower, leader):
        """Makes follower move with leader and removes the follower from normal snapping."""
        if follower is None or leader is None or follower is leader:
            return
        self.skip_gump(follower, keep_fresh=True)
        self.attached[follower] = leader
        self._fmap = None
        self.add(leader)

    def detach(self, follower):
        """Releases follower so it snaps like any other window again, if it is still open."""
        self._fmap = None
        if self.attached.pop(follower, None) is not None and Kit.is_open(follower):
            self.add(follower)

    def followers(self, g):
        """Returns the gumps attached to leader g. Uses the map built for the current pass when there is one;
        otherwise scans, forgetting closed gumps on the way.
        """
        fm = self._fmap
        if fm is not None:
            lst = fm.get(g)
            return list(lst) if lst else []
        out = []
        for f, l in list(self.attached.items()):
            if not Kit.is_open(f):
                self._forget(f)
            elif l is g:
                out.append(f)
        return out

    def _forget(self, g):
        """Drops every record of gump g, and of anything attached to it. A dragged gump's last key and
        rectangle are kept so the drop can still be reported.
        """
        if g in self.dragged:
            k, r = self.drag_key.get(g), self.drag_rect.get(g)
            if k is not None and r is not None:
                self.lost[g] = (k, r)
        for d in (self.drag_key, self.drag_rect, self.drag, self.by_code, self.links, self.moved_cb):
            d.pop(g, None)
        for s in (self.members, Kit._pinned, self.moved, self.dragged, self.no_snap):
            s.discard(g)
        self._fmap = None
        self.attached.pop(g, None)
        for f, l in list(self.attached.items()):
            if l is g:
                self.attached.pop(f, None)
        if self.last is not None:
            self.last.pop(g, None)

    def _prune(self):
        """Forgets gumps that have closed and returns the list of open ones."""
        live = []
        for g in self.gumps:
            if Kit.is_open(g):
                live.append(g)
            else:
                self._forget(g)
        self.gumps = live
        return live

    def pressed(self):
        """Returns True or False for whether the left mouse button is held, or None when the client does not
        say. The client's mouse getter is found by reflection once and cached.
        """
        if self.button is None:
            self.button = False
            try:
                m = Client._member(Client._type("ClassicUO.Input.Mouse"), "LButtonPressed")
                bool(m[0]())
                self.button = m[0]
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
        """Returns the (x, y, width, height) of gump g, or None if it has no usable size."""
        r = Kit.rect(g)
        return r if r is not None and r[2] > 0 and r[3] > 0 else None

    @staticmethod
    def pos(g):
        """Returns the (x, y) of gump g."""
        return Kit.pos(g)

    @staticmethod
    def visible(g):
        """True if gump g is visible."""
        return bool(g.IsVisible)

    @staticmethod
    def move(g, x, y):
        """Moves gump g to x, y and notes its new rectangle."""
        g.SetPos(int(x), int(y))
        Kit.note_rect(g, x, y)

    def tick(self, now=None):
        """Script thread, rate limited to SNAP_EVERY seconds (every pass while the script is starting). One
        pass of dragging and tidying.

        Escape leaves layout arrange mode. While the mouse is up it runs keep() on a timer (or when the set
        of windows changed) to keep windows on screen; while starting it also retries windows that wait for
        the seamless fit. While a button is down it compares each gump's place with the last pass: a
        changed place is a drag, which carries followers and updates arrange hover; a gump that stopped
        moving (button released, or still for SNAP_SETTLE when the button state is unknown) is snapped.
        Moves made by code are skipped so they are not taken for drags.
        """
        now = time.time() if now is None else now
        boot = HOST.booting()
        if now < self.next and self.next - now <= SNAP_EVERY and not boot:
            return
        self.next = now + SNAP_EVERY
        if LAYOUT.arrange and not self.drag and API.IsKeyPressed("ESCAPE"):
            LAYOUT.set_arrange(False)
        pressed = self.pressed()
        self.down = pressed is not False or bool(self.drag)
        if pressed is not True:
            if now >= self.keep_at:
                self.keep_at = now + (0.0 if boot else KEEP_EVERY)
                if now >= self.sweep_at or self._keep_sig() != self.keep_sig:
                    self.sweep_at = now + KEEP_SWEEP
                    self.keep()
                    self.keep_sig = self._keep_sig()
                # While starting, windows waiting for the seamless fit are retried on every pass.
                elif boot and LAYOUT.assign and LAYOUT.retry_due(now):
                    self.keep(light=bool(LAYOUT.fresh_adds) and not LAYOUT.fresh)
            elif LAYOUT.assign and (LAYOUT.fresh or LAYOUT.fresh_adds or LAYOUT.retry_due(now)):
                self.keep(light=bool(LAYOUT.fresh_adds) and not LAYOUT.fresh)
        # With the button up and nothing dragged there is nothing to compare; only prune now and then.
        if pressed is False and not self.drag:
            self.last = None
            if now >= self.prune_at:
                self.prune_at = now + SNAP_PRUNE
                self._prune()
            return
        if pressed is not True or now >= self.prune_at:
            self.prune_at = now + SNAP_PRUNE
            live = self._prune()
        else:
            live = self.gumps
        last = self.last
        if last is None:
            last = self.last = {}
            for g in live:
                p = self.pos(g)
                if p is not None:
                    last[g] = p
            return
        drag = self.drag
        by_code = self.by_code
        if by_code:
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
                if by_code and g in by_code:
                    del by_code[g]
                    continue
                if pressed is False:
                    continue
                drag[g] = now
                self.moved.add(g)
                self.dragged.add(g)
                r = None
                if LAYOUT.loaded:
                    if g not in self.drag_key:
                        self.drag_key[g] = LAYOUT._key_of(g)
                    r = self.rect(g)
                    if r is not None:
                        self.drag_rect[g] = r
                if LAYOUT.arrange:
                    LAYOUT.arrange_hover(g, r)
                if self.enabled and g not in self.no_snap and g not in LAYOUT.held:
                    self.follow(g, dx, dy, set([g]))
            elif g in drag:
                if pressed is False or (pressed is None and now - drag[g] >= SNAP_SETTLE):
                    del drag[g]
                    if self.enabled and g not in self.no_snap and not LAYOUT.takes(g):
                        self.snap(g, live)
        if (self.moved or self.lost) and not drag:
            self._tell_moved()

    def follow(self, leader, dx, dy, seen):
        """Moves every window linked to leader by the same offset (dx, dy), and theirs in turn. seen stops loops.
        A window held by a layout zone leaves the link.
        """
        links = self.links
        if not links:
            return
        held = LAYOUT.held
        for g in self.gumps:
            if g in seen or links.get(g) is not leader:
                continue
            if g in held:
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
        """Snaps gump g to its neighbours after a drag, building the follower map for the duration."""
        if self._fmap is not None:
            return self._snap(g, live)
        self._build_fmap()
        try:
            return self._snap(g, live)
        finally:
            self._fmap = None

    def _snap(self, g, live):
        """Moves gump g to the nearest edge or corner of another visible window within SNAP_DIST, or to the
        screen edge, anchor or grid line if there is none, and links it to the window it snapped to.
        Corners win over single edges; an edge only counts if the two windows overlap on the other axis.
        """
        r = self.rect(g)
        if r is None:
            return
        x, y, w, h = r
        corner = None
        ex = ey = None
        links = self.links
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
            for tx, ty in ((ox + ow, oy), (ox + ow, oy + oh - h), (ox - w, oy),
                           (ox - w, oy + oh - h), (ox, oy + oh), (ox + ow - w, oy + oh),
                           (ox, oy - h), (ox + ow - w, oy - h)):
                d = max(abs(x - tx), abs(y - ty))
                if d <= SNAP_DIST and (corner is None or d < corner[0]):
                    corner = (d, tx, ty, lead)
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
            links.pop(g, None)
            nx, ny = self.snap_screen(x, y, w, h)
        else:
            links[g] = leader
        nx, ny = Kit.clamp(nx, ny, w, h)
        if (nx, ny) != (x, y):
            self.move(g, nx, ny)
            if self.last is not None:
                self.last[g] = (nx, ny)
            self.follow(g, nx - x, ny - y, set([g]))

    def _keep_sig(self):
        """Returns a value that changes when anything affecting the keep-on-screen pass changes (screen
        size, windows, their rectangles and visibility, occupied zones). While something is moving it
        always returns a new object so the pass is not skipped.
        """
        if self.down or Kit._pend or LAYOUT.arrange or LAYOUT.dirty or LAYOUT.fresh or LAYOUT.fresh_adds:
            return object()
        out = [Kit.screen(), safe(LAYOUT.occupied)]
        for g in self.gumps + list(self.attached) + [cw for cw in ClientWin.found.values() if cw is not None]:
            try:
                out.append((id(g), Kit.is_open(g), Kit.rect(g), bool(g.IsVisible)))
            except Exception:
                out.append(id(g))
        return out

    def keep(self, light=False):
        """Keeps every window on screen and inside its zone, and re-runs the layout for the current screen.
        light limits the pass to windows just added.
        """
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return
        live = self._prune()
        Kit.prune_pending()
        try:
            self._keep_body(W, H, live, light)
        finally:
            self._fmap = None

    def _build_fmap(self):
        """Builds the leader to followers map once for a pass."""
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
        """The work of keep(): if the screen size changed, moves every window to the same relative place;
        then clamps each window (with its followers) onto the screen and lets LAYOUT arrange its zones.
        A layout error is reported to the player and does not stop the pass.
        """
        self._build_fmap()
        new = None
        if light:
            new = set(LAYOUT.fresh_adds)
            att = self.attached
            for g in list(new):
                l = att.get(g)
                if l is not None:
                    new.add(l)
        try:
            Kit.scroll_sweep()
        except Exception:
            pass
        old = self.screen
        if old != (W, H):
            new = None
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
            Kit.note_screen((W, H))
        held = LAYOUT.held
        for g in live:
            if new is not None and g not in new:
                continue
            if g not in self.drag and g not in held:
                self.keep_one(g)
        try:
            LAYOUT.keep(W, H, new)
        except Exception as ex:
            HOST._tell("%s: layout error: %s%s" % (APP_NAME, ex, _error_where()))
        if (self.moved or self.lost) and not self.drag:
            self._tell_moved()

    def keep_one(self, g):
        """Clamps gump g and its visible followers as one block onto the screen. Returns True if it moved.
        A window hidden behind a zone tab is left alone.
        """
        r = self.rect(g)
        if r is None or (Kit._behind and self.attached.get(g) in Kit._behind):
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
        """Moves gump g and its followers by (dx, dy)."""
        for w in [g] + self.followers(g):
            p = self.pos(w)
            if p is None:
                continue
            self.move(w, p[0] + dx, p[1] + dy)
            if self.last is not None:
                self.last[w] = (p[0] + dx, p[1] + dy)
        self.moved.add(g)

    @staticmethod
    def near_anchor(x, y, w, h):
        """Returns (distance, x, y) of the nearest anchor point for a window at x, y of size w by h, or None
        if none is within SNAP_ANCHOR.
        """
        found = [(max(abs(ax - x), abs(ay - y)), ax, ay) for ax, ay in Kit.anchor_targets(w, h)]
        best = min(found, key=_first) if found else None
        return best if best is not None and best[0] <= SNAP_ANCHOR else None

    def snap_screen(self, x, y, w, h):
        """Returns the place a window dropped at x, y should take: the nearest anchor, else the screen edges
        within SNAP_DIST, then grid lines when the grid is on.
        """
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            return x, y
        best = Snap.near_anchor(x, y, w, h)
        if best is not None:
            return best[1], best[2]
        nx, ny = x, y
        for tx in (0, max(0, W - w)):
            if abs(tx - x) <= SNAP_DIST:
                nx = tx
        for ty in (0, max(0, H - h)):
            if abs(ty - y) <= SNAP_DIST:
                ny = ty
        if HOST.grid_shown():
            step = HOST.grid_size()

            def on_line(lo, size, cur):
                """Returns the grid line near the edge lo (or the far edge lo + size) if within SNAP_DIST and the
                window has not already snapped on this axis; otherwise returns cur.
                """
                cands = []
                for edge, back in ((lo, 0), (lo + size, size)):
                    line = int(round(float(edge) / step)) * step
                    if abs(line - edge) <= SNAP_DIST:
                        cands.append((abs(line - edge), line - back))
                return min(cands)[1] if cands and cur == lo else cur

            nx, ny = on_line(x, w, nx), on_line(y, h, ny)
        return nx, ny


class Grid(object):
    """The screen grid overlay that the action bar's Grid button shows, so windows can be lined up.
    It draws thin lines every grid step (stronger every fourth), the screen centre and the anchor
    points, behind the other windows, and redraws when the screen size or step changes.
    """
    MINOR, MAJOR = 0.16, 0.34
    CROSS, MARK = 0.55, 0.75
    MARK_W = 10

    def __init__(self, host):
        """Starts hidden. host supplies the grid size."""
        self.host = host
        self.g = None
        self.shown = False
        self.drawn = None

    @staticmethod
    def show_overlay(g, x, y, w, h, under=False):
        """Puts overlay gump g at x, y with size w by h as a click-through, immovable window (behind the
        others when under is set) and removes it from snapping. Client thread.
        """
        g.SetRect(x, y, w, h)
        g.SetAcceptMouseInput(False)
        g.CanMove = False
        if under:
            with Kit.quiet:
                import System
                g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
        Kit.add_front(g)
        SNAP.skip_gump(g)

    def toggle(self):
        """Shows the grid if hidden, hides it if shown."""
        self.hide() if self.shown else self.show()

    def show(self):
        """Shows the grid, building it on the client thread."""
        self.shown = True
        Kit.on_client(self.build)

    def hide(self):
        """Hides the grid and disposes its gump."""
        self.shown = False
        g, self.g = self.g, None
        Kit.dispose(g)

    def redraw(self):
        """Rebuilds the grid if it is showing."""
        if self.shown:
            Kit.on_client(self.build)

    def tick(self):
        """Rebuilds the grid when the screen size or grid step differs from what was drawn."""
        if self.shown and self.drawn is not None:
            W, H = Kit.screen()
            if (W, H, self.host.grid_size()) != self.drawn:
                self.redraw()

    def build(self):
        """Draws the grid over the whole screen on the client thread: lines, the gold centre cross, the anchor
        marks and a caption saying what it is for.
        """
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
        for ax, ay in Kit.anchor_targets(m, m):
            Kit.add_box(g, ax, ay, m, m, self.MARK, "#FFD700")
        Kit.add_label(g, "GRID %d px: windows snap to its lines, the screen's corners, edges and centre  (the Action "
                      "Bar's Grid button hides it)" % step, m + 8, m + 4, Kit.HUE_TITLE)
        self.g = g
        self.drawn = (W, H, step)
        Grid.show_overlay(g, 0, 0, W, H, True)
        Kit.dispose(old)


# Names of the saved settings that hold the layout: the active layout, the list of layouts, each named
# layout, the same three for window frames, and the layout options.
LAYOUT_VAR = "VirtueAssistant_layout"
LAYOUT_ACTIVE = "VirtueAssistant_layout_active"
LAYOUT_LIST = "VirtueAssistant_layout_list"
LAYOUT_NAMED = "VirtueAssistant_layout_%s"
FRAMES_ACTIVE = "VirtueAssistant_frames_active"
FRAMES_LIST = "VirtueAssistant_frames_list"
FRAMES_NAMED = "VirtueAssistant_frames_%s"
LAYOUT_OPTS = "VirtueAssistant_layout_opts"
LAYOUT_DEFAULT = "Default"
LAYOUT_MIRRORED = "Mirrored"
LAYOUT_MINE = "Default (mine)"
LAYOUT_GONE = frozenset(("spelltimers", "bandage", "swing"))
DUNGEON_AREAS = ((0, 5120, 0, 6143, 2303),)
# Default window assignment to zones: zone id, then the window keys that stack in it.
WINDOWS_DEFAULT = ("L1=character;L2=bag;C1=unitframes.player;C2=unitframes.target;C4=actionbar;"
                   "R1=worldmap;R2=ultima.friend,ultima.neutral,ultima.foe;R3=meters")
# The same assignment with the sides swapped, for the mirrored layout.
WINDOWS_MIRRORED = ("L1=worldmap;L2=ultima.friend,ultima.neutral,ultima.foe,meters;"
                    "C1=unitframes.player;C2=unitframes.target;C4=actionbar;R1=character;R2=bag")
# Zone sizing rules as shares of the screen with pixel limits: side zones, spill zones, the minimum
# share kept for the centre, and the top and bottom strips.
SIDE_MIN, SIDE_MAX, SIDE_SHARE = 240, 440, 0.22
SPILL_MIN, SPILL_MAX, SPILL_SHARE = 240, 360, 0.12
CENTRE_MIN_SHARE = 0.40
TOP_MIN, TOP_MAX, BOT_MIN, BOT_MAX, STRIP_SHARE = 110, 180, 100, 160, 0.14
# Side zone slots: id, share of the side's height, minimum height, kind (w window, r reserved) and
# shrink priority.
LEFT_SLOTS = (("L1", 0.32, 260, "w", 2), ("L2", 0.38, 180, "w", 1), ("L3", 0.30, 160, "r", 0))
RIGHT_SLOTS = (("R1", 0.32, 200, "w", 2), ("R2", 0.40, 240, "w", 3), ("R3", 0.28, 120, "w", 1))
MINI_BAR = 46
ZONE_MIN_W, ZONE_MIN_H = 96, 64
# Colours of the zone kinds on the layout editor.
ZONE_COLORS = {"w": "#3A78C8", "k": "#3AA060", "r": "#C88A3A"}
ZONE_KINDS = (("w", "window"), ("k", "keep clear"), ("r", "reserved"))
ZONE_STACKS = (("d", "down"), ("u", "up"), ("r", "right"), ("l", "left"), ("t", "tabs"))
TAB_H = 26
TAB_X = -20000
SHRINK_MAX = 6
# Owner name under which the layout code registers its hooks.
LAYOUT_OWNER = "interface"
SEAM_PAD = 6
REVEAL_H = 14
REVEAL_HOLD = 0.6
SEAM_WAIT = 2.0
SEAM_RETRY = 0.1


def ratio_class(W, H):
    """Returns "narrow", "wide" or "ultrawide" for a screen of W by H (wide when it cannot be measured)."""
    if W <= 0 or H <= 0:
        return "wide"
    r = float(W) / float(H)
    return "narrow" if r < 1.5 else "wide" if r < 2.0 else "ultrawide"


def _clampv(v, lo, hi):
    """Returns v limited to lo and hi."""
    return max(lo, min(hi, v))


def _ordinal(n):
    """Returns n as a word such as 1st, 2nd or 13th, or "never" for zero or less."""
    n = int(n)
    if n <= 0:
        return "never"
    if n % 100 in (11, 12, 13):
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


class Zone(object):
    """One rectangle of the screen layout: a zone where windows are placed, kept clear or reserved.

    The rectangle is stored in thousandths of the screen so it scales with the resolution, with an exact
    pixel copy for free zones. Pins say which screen edges (L, T, R, B) or centre lines (X, Y) it holds.
    Flags set how windows fill and stack in it.
    """
    __slots__ = ("id", "kind", "rect", "pins", "min", "stack", "prio", "px", "squeezed", "fit",
                 "hug", "arch", "overlap", "lock", "solo", "free", "exact")

    def __init__(self, id, kind="w", rect=(0, 0, 200, 200), pins="", mins=(0, 0), stack="d",
                 prio=0, fit="w", hug=False, arch=False, overlap=False, lock=False, solo=False, free=False):
        """Builds a zone, forcing every argument to a legal value (unknown kinds become window zones, flags
        that do not apply to the kind are off, priority is limited to 0 to SHRINK_MAX).
        """
        self.id = str(id)
        self.kind = kind if kind in ("w", "k", "r") else "w"
        self.rect = tuple(int(v) for v in rect)
        self.pins = "".join(c for c in str(pins or "").upper() if c in "LTRBXY")
        self.min = (int(mins[0]), int(mins[1]))
        self.stack = stack if stack in ("d", "u", "r", "l", "t") else "d"
        self.prio = max(0, min(SHRINK_MAX, int(prio)))
        self.fit = fit if fit in ("w", "s", "n") else "w"
        self.hug = bool(hug) and self.kind == "w"
        self.arch = bool(arch) and self.kind == "k"
        self.overlap = bool(overlap)
        self.lock = bool(lock)
        self.solo = bool(solo)
        self.free = bool(free)
        self.px = None
        self.squeezed = False
        self.exact = None

    def kind_name(self):
        """Returns the player's word for the zone kind."""
        return dict(ZONE_KINDS)[self.kind]

    def stack_name(self):
        """Returns the player's word for the stacking direction."""
        return dict(ZONE_STACKS)[self.stack]

    def copy(self):
        """Returns an independent copy of the zone, with its pixel and exact rectangles."""
        z = Zone(self.id, self.kind, self.rect, self.pins, self.min, self.stack, self.prio,
                 self.fit, self.hug, self.arch, self.overlap, self.lock, self.solo, self.free)
        z.px = tuple(self.px) if self.px else None
        z.exact = self.exact
        return z

    def set_px(self, x, y, w, h, W, H):
        """Sets the zone from pixels x, y, w, h on a screen of W by H, keeping it on screen, and derives the
        thousandths rectangle and the exact copy from it. A screen size of zero leaves the rectangle alone.
        """
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
            self.exact = self.px + (int(W), int(H))

    def note_pins(self, W, H):
        """Works out which edges and centre lines the pixel rectangle touches (within SNAP_DIST, or half a
        pixel for a free zone) and stores them as the pins.
        """
        if not self.px or W <= 0 or H <= 0:
            return
        x, y, w, h = self.px
        lim = 0.5 if self.free else SNAP_DIST
        self.pins = "".join(c for c, d in (("L", x), ("T", y), ("R", W - (x + w)), ("B", H - (y + h)),
                                           ("X", abs((x + w / 2.0) - W / 2.0)), ("Y", abs((y + h / 2.0) - H / 2.0)))
                            if d <= lim)

    def save_text(self):
        """Returns the zone as one line of text for saving.
        The fields are separated by colons: id, kind, rect (four numbers), pins, minimum size, stack,
        priority, fit, then up to six flags (hug, arch, overlap, lock, solo, free) as 0 or 1. Only as many
        flags are written as are needed, and a free zone adds its six exact numbers. A colon or semicolon
        in the id is saved as a space.
        """
        # Older saves with fewer fields still read back; the parser treats missing flags as off.
        flags = (self.hug, self.arch, self.overlap, self.lock, self.solo, self.free)
        n = (6 if self.free else 5 if self.solo else 4 if self.overlap or self.lock else
             2 if self.hug or self.arch else 0)
        extra = "".join(":%d" % v for v in flags[:n])
        if self.free and self.exact:
            extra += ":%d,%d,%d,%d,%d,%d" % self.exact
        return "%s:%s:%d,%d,%d,%d:%s:%d,%d:%s:%d:%s%s" % (
            self.id.replace(":", " ").replace(";", " "), self.kind, self.rect[0], self.rect[1],
            self.rect[2], self.rect[3], self.pins, self.min[0], self.min[1], self.stack, self.prio, self.fit, extra)

    @staticmethod
    def parse(text):
        """Reads a zone from text written by save_text. Returns None if it is malformed.
        Missing flag fields count as off, and the exact numbers are kept only for a free zone and only
        when all of them are valid.
        """
        try:
            f = text.split(":")
            if len(f) < 7 or not f[0].strip():
                return None
            rect = [int(v) for v in f[2].split(",")]
            mn = [int(v) for v in f[4].split(",")]
            if len(rect) != 4 or len(mn) != 2 or rect[2] <= 0 or rect[3] <= 0:
                return None
            fit = f[7].strip() if len(f) > 7 else "w"
            hug, arch, overlap, lock, solo, free = [len(f) > i and f[i].strip() == "1" for i in range(8, 14)]
            z = Zone(f[0].strip(), f[1].strip(), rect, f[3], mn, f[5].strip(), int(f[6]), fit,
                     hug, arch, overlap, lock, solo, free)
            e = f[14].strip() if free and len(f) > 14 else ""
            if re.match(r"^\d+(,\d+){5}$", e):
                e = tuple(int(v) for v in e.split(","))
                if e[2] > 0 and e[3] > 0 and e[4] > 0 and e[5] > 0:
                    z.exact = e
            return z
        except Exception:
            return None


class ZoneSet(object):
    """A named set of zones (one screen layout): the zones, the snap grid and the screen size they were
    drawn for.

    Holds the pixel maths that keeps zones tiling the screen: building the default set, reflowing to
    a new screen size, pushing overlaps apart, filling gaps and evening out neighbours.
    """
    def __init__(self, name, zones=None, grid=GRID_DEFAULT, screen=(0, 0), generated=False):
        """Create a set. zones is a list of Zone; grid is the snap step in pixels; screen is the (width,
        height) the rects were drawn for; generated marks a set built by default(). skipped collects ids
        of saved zones that failed to parse; needs maps zone id to wanted pixel size.
        """
        self.name = str(name)
        self.zones = list(zones or [])
        self.grid = int(grid or GRID_DEFAULT)
        self.screen = (int(screen[0]), int(screen[1]))
        self.generated = generated
        self.skipped = []
        self.ver = 2
        self.needs = {}

    def by_id(self, zid):
        """Return the zone with this id, or None."""
        for z in self.zones:
            if z.id == zid:
                return z
        return None

    def ids(self):
        """Return the ids of all zones, in order."""
        return [z.id for z in self.zones]

    def copy(self, name=None):
        """Return an independent copy of the set (zones copied), optionally under a new name."""
        out = ZoneSet(name or self.name, [z.copy() for z in self.zones], self.grid, self.screen, self.generated)
        out.ver = self.ver
        return out

    def save_text(self):
        """Return the saved text: a header (grid, screen size, format version) then each zone's text, split
        by semicolons.
        """
        return "grid=%d,screen=%dx%d,v=%d;" % (self.grid, self.screen[0], self.screen[1], self.ver) + \
            ";".join(z.save_text() for z in self.zones)

    @staticmethod
    def parse(name, text):
        """Build a ZoneSet from saved text, or None when the text is empty.

        The header is optional (older saves have none, and read as version 1 on the default grid). Zones
        that fail to parse are skipped and their ids listed in skipped; a repeated id keeps the first
        zone.
        """
        text = str(text or "").strip()
        if not text:
            return None
        parts = text.split(";")
        grid, screen, ver = GRID_DEFAULT, (0, 0), 1
        head = parts[0]
        if head.startswith("grid="):
            parts = parts[1:]
            for item in head.split(","):
                with Kit.quiet:
                    k, v = item.split("=", 1)
                    if k == "grid":
                        grid = int(v)
                    elif k == "screen":
                        w, h = v.lower().split("x")
                        screen = (int(w), int(h))
                    elif k == "v":
                        ver = int(v)
        zs = ZoneSet(name, [], grid, screen)
        zs.ver = ver
        for p in parts:
            if not p.strip():
                continue
            z = Zone.parse(p)
            if z is None:
                zs.skipped.append(p.split(":")[0].strip() or "?")
            elif zs.by_id(z.id) is None:
                zs.zones.append(z)
        return zs

    @staticmethod
    def default(W, H, occupied=(), game_grows=True):
        """Build the ready-made set for a W x H screen: side bands of window zones left and right, two top
        strips, the keep-clear game view zone in the middle and a bottom strip; ultrawide screens also
        get edge zones.

        occupied is the set of zone ids that hold windows, so empty window slots can shrink. game_grows
        lets the game view stretch into a side band that has no windows.
        """
        zs = ZoneSet(LAYOUT_DEFAULT, [], GRID_DEFAULT, (W, H), generated=True)
        if W <= 0 or H <= 0:
            return zs
        occupied = set(occupied)
        cls = ratio_class(W, H)
        if cls == "narrow":
            side, spill = SIDE_MIN, 0
        else:
            side = int(_clampv(SIDE_SHARE * W, SIDE_MIN, SIDE_MAX))
            spill = (int(_clampv(SPILL_SHARE * W, SPILL_MIN, SPILL_MAX)) if cls == "ultrawide" else 0)
        if W - 2 * side - 2 * spill < CENTRE_MIN_SHARE * W:
            spill = 0
            if W - 2 * side < CENTRE_MIN_SHARE * W:
                side = max(SIDE_MIN, int((W - CENTRE_MIN_SHARE * W) / 2))
        lx, rx = spill, W - spill - side
        cx, cw = spill + side, W - 2 * (spill + side)
        top_h = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX))
        bot_h = int(_clampv(STRIP_SHARE * H, BOT_MIN, BOT_MAX))

        def add(z, x, y, w, h):
            """Place a zone at a pixel rect, pin it to the screen edges it touches and add it to the set."""
            z.set_px(x, y, w, h, W, H)
            z.note_pins(W, H)
            zs.zones.append(z)
            return z

        def band(x, slots):
            """Stack the given slots down one side band at x, giving each its height from _band_heights."""
            heights = ZoneSet._band_heights(H, slots, occupied)
            y = 0
            for (zid, share, mn, kind, prio), (h, squeezed) in zip(slots, heights):
                add(Zone(zid, kind, (0, 0, 1, 1), "", (SIDE_MIN, mn), "d", prio), x, y, side, h).squeezed = squeezed
                y += h

        band(lx, LEFT_SLOTS)
        half = cw // 2
        for zid, x, w, p in (("C1", cx, half, 3), ("C2", cx + half, cw - half, 2)):
            add(Zone(zid, "w", (0, 0, 1, 1), "T", (300, TOP_MIN), "d", p), x, 0, w, top_h)
        gx, gw = cx, cw
        if game_grows:
            if not any(s[0] in occupied for s in LEFT_SLOTS if s[3] == "w"):
                gx, gw = 0, gw + cx
            if not any(s[0] in occupied for s in RIGHT_SLOTS if s[3] == "w"):
                gw = W - gx
        add(Zone("C3", "k", (0, 0, 1, 1), "XY", (0, 0), "d", 0), gx, top_h, gw, H - top_h - bot_h)
        add(Zone("C4", "w", (0, 0, 1, 1), "B", (600, BOT_MIN), "r", 1), cx, H - bot_h, cw, bot_h)
        band(rx, RIGHT_SLOTS)
        if spill:
            for zid, x in (("L0", 0), ("R0", W - spill)):
                add(Zone(zid, "w", (0, 0, 1, 1), "", (SPILL_MIN, 120), "d", 1), x, 0, spill, H)
        return zs

    @staticmethod
    def _band_heights(H, slots, occupied):
        """Work out the pixel height of each slot of a side band of total height H.

        Returns a list of (height, squeezed) per slot. Empty window slots shrink to a small share,
        minimums are honoured by taking from the slots with spare height, slots that still cannot fit
        shrink to a mini bar (squeezed) in priority order, and a capped slot hands its extra height to
        the window slots.
        """
        n = len(slots)
        room = H
        any_win = any(zid in occupied for zid, sh, mn, kind, prio in slots if kind == "w")
        share, mins = [], []
        for zid, sh, mn, kind, prio in slots:
            empty = kind == "w" and zid not in occupied and any_win
            share.append(0.0 if empty else float(sh))
            mins.append(46 if empty else int(mn))
        squeezed = [False] * n
        order = sorted([i for i in range(n) if slots[i][4] > 0 and slots[i][3] == "w"], key=lambda i: slots[i][4])
        while sum(mins) > room and order:
            i = order.pop(0)
            if mins[i] > MINI_BAR:
                mins[i] = MINI_BAR
                squeezed[i] = True
                share[i] = 0.0
        total = sum(share) or 1.0
        h = [room * sh / total for sh in share]
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
        for i in range(n):
            if slots[i][3] == "r" and h[i] > slots[i][1] * room:
                extra, h[i] = h[i] - slots[i][1] * room, slots[i][1] * room
                takers = [j for j in range(n) if slots[j][3] == "w" and not squeezed[j] and share[j] > 0]
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
        extra = room - sum(out)
        if out and extra:
            out[out.index(max(out))] += extra
        return [(max(1, out[i]), squeezed[i]) for i in range(n)]

    def reflow(self, W, H, step):
        """Rescale every zone to a new screen size W x H on a grid of the given step.

        Zones keep their edge pins, free zones keep exact pixels when the screen matches, neighbours
        that were flush stay flush, minimum sizes are met where room allows and overlaps are pushed
        apart. Zones with a pending need are laid out first and then grown by _apply_needs. Sets
        self.screen at the end.
        """
        if W <= 0 or H <= 0:
            return
        step = max(8, int(step or GRID_DEFAULT))
        if self.needs:
            drawn = [(z, z.rect, z.exact) for z in self.zones]
            self.needs, needs = {}, self.needs
            self.reflow(W, H, step)
            self.needs = needs
            self._apply_needs(W, H)
            self._keep_clear(W, H)
            for z, r, e in drawn:
                z.rect, z.exact = r, e
            return
        oldW, oldH = self.screen if self.screen[0] > 0 and self.screen[1] > 0 else (W, H)
        flush = self._flush_pairs(oldW, oldH)

        def on_grid(v, limit, free):
            """Snap a screen position to the grid (free zones use single pixels) and keep it inside 0..limit."""
            st = 1 if free else step
            return _clampv(int(round(float(v) / st)) * st, 0, limit)

        exact = set()
        for z in self.zones:
            l, t, w, h = z.rect
            f = z.free
            e = z.exact if f and z.exact and z.exact[4:] == (W, H) else None
            if e is not None:
                exact.add(z.id)
                x0, y0, x1, y1 = e[0], e[1], e[0] + e[2], e[1] + e[3]
            else:
                x0, y0 = on_grid(W * l / 1000.0, W, f), on_grid(H * t / 1000.0, H, f)
                x1, y1 = on_grid(W * (l + w) / 1000.0, W, f), on_grid(H * (t + h) / 1000.0, H, f)
            if f:
                z.pins = "".join(c for c, on in (("L", x0 <= 0), ("T", y0 <= 0), ("R", x1 >= W), ("B", y1 >= H))
                                 if on)
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
        for a, b, side in flush:
            za, zb = self.by_id(a), self.by_id(b)
            if za is None or zb is None or za.px is None or zb.px is None or (a in exact and b in exact):
                continue
            ax, ay, aw, ah = za.px
            bx, by, bw, bh = zb.px
            if side == "h":
                nx = ax + aw
                right = W if "R" in zb.pins else bx + bw
                if right - nx >= ZONE_MIN_W:
                    zb.px = (nx, by, right - nx, bh)
            else:
                ny = ay + ah
                bottom = H if "B" in zb.pins else by + bh
                if bottom - ny >= ZONE_MIN_H:
                    zb.px = (bx, ny, bw, bottom - ny)
        for z in self.zones:
            if z.kind == "k":
                continue
            x, y, w, h = z.px
            if w < z.min[0]:
                w = min(z.min[0], max(w, self._free(z, 0, W) - x))
            if h < z.min[1]:
                h = min(z.min[1], max(h, self._free(z, 1, H) - y))
            z.set_px(x, y, w, h, W, H)
            z.squeezed = z.prio > 0 and z.px[3] < z.min[1]
        for z in self.zones:
            if z.kind != "k" and not z.overlap and self.overlaps(z):
                self.push_clear(z, W, H)
        for z in self.zones:
            if z.kind == "k" and not z.overlap:
                z.set_px(*(ZoneSet.cut_clear(z, self.zones) + (W, H)))
        for z in self.zones:
            z.set_px(z.px[0], z.px[1], z.px[2], z.px[3], W, H)
        self.screen = (W, H)

    @staticmethod
    def cut_clear(z, zones):
        """Return the rect of keep-clear zone z cut back so it no longer overlaps any window zone.

        The overlap is trimmed on the side that costs least; if that would make it too small the rect is
        left alone.
        """
        x, y, w, h = z.px
        for o in zones:
            if o is z or o.kind != "w" or o.px is None:
                continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh:
                cut, side = min([(x + w - ox, "R"), ((ox + ow) - x, "L"), (y + h - oy, "B"), ((oy + oh) - y, "T")])
                if side == "R":
                    w -= cut
                elif side == "L":
                    x, w = x + cut, w - cut
                elif side == "B":
                    h -= cut
                else:
                    y, h = y + cut, h - cut
                if w < ZONE_MIN_W or h < ZONE_MIN_H:
                    x, y, w, h = z.px
                    break
        return x, y, max(1, w), max(1, h)

    def _flush_pairs(self, W, H):
        """List pairs of zones that touched edge to edge on the old screen size W x H.

        Each entry is (id of a, id of b, "h" when b sits right of a, "v" when below). Free zones count
        as touching within a pixel or so; others within the snap distance. Pairs whose zones have more
        pins come first so edges anchored to the screen are settled before the rest.
        """
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
                f = a.free or b.free
                tw, th = (1.0 + W / 1000.0, 1.0 + H / 1000.0) if f else (SNAP_DIST, SNAP_DIST)
                if abs(bx - (ax + aw)) <= tw and by < ay + ah and ay < by + bh:
                    out.append((a.id, b.id, "h"))
                if abs(by - (ay + ah)) <= th and bx < ax + aw and ax < bx + bw:
                    out.append((a.id, b.id, "v"))

        def rank(zid):
            """Sort key: more edge pins sorts first."""
            z = self.by_id(zid)
            return -len(z.pins) if z else 0

        out.sort(key=lambda p: (rank(p[0]), rank(p[1])))
        return out

    def _free(self, z, i, lim):
        """Return how far zone z can reach on axis i (0 across, 1 down) before it meets the next window or
        game zone, at most lim.
        """
        r, j = z.px, 1 - i
        for o in self.zones:
            if o is z or o.kind == "k" or o.px is None:
                continue
            p = o.px
            if p[i] >= r[i] + r[i + 2] and p[j] < r[j] + r[j + 2] and r[j] < p[j] + p[j + 2]:
                lim = min(lim, p[i])
        return lim

    def overlaps(self, z, px=None):
        """Return the zones that z overlaps (z at its own rect, or at px when given).

        Zones allowed to overlap, and a game view zone against a bag zone, never count.
        """
        x, y, w, h = px or z.px
        out = []
        if z.overlap:
            return out
        for o in self.zones:
            if o is z or o.px is None or o.overlap:
                continue
            if (z.kind == "r" and o.kind == "k") or (z.kind == "k" and o.kind == "r"):
                continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh:
                out.append(o)
        return out

    def push_clear(self, z, W, H, step=None):
        """Move zone z to the nearest free spot so it overlaps nothing; step snaps the spot to the grid.

        Tries up to twelve moves, each to the side of an overlapped zone. Returns True when z ends
        clear.
        """
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
                        gx, gy = (int(round(float(nx) / step)) * step, int(round(float(ny) / step)) * step)
                        if (0 <= gx <= W - w and 0 <= gy <= H - h and not self.overlaps(z, (gx, gy, w, h))):
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
        """Trim each keep-clear zone so it does not run under a window zone."""
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
                if oy + oh >= y + h and oy > y:
                    h = oy - y
                elif oy <= y and oy + oh < y + h:
                    h, y = h - (oy + oh - y), oy + oh
                elif ox + ow >= x + w and ox > x:
                    w = ox - x
                elif ox <= x and ox + ow < x + w:
                    w, x = w - (ox + ow - x), ox + ow
            z.px = (x, y, max(1, w), max(1, h))

    def _apply_needs(self, W, H):
        """Grow zones to their wanted pixel size (self.needs), taking room from the neighbours.

        A zone grows towards the screen centre away from its pinned edge. Neighbours in its way are cut
        back to their own minimum, never below it.
        """
        for z in self.zones:
            need = self.needs.get(z.id)
            if need is None or z.px is None or z.kind == "k":
                continue
            r = list(z.px)
            for i, pin, S in ((1, "B", H), (0, "R", W)):
                n, a, s, j = need[i], r[i], r[i + 2], 1 - i
                if not n or n <= s:
                    continue
                grow = min(n - s, S - s)
                others = [o for o in self.zones if o is not z and o.kind == "w" and not o.overlap and o.px is not None
                          and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]]
                if pin in z.pins or a + s / 2.0 >= S / 2.0:
                    na = max(0, a - grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] < a and p[i] + p[i + 2] > na:
                            cut = max(p[i] + max(o.min[i], 1), na)
                            p[i + 2] = cut - p[i]
                            o.px = tuple(p)
                            na = max(na, cut)
                    r[i], r[i + 2] = na, s + (a - na)
                else:
                    ne = min(S, a + s + grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] >= a + s and p[i] < ne:
                            top = min(p[i] + p[i + 2] - max(o.min[i], 1), ne)
                            p[i], p[i + 2] = top, p[i] + p[i + 2] - top
                            o.px = tuple(p)
                            ne = min(ne, top)
                    r[i + 2] = ne - a
            z.px = tuple(r)

    def fill_gaps(self, W, H, step):
        """Stretch zones outward over any free space beside them, up to the grid or the neighbour."""
        step = max(8, int(step or GRID_DEFAULT))
        order = sorted(self.zones, key=lambda z: {"w": 0, "r": 1, "k": 2}[z.kind])
        for z in order:
            if z.overlap or z.lock:
                continue
            r = list(z.px)
            st = 1 if z.free else step
            for i, lo, hi, S in ((0, "L", "R", W), (1, "T", "B", H)):
                lim = max([0] + [o.px[i] + o.px[i + 2] for o in self.overlaps_side(z, lo)])
                n = 0 if lim == 0 else ((lim + st - 1) // st) * st
                if n < r[i]:
                    r[i], r[i + 2] = n, r[i + 2] + (r[i] - n)
                lim = min([S] + [o.px[i] for o in self.overlaps_side(z, hi)])
                e = S if lim == S else (lim // st) * st
                if e > r[i] + r[i + 2]:
                    r[i + 2] = e - r[i]
            z.set_px(r[0], r[1], r[2], r[3], W, H)

    def overlaps_side(self, z, side):
        """Return the zones next to z on the given side (L, R, T or B) that share part of its edge."""
        i = 0 if side in ("L", "R") else 1
        j, r = 1 - i, z.px
        return [o for o in self.zones if o is not z and o.px is not None and set((z.kind, o.kind)) != set(("r", "k"))
                and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]
                and (o.px[i] + o.px[i + 2] <= r[i] if side in ("L", "T") else o.px[i] >= r[i] + r[i + 2])]

    def even_out(self, z, W, H, step):
        """Resize z and the zones lined up with it to equal widths (or heights) across the same span.

        Looks for a row of aligned zones first, then a column. Returns how many zones were evened (under
        2 means nothing changed).
        """
        step = max(8, int(step or GRID_DEFAULT))
        D = SNAP_DIST

        def run(horizontal):
            """Collect the chain of aligned, touching window zones through z, horizontal or vertical. Returns
            (chain, axis).
            """
            same = [o for o in self.zones if o.kind == "w" and o.px is not None and (
                (abs(o.px[1] - z.px[1]) <= D and abs(o.px[3] - z.px[3]) <= D) if horizontal else
                (abs(o.px[0] - z.px[0]) <= D and abs(o.px[2] - z.px[2]) <= D))]
            i = 0 if horizontal else 1
            same.sort(key=lambda o: o.px[i])
            chain = [z]
            for direction in (1, -1):
                cur = z
                for _ in range(len(same)):
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
        """Return an unused id of the form Zone N for a new zone."""
        n = len(self.zones) + 1
        while self.by_id("Zone %d" % n) is not None:
            n += 1
        return "Zone %d" % n


class ClientWin(object):
    """Wrapper round one of TazUO's own windows (the world map, the journal) so a zone can hold it like
    a Virtue Assistant window.

    It gives the client window the same calls the zone code uses (GetX, GetY, GetWidth, GetHeight,
    SetPos, fit, free). The client's own control is reached through reflection; failures are kept in
    fail and told once. Class state: found caches the wrapper per kind, looked rate-limits the
    search, errors keeps why a search failed.
    """
    KINDS = {"worldmap": ("WorldMapGump",), "journal": ("ResizableJournal",)}
    TITLES = {"worldmap": "TazUO's World Map", "journal": "TazUO's journal"}
    INSET = {"worldmap": 4}
    DROPS = ("worldmap",)
    LOOK_EVERY = 1.0
    LOCK_VAR = "Layout_client_locked_%s"
    found = {}
    looked = {}
    errors = {}
    _pt = [None]
    _bf = [None]

    @staticmethod
    def point(x, y):
        """Build the client's own point type for (x, y); the type is looked up once and cached."""
        import System
        t = ClientWin._pt[0]
        if t is None:
            t = ClientWin._pt[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("Location").PropertyType
        return System.Activator.CreateInstance(t, System.Array[object]([int(x), int(y)]))

    @staticmethod
    def bounds(raw):
        """Return the raw bounds rectangle of a client control, read from its private _bounds field (cached
        lookup).
        """
        f = ClientWin._bf[0]
        if f is None:
            f = ClientWin._bf[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetField("_bounds",
                                                                                     Client.flags(public=False))
        return f.GetValue(raw)

    def __init__(self, kind, raw):
        """Wrap raw, the client control of the given kind.

        own is the window's state before we took it over: x, y, width, height, CanMove and locked, used
        by free(). tries counts resize attempts, fail holds the reasons a hold did not work, mins is the
        control's minimum size.
        """
        self.kind, self.raw = kind, raw
        self.own = None
        self.tries = 0
        self.fail = {}
        self.warned = False
        self.mins = None
        self._rc = None

    @staticmethod
    def of(kind):
        """Return the wrapper for the client window of this kind, or None when it is not open.

        The search runs at most once per LOOK_EVERY seconds; a disposed window is forgotten. A failed
        search is kept in errors.
        """
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
            with Kit.quiet:
                if not raw.IsDisposed:
                    cw = ClientWin(kind, raw)
                    break
        ClientWin.found[kind] = cw
        return cw

    @property
    def IsDisposed(self):
        """True when the client window is gone (or cannot be read)."""
        try:
            return bool(self.raw.IsDisposed)
        except Exception:
            return True

    @property
    def IsVisible(self):
        """True when the client window is shown."""
        try:
            return bool(self.raw.IsVisible)
        except Exception:
            return False

    def rect(self):
        """Return (x, y, width, height) of the client window.

        During a hop the rectangle is cached for the pass, so many zone checks read it once.
        """
        hop = HOST.in_hop
        if hop:
            c = self._rc
            if c is not None and c[0] == HOST.pass_id:
                return c[1]
        b = ClientWin.bounds(self.raw)
        r = (int(b.X), int(b.Y), int(b.Width), int(b.Height))
        self._rc = (HOST.pass_id, r) if hop else None
        return r

    def GetX(self):
        """Left edge of the client window."""
        return self.rect()[0]

    def GetY(self):
        """Top edge of the client window."""
        return self.rect()[1]

    def GetWidth(self):
        """Width of the client window."""
        return self.rect()[2]

    def GetHeight(self):
        """Height of the client window."""
        return self.rect()[3]

    def _put_bounds(self, x, y, w, h):
        """Write the control's bounds field directly, the fallback when setting Location does not stick."""
        import System
        self.rect()
        f = ClientWin._bf[0]
        self._rc = None
        f.SetValue(self.raw, System.Activator.CreateInstance(
            f.FieldType, System.Array[object]([int(x), int(y), int(w), int(h)])))

    def SetPos(self, x, y):
        """Move the client window to (x, y). Returns True when it ended there; otherwise records why in
        fail.
        """
        x, y = int(x), int(y)
        why = None
        self._rc = None
        try:
            self.raw.Location = ClientWin.point(x, y)
        except Exception as ex:
            why = Tz.why(ex)
        try:
            r = self.rect()
            if r[:2] != (x, y):
                self._put_bounds(x, y, r[2], r[3])
                r = self.rect()
            if r[:2] == (x, y):
                self.fail.pop("place", None)
                return True
        except Exception as ex:
            why = why or Tz.why(ex)
        self.fail["place"] = "it couldn't be moved (%s)" % (why or "the client put it back")
        return False

    def _locked(self):
        """Return whether the client window is locked, or None when that cannot be read."""
        try:
            return bool(self.raw.IsLocked)
        except Exception:
            return None

    def _lock(self, on):
        """Lock or unlock the client window and its CanMove flag, so the player cannot drag it while it
        sits in a zone.

        On unlock, CanMove is only given back when the window was movable before we took it over.
        """
        raw = self.raw
        on = bool(on)
        with Kit.quiet:
            if bool(raw.IsLocked) != on:
                Tz.call(raw, "SetLockStatus", (on,))
        with Kit.quiet:
            if on and raw.CanMove:
                raw.CanMove = False
            elif not on and not raw.CanMove and self.own is not None and self.own[4]:
                raw.CanMove = True

    def _min_size(self):
        """Return the window's own minimum (width, height), read once."""
        if self.mins is None:
            self.mins = (int(Typing._get(self.raw, "_minW", None, 0) or 0),
                         int(Typing._get(self.raw, "_minH", None, 0) or 0))
        return self.mins

    def fit(self, w, h, lock=True):
        """Hold the client window at w x h (never below its own minimum), locked unless lock is False.

        The first call stores the window's own state in own, so free() can put it back. A lock left over
        from an earlier run is not mistaken for the window's own. Resizing is retried each call; after
        four tries fail records that it stays the wrong size.
        """
        raw = self.raw
        if self.own is None:
            try:
                lk = self._locked()
                if lk and Kit.get_var(ClientWin.LOCK_VAR % self.kind, "") == "1":
                    lk = False
                self.own = self.rect() + (bool(raw.CanMove), lk)
            except Exception:
                self.own = None
            Kit.put_var(ClientWin.LOCK_VAR % self.kind, "1")
        self._lock(lock)
        mw, mh = self._min_size()
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
        if self.tries > 4:
            self.fail["size"] = "it stays %d x %d, not %d x %d" % (r[2], r[3], w, h)
        with Kit.quiet:
            Tz.put(raw, "_isFullscreen", False)
        p = ClientWin.point(w, h)
        self._rc = None
        try:
            Tz.call(raw, "ResizeWindow", (p,))
        except Exception as ex:
            self.fail["size"] = "it couldn't be resized (%s)" % Tz.why(ex)

    def free(self):
        """Give the client window back: restore its own lock, movable state, size and place. Clears the
        failures.
        """
        own, self.own, self.tries = self.own, None, 0
        self._rc = None
        Kit.put_var(ClientWin.LOCK_VAR % self.kind, "")
        if own is None or self.IsDisposed:
            return
        with Kit.quiet:
            self._lock(bool(own[5]))
            if not own[5]:
                self.raw.CanMove = own[4]
            Tz.call(self.raw, "ResizeWindow", (ClientWin.point(own[2], own[3]),))
            self.SetPos(own[0], own[1])
        self.fail = {}

    def report(self):
        """Say once, in the journal, why the window could not be held in its zone."""
        if self.fail and not self.warned:
            self.warned = True
            Kit.say("%s couldn't be held in its zone: %s." % (ClientWin.TITLES.get(self.kind, self.kind),
                "; ".join(self.fail[k] for k in ("place", "size") if k in self.fail)), Kit.HUE_BAD)


class Tex(object):
    """Registers images with the client's texture table so Legion gumps can draw them by name.

    State: ok is None until find() has run, then True or False; parts holds the reflected client
    objects and the outcome of find (kept for the client process, so a later start skips the lookup);
    names is every texture name this script has added, so they can be disposed.
    """
    ok = None
    parts = {}
    names = set()

    @staticmethod
    def find():
        """Look up the client's texture table, graphics device and gump loader through reflection. Returns
        True when all of them were found. The answer is cached, and also kept in parts for the next start
        of the script in this client; a failure leaves Tex.ok False and nothing else is touched.
        """
        if Tex.ok is not None:
            return Tex.ok
        try:
            import clr
            import System
            static = Client.flags(True)
            inst = Client.flags()
            p = Tex.parts
            lt = Client._type("ClassicUO.Assets.ExternalImageLoader")
            loader = lt.GetProperty("Instance", static).GetValue(None, None)
            p["table"] = lt.GetField("_zipNamedTextures", inst).GetValue(loader)
            p["device"] = lt.GetProperty("GraphicsDevice", inst).GetValue(loader, None)
            p["tex_t"] = Client._type("Microsoft.Xna.Framework.Graphics.Texture2D")
            p["format"] = System.Enum.Parse(Client._type("Microsoft.Xna.Framework.Graphics.SurfaceFormat"), "Color")
            p["set_data"] = [m for m in p["tex_t"].GetMethods() if m.Name == "SetData" and m.IsGenericMethodDefinition
                             and len(m.GetParameters()) == 1][0].MakeGenericMethod(clr.GetClrType(System.UInt32))
            game = Client._type("ClassicUO.Client").GetProperty("Game", static).GetValue(None, None)
            gumps = Tz.get(Tz.get(game, "UO"), "Gumps")
            p["gumps"] = gumps
            p["hued"] = gumps.GetType().GetMethod("GetHuedGumpPixels")
            Tex.ok = all(p.get(k) is not None for k in ("table", "device", "tex_t", "set_data", "gumps", "hued"))
        except Exception:
            Tex.ok = False
        Tex.parts["ok"] = Tex.ok
        return Tex.ok

    @staticmethod
    def gump_pixels(gid):
        """Return (pixels, width, height) of a gump by its id, or None when the gump is empty."""
        import System
        args = System.Array[System.Object]([System.UInt32(gid), System.UInt16(0), False, None])
        px = Tex.parts["hued"].Invoke(Tex.parts["gumps"], args)
        b = args[3]
        if px is None or not len(px) or int(b.Width) <= 0 or int(b.Height) <= 0:
            return None
        return list(px), int(b.Width), int(b.Height)

    @staticmethod
    def put(name, w, h, pixels):
        """Create a texture w x h from the pixel list and store it in the client's table under name,
        disposing any texture it replaces.
        """
        import System
        p = Tex.parts
        tex = System.Activator.CreateInstance(p["tex_t"], System.Array[System.Object](
            [p["device"], int(w), int(h), False, p["format"]]))
        p["set_data"].Invoke(tex, System.Array[System.Object]([System.Array[System.UInt32](pixels)]))
        table = p["table"]
        old = table[name] if table.ContainsKey(name) else None
        table[name] = tex
        Tex.names.add(name)
        if old is not None:
            safe(old.Dispose)

    @staticmethod
    def drop(names=None):
        """Remove and dispose the named textures (all of ours when names is None)."""
        if not Tex.ok:
            return
        table = Tex.parts["table"]
        for name in list(Tex.names if names is None else names):
            Tex.names.discard(name)
            with Kit.quiet:
                if table.ContainsKey(name):
                    tex = table[name]
                    table.Remove(name)
                    tex.Dispose()

    @staticmethod
    def has(name):
        """True when a texture called name is in the client's table and not disposed.

        The table outlives a script Stop, so a texture kept across one is found again by name. False when
        the table cannot be reached.
        """
        if not Tex.ok:
            return False
        table = Tex.parts["table"]
        with Kit.quiet:
            return bool(table.ContainsKey(name)) and not table[name].IsDisposed
        return False

    @staticmethod
    def control(g, name, x, y, w, h):
        """Add a texture control for the named texture to gump g at the given rect. It ignores the mouse,
        so clicks pass through to what is under it. Returns the control.
        """
        t = G.LegionTextureControl(name, int(w), int(h))
        t.SetRect(int(x), int(y), int(w), int(h))
        safe(lambda: t.SetAcceptMouseInput(False))
        g.Add(t)
        return t


class Layout(object):
    """The zone and layout manager: which window sits in which zone, and the code that places, sizes,
    locks and repairs windows to match.

    There is one Layout, owned by the mother script. It holds the saved frame sets and window
    layouts, the window to zone assignments, Arrange mode, tabbed zones (one window shown at a time
    under a strip of tabs), layouts by situation, share codes, and the client's own windows (world map,
    journal). Its work runs on the client tick, in short hops.
    """
    def __init__(self):
        """Sets up empty state: windows, assignments, frame sets, caches for placement, the start-up plan,
        Arrange mode, undo, the situation settings and the tab and tab strip records.
        """
        self.wins = {}
        self.assign = {}
        self.frames = None
        self.frames_name = LAYOUT_DEFAULT
        self.layout_name = ""
        self.game_grows = True
        self.fit_view = True
        self.screen = None
        self.dirty = True
        self.occ = None
        self.gump_key = {}
        self.placed = {}
        self.titles = {}
        self.min_seen = {}
        self.loaded = False
        self.page_refresh = False
        self.enabled = True
        self.seamless = False
        self.gv_off_done = False
        self.seam_skip = {}
        self.seam_wait = {}
        self.hooks = {}
        self.owner = {}
        self.fitted = {}
        self.base = {}
        self.fresh = False
        self.fresh_adds = set()
        self.client_seen = {}
        self.journal_held = self.journal_px = None
        self.pair_tried = None
        self.client_settle = {}
        self.misfit = {}
        self.fallback = {}
        self.client_told = set()
        self.chat_seen = (0.0, None)
        self.held = {}
        self.arrange = False
        self.arrange_last = 0.0
        self.arrange_g = None
        self.arrange_lit = {}
        self.arrange_hot = None
        self.client_target = {}
        self.repair_at = 0.0
        self.repair_told = set()
        self.freed = None
        self.page_preview = ""
        self.homes = None
        self.back_told = False
        self._arrange_sig = None
        self.rev = {}
        self.retry_at = 0.0
        self.slot_was = {}
        self.bags_swept = False
        self.reclaim_undo = self._vp_fields = self.gv_applied = self.small_said = None
        self._undo_read = self.gv_small_told = self.gv_checked = self.need_due = self.migrating = False
        self.situ = {"on": False, "base": ""}
        self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None
        self.situ_at = 0.0
        self.situ_busy = False
        self.situ_bank = (-1e9, 0, 0, -1)
        self.tabs = {}
        self.behind = {}
        self.strips = {}
        self.planned = {}
        self.plan_occ = self.plan_sig = None

    def _client_getter(self, kind, key):
        """Return a function that finds the client window of this kind for placement key.

        The function forgets cached placement when the window is replaced, and once tells the player why
        a zoned window could not be found.
        """
        def get():
            """Return the client window wrapper, or None."""
            cw = ClientWin.of(kind)
            if cw is not self.client_seen.get(kind):
                self.client_seen[kind] = cw
                self.fitted.pop(key, None)
                self.placed.pop(key, None)
            if cw is None and kind not in self.client_told and ClientWin.errors.get(kind) \
                    and self.zone_of(key) is not None:
                self.client_told.add(kind)
                Kit.say("%s can't be found for its zone: %s." % (
                    ClientWin.TITLES.get(kind, kind), ClientWin.errors[kind]), Kit.HUE_BAD)
            return cw

        return get

    def _client_fit(self, kind):
        """Return the fit function a zone uses on the client window of this kind: size it, or free it when
        no size is given.
        """
        def fit(w, h, mode):
            """Hold the client window at w x h, or give it back when w or h is None. Locks it unless Arrange
            mode is on.
            """
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
        """In Arrange mode, notice when the player drops a client window (the world map) and hand it to
        dropped().

        A window not in a zone must stop moving before it counts as dropped; one already in a zone
        counts when it is dragged further than the snap distance from where we put it. Nothing happens
        while the snap key is held.
        """
        if not self.arrange:
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
                self.client_settle.pop(key, None)
                at = self.client_target.get(key)
                if at is not None and max(abs(r[0] - at[0]), abs(r[1] - at[1])) > SNAP_DIST \
                        and SNAP.pressed() is not True:
                    self.client_target.pop(key, None)
                    self.dropped(cw)
                continue
            st = self.client_settle.get(key)
            if st is None or st[0] is not cw:
                self.client_settle[key] = (cw, r, r)
                continue
            settled, last = st[1], st[2]
            if r != last:
                self.client_settle[key] = (cw, settled, r)
                continue
            if r == settled or SNAP.pressed() is True:
                continue
            self.client_settle[key] = (cw, r, r)
            if (r[2], r[3]) != (settled[2], settled[3]):
                continue
            self.dropped(cw)

    CHAT_ROOM = 18

    def _chat_line(self):
        """Return (x, top, width) of the chat entry line of the client, or None when it cannot be found.

        Read through reflection and cached for half a second, since it is asked for on every placement.
        The room reserved is CHAT_ROOM pixels.
        """
        now = time.time()
        at, rect = self.chat_seen
        if now - at < 0.5:
            return rect
        rect = None
        try:
            Typing._find()
            sc = Typing._get(None, "SystemChat", Typing.uim) if Typing.uim is not None else None
            if sc is not None and not bool(Typing._get(sc, "IsDisposed", default=True)):
                b = ClientWin.bounds(sc)
                sx = int(Typing._get(sc, "ParentX", default=0) or 0) + int(b.X)
                sy = int(Typing._get(sc, "ParentY", default=0) or 0) + int(b.Y)
                top = sy + int(b.Height) - Layout.CHAT_ROOM
                tb = Typing._get(sc, "TextBoxControl")
                if tb is not None:
                    tby = int(ClientWin.bounds(tb).Y)
                    if 0 <= tby < int(b.Height):
                        top = min(top, sy + tby)
                if int(b.Width) > 0 and int(b.Height) > 0:
                    rect = (sx, top, int(b.Width))
        except Exception:
            rect = None
        self.chat_seen = (now, rect)
        return rect

    def _clear_of_chat(self, x, y, w, h, H):
        """Return the height of the rect a zone can use without covering the chat entry line.

        Without a known chat line, a rect touching the screen bottom gives up CHAT_ROOM pixels. At least
        60 pixels are kept.
        """
        line = self._chat_line()
        if line is None:
            cut = Layout.CHAT_ROOM if H and y + h >= H - 2 else 0
            bottom = y + h - cut
        else:
            lx, top, lw = line
            if x >= lx + lw or lx >= x + w or not (y < top < y + h):
                return h
            bottom = top
        return max(min(h, 60), bottom - y)

    def _hold_journal(self, zs, H=0):
        """Hold the client journal in the first journal zone (kind r), clear of the chat line, or free it
        when there is no zone.
        """
        z = (next((zz for zz in zs.zones if zz.kind == "r" and zz.px is not None), None)
             if self.layout_name or self.assign else None)
        cw = ClientWin.of("journal") if z is not None else None
        held = self.journal_held
        if held is not None and held is not cw:
            held.free()
            self.journal_held = None
        if cw is None:
            self.journal_px = None
            return
        x, y, w, h = z.px
        h = self._clear_of_chat(x, y, w, h, H)
        cw.fit(w, h)
        self.journal_px = (x, y, w, h)
        try:
            if (cw.GetX(), cw.GetY()) != (x, y):
                cw.SetPos(x, y)
        except Exception:
            pass
        cw.report()
        self.journal_held = cw

    def beside_journal(self, x, y, w, h):
        """Returns the x at which a window at x, y, w by h should sit so that it does not cover the client
        journal held in its zone: the journal's right edge, or its left side when there is no room on the
        right. Returns x unchanged when it does not overlap the journal.
        """
        r = self.journal_px
        if r is None or not (r[0] <= x < r[0] + r[2] and y < r[1] + r[3] and r[1] < y + h):
            return x
        W = Kit.screen()[0]
        return r[0] + r[2] if not W or r[0] + r[2] + w <= W else max(0, r[0] - w)

    def load(self):
        """Reads the saved layout state into memory: the active frame set and window layout, the options,
        which window sits in which zone, the situation settings, the chosen tab of each tabbed zone and
        whether the layout is switched on.

        Registers the world map as a window that can be zoned. Resets the one-shot told flags and the start-up
        plan, and marks the layout dirty so the next hop places everything. Rewrites the saved assignment
        when it still names windows that no longer exist.
        """
        self.freed = None
        self.homes = None
        self.repair_told = set()
        self.back_told = False
        self.loaded = True
        self.bags_swept = False
        self.planned, self.plan_occ, self.plan_sig = {}, None, None
        self.seam_skip = {}
        self.seam_wait = {}
        if "worldmap" not in self.wins:
            self.add("worldmap", self._client_getter("worldmap", "worldmap"), "TazUO's World Map",
                     {"fit": self._client_fit("worldmap"), "exact": True, "client": True,
                      "inset": ClientWin.INSET.get("worldmap", 0)})
        self.frames_name = Kit.get_var(FRAMES_ACTIVE, LAYOUT_DEFAULT) or LAYOUT_DEFAULT
        if self.frames_name != LAYOUT_DEFAULT and self.frames_name not in self.frame_names():
            self.frames_name = LAYOUT_DEFAULT
        self.layout_name = Kit.get_var(LAYOUT_ACTIVE, "")
        opts = Kit.get_var(LAYOUT_OPTS, "game=1")
        self.game_grows = "game=0" not in opts
        self.fit_view = "fit=0" not in opts
        raw = Kit.get_var(LAYOUT_VAR, "")
        self.seamless = "seam=1" in opts
        owner = dict.get(HOST.by_key, LAYOUT_OWNER)
        self.enabled = bool(owner is not None and owner.enabled and owner.api is not None)
        self.assign = self.parse_windows(raw)[1]
        if raw and raw != self.windows_text() and any(k.strip() in LAYOUT_GONE for part in str(raw).split(";")
                if "=" in part and part.split("=", 1)[0].strip() != "frames" for k in part.split("=", 1)[1].split(",")):
            self.save_assign()
        self.frames = None
        self.dirty = True
        self.situ_load()
        self.tabs = self._tabs_parse(Kit.get_var(self.TABS_VAR, ""))

    def save_assign(self):
        """Save the window to zone assignment and refresh the remembered homes of the windows."""
        Kit.put_var(LAYOUT_VAR, self.windows_text())
        self._note_homes()

    RECLAIM_VAR = "VirtueAssistant_reclaim_undo"
    RECLAIM_FIXED = "VirtueAssistant_reclaim_fixed"

    def _undo_load(self):
        """Return the saved undo record for Reclaim space, reading it from the saved variable on first use.

        The record is (frame set name, saved text, None, whether the set was the default one).
        """
        if self.reclaim_undo is None and not self._undo_read:
            self._undo_read = True
            p = str(Kit.get_var(self.RECLAIM_VAR, "") or "").split("|", 2)
            if len(p) == 3 and p[0]:
                self.reclaim_undo = (p[0], p[2], None, p[1] == "1")
        return self.reclaim_undo

    def _undo_set(self, undo):
        """Remember the Reclaim space undo record in memory and in its saved variable (None clears it)."""
        self.reclaim_undo = undo
        self._undo_read = True
        Kit.put_var(self.RECLAIM_VAR, "" if undo is None else "%s|%d|%s" % (undo[0], 1 if undo[3] else 0, undo[1]))

    @staticmethod
    def _reclaim_edges(z, blockers, W, H):
        """Return the rect of zone z stretched on each side as far as the blocking zones allow."""
        r = list(z.px)
        for side in "LTRB":
            i = 0 if side in "LR" else 1
            j = 1 - i
            ps = [o.px for o in blockers if o is not z and o.px is not None
                  and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]]
            if side in "LT":
                lim = max([0] + [p[i] + p[i + 2] for p in ps if p[i] + p[i + 2] <= r[i]])
                if lim < r[i]:
                    r[i], r[i + 2] = lim, r[i + 2] + (r[i] - lim)
            else:
                lim = min([(W, H)[i]] + [p[i] for p in ps if p[i] >= r[i] + r[i + 2]])
                if lim > r[i] + r[i + 2]:
                    r[i + 2] = lim - r[i]
        return tuple(r)

    def reclaim_zones(self, zs, W, H):
        """Stretch the zones of zs over free space, keep-clear zones first, then window zones. Returns the
        ids changed.

        Zones that hug, are locked or may overlap are left alone, and window zones never grow over the
        journal zone's kind (r).
        """
        fixed = [o for o in zs.zones if o.px is not None and not o.hug and (o.kind != "k" and not o.overlap)]
        others = [o for o in zs.zones if o.px is not None and o.kind != "r"]
        changed = []
        for kind, blockers in (("k", fixed), ("w", others)):
            for z in zs.zones:
                if z.kind != kind or z.lock or z.px is None or (kind == "w" and (z.hug or z.overlap)):
                    continue
                r = self._reclaim_edges(z, blockers, W, H)
                if r != tuple(z.px):
                    z.set_px(r[0], r[1], r[2], r[3], W, H)
                    changed.append(z.id)
        return changed

    @staticmethod
    def _game_px(zs):
        """Return the pixel rect of the largest keep-clear zone (the game view), or None."""
        best = None
        for z in zs.zones:
            if z.kind == "k" and z.px is not None and z.px[2] > 2 and z.px[3] > 2 and (
                    best is None or z.px[2] * z.px[3] > best[2] * best[3]):
                best = tuple(z.px)
        return best

    def reclaim_space(self):
        """Settings button: tighten every zone of the layout in use so the game area grows, saving the
        result.

        When the layout is the generated default it is saved as a new set called Reclaimed; otherwise it
        replaces the set in use. An undo record is kept so reclaim_back can restore it. Says what
        happened in the journal.
        """
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        if zs is None or not zs.zones:
            Kit.say("no frame layout in use.", Kit.HUE_INFO)
            return
        was = (self._game_px(zs) or (0, 0, 0, 0))[2:]
        default = self.frames_name == LAYOUT_DEFAULT
        undo = (zs.name, zs.save_text(), was, default)
        moved = self.reclaim_zones(zs, W, H)
        now = (self._game_px(zs) or (0, 0, 0, 0))[2:]
        if not moved or now[0] * now[1] < was[0] * was[1]:
            self.frames, self.dirty = None, True
            Kit.say("Reclaim space: every zone is already tight.", Kit.HUE_INFO)
            return
        self._undo_set(undo)
        target = zs.name if not default else "Reclaimed"
        zs.generated = False
        self.save_frames(zs, target, W, H)
        self.use_frames(target, False)
        self.refit_all()
        Kit.say("Reclaim space: %d zone%s tightened; game area %d x %d (was %d x %d). Undo puts it back." % (
            len(moved), "" if len(moved) == 1 else "s", now[0], now[1], was[0], was[1]), Kit.HUE_GOOD)

    def reclaim_back(self):
        """Settings button: undo the last Reclaim space from the saved undo record."""
        undo = self._undo_load()
        if undo is None:
            return
        self._undo_set(None)
        W, H = Kit.screen()
        if undo[3]:
            self.use_frames(LAYOUT_DEFAULT, False)
        else:
            zs = ZoneSet.parse(undo[0], undo[1])
            if zs is None:
                return
            zs.reflow(W, H, HOST.grid_size())
            self.save_frames(zs, undo[0], W, H)
            self.use_frames(undo[0], False)
        self.refit_all()
        Kit.say("Reclaim space undone.", Kit.HUE_INFO)

    def _repair_stretched(self, zs, W, H):
        """One-time repair of hugging zones that an earlier Reclaim space stretched too tall, run once per
        account.

        Resets them to the top strip height and saves the set; an undo record is kept.
        """
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
        Kit.say("%d frame zone%s Reclaim space stretched in layout \"%s\" put right; Settings > Interface's "
                   "Undo puts it back." % (len(tall), "" if len(tall) == 1 else "s", zs.name), Kit.HUE_GOOD)

    def refit_all(self):
        """Mark everything dirty so the next hop re-places and re-fits every window."""
        self.dirty = self.fresh = self.page_refresh = True
        self.seam_skip = {}
        self.seam_wait = {}

    def save_opts(self):
        """Save the layout options (game view grows, fit view, one panel look) in their saved variable."""
        Kit.put_var(LAYOUT_OPTS, "game=%d;fit=%d;seam=%d;art=plain" % (self.game_grows, self.fit_view, self.seamless))

    def set_enabled(self, on):
        """Switch zones on or off. Off stops Arrange mode, releases every window and gives the game view
        back.
        """
        on = bool(on)
        if on == self.enabled:
            return
        if not on:
            self.set_arrange(False, tell=False)
        self.enabled, self.gv_off_done = on, False
        self.refit_all()
        HOST.poke()

    def _off(self):
        """Undoes everything the layout did: tabs and their strips, seams, fitted windows, placed sizes, locks
        and the held client windows.

        Runs when zones are switched off, so every window is free and the player's own game view comes
        back (restored once).
        """
        if self.behind or self.strips or Kit._behind:
            self._tabs_off()
        Seam.undo_all()
        for key in list(self.fitted):
            self._unfit(key)
        for key in list(self.placed):
            g = self.gump_of(key)
            info = Kit.scroll_info(g) if g is not None else None
            if info is not None:
                with Kit.quiet:
                    Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"])
                    Kit.moved_by_code(g)
        self.placed = {}
        if self.held:
            self._release(set())
        held, self.journal_held, self.journal_px = self.journal_held, None, None
        if held is not None:
            held.free()
        if not self.gv_off_done:
            self.gv_off_done = True
            self.game_view_restore()

    @staticmethod
    def parse_windows(text):
        """Parse the saved window text into (frame set name, {zone id: [window keys]}).

        Windows that no longer exist (LAYOUT_GONE) are dropped.
        """
        frames, out = LAYOUT_DEFAULT, {}
        for part in str(text or "").split(";"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            k = k.strip()
            if k == "frames":
                frames = v.strip() or LAYOUT_DEFAULT
                continue
            keys = [s.strip() for s in v.split(",") if s.strip() and s.strip() not in LAYOUT_GONE]
            if k and keys:
                out[k] = keys
        return frames, out

    def windows_text(self, frames=None, assign=None):
        """Return the saved text of the window assignment: the frame set name, then each zone and its
        windows.
        """
        a = self.assign if assign is None else assign
        return ";".join(["frames=%s" % (frames or self.frames_name)] + [
            "%s=%s" % (zid, ",".join(a[zid])) for zid in sorted(a) if a[zid]])

    @staticmethod
    def _names(var):
        """Return the names stored in a comma separated saved variable."""
        return [n for n in Kit.get_var(var, "").split(",") if n.strip()]

    def frame_names(self):
        """Return the names of the saved frame sets."""
        return self._names(FRAMES_LIST)

    def layout_names(self):
        """Return the names of the saved window layouts."""
        return self._names(LAYOUT_LIST)

    @staticmethod
    def clean_name(name, fallback):
        """Return name cleaned for saving: letters, digits and a few marks only, at most 24 characters, or
        fallback if empty.
        """
        name = re.sub(r"[^A-Za-z0-9 ()'_-]", "", str(name or "")).strip()[:24]
        return name or fallback

    def add(self, key, getter, title=None, hooks=None, owner=None):
        """Register a window that zones can hold, under key.

        getter returns the window (or None while it is closed); title is the name shown to the player;
        hooks is a dict of optional callbacks (fit, min, redraw, exact, client, inset); owner is the
        (module key, part) that owns it.
        """
        key = str(key)
        if key in LAYOUT_GONE:
            return
        t = self.titles[key] = str(title or key)
        self.wins[key] = (getter, t)
        self.hooks[key] = hooks if hooks is not None else {}
        if owner is not None:
            self.owner[key] = owner
        self.fitted.pop(key, None)
        self.dirty = True

    def remove(self, key):
        """Forget a window and every cache that holds it."""
        key = str(key)
        for d in (self.wins, self.placed, self.hooks, self.owner, self.fitted, self.base, self.slot_was, self.min_seen):
            d.pop(key, None)
        self.dirty = True

    def owner_of(self, key):
        """Return (module key, part) of the module that owns this window, or (None, None).

        Searches by the key and then by its dotted parents.
        """
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
        """Return (key, title) for each window of the module, sorted by title."""
        return sorted([(key, self.title_of(key)) for key in self.wins if self.owner_of(key)[0] == module_key],
                      key=lambda kt: kt[1].lower())

    def all_windows(self):
        """Return (key, title) for every window that can be zoned, sorted by title.

        Windows assigned to a zone but not open now are included and marked (not open).
        """
        out = []
        for key in list(self.wins) + sorted(set(k for ks in self.assign.values() for k in ks if k not in self.wins)):
            mk = self.owner_of(key)[0]
            s = dict.get(HOST.by_key, mk) if mk else None
            t = self.title_of(key)
            if s is not None and s.title != t:
                t = "%s: %s" % (s.title, t)
            out.append((key, t if key in self.wins else t + " (not open)"))
        out.sort(key=lambda kt: kt[1].lower())
        return out

    def zone_choices(self):
        """Return the zone ids a window can be given (kind w zones), with None first for free."""
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames
        out = [None]
        if zs is not None:
            out.extend(z.id for z in zs.zones if z.kind == "w")
        return out

    def assign_to(self, key, zid, tell=True):
        """Put the window key in zone zid (None frees it), save, and refresh.

        The world map keeps its zone to itself, and a refusal is told when tell is True. An emptied bags
        zone is dropped. Says where the window went when tell is True.
        """
        key = str(key)
        old = self.zone_of(key)
        if old == zid:
            return
        if tell and zid and ((key != "worldmap" and zid == self._map_zone())
                             or (key == "worldmap" and self.assign.get(zid))):
            Kit.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."
                       % (self.title_of(key) if key != "worldmap" else "it"), Kit.HUE_BAD)
            self.page_refresh = True
            return
        if old is not None:
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if not self.assign[old]:
                del self.assign[old]
        if zid:
            self.assign.setdefault(zid, []).append(key)
            self.unfree(key)
        elif tell:
            self.free_by_you([key])
        self.save_assign()
        W, H = Kit.screen()
        empty = old is not None and not self.assign.get(old)
        if key == "bag" and empty and W > 0 and H > 0 and self.drop_empty_bags(self.frames_in_use(W, H), W, H, (old,)):
            self.frames, self.dirty = None, True
        if not zid:
            self.free_scrolled()
        self.placed.pop(key, None)
        self.dirty = True
        self.page_refresh = True
        if tell:
            API.SysMsg(('%s: %s is in zone "%s".' % (APP_NAME, self.title_of(key), zid)) if zid else
                       ("%s: %s is free (it stays where you put it)." % (APP_NAME, self.title_of(key))), Kit.HUE_GOOD)
        HOST.poke()

    def zone_of(self, key):
        """Return the id of the zone this window is assigned to, or None. Uses a reverse index rebuilt on a
        miss.
        """
        zid = self.rev.get(key)
        if zid is not None and key in self.assign.get(zid, ()):
            return zid
        self.rev = dict((k, z) for z, keys in self.assign.items() for k in keys)
        return self.rev.get(key)

    def need(self, key, w, h):
        """Tells the layout a window wants at least w x h pixels (a zero means no wish) in its zone. In a
        tabbed zone the height is raised by the tab strip.

        The wish is kept in the frame set and the zone is grown on the next hop when need_due is set.
        """
        zid = self.zone_of(str(key))
        zs = self.frames
        if zid is None or zs is None:
            return
        z = zs.by_id(zid)
        want = (w, h + TAB_H if h and z is not None and z.stack == "t" else h) if (w or h) else None
        if zs.needs.get(zid) != want:
            if want is None:
                zs.needs.pop(zid, None)
            else:
                zs.needs[zid] = want
            self.need_due = True

    def zone_base(self, key):
        """Returns the (width, height) of the window's zone in pixels, less the tab strip of a tabbed zone, or
        None when it has no zone.
        """
        zid = self.zone_of(str(key))
        zs = self.frames
        z = zs.by_id(zid) if (zid is not None and zs is not None) else None
        if z is None:
            return None
        W, H = zs.screen
        if W <= 0 or H <= 0:
            W, H = Kit.screen()
        tab = TAB_H if z.stack == "t" else 0
        return (max(1, int(W * z.rect[2] / 1000.0)), max(1, int(H * z.rect[3] / 1000.0) - tab))

    def holds(self, key):
        """True when zones are on and this window is assigned to a zone that exists."""
        if not self.enabled:
            return False
        zid = self.zone_of(str(key))
        if zid is None:
            return False
        zs = self.frames
        return zs is None or zs.by_id(zid) is not None

    def locked(self, key):
        """True when the window is locked in its zone (held and not in Arrange mode)."""
        return not self.arrange and self.holds(key)

    def _hold(self, g, key):
        """Take hold of gump g for key: remember its own CanMove, drop its snap links, and set CanMove to
        match Arrange mode.

        Client windows are held by ClientWin, so they are skipped here.
        """
        if isinstance(g, ClientWin):
            return
        if g not in self.held:
            self.held[g] = (key, bool(g.CanMove))
            for f, l in list(SNAP.links.items()):
                if f is g or l is g:
                    SNAP.links.pop(f, None)
        if bool(g.CanMove) != bool(self.arrange):
            g.CanMove = bool(self.arrange)

    def _release(self, keep):
        """Let go of held gumps that are not in keep, giving back their own CanMove.

        A window that no longer has a zone is redrawn through its redraw hook when it has one.
        """
        for g in [g for g in self.held if g not in keep]:
            key, own = self.held.pop(g)
            if g in SNAP.drag or not Kit.is_open(g):
                continue
            if not own and not self.holds(key):
                rd = (self.hooks.get(key) or {}).get("redraw")
                if callable(rd):
                    safe(rd)
                    continue
                own = True
            if bool(g.CanMove) != own:
                g.CanMove = own

    def set_arrange(self, on, tell=True):
        """Turn Arrange mode on or off. In Arrange mode held windows can be dragged between zones.

        It switches itself off after sixty seconds with no drag. tell says it in the journal.
        """
        on = bool(on) and self.enabled
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
            API.SysMsg(("%s: Arrange mode on; drag windows on to zones, then click Done." if on else
                        "%s: windows locked in their zones.") % APP_NAME, Kit.HUE_GOOD)
        HOST.poke()

    def _arrange_tick(self, zs, W, H):
        """Per hop in Arrange mode: end it after the idle time and redraw the zone overlay when the zones
        changed.

        The overlay is a gump of tinted zone boxes, borders, names and a hint line, with the grid on
        top. A hidden lit box per window zone is shown while a window is dragged over it.
        """
        if not self.arrange:
            return
        now = time.time()
        if SNAP.drag:
            self.arrange_last = now
        elif now - self.arrange_last > 60.0:
            self.set_arrange(False)
            return
        sig = (W, H, tuple((z.id, z.kind, tuple(z.px)) for z in zs.zones if z.px is not None))
        if self.arrange_g is not None and Kit.is_open(self.arrange_g) and self._arrange_sig == sig:
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
            lit.IsVisible = False
            self.arrange_lit[z.id] = lit
            for bx, by, bw_, bh in ((x, y, w, 2), (x, y + h - 2, w, 2), (x, y, 2, h), (x + w - 2, y, 2, h)):
                Kit.add_box(g, bx, by, bw_, bh, 0.9, col)
            name = Kit.fit(z.id, max(20, w - 28))
            pw = Kit.text_w(name) + 12
            Kit.add_box(g, x + 6, y + h - 6 - 22, pw, 22, 0.85, "#000000")
            Kit.add_label(g, name, x + 12, y + h - 6 - 20, Kit.HUE_TITLE)
        tip = "Drag windows onto zones; Esc or Done to finish"
        tw = Kit.text_w(tip) + 24
        Kit.add_box(g, (W - tw) // 2, 6, tw, 26, 0.85, "#000000")
        Kit.add_label(g, tip, (W - tw) // 2 + 12, 10, Kit.HUE_TITLE)
        Grid.show_overlay(g, 0, 0, W, H)
        self.arrange_g = g
        self.arrange_hot = None

    def arrange_hover(self, g, r=None):
        """Light up the zone under the dragged gump g (or rect r) in the overlay, and dim the one it left."""
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
                box.IsVisible = k == zid
        self.arrange_hot = zid

    def _min_of(self, key, g=None):
        """Return the smallest (width, height) a window can be given: from its min hook, or the client
        window's own minimum. None when it has no minimum.
        """
        hooks = self.hooks.get(key) or {}
        mn = hooks.get("min")
        if callable(mn):
            mn = safe(mn)
        if mn:
            with Kit.quiet:
                return int(mn[0]), int(mn[1])
        g = g if g is not None else self.gump_of(key)
        if isinstance(g, ClientWin):
            m = g._min_size()
            if m[0] > 0 or m[1] > 0:
                return m
        return None

    def _too_small(self, key, z, g=None):
        """Returns True, and says so in the journal, when the body of zone z (below the tab strip, if any) is
        smaller than the window's minimum.
        """
        mn = self._min_of(key, g)
        if mn is None or z is None or z.px is None:
            return False
        b = self._body(z)
        if b[2] >= mn[0] and b[3] >= mn[1]:
            return False
        Kit.say("%s needs a zone at least %d x %d." % (self.title_of(key), mn[0], mn[1]), Kit.HUE_BAD)
        return True

    def title_of(self, key):
        """Return the title shown for a window key: its registered title, else the owning module's part
        title, else the module's own title, else the key itself.
        """
        t = self.titles.get(key)
        if t is not None:
            return t
        mk, part = self.owner_of(key)
        s = dict.get(HOST.by_key, mk) if mk else None
        if s is None:
            s = HOST.page_slot(key)
            return s.title if s is not None else key
        p = s.part(part) if part else None
        return p[1] if p else s.title

    def drop_empty_bags(self, zs, W, H, ids):
        """Remove empty "<zone> bags" zones from zs, save the frame set and say so. Returns True when any
        was removed.

        Bag zones are made by pair_below for a window that rides below another. The generated default
        set is never changed. ids limits which zones are looked at.
        """
        gone = [z for z in zs.zones if z.id in ids and z.id.endswith(" bags") and z.kind == "w"
                and not self.assign.get(z.id)]
        if not gone or zs.generated or zs.name == LAYOUT_DEFAULT:
            return False
        zs.zones = [z for z in zs.zones if z not in gone]
        for z in gone:
            zs.needs.pop(z.id, None)
        self.save_frames(zs, zs.name, W, H)
        Kit.say('empty zone%s %s removed; frame layout "%s" saved.' % ("" if len(gone) == 1 else "s", ", ".join(
            '"%s"' % z.id for z in gone), zs.name), Kit.HUE_INFO)
        return True

    PAIR_MIN_H = 120

    def _flush_below(self, top, z):
        """True when zone z starts right under zone top (within the snap distance) and shares more than
        half the narrower width with it.
        """
        if top is None or z is None or top is z or top.px is None or z.px is None:
            return False
        tx, ty, tw, th = top.px
        zx, zy, zw, zh = z.px
        if abs(zy - (ty + th)) > SNAP_DIST:
            return False
        ov = min(tx + tw, zx + zw) - max(tx, zx)
        return ov * 2 > min(tw, zw)

    def _free_under(self, zs, top, H):
        """Return the y a zone placed under top could reach before meeting another zone (at most H)."""
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
        """Find or make a zone directly under the zone of top_key for the window bottom_key (for example
        the bags under the Paperdoll). Returns (top rect, bottom rect) in pixels, with the bottom None
        when no room exists, or None when zones are off or the top window has no window zone.

        Order of tries: the window's own zone when it already sits below; another zone flush below the
        top one (the one named "<zone> bags" first); then a new zone cut from the free space under the
        top zone, or from the bottom of the top zone when it is tall enough. The frame set is saved, and
        the generated default is first copied into a set of the player's own. pair_tried stops a failed
        search repeating each hop.
        """
        if not self.loaded or not self.enabled:
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
                self.assign_to(bottom_key, None, tell=False)
            return None
        if bz is not None and self._flush_below(tz, bz):
            return tz.px, bz.px
        moved = bz is not None
        best = None
        for z in zs.zones:
            if z.kind == "w" and self._flush_below(tz, z):
                tx, ty, tw, th = tz.px
                ov = min(tx + tw, z.px[0] + z.px[2]) - max(tx, z.px[0])
                rank = (z.id == "%s bags" % tz.id, ov)
                if best is None or rank > best[0]:
                    best = (rank, z)
        if best is not None:
            self.assign_to(bottom_key, best[1].id, tell=False)
            if moved:
                Kit.say('%s rides in the %s window, so it takes the zone under it ("%s").'
                           % (self.title_of(bottom_key), self.title_of(top_key), best[1].id), Kit.HUE_INFO)
            return tz.px, best[1].px
        mark = (zs.name, tz.id, tuple(tz.px))
        if self.pair_tried == mark:
            return tz.px, None
        self.pair_tried = mark
        name = zs.name
        if zs.generated or name == LAYOUT_DEFAULT:
            zs = ZoneSet.default(W, H, (), False)
            zs.name, zs.generated = LAYOUT_MINE, False
            name = LAYOUT_MINE
            tz = zs.by_id(tz.id)
            if tz is None or tz.px is None:
                return None
        else:
            zs = zs.copy()
            tz = zs.by_id(tz.id)
        old = zs.by_id("%s bags" % tz.id)
        if old is not None and old.kind == "w" and not [k for k in self.assign.get(old.id, []) if k != bottom_key]:
            zs.zones.remove(old)
        tx, ty, tw, th = tz.px
        room = self._free_under(zs, tz, H) - (ty + th)
        split = False
        if room >= max(ZONE_MIN_H, self.PAIR_MIN_H):
            nx, ny, nw, nh = tx, ty + th, tw, room
        elif th >= 2 * ZONE_MIN_H:
            split = True
            ht = max(ZONE_MIN_H, min(th - ZONE_MIN_H, int(round(th * 0.46))))
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
        Kit.say('zone "%s" made under "%s" for the bags%s; frame layout "%s" saved.' % (
            nid, tz.id, " (split in two)" if split else "", name), Kit.HUE_GOOD)
        zs2 = self.frames_in_use(W, H)
        t2, b2 = zs2.by_id(tz.id), zs2.by_id(nid)
        if t2 is None or b2 is None or t2.px is None or b2.px is None:
            return tz.px, nz.px
        return t2.px, b2.px

    def gump_of(self, key):
        """Return the open window for key (a gump or ClientWin), or None when it is closed or its getter
        fails.
        """
        w = self.wins.get(key)
        if w is None:
            return None
        try:
            g = w[0]()
        except Exception:
            return None
        return g if Kit.is_open(g) else None

    def occupied(self):
        """Returns the ids of zones that hold at least one open window, plus the zones the start-up plan
        expects to be occupied while that plan lasts.
        """
        live = set(zid for zid, keys in self.assign.items() if any(self.gump_of(key) is not None for key in keys))
        return live | self.plan_occ if self.plan_occ is not None else live

    def frames_in_use(self, W, H):
        """Return the zone set to use for a W x H screen, loading it when the screen, the choice or dirty
        changed.

        A saved set is loaded and reflowed; a missing one falls back to the generated default, built
        from the zones that are occupied. Repairs and the empty bag sweep run once after loading.
        """
        if self.frames is not None and not self.dirty and self.screen == (W, H):
            return self.frames
        zs = self.load_frames(self.frames_name, W, H) if self.frames_name != LAYOUT_DEFAULT else None
        if zs is not None:
            self._repair_stretched(zs, W, H)
            if not self.bags_swept:
                self.bags_swept = True
                self.drop_empty_bags(zs, W, H, zs.ids())
        elif self.frames_name != LAYOUT_DEFAULT:
            self.frames_name = LAYOUT_DEFAULT
            Kit.put_var(FRAMES_ACTIVE, LAYOUT_DEFAULT)
        if zs is None:
            zs = ZoneSet.default(W, H, self.occupied(), self.game_grows)
        self._overlap_shape(zs)
        self.frames, self.screen, self.dirty = zs, (W, H), False
        return zs

    @staticmethod
    def _overlap_shape(zs):
        """Keep-clear zones that may overlap windows are drawn as plain rectangles, so their arch is turned
        off.
        """
        for k in zs.zones:
            if k.kind == "k" and k.overlap:
                k.arch = False

    GV_VAR = "Layout_gameview_own"
    GV_LOCK_VAR = "Layout_gameview_lock"
    GV_MIN = (640, 480)

    def _viewport(self):
        """Return (type, instance) of the client's world viewport gump, the game view."""
        t = Tz.T("ClassicUO.Game.UI.Gumps.WorldViewportGump")
        return t, Tz.get(None, "Instance", t)

    def _vp_border(self):
        """Return the width of the game view's border: none when the game window is full size, otherwise
        five pixels.
        """
        return 0 if self._vp_full() else 5

    def _vp_set(self, x, y, w, h):
        """Place the game view so its inside is the rect (x, y, w, h), allowing for the border."""
        t, vp = self._viewport()
        b = self._vp_border()
        Tz.call(vp, "ResizeGameWindow", (ClientWin.point(w, h),), t)
        Tz.call(vp, "SetGameWindowPosition", (ClientWin.point(x - b, y - b),), t)

    def _vp_get(self):
        """Return the game view's inside rect (x, y, w, h), without its border."""
        r = ClientWin.bounds(self._viewport()[1])
        b = self._vp_border()
        return int(r.X) + b, int(r.Y) + b, int(r.Width) - 2 * b, int(r.Height) - 2 * b

    @staticmethod
    def _profile():
        """Return the client's current profile object, or None."""
        Typing._find()
        return Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None

    def _vp_full(self):
        """True when the profile has the game window at full size."""
        cur = self._profile()
        return bool(Typing._get(cur, "GameWindowFullSize", default=False)) if cur is not None else False

    def _vp_chrome(self, on):
        """Show or hide the game view's own border and button (its drag chrome)."""
        t, vp = self._viewport()
        fs = self._vp_fields
        if fs is None:
            fs = self._vp_fields = [t.GetField(n, Client.flags(public=False)) for n in ("_borderControl", "_button")]
        for f in fs:
            ctl = f.GetValue(vp) if f is not None else None
            if ctl is not None and bool(ctl.IsVisible) != bool(on):
                ctl.IsVisible = bool(on)

    def _vp_lock(self, locked):
        """Lock or unlock the game view in the profile and on the control, so it cannot be dragged."""
        cur = self._profile()
        if cur is not None:
            Tz.put(cur, "GameWindowLock", bool(locked))
        t, vp = self._viewport()
        vp.CanMove = not locked

    def _game_view(self, zs):
        """Fit the client's game view to the game zone of zs when Fit game view is on, or give it back.

        The first fit stores the player's own rect and lock in saved variables so it can be restored. A
        zone smaller than the client allows (GV_MIN) is not used, and the player is told once. Skipped
        when the game window is at full size.
        """
        want = self._game_px(zs) if self.fit_view and self.assign and not self._vp_full() else None
        if want is not None and (want[2] < self.GV_MIN[0] or want[3] < self.GV_MIN[1]):
            if not self.gv_small_told:
                self.gv_small_told = True
                Kit.say("the game view would be %d x %d, under the client's smallest (%d x %d); left as you "
                           "set it." % (want[2], want[3], self.GV_MIN[0], self.GV_MIN[1]), Kit.HUE_INFO)
            want = None
        if not self.gv_checked:
            self.gv_checked = True
            if want is None and Kit.get_var(self.GV_VAR, ""):
                self.game_view_restore()
                return
        if want == self.gv_applied:
            if want is not None:
                self._vp_chrome(False)
            return
        if want is None:
            self.game_view_restore()
            return
        if not Kit.get_var(self.GV_VAR, ""):
            Kit.put_var(self.GV_VAR, "%d,%d,%d,%d" % self._vp_get())
            cur = self._profile()
            lk = bool(Typing._get(cur, "GameWindowLock", default=False)) if cur is not None else False
            Kit.put_var(self.GV_LOCK_VAR, "1" if lk else "0")
        self._vp_set(*want)
        self._vp_chrome(False)
        self._vp_lock(True)
        self.gv_applied = want

    def game_view_restore(self):
        """Put the game view back to the rect and lock saved before the first fit, and show its border
        again.

        Does nothing when nothing was saved; the saved values are cleared once it succeeds.
        """
        self.gv_applied = None
        raw = Kit.get_var(self.GV_VAR, "")
        if not raw:
            return
        try:
            x, y, w, h = [int(v) for v in raw.split(",")]
            self._vp_set(x, y, w, h)
            if not self._vp_full():
                self._vp_chrome(True)
            lk = Kit.get_var(self.GV_LOCK_VAR, "")
            if lk:
                self._vp_lock(lk == "1")
        except Exception:
            return
        Kit.put_var(self.GV_VAR, "")
        Kit.put_var(self.GV_LOCK_VAR, "")

    def load_frames(self, name, W, H):
        """Load the saved frame set called name for the screen shape (narrow, wide or ultrawide) and reflow
        it to W x H.

        Falls back to the set saved without a shape, copying it to this shape. Zones that could not be
        read are told once. Returns None when the set is not saved.
        """
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
            HOST._tell('%s: zone "%s" in frame layout "%s" couldn\'t be read; skipped.' % (APP_NAME, zid, name))
        zs.reflow(W, H, HOST.grid_size())
        if fresh and zs.zones:
            Kit.put_var(var + "@" + cls, zs.save_text())
        return zs

    def save_frames(self, zs, name, W, H):
        """Save zs as the frame set name for this W x H screen: under its own key and under the key of its
        screen shape.

        Records edge pins, the grid and the name in the saved list.
        """
        zs.name = name
        zs.screen = (W, H)
        zs.grid = HOST.grid_size()
        for z in zs.zones:
            z.note_pins(W, H)
        text = zs.save_text()
        Kit.put_var(FRAMES_NAMED % name, text)
        cls = ratio_class(W, H)
        for k in ("narrow", "wide", "ultrawide"):
            Kit.put_var((FRAMES_NAMED % name) + "@" + k, text if k == cls else "")
        names = self.frame_names()
        if name not in names:
            names.append(name)
            Kit.put_var(FRAMES_LIST, ",".join(names))
        self.page_refresh = True

    def use_frames(self, name, tell=True):
        """Make the frame set name the one in use (the default when it does not exist) and refit.

        tell says it in the journal, with how many windows lost their zone.
        """
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
            Kit.say('frame layout "%s" in use%s.' % (name, ("; %s had no zone and are free" % Kit.count(free, "window"))
                if free else ""), Kit.HUE_GOOD)
        self.page_refresh = True

    def remove_frames(self, name):
        """Delete a saved frame set and all its screen shape copies. The default set cannot be deleted.
        Returns True when deleted.
        """
        if name == LAYOUT_DEFAULT:
            return False
        names = [n for n in self.frame_names() if n != name]
        Kit.put_var(FRAMES_LIST, ",".join(names))
        for cls in ("", "@narrow", "@wide", "@ultrawide"):
            Kit.put_var((FRAMES_NAMED % name) + cls, "")
        if self.frames_name == name:
            self.use_frames(LAYOUT_DEFAULT, tell=False)
        Kit.say('frame layout "%s" deleted.' % name, Kit.HUE_GOOD)
        self.page_refresh = True
        return True

    def window_layout_text(self, name):
        """Return the saved window layout text for name: the two built-in layouts or the saved one."""
        if name == LAYOUT_DEFAULT:
            return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_DEFAULT)
        if name == LAYOUT_MIRRORED:
            return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_MIRRORED)
        return Kit.get_var(LAYOUT_NAMED % name, "")

    def use_windows(self, name, tell=True):
        """Switches to the window layout name, or to none (every window free) when name is empty.

        The layout's frame set is switched to as well when it differs. tell says it in the journal. While
        layouts by situation are on, a switch the player makes becomes the base layout that the situations
        return to.
        """
        if (name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and name not in self.layout_names()):
            name = ""
        if self.situ["on"] and not self.situ_busy:
            self.situ["base"] = name
            self.situ_now = self.situ_last
            self.situ_pend = self.situ_back = None
            self.situ_save()
        frames, assign = (self.parse_windows(self.window_layout_text(name)) if name else (self.frames_name, {}))
        if name:
            self.unfree(None)
        else:
            self.free_by_you(list(self.wins) + [k for ks in self.assign.values() for k in ks])
        self.layout_name = name
        Kit.put_var(LAYOUT_ACTIVE, name)
        self.assign = assign
        self.save_assign()
        self.free_scrolled()
        self.placed = {}
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and frames != self.frames_name:
            self.use_frames(frames, tell=False)
        else:
            self.dirty = True
        if tell:
            API.SysMsg(('%s: window layout "%s" in use.' % (APP_NAME, name)) if name else
                       ("%s: every window is free; drop one on a zone to slot it." % APP_NAME), Kit.HUE_GOOD)
        self.page_refresh = True

    def save_windows(self, name=None):
        """Save the current window to zone assignment as a window layout (named by the player, or the
        active one).

        The built-in layouts are never overwritten; a copy called "<name> (mine)" is made instead.
        """
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
        Kit.say('window layout "%s" saved.' % name, Kit.HUE_GOOD)
        self.page_refresh = True

    CODE_HEAD, CODE_TAG, CODE_VER, CODE_FILE, CODE_MAX = "VA-", "VAL1", 1, "layout-code.txt", 8000
    CODE_RAW = 65536
    CODE_BAD = "Interface: that isn't a Virtue Assistant layout code."

    def _shipped(self, key):
        """Returns True when the window is the world map or belongs to a module that ships with Virtue
        Assistant. Share codes list only those windows.
        """
        if key == "worldmap":
            return True
        s = dict.get(HOST.by_key, self.owner_of(key)[0] or "")
        return s is not None and s.shipped

    def share_code(self):
        """Returns the share code of the layouts in use: the text VA- followed by the frame set, the zones and
        the shipped windows' assignment, packed with zlib, a one byte format number and a two byte
        checksum, written in base 64. Returns an empty string when there are no zones.

        A saved frame set is read as saved for this screen's shape rather than as reflowed to it, so the
        receiver gets the layout as it was drawn.
        """
        import zlib
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames
        if zs is None or not zs.zones:
            return ""
        if self.frames_name != LAYOUT_DEFAULT and W > 0 and H > 0:
            var = FRAMES_NAMED % self.frames_name
            text = Kit.get_var(var + "@" + ratio_class(W, H), "")
            raw = ZoneSet.parse(self.frames_name, text or Kit.get_var(var, ""))
            if raw is not None and raw.zones:
                zs = raw
        keep = {}
        for zid, keys in self.assign.items():
            ks = [k for k in keys if self._shipped(k)]
            if ks:
                keep[zid] = ks
        text = "\n".join((self.CODE_TAG, self.frames_name, zs.save_text(), self.windows_text(self.frames_name, keep)))
        data = [self.CODE_VER] + list(bytearray(zlib.compress(text.encode("utf-8"), 9)))
        c = Kit.checksum(data)
        data += [(c >> 8) & 255, c & 255]
        n = len(data)
        return self.CODE_HEAD + Kit.b64(data + [0] * (-n % 3))[:(n * 4 + 2) // 3]

    def _code_read(self, t):
        """Checks and unpacks the part of a share code after its VA- head. Returns (frame set name, ZoneSet,
        {zone id: [window keys]}) or None for anything that is not a valid code: bad length or letters,
        wrong format number, bad checksum, a pack that unpacks too big, wrong tag or lines, or no zones.
        """
        import zlib
        try:
            if len(t) % 4 == 1 or len(t) > self.CODE_MAX:
                return None
            if any(ch not in Kit.B64_REV for ch in t):
                return None
            full = Kit.unb64(t + "A" * (-len(t) % 4))
            n = len(t) * 3 // 4
            data = full[:n]
            if n < 4 or any(full[n:]) or data[0] != self.CODE_VER:
                return None
            if Kit.checksum(data[:-2]) != (data[-2] << 8 | data[-1]):
                return None
            d = zlib.decompressobj()
            raw = d.decompress(bytes(bytearray(data[1:-2])), self.CODE_RAW)
            if d.unconsumed_tail or len(raw) >= self.CODE_RAW:
                return None
            lines = raw.decode("utf-8").split("\n")
            if len(lines) != 4 or lines[0] != self.CODE_TAG:
                return None
            zs = ZoneSet.parse(lines[1], lines[2])
            if zs is None or not zs.zones:
                return None
            return lines[1], zs, self.parse_windows(lines[3])[1]
        except Exception:
            return None

    def load_code(self, text):
        """Loads a pasted share code: saves its frame set and window layout under a name ending in (shared),
        fitted to this screen, adds it to the layout list and switches to it. Tells the player and returns
        False when the text is not a valid code.
        """
        t = re.sub(r"\s+", "", str(text or ""))
        got = self._code_read(t[len(self.CODE_HEAD):]) if t.startswith(self.CODE_HEAD) else None
        if got is None:
            API.SysMsg(self.CODE_BAD, Kit.HUE_BAD)
            return False
        name, zs, assign = got
        name = name[:-9] if name.endswith(" (shared)") else name
        nm = self.clean_name(name, "Shared")[:15].strip() + " (shared)"
        W, H = Kit.screen()
        if W <= 0 or H <= 0:
            W, H = zs.screen
        if (W, H) != zs.screen:
            zs.reflow(W, H, HOST.grid_size())
        self.save_frames(zs, nm, W, H)
        Kit.put_var(LAYOUT_NAMED % nm, self.windows_text(nm, assign))
        names = self.layout_names()
        if nm not in names:
            names.append(nm)
            Kit.put_var(LAYOUT_LIST, ",".join(names))
        self.use_windows(nm)
        return True

    SITU_VAR = "VirtueAssistant_layout_situations"
    SITU_KINDS = ("war", "bank", "dungeon", "town")
    SITU_SAY = {"war": "war mode", "bank": "bank", "dungeon": "dungeon", "town": "town"}
    SITU_EVERY, SITU_HOLD, SITU_WAR_HOLD, SITU_BANK_FOR, SITU_BANK_NEAR = 1.0, 2.0, 0.5, 300.0, 8

    def situ_load(self):
        """Reads the saved settings of layouts by situation (on or off, the layout for each situation and the
        base layout) and clears the running state.
        """
        s = {"on": False, "base": ""}
        for k in self.SITU_KINDS:
            s[k] = ""
        for k, v in Kit.codec_load(Kit.get_var(self.SITU_VAR, "")).items():
            if k == "on":
                s["on"] = v == "1"
            elif k in s:
                s[k] = self.clean_name(v, "")
        self.situ = s
        self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None
        self.situ_at = 0.0

    def situ_park(self):
        """Writes the layout, frame set and window assignment that were in use before a situation took over
        back into the saved variables when the script stops, so a restart does not keep the situation's
        layout. Does nothing when no situation is active.
        """
        b, self.situ_back = self.situ_back, None
        if b is None or not self.situ_now:
            return
        Kit.put_var(LAYOUT_ACTIVE, b[0])
        Kit.put_var(FRAMES_ACTIVE, b[1])
        Kit.put_var(LAYOUT_VAR, self.windows_text(b[1], b[2]))

    def situ_save(self):
        """Saves the situation settings as one variable of name=value pairs."""
        s = self.situ
        Kit.put_var(self.SITU_VAR, ";".join(["on=%d" % (1 if s["on"] else 0)] + [
            "%s=%s" % (k, s.get(k, "")) for k in self.SITU_KINDS + ("base",)]))

    def situ_set(self, on):
        """Switches layouts by situation on or off. Off while a situation is active goes back to the base
        layout; on takes the layout in use as the base.
        """
        on = bool(on)
        if on == self.situ["on"]:
            return
        if not on and self.situ_now:
            self._situ_go("", self.situ["base"], self.situ_now)
        self.situ["on"] = on
        self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None
        self.situ_at = 0.0
        if on:
            self.situ["base"] = self.layout_name
        self.situ_save()

    def situ_pick(self, kind, name):
        """Sets the layout (name) used for situation kind (war, bank, dungeon or town) and saves it."""
        if kind not in self.SITU_KINDS:
            return
        self.situ[kind] = self.clean_name(name, "")
        self.situ_now = self.situ_pend = None
        self.situ_save()

    def _bank_note(self, now, w):
        """Remembers when and where the bank was last seen open (now, and w = x, y and facet from Guard), so
        the bank situation holds while the player stays near it.
        """
        try:
            b = int(API.Bank or 0)
            it = API.FindItem(b) if b else None
            up = it is not None and bool(it.Opened)
        except Exception:
            up = False
        if up and w is not None:
            self.situ_bank = (now, w[0], w[1], w[2])

    def situ_want(self, now):
        """Returns (situation kind, layout name) that fits the player right now: the first kind that has a
        layout and applies, in the order war mode, bank, dungeon, town; otherwise ("", the base layout).
        The bank applies for SITU_BANK_FOR seconds after it was opened while the player stays within
        SITU_BANK_NEAR tiles on the same facet; a dungeon is one of DUNGEON_AREAS; a town is a guarded area.
        """
        s = self.situ
        w = None
        if s["bank"]:
            w = Guard._where()
            self._bank_note(now, w)
        for kind in self.SITU_KINDS:
            if not s[kind]:
                continue
            if kind == "war":
                me = HOST.me()
                hit = me is not None and bool(me.InWarMode)
            elif kind == "bank":
                b = self.situ_bank
                hit = (w is not None and now - b[0] <= self.SITU_BANK_FOR and b[3] == w[2]
                       and max(abs(b[1] - w[0]), abs(b[2] - w[1])) <= self.SITU_BANK_NEAR)
            elif kind == "dungeon":
                if w is None:
                    w = Guard._where()
                hit = False
                for a in DUNGEON_AREAS:
                    if w is not None and a[0] == w[2] and a[1] <= w[0] <= a[3] and a[2] <= w[1] <= a[4]:
                        hit = True
            else:
                hit = GUARD.guarded() is True
            if hit:
                return kind, s[kind]
        return "", s["base"]

    def situ_tick(self, now, busy=False):
        """Called from the Interface module's tick with the time now: at most every SITU_EVERY seconds works out the
        wanted situation and switches layouts once it has held for SITU_HOLD seconds (SITU_WAR_HOLD for war
        mode, so it reacts quickly). Nothing switches while busy, in Arrange mode or while a window is
        dragged.
        """
        if not self.situ["on"] or not self.enabled or now < self.situ_at:
            return
        self.situ_at = now + self.SITU_EVERY
        if self.situ_now == "" and self.layout_name != self.situ["base"]:
            self.situ["base"] = self.layout_name
            self.situ_back = None
            self.situ_save()
        try:
            kind, name = self.situ_want(now)
        except Exception:
            return
        self.situ_last = kind
        was = self.situ_now
        if kind == was:
            self.situ_pend = None
            return
        if was is None and name == self.layout_name:
            self.situ_now, self.situ_pend = kind, None
            return
        hold = self.SITU_WAR_HOLD if kind == "war" else self.SITU_HOLD
        p = self.situ_pend
        if p is None or p[0] != kind:
            self.situ_pend = (kind, now)
            self.situ_at = now + min(hold, self.SITU_EVERY)
            return
        if now - p[1] < hold:
            self.situ_at = min(self.situ_at, p[1] + hold)
            return
        if busy or self.arrange or SNAP.pressed():
            return
        self.situ_now, self.situ_pend = kind, None
        self._situ_go(kind, name, was)

    def _situ_go(self, kind, name, was):
        """Switches to layout name for situation kind ("" means back to the base layout; was is the situation
        that was active). The layout and window assignment in use before the first switch is kept in
        situ_back and put back exactly when the player leaves every situation. Says it in the journal.
        """
        if name == self.layout_name and (kind or self.situ_back is None):
            return
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and name not in self.layout_names():
            return
        if kind and was in ("", None) and self.situ_back is None:
            self.situ_back = (self.layout_name, self.frames_name, dict((z, list(v)) for z, v in self.assign.items()))
        back = self.situ_back if not kind else None
        self.situ_busy = True
        try:
            self.use_windows(name, tell=False)
        finally:
            self.situ_busy = False
        if back is not None:
            self.situ_back = None
            if back[0] == name:
                if back[1] != self.frames_name:
                    self.use_frames(back[1], tell=False)
                self.unfree(None)
                self.assign = back[2]
                self.save_assign()
                self.placed = {}
                self.dirty = True
        t = name or "(none)"
        API.SysMsg("Interface: %s layout (%s)." % (t, self.SITU_SAY[kind]) if kind else "Interface: back to %s." % t,
                   Kit.HUE_INFO)

    def free_scrolled(self):
        """Give back windows that are fitted or sized by a zone but no longer held by one: undo their fit,
        and put scrolling windows at their own size.
        """
        for key in [k for k in self.fitted if not self.holds(k)]:
            self._unfit(key)
        for key, rect in list(self.placed.items()):
            if not self.holds(key):
                g = self.gump_of(key)
                info = Kit.scroll_info(g) if g is not None else None
                if info is not None:
                    with Kit.quiet:
                        Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"])
                        Kit.moved_by_code(g)
                self.placed.pop(key, None)

    def keep(self, W, H, only=None):
        """The main placement pass for a W x H screen: hold every window that has a zone and put it in its
        slot.

        Runs on the client tick (many windows may be dragged or opened between passes, so it is re-run
        when something changes: dirty, fresh, a new window). only limits the pass to those gumps. With
        zones off it undoes everything instead. Steps: pick the zone set; hold the client journal, watch
        dropped client windows, redraw the Arrange overlay and repair homes; then for each zone collect
        its open, visible windows (with the windows that follow them), give each a slot with _slots, fit
        it with _fit_slot, hide all but the shown window of a tabbed zone, release windows that left their
        zone, strip or restore the seamless chrome, keep the tab strips, fit the game view and grow zones
        that asked for more room. Windows that moved get their moved callback after one flush.
        """
        if not self.loaded or W <= 0 or H <= 0:
            return
        if not self.enabled:
            self.fresh_adds.clear()
            self._off()
            return
        occ = self.occupied()
        if occ != self.occ:
            self.occ = occ
            if self.frames_name == LAYOUT_DEFAULT:
                self.dirty = True
        zs = self.frames_in_use(W, H)
        Kit.flush()
        self.fresh = False
        self.fresh_adds.clear()
        Fill.prune()
        if self.behind:
            self._tabs_prune(zs)
        for key in [k for k in self.fitted if not self.holds(k)]:
            self._unfit(key)
        now = time.time()
        # Each job is isolated: one failing job must not stop the rest of the pass.
        jobs = [(self._hold_journal, (zs, H)), (self._client_drops, ()), (self._arrange_tick, (zs, W, H))]
        if now >= self.repair_at and not SNAP.drag:
            self.repair_at = now + 2.0
            jobs.append((self._repair, (zs,)))
        for fn, args in jobs:
            try:
                fn(*args)
            except Exception:
                pass
        drag = SNAP.drag
        told = []
        seen = set()
        jobs = []
        if only is None:
            self.gump_key = {}
        for z in (zs.zones if self.assign else ()):
            keys = self.assign.get(z.id)
            if not keys or z.kind != "w" or z.px is None:
                continue
            if only is not None and not any(self.gump_of(k) in only for k in keys):
                continue
            items = []
            for key in keys:
                g = self.gump_of(key)
                if g is None:
                    continue
                self.gump_key[g] = key
                # A window already ridden by another (attached), hidden or listed twice is left to its owner.
                if g in seen or g in SNAP.attached or not Snap.visible(g):
                    continue
                riding = (self.hooks.get(key) or {}).get("riding")
                if riding is not None:
                    try:
                        if riding():
                            continue
                    except Exception:
                        pass
                seen.add(g)
                self._hold(g, key)
                r = Snap.rect(g)
                if r is None:
                    if isinstance(g, ClientWin):
                        try:
                            g.rect()
                            why = "it has no size"
                        except Exception as ex:
                            why = Tz.why(ex)
                        g.fail["size"] = "its place and size couldn't be read (%s)" % why
                        g.report()
                    continue
                hooks = self.hooks.get(key) or {}
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
            # In a tabbed zone only the shown window stays on screen; the others are marked as behind it.
            if items and z.stack == "t":
                shown = self.tab_shown(z)
                for it in items:
                    if it[0] != shown:
                        self.behind[it[0]] = z.id
            if items:
                jobs.extend((it, slot, z) for it, slot in zip(items, self._slots(z, items)))
        # Kit._behind is the set of gumps kept off screen behind tabs, shared with the snap code.
        if self.behind or Kit._behind:
            Kit._behind = set(g for g in map(self.gump_of, self.behind) if g is not None)
        # Padding between windows: thin in One panel mode, the full margin for a solo zone.
        thin, full = (Seam.pad(),) * 4, (Kit.MARGIN,) * 4
        small = set()
        for it, slot, z in jobs:
            if it[1] in drag:
                continue
            if self._small(it[0], z, it[1]):
                small.add(it[1])
                self.placed[it[0]] = slot
                if it[0] in self.fitted:
                    self._unfit(it[0])
                if self._move_all(it[1], it[4], it[2], slot[0], slot[1]):
                    told.append(it[1])
                continue
            try:
                pads = (full if z.solo else thin) if self.seamless and it[0] not in self.behind else None
                if self._fit_slot(it, slot, z, pads):
                    told.append(it[1])
            except Exception:
                self.placed[it[0]] = slot
        if only is None:
            self._release(seen)
            for g in [g for g in Seam.recs if g not in seen]:
                Seam.undo(g)
        bare = set()
        if self.seamless and self.enabled:
            for it, slot, z in [j for j in jobs if j[0][1] not in small and j[0][0] not in self.behind]:
                for g in [it[1]] + list(it[4]):
                    try:
                        if not isinstance(g, ClientWin) and Seam.strip(g, g is it[1] and it[5].get("untitled")):
                            bare.add(g)
                    except Exception:
                        pass
        for g in ([g for g in Seam.bare if g not in bare] if only is None else ()):
            Seam.unstrip(g)
        if only is None and (self.strips or self.behind or any(z.stack == "t" for z in zs.zones)):
            try:
                self._strips_keep(zs)
            except Exception:
                pass
        try:
            self._game_view(zs)
        except Exception:
            pass
        if self.assign and self.need_due:
            self.need_due = False
            zs.reflow(W, H, HOST.grid_size())
        # The start-up plan only lasts while the script is starting, or until the zones it was made for change.
        if self.plan_occ is not None and (not HOST.booting() or self._plan_sig(zs) != self.plan_sig):
            self.plan_drop()
        if told:
            Kit.flush()
            for g in told:
                fn = SNAP.moved_cb.get(g)
                if fn is not None:
                    try:
                        fn()
                    except Exception:
                        pass

    def _base(self, key, g, ext, mini):
        """Return the natural (width, height) of a window used to weigh it against others in its zone.

        A minimised window uses its current size; otherwise the size it had before it was filled,
        remembered per key.
        """
        if mini:
            return ext[2], ext[3]
        b = self.base.get(key)
        if b is None:
            rec = Fill.recs.get(g)
            b = rec["nat"] if rec is not None else (ext[2], ext[3])
            self.base[key] = b
        return b

    def _slots(self, z, items):
        """Divides the zone z among the items (windows) and returns one (x, y, w, h) slot per item.

        Windows are stacked along the zone's stack direction (d down, u up, r right, l left). Slots are
        shared by the windows' natural sizes; a minimised window keeps its own length when others are
        open. When the fixed parts do not fit, all windows are shared by weight. In a tabbed zone (t)
        every window gets the whole body below the tab strip.
        """
        if z.stack == "t":
            return [self._body(z)] * len(items)
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
        if free < n or total <= 0:
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
        pos = (zy if z.stack == "d" else zy + zh if z.stack == "u" else zx if z.stack == "r" else zx + zw)
        back = z.stack in ("u", "l")
        for ln in lens:
            if back:
                pos -= ln
            out.append((zx, pos, zw, ln) if down else (pos, zy, ln, zh))
            if not back:
                pos += ln
        return out

    TABS_VAR = "VirtueAssistant_layout_tabs"
    TABS_CAP = 64

    @staticmethod
    def _body(z):
        """Returns the rectangle of zone z that windows fill: the zone itself, or below the tab strip when the
        zone is tabbed.
        """
        zx, zy, zw, zh = z.px
        return (zx, zy + TAB_H, zw, max(1, zh - TAB_H)) if z.stack == "t" else (zx, zy, zw, zh)

    @staticmethod
    def _tabs_parse(text):
        """Reads the saved tab choices (zone id=window key pairs joined by semicolons) into a dict."""
        out = {}
        for part in str(text or "").split(";"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            if k.strip() and v.strip():
                out[k.strip()] = v.strip()
        return out

    def _tabs_save(self):
        """Saves the chosen tab of each tabbed zone."""
        Kit.put_var(self.TABS_VAR, ";".join("%s=%s" % kv for kv in sorted(self.tabs.items())))

    def tab_shown(self, z):
        """Returns the key of the window shown in tabbed zone z: the player's pick while it is still open and
        usable, else the first usable window, else the first. None when the zone has no windows.
        """
        keys = self.assign.get(z.id, [])
        if not keys:
            return None
        k = self.tabs.get(z.id)
        if k in keys and self._tab_ok(k):
            return k
        return next((k for k in keys if self._tab_ok(k)), keys[0])

    def _tab_ok(self, key):
        """Returns True when the window is open, visible and not riding along with another window, so it can
        be shown as a tab.
        """
        g = self.gump_of(key)
        if g is None or not Snap.visible(g):
            return False
        riding = (self.hooks.get(key) or {}).get("riding")
        return riding is None or not safe(riding, False)

    def tab_pick(self, zid, key):
        """Shows window key in tabbed zone zid, saves the choice (the saved list is trimmed to the zones in
        use past TABS_CAP) and asks for a fresh placement pass. Returns False when the window is not in
        that zone.
        """
        zid, key = str(zid), str(key)
        if key not in self.assign.get(zid, ()):
            return False
        if self.tabs.get(zid) != key:
            self.tabs[zid] = key
            if len(self.tabs) > self.TABS_CAP:
                self.tabs = dict(kv for kv in self.tabs.items() if kv[0] in self.assign)
            self._tabs_save()
        for k in self.assign.get(zid, ()):
            self.seam_skip.pop(k, None)
            self.seam_wait.pop(k, None)
        self.fresh = True
        HOST.poke()
        return True

    def spot(self, key):
        """Returns the slot a window is held in. A window waiting behind a tab reports it with x at TAB_X, off
        the screen, which is where it is kept.
        """
        slot = self.placed.get(key)
        if slot is None:
            return self.plan_at(key)
        if key not in self.behind:
            return slot
        return (TAB_X,) + tuple(slot[1:])

    def _unhide(self, key):
        """Brings window key back from behind a tab: forgets that it is hidden and moves it from the off screen
        place back to its slot.
        """
        self.behind.pop(key, None)
        g = self.gump_of(key)
        if g is None:
            return
        Kit._behind.discard(g)
        r = Snap.rect(g)
        if r is None or r[0] > TAB_X // 2:
            return
        slot = self.placed.get(key)
        x = slot[0] if slot is not None else Kit.clamp(0, r[1], r[2], r[3])[0]
        self._move_all(g, SNAP.followers(g), r, x, r[1])

    def _tabs_prune(self, zs):
        """Unhides every hidden window whose zone no longer holds it as a hidden tab (the zone changed, the
        window moved or it is the shown tab now).
        """
        for key, zid in list(self.behind.items()):
            z = zs.by_id(zid) if zs is not None else None
            if (z is None or z.stack != "t" or z.kind != "w" or z.px is None or not self.holds(key)
                    or self.zone_of(key) != zid or self.tab_shown(z) == key):
                self._unhide(key)

    def _tabs_off(self):
        """Unhides every window and removes every tab strip; part of switching zones off."""
        for key in list(self.behind):
            self._unhide(key)
        Kit._behind = set()
        for s in list(self.strips.values()):
            Kit.dispose(s["g"])
        self.strips = {}

    def _strips_keep(self, zs):
        """Keeps one tab strip window per tabbed zone that has windows: removes strips of zones that are gone
        and rebuilds a strip only when its signature (place, windows, shown tab, titles, look, alpha)
        changed.
        """
        want = {}
        for z in (zs.zones if self.assign else ()):
            if z.stack != "t" or z.kind != "w" or z.px is None:
                continue
            keys = tuple(k for k in self.assign.get(z.id, []) if self.gump_of(k) is not None)
            if keys:
                want[z.id] = (tuple(z.px), keys, self.tab_shown(z), tuple(self.title_of(k) for k in keys), Kit.look(),
                              Kit.SECTION_ALPHA)
        for zid in [k for k in self.strips if k not in want]:
            Kit.dispose(self.strips.pop(zid)["g"])
        for zid, sig in want.items():
            s = self.strips.get(zid)
            if s is not None and s["sig"] == sig and Kit.is_open(s["g"]):
                continue
            old = s["g"] if s is not None else None
            self.strips[zid] = {"g": self._strip(zid, sig), "sig": sig}
            Kit.dispose(old)

    def _strip(self, zid, sig):
        """Builds the tab strip gump of one zone from its signature sig: one button and title per window, the
        shown tab in the title colour, laid across the top of the zone. Clicking a tab shows that window.
        """
        (x, y, w, h), keys, shown, titles = sig[0], sig[1], sig[2], sig[3]
        g = G.CreateGump(True, False)
        Kit.add_section(g, 0, 0, w, TAB_H)
        share = max(1, w // len(keys))
        bw, bh = Kit.pic_size(Kit.ART_PAGE[0])
        bw, bh = bw or 30, bh or 22
        for i, (k, t) in enumerate(zip(keys, titles)):
            bx = i * share + 4
            fn = self._tab_click(zid, k)
            tip = "Show %s in this zone" % t
            b = G.CreateGumpButton("", Kit.HUE_TEXT, Kit.ART_PAGE[0], Kit.ART_PAGE[1], Kit.ART_PAGE[2])
            b.SetPos(bx, max(0, (TAB_H - bh) // 2))
            g.Add(b)
            Kit.on_click(b, fn)
            Kit.with_tip(b, tip)
            lbl = Kit.add_label(g, Kit.fit(t, max(10, share - bw - 15)), bx + bw + 5, max(0, (TAB_H - 16) // 2),
                                Kit.HUE_TITLE if k == shown else Kit.HUE_TEXT)
            lbl.SetAcceptMouseInput(True)
            Kit.on_click(lbl, fn)
            Kit.with_tip(lbl, tip)
        g.SetRect(x, y, w, TAB_H)
        g.CanMove = False
        Kit.add_front(g)
        SNAP.skip_gump(g)
        return g

    def _tab_click(self, zid, key):
        """Returns the click handler of the tab for window key in zone zid."""
        def hit():
            """Click handler: shows the window of this tab."""
            self.tab_pick(zid, key)

        return hit

    def retry_due(self, now):
        """True when a window that is waiting for the seamless fit has come due for another try.

        Adds each waiting window to fresh_adds; waits older than twice SEAM_WAIT, or windows that are
        closed or no longer held, are dropped.
        """
        if not self.seam_wait or now < self.retry_at:
            return False
        self.retry_at = now + SEAM_RETRY
        for key, was in list(self.seam_wait.items()):
            g = self.gump_of(key)
            if g is None or not Snap.visible(g) or not self.holds(key) or now - was[1] > 2 * SEAM_WAIT:
                self.seam_wait.pop(key, None)
            else:
                self.fresh_adds.add(g)
        return bool(self.fresh_adds)

    def plan(self):
        """Plans where each zoned window will sit before any of them is open, so a window built during
        start-up can open straight in its slot instead of being moved afterwards. Called once when the
        modules are queued to start.

        Works from the saved assignment: a zone counts as occupied when a window in it is open or its
        module and part are on. Fills planned (window key to body rectangle, zone and seamless padding) for
        each window zone that holds exactly one window, or the shown tab of a tabbed zone, and plan_occ
        with the occupied zones. Returns True when anything was planned.
        """
        self.plan_drop()
        W, H = Kit.screen()
        o = dict.get(HOST.by_key, LAYOUT_OWNER)
        if not self.loaded or not self.assign or W <= 0 or H <= 0 or o is None or not o.enabled:
            return False
        on = {}
        for zid, keys in self.assign.items():
            for key in keys:
                mk, part = self.owner_of(key)
                s = dict.get(HOST.by_key, mk) if mk else None
                if self.gump_of(key) is not None or (s is not None and s.enabled
                                                     and (part is None or s.parts_on.get(part))):
                    on.setdefault(zid, []).append(key)
        self.plan_occ = set(on)
        self.occ = self.occupied()
        if self.frames_name == LAYOUT_DEFAULT:
            self.dirty = True
        zs = self.frames_in_use(W, H)
        self.fresh = False
        pad = (Seam.pad(),) * 4
        for z in zs.zones:
            keys = on.get(z.id)
            if not keys or z.kind != "w" or z.px is None:
                continue
            if z.stack == "t":
                k = self.tabs.get(z.id)
                keys = [k if k in keys else keys[0]]
            elif len(keys) > 1:
                continue
            pads = ((Kit.MARGIN,) * 4 if z.solo else pad) if self.seamless else None
            self.planned[keys[0]] = (tuple(self._body(z)), z, pads)
        self.plan_sig = self._plan_sig(zs)
        return bool(self.planned)

    def _plan_sig(self, zs):
        """Returns a signature of the plan (screen, frame set, assignment, seamless setting and the planned
        zone rectangles), so a later pass can tell that the plan no longer holds.
        """
        ids = set(p[1].id for p in self.planned.values())
        px = [(z.id, z.px) for z in zs.zones if z.id in ids]
        return zs.screen, self.frames_name, self.windows_text(), self.seamless, sorted(px)

    def plan_drop(self):
        """Forgets the start-up plan."""
        self.planned, self.plan_occ, self.plan_sig = {}, None, None

    def plan_prune(self):
        """Drops from plan_occ the zones whose windows are not open any more. Returns True when it changed
        anything, so the start-up settle check waits another round.
        """
        if not self.plan_occ:
            return False
        live = set(z for z in self.plan_occ if any(self.gump_of(k) is not None for k in self.assign.get(z, ())))
        if live == self.plan_occ:
            return False
        self.plan_occ = live
        return True

    def plan_at(self, key):
        """Returns the planned slot of window key, or None. The plan is dropped (and None returned) as soon as
        start-up is over. With One panel mode on and on the client thread, the slot is grown to cover the
        gap between windows, as _fit_slot would.
        """
        p = self.planned.get(key) if self.planned else None
        if p is not None and not HOST.booting():
            self.plan_drop()
            return None
        if p is None or not self.holds(key):
            return None
        slot, z, pads = p
        if pads is not None and Client.on_client_thread() and not (self.hooks.get(key) or {}).get("untitled"):
            grown = Seam.grow(slot, Seam.clip(slot, pads))
            if grown[3] <= Kit.screen()[1]:
                return grown
        return slot

    def fit_added(self, key):
        """Fits window key straight away when it was just added to the layout and has a planned slot, so it
        does not flash at the wrong place or size.
        """
        key = str(key)
        g = self.gump_of(key) if key in self.planned else None
        if g is not None and Snap.visible(g):
            self.fit_now(key, g)

    def fit_now(self, key, g):
        """Fits one window straight away, without waiting for the next pass, using its last slot (or its
        planned slot while starting).

        Used when a window redraws itself in One panel mode and would flash at the wrong size. Only on
        the client thread, and not while the layout is dirty (unless the window is planned), the window is
        dragged, attached or has followers. A window behind a tab is kept hidden.
        """
        was = self.slot_was.get(key) or (self.planned.get(key) if self.planned else None)
        if key in self.behind:
            Kit._behind.add(g)
        if (was is None or not (self.seamless and self.enabled) or key not in self.wins
                or ((self.dirty or self.fresh) and key not in self.planned) or g in SNAP.drag
                or g in SNAP.attached or not Client.on_client_thread()):
            return
        Kit.flush()
        hooks = self.hooks.get(key) or {}
        r = Snap.rect(g)
        if r is None or hooks.get("riding") is not None or SNAP.followers(g):
            return
        try:
            mini = hooks.get("state") is not None and hooks["state"]() == "minimized"
        except Exception:
            mini = False
        slot, z, pads = was
        self.gump_key[g] = key
        try:
            self._fit_slot((key, g, r, r, [], hooks, mini, self._base(key, g, r, mini)), slot, z, pads)
            if not isinstance(g, ClientWin) and key not in self.behind:
                Seam.strip(g, hooks.get("untitled"))
        except Exception:
            pass

    def _fit_slot(self, it, slot, z=None, pads=None):
        """Put the window of item it into slot (inside zone z), with the seamless padding pads when One
        panel mode is on.

        Returns True when anything moved. In One panel mode the slot is first grown to cover the gap
        between windows; the grown slot is kept only if the window really reaches it, otherwise it is
        retried for SEAM_WAIT seconds and then falls back to the plain slot (seam_skip). The item is the
        tuple built in keep.
        """
        key, g, r, ext, fol, hooks, mini, base = it
        ins = int(hooks.get("inset") or 0)
        if g in Seam.recs and not Client.on_client_thread():
            return False
        self.slot_was[key] = (slot, z, pads)
        slot = (slot[0] - ins, slot[1] - ins, slot[2] + 2 * ins, slot[3] + 2 * ins)
        self.placed[key] = slot
        if pads is not None:
            pads = Seam.clip(slot, pads)
        grown = Seam.grow(slot, pads) if pads is not None else None
        if (grown is not None and self.seam_skip.get(key) != slot and Seam.can(g, hooks, mini)
                and grown[3] <= Kit.screen()[1]):
            self.placed[key] = grown
            if Seam.holds(g, slot, pads, grown, r):
                return False
            Seam.undo(g)
            Seam.unstrip(g)
            self._fit_at(it, grown, z, ins)
            r2 = Snap.rect(g)
            rec = Fill.recs.get(g)
            S = self.MISFIT_SLACK
            if r2 is not None and (rec is None or rec.get("k", 1.0) >= 0.995):
                if r2[:2] != grown[:2]:
                    self._move_all(g, fol, r2, grown[0], grown[1])
                if fol or (abs(r2[2] - grown[2]) <= S and abs(r2[3] - grown[3]) <= S):
                    self.seam_wait.pop(key, None)
                    return Seam.trim(g, slot, pads)
                was = self.seam_wait.get(key)
                now = time.time()
                if was is None or was[0] != slot:
                    was = self.seam_wait[key] = (slot, now)
                if now - was[1] < SEAM_WAIT:
                    return False
            self.seam_skip[key] = slot
            self.placed[key] = slot
        self.seam_wait.pop(key, None)
        if g in Seam.recs:
            Seam.undo(g)
        return self._fit_at(it, slot, z, ins)

    def _fit_at(self, it, slot, z, ins):
        """Sizes and places the window at slot: its fit hook if it has one, else the general fill; then moves
        it and the windows that follow it.

        Hooks used: fit (size to w, h), exact (position exactly), verify (check the size took), fill
        (fill style), pieces_out (followers sit outside the slot), client (client window). A window behind
        a tab is kept at TAB_X. Returns True when anything moved.
        """
        key, g, r, ext, fol, hooks, mini, base = it
        sx, sy, sw, sh = slot
        fit_fn = hooks.get("fit")
        rec = self.fitted.get(key)
        if fit_fn is not None:
            tw, th = sw, sh
            if fol and not hooks.get("pieces_out"):
                tw, th = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            told = rec.get("told") if rec is not None else None
            # The window is only told a new size when it changed by more than 4 pixels, or just became exactly
            # the slot.
            if told is None or abs(told[0] - tw) > 4 or abs(told[1] - th) > 4 \
                    or (told != (tw, th) and (tw, th) == (sw, sh)) or hooks.get("client"):
                self.fitted[key] = rec = {"kind": "fit", "told": (tw, th)}
                try:
                    fit_fn(tw, th, "w")
                except Exception:
                    pass
        elif rec is None:
            self.fitted[key] = {"kind": "fill"}
        if hooks.get("exact"):
            gx, gy = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
            if hooks.get("pieces_out"):
                gx, gy = sx, sy
            if isinstance(g, ClientWin):
                gx, gy = self._client_overflow(key, g, z, gx, gy, sw, sh, ins)
                self.client_target[key] = (gx, gy)
            if fit_fn is not None and hooks.get("verify"):
                self._verify(key, g, r, rec, fit_fn, mini)
                # A window that misses the size it was told for eight passes falls back to the general fill.
                fb = self.fallback.get(key)
                if fb is not None and not mini and not fol:
                    if fb != (sw, sh):
                        self.fallback.pop(key, None)
                    else:
                        done = Fill.fit(g, sx, sy, sw, sh, hooks.get("fill") or "anchor")
                        if done is not None:
                            if done:
                                Kit.moved_by_code(g)
                            return bool(done)
            return self._move_all(g, fol, r, gx, gy)
        if fol:
            if hooks.get("pieces_out"):
                lx, ly, lw, lh = sx, sy, sw, sh
            else:
                lx, ly = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
                lw, lh = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            if lw < 40 or lh < 20:
                return self._move_all(g, fol, r, sx + (r[0] - ext[0]), sy + (r[1] - ext[1]))
            done = Fill.fit(g, lx, ly, lw, lh, hooks.get("fill") or "anchor")
            if done is None:
                return self._move_all(g, fol, r, lx, ly)
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
        if done is None:
            Fill.unfit(g)
            info = Kit.scroll_info(g)
            fw, fh = (info["w"], info["h"]) if info is not None else (r[2], r[3])
            if (r[0], r[1]) == (TAB_X if g in Kit._behind else sx, sy) and r[3] == min(fh, sh):
                return False
            Kit._place_raw(g, sx, sy, fw, fh, None, sh if fh > sh else None)
            done = True
        if done:
            Kit.moved_by_code(g)
        return bool(done)

    @staticmethod
    def _move_all(g, fol, r, x, y):
        """Moves gump g, and the windows that follow it by the same distance, to (x, y). A window behind a tab
        keeps its off screen x. Returns True when it moved.
        """
        if g in Kit._behind:
            x = TAB_X
        if (r[0], r[1]) == (x, y):
            return False
        Snap.move(g, x, y)
        Kit.moved_by_code(g)
        for f in fol:
            pf = Snap.pos(f)
            if pf is not None:
                Snap.move(f, pf[0] + x - r[0], pf[1] + y - r[1])
                Kit.moved_by_code(f)
        return True

    def _client_overflow(self, key, g, z, gx, gy, sw, sh, ins):
        """Place a client window that has a minimum larger than its slot so it spills over the least
        valuable area.

        Tries the window shifted by none, half and all of the overflow on each axis and takes the
        cheapest: overlap with window zones costs 100 per pixel, with other zones 10, and area off
        screen costs 1. Tells the player once how big the zone needs to be.
        """
        try:
            mw, mh = g._min_size()
        except Exception:
            return gx, gy
        rw, rh = max(sw, mw), max(sh, mh)
        if rw <= sw and rh <= sh:
            return gx, gy
        zs = self.frames
        W, H = Kit.screen()
        if (z is not None and z.px is not None and (key, z.id, z.px) != self.small_said):
            self.small_said = (key, z.id, z.px)
            Kit.say('%s needs zone "%s" to be at least %d x %d; it is %d x %d.' % (
                self.title_of(key), z.id, max(z.px[2], mw - 2 * ins), max(z.px[3], mh - 2 * ins), z.px[2],
                z.px[3]), Kit.HUE_BAD)
        ox, oy = rw - sw, rh - sh

        def cost(x, y):
            """Return the placement cost of putting the oversized window at (x, y): weighted overlap with other
            zones plus area off screen.
            """
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

    MISFIT_SLACK = 2

    def _verify(self, key, g, r, rec, fit_fn, it_mini=False):
        """Check that a window took the size it was told. After more than a slack of 2 pixels off, retry
        the fit on passes 2, 4, 8 and so on and, at the eighth miss, record a fallback size so the
        general fill takes over.
        """
        told = rec.get("told") if rec is not None else None
        if told is None or SNAP.drag:
            return
        if it_mini or not (abs(r[2] - told[0]) > self.MISFIT_SLACK or abs(r[3] - told[1]) > self.MISFIT_SLACK):
            self.misfit.pop(key, None)
            return
        n = self.misfit.get(key, 0) + 1
        self.misfit[key] = n
        if n == 8 and key not in self.fallback:
            self.fallback[key] = (int(told[0]), int(told[1]))
        if n >= 2 and n & (n - 1) == 0:
            try:
                fit_fn(told[0], told[1], "again")
            except Exception:
                pass

    def _unfit(self, key):
        """Stop fitting a window: forget its records, tell its fit hook to free the window, undo any
        seamless chrome and fill.
        """
        rec = self.fitted.pop(key, None)
        for d in (self.base, self.misfit, self.fallback, self.client_settle, self.slot_was):
            d.pop(key, None)
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
        if g is not None and g in Seam.recs:
            Seam.undo(g)
        if g is not None:
            Fill.unfit(g)

    def _small(self, key, z, g):
        """Returns True when zone z is smaller than the window's minimum; asked once per zone size and stack,
        then remembered.
        """
        sig = (z.id, tuple(z.px), z.stack)
        was = self.min_seen.get(key)
        if was is None or was[0] != sig:
            was = self.min_seen[key] = (sig, self._too_small(key, z, g))
        return was[1]

    def report_fit(self):
        """Settings button (Check fit): says in the journal, zone by zone, whether each zoned window fills its
        zone.

        Lists empty zones, windows assigned but not open, windows waiting behind a tab, each window's size
        and place against its slot (a window riding with another counts as filling their joint rect),
        windows drawn scaled down, the One panel counts and a total.
        """
        W, H = Kit.screen()
        zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        n = bad = hid = 0
        ridden = []
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, [])
            rides = [safe((self.hooks.get(k) or {}).get("riding") or (lambda: False), False) for k in keys]
            if keys and all(rides) and z.px is not None:
                ridden.append(z.px)
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, [])
            shut = [k for k in keys if self.gump_of(k) is None]
            if z.kind == "w" and not keys:
                Kit.say('zone "%s": empty.' % z.id, Kit.HUE_INFO)
            if shut:
                names = ", ".join(self.title_of(k) for k in shut)
                Kit.say('zone "%s": %s.' % (z.id, ("empty (%s not open)" if len(shut) == len(keys) else "%s not open")
                                            % names), Kit.HUE_BAD)
            for key in keys:
                g = self.gump_of(key)
                slot = self.placed.get(key)
                if g is None or slot is None:
                    continue
                if key in self.behind:
                    n += 1
                    hid += 1
                    Kit.say('%s: behind a tab in "%s".' % (self.title_of(key), z.id), Kit.HUE_GOOD)
                    continue
                r = Snap.rect(g)
                if r is None:
                    continue
                n += 1
                want = tuple(slot)
                ok = all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, want))
                for p in ridden:
                    x0, y0 = min(want[0], p[0]), min(want[1], p[1])
                    u = (x0, y0, max(want[0] + want[2], p[0] + p[2]) - x0, max(want[1] + want[3], p[1] + p[3]) - y0)
                    if all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, u)):
                        ok = True
                if not ok:
                    bad += 1
                Kit.say('%s in "%s": %d x %d at %d, %d%s.' % (self.title_of(key), z.id, r[2], r[3], r[0], r[1],
                    "; fills it" if ok else "; its zone is %d x %d at %d, %d" % (want[2], want[3], want[0], want[1])),
                    Kit.HUE_GOOD if ok else Kit.HUE_BAD)
                k, full = self.drawn_at(key, g)
                if k < 0.995 and full is not None:
                    Kit.say('%s is drawn at %d%% in zone "%s"; %d x %d shows it at 100%%.'
                               % (self.title_of(key), int(round(k * 100)), z.id, full[0], full[1]), Kit.HUE_INFO)
        if self.seamless:
            Kit.say("One panel: on; %s without a title row, %s with its title hidden in place, %s left as is." % (
                Kit.count(len(Seam.recs), "window"),
                Kit.count(sum(1 for r in Seam.bare.values() if r["title"]), "window"),
                Kit.count(max(0, n - hid - len(Seam.recs) - sum(1 for r in Seam.bare.values() if r["title"])),
                          "window")), Kit.HUE_INFO)
        if not n:
            Kit.say("no window sits in a zone.", Kit.HUE_INFO)
        else:
            Kit.say("%d of %d windows fill their zone; screen %d x %d (UI scale %.2f)." % (
                n - bad, n, W, H, Kit.render_scale()), Kit.HUE_INFO)

    def drawn_at(self, key, g):
        """Return (scale, full size) a window is drawn at: its own drawn_at hook, else the fill record. A
        scale of 1.0 has no full size.
        """
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

    def _map_zone(self):
        """Return the zone that holds the world map, or None."""
        return self.zone_of("worldmap")

    FREED_VAR = "VirtueAssistant_layout_freed"
    HOMES_VAR = "VirtueAssistant_layout_homes"

    def _freed(self):
        """Return the set of window keys the player freed (saved), reading it on first use."""
        if self.freed is None:
            self.freed = set(k for k in Kit.get_var(self.FREED_VAR, "").split(",") if k.strip())
        return self.freed

    def free_by_you(self, keys):
        """Remember that the player freed these windows, so repair does not put them back in a zone."""
        f = self._freed()
        n = len(f)
        f.update(str(k) for k in keys)
        if len(f) != n:
            Kit.put_var(self.FREED_VAR, ",".join(sorted(f)))

    def unfree(self, key=None):
        """Take one window key (or all when None) off the freed list and save it."""
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
        """Return the {window key: zone id} of where each window last sat, read from its saved variable.

        An empty saved value sets migrating, so the first repair also seats windows of an older save.
        """
        if self.homes is None:
            self.homes = {}
            raw = Kit.get_var(self.HOMES_VAR, "")
            self.migrating = not raw
            for part in raw.split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    if k.strip() and v.strip():
                        self.homes[k.strip()] = v.strip()
        return self.homes

    def _note_homes(self):
        """Record the current zone of every assigned window as its home and save the list, keeping at most
        64 homes.
        """
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
        """Every two seconds, put windows that wandered back into a zone: a window that squats in the world
        map zone, or a known window with a saved home that has no zone now.

        Windows the player freed are left alone. Where no zone fits, the player is told once. Runs on
        the client tick.
        """
        if not self.assign:
            return
        homes = self._homes()
        if not homes:
            self._note_homes()
        mz = self._map_zone()
        squat = [k for k in (self.assign.get(mz, []) if mz else []) if k != "worldmap"]
        freed = self._freed()
        todo = list(squat)
        listed = None
        for key in ("ultima.friend", "ultima.neutral", "ultima.foe", "ultima.combat", "meters", "worldmap"):
            if (key not in self.wins or key in freed or key in squat or self.holds(key)):
                continue
            if listed is None:
                listed = set()
                if self.layout_name:
                    for ks in self.parse_windows(self.window_layout_text(self.layout_name))[1].values():
                        listed.update(ks)
            mod = key.split(".")[0]
            kin = any(k.split(".")[0] == mod for ks in self.assign.values() for k in ks)
            if key in homes or key in listed or (kin and key != "worldmap") or (self.migrating and key != "worldmap"):
                todo.append(key)
        changed = []
        for key in todo:
            if self.gump_of(key) is None:
                continue
            cur = self.zone_of(key)
            home = self._home_for(key, zs, mz)
            if home is None:
                if key not in self.repair_told and key != "worldmap":
                    self.repair_told.add(key)
                    Kit.say("%s has no zone to go back to; drop it on one in Arrange mode."
                               % self.title_of(key), Kit.HUE_INFO)
                if cur is None:
                    continue
            if cur is not None:
                self.assign[cur] = [k for k in self.assign[cur] if k != key]
                if not self.assign[cur]:
                    del self.assign[cur]
            if home is not None:
                self.assign.setdefault(home, []).append(key)
            self._refit(key)
            changed.append((key, home))
        if changed:
            self.save_assign()
            self.dirty = self.fresh = True
            self.page_refresh = True
            for key, home in changed:
                if home is not None:
                    Kit.say('%s put back in zone "%s".' % (self.title_of(key), home), Kit.HUE_GOOD)
            self.free_scrolled()
            HOST.poke()

    def _home_for(self, key, zs, mz):
        """Choose the zone for a window being repaired, or None.

        Order: its last home, if free of other modules' windows; the default layout's zone for it; a
        zone beside one that holds the same module's windows; a zone with the same module's windows; the
        empty zone nearest to the window. The world map only takes an empty zone it was at before.
        """
        wz = [z for z in zs.zones if z.kind == "w" and z.px is not None and z.id != mz]
        if key == "worldmap":
            wz = [z for z in zs.zones if z.kind == "w" and z.px is not None and not self.assign.get(z.id)]
        ids = set(z.id for z in wz)
        mod = key.split(".")[0]

        def kin_only(zid):
            """True when the zone holds only windows of the same module as key."""
            return all(k.split(".")[0] == mod for k in self.assign.get(zid, []) if k != key)

        last = self._homes().get(key)
        if last in ids and kin_only(last):
            return last
        if key == "worldmap":
            return None
        zid = next((zid for zid, keys in self.parse_windows(WINDOWS_DEFAULT)[1].items() if key in keys), None)
        if zid in ids and kin_only(zid):
            return zid
        empty = [z for z in wz if not self.assign.get(z.id)]
        kin = [z for z in wz if z.id in self.assign
               and any(k != key and k.split(".")[0] == mod for k in self.assign[z.id])]
        if kin:
            for kz in kin:
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
            empty.sort(key=lambda z: (z.px[0] + z.px[2] / 2.0 - cx) ** 2 + (z.px[1] + z.px[3] / 2.0 - cy) ** 2)
            return empty[0].id
        return None

    def _refit(self, key):
        """Forget the slot and size told to a window, so the next pass fits it again."""
        self.placed.pop(key, None)
        self.min_seen.pop(key, None)
        rec = self.fitted.get(key)
        if rec is not None and rec.get("kind") == "fit":
            rec.pop("told", None)

    def _key_of(self, g):
        """Return the window key of gump g, or None."""
        key = self.gump_key.get(g)
        if key is None:
            for k in self.wins:
                if self.gump_of(k) is g:
                    return k
        return key

    def _drop_zone(self, r):
        """Return the window zone a dragged window at rect r would land in, or None.

        A zone more than half covered by the rect wins (the largest overlap); otherwise the zone under
        its centre.
        """
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2
        hit = None
        covered = None
        for z in self.frames.zones:
            if z.kind != "w" or z.px is None:
                continue
            x, y, w, h = z.px
            if hit is None and x <= cx < x + w and y <= cy < y + h:
                hit = z
            ow = min(x + w, r[0] + r[2]) - max(x, r[0])
            oh = min(y + h, r[1] + r[3]) - max(y, r[1])
            if (ow > 0 and oh > 0 and ow * oh * 2 > w * h and (covered is None or ow * oh > covered[0])):
                covered = (ow * oh, z)
        if covered is not None:
            hit = covered[1]
        return hit

    def takes(self, g):
        """True when dropping gump g now would put it in a zone: Arrange mode on, a known window, a zone
        under it, and the Alt key not held.
        """
        if not self.loaded or self.frames is None or not self.arrange:
            return False
        if self._key_of(g) is None or safe(Follow.alt_held, False):
            return False
        r = Snap.rect(g)
        return r is not None and self._drop_zone(r) is not None

    def _back(self):
        """Mark the layout dirty and wake the host so a window dropped nowhere snaps back to its slot."""
        self.dirty = True
        HOST.poke()

    def dropped(self, g, key=None, rect=None):
        """Handles a window dropped in Arrange mode: moves it to the zone it was dropped on, at the position
        in the stack that its centre points to, or makes it the shown tab of a tabbed zone. Outside Arrange
        mode it just snaps back to its slot.

        Arguments: g the gump (or key to look it up instead), rect the drop rect when it is not the
        gump's own. A drop on a zone with exactly one open window swaps the two (not in a tabbed zone);
        one that is too small, or that breaks the world map's zone to itself, snaps back and says why.
        Holding Alt leaves the drop alone.
        """
        if not self.loaded or self.frames is None:
            return
        if key is None:
            key = self._key_of(g)
        else:
            g = self.gump_of(key)
            if g is None:
                return
        if key is None:
            return
        if not self.arrange:
            if self.zone_of(key) is not None:
                self.fresh = self.dirty = True
                HOST.poke()
            return
        self.arrange_last = time.time()
        if safe(Follow.alt_held, False):
            return
        r = rect if rect is not None else Snap.rect(g)
        if r is None:
            return
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2
        hit = self._drop_zone(r)
        self.fresh = True
        if self.arrange_hot is not None:
            box = self.arrange_lit.get(self.arrange_hot)
            if box is not None:
                box.IsVisible = False
            self.arrange_hot = None
        for f, l in list(SNAP.links.items()):
            if f is g or l is g:
                SNAP.links.pop(f, None)
        old = self.zone_of(key)
        if hit is None:
            if old is None:
                return
            self._back()
            if not self.back_told:
                self.back_told = True
                Kit.say("%s stays in its zone; drop it on another zone to move it (Settings > Interface frees "
                           "windows)." % self.title_of(key), Kit.HUE_INFO)
            return
        if old == hit.id and len(self.assign.get(old, [])) <= 1:
            self._back()
            return
        if old == hit.id and hit.stack == "t":
            self.tab_pick(hit.id, key)
            self._back()
            return
        mz = self._map_zone()
        others_there = [k for k in self.assign.get(hit.id, []) if k != key]
        lone = len(others_there) == 1 and self.gump_of(others_there[0]) is not None
        if (key != "worldmap" and hit.id == mz and hit.id != old and (old is None or not lone)) \
                or (key == "worldmap" and others_there and (old is None or not lone)):
            self._back()
            Kit.say("TazUO's World Map keeps its zone to itself; drop %s on another zone."
                       % (self.title_of(key) if key != "worldmap" else "it"), Kit.HUE_BAD)
            return
        if old != hit.id and self._too_small(key, hit, g):
            self._back()
            return
        swap = None
        slots_was = dict((k, self.placed.get(k)) for k in self.assign.get(hit.id, []))
        if old is not None:
            others = [k for k in self.assign.get(hit.id, []) if k != key] if old != hit.id else []
            if len(others) == 1 and self.gump_of(others[0]) is not None and hit.stack != "t":
                swap = others[0]
                if self._too_small(swap, self.frames.by_id(old)):
                    self._back()
                    return
            for k in list(self.assign.get(old, [])) + list(self.assign.get(hit.id, [])):
                self._refit(k)
            at = self.assign[old].index(key) if key in self.assign[old] else 0
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if swap is not None:
                self.assign[old].insert(min(at, len(self.assign[old])), swap)
                self.assign[hit.id] = [k for k in self.assign[hit.id] if k != swap]
                self.placed.pop(swap, None)
            if not self.assign[old]:
                del self.assign[old]
        keys = self.assign.setdefault(hit.id, [])
        pos = len(keys)
        if hit.stack == "t":
            self.tabs[hit.id] = key
            self._tabs_save()
        for i, k in enumerate(keys if hit.stack != "t" else ()):
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
        self.unfree(key)
        self.save_assign()
        self.dirty = True
        HOST.poke()

    def _size_of(self, key):
        """Return the natural size of a window, or None."""
        base = self.base.get(key)
        if base is None:
            g = self.gump_of(key)
            r = Snap.rect(g) if g is not None and not isinstance(g, ClientWin) else None
            base = (r[2], r[3]) if r else None
        return base

    def slots_for(self, z, keys):
        """Return (key, slot) for each window of keys as it would be laid out in zone z."""
        if not keys or z is None or z.px is None:
            return []
        return list(zip(keys, self._slots(z, [(k, None, None, None, None, None, False, self._size_of(k) or (100, 100))
                                              for k in keys])))

    def preview_text(self, key, z, keys=None):
        """Returns the preview line shown while dragging window key over zone z.

        A line starting with ! is a refusal (a zone kind that cannot hold it, the world map's zone, too
        small for the body below any tab strip). Otherwise it says the size it would get, with the
        percentage when it would be drawn smaller.
        """
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
        b = self._body(z)
        if mn and (b[2] < mn[0] or b[3] < mn[1]):
            return ("!%s needs %d x %d at least; this zone is %d x %d." % (t, mn[0], mn[1], b[2], b[3]))
        keys = ([k for k in (keys if keys is not None else self.assign.get(z.id, [])) if k != key] + [key])
        slot = None
        for k, sl in self.slots_for(z, keys):
            if k == key:
                slot = sl
        if slot is None:
            slot = z.px
        w, h = max(1, slot[2]), max(1, slot[3])
        base = self._size_of(key)
        shown = ""
        if base and base[0] > 0 and base[1] > 0:
            sc = min(1.0, float(w) / base[0], float(h) / base[1])
            if sc < 0.995:
                shown = " (shown at %d%%)" % int(round(sc * 100))
        return "%s: %d x %d here%s." % (t, w, h, shown)

    def status_text(self):
        """Return the Settings line with the screen size, its shape, the grid step and how many squares it
        holds.
        """
        W, H = Kit.screen()
        step = HOST.grid_size()
        if W <= 0 or H <= 0:
            return "Screen: not known yet"
        return "Screen: %d x %d, %s; grid %d px, %d x %d squares" % (
            W, H, ratio_class(W, H), step, (W + step - 1) // step, (H + step - 1) // step)


class Seam(object):
    """One panel (seamless) mode: strips the frames and title rows of zoned windows so the zones read
    as one panel, and puts them back when it is switched off.

    Class state: recs holds windows cut down to a bare client rect (with what was changed), bare
    holds windows whose title row was hidden, catchers holds the hover strips that bring a title
    back, and the rest are caches for the edge look.
    """
    recs = {}
    bare = {}
    titled_n = {}
    edge = [None]
    catchers = {}
    seen = [None, 0.0]

    @staticmethod
    def pad():
        """Return the gap in pixels the window frame's edge takes, measured from the frame art once and
        cached.
        """
        if Seam.edge[0] is None:
            s = [Kit.pic_size(Kit.WINDOW_BG + i) for i in (1, 3, 5, 7)]
            Seam.edge[0] = min(Kit.MARGIN, max([SEAM_PAD, s[0][1], s[1][0], s[2][0], s[3][1]]) + 1)
        return Seam.edge[0]

    @staticmethod
    def title_of(raw, w):
        """Return the child controls of raw that make up its title row, or an empty list when it has none.

        A title row is recognised by a 30 pixel high control at the frame margin that spans the window
        width.
        """
        M = Kit.MARGIN
        rects = [(c, Kit._raw_rect(c)) for c in Kit._children(raw)]
        if not any(r is not None and abs(r[0] - M) <= 2 and abs(r[1] - M) <= 2 and abs(r[3] - 30) <= 1
                   and r[2] >= w - 2 * M - 6 for c, r in rects):
            return []
        return [c for c, r in rects if r is not None and M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36]

    @staticmethod
    def titled(g):
        """True when gump g has a title row to hide. The answer is cached per gump and child count."""
        if g in Seam.recs:
            return True
        raw = Kit._raw_gump(g)
        r = Kit.rect(g)
        if raw is None or r is None:
            return False
        n = int(raw.Children.Count)
        had = Seam.titled_n.get(g)
        if had is not None and had[0] == n:
            return had[1]
        Kit._prune(Seam.titled_n, 32)
        on = bool(Seam.title_of(raw, r[2]))
        Seam.titled_n[g] = (n, on)
        return on

    @staticmethod
    def strip(g, untitled=False):
        """Hide the frame art of g (and, unless untitled, its title row, which shows again on hover) for
        One panel mode.

        Returns True when g is stripped. The record in bare notes what was hidden so unstrip can put it
        back, and is kept up to date when the window gains new children. A window without frame parts is
        left alone.
        """
        parts = Kit._frame_parts.get(g)
        raw = Kit._raw_gump(g)
        if not parts or raw is None:
            return False
        rec = Seam.bare.get(g)
        n = int(raw.Children.Count)
        if rec is not None and rec["parts"] is parts:
            if rec["n"] != n:
                cur = Kit._children(raw)
                have = set(cur)
                M = Kit.MARGIN
                for p in parts:
                    Kit.set(p, "IsVisible", False)
                rec["title"] = [t for t in rec["title"] if t[0] in have]
                for c in [c for c in cur if c not in rec["kids"]] if rec["band"] else ():
                    r = Kit._raw_rect(c)
                    if r is None or not (M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36):
                        continue
                    v = bool(c.IsVisible)
                    rec["title"].append([c, None, None, v])
                    c.IsVisible = v and rec["open"]
                rec["kids"], rec["n"] = have, len(cur)
            Seam.watch(rec, False)
            return True
        keep = (rec["open"], rec["until"]) if rec is not None else (False, 0.0)
        if rec is not None:
            Seam.unstrip(g)
        r = Kit.rect(g)
        free = r is not None and g not in Seam.recs and not untitled
        title = Seam.title_of(raw, r[2]) if free else []
        frame = set(c for c in map(Kit.client_control, parts) if c is not None)
        title = [[c, None, None, bool(c.IsVisible)] for c in title if c not in frame]
        for p in parts:
            Kit.set(p, "IsVisible", False)
        for t in title:
            t[0].IsVisible = False
        Kit._prune(Seam.bare, 32)
        Seam.bare[g] = {"parts": parts, "n": n, "title": title, "open": keep[0], "until": keep[1], "band": bool(title),
                        "kids": set(Kit._children(raw))}
        for t in title:
            t[0].IsVisible = t[3] and keep[0]
        return True

    @staticmethod
    def unstrip(g):
        """Undo strip: show the frame parts and title row of g again."""
        rec = Seam.bare.pop(g, None)
        if rec is None or not Kit.is_open(g):
            return
        on = Kit._frame_want.get(g, True)
        for p in rec["parts"]:
            Kit.set(p, "IsVisible", on)
        for t in rec["title"]:
            with Kit.quiet:
                t[0].IsVisible = t[3]

    @staticmethod
    def cut(pads):
        """Return how many pixels to cut from the left, top, right and bottom of a window frame given the
        padding it keeps.
        """
        M = Kit.MARGIN
        return M - pads[0], M + 30 + Kit.GAP - pads[1], M - pads[2], M - pads[3]

    @staticmethod
    def clip(slot, pads):
        """Reduce the padding on edges where the slot touches the screen edge, so the cut never goes off
        screen.
        """
        W, H = Kit.screen()
        M = Kit.MARGIN
        if W <= 0 or H <= 0:
            return pads
        return (min(M, max(pads[0], M - slot[0])), pads[1], min(M, max(pads[2], M - (W - slot[0] - slot[2]))),
                min(M, max(pads[3], M - (H - slot[1] - slot[3]))))

    @staticmethod
    def grow(slot, pads):
        """Return the slot grown by the cut, so the window's frame reaches the slot's edges."""
        l, t, r, b = Seam.cut(pads)
        return slot[0] - l, slot[1] - t, slot[2] + l + r, slot[3] + t + b

    @staticmethod
    def can(g, hooks, mini):
        """True when window g can be cut to the bare client rect: not minimised, not a client window, has
        frame parts and a title row, is not scrolled, and the client thread is running.
        """
        return not (mini or isinstance(g, ClientWin) or hooks.get("untitled")) and bool(Kit._frame_parts.get(g)) \
            and g not in Kit._scrolled and Client.on_client_thread() and Seam.titled(g)

    @staticmethod
    def holds(g, slot, pads, grown, r):
        """True when g is already trimmed for exactly this slot and padding, so nothing needs doing.

        When children were added since, they are adopted first; a failure returns False to force a
        retrim.
        """
        rec = Seam.recs.get(g)
        if rec is None or rec["slot"] != tuple(slot) or rec["pads"] != pads or r is None or r[:2] != grown[:2]:
            return False
        try:
            kids = rec["raw"].Children
            n = int(kids.Count)
            if (n != rec["n"] or (n and kids[n - 1] is not rec["last"])) and not Seam.refresh(g, rec):
                return False
            rb = rec["catch"]
            if rb is not None and bool(rb.CanMove) != bool(LAYOUT.arrange):
                rb.CanMove = bool(LAYOUT.arrange)
        except Exception:
            return False
        Seam.watch(rec, True)
        return True

    @staticmethod
    def refresh(g, rec):
        """Take in children added to a trimmed window: hide new frame art, move new title controls out of
        sight.
        """
        cur = Kit._children(rec["raw"])
        have = set(cur)
        if rec["catch"] is not None and rec["catch"] not in have:
            return False
        frame = set(c for c in map(Kit.client_control, Kit._frame_parts.get(g) or ()) if c is not None)
        rec["frame"] = [fv for fv in rec["frame"] if fv[0] in have]
        rec["title"] = [t for t in rec["title"] if t[0] in have]
        new = [c for c in cur if c not in rec["kids"]]
        for c in new:
            if c in frame:
                rec["frame"].append((c, bool(c.IsVisible)))
                c.IsVisible = False
        Seam.adopt(rec, [c for c in new if c not in frame])
        rec["kids"], rec["n"], rec["last"] = have, len(cur), cur[-1] if cur else None
        return True

    @staticmethod
    def adopt(rec, new):
        """Add new children that sit in the title row to the record and move them down out of the trimmed
        area.
        """
        M = Kit.MARGIN
        down = 30 + Kit.GAP
        for c in new:
            r = Kit._raw_rect(c)
            if r is None or not (M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36):
                continue
            rec["title"].append([c, r[0], r[1], bool(c.IsVisible)])
            c.Location = ClientWin.point(r[0], r[1] + down)
            c.IsVisible = rec["open"] and rec["title"][-1][3]

    @staticmethod
    def watch(rec, trimmed):
        """Keep a trimmed window trimmed: hide frame art that reappeared and re-hide or re-place title
        controls the window moved.
        """
        M = Kit.MARGIN
        down = 30 + Kit.GAP
        for c, v in rec.get("frame", ()) if trimmed else ():
            try:
                if c.IsVisible:
                    c.IsVisible = False
            except Exception:
                pass
        for t in rec["title"]:
            c = t[0]
            try:
                r = Kit._raw_rect(c) if trimmed else None
                if r is not None and r[1] < M + 34:
                    t[1], t[2], t[3] = r[0], r[1], bool(c.IsVisible)
                    c.Location = ClientWin.point(r[0], r[1] + down)
                    c.IsVisible = rec["open"] and t[3]
                elif not rec["open"] and bool(c.IsVisible):
                    t[3] = True
                    c.IsVisible = False
            except Exception:
                pass

    @staticmethod
    def trim(g, slot, pads):
        """Cut window g to the bare client rect inside slot: hide its frame and title row and cover it with
        a catcher box.

        The catcher is a nearly transparent box at the bottom of the draw order that takes mouse input
        and moves the window in Arrange mode. A record in recs stores what was changed so undo can
        restore it. Returns True.
        """
        raw = Kit._raw_gump(g)
        if raw is None:
            return False
        M = Kit.MARGIN
        down = 30 + Kit.GAP
        frame = set(c for c in map(Kit.client_control, Kit._frame_parts.get(g) or ()) if c is not None)
        hid, title = [], []
        for c in Kit._children(raw):
            r = Kit._raw_rect(c)
            if r is None:
                continue
            vis = bool(c.IsVisible)
            if c in frame:
                c.IsVisible = False
                hid.append((c, vis))
            elif M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36:
                c.IsVisible = False
                c.Location = ClientWin.point(r[0], r[1] + down)
                title.append([c, r[0], r[1], vis])
        l, t = Seam.cut(pads)[:2]
        box = G.CreateGumpColorBox(0.01, "#000000")
        box.SetRect(l, t, slot[2], slot[3])
        g.Add(box)
        Kit.flush()
        rb = Kit.client_control(box)
        if rb is not None and raw.Children.Remove(rb):
            raw.Children.Insert(0, rb)
            rb.AcceptMouseInput = True
            rb.CanMove = bool(LAYOUT.arrange)
            if len(Seam.catchers) > 64:
                for k in [k for k in Seam.catchers if k.IsDisposed]:
                    Seam.catchers.pop(k, None)
            Seam.catchers[rb] = g
        was = bool(raw.AcceptMouseInput)
        Kit._prune(Seam.recs, 32)
        if rb is not None and rb in Seam.catchers:
            raw.AcceptMouseInput = False
        cur = Kit._children(raw)
        n = len(cur)
        Seam.recs[g] = {"slot": tuple(slot), "pads": pads, "raw": raw, "n": n, "frame": hid, "title": title,
                        "open": False, "until": 0.0, "box": box, "catch": rb, "mouse": was,
                        "last": cur[-1] if n else None, "kids": set(cur)}
        return True

    @staticmethod
    def undo(g):
        """Undo trim: restore location and visibility of the hidden controls, remove the catcher and give
        the mouse back.
        """
        rec = Seam.recs.pop(g, None)
        if rec is None or not Kit.is_open(g):
            return False
        Seam.bare.pop(g, None)
        on = Kit._frame_want.get(g)
        for c, x, y, vis in [(c, None, None, v if on is None else on) for c, v in rec["frame"]] + rec["title"]:
            with Kit.quiet:
                if x is not None:
                    c.Location = ClientWin.point(x, y)
                c.IsVisible = vis
        rec["raw"].AcceptMouseInput = rec["mouse"]
        Seam.catchers.pop(rec.get("catch"), None)
        Kit.dispose(rec["box"])
        return True

    @staticmethod
    def undo_all():
        """Undo every trim and strip."""
        for g in list(Seam.recs):
            Seam.undo(g)
        for g in list(Seam.bare):
            Seam.unstrip(g)

    @staticmethod
    def hover(all_on=False):
        """Show the title row of trimmed windows while the mouse is over the top of their slot, and hide it
        again after REVEAL_HOLD.

        all_on shows every title (used while the player holds the key for it). Cheap exit when the mouse
        and counts are unchanged for a quarter of a second.
        """
        if not (Seam.recs or Seam.bare):
            return
        m = Kit.mouse_pos()
        now = time.time()
        sig = (m, all_on, len(Seam.recs), len(Seam.bare))
        if sig == Seam.seen[0] and now < Seam.seen[1]:
            return
        Seam.seen[0], Seam.seen[1] = sig, now + 0.25
        for d, trimmed in ((Seam.recs, True), (Seam.bare, False)):
            for g, rec in list(d.items()):
                if not rec["title"]:
                    continue
                if not Kit.is_open(g):
                    d.pop(g, None)
                    continue
                r = rec["slot"] if trimmed else Kit.rect(g)
                if r is None:
                    continue
                x, y, w, h = r
                top = rec["pads"][1] if trimmed else Kit.MARGIN + 4
                band = 30 + top if rec["open"] else REVEAL_H
                if all_on or (m is not None and x <= m[0] < x + w and y <= m[1] < y + band):
                    rec["until"] = now + REVEAL_HOLD
                want = now < rec["until"]
                if want:
                    Seam.seen[1] = min(Seam.seen[1], rec["until"])
                if want != rec["open"]:
                    rec["open"] = want
                    for t in rec["title"]:
                        try:
                            t[0].IsVisible = want and t[3]
                        except Exception:
                            pass


class Fade(object):
    """Fades idle windows. After a window has had no mouse over it and nothing changed in it for the
    chosen time, every control in it is drawn at a lower alpha; the mouse over it, a change in it or a
    wake call brings it back.

    Settings are the saved fade, fade_to, fade_after and fade_all preferences (Settings > Interface,
    LOOK). tick() runs from the host's main loop while fading is on. The Virtue Assistant window and the
    alerts never fade, nor does a window whose hooks say fade is False; the Action Bar and the unit
    frames fade only when fade_all is set. Nothing is touched in Arrange mode.
    """
    EVERY = 0.2
    HIT_EVERY = 1.0
    PRUNE_EVERY = 2.0
    RETRY = 1.0
    NEAR = 0.003
    CAP = 64
    TO, AFTER = (20, 90), (2, 30)
    KEYS = ("fade", "fade_to", "fade_after", "fade_all")
    ALL_ONLY = ("actionbar", "unitframes")

    def __init__(self):
        """Sets up empty state with fading off."""
        self.on = self.all = False
        self.to, self.after = 0.4, 6.0
        self.base = {}
        self.dim = {}
        self.gk = {}
        self.woke = {}
        self.under = set()
        self.mouse = self.sig = None
        self.next = self.hit_at = self.prune_at = 0.0
        self.kids = {}
        self.look_at = 0.0

    def load(self, host):
        """Reads the saved fade settings from the host's preferences."""
        self.opts(host.pref_int("fade", 0) == 1, host.pref_int("fade_to", 40), host.pref_int("fade_after", 6),
                  host.pref_int("fade_all", 0) == 1)

    def opts(self, on, to, after, all_):
        """Applies the settings: on, the faded alpha to as a percentage (TO limits), the idle time after in
        seconds (AFTER limits) and whether the Action Bar and unit frames fade too. Windows that are
        dimmed are restored when fading goes off or the level or scope changes.
        """
        to = max(self.TO[0], min(self.TO[1], int(to))) / 100.0
        after = float(max(self.AFTER[0], min(self.AFTER[1], int(after))))
        on, all_ = bool(on), bool(all_)
        if self.on and (not on or to != self.to or all_ != self.all):
            self.reset()
        self.on, self.to, self.after, self.all = on, to, after, all_
        if not on:
            self.base, self.woke = {}, {}

    def set(self, new):
        """Takes new settings from a dict with the KEYS (fade, fade_to, fade_after, fade_all), applies them,
        writes the checked values back to the preferences (as strings) and saves them.
        """
        p = HOST.prefs
        for k in self.KEYS:
            try:
                p[k] = str(int(new[k]))
            except Exception:
                pass
        self.load(HOST)
        p["fade"], p["fade_all"] = ("1" if self.on else "0"), ("1" if self.all else "0")
        p["fade_to"], p["fade_after"] = str(int(round(self.to * 100))), str(int(self.after))
        HOST.save_prefs()

    def reset(self):
        """Restores every dimmed window to its own alpha and forgets what was seen."""
        for k, gs in list(self.dim.items()):
            for g in gs:
                if Kit.is_open(g):
                    self._walk(g, False)
        self.dim, self.gk, self.under, self.mouse, self.sig, self.kids = {}, {}, set(), None, None, {}

    def wake(self, key):
        """Marks window key, its parts and the windows it owns as just used (a window that redraws calls this),
        so they come back at once.
        """
        now = time.time()
        key = str(key)
        self.woke[key] = now
        pre = key + "."
        for k in list(LAYOUT.wins) + list(Kit._wins):
            if k.startswith(pre) or LAYOUT.owner.get(k, (None,))[0] == key:
                self.woke[k] = now

    def _may(self, k, g, skip):
        """Returns True when window k (gump g) may fade: not skipped, not hidden behind a tab, not a lone
        module settings window, not opted out by its hooks and not an Action Bar or unit frames window
        unless fade_all is set.
        """
        if g in skip or g in Kit._behind or k in LAYOUT.behind or k.endswith("_alone"):
            return False
        if (LAYOUT.hooks.get(k) or {}).get("fade") is False:
            return False
        return self.all or not any(k == p or k.startswith(p + ".") for p in self.ALL_ONLY)

    def _units(self):
        """Returns {window key: [gumps]} of every window that may fade: those the windows helper registered,
        then zoned windows (not client ones), with the tab strip of a zone added to the shown window of that
        zone so both fade together. The Virtue Assistant window, the alerts and the alert history are
        left out.
        """
        c = HOST.config
        own = (c.g if c is not None else None, ALERTS.g, HOST.alert_log.g)
        skip = set(g for g in own if g is not None)
        out = {}
        seen = set()
        no = set()
        for k, w in list(Kit._wins.items()):
            g = w.win.get(w.gkey)
            if not w.fade:
                no.add(k)
            elif Kit.is_open(g) and self._may(k, g, skip):
                out[k] = [g]
                seen.add(g)
        for k in list(LAYOUT.wins):
            if k in out or k in no:
                continue
            g = LAYOUT.gump_of(k)
            if g is not None and g not in seen and not isinstance(g, ClientWin) and self._may(k, g, skip):
                out[k] = [g]
                seen.add(g)
        for zid, rec in list(LAYOUT.strips.items()):
            sg = rec.get("g")
            if not Kit.is_open(sg):
                continue
            for k in LAYOUT.assign.get(zid) or ():
                if k in out and k not in LAYOUT.behind:
                    out[k].append(sg)
                    break
        return out

    @staticmethod
    def _kids(g):
        """Returns how many controls a gump has (its children and their children), or -1 if that cannot be
        read. A change in the count shows the window redrew itself.
        """
        try:
            kids = Kit.client_control(g).Children
            n = 0
            for i in range(int(kids.Count)):
                n += 1 + int(kids[i].Children.Count)
            return n
        except Exception:
            return -1

    @staticmethod
    def _over(g, m):
        """Returns True when mouse position m is inside gump g."""
        r = Kit.rect(g)
        return r is not None and r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]

    def tick(self, now):
        """Called from the host's main loop with the time now. At most every EVERY seconds: resets when the
        layout changed shape, tracks which windows the mouse is over (the hit test runs at most every
        HIT_EVERY seconds when the mouse is still), and dims windows that have been quiet for the idle time
        and restores those that woke. A dimmed window whose number of controls changed is dimmed again so
        the new controls fade too.
        """
        if now < self.next:
            return
        self.next = now + self.EVERY
        L = LAYOUT
        # Anything in this signature changing (layout, look, tabs, Arrange) puts every window back before
        # fading starts again.
        sig = (L.frames_name, L.layout_name, L.arrange, L.enabled, L.seamless, frozenset(L.behind), Kit.look())
        if sig != self.sig:
            if self.sig is not None:
                self.reset()
            self.sig = sig
        if L.arrange:
            return
        m = Kit.mouse_pos()
        units = self._units()
        woke = self.woke
        for k, gs in units.items():
            if self.gk.get(k) is not gs[0]:
                self.gk[k] = gs[0]
                woke[k] = max(woke.get(k, 0.0), now)
        if m != self.mouse or now >= self.hit_at:
            self.mouse, self.hit_at = m, now + self.HIT_EVERY
            self.under = set(k for k, gs in units.items() if m is not None and any(self._over(g, m) for g in gs))
        for k in self.under:
            if k in units:
                woke[k] = now
        # A window is due to fade when it has not been woken for the idle time.
        want = set(k for k in units if now - woke.get(k, now) >= self.after)
        for k, gs in list(self.dim.items()):
            if k not in want or units.get(k) != gs:
                self.dim.pop(k, None)
                for g in gs:
                    if Kit.is_open(g):
                        self._walk(g, False)
        if now >= self.look_at:
            self.look_at = now + self.RETRY
            for k, gs in list(self.dim.items()):
                for g in gs:
                    if not Kit.is_open(g):
                        continue
                    n = self._kids(g)
                    if n != self.kids.get(g, n):
                        self.kids[g] = n
                        self._walk(g, True)
        for k in want:
            if k not in self.dim:
                if all([self._walk(g, True) for g in units[k]]):
                    self.dim[k] = list(units[k])
                    for g in units[k]:
                        self.kids[g] = self._kids(g)
                else:
                    # A window that could not be dimmed all at once is tried again after RETRY seconds.
                    woke[k] = now - self.after + self.RETRY
        if now >= self.prune_at:
            self.prune_at = now + self.PRUNE_EVERY
            self._prune(units, now)

    def _prune(self, units, now):
        """Drops records of closed windows and windows no longer listed so the tables stay small."""
        self.base = dict((g, r) for g, r in self.base.items() if Kit.is_open(g))
        self.kids = dict((g, n) for g, n in self.kids.items() if g in self.base)
        self.gk = dict((k, g) for k, g in self.gk.items() if k in units)
        self.woke = dict((k, t) for k, t in self.woke.items() if k in units or now - t < self.after)

    def _walk(self, g, on):
        """Dims (on) or restores (off) every control of gump g through Kit.walk. Returns False when it could
        not (nothing to restore, or too many gumps recorded), True otherwise.

        base[g] holds, per control, (the control's own alpha, the alpha set here). A control whose alpha
        was changed by something else since is left at that value instead of being restored.
        """
        old = self.base.get(g)
        if old is None:
            if not on:
                return False
            if len(self.base) >= self.CAP:
                self.base = dict((b, r) for b, r in self.base.items() if Kit.is_open(b))
                if len(self.base) >= self.CAP:
                    return False
            old = {}
        new = {}
        f = self.to
        near = self.NEAR

        def one(c):
            """Dims or restores one control c; controls that cannot be read are skipped."""
            try:
                a = float(c.Alpha)
                r = old.get(c)
                if on:
                    b = r[0] if r is not None and abs(a - r[1]) <= near else a
                    v = b * f
                elif r is None:
                    return
                elif abs(a - r[1]) > near:
                    new[c] = (a, a)
                    return
                else:
                    b = v = r[0]
                c.Alpha = v
                new[c] = (b, v)
            except Exception:
                pass

        ok = Kit.walk(g, one)
        self.base[g] = new
        return ok


SNAP = Snap()
ALERTS = Alerts()
GUARD = Guard()
LAYOUT = Layout()
FADE = Fade()
HOST = Host()
MODULE_FILES = (("actionbar", "Action Bar", "ActionBarModule.py"), ("hud", "Character HUD", "CharacterHudModule.py"),
    ("interface", "Interface", "InterfaceModule.py"), ("inventory", "Inventory", "InventoryModule.py"),
    ("grimoire", "Grimoire", "GrimoireModule.py"), ("worldmap", "World Map", "WorldMapModule.py"),
    ("ultima", "Ultima Tracker", "UltimaTrackerModule.py"),
    ("social", "Social", "SocialModule.py"), ("prices", "Reagent Prices", "ReagentPricesModule.py"),
    ("skills", "Skills", "SkillsModule.py"),
    ("butler", "Property Butler", "PropertyButlerModule.py"), ("meters", "Meters", "MetersModule.py"),
    ("mongotchi", "Mongotchi", "MongotchiModule.py"),)
RETIRED_KEYS = ("autodoors",)


def module_folders():
    """Return the folders that hold module files: every folder named VirtueAssistant...Modules beside
    the script, in its parent, or under the client's LegionScripts folder. The folder named
    MODULE_DIR comes first.
    """
    places = []
    base = str(API.ScriptPath or "").rstrip("/\\")
    if base:
        if os.path.isfile(base):
            base = os.path.dirname(base)
        places += [base, os.path.dirname(base)]
    with Kit.quiet:
        import System
        root = str(System.AppDomain.CurrentDomain.BaseDirectory).rstrip("/\\")
        places += [os.path.join(root, "LegionScripts"), root]
    found = {}
    for p in places:
        if not p:
            continue
        for n in (safe(lambda: os.listdir(p), []) or []):
            if n in found or not (n.startswith("VirtueAssistant") and n.endswith("Modules")):
                continue
            d = os.path.join(p, n)
            if os.path.isdir(d):
                found[n] = d
    names = ([MODULE_DIR] if MODULE_DIR in found else []) + sorted(n for n in found if n != MODULE_DIR)
    return [found[n] for n in names]


def _read_text(path):
    """Return the text of a file, with a .NET fallback when Python cannot open it.

    The bytes are read through .NET and decoded as UTF-8; text that does not decode cleanly goes
    through Python's own reader instead. Line ends are returned as newlines.
    """
    try:
        import System
        raw = System.IO.File.ReadAllBytes(path)
        text = System.Text.Encoding.UTF8.GetString(raw)
        if len(text) != raw.Length or "\ufffd" in text:
            raise ValueError(path)
    except Exception:
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception:
            import System
            return str(System.IO.File.ReadAllText(path))
    return text.replace("\r\n", "\n").replace("\r", "\n") if "\r" in text else text


class _Reg(object):
    """Stand-in for HOST.add that only records the registration arguments of a module file, so they can
    be read without running the module.
    """
    ok = False

    def take(self, key, title, desc, factory=None, interval=None, default_on=False,
             category=None, parts=(), aliases=()):
        """Record the arguments of a HOST.add call and mark the registration valid."""
        self.key, self.title, self.desc = str(key), str(title), str(desc)
        self.interval = interval if isinstance(interval, (int, float)) else None
        self.default_on = bool(default_on)
        self.category = category
        self.parts = tuple(tuple(p) for p in (parts or ()))
        self.aliases = tuple(aliases or ())
        self.ok = True


def _balanced(text, start):
    """Return the text between the bracket at start and its matching close bracket, or None.

    Quotes and comments are skipped so brackets inside them do not count.
    """
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
    """Read the HOST.add registration out of a module file's text without running it. Returns a _Reg or
    None.

    The last HOST.add call is found, its arguments are evaluated with no builtins and only numeric
    constants of the mother script in scope. This lets a module that has a run interval be added
    lazily, loaded only when switched on.
    """
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
    reg = _Reg()
    ns["_reg"] = reg.take
    try:
        eval("_reg(" + args + ")", {"__builtins__": {}}, ns)
    except Exception:
        return None
    return reg if reg.ok else None


def load_modules():
    """Finds the module files (*Module.py) beside the mother script and loads each into this script's
    namespace.

    Modules load in the order of MODULE_FILES, then any others by name. A retired module, or one now
    merged into another, is skipped with a note. A module with an interval is registered lazily from
    its registration; its text is kept in HOST.texts (up to 64 files) so the compile-ahead and the
    load need not read it again. Any other module is compiled and run here. A module that fails to
    load is told, and a stub is added so its name stays in the list. Every module added from the
    shipped module folder is marked shipped, which is what share codes check.
    """
    folders = module_folders()
    if not folders:
        Kit.say("no %s folder beside this script, so no modules loaded." % MODULE_DIR, Kit.HUE_BAD)
        return
    order = dict((f, i) for i, (_, _, f) in enumerate(MODULE_FILES))
    entries, taken = [], set()
    for d in folders:
        for n in sorted(n for n in safe(lambda: os.listdir(d), []) or [] if n.endswith("Module.py")):
            if n not in taken:
                taken.add(n)
                entries.append((d, n))
    entries.sort(key=lambda e: order.get(e[1], len(order)))
    titles = dict((f, (k, t)) for k, t, f in MODULE_FILES)
    for where, name in entries:
        path = os.path.join(where, name)
        ship = os.path.basename(where) == MODULE_DIR
        n0 = len(HOST.slots)
        if not os.path.isfile(path):
            continue
        m = None
        try:
            text = _read_text(path)
            m = read_registration(text)
            if m is not None and m.key in RETIRED_KEYS:
                Kit.say("skipped %s (retired; the file can be deleted)." % name, Kit.HUE_INFO)
                continue
            if m is not None and m.key in HOST.old_map and HOST.old_map[m.key][0] != m.key:
                mk, pk = HOST.old_map[m.key]
                home = dict.get(HOST.by_key, mk)
                Kit.say("skipped %s (now part of %s; the file can be deleted)." % (
                    name, home.title if home else mk), Kit.HUE_INFO)
                continue
            if m is not None and dict.__contains__(HOST.by_key, m.key):
                API.SysMsg(HOST.TWICE % (APP_NAME, m.title, m.key), Kit.HUE_BAD)
                continue
            if m is not None and m.interval is not None:
                HOST.add_lazy(m.key, m.title, m.desc, path, m.interval, m.default_on, m.category, m.parts, m.aliases)
                if len(HOST.texts) < 64:
                    # Read once here for the registration; kept for the later load.
                    HOST.texts[path] = text
                continue
            exec(HOST.compiled(text, path), globals())
        except Exception as ex:
            line = getattr(ex, "lineno", None)
            if line:
                msg = "%s (%s line %s)" % (getattr(ex, "msg", None) or ex, name, line)
            else:
                msg = "%s%s" % (ex, _error_where())
            Kit.say("couldn't load %s (%s)." % (name, msg), Kit.HUE_BAD)
            kt = (m.key, m.title) if m is not None else titles.get(name)
            if kt is not None and not dict.__contains__(HOST.by_key, kt[0]):
                key, title = kt
                s = HOST.add(key, title, "", lambda: None, 0.1)
                s.api, s.broken = None, msg
        finally:
            for s in HOST.slots[n0:]:
                s.shipped = ship


def _module_sysstats():
    """The System Stats module, built in the mother script: a small button and window showing ping,
    frames per second, frame time, memory, network traffic and packets, and the busiest parts of
    Virtue Assistant (as many rows as the window's height allows).

    The window can be resized and the size is saved. Returns the start, tick and stop hooks the host
    runs, plus a settings page (Show start-up times and Don't warn me about TazUO settings); ticks on
    the client thread. Saves its positions, size, minimised state and open state under the SystemStats
    keys, and its two tick boxes as the main settings startup and tz_quiet.
    """
    KEY = "sysstats"
    TITLE = "System Stats"
    POS_KEY, MIN_KEY, BTN_KEY, OPEN_KEY = ("SystemStats_pos", "SystemStats_min", "SystemStats_btn", "SystemStats_open")
    SIZE_KEY = "SystemStats_size"
    W, W_MAX, MINI_W, MINI_H = 300, 600, 240, 46
    TRAY_ICON = 0x1F2D
    EVERY, CLOSED_EVERY, RESIZE_SETTLE, SOCK_EVERY, BTN = 0.3, 2.0, 0.35, 1.0, 46
    ROWS = ("Ping", "FPS", "Frame", "Memory", "In", "Out", "Packets")
    TOP_MIN, TOP_MAX, TOP_EVERY, TOP_TITLE = 5, 12, 1.0, "BUSIEST PARTS  (share, ms)"
    VAL_W, VAL_WORST = 110, "100.0%, 99999 ms"
    TOP_KEYS = tuple(("top_name%d" % i, "top_val%d" % i) for i in range(TOP_MAX))
    M = Kit.MARGIN
    YB = M + 30 + Kit.GAP
    HB = len(ROWS) * 20 + 4
    Y2 = YB + HB + Kit.GAP
    FIXED_H = Y2 + 26 + M
    settings = {"startup": False, "tz_quiet": False}
    st = {"shutting": False, "minimized": False, "docked": False, "open": False, "queue": [],
          "next": 0.0, "vals": {}, "tip": None, "top_next": 0.0, "top": (), "size": None, "drawn": None,
          "resize_at": 0.0, "preview": False, "rows": TOP_MIN, "name_w": 100, "sock": (0.0, None), "gc": None,
          "ping": None}
    win = {"g": None, "c": {}, "store": ({}, {})}
    btn = {"g": None, "b": None, "lbl": None, "store": ({}, {})}
    queue = Kit.queuer(st)

    def load_settings():
        """Read the main settings startup and tz_quiet into the settings dict."""
        settings.update([(k, HOST.pref_int(k, 0) == 1) for k in list(settings)])

    def save_settings():
        """Write both tick boxes to the main settings (1 or 0) and save them."""
        HOST.prefs.update([(k, "1" if v else "0") for k, v in settings.items()])
        HOST.save_prefs()

    def own_size(w, h):
        """Returns the (width, height) the window may have for a requested w by h: the width held between W
        and W_MAX and the height rounded to a whole number of busiest-parts rows.
        """
        n = max(TOP_MIN, min(TOP_MAX, (int(h) - FIXED_H + 10) // 20))
        return max(W, min(W_MAX, int(w))), FIXED_H + n * 20

    def load_size():
        """Returns the saved window size (own_size applied to it), or the default size when none is saved."""
        try:
            w, h = [int(p) for p in Kit.get_var(SIZE_KEY, "").split(",")[:2]]
        except ValueError:
            return own_size(W, 0)
        return own_size(w, h)

    def busiest(now):
        """Return the five busiest running parts as ((fitted name, text), ...), busiest first.

        Each text reads percent of a second spent, then the slowest tick in ms. A module with parts is
        listed by its running parts, one without by itself. now is the time of the reading.
        """
        rows = []
        for s in HOST.slots:
            if not s.running:
                continue
            if s.parts:
                pl = s.part_load
                # busy_share is milliseconds per second; dividing by 10 when printing makes it a percentage.
                rows.extend((Host.busy_share(pl[p[0]], now), pl[p[0]][2], p[1]) for p in s.parts
                            if p[0] in s.parts_running and p[0] in pl)
            else:
                rows.append((Host.busy_share(s.load, now), s.load[2], s.title))
        rows.sort(key=lambda r: -r[0])
        nw = st["name_w"]
        return tuple((Kit.fit(t, nw), "%.1f%%, %d ms" % (b / 10.0, min(w, 99999))) for b, w, t in rows[:st["rows"]])

    def net_stats(now):
        """Returns the client's network statistics object, looked up again at most once every SOCK_EVERY
        seconds. now is the current time. None when the client does not expose it.
        """
        at, stats = st["sock"]
        if stats is None or not 0 <= now - at <= SOCK_EVERY:
            stats = Tz.get(Tz.get(None, "Socket", Tz.T("ClassicUO.Network.AsyncNetClient")), "Statistics")
            st["sock"] = (now, stats)
        return stats

    def read(now):
        """Read ping, frame rate, network rates, packet counts and memory from the client. Returns {row
        name: text}.
        """
        v = {}
        with Kit.quiet:
            fps = int(Tz.get(None, "CurrentRefreshRate", Tz.T("ClassicUO.CUOEnviroment")))
            v["FPS"] = str(fps)
            v["Frame"] = "%.1f ms" % (1000.0 / fps) if fps > 0 else "-"
        with Kit.quiet:
            stats = net_stats(now)
            src = str(Typing._get(stats, "CurrentPingSource", default="") or "")
            v["Ping"] = "off" if src.endswith("Disabled") else "%d ms" % int(Tz.get(stats, "Ping"))
            v["In"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesReceived")) / 1024.0)
            v["Out"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesSent")) / 1024.0)
            v["Packets"] = "%d in, %d out" % (int(Tz.get(stats, "TotalPacketsReceived")),
                                              int(Tz.get(stats, "TotalPacketsSent")))
        with Kit.quiet:
            if st["gc"] is None:
                import System
                st["gc"] = System.GC.GetTotalMemory
            v["Memory"] = "%d MB" % (int(st["gc"](False)) // (1024 * 1024))
        return v

    def show_ping(text):
        """Shows the ping text on the face of the round button, dropping the ms unit when it does not fit.
        Does nothing when the text has not changed.
        """
        lbl = btn["lbl"]
        if lbl is None or text == st["ping"]:
            return
        st["ping"] = text
        if Kit.text_w(text) > BTN - 6:
            text = Kit.fit(text.replace(" ms", ""), BTN - 6)
        Kit.set_text(lbl, text)
        lbl.SetPos(max(3, (BTN - Kit.text_w(text)) // 2), (BTN - 16) // 2)

    def build_button():
        """Build the small round button that opens and closes the window; its tip shows the current
        figures.
        """
        x, y = Kit.load_pos(BTN_KEY, (8, 200), (BTN, BTN))
        store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, BTN, BTN, corners=False)
        st["tip"] = st["ping"] = None
        lbl = Kit.inert(Kit.add_label(g, "", 3, (BTN - 16) // 2, Kit.HUE_TEXT))
        b = Kit.catcher(g, 0, 0, BTN, BTN, queue("toggle"), "Click to open or close System Stats; drag to move",
                        movable=True)
        Kit.show_window(g, x, y, BTN, BTN, None, False, None, lambda: Kit.save_pos(BTN_KEY, g), btn,
                        {"g": g, "b": b, "lbl": lbl, "store": store})
        show_ping(st["vals"].get("Ping", "-"))

    def build_window():
        """Builds the window with one row per figure and the busiest-parts section (its row count follows
        the saved size), or just its title when minimised; then fills the values.
        """
        held = HOST.layout_holds(KEY)
        st["resize_at"], st["preview"] = 0.0, False
        if st["size"] is None:
            st["size"] = load_size()
        ww, h = st["size"]
        n = (h - FIXED_H) // 20
        vw = max(VAL_W, Kit.text_w(VAL_WORST) + 4)
        st["rows"], st["name_w"] = n, ww - 2 * M - vw - 28
        rs = None if held else (W, FIXED_H + TOP_MIN * 20, on_resized)
        g, store, c = wnd.begin(ww, h, resize=rs)
        if not st["minimized"]:
            wnd.frame(g, mouse=rs is None)
            Kit.add_section(g, M, YB, ww - 2 * M, HB)
            st["top_next"] = time.time() + TOP_EVERY
            st["top"] = busiest(time.time())
            for i, name in enumerate(ROWS):
                Kit.add_label(g, name + ":", M + 10, YB + 6 + i * 20, Kit.HUE_INFO)
                c[name] = Kit.add_label(g, "", M + 90, YB + 6 + i * 20, Kit.HUE_TEXT)
            Kit.add_section(g, M, Y2, ww - 2 * M, h - Y2 - M, Kit.fit(TOP_TITLE, ww - 2 * M - 16))
            for i, (kn, kv) in enumerate(TOP_KEYS[:n]):
                c[kn] = Kit.add_label(g, "", M + 10, Y2 + 26 + i * 20, Kit.HUE_INFO)
                c[kv] = Kit.add_label(g, "", ww - M - 10 - vw, Y2 + 26 + i * 20, Kit.HUE_TEXT)
        wnd.end(g)
        st["drawn"] = None if st["minimized"] else (ww, h)
        refresh()

    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, default=(70, 200), mini=(MINI_W, MINI_H),
                     icon=TRAY_ICON)

    def refresh():
        """Write the latest values into the window's labels (one status line when minimised), then the
        busiest-parts rows, blank where there are fewer than five.
        """
        v = st["vals"]
        c = win["c"]
        if "status" in c:
            Kit.set_text(c["status"], "%s: %s, %s FPS" % (TITLE, v.get("Ping", "-"), v.get("FPS", "-")))
            return
        for name in ROWS:
            lbl = c.get(name)
            if lbl is not None:
                Kit.set_text(lbl, v.get(name, "-"))
        top = st["top"]
        for i, (kn, kv) in enumerate(TOP_KEYS):
            if kn not in c:
                break
            row = top[i] if i < len(top) else ("", "")
            Kit.set_text(c[kn], row[0])
            Kit.set_text(c[kv], row[1])

    def on_resized(*args):
        """Resize event of the window: remembers when it happened and, when the size differs from what is
        drawn, dims the window as a preview until the resize settles.
        """
        st["resize_at"] = time.time()
        g = win["g"]
        if st["preview"] or st["minimized"] or not Kit.is_open(g):
            return
        if (int(g.GetWidth()), int(g.GetHeight())) != st["drawn"]:
            st["preview"] = True
            g.SetAlpha(0.55)

    def apply_resize():
        """Applies a settled resize: takes the new size (cut to the screen height), saves it and redraws the
        window with as many busiest-parts rows as fit. A window held by a zone, or one whose size did not
        really change, is only made opaque again.
        """
        g = win["g"]
        st["preview"] = False
        if not Kit.is_open(g) or st["minimized"]:
            return
        if HOST.layout_holds(KEY):
            g.SetAlpha(0)
            return
        gw, gh = int(g.GetWidth()), int(g.GetHeight())
        drawn = st["drawn"] or (0, 0)
        if abs(gw - drawn[0]) <= 2 and abs(gh - drawn[1]) <= 2:
            g.SetAlpha(0)
            return
        sh = Kit.screen()[1]
        size = own_size(gw, min(gh, sh) if sh > 0 else gh)
        st["size"] = size
        Kit.put_var(SIZE_KEY, "%d,%d" % size)
        build_window()

    def page_table(w):
        """Return the settings page table: START-UP (Show start-up times) and SHARD RULES (the TazUO warning switch).

        Reads the main settings first, so the page shows the saved choice even while the module is off and
        its start never ran. w is the page width, which this table does not need.
        """
        load_settings()
        return (("START-UP", (("check", "startup", "Show start-up times",
                               "After loading, list in the journal how long each step took"),)),
                ("SHARD RULES", (("check", "tz_quiet", "Don't warn me about TazUO settings",
                                  "No journal line when a TazUO setting breaks this shard's rules"),)))

    cfg = Kit.Page(settings, page_table, save_settings)

    def open_window():
        """Open the window and dock it."""
        st["open"] = True
        st["next"] = 0.0
        build_window()
        wnd.dock()

    def close_window():
        """Close the window, take it off the dock, forget the busiest list and save that it is closed."""
        st["open"] = False
        st["top"] = ()
        HOST.dock_remove(KEY)
        wnd.close()
        Kit.put_var(OPEN_KEY, "0")

    def _start():
        """Module start: load saved settings and state, build the button and open the window when it was open
        or a zone holds it.
        """
        load_settings()
        st.update({"shutting": False, "docked": False, "queue": [], "next": 0.0, "top_next": 0.0, "size": None,
                   "resize_at": 0.0, "preview": False, "sock": (0.0, None), "minimized": Kit.load_min(MIN_KEY)
                   or HOST.dock_wanted(KEY), "open": Kit.get_var(OPEN_KEY, "0") == "1"})
        build_button()
        if st["open"] or HOST.layout_holds(KEY):
            open_window()

    def _tick():
        """Module tick: runs queued clicks, applies a settled resize, then reads and shows the figures about
        three times a second.

        The figures are refreshed only when the window is shown; the button tip is rewritten when it
        changed. The busiest parts are collected once a second, only while the window is open and not
        minimised.
        """
        now = time.time()
        while st["queue"]:
            action = st["queue"].pop(0)
            if action == "toggle":
                if Kit.just_dragged(btn["g"]):
                    continue
                if st["open"] and not HOST.layout_holds(KEY):
                    close_window()
                elif not st["open"]:
                    Kit.put_var(OPEN_KEY, "1")
                    st["minimized"] = st["docked"] = False
                    open_window()
            elif action == "redraw":
                if st["open"]:
                    build_window()
            else:
                Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY)
        if st["open"] and Kit.was_clicked(win["store"], "close"):
            close_window()
        if st["resize_at"] and now - st["resize_at"] >= RESIZE_SETTLE and not (SNAP.drag or SNAP.pressed() is True):
            st["resize_at"] = 0.0
            apply_resize()
        if not st["open"] and HOST.layout_holds(KEY):
            open_window()
        if not 0 <= st["next"] - now <= CLOSED_EVERY:
            st["next"] = now + (EVERY if st["open"] else CLOSED_EVERY)
            v = st["vals"] = read(now)
            show_ping(v.get("Ping", "-"))
            tip = "Ping %s, %s FPS, memory %s; click to open or close, drag to move" % (
                v.get("Ping", "-"), v.get("FPS", "-"), v.get("Memory", "-"))
            if tip != st["tip"] and btn["b"] is not None:
                st["tip"] = tip
                Kit.with_tip(btn["b"], tip)
            # The busiest list costs a pass over every module, so it is only gathered while someone can see it.
            if st["open"] and not st["minimized"] and not 0 <= st["top_next"] - now <= TOP_EVERY:
                st["top_next"] = now + TOP_EVERY
                st["top"] = busiest(now)
            if st["open"] and win["g"] is not None and not (st["minimized"] and st["docked"]):
                refresh()

    def _stop():
        """Module stop: save state, close the window and the button."""
        st["shutting"] = True
        HOST.dock_remove(KEY)
        Kit.save_min(MIN_KEY, st["minimized"])
        Kit.put_var(OPEN_KEY, "1" if st["open"] else "0")
        wnd.close()
        b, btn["g"] = btn["g"], None
        btn["b"] = btn["lbl"] = None
        Kit.save_pos(BTN_KEY, b)
        Kit.dispose(b)

    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed}


# Without the modules (running alone) the mother script does nothing further.
if not VA_ALONE:
    if not HOST.self_run(globals()):
        Kit.data_setup()
        PROFILES = Profiles()
        HOST.boot_mark("data setup")
        try:
            PROFILES.startup()
        except Exception as _ex:
            Kit.say("couldn't put the favourite profile on this character (%s%s)."
                    % (Tz.why(_ex), _error_where()), Kit.HUE_BAD)
        HOST.boot_mark("profiles")
        load_modules()
        HOST.boot_mark("module files")
        HOST.add("sysstats", "System Stats", "Ping, FPS and memory button", _module_sysstats, 0.1,
                 category="On screen").shipped = True
        HOST.run()
else:
    Kit.data_setup()
    PROFILES = Profiles()
