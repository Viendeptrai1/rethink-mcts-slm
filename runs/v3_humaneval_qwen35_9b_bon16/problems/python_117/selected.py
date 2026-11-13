def select_words(s, n):
    vowels = set('aeiouAEIOU')
    consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
    
    words = s.split()
    result = []
    
    for word in words:
        count = sum(1 for char in word if char in consonants)
        if count == n:
            result.append(word)
    
    return result