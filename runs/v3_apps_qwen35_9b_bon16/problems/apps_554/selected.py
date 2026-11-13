import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
        
    # Count how many times each flower is included in the chosen subarrays
    # Since we can choose any subset of suggested subarrays independently,
    # for each flower, we sum the moods of all suggested subarrays that cover this flower.
    # If the total contribution for a flower is positive, we include ALL suggested subarrays covering it.
    # If it's negative or zero, we include none (since including a subset would only reduce the sum further or stay same).
    # Actually, the logic is simpler:
    # For each suggested subarray i, if the sum of elements in that subarray is positive, we take it.
    # If it's negative, we don't take it. If zero, it doesn't matter.
    # Why? Because the total happiness is the sum over all chosen subarrays of (sum of elements in that subarray).
    # Total Happiness = Sum_{chosen subarray j} (Sum_{k=l_j}^{r_j} a[k])
    # This is equivalent to Sum_{j in chosen} (subarray_sum_j).
    # Since the choice of one subarray does not affect the contribution of another (linearity),
    # we can optimize each subarray's inclusion independently.
    # We include subarray j if and only if its sum > 0.
    
    total_happiness = 0
    
    for _ in range(m):
        l = int(next(iterator))
        r = int(next(iterator))
        
        # Calculate sum of the subarray a[l-1 : r]
        current_sum = 0
        for k in range(l-1, r):
            current_sum += a[k]
            
        if current_sum > 0:
            total_happiness += current_sum
            
    print(total_happiness)

if __name__ == "__main__":
    solve()