def get_closest_vowel(word):
    vowels = "aeiouAEIOU"
    length = len(word)
    
    # Start from the second last character and go backwards
    for i in range(length - 2, 0, -1):
        if word[i] in vowels and word[i-1] not in vowels and word[i+1] not in vowels:
            return word[i]
    
    return ""

# Example usage:
# print(get_closest_vowel("yogurt"))  # Output: "u"
# print(get_closest_vowel("FULL"))    # Output: "U"
# print(get_closest_vowel("quick"))   # Output: ""
# print(get_closest_vowel("ab"))      # Output: ""