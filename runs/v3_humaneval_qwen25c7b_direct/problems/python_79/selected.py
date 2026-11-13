def decimal_to_binary(decimal):
    if decimal == 0:
        return "db0db"
    binary = ""
    while decimal > 0:
        binary = str(decimal % 2) + binary
        decimal //= 2
    return f"db{binary}db"