def find_max(words):
    def unique_char_count(word):
        return len(set(word))
    
    max_word = ""
    max_unique_chars = 0
    
    for word in words:
        unique_count = unique_char_count(word)
        if (unique_count > max_unique_chars) or (unique_count == max_unique_chars and word < max_word):
            max_word = word
            max_unique_chars = unique_count
    
    return max_word

# Test cases
print(find_max(["name", "of", "string"]))  # Output: "string"
print(find_max(["name", "enam", "game"]))  # Output: "enam"
print(find_max(["aaaaaaa", "bb", "cc"]))   # Output: "aaaaaaa"