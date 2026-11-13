def triples_sum_to_zero(l: list) -> bool:
    n = len(l)
    for i in range(n-2):
        seen = set()
        target = -l[i]
        for j in range(i+1, n):
            if target - l[j] in seen:
                return True
            seen.add(l[j])
    return False