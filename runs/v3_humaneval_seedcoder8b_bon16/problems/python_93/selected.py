def encode(message):
    vowels = 'aeiou'
    result = ''
    for char in message:
        if char.isalpha():
            if char.lower() in vowels:
                new_char = chr((ord(char.lower()) - ord('a') + 2) % 26 + ord('a'))
            else:
                new_char = char.swapcase()
            result += new_char
        else:
            result += char
    return result.upper()