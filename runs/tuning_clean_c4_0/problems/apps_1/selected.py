import sys

def max_digit_sum_number(x):
    x_str = str(x)
    n = len(x_str)
    
    # Start with the highest possible digit (9) and fill in the remaining places
    result = ['9'] * n
    
    # Adjust the result to ensure it does not exceed x
    for i in range(n):
        if int(''.join(result)) > x:
            result[i] = str(int(x_str[i]) - 1)
            result[i+1:] = ['9'] * (n - i - 1)
            break
    
    # Convert list to string and remove leading zeros
    result_str = ''.join(result).lstrip('0')
    
    # If the result is empty, it means x was 0, but since x is at least 1, this won't happen
    return result_str if result_str else '0'

# Read input from standard input
x = int(sys.stdin.read().strip())

# Print the result
print(max_digit_sum_number(x))