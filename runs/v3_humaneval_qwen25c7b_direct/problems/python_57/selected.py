def monotonic(l: list) -> bool:
    return l == sorted(l) or l == sorted(l, reverse=True)