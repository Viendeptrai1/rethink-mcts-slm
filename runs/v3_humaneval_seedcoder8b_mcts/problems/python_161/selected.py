def solve(s):
    has_letter = False
    result = []
    for char in s:
        if char.isalpha():
            has_letter = True
            result.append(char.swapcase())
        else:
            result.append(char)
    
    if not has_letter:
        return s[::-1]
    return ''.join(result)