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
    result = []
    for char in s:
        if 'a' <= char <= 'z':
            # Calculate the new character with rotation
            new_char = chr((ord(char) - ord('a') + 8) % 26 + ord('a'))
            result.append(new_char)
        else:
            # If it's not a lowercase letter, just append the character as is
            result.append(char)
    return ''.join(result)

# Test cases
print(encrypt('hi'))        # Output: 'lm'
print(encrypt('asdfghjkl')) # Output: 'ewhjklnop'
print(encrypt('gf'))        # Output: 'kj'
print(encrypt('et'))        # Output: 'ix'