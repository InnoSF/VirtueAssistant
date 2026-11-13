# Run-alone helper: not a module and not a script to start by hand. A module file runs it when it
# is started on its own, without the mother script, so the module can be tried by itself.
#
# It looks in the folder that holds the Legion scripts for the newest mother script file, takes out
# the one line that loads the API module (the Legion script already has it) and runs the rest in
# this namespace. The mother then loads the modules folder and the module registers itself as it
# would normally. With no mother script file found it says so in the game and stops.
import os
import re
# The folder above the one holding this script: the folder of the Legion scripts.
VA_ROOT = os.path.dirname(str(API.ScriptPath).rstrip("/\\"))
# Mother script files named by version, oldest first; the last one is the newest. Sorted by the
# numbers in the name, so a longer number sorts after a shorter one.
VA_ALONE = sorted((n for n in os.listdir(VA_ROOT) if re.match(r"VirtueAssistantV[\d-]+\.py$", n)),
                  key=lambda n: [int(x) for x in re.findall(r"\d+", n)])
# No mother script file beside this folder: tell the player and stop.
if not VA_ALONE:
    API.SysMsg("Run alone: VirtueAssistantV<version>.py must be in LegionScripts, beside this folder.", 33)
    raise SystemExit
# Run the newest mother script, with the line that loads the API module left out, under its own
# file name so errors point at it.
exec(compile(re.sub(r"(?m)^import API$", "", open(os.path.join(VA_ROOT, VA_ALONE[-1])).read()), VA_ALONE[-1], "exec"))
