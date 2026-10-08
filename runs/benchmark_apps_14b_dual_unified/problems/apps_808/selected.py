import sys

def simple_exponential_notation(x):
    # Remove leading zeros
    x = x.lstrip('0')
    
    # Check if the number is an integer
    if '.' not in x:
        x += '.'
    
    # Split the number into integer and fractional parts
    integer_part, fractional_part = x.split('.')
    
    # Initialize a and b
    a = float(integer_part + '.' + fractional_part)
    b = 0
    
    # Adjust a and b to fit the format 1 <= a < 10
    while a >= 10:
        a /= 10
        b += 1
    while a < 1:
        a *= 10
        b -= 1
    
    # Format the result
    if b == 0:
        return f"{int(a) if a.is_integer() else a:.15g}"
    else:
        return f"{int(a) if a.is_integer() else a:.15g}E{b}"

# Read input from stdin
x = sys.stdin.read().strip()

# Print the result
print(simple_exponential_notation(x))