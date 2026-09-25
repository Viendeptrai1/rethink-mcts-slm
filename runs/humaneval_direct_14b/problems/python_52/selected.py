def below_threshold(l: list, t: int) -> bool:
    return all(x < t for x in l)