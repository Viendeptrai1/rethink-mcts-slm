def encode(message):
    def shift_vowel(c):
        vowels = 'aeiouAEIOU'
        if c in vowels:
            if c.islower():
                return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            else:
                return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c

    encoded_message = ''.join(shift_vowel(c).swapcase() if c.isalpha() else c for c in message)
    return encoded_message

# Example usage:
# print(encode('test'))  # Output: 'TGST'
# print(encode('This is a message'))  # Output: 'tHKS KS C MGSSCGG'