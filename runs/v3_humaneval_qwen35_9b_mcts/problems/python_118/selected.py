def get_closest_vowel(word):
    vowels = set("aeiouAEIOU")
    n = len(word)
    
    # Scan from right to left
    for i in range(n - 1, 0, -1):
        # Check if current character is a vowel
        if word[i] in vowels:
            # Check if the character to the right is a consonant
            if i < n - 1 and word[i + 1] not in vowels:
                # Check if the character to the left is a consonant
                if i > 0 and word[i - 1] not in vowels:
                    return word[i]
    
    return ""