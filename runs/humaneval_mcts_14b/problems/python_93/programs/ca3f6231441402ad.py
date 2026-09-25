def encode(message):
    def shift_vowel(c):
        vowels = 'aeiouAEIOU'
        if c in vowels:
            if c.islower():
                return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
            else:
                return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c

    encoded_message = []
    for char in message:
        if char.isalpha():
            # Swap case
            swapped_char = char.lower() if char.isupper() else char.upper()
            # Shift vowel if applicable
            encoded_char = shift_vowel(swapped_char)
            encoded_message.append(encoded_char)
        else:
            encoded_message.append(char)

    return ''.join(encoded_message)

# Test cases
print(encode('test'))  # Output: 'TGST'
print(encode('This is a message'))  # Output: 'tHKS KS C MGSSCGG'