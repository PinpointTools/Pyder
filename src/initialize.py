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
        domainSystem,
        qtorgtk,
        framework,
        variant,
        packageManager,
    ):
        self.projectName = projectName
        self.domainSystem = domainSystem
        self.framework = framework
        self.variant = variant
        self.packageManager = packageManager
        self.qtorgtk = qtorgtk

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
        os.makedirs(self.projectName)
        os.makedirs(f"{self.projectName}/icon")
        os.makedirs(f"{self.projectName}/src/backend")
        os.makedirs(f"{self.projectName}/src/frontend")

    def copyIcons(self):
        if getattr(sys, "frozen", False):
            resourceRoot = os.path.abspath(sys._MEIPASS)
        else:
            resourceRoot = str(SOURCE_ROOT)

        sourceDir = Path(resourceRoot) / "icon"
        destinationDir = Path(self.projectName) / "icon"

        for iconName in ("512.png", "512.ico", "512.icns"):
            shutil.copy2(sourceDir / iconName, destinationDir / iconName)

        print.success(f"Icons copied to {destinationDir}")

    def startPackageManager(self):
        print.log(f"Installing frontend with {self.packageManager}...")
        frontendDir = os.path.join(self.projectName, "src", "frontend")
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
                "npm",
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
                self.packageManager,
                "create",
                "vite@latest",
                "src/frontend",
                "--template",
                template,
                "--no-interactive",
            ]

        subprocess.run(command, cwd=self.projectName, check=True)
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
import subprocess
import sys
from pathlib import Path
import window as w
import time

projectRoot = Path(__file__).resolve().parent
frontendDir = projectRoot / "src" / "frontend"
packageManager = "{self.packageManager}"

def buildFrontend():
    subprocess.run([packageManager, "run", "build"], cwd=frontendDir, check=True)

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
    subprocess.run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "window.py",
            "--noconfirm",
            "--windowed",
            "--name",
            "{self.projectName}",
            "--add-data",
            dataArg,
            "--add-data",
            iconArg,
            f"--icon={{pyinstallerIcon}}",
        ],
        cwd=projectRoot,
        check=True,
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["test", "compile", "dev"])
    args = parser.parse_args()

    if args.command == "test":
        buildFrontend()
        subprocess.run([sys.executable, "window.py"], cwd=projectRoot, check=True)
    if args.command == "compile":
        compileApp()
    if args.command == "dev":
        devServer = subprocess.Popen([packageManager, "run", "dev"], cwd=frontendDir)
        print("Starting dev server...")
        try:
            time.sleep(1)
            w.startWindow(True)
        finally:
            devServer.terminate()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        exit(1)"""
            with open(f"{self.projectName}/run.py", "w") as f:
                f.write(script)
##########################################################################################

#################################### API SCRIPT ##################################
            apiScript = f"""import webview as wv
import sys
import os

class API:
    def __init__(self):
        self.window = wv.active_window()
        self.appID = "{self.domainSystem}.{self.projectName}"

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
            with open(f"{self.projectName}/src/backend/api.py", "w") as f:
                f.write(apiScript)
##########################################################################################

################################# WINDOW SCRIPT ########################################
            windowScript = f"""import os
import sys

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

def startWindow(dev):
    if dev:
        pathToApp = "http://localhost:5173"
    else:
        pathToApp = os.path.join(distDir, "index.html")
        if not os.path.exists(pathToApp):
            raise FileNotFoundError(
                "Frontend build output was not found. Run `python run.py test` or `python run.py compile` first."
            )

    wv.create_window(
        title="{self.projectName}",
        url=str(pathToApp),
        js_api=API(),
        width=800,
        height=600,
    )

    wv.start(
        http_server=True,
        private_mode=False,
        debug=not getattr(sys, "frozen", False),
        icon=iconPath,
    )

if __name__ == "__main__":
    startWindow(False)"""
            with open(f"{self.projectName}/window.py", "w") as f:
                f.write(windowScript)
##########################################################################################

##################################### GIT IGNORE #################################
            gitIgnore = """# python
__pycache__
*.pyc
build

# npm
node_modules
dist

*-lock.yaml
*-lock.json

# misc
.env"""
            with open(f"{self.projectName}/.gitignore", "w") as f:
                f.write(gitIgnore)

##########################################################################################

        with open(f"{self.projectName}/requirements.txt", "w") as f:
            for lib in libraries():
                f.write(f"{lib}\n")

        mainScript()
        pythonExecutable = self.getPythonExecutable()
        subprocess.run([pythonExecutable, "-m", "venv", "venv"], cwd=self.projectName, check=True)

        if sys.platform == "win32":
            venvPython = ".\\venv\\Scripts\\python"
            subprocess.run(
                [venvPython, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=self.projectName,
                check=True,
            )
        else:
            venvPython = "./venv/bin/python"
            subprocess.run(
                [venvPython, "-m", "pip", "install", "-r", "requirements.txt"],
                cwd=self.projectName,
                check=True,
            )

        print.success(f"Backend scaffolded in {self.projectName}/src/backend")

def start(
    projectName,
    domainSystem,
    qtorgtk,
    framework,
    variant,
    packageManager,
):
    init = Initialize(
        projectName,
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
    print.success(f"Project initialized in {projectName}")
    print.log(f"Before you run the app, make sure you've installed the required dependencies at `{projectName}/src/frontend/`")
    print.log(f"The reason why this wasn't installed automatically is because of subprocess being a bitch because it can't run `{packageManager} install` @ `{projectName}/src/frontend/`")
    print.log(f"For python libraries @ `{projectName}/requirements.txt`, it's already installed in a virtual environment. Just activate it with `source venv/bin/activate` (Linux/macOS) or `venv\\Scripts\\activate` (Windows)")
    print.log("To run the app, use `python run.py test`. This command will build Vite, and then launch `window.py`.")
    print.log("To open the already-built app directly, use `python window.py`.")
    print.log("To compile the app, use `python run.py compile`. This command will build Vite and package `window.py` with PyInstaller.")
    print.empty()

    print.log("If you're lazy (like me), just copy this code below. This for macOS/Linux.")
    print.log(f"  cd {projectName}/src/frontend/ && {packageManager} install && cd ../.. && venv/bin/python run.py dev")
    print.log("For windows powershell.")
    print.log(f"  cd {projectName}\\src\\frontend\\ && {packageManager} install && cd ..\\.. && venv\\Scripts\\python run.py dev")
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
