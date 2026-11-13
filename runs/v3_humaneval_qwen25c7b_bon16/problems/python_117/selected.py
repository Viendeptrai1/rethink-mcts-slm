def select_words(s, n):
    if not s:
        return []

    words = s.split()
    vowels = "aeiouAEIOU"
    result = []

    for word in words:
        consonant_count = sum(1 for char in word if char.isalpha() and char not in vowels)
        if consonant_count == n:
            result.append(word)

    return result