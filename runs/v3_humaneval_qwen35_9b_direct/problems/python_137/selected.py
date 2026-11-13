def compare_one(a, b):
    def to_float(value):
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            value = value.replace(',', '.')
            return float(value)
        return None

    float_a = to_float(a)
    float_b = to_float(b)

    if float_a is None or float_b is None:
        return None

    if float_a == float_b:
        return None

    if float_a > float_b:
        return a
    else:
        return b