def compare_one(a, b):
    def parse_value(value):
        if isinstance(value, str):
            value = value.replace(',', '.')
            try:
                return float(value)
            except ValueError:
                return value
        return value

    parsed_a = parse_value(a)
    parsed_b = parse_value(b)

    if parsed_a == parsed_b:
        return None
    elif parsed_a > parsed_b:
        return a
    else:
        return b

# Test cases
print(compare_one(1, 2.5))  # ➞ 2.5
print(compare_one(1, "2,3"))  # ➞ "2,3"
print(compare_one("5,1", "6"))  # ➞ "6"
print(compare_one("1", 1))  # ➞ None