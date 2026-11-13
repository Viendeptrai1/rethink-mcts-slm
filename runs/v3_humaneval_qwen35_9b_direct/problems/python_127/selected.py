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
    
    inter_start = max(start1, start2)
    inter_end = min(end1, end2)
    
    if inter_start > inter_end:
        return "NO"
    
    length = inter_end - inter_start + 1
    
    if is_prime(length):
        return "YES"
    else:
        return "NO"