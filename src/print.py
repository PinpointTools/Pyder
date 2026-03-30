from termcolor import colored

def success(message):
    symbol = "✓"
    color = "green"
    pta(symbol, color, message)
def error(message):
    symbol = "✗"
    color = "light_red"
    pta(symbol, color, message)
def log(message):
    symbol = "⋯"
    color = "dark_grey"
    pta(symbol, color, message)
def warning(message):
    symbol = "!"
    color = "yellow"
    pta(symbol, color, message)

def pta(tag, color, message):
    print(
        colored(f"{tag}", color, force_color=True)
        + " " +
        message
    )

def empty():
    print("")