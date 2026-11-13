def solve(s):
    has_letter = any(c.isalpha() for c in s)
    
    if not has_letter:
        return s[::-1]
    
    result = []
    for char in s:
        if char.isalpha():
            if char.islower():
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)
    
    return "".join(result)