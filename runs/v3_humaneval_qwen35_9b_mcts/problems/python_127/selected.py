def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def intersection(interval1, interval2):
    start1, end1 = interval1
    start2, end2 = interval2
    
    max_start = max(start1, start2)
    min_end = min(end1, end2)
    
    if max_start > min_end:
        return "NO"
    
    length = min_end - max_start
    
    if is_prime(length):
        return "YES"
    else:
        return "NO"