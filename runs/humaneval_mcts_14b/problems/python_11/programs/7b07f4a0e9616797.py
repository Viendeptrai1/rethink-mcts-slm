from typing import List

def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    
    # Validate input lengths
    if len(a) != len(b):
        raise ValueError("Input strings must be of the same length.")
    
    # Validate input characters
    if not (set(a) <= {'0', '1'} and set(b) <= {'0', '1'}):
        raise ValueError("Input strings must consist only of '1's and '0's.")
    
    # Perform XOR operation
    result = []
    for char_a, char_b in zip(a, b):
        xor_result = '1' if char_a != char_b else '0'
        result.append(xor_result)
    
    return ''.join(result)