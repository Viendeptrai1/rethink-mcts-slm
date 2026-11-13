def encode(message):
    def shift_vowel(char):
        vowels = 'aeiouAEIOU'
        if char in vowels:
            if char.islower():
                return chr((ord(char) - ord('a') + 2) % 26 + ord('a'))
            else:
                return chr((ord(char) - ord('A') + 2) % 26 + ord('A'))
        return char

    encoded_message = []
    for char in message:
        if char.isalpha():
            shifted_char = shift_vowel(char)
            encoded_message.append(shifted_char.swapcase())
        else:
            encoded_message.append(char)

    return ''.join(encoded_message)