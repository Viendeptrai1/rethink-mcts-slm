def vowels_count(s):
    vowels = set('aeiouAEIOU')
    count = sum(1 for char in s if char in vowels)
    if s.endswith('y') or s.endswith('Y'):
        count += 1
    return count