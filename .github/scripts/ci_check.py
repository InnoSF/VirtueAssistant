import os
import re
import sys

MOTHER_RE = re.compile(r"^VirtueAssistantV(\d+(?:-\d+)*)\.py$")
BAD_NAMES = ("*" + "pers" + "onalmodules*", "bandage" + "target*", "insp" + "ector*")


def fail_list(errs, title):
    if errs:
        print("FAIL " + title + ":")
        for e in errs:
            print("  " + e)
    else:
        print("ok   " + title)
    return len(errs)


def glob_match(name, pat):
    rx = "^" + re.escape(pat).replace("\\*", ".*") + "$"
    return re.match(rx, name, re.I) is not None


def mothers(root):
    return sorted(n for n in os.listdir(root) if n.startswith("VirtueAssistantV") and n.endswith(".py") and os.path.isfile(os.path.join(root, n)))


def py_files(root):
    out = [n for n in mothers(root)]
    mods = os.path.join(root, "VirtueAssistantModules")
    if os.path.isdir(mods):
        for n in sorted(os.listdir(mods)):
            if n.endswith(".py") and os.path.isfile(os.path.join(mods, n)):
                out.append("VirtueAssistantModules/" + n)
    rd = os.path.join(root, "readable")
    if os.path.isdir(rd):
        found = []
        for d, subs, names in os.walk(rd):
            for n in names:
                if n.endswith(".py"):
                    rel = os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/")
                    found.append(rel)
        out.extend(sorted(found))
    return out


def text_files(root):
    out = [n for n in sorted(os.listdir(root)) if n.startswith("PATCHLOG-") and n.endswith(".md")]
    dd = os.path.join(root, "docs")
    if os.path.isdir(dd):
        for d, subs, names in os.walk(dd):
            for n in sorted(names):
                if n.endswith(".md"):
                    out.append(os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/"))
    return out


def read(root, rel):
    f = open(os.path.join(root, rel), "rb")
    try:
        return f.read()
    finally:
        f.close()


def check_mother(root):
    errs = []
    ms = mothers(root)
    ver = ""
    if len(ms) != 1:
        errs.append("expected exactly one top-level VirtueAssistantV*.py, found %d: %s" % (len(ms), " ".join(ms) or "none"))
    elif not MOTHER_RE.match(ms[0]):
        errs.append("mother name is not VirtueAssistantV<digits>-<digits>.py: " + ms[0])
    else:
        ver = MOTHER_RE.match(ms[0]).group(1).replace("-", ".")
        if not os.path.isfile(os.path.join(root, "PATCHLOG-" + ver + ".md")):
            errs.append("missing PATCHLOG-" + ver + ".md for " + ms[0])
    mods = os.path.join(root, "VirtueAssistantModules")
    if not os.path.isdir(mods):
        errs.append("missing VirtueAssistantModules")
    else:
        for d, subs, names in os.walk(mods):
            if d != mods:
                for n in names:
                    if n.endswith(".py"):
                        errs.append("nested module file is not shipped or checked: " + os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/"))
    return errs, (ms[0] if ver else ""), ver


def house_syntax(tree):
    import ast
    kinds = []
    for node in ast.walk(tree):
        k = None
        if isinstance(node, ast.JoinedStr):
            k = "f-string"
        elif hasattr(ast, "NamedExpr") and isinstance(node, ast.NamedExpr):
            k = "walrus"
        elif hasattr(ast, "Match") and isinstance(node, ast.Match):
            k = "match"
        elif isinstance(node, (ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith, ast.Await)):
            k = "async/await"
        elif isinstance(node, ast.AnnAssign):
            k = "annotation"
        elif isinstance(node, (ast.FunctionDef, ast.Lambda)):
            a = node.args
            if getattr(a, "posonlyargs", None):
                k = "positional-only parameters"
            elif isinstance(node, ast.FunctionDef) and (node.returns is not None or any(x is not None and x.annotation is not None for x in a.args + a.kwonlyargs + [a.vararg, a.kwarg])):
                k = "annotation"
        if k:
            kinds.append((getattr(node, "lineno", 0), k))
    return sorted(kinds)


def run_checks(root):
    import ast
    bad = 0
    files = py_files(root)
    print("python files: %d" % len(files))
    errs, mother, ver = check_mother(root)
    bad += fail_list(errs, "one mother and its patch log")
    syn = []
    hs = []
    asc = []
    for rel in files:
        raw = read(root, rel)
        pos = -1
        for i in range(len(raw)):
            if raw[i] > 127:
                pos = i
                break
        if pos >= 0:
            asc.append("%s: non-ASCII byte at line %d" % (rel, raw[:pos].count(b"\n") + 1))
        try:
            tree = ast.parse(raw.decode("utf-8", "replace"), rel)
        except SyntaxError as e:
            syn.append("%s: line %s: %s" % (rel, e.lineno, e.msg))
            continue
        k = house_syntax(tree)
        if k:
            hs.append("%s: %s at line %d" % (rel, k[0][1], k[0][0]))
    bad += fail_list(syn, "Python 3 syntax")
    bad += fail_list(hs, "IronPython 3.4 house syntax (no f-string, walrus, match, async, annotations)")
    bad += fail_list(asc, "plain ASCII")
    name = os.environ.get("BLOCKED_NAME", "").strip()
    if not name:
        print("note the name check is skipped: repository variable or secret BLOCKED_NAME is not set")
    else:
        rx = re.compile(r"\b" + re.escape(name), re.I)
        hits = []
        for rel in files + text_files(root):
            txt = read(root, rel).decode("utf-8", "replace")
            for i, line in enumerate(txt.splitlines(), 1):
                if rx.search(line):
                    hits.append("%s: line %d" % (rel, i))
                    break
        bad += fail_list(hits, "blocked name")
    names = []
    for d, subs, fs in os.walk(root):
        if ".git" in subs:
            subs.remove(".git")
        for n in subs + fs:
            for p in BAD_NAMES:
                if glob_match(n, p):
                    names.append(os.path.relpath(os.path.join(d, n), root).replace(os.sep, "/"))
                    break
    bad += fail_list(names, "no private module files")
    out = os.environ.get("GITHUB_OUTPUT", "")
    if out and mother:
        f = open(out, "a")
        try:
            f.write("mother=" + mother + "\n")
            f.write("ver=" + ver + "\n")
        finally:
            f.close()
    return bad


def run_ipy(root):
    files = py_files(root)
    errs = 0
    for rel in files:
        try:
            src = read(root, rel).decode("utf-8")
            compile(src, rel, "exec")
        except Exception as e:
            errs += 1
            print("ERR " + rel + ": " + str(e))
    print("%s files=%d errs=%d" % (sys.version.split()[0], len(files), errs))
    return errs


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "checks"
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    if mode == "ipy":
        n = run_ipy(root)
    else:
        n = run_checks(root)
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
