def min_rolls_to_get_points(t, queries):
    results = []
    for x in queries:
        # Calculate the minimum number of rolls required to get exactly x points
        # This is equivalent to finding the smallest integer n such that:
        # 2 + 3 + ... + 7 <= x <= 2 + 3 + ... + 7 + 7
        # The sum of the first 6 natural numbers is 21, so we need to find n such that:
        # 21 * n <= x <= 21 * (n + 1)
        # Solving for n:
        # n <= x / 21
        # n >= x / 28
        # n is the ceiling of x / 21
        n = (x + 20) // 21  # This is equivalent to math.ceil(x / 21)
        results.append(n)
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
queries = list(map(int, data[1:t+1]))

# Get results
results = min_rolls_to_get_points(t, queries)

# Print results
for result in results:
    print(result)