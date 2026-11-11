def max_elements(p):
    p_str = str(p)
    n = len(p_str)
    
    # If p is a single digit, it can only be formed from itself
    if n == 1:
        return 1
    
    # Check if p can be formed by concatenating two smaller numbers
    for i in range(1, n):
        left = int(p_str[:i])
        right = int(p_str[i:])
        
        # Check if left >= right and if their concatenation forms p
        if left >= right and str(left) + str(right) == p_str:
            return 2
    
    # If no such pair is found, p must be formed from a single number repeated
    return 1

# Read input from stdin
import sys
p = int(sys.stdin.read().strip())

# Print the result
print(max_elements(p))