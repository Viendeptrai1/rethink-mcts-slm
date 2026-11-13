def compare_one(a, b):
    def to_float(value):
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            value = value.replace(',', '.')
            return float(value)
        raise ValueError("Unsupported type")

    val_a = to_float(a)
    val_b = to_float(b)

    if val_a > val_b:
        return a
    elif val_b > val_a:
        return b
    else:
        return None