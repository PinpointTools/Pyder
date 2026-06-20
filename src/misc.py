import sys
import os

def convertNameToID(name: str) -> str:
    return "".join(
        c.lower() if c.isalnum() else "-" if c == " " else ""
        for c in name
    ).strip("-")

def getPython():
    if sys.platform == "win32":
        pathToScripts = "\\Scripts\\"
    else:
        pathToScripts = "/bin/"

    if os.path.exists(".venv"):
        return f".venv{pathToScripts}"
    elif os.path.exists("venv"):
        return f"venv{pathToScripts}"