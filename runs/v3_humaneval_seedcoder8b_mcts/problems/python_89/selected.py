def encrypt(s):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    rotated = alphabet[4:] + alphabet[:4]
    trans = str.maketrans(alphabet, rotated)
    return s.translate(trans)