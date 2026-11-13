def compare_one(a, b):
    def parse(value):
        if isinstance(value, str):
            # Replace comma with dot for decimal separator normalization
            normalized = value.replace(',', '.')
            return float(normalized)
        elif isinstance(value, (int, float)):
            return float(value)
        else:
            raise ValueError(f"Unsupported type: {type(value)}")

    val_a = parse(a)
    val_b = parse(b)

    if val_a == val_b:
        return None

    if val_a > val_b:
        return a
    else:
        return b