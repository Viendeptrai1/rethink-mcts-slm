def compare_one(a, b):
    def parse_number(value):
        if isinstance(value, str):
            value = value.replace(',', '.')
            return float(value)
        return float(value)

    num_a = parse_number(a)
    num_b = parse_number(b)

    if num_a > num_b:
        return a
    elif num_b > num_a:
        return b
    else:
        return None