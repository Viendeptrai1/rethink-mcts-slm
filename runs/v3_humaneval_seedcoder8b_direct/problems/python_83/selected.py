def starts_one_ends(n):
    if n == 1:
        return 2
    
    count = 0
    for i in range(1, 10):
        count += 10 ** (n - 1)
    
    return count