def starts_one_ends(n):
    if n == 1:
        return 2
    
    count = 9 * 10 ** (n - 2) + 9
    return count