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
            # Calculate the new character index
            original_index = ord(char) - ord('a')
            new_index = (original_index + 4) % 26
            new_char = chr(new_index + ord('a'))
            result.append(new_char)
        else:
            # Non-alphabetic characters remain unchanged
            result.append(char)
    return ''.join(result)