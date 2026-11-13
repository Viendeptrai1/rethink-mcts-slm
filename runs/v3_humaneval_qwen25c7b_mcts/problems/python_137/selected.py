def compare_one(a, b):
    def to_float(value):
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    
    fa = to_float(a)
    fb = to_float(b)
    
    if fa == fb:
        return None
    elif fa > fb:
        return a
    else:
        return b