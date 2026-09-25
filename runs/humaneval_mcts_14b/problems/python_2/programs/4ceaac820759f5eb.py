def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    an integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    """
    # Convert the number to a string
    number_str = str(number)
    
    # Split the string at the decimal point
    parts = number_str.split('.')
    
    # If there is no decimal part, return 0.0
    if len(parts) == 1:
        return 0.0
    
    # Convert the decimal part back to a float and return it
    decimal_part = float('0.' + parts[1])
    return decimal_part