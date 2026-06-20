def convertNameToID(name: str) -> str:
    return "".join(
        c.lower() if c.isalnum() else "-" if c == " " else ""
        for c in name
    ).strip("-")