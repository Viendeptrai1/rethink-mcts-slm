def vowels_count(s):
    vowels = set('aeiouAEIOU')
    count = 0
    for i, char in enumerate(s):
        if char in vowels:
            count += 1
        elif char == 'y' or char == 'Y':
            if i == len(s) - 1:
                count += 1
    return count