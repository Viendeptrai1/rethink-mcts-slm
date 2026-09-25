def is_sorted(lst):
    '''
    Given a list of numbers, return whether or not they are sorted
    in ascending order. If list has more than 1 duplicate of the same
    number, return False. Assume no negative numbers and only integers.
    '''
    if len(lst) <= 1:
        return True

    previous = lst[0]
    duplicate_count = 1

    for i in range(1, len(lst)):
        if lst[i] < previous:
            return False
        if lst[i] == previous:
            duplicate_count += 1
            if duplicate_count > 2:
                return False
        else:
            duplicate_count = 1
        previous = lst[i]

    return True