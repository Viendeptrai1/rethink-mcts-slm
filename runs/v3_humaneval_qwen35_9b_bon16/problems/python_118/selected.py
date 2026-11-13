def get_closest_vowel(word):
    """You are given a word. Your task is to find the closest vowel that stands between 
    two consonants from the right side of the word (case sensitive).
    
    Vowels in the beginning and ending doesn't count. Return empty string if you didn't
    find any vowel met the above condition. 

    You may assume that the given string contains English letter only.
    """
    vowels = set("aeiouAEIOU")
    
    # Find the first vowel from the right that is not the last character
    # and check if it has a consonant immediately to its right
    n = len(word)
    
    # We need to find a vowel at index i such that:
    # 1. i is not 0 (beginning)
    # 2. i is not n-1 (ending)
    # 3. word[i] is a vowel
    # 4. word[i+1] is a consonant
    # Among all such vowels, we want the one closest to the right, which means the largest index i.
    # However, the problem says "closest vowel that stands between two consonants from the right side".
    # This phrasing is a bit ambiguous. Let's re-read: "find the closest vowel that stands between two consonants from the right side of the word".
    # This likely means we scan from the right and find the first vowel that is preceded by a consonant and followed by a consonant? 
    # Or simply: find a vowel between two consonants, and among those, pick the one closest to the right end.
    
    # Let's re-examine the example: "yogurt" -> "u"
    # y (consonant), o (vowel), g (consonant), u (vowel), r (consonant), t (consonant)
    # Vowels are 'o' and 'u'.
    # 'o' is between 'y' and 'g' (both consonants).
    # 'u' is between 'g' and 'r' (both consonants).
    # Both are between two consonants. Which one is returned? "u".
    # "u" is closer to the right than "o". So we want the rightmost vowel that is between two consonants.
    
    # Example: "quick" -> ""
    # q (c), u (v), i (v), c (c), k (c)
    # 'u' is between 'q' and 'i' (i is vowel, not consonant) -> not between two consonants.
    # 'i' is between 'u' and 'c' (u is vowel) -> not between two consonants.
    # So no vowel is between two consonants.
    
    # Example: "ab" -> ""
    # a (v), b (c). 'a' is at beginning, so doesn't count.
    
    # So the algorithm is:
    # Iterate through the string from left to right (or right to left, but we want the rightmost).
    # Actually, we just need to find all vowels that are between two consonants (i.e., word[i-1] is consonant and word[i+1] is consonant).
    # Then pick the one with the largest index.
    
    candidates = []
    
    for i in range(1, n - 1):
        if word[i] in vowels:
            if word[i-1] not in vowels and word[i+1] not in vowels:
                candidates.append(i)
    
    if not candidates:
        return ""
    
    # Return the character at the largest index found
    return word[max(candidates)]