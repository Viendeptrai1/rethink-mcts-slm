def compare_one(a, b):
    def convert_to_number(value):
        if isinstance(value, str):
            value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Invalid number format: {value}")
        return value

    num_a = convert_to_number(a)
    num_b = convert_to_number(b)

    if num_a > num_b:
        return a
    elif num_b > num_a:
        return b
    else:
        return None