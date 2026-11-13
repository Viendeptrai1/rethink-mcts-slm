def triples_sum_to_zero(l: list) -> bool:
    n = len(l)
    for i in range(n-2):
        seen = set()
        target = -l[i]
        for j in range(i+1, n):
            complement = target - l[j]
            if complement in seen:
                return True
            seen.add(l[j])
    return False