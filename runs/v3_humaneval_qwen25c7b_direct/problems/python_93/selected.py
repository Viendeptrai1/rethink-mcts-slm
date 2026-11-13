def encode(message):
    vowels = "aeiou"
    shifted_vowels = {v: chr((ord(v) - ord('a') + 2) % 26 + ord('a')) for v in vowels}
    shifted_vowels.update({v.upper(): shifted_vowels[v].upper() for v in vowels})
    
    def swap_case_and_shift(c):
        if c.isalpha():
            swapped = c.swapcase()
            return shifted_vowels.get(swapped, swapped)
        else:
            return c
    
    return ''.join(swap_case_and_shift(c) for c in message)