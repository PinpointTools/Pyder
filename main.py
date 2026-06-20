import src.interactive as inter
import src.print as print
import src.initialize as init
import src.misc as misc

import argparse
import subprocess
import sys
import os
import urllib.request

if getattr(sys, 'frozen', False):
    basePath = sys._MEIPASS
else:
    basePath = os.path.dirname(os.path.abspath(__file__))

def argParser():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # == Run ==
    runParser = subparsers.add_parser("run", help="Able to run commands that are available in the project's run.py")
    runParser.add_argument("runArgs", nargs=argparse.REMAINDER, help="Arguments to pass to run.py")

    # == Version ==
    subparsers.add_parser("version", help="Displays current version")

    # == Install ==
    installParser = subparsers.add_parser("install", help="Installs the project's dependencies")
    installParser.add_argument("type", choices=["frontend", "backend"], help="Install either in Frontend or Backend")
    installParser.add_argument("package", nargs=argparse.REMAINDER, help="Package(s) to install")

    # == Init ==
    initParser = subparsers.add_parser("init", help="Initializes a new Pyder project with the maintainer's choice of framework.")
    initParser.add_argument("name", help="Name of the project")
    initParser.add_argument("domainSystem", help="The domain system to use (e.g. io.github.pinpointtools)")
    
    # == == ==
    args = parser.parse_args()
    
    if args.command is None:
        inter.start()
    elif args.command == "run":
        subprocess.run(["python3", "run.py", *args.runArgs])
    elif args.command == "version":
        url = "https://raw.githubusercontent.com/PinpointTools/Pyder/refs/heads/main/version.txt"
        try:
            with urllib.request.urlopen(url) as response:
                latestVersion = response.read().decode('utf-8').strip()
        except Exception as e:
            print.error(f"Error fetching URL: {e}")
            return None

        versionPath = os.path.join(basePath, "version.txt")
        with open(versionPath, "r") as f:
            version = f.read().strip()
        print.log(f"pyder ver; {version}")
        
        if version != latestVersion:
            print.warning(f"your pyder is out of date! ({version} != {latestVersion})")
        else:
            print.success(f"your pyder is up to date! ({version} == {latestVersion})")
    elif args.command == "install":
        if args.package:
            print.log(f"Installing {args.package} for {args.type}...")
            if args.type == "frontend":
                subprocess.run(["npm", "install", *args.package], cwd="src/frontend")
            elif args.type == "backend":
                if sys.platform == "win32":
                    pathToScripts = "\\Scripts\\"
                else:
                    pathToScripts = "/bin/"
                    
                if os.path.exists(".venv"):
                    subprocess.run([f".venv{pathToScripts}pip", "install", *args.package])
                elif os.path.exists("venv"):
                    subprocess.run([f"venv{pathToScripts}pip", "install", *args.package])
                else:
                    return print.error("No virtual environment found. Or it's a different folder name? We'll never know!")
            print.success(f"Sucsesfully installed {args.package} for {args.type}.")
            print.log("Or did it fail? Hopefully it didn't.")
        else:
            print.error("Please specify a package to install")
    elif args.command == "init":
        if args.name and args.domainSystem:
            print.log(f"Initializing new Pyder project '{args.name}' with domain system '{args.domainSystem}'...")
            
            init.start(
                args.name,
                misc.convertNameToID(args.name),
                args.domainSystem,
                "Qt",
                "Svelte",
                "TypeScript",
                "pnpm",
                False,
            )
        else:
            print.error("Please specify a name and domain system for the project")
    return args

if __name__ == "__main__":
    try:
        argParser()
    except KeyboardInterrupt:
        print.warning("Keyboard interuption. Exiting...")