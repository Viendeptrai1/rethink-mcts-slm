def decimal_to_binary(decimal):
    """Convert a decimal number to binary format with 'db' prefix and suffix."""
    if decimal == 0:
        binary_representation = "0"
    else:
        binary_representation = bin(decimal)[2:]
    return f"db{binary_representation}db"