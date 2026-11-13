def pairs_sum_to_zero(lst):
    seen = set()
    for num in lst:
        if -num in seen:
            return True
        seen.add(num)
    return False