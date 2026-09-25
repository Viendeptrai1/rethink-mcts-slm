def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlapping cases. """
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

# Test cases
print(how_many_times('', 'a'))  # Output: 0
print(how_many_times('aaa', 'a'))  # Output: 3
print(how_many_times('aaaa', 'aa'))  # Output: 3