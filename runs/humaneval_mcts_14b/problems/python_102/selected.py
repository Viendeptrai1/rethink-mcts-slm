def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.
    """
    # Step 1: Check if the input values x and y are valid
    if not (isinstance(x, int) and isinstance(y, int) and x > 0 and y > 0 and x <= y):
        return -1
    
    # Step 2: Find the largest even number in the range [x, y]
    for num in range(y, x - 1, -1):
        if num % 2 == 0:
            return num
    
    # If no even number is found, return -1
    return -1

# Example usage:
# print(choose_num(12, 15))  # Output: 14
# print(choose_num(13, 12))  # Output: -1