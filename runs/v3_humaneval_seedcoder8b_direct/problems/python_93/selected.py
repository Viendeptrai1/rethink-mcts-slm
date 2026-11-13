def encode(message):
    vowels = 'aeiouAEIOU'
    vowel_shift = {v: chr((ord(v) - 97 + 2) % 26 + 97) for v in 'aeiou'}
    vowel_shift.update({v: chr((ord(v) - 65 + 2) % 26 + 65) for v in 'AEIOU'})
    
    result = []
    for char in message:
        if char.isalpha():
            if char in vowels:
                result.append(vowel_shift[char])
            else:
                result.append(char.swapcase())
        else:
            result.append(char)
    
    return ''.join(result)