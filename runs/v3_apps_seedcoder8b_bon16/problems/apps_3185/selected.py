def find_n_from_factorial(factorial_value):
    from math import factorial, isqrt
    import bisect
    
    # Function to estimate the upper bound of the search space for n
    def estimate_upper_bound(factorial_value):
        # Starting at 1! and doubling until factorial is greater than factorial_value
        n = 1
        while factorial(n) < factorial_value:
            n *= 2
        return n
    
    # Binary search to find the exact n
    low, high = 1, estimate_upper_bound(factorial_value)
    while low < high:
        mid = (low + high) // 2
        if factorial(mid) < factorial_value:
            low = mid + 1
        else:
            high = mid
    
    # Check if the found value is correct
    if factorial(low) == factorial_value:
        return low
    return -1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    factorial_value = int(input)
    result = find_n_from_factorial(factorial_value)
    print(result)