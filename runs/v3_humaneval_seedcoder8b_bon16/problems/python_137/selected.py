def compare_one(a, b):
    def parse_value(val):
        if isinstance(val, str):
            try:
                return float(val.replace(',', '.'))
            except ValueError:
                return val
        return val

    a_parsed, b_parsed = parse_value(a), parse_value(b)

    if a_parsed > b_parsed:
        return a
    elif b_parsed > a_parsed:
        return b
    else:
        return None