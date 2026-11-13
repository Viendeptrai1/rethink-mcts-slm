def strlen(string: str) -> int:
    if not string:
        return 0
    return 1 + strlen(string[1:])