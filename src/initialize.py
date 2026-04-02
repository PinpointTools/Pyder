import os
import shutil
import subprocess
import sys
from pathlib import Path
import src.print as print

SOURCE_ROOT = Path(__file__).resolve().parent.parent
class Initialize:
    def __init__(
        self,
        projectName,
        projectID,
        domainSystem,
        qtorgtk,
        framework,
        variant,
        packageManager,
    ):

        self.projectName = projectName
        self.projectID = projectID
        self.domainSystem = domainSystem
        self.framework = framework
        self.variant = variant
        self.packageManager = packageManager
        self.qtorgtk = qtorgtk

    def resolveCommand(self, command):
        commandPath = shutil.which(command)
        if commandPath:
            return commandPath

        if os.name == "nt":
            commandPath = shutil.which(f"{command}.cmd")
            if commandPath:
                return commandPath

        return command

    def getPythonExecutable(self):
        if not getattr(sys, "frozen", False):
            return sys.executable

        for candidate in ("python3", "python"):
            pythonExecutable = shutil.which(candidate)
            if pythonExecutable:
                return pythonExecutable

        raise FileNotFoundError(
            "Python executable was not found in PATH. Install Python and try again."
        )

    def fileSystem(self):
        os.makedirs(self.projectID)
        os.makedirs(f"{self.projectID}/icon")
        os.makedirs(f"{self.projectID}/src/backend")
        os.makedirs(f"{self.projectID}/src/frontend")

    def copyIcons(self):
        if getattr(sys, "frozen", False):
            resourceRoot = os.path.abspath(sys._MEIPASS)
        else:
            resourceRoot = str(SOURCE_ROOT)

        sourceDir = Path(resourceRoot) / "icon"
        destinationDir = Path(self.projectID) / "icon"

        for iconName in ("512.png", "512.ico", "512.icns"):
            shutil.copy2(sourceDir / iconName, destinationDir / iconName)

        print.success(f"Icons copied to {destinationDir}")

    def startPackageManager(self):
        print.log(f"Installing frontend with {self.packageManager}...")
        frontendDir = os.path.join(self.projectID, "src", "frontend")
        templateMap = {
            ("Vanilla", "JavaScript"): "vanilla",
            ("Vanilla", "TypeScript"): "vanilla-ts",
            ("Svelte", "JavaScript"): "svelte",
            ("Svelte", "TypeScript"): "svelte-ts",
            ("React", "JavaScript"): "react",
            ("React", "TypeScript"): "react-ts",
            ("Vue", "JavaScript"): "vue",
            ("Vue", "TypeScript"): "vue-ts",
        }
        template = templateMap.get((self.framework, self.variant))

        if self.packageManager == "npm":
            command = [
                self.resolveCommand("npm"),
                "create",
                "vite@latest",
                "src/frontend",
                "--",
                "--template",
                template,
                "--no-interactive",
            ]
        else:
            command = [
                self.resolveCommand(self.packageManager),
                "create",
                "vite@latest",
                "src/frontend",
                "--template",
                template,
                "--no-interactive",
            ]

        subprocess.run(command, cwd=self.projectID, check=True)
        print.success(f"Frontend scaffolded in {frontendDir}")

    def startPython(self):
        def libraries():
            requiredLibs = ["pyinstaller", 'pywebview; sys_platform != "linux"']
            if self.qtorgtk == "GTK":
                requiredLibs.append('pywebview[gtk]; sys_platform == "linux"')
            else:
                requiredLibs.append('pywebview[qt]; sys_platform == "linux"')
            return requiredLibs

################################ MAIN RUN SCRIPT #########################################
        def mainScript():
            script = f"""# Project initialized with Pyder! @ https://github.com/PinpointTools/Pyder
# Pyder is a Python-based tool for building cross-platform desktop applications.
# If you love how Pyder works, please consider starring it on GitHub.

import argparse
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
import window as w
from pyder import *

projectRoot = Path(__file__).resolve().parent
frontendDir = projectRoot / "src" / "frontend"
devServerHost = "localhost"
devServerPort = 5173
packageManager = "{self.packageManager}"

def resolveCommand(command):
    commandPath = shutil.which(command)
    if commandPath:
        return commandPath

    if sys.platform == "win32":
        commandPath = shutil.which(f"{{command}}.cmd")
        if commandPath:
            return commandPath
    return command

packageManager = resolveCommand(packageManager)
def buildFrontend():
    subprocess.run([packageManager, "run", "build"], cwd=frontendDir, check=True)

class SeparateWindow:
    def waitForDevServer(self, timeoutSeconds=20):
        deadline = time.time() + timeoutSeconds
        while time.time() < deadline:
            try:
                with socket.create_connection((devServerHost, devServerPort), timeout=1):
                    return
            except OSError:
                time.sleep(0.25)
                
        raise TimeoutError(
            f"Timed out waiting for the frontend dev server at http://{{devServerHost}}:{{devServerPort}}."
        )

    def launchFrontendDevServerInSeparateWindow(self):
        if sys.platform == "win32":
            subprocess.run(
                [
                    "cmd",
                    "/c",
                    "start",
                    "Protux Frontend Dev Server",
                    packageManager,
                    "run",
                    "dev",
                ],
                cwd=frontendDir,
                check=True,
            )
            return
    
        if sys.platform == "darwin":    
            script = (
                f'tell application "Terminal" to do script '
                f'"cd {{frontendDir}} && {{packageManager}} run dev"'
            )
            subprocess.run(["osascript", "-e", script], check=True)
            return
    
        for terminal in ("x-terminal-emulator", "gnome-terminal", "konsole", "xterm"):
            terminalPath = shutil.which(terminal)
            if terminalPath:
                subprocess.run(
                    [terminalPath, "-e", packageManager, "run", "dev"],
                    cwd=frontendDir,
                    check=True,
                )
                return
    
        raise RuntimeError(
            "Could not find a terminal emulator to launch the frontend dev server. "
            "Run `python run.py dev backend` in a separate terminal instead."
        )

def runDevServer():
    subprocess.run([packageManager, "run", "dev"], cwd=frontendDir, check=True)

def compileApp():
    buildFrontend()
    separator = ";" if sys.platform == "win32" else ":"
    dataArg = f"{{frontendDir / 'dist'}}{{separator}}src/frontend/dist"
    iconArg = f"{{'icon'}}{{separator}}icon"
    if sys.platform == "win32":
        pyinstallerIcon = "icon/512.ico"
    elif sys.platform == "darwin":
        pyinstallerIcon = "icon/512.icns"
    else:
        pyinstallerIcon = "icon/512.png"

    pyinstallerArgs = [
        sys.executable,
        "-m",
        "PyInstaller",
        "window.py",
        "--noconfirm",
        "--windowed",
        "--name",
        pyder_projectName,
        "--add-data",
        dataArg,
        "--add-data",
        iconArg,
        f"--icon={{pyinstallerIcon}}",
    ]

    if sys.platform == "win32":
        pyinstallerArgs.extend(["--collect-all", "winpty"])

    subprocess.run(
        pyinstallerArgs,
        cwd=projectRoot,
        check=True,
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["test", "compile", "dev"])
    parser.add_argument("target", nargs="?", choices=["window", "server"])
    args = parser.parse_args()

    if args.command != "dev" and args.target is not None:
        parser.error("`window` and `server` targets are only valid with `python run.py dev`.")

    if args.command == "test":
        buildFrontend()
        w.startWindow()
    elif args.command == "compile":
        compileApp()
    elif args.command == "dev":
        if args.target == "window":
            w.startWindow(True)
        elif args.target == "server":
            runDevServer()
        else:
            SeparateWindow().launchFrontendDevServerInSeparateWindow()
            SeparateWindow().waitForDevServer()
            w.startWindow(True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        exit(1)"""
            with open(f"{self.projectID}/run.py", "w") as f:
                f.write(script)
##########################################################################################

#################################### API SCRIPT ##################################
            apiScript = """import webview as wv
import sys
import os
from pyder import *

class API:
    def __init__(self):
        self.window = wv.active_window()
        self.appID = f"{pyder_domainSystem}.{pyder_projectID}"

    def getConfigPath(self):
        if sys.platform == "win32":
            configPath = os.path.join(os.getenv("APPDATA"), self.appID)
        elif sys.platform == "darwin":
            configPath = os.path.join(os.getenv("HOME"), "Library", "Application Support", self.appID)
        elif sys.platform == "linux":
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        else:
            configPath = os.path.join(os.getenv("HOME"), ".config", self.appID)
        return configPath"""
            with open(f"{self.projectID}/src/backend/api.py", "w") as f:
                f.write(apiScript)
##########################################################################################

################################# WINDOW SCRIPT ########################################
            windowScript = """import os
import sys
import json
from pyder import *

import webview as wv
from src.backend.api import API

if getattr(sys, "frozen", False):
    resourceRoot = os.path.abspath(sys._MEIPASS)
    projectRoot = os.path.dirname(os.path.abspath(sys.executable))
else:
    projectRoot = os.path.dirname(os.path.abspath(__file__))
    resourceRoot = projectRoot

distDir = os.path.join(resourceRoot, "src", "frontend", "dist")

iconPath = ""
if sys.platform == "win32":
    iconPath = os.path.join(resourceRoot, "icon", "512.ico")
elif sys.platform == "darwin":
    iconPath = os.path.join(resourceRoot, "icon", "512.icns")
else:
    iconPath = os.path.join(resourceRoot, "icon", "512.png")

def startWindow(dev=False):
    if dev:
        pathToApp = "http://localhost:5173"
    else:
        pathToApp = os.path.join(distDir, "index.html")
        if not os.path.exists(pathToApp):
            raise FileNotFoundError(
                "Frontend build output was not found. Run `python run.py test` or `python run.py compile` first."
            )

    wv.create_window(
        title=pyder_projectName,
        url=str(pathToApp),
        js_api=API(),
        width=pyder_window_initSize_v1,
        height=pyder_window_initSize_v2,
        min_size=(pyder_window_minSize_v1, pyder_window_minSize_v2)
    )

    wv.start(
        http_server=True,
        private_mode=True,
        debug=not getattr(sys, "frozen", False),
        icon=iconPath,
    )

if __name__ == "__main__":
    startWindow()"""
            with open(f"{self.projectID}/window.py", "w") as f:
                f.write(windowScript)
##########################################################################################

##################################### GIT IGNORE #################################
            gitIgnore = """# python
__pycache__
*.pyc
build
dist
*venv*

# npm
node_modules
dist

# misc
.env"""
            with open(f"{self.projectID}/.gitignore", "w") as f:
                f.write(gitIgnore)
##########################################################################################

##################################### PYDER PYTHON #################################
            pyderProject = f"""_pyder_project = [
    {{
        "projectName": "{self.projectName}",
        "domainSystem": "{self.domainSystem}",
        "projectID": "{self.projectID}",
        "version": "0.1.0",
        "window": {{
            "minSize": [800, 600],
            "initSize": [800, 600]
        }}
    }}
]

pyder_projectName = _pyder_project[0]["projectName"]
pyder_domainSystem = _pyder_project[0]["domainSystem"]
pyder_projectID = _pyder_project[0]["projectID"]
pyder_version = _pyder_project[0]["version"]

pyder_window = _pyder_project[0]["window"]
pyder_window_minSize_v1, pyder_window_minSize_v2 = pyder_window["minSize"]
pyder_window_initSize_v1, pyder_window_initSize_v2 = pyder_window["initSize"]"""
            with open(f"{self.projectID}/pyder.py", "w") as f:
                f.write(pyderProject)
##########################################################################################

        with open(f"{self.projectID}/requirements.txt", "w") as f:
            for lib in libraries():
                f.write(f"{lib}\n")

        mainScript()
        pythonExecutable = self.getPythonExecutable()
        subprocess.run([pythonExecutable, "-m", "venv", "venv"], cwd=self.projectID, check=True)

        if sys.platform == "win32":
            venvPython = f".\\{self.projectID}\\venv\\Scripts\\python"
            subprocess.run(
                [venvPython, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=self.projectID,
                check=True,
            )
        else:
            venvPython = f"./{self.projectID}/venv/bin/python"
            subprocess.run(
                [venvPython, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=self.projectID,
                check=True,
            )

        print.success(f"Backend scaffolded in {self.projectID}/src/backend")

def start(
    projectName,
    projectID,
    domainSystem,
    qtorgtk,
    framework,
    variant,
    packageManager,
):
    init = Initialize(
        projectName,
        projectID,
        domainSystem,
        qtorgtk,
        framework,
        variant,
        packageManager,
    )
    init.fileSystem()
    init.copyIcons()
    init.startPackageManager()
    init.startPython()

    # yap yap
    print.success(f"Project initialized in {projectID}")
    print.log(f"Before you run the app, make sure you've installed the required dependencies at `{projectID}/src/frontend/`")
    print.log(f"The reason why this wasn't installed automatically is because of subprocess being a bitch because it can't run `{packageManager} install` @ `{projectID}/src/frontend/`")
    print.log(f"For python libraries @ `{projectID}/requirements.txt`, it's already installed in a virtual environment. Just activate it with `source venv/bin/activate` (Linux/macOS) or `venv\\Scripts\\activate` (Windows)")
    print.log("To run the app, use `python run.py test`. This command will build Vite, and then launch `window.py`.")
    print.log("To open the already-built app directly, use `python window.py`.")
    print.log("To compile the app, use `python run.py compile`. This command will build Vite and package `window.py` with PyInstaller.")
    print.empty()

    print.log("If you're lazy (like me), just copy this code below. This for macOS/Linux.")
    print.log(f"  cd {projectID}/src/frontend/ && {packageManager} install && cd ../.. && venv/bin/python run.py dev")
    print.log("For windows powershell <7.")
    print.log(f"  cd project-test\\src\\frontend; if ($?) {{ {packageManager} install }}; if ($?) {{ cd ..\\.. }}; if ($?) {{ venv\\Scripts\\python run.py dev }}")
    print.log("For windows powershell 7+.")
    print.log(f"  cd {projectID}\\src\\frontend && {packageManager} install && cd ..\\.. && venv\\Scripts\\python run.py dev")
    print.empty()

    print.log("To compile after installing the frontend dependencies, run:")
    print.log("  `venv/bin/python run.py compile` (Linux/macOS)")
    print.log("  `venv\\Scripts\\python run.py compile` (Windows)")
    print.empty()

    print.log("Documentation @ https://github.com/PinpointTools/Pyder/wiki")
    print.warning("PLEASE READ THEM. PLEASE.")
    print.empty()
    print.success("Made with <3 from Pinpoint Tools Team.")
    print.warning("Pyder is in ALPHA!!! Expect there to be bugs. Report them @ https://github.com/PinpointTools/Pyder/issues")
