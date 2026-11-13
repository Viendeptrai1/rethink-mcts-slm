def string_xor(a: str, b: str) -> str:
    # Use zip to iterate over pairs of characters from both strings
    # Convert each pair to integers (0 or 1), perform XOR operation, 
    # convert the result back to a character ('0' or '1'), and join the results into a single string
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))