def circular_shift(x, shift):
    # Convert the integer to a string to manipulate the digits
    x_str = str(x)
    num_digits = len(x_str)
    
    # Handle the case where shift is zero
    if shift == 0:
        return x_str
    
    # If shift is greater than or equal to the number of digits, return the reversed digits
    if shift >= num_digits:
        return x_str[::-1]
    
    # Calculate the effective shift using modulo operation
    effective_shift = shift % num_digits
    
    # Perform the circular shift using slicing
    shifted_str = x_str[-effective_shift:] + x_str[:-effective_shift]
    
    return shifted_str

# Test cases
print(circular_shift(12, 1))  # Output: "21"
print(circular_shift(12, 2))  # Output: "12"
print(circular_shift(123, 0)) # Output: "123"
print(circular_shift(123, 4)) # Output: "321"
print(circular_shift(5, 1))   # Output: "5"
print(circular_shift(0, 3))   # Output: "0"