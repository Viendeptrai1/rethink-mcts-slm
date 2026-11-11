import sys

def min_insertions_to_avoid_zero_sum_subsegments(n, a):
    prefix_sums = [0] * (n + 1)
    seen_sums = set()
    insertions = 0
    
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + a[i - 1]
        
        if prefix_sums[i] in seen_sums:
            # Insert an element between the previous occurrence and current position
            insertions += 1
            # Adjust the prefix sum to avoid zero-sum subsegment
            prefix_sums[i] += 1
            # Clear the seen sums to start fresh after insertion
            seen_sums.clear()
        
        seen_sums.add(prefix_sums[i])
    
    return insertions

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(min_insertions_to_avoid_zero_sum_subsegments(n, a))