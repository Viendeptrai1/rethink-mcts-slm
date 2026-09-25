def select_words(s, n):
    vowels = set('aeiouAEIOU')
    result = []

    for word in s.split():
        consonant_count = sum(1 for char in word if char.isalpha() and char not in vowels)
        if consonant_count == n:
            result.append(word)

    return result

# Example usage:
# print(select_words("Mary had a little lamb", 4))  # Output: ["little"]
# print(select_words("Mary had a little lamb", 3))  # Output: ["Mary", "lamb"]
# print(select_words("simple white space", 2))     # Output: []
# print(select_words("Hello world", 4))            # Output: ["world"]
# print(select_words("Uncle sam", 3))              # Output: ["Uncle"]