def encrypt(s):
    def rotate_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + (2 * 2)) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + (2 * 2)) % 26 + ord('A'))
        else:
            return c

    return ''.join(rotate_char(c) for c in s)

# Example usage:
# print(encrypt('hi'))  # Output: 'lm'
# print(encrypt('asdfghjkl'))  # Output: 'ewhjklnop'
# print(encrypt('gf'))  # Output: 'kj'
# print(encrypt('et'))  # Output: 'ix'