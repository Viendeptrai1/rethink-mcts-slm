def to_simple_exponential_notation(x: str) -> str:
    # Remove leading and trailing whitespaces
    x = x.strip()
    
    # Determine the sign of the number
    sign = ''
    if x[0] == '-':
        sign = '-'
        x = x[1:]
    elif x[0] == '+':
        x = x[1:]
    
    # Split the number into integer and fractional parts
    if '.' in x:
        integer_part, fractional_part = x.split('.')
    else:
        integer_part, fractional_part = x, ''
    
    # Remove leading zeroes from integer part
    integer_part = integer_part.lstrip('0')
    if not integer_part:
        integer_part = '0'
    
    # Remove trailing zeroes from fractional part
    fractional_part = fractional_part.rstrip('0')
    
    # Combine integer and fractional parts
    if fractional_part:
        number = integer_part + '.' + fractional_part
    else:
        number = integer_part
    
    # Convert to float for exponentiation
    number = float(number)
    
    # Handle zero case
    if number == 0:
        return '0'
    
    # Determine the exponent
    import math
    exponent = math.floor(math.log10(abs(number)))
    
    # Normalize the number
    normalized_number = number / (10 ** exponent)
    
    # Format the normalized number
    if normalized_number.is_integer():
        normalized_number = int(normalized_number)
    
    # Construct the result
    if exponent == 0:
        result = f"{sign}{normalized_number}"
    else:
        result = f"{sign}{normalized_number}E{exponent}"
    
    return result

# Read input
x = input().strip()

# Get the result
result = to_simple_exponential_notation(x)

# Print the result
print(result)