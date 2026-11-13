def encrypt(s):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    rotated = alphabet[4:] + alphabet[:4]
    return ''.join(rotated[alphabet.index(c)] for c in s.lower())