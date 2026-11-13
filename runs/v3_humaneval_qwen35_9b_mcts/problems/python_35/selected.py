def max_element(l: list):
    """Return maximum element in the list.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """
    if not l:
        raise ValueError("max() arg is an empty sequence")
    
    def _max_recursive(lst):
        if len(lst) == 1:
            return lst[0]
        mid = len(lst) // 2
        left_max = _max_recursive(lst[:mid])
        right_max = _max_recursive(lst[mid:])
        return left_max if left_max > right_max else right_max
    
    return _max_recursive(l)