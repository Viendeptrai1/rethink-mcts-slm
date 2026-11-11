import sys

def simple_exponential_notation(x):
    # Remove leading zeros
    x = x.lstrip('0')
    
    # Handle cases where x is less than 1
    if x.startswith('.'):
        x = '0' + x
    
    # Split the number into integer and fractional parts
    integer_part, _, fractional_part = x.partition('.')
    
    # Determine the exponent
    if integer_part != '0':
        exponent = len(integer_part) - 1
        mantissa = integer_part[0] + '.' + integer_part[1:] + fractional_part
    else:
        exponent = len(fractional_part) - fractional_part.find('1') - 1
        mantissa = '1.' + fractional_part[fractional_part.find('1') + 1:]
    
    # Remove trailing zeros from the mantissa
    mantissa = mantissa.rstrip('0')
    
    # Remove the decimal point if it's the last character
    if mantissa.endswith('.'):
        mantissa = mantissa[:-1]
    
    # Format the result
    if exponent == 0:
        return mantissa
    else:
        return f"{mantissa}E{exponent}"

# Read input from standard input
x = sys.stdin.read().strip()

# Print the result
print(simple_exponential_notation(x))