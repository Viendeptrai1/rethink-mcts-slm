def even_odd_count(num):
    """Given an integer. return a tuple that has the number of even and odd digits respectively.

     Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """
    count_even = 0
    count_odd = 0

    # Convert number to string and handle negative sign
    num_str = str(num)
    
    # Iterate over each character in the string
    for char in num_str:
        # Skip the negative sign if present
        if char == '-':
            continue
        
        digit = int(char)
        if digit % 2 == 0:
            count_even += 1
        else:
            count_odd += 1
            
    return (count_even, count_odd)