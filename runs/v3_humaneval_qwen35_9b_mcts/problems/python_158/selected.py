def find_max(words):
    if not words:
        return ""
    
    max_unique_count = -1
    result_word = ""
    
    for word in words:
        unique_count = len(set(word))
        
        if unique_count > max_unique_count:
            max_unique_count = unique_count
            result_word = word
        elif unique_count == max_unique_count:
            if word < result_word:
                result_word = word
                
    return result_word