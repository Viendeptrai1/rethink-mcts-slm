def frog_jumps(t, queries):
    results = []
    for a, b, k in queries:
        # Calculate the net effect of the first k jumps
        net_effect = 0
        full_cycles = k // 2
        remainder_jumps = k % 2
        
        # Each full cycle adds a net effect of (a - b)
        net_effect += full_cycles * (a - b)
        
        # If there's an odd number of jumps, add the effect of the last jump
        if remainder_jumps == 1:
            net_effect += a
        
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