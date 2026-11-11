def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    """
    rotation = 2 * 2  # The rotation factor is 4
    encrypted_string = ""
    
    for char in s:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            rotated_char = chr((ord(char) - base + rotation) % 26 + base)
            encrypted_string += rotated_char
        else:
            encrypted_string += char
    
    return encrypted_string