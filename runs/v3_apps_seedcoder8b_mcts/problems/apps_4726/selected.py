def check_time_limit(m, n, t):
    # Define the maximum number of operations for each algorithm type
    complexities = [
        lambda n: 1,  # O(1)
        lambda n: 2**n,  # O(2^n)
        lambda n: n**4,  # O(n^4)
        lambda n: n**3,  # O(n^3)
        lambda n: n**2,  # O(n^2)
        lambda n: n * (n.bit_length()),  # O(n log n)
        lambda n: n  # O(n)
    ]
    
    # Calculate the number of operations for the given algorithm type and input size
    operations = complexities[t-1](n)
    
    # Compare the number of operations to the limit m
    if operations <= m:
        return "AC"
    else:
        return "TLE"

# Read input
m, n, t = map(int, input().split())

# Output the result
print(check_time_limit(m, n, t))