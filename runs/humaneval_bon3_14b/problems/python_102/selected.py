def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.
    """
    if x > y:
        return -1
    
    # Start from the largest number in the range and go downwards
    for num in range(y, x - 1, -1):
        if num % 2 == 0:
            return num
    
    return -1

# Example usage:
# print(choose_num(12, 15))  # Output: 14
# print(choose_num(13, 12))  # Output: -1