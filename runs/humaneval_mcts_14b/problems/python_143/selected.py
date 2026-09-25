def words_in_sentence(sentence):
    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    result = []
    for word in sentence.split():
        if is_prime(len(word)):
            result.append(word)
    
    return ' '.join(result)

# Example usage:
# print(words_in_sentence("This is a test"))  # Output: "is"
# print(words_in_sentence("lets go for swimming"))  # Output: "go for"