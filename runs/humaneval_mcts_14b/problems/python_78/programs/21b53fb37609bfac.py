def hex_key(num):
    # Set of prime hexadecimal digits
    PRIME_HEX_DIGITS = {'2', '3', '5', '7', 'B', 'D'}
    
    # Count the number of prime hexadecimal digits in the input string
    count = sum(1 for digit in num if digit in PRIME_HEX_DIGITS)
    
    return count

# Example usage:
# print(hex_key("AB"))  # Output: 1
# print(hex_key("1077E"))  # Output: 2
# print(hex_key("ABED1A33"))  # Output: 4
# print(hex_key("123456789ABCDEF0"))  # Output: 6
# print(hex_key("2020"))  # Output: 2