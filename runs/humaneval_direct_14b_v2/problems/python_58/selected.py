def common(l1: list, l2: list) -> list:
    return sorted(set(l1) & set(l2))