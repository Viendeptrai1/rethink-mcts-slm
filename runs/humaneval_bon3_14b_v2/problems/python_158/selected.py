def find_max(words):
    if not words:
        return ""
    
    max_unique_count = 0
    result_word = ""
    
    for word in words:
        unique_chars = set(word)
        unique_count = len(unique_chars)
        
        if unique_count > max_unique_count or (unique_count == max_unique_count and word < result_word):
            max_unique_count = unique_count
            result_word = word
    
    return result_word