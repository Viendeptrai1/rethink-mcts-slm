def solve(s):
    has_letter = any(c.isalpha() for c in s)
    if not has_letter:
        return s[::-1]
    result = []
    for c in s:
        if c.isalpha():
            if c.islower():
                result.append(c.upper())
            else:
                result.append(c.lower())
        else:
            result.append(c)
    return ''.join(result)