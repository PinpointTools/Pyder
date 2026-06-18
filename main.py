import src.interactive as init
import src.print as print
import argparse
import subprocess
import sys

def argParser():
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    runParser = subparsers.add_parser("run", help="Able to run commands that are available in the project's run.py")
    runParser.add_argument("runArgs", nargs=argparse.REMAINDER, help="Arguments to pass to run.py")
    
    args = parser.parse_args()
    
    if args.command is None:
        init.start()
    elif args.command == "run":
        subprocess.run([sys.executable, "run.py", *args.runArgs])
    
    return args

if __name__ == "__main__":
    try:
        argParser()
    except KeyboardInterrupt:
        print.warning("Keyboard interuption. Exiting...")