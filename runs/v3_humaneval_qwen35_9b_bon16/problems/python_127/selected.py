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

    intersect_start = max(start1, start2)
    intersect_end = min(end1, end2)

    if intersect_start > intersect_end:
        return "NO"

    length = intersect_end - intersect_start + 1

    if is_prime(length):
        return "YES"
    else:
        return "NO"