import sys

def min_hours_to_build_houses(n, hills):
    max_k = (n + 1) // 2
    result = [0] * max_k
    
    for k in range(1, max_k + 1):
        min_decreases = float('inf')
        for start in range(k - 1, n - k + 1):
            decreases = sum(max(hills[start+i-1] - hills[start+i], 0) for i in range(1, k))
            min_decreases = min(min_decreases, decreases)
        
        result[k-1] = min_decreases
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
hills = list(map(int, data[1:]))

# Calculate results
results = min_hours_to_build_houses(n, hills)

# Output results
print(" ".join(map(str, results)))