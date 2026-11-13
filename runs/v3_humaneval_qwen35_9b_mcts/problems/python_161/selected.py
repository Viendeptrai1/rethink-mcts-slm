def solve(s):
    has_letter = False
    result = []
    
    for char in s:
        if char.isalpha():
            has_letter = True
            if char.islower():
                result.append(char.upper())
            else:
                result.append(char.lower())
        else:
            result.append(char)
    
    if not has_letter:
        return s[::-1]
    
    return "".join(result)