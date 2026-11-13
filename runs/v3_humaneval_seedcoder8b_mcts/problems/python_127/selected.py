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
    
    # Find the intersection
    start_intersection = max(start1, start2)
    end_intersection = min(end1, end2)
    
    # Check if there is an intersection
    if start_intersection > end_intersection:
        return "NO"
    
    # Calculate the length of the intersection
    intersection_length = end_intersection - start_intersection
    
    # Check if the length is a prime number
    if is_prime(intersection_length):
        return "YES"
    else:
        return "NO"