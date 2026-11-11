def encrypt(s):
    def rotate_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 8) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 8) % 26 + ord('A'))
        else:
            return c

    return ''.join(rotate_char(c) for c in s)