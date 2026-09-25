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
    rotation = 4
    result = []
    
    for char in s:
        if 'a' <= char <= 'z':
            # Calculate the new character position with wrap-around using modulo
            new_char = chr((ord(char) - ord('a') + rotation) % 26 + ord('a'))
            result.append(new_char)
        else:
            # If the character is not a lowercase letter, leave it unchanged
            result.append(char)
    
    return ''.join(result)

# Example usage:
# print(encrypt('hi'))  # Output: 'lm'
# print(encrypt('asdfghjkl'))  # Output: 'ewhjklnop'
# print(encrypt('gf'))  # Output: 'kj'
# print(encrypt('et'))  # Output: 'ix'