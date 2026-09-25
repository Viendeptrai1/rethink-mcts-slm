def encode(message):
    def swap_case_and_shift_vowel(char):
        vowels = 'aeiouAEIOU'
        shifted_vowels = {
            'a': 'c', 'e': 'g', 'i': 'k', 'o': 'q', 'u': 'w',
            'A': 'C', 'E': 'G', 'I': 'K', 'O': 'Q', 'U': 'W'
        }
        
        if char.isalpha():
            if char in vowels:
                return shifted_vowels[char]
            else:
                return char.swapcase()
        return char

    encoded_message = ''.join(swap_case_and_shift_vowel(char) for char in message)
    return encoded_message

# Test cases
print(encode('test'))  # Output: 'TGST'
print(encode('This is a message'))  # Output: 'tHKS KS C MGSSCGG'