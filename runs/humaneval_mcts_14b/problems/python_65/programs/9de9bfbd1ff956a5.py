def circular_shift(x, shift):
    """Circular shift the digits of the integer x, shift the digits right by shift
    and return the result as a string.
    If shift > number of digits, return digits reversed.
    """
    x_str = str(x)
    num_digits = len(x_str)
    
    if shift >= num_digits:
        return x_str[::-1]
    
    shift = shift % num_digits
    return x_str[-shift:] + x_str[:-shift]

# Test cases
print(circular_shift(12, 1))  # Expected output: "21"
print(circular_shift(12, 2))  # Expected output: "12"
print(circular_shift(0, 1))   # Expected output: "0"
print(circular_shift(12345, 3))  # Expected output: "34512"
print(circular_shift(12345, 5))  # Expected output: "54321"