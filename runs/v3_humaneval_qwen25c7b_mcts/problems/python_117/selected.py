def select_words(s, n):
    if not s:
        return []

    words = s.split()
    result = []

    for word in words:
        consonant_count = sum(1 for char in word.lower() if char.isalpha() and char not in 'aeiou')
        if consonant_count == n:
            result.append(word)

    return result