def decimal_to_binary(decimal):
    """Converts a decimal number to binary format with 'db' prefix and suffix."""
    if decimal == 0:
        return "db0db"
    
    binary = ""
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal = decimal // 2
    
    return f"db{binary}db"

# Example usage:
# print(decimal_to_binary(15))  # Output: "db1111db"
# print(decimal_to_binary(32))  # Output: "db100000db"