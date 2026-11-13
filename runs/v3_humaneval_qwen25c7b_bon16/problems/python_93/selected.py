def encode(message):
    vowels = 'aeiou'
    mapping = {v: chr((ord(v) - ord('a') + 2) % 26 + ord('a')) for v in vowels}
    mapping.update({k.upper(): v.upper() for k, v in mapping.items()})
    
    def swap_case(c):
        if c.isalpha():
            return c.swapcase()
        return c
    
    return ''.join(mapping.get(swap_case(c), swap_case(c)) for c in message)