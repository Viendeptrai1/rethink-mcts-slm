def find_max(words):
    if not words:
        return ""
    
    max_unique_count = -1
    result_word = ""
    
    for word in words:
        unique_chars = len(set(word))
        if unique_chars > max_unique_count:
            max_unique_count = unique_chars
            result_word = word
        elif unique_chars == max_unique_count:
            if word < result_word:
                result_word = word
                
    return result_word