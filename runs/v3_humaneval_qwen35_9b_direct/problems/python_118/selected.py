def get_closest_vowel(word):
    vowels = set("aeiouAEIOU")
    n = len(word)
    
    # Find the first consonant from the left (index 0)
    left_consonant_idx = -1
    for i in range(n):
        if word[i] not in vowels:
            left_consonant_idx = i
            break
    
    if left_consonant_idx == -1:
        return ""
    
    # Find the last consonant from the right (index n-1)
    right_consonant_idx = -1
    for i in range(n - 1, -1, -1):
        if word[i] not in vowels:
            right_consonant_idx = i
            break
    
    if right_consonant_idx == -1:
        return ""
    
    # Check if there is at least one character between the two consonants
    if right_consonant_idx <= left_consonant_idx + 1:
        return ""
    
    # Search for the closest vowel between the two consonants from the right side
    # We start from the right_consonant_idx - 1 and move left until we hit left_consonant_idx
    for i in range(right_consonant_idx - 1, left_consonant_idx, -1):
        if word[i] in vowels:
            return word[i]
    
    return ""