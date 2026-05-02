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

        for iconName in ("favicon.png", "favicon.ico", "favicon.icns"):
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
        def mainScript():
##################################### PYDER PYTHON #################################
            pyderProject = f"""_pyder_project = [
    {{
        "projectName": "{self.projectName}",
        "domainSystem": "{self.domainSystem}",
        "projectID": "{self.projectID}",
        "packageManager": "{self.packageManager}",
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
pyder_packageManager = _pyder_project[0]["packageManager"]
pyder_version = _pyder_project[0]["version"]

pyder_window = _pyder_project[0]["window"]
pyder_window_minSize_v1, pyder_window_minSize_v2 = pyder_window["minSize"]
pyder_window_initSize_v1, pyder_window_initSize_v2 = pyder_window["initSize"]"""
            with open(f"{self.projectID}/pyder.py", "w") as f:
                f.write(pyderProject)
##########################################################################################

        def copyTemplateFiles():
            templateDir = SOURCE_ROOT / "template" / "vite"
            destinationDir = Path(self.projectID)

            for file in ("window.py", "run.py", "requirements.txt", ".gitignore"):
                shutil.copy2(templateDir / file, destinationDir / file)

            os.makedirs(destinationDir / "src" / "backend", exist_ok=True)
            shutil.copy2(templateDir / "src" / "backend" / "api.py", destinationDir / "src" / "backend" / "api.py")

            print.success(f"Template files copied to {destinationDir}")

        mainScript()
        copyTemplateFiles()
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
