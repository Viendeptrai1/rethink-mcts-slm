def select_words(s, n):
    def count_consonants(word):
        vowels = "aeiouAEIOU"
        return sum(1 for char in word if char.isalpha() and char not in vowels)
    
    if not s:
        return []
    
    words = s.split()
    result = [word for word in words if count_consonants(word) == n]
    
    return result