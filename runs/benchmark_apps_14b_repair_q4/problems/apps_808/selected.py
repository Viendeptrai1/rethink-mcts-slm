import sys

def simple_exponential_notation(x):
    # Remove leading zeros
    x = x.lstrip('0')
    
    # Check if the number is less than 1
    if '.' in x:
        decimal_point_index = x.index('.')
        if decimal_point_index == 0:
            # Number is less than 1, find the first non-zero digit
            for i in range(1, len(x)):
                if x[i] != '0':
                    a = x[i]
                    b = -(i - 1)
                    break
            else:
                # All digits after decimal point are zero
                a = '1'
                b = 0
        else:
            # Number is greater than or equal to 1
            a = x[:decimal_point_index] + '.' + x[decimal_point_index+1:].rstrip('0')
            b = decimal_point_index - 1
    else:
        # Number is an integer
        a = x.rstrip('0')
        b = len(a) - 1
        if b > 0:
            a = a[0] + '.' + a[1:]
    
    # Format the result
    if b == 0:
        return a
    elif '.' in a and a.endswith('.'):
        a = a[:-1]
    return f"{a}E{b}"

# Read input from stdin
x = sys.stdin.read().strip()

# Print the result
print(simple_exponential_notation(x))