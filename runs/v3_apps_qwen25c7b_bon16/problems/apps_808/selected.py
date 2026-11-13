import sys

def simple_exponential_notation(x):
    # Convert the input string to a float
    num = float(x)
    
    # Format the number in scientific notation with 1 decimal place
    scientific = "{:.1e}".format(num)
    
    # Split the scientific notation into coefficient and exponent parts
    coeff, exp = scientific.split('e')
    
    # Remove trailing zeros from the coefficient
    coeff = coeff.rstrip('0')
    
    # Remove the decimal point if the coefficient is an integer
    coeff = coeff.rstrip('.')
    
    # Adjust the exponent accordingly
    exp = str(int(exp))
    
    # Construct the final result
    if int(exp) == 0:
        return coeff
    else:
        return f"{coeff}E{exp}"

# Read input from stdin
input_str = sys.stdin.read().strip()

# Get the result
result = simple_exponential_notation(input_str)

# Print the result
print(result)