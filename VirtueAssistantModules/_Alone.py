import os
import re
VA_ROOT=os.path.dirname(str(API.ScriptPath).rstrip("/\\"))
VA_ALONE=sorted((n for n in os.listdir(VA_ROOT)if re.match(r"VirtueAssistantV[\d-]+\.py$",n)),key=lambda n:[int(a)for a in re.findall(r"\d+",n)])
if not VA_ALONE:API.SysMsg("Run alone: VirtueAssistantV<version>.py must be in LegionScripts, beside this folder.",33);raise SystemExit
exec(compile(re.sub(r"(?m)^import API$","",open(os.path.join(VA_ROOT,VA_ALONE[-1])).read()),VA_ALONE[-1],"exec"))
