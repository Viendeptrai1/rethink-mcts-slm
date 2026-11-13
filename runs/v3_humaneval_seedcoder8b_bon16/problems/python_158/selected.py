def find_max(words):
    if not words:
        return ""
    
    def unique_count(word):
        return len(set(word))
    
    max_unique = max(unique_count(word) for word in words)
    max_words = [word for word in words if unique_count(word) == max_unique]
    
    return min(max_words)