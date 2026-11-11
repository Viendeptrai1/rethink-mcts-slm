def select_words(s, n):
    vowels = set('aeiouAEIOU')
    result = []
    
    for word in s.split():
        consonant_count = sum(1 for char in word if char.isalpha() and char not in vowels)
        if consonant_count == n:
            result.append(word)
    
    return result