import math

def simple_exponential_notation(x):
    # Convert input string to float
    num = float(x)
    
    # Handle special cases
    if num == 0:
        return "0"
    elif num >= 10:
        exp = int(math.floor(math.log10(num)))
        a = num / (10 ** exp)
    else:
        exp = -int(math.ceil(math.log10(abs(num))))
        a = num * (10 ** (-exp))
    
    # Format the result
    if exp != 0:
        return f"{a:.{abs(exp)}f}E{exp}"
    else:
        return f"{a:.0f}"

# Read input from stdin
x = input().strip()

# Print the result
print(simple_exponential_notation(x))