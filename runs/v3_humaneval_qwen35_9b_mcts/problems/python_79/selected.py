def decimal_to_binary(decimal):
    """Converts a decimal number to a binary string with 'db' prefix and suffix."""
    if decimal == 0:
        binary_str = "0"
    else:
        binary_digits = []
        n = decimal
        while n > 0:
            binary_digits.append(str(n % 2))
            n //= 2
        binary_str = ''.join(reversed(binary_digits))
    
    return "db" + binary_str + "db"