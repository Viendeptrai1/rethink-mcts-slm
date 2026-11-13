def unique_digits(x):
    """Given a list of positive integers x. return a sorted list of all 
    elements that hasn't any even digit.

    Note: Returned list should be sorted in increasing order.
    
    For example:
    >>> unique_digits([15, 33, 1422, 1])
    [1, 15, 33]
    >>> unique_digits([152, 323, 1422, 10])
    []
    """
    result = []
    for num in x:
        has_even = False
        temp = num
        while temp > 0:
            digit = temp % 10
            if digit % 2 == 0:
                has_even = True
                break
            temp = temp // 10
        if not has_even:
            result.append(num)
    result.sort()
    return result