def to_simple_exponential_notation(x):
    import decimal
    from decimal import Decimal
    
    # Set the precision to handle very large numbers
    decimal.getcontext().prec = len(x) + 10  # Add some extra precision to avoid rounding issues
    x = Decimal(x)
    
    if x == 0:
        return "0"
    
    # Determine the exponent b
    b = 0
    while x >= 10:
        x /= 10
        b += 1
    while x < 1:
        x *= 10
        b -= 1
    
    # Convert x to a string and strip trailing zeros
    a_str = str(x.normalize())
    
    # Remove the decimal point if a is an integer
    if a_str.endswith('.'):
        a_str = a_str[:-1]
    
    # If b is zero, we just return a
    if b == 0:
        return a_str
    
    return f"{a_str}E{b}"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = to_simple_exponential_notation(input)
    print(result)