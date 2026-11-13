def median(l: list) -> float:
    sorted_l = sorted(l)
    n = len(sorted_l)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2.0
    else:
        return sorted_l[mid]