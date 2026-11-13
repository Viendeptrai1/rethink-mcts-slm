def is_sorted(lst):
    seen = set()
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
        if lst[i] == lst[i + 1]:
            if lst[i] in seen:
                return False
        seen.add(lst[i])
    return True