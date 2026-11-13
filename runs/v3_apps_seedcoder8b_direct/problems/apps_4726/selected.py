def check_time_limit(m, n, t):
    # Define the maximum number of operations for each complexity type
    complexities = [
        lambda n: 1,  # O(1)
        lambda n: n,  # O(n)
        lambda n: n**2,  # O(n^2)
        lambda n: n**3,  # O(n^3)
        lambda n: n**4,  # O(n^4)
        lambda n: n * (n.bit_length()),  # O(n log n)
        lambda n: 2**n  # O(2^n)
    ]
    
    # Calculate the number of operations for the given complexity type
    operations = complexities[t-1](n)
    
    # Check if the number of operations is within the limit
    if operations <= m:
        return "AC"
    else:
        return "TLE"

# Read input
m, n, t = map(int, input().split())

# Output the result
print(check_time_limit(m, n, t))