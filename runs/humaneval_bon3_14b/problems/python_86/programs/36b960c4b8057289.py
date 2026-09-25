def anti_shuffle(s):
    def sort_word(word):
        return ''.join(sorted(word))

    result = []
    for word in s.split(' '):
        sorted_word = sort_word(word)
        result.append(sorted_word)

    return ' '.join(result)

# Example usage:
# print(anti_shuffle('Hi'))  # Output: 'Hi'
# print(anti_shuffle('hello'))  # Output: 'ehllo'
# print(anti_shuffle('Hello World!!!'))  # Output: 'Hello !!!Wdlor'