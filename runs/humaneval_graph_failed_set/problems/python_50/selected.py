def decode_shift(s: str) -> str:
    """
    Decodes a string that was encoded with the encode_shift function by shifting
    every character back by 5 positions in the alphabet.
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string.")
    
    decoded_chars = []
    for ch in s:
        if not ('a' <= ch <= 'z'):
            raise ValueError("Input string must contain only lowercase alphabetic characters.")
        
        # Calculate the new character by shifting back by 5 positions
        new_char = chr(((ord(ch) - ord("a") - 5) % 26) + ord("a"))
        decoded_chars.append(new_char)
    
    return "".join(decoded_chars)