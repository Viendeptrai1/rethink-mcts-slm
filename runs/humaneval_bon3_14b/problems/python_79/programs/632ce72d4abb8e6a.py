def decimal_to_binary(decimal):
    """Converts a decimal number to binary format with 'db' prefix and suffix."""
    # Convert the decimal number to binary and remove the '0b' prefix
    binary_str = bin(decimal)[2:]
    # Add 'db' at the beginning and the end of the binary string
    return f"db{binary_str}db"

# Example usage:
# print(decimal_to_binary(15))  # Output: "db1111db"
# print(decimal_to_binary(32))  # Output: "db100000db"