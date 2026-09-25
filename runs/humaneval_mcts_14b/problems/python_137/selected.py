def compare_one(a, b):
    def parse_number(value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, str):
            # Replace comma with dot for decimal conversion
            value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Invalid number format: {value}")
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    num_a = parse_number(a)
    num_b = parse_number(b)

    if num_a > num_b:
        return a
    elif num_b > num_a:
        return b
    else:
        return None

# Test cases
print(compare_one(1, 2.5))  # ➞ 2.5
print(compare_one(1, "2,3"))  # ➞ "2,3"
print(compare_one("5,1", "6"))  # ➞ "6"
print(compare_one("1", 1))  # ➞ None