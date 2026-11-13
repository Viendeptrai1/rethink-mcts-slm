def frog_jumps(t, queries):
    results = []
    for a, b, k in queries:
        # Calculate the net effect of the first k jumps
        if k % 2 == 0:
            # If k is even, the net effect is k/2 * (a - b)
            net_effect = (k // 2) * (a - b)
        else:
            # If k is odd, the net effect is (k//2 + 1) * a - (k//2) * b
            net_effect = ((k // 2) + 1) * a - (k // 2) * b
        
        results.append(net_effect)
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
queries = []
index = 1
for _ in range(t):
    a = int(data[index])
    b = int(data[index + 1])
    k = int(data[index + 2])
    queries.append((a, b, k))
    index += 3

# Get results
results = frog_jumps(t, queries)

# Print results
for result in results:
    print(result)