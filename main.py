import src.interactive as init
import src.print as print
import argparse
import subprocess
import sys
import urllib.request

def argParser():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    runParser = subparsers.add_parser("run", help="Able to run commands that are available in the project's run.py")
    runParser.add_argument("runArgs", nargs=argparse.REMAINDER, help="Arguments to pass to run.py")

    subparsers.add_parser("version", help="Displays current version")
    
    args = parser.parse_args()
    
    if args.command is None:
        init.start()
    elif args.command == "run":
        subprocess.run([sys.executable, "run.py", *args.runArgs])
    elif args.command == "version":
        url = "https://raw.githubusercontent.com/PinpointTools/Pyder/refs/heads/main/version.txt"
        try:
            with urllib.request.urlopen(url) as response:
                latestVersion = response.read().decode('utf-8').strip()
        except Exception as e:
            print.error(f"Error fetching URL: {e}")
            return None
        
        with open("version.txt", "r") as f:
            version = f.read().strip()
        print.log(f"pyder ver; {version}")
        
        if version != latestVersion:
            print.warning(f"your pyder is out of date! ({version} != {latestVersion})")
        else:
            print.log(f"your pyder is up to date! ({version} == {latestVersion})")
    return args

if __name__ == "__main__":
    try:
        argParser()
    except KeyboardInterrupt:
        print.warning("Keyboard interuption. Exiting...")