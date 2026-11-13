def construct_string(a00, a01, a10, a11):
    # Check if it's possible to form the string
    if (a00 + a01 != a10) or (a00 + a10 != a11) or (a01 + a10 != a00) or (a01 + a11 != a00):
        return "Impossible"
    
    # Construct the string
    result = []
    if a00 > 0:
        result.append('0')
        result.append('0')
        a00 -= 1
    
    while a01 > 0:
        result.append('0')
        result.append('1')
        a01 -= 1
    
    while a10 > 0:
        result.append('1')
        result.append('0')
        a10 -= 1
    
    while a11 > 0:
        result.append('1')
        result.append('1')
        a11 -= 1
    
    return ''.join(result)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
a00, a01, a10, a11 = int(data[0]), int(data[1]), int(data[2]), int(data[3])
print(construct_string(a00, a01, a10, a11))