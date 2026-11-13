def vowels_count(s):
    vowels = set('aeiouAEIOU')
    count = sum(1 for char in s if char in vowels)
    
    if s and s[-1].lower() == 'y':
        count += 1
    
    return count