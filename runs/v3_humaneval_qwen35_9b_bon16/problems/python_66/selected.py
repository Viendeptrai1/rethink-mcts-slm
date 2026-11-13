def digitSum(s):
    total = 0
    for char in s:
        if 'A' <= char <= 'Z':
            total += ord(char)
    return total