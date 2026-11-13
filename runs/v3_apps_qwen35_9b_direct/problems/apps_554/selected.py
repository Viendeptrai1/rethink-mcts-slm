import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
            
        # Count how many times each flower is included in the chosen subarrays
        # Since we want to maximize the sum, for each flower, we should include it
        # in the total count if the coefficient (number of subarrays covering it) * mood > 0
        # Actually, the problem says: choose a subset of suggested subarrays.
        # The contribution of a flower i is: a[i] * (number of chosen subarrays covering i).
        # Let x_j be 1 if we choose subarray j, 0 otherwise.
        # Total happiness = sum over j of (sum over i in subarray j of a[i])
        # This is equivalent to: sum over i of (a[i] * count_i), where count_i is the number of chosen subarrays covering i.
        # But notice: Total = sum_{j} (sum_{i=l_j}^{r_j} a[i])
        # We can simply calculate the sum of each suggested subarray.
        # If the sum of a subarray is positive, we should definitely choose it to increase the total.
        # If it is negative, we should not choose it (since we can choose any subset, including empty).
        # If it is zero, it doesn't matter.
        # So the strategy is: calculate the sum for each of the m subarrays. If sum > 0, add it to the result.
        
        total_happiness = 0
        
        for _ in range(m):
            l = int(next(iterator))
            r = int(next(iterator))
            
            # Convert 1-based indexing to 0-based
            current_sum = 0
            for idx in range(l - 1, r):
                current_sum += a[idx]
            
            if current_sum > 0:
                total_happiness += current_sum
                
        print(total_happiness)
        
    except StopIteration:
        pass

if __name__ == "__main__":
    solve()