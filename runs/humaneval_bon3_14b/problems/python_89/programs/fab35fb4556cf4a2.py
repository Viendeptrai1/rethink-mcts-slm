def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    """
    def shift_char(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 8) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 8) % 26 + ord('A'))
        else:
            return c

    return ''.join(shift_char(c) for c in s)

# Example usage:
# print(encrypt('hi'))  # Output: 'lm'
# print(encrypt('asdfghjkl'))  # Output: 'ewhjklnop'
# print(encrypt('gf'))  # Output: 'kj'
# print(encrypt('et'))  # Output: 'ix'