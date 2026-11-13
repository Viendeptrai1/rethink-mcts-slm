from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
    result = []
    for char_a, char_b in zip(a, b):
        val_a = int(char_a)
        val_b = int(char_b)
        xor_result = val_a ^ val_b
        result.append(str(xor_result))
    return ''.join(result)