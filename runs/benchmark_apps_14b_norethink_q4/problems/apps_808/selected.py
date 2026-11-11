import sys

def simple_exponential_notation(x):
    # Remove leading zeros
    x = x.lstrip('0')
    
    # Find the position of the decimal point
    decimal_pos = x.find('.')
    
    if decimal_pos == -1:
        # No decimal point, it's an integer
        if len(x) == 1:
            return x
        else:
            return x[0] + '.' + x[1:] + 'E' + str(len(x) - 1)
    
    # Remove trailing zeros after the decimal point
    x = x.rstrip('0')
    
    # If all digits are zeros after removing trailing zeros, it becomes zero
    if decimal_pos == len(x):
        return '0'
    
    # Calculate the exponent b
    if decimal_pos == 0:
        # Decimal point at the start, move it to the right
        b = 0
        while x[b + 1] == '0':
            b -= 1
        a = x[b + 1]
        if len(x) > b + 2:
            a += '.' + x[b + 2:]
        return a + 'E' + str(b)
    elif decimal_pos == 1:
        # Decimal point after the first digit, no need for exponent
        a = x[0] + '.' + x[2:]
        return a
    else:
        # Decimal point somewhere else, calculate the exponent
        a = x[0] + '.' + x[2:decimal_pos]
        b = decimal_pos - 1
        return a + 'E' + str(b)

# Read input from stdin
x = sys.stdin.read().strip()

# Print the result
print(simple_exponential_notation(x))