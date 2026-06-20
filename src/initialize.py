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
        isTest
    ):

        self.projectName = projectName
        self.projectID = projectID
        self.domainSystem = domainSystem
        self.framework = framework
        self.variant = variant
        self.packageManager = packageManager
        self.qtorgtk = qtorgtk
        self.isTest = isTest

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

        if not self.isTest:
            print.success(f"Icons copied to {destinationDir}")

    def startPackageManager(self):
        if not self.isTest:
            print.log(f"Installing frontend with {self.packageManager}...")
        frontendDir = os.path.join(self.projectID, "src", "frontend")
        # ("", ""): "",
        templateMap = {
            ("Vanilla", "JavaScript"): "vanilla",
            ("Vanilla", "TypeScript"): "vanilla-ts",
            ("Svelte", "JavaScript"): "svelte",
            ("Svelte", "TypeScript"): "svelte-ts",
            ("React", "JavaScript"): "react",
            ("React", "TypeScript"): "react-ts",
            ("Vue", "JavaScript"): "vue",
            ("Vue", "TypeScript"): "vue-ts",
            ("Preact", "JavaScript"): "preact",
            ("Preact", "TypeScript"): "preact-ts",
            ("Lit", "JavaScript"): "lit",
            ("Lit", "TypeScript"): "lit-ts",
            ("Solid", "JavaScript"): "solid",
            ("Solid", "TypeScript"): "solid-ts",
            ("Ember", "JavaScript"): "ember",
            ("Ember", "TypeScript"): "ember-ts",
            ("Qwik", "JavaScript"): "qwik",
            ("Qwik", "TypeScript"): "qwik-ts",
            ("Amber", "JavaScript"): "amber",
            ("Amber", "TypeScript"): "amber-ts",
            ("Marko", "JavaScript"): "marko",
            ("Marko", "TypeScript"): "marko-ts",
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

        if not self.isTest:
            subprocess.run(command, cwd=self.projectID, check=True)
            print.success(f"Frontend scaffolded in {frontendDir}")
        else:
            subprocess.run(command, cwd=self.projectID, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

        def gtkorqt():
            with open(f"{self.projectID}/requirements.txt", "w") as f:
                f.write("pyinstaller\npywebview; sys_platform != 'linux'\n")
            if self.qtorgtk == "GTK":
                packages = ["pywebview[gtk]; sys_platform == 'linux'"]
                with open(f"{self.projectID}/requirements.txt", "a") as f:
                    f.write("\n".join(packages))
            elif self.qtorgtk == "Qt":
                packages = [
                    "pywebview[qt]; sys_platform == 'linux'",
                    "qtpy",
                    "PyQt6",
                    "PyQt6-WebEngine",
                ]
                with open(f"{self.projectID}/requirements.txt", "a") as f:
                    f.write("\n".join(packages))
            else:
                print.error("Invalid qtorgtk value")

        def copyTemplateFiles():
            templateDir = SOURCE_ROOT / "template" / "vite"
            destinationDir = Path(self.projectID)

            for file in ("window.py", "run.py", ".gitignore"):
                shutil.copy2(templateDir / file, destinationDir / file)

            os.makedirs(destinationDir / "src" / "backend", exist_ok=True)
            shutil.copy2(templateDir / "src" / "backend" / "api.py", destinationDir / "src" / "backend" / "api.py")

            if not self.isTest:
                print.success(f"Template files copied to {destinationDir}")

        mainScript()
        copyTemplateFiles()
        gtkorqt()

        print.success(f"Backend scaffolded in {self.projectID}/src/backend")

def start(
    projectName,
    projectID,
    domainSystem,
    qtorgtk,
    framework,
    variant,
    packageManager,
    needVenv,
):
    init = Initialize(
        projectName,
        projectID,
        domainSystem,
        qtorgtk,
        framework,
        variant,
        packageManager,
        needVenv,
    )

    init.fileSystem()
    init.copyIcons()
    init.startPackageManager()
    init.startPython()

    # yap yap
    if not init.isTest:
        print.success(f"Project initialized in {projectID}")
        print.log("To install the required dependencies for the frontend and the backend, run:")
        print.log("  python run.py init")
        print.empty()

        print.log("To run the development server, run:")
        print.log("  python run.py dev")
        print.warning("THIS MAY NOT WORK MOST OF THE TIME.")
        print.log("Running it in a different process (window or server)")
        print.log("  python run.py dev server")
        print.log("  python run.py dev window")
        print.empty()

        print.log("To compile the app, run:")
        print.log("  python run.py compile")
        print.empty()
    
        print.log("Documentation @ https://github.com/PinpointTools/Pyder/wiki")
        print.warning("PLEASE READ THEM. PLEASE.")
        print.empty()
        print.success("Made with <3 from Pinpoint Tools Team.")
        print.warning("Pyder is in ALPHA!!! Expect there to be bugs. Report them @ https://github.com/PinpointTools/Pyder/issues")
