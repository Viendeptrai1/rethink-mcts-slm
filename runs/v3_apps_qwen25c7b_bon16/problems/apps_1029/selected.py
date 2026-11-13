def max_elements(p):
    result = 1
    while p >= 10:
        digit = p % 10
        if p >= 10 * digit:
            p //= 10
            result += 1
        else:
            break
    return result

# Reading input from stdin
import sys
input = sys.stdin.read().strip()
p = int(input)

# Printing the result
print(max_elements(p))