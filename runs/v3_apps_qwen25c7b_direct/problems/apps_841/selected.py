def generate_sequence(n):
    if n == 1:
        return "1337"
    
    # Calculate the number of subsequences we need to add
    additional_subsequences = n - 1
    
    # We need to add '1' at the beginning and '7' at the end to ensure we get the required subsequences
    result = "1" + "3" * (additional_subsequences // 2) + "7"
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Number of queries
t = int(data[0])

# Process each query
results = []
for i in range(1, t + 1):
    n = int(data[i])
    results.append(generate_sequence(n))

# Print results
for result in results:
    print(result)