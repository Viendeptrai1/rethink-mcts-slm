def generate_integers(a, b):
    # Ensure a is less than or equal to b
    if a > b:
        a, b = b, a
    
    # Initialize an empty list to store even digits
    even_digits = []
    
    # Start from the first even number greater than or equal to a
    start = a if a % 2 == 0 else a + 1
    
    # Iterate through the range, stepping by 2 to get only even numbers
    for num in range(start, b + 1, 2):
        even_digits.append(num)
    
    return even_digits