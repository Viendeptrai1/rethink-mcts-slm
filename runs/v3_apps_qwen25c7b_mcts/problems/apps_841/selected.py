def generate_sequence(n):
    if n == 1:
        return "1337"
    
    # Calculate the number of '1's needed
    num_ones = 1
    
    # Calculate the number of '3's needed
    num_threes = (n - 1) // 4 + 3
    
    # Calculate the number of '7's needed
    num_sevens = n - num_ones - num_threes
    
    # Construct the sequence
    sequence = "1" * num_ones + "3" * num_threes + "7" * num_sevens
    
    return sequence

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