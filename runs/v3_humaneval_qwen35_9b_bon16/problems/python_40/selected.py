def triples_sum_to_zero(l: list):
    """
    triples_sum_to_zero takes a list of integers as an input.
    it returns True if there are three distinct elements in the list that
    sum to zero, and False otherwise.
    """
    s = set(l)
    if len(s) < 3:
        return False
    for i in s:
        for j in s:
            if j == i:
                continue
            if (-i - j) in s:
                return True
    return False