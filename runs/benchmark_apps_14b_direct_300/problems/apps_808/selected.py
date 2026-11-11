import sys

def simple_exponential_notation(x):
    # Remove leading zeros
    x = x.lstrip('0')
    
    # Handle the case where x is a whole number
    if '.' not in x:
        x += '.'
    
    # Find the position of the decimal point
    decimal_pos = x.index('.')
    
    # Determine the exponent b
    if decimal_pos == 0:
        # Case where x is less than 1
        b = -1
        while x[0] == '0':
            x = x[1:]
            b -= 1
    else:
        # Case where x is greater than or equal to 1
        b = decimal_pos - 1
    
    # Adjust the mantissa a
    a = x[0]
    if decimal_pos > 1:
        a += x[1:decimal_pos]
    elif decimal_pos < len(x) - 1:
        a += x[decimal_pos+1:]
    
    # Remove trailing zeros from a
    a = a.rstrip('0')
    
    # Remove decimal point if a is an integer
    if '.' in a:
        a = a.rstrip('.')
    
    # Construct the result
    if b == 0:
        return a
    else:
        return f"{a}E{b}"

# Read input from stdin
x = sys.stdin.read().strip()

# Print the result
print(simple_exponential_notation(x))