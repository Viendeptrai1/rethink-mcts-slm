def how_many_times(string: str, substring: str) -> int:
    if not substring:
        return 0
    
    count = 0
    start = 0
    while start <= len(string) - len(substring):
        pos = string.find(substring, start)
        if pos != -1:
            count += 1
            start = pos + 1
        else:
            break
    return count