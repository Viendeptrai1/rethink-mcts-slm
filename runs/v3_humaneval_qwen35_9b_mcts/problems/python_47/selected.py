def median(l: list):
    sorted_l = sorted(l)
    n = len(sorted_l)
    if n % 2 == 1:
        return sorted_l[n // 2]
    else:
        mid1 = sorted_l[n // 2 - 1]
        mid2 = sorted_l[n // 2]
        return (mid1 + mid2) / 2