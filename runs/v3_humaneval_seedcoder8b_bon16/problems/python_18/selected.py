def how_many_times(string: str, substring: str) -> int:
    if not string or not substring:
        return 0
    
    count = 0
    start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            return count
        count += 1
        start += 1