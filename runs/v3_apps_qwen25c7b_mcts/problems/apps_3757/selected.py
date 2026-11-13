def find_string(a_00, a_01, a_10, a_11):
    # Check for consistency
    if a_00 + a_01 != a_10 + a_11:
        return "Impossible"
    
    # Construct the string
    result = []
    while a_01 > 0:
        result.append('0')
        result.append('1')
        a_01 -= 1
    
    while a_10 > 0:
        result.append('1')
        result.append('0')
        a_10 -= 1
    
    # If there are remaining a_00 or a_11, add them
    if a_00 > 0:
        result.extend(['0'] * a_00)
    elif a_11 > 0:
        result.extend(['1'] * a_11)
    
    return ''.join(result)

# Example usage
import sys
input = sys.stdin.read
data = input().split()
a_00 = int(data[0])
a_01 = int(data[1])
a_10 = int(data[2])
a_11 = int(data[3])

print(find_string(a_00, a_01, a_10, a_11))