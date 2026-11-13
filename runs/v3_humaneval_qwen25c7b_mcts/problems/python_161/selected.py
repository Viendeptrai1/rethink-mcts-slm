def solve(s):
    new_s = []
    for char in s:
        if char.isalpha():
            new_s.append(char.swapcase())
        else:
            new_s.append(char)
    
    if all(not char.isalpha() for char in s):
        return ''.join(new_s[::-1])
    
    return ''.join(new_s)