def to_simple_exponential_notation(x: str) -> str:
    import decimal
    from decimal import Decimal

    # Set the precision to handle large numbers
    decimal.getcontext().prec = 1000

    # Convert the input string to a Decimal
    x_decimal = Decimal(x)

    # Convert the Decimal to a string in scientific notation
    scientific_notation = f"{x_decimal:.1000e}"

    # Split the scientific notation into coefficient and exponent
    coefficient, exponent = scientific_notation.split('e')
    exponent = int(exponent)

    # Remove trailing zeros from the coefficient
    coefficient = coefficient.rstrip('0').rstrip('.')

    # If the coefficient is an integer, remove the decimal point
    if '.' in coefficient:
        if coefficient.endswith('.'):
            coefficient = coefficient[:-1]
    else:
        coefficient = coefficient

    # If the exponent is zero, return just the coefficient
    if exponent == 0:
        return coefficient

    # Construct the simple exponential notation
    return f"{coefficient}E{exponent}"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    result = to_simple_exponential_notation(input)
    print(result)