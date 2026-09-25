def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlapping cases. """
    count = start = 0
    while True:
        start = string.find(substring, start)
        if start == -1:
            break
        count += 1
        start += 1
    return count

# Test cases
print(how_many_times('', 'a'))  # Output: 0
print(how_many_times('aaa', 'a'))  # Output: 3
print(how_many_times('aaaa', 'aa'))  # Output: 3