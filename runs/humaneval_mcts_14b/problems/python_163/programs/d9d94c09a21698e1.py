def generate_integers(a, b):
    """
    Given two positive integers a and b, return the even digits between a
    and b, in ascending order.

    For example:
    generate_integers(2, 8) => [2, 4, 6, 8]
    generate_integers(8, 2) => [2, 4, 6, 8]
    generate_integers(10, 14) => []
    """
    # Define the set of single-digit even numbers
    even_digits = {0, 2, 4, 6, 8}
    
    # Determine the range boundaries
    start = min(a, b)
    end = max(a, b)
    
    # Filter the even digits that fall within the range
    result = [digit for digit in even_digits if start <= digit <= end]
    
    return result