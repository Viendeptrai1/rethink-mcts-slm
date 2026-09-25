import sys

def min_moves_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for '00', '25', '50', '75' at the end of the string
    for i in range(length - 1, -1, -1):
        if n_str[i] == '0':
            for j in range(i - 1, -1, -1):
                if n_str[j] == '0' or n_str[j] == '5':
                    return length - 1 - j
        elif n_str[i] == '5':
            for j in range(i - 1, -1, -1):
                if n_str[j] == '2' or n_str[j] == '7':
                    return length - 1 - j
    
    return -1

# Read input
n = int(sys.stdin.read().strip())

# Output the result
print(min_moves_to_divisible_by_25(n))