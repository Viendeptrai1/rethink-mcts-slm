def can_reorder(a, n):
    total_sum = sum(a)
    
    # If the total sum is odd, we can always split it into two parts with different sums
    if total_sum % 2 != 0:
        return a
    
    # If the total sum is even, we need to check if we can find a valid split
    target_sum = total_sum // 2
    
    # Try to find a subset of n elements whose sum is not equal to target_sum
    from itertools import combinations
    
    for comb in combinations(a, n):
        if sum(comb) != target_sum:
            # Found a valid split
            remaining = [x for x in a if x not in comb]
            return list(comb) + remaining
    
    # If no valid split is found, return -1
    return "-1"

# Read input
n = int(input())
a = list(map(int, input().split()))

# Get the result
result = can_reorder(a, n)

# Print the result
if result == "-1":
    print("-1")
else:
    print(" ".join(map(str, result)))