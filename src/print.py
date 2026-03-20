from termcolor import colored

def success(m):
    s = "✓"
    c = "green"
    pta(s, c, m)
def error(m):
    s = "✗"
    c = "light_red"
    pta(s, c, m)
def log(m):
    s = "⋯"
    c = "dark_grey"
    pta(s, c, m)
def warning(m):
    s = "!"
    c = "yellow"
    pta(s, c, m)

def pta(t, c, m):
    print(
        colored(f"{t}", c, force_color=True)
        + " " +
        m
    )

def empty():
    print("")