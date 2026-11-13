def pairs_sum_to_zero(l):
    seen = set()
    for num in l:
        complement = -num
        if complement in seen:
            return True
        seen.add(num)
    return False