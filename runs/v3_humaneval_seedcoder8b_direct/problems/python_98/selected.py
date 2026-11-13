def count_upper(s):
    count = 0
    vowels = set('AEIOU')
    for i in range(0, len(s), 2):
        if s[i] in vowels:
            count += 1
    return count