import math

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
    
    # Calculate the intersection interval
    start_intersection = max(start1, start2)
    end_intersection = min(end1, end2)
    
    # Calculate the length of the intersection
    length_intersection = end_intersection - start_intersection + 1
    
    # Check if there is an intersection
    if length_intersection > 0 and is_prime(length_intersection):
        return "YES"
    else:
        return "NO"

# Test cases
print(intersection((1, 2), (2, 3)))  # Output: "NO"
print(intersection((-1, 1), (0, 4)))  # Output: "NO"
print(intersection((-3, -1), (-5, 5)))  # Output: "YES"