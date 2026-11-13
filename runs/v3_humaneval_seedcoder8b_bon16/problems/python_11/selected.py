from typing import List

def string_xor(a: str, b: str) -> str:
    result = []
    for i in range(len(a)):
        # XOR the corresponding bits from a and b
        result.append(str(int(a[i]) ^ int(b[i])))
    return ''.join(result)