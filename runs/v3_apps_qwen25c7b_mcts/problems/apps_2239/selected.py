def min_rolls_to_score(x):
    # Iterate over possible number of rolls starting from 1
    for rolls in range(1, x + 1):
        # Check if it's possible to achieve the target score with the current number of rolls
        if x % rolls == 0 and x // rolls <= 6:
            return rolls

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Number of queries
t = int(data[0])

# Process each query
results = []
for i in range(t):
    x = int(data[i + 1])
    results.append(min_rolls_to_score(x))

# Print results
for result in results:
    print(result)