from decimal import Decimal, getcontext

def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    an integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    # Set precision high enough to handle typical floating point operations
    getcontext().prec = 28
    
    # Convert the number to Decimal for high precision arithmetic
    decimal_number = Decimal(str(number))
    
    # Get the integer part
    integer_part = decimal_number.to_integral_value()
    
    # Subtract the integer part from the original number to get the decimal part
    decimal_part = decimal_number - integer_part
    
    # Convert the result back to float
    return float(decimal_part)