def solve(n):
    if n == 2:
        return "NO"
    
    if n == 4:
        return "YES\n2 4 1 5"
    
    if n == 6:
        return "NO"
    
    if n == 8:
        return "YES\n2 4 6 8 1 3 5 11"
    
    if n == 10:
        return "NO"
    
    # For larger n, we can construct the array as follows:
    # First half: 2, 4, 6, ..., n
    # Second half: 1, 3, 5, ..., n+1
    # This ensures the sums are equal and the constraints are met.
    first_half = list(range(2, n + 1, 2))
    second_half = list(range(1, n + 2, 2))
    
    return f"YES\n{' '.join(map(str, first_half))}\n{' '.join(map(str, second_half))}"

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Process each test case
t = int(data[0])
results = []
index = 1
for _ in range(t):
    n = int(data[index])
    index += 1
    results.append(solve(n))

# Print results
for result in results:
    print(result)