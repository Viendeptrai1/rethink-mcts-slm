def hex_key(num):
    # Define the set of prime hexadecimal digits
    prime_hex_digits = {'2', '3', '5', '7', 'B', 'D'}
    
    # Initialize a counter for prime digits
    prime_count = 0
    
    # Iterate over each character in the input string
    for char in num:
        # Check if the character is a prime hexadecimal digit
        if char in prime_hex_digits:
            prime_count += 1
    
    return prime_count

# Example usage:
# print(hex_key("AB"))  # Output: 1
# print(hex_key("1077E"))  # Output: 2
# print(hex_key("ABED1A33"))  # Output: 4
# print(hex_key("123456789ABCDEF0"))  # Output: 6
# print(hex_key("2020"))  # Output: 2