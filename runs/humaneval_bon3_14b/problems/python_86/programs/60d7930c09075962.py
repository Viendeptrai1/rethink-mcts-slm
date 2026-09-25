def anti_shuffle(s):
    def sort_word(word):
        return ''.join(sorted(word))

    words = s.split(' ')
    sorted_words = [sort_word(word) for word in words]
    return ' '.join(sorted_words)

# Example usage:
# print(anti_shuffle('Hi'))  # Output: 'Hi'
# print(anti_shuffle('hello'))  # Output: 'ehllo'
# print(anti_shuffle('Hello World!!!'))  # Output: 'Hello !!!Wdlor'