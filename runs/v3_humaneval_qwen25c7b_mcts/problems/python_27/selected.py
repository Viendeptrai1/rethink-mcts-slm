def flip_case(s: str) -> str:
    return ''.join(c.lower() if c.isupper() else c.upper() for c in s)