def vowels_count(s):
    if not s:
        return 0
    
    vowels = set('aeiouAEIOU')
    count = sum(1 for char in s if char in vowels)
    
    if s[-1].lower() == 'y':
        count += 1
    
    return count