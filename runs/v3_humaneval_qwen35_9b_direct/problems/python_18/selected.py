def how_many_times(string: str, substring: str) -> int:
    if not substring:
        return 0
    count = 0
    start = 0
    while True:
        idx = string.find(substring, start)
        if idx == -1:
            break
        count += 1
        start = idx + 1
    return count