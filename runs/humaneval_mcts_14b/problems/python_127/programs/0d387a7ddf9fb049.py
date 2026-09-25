def is_prime(n):
    """Check if a number is a prime number."""
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
    """Determine if the length of the intersection of two intervals is a prime number."""
    start1, end1 = interval1
    start2, end2 = interval2
    
    # Calculate the intersection
    start = max(start1, start2)
    end = min(end1, end2)
    
    # Check if there is an intersection
    if start > end:
        return "NO"
    
    # Calculate the length of the intersection
    intersection_length = end - start + 1
    
    # Check if the length is a prime number
    if is_prime(intersection_length):
        return "YES"
    else:
        return "NO"

# Test cases
print(intersection((1, 2), (2, 3)))  # Output: "NO"
print(intersection((-1, 1), (0, 4)))  # Output: "YES"
print(intersection((-3, -1), (-5, 5)))  # Output: "YES"