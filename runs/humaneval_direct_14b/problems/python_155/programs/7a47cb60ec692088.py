def even_odd_count(num):
    """Given an integer, return a tuple that has the number of even and odd digits respectively.

    Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """
    # Convert the number to a string and remove the negative sign if present
    num_str = str(abs(num))
    
    # Initialize counters for even and odd digits
    even_count = 0
    odd_count = 0
    
    # Iterate over each character in the string
    for char in num_str:
        digit = int(char)
        if digit % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    
    # Return the counts as a tuple
    return (even_count, odd_count)