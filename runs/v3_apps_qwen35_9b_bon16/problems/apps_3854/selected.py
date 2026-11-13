import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    
    coins = []
    for _ in range(n):
        coins.append(int(next(iterator)))
    
    # dp[i] will store a set of all possible sums 's' such that:
    # we can form sum 'i' using a subset of coins, AND
    # we can form sum 's' using a subset of that SAME subset.
    # Actually, a simpler approach for this specific problem structure:
    # We need to find all x such that there exists a subset S with sum(k) where x is a subset sum of S.
    # This is equivalent to: there exist two disjoint subsets A and B such that sum(A) + sum(B) = k and sum(A) = x.
    # Wait, not necessarily disjoint in the sense of partitioning the whole set, but A is a subset of S, and S has sum k.
    # So S = A U B where A and B are disjoint and sum(A) + sum(B) = k.
    # Then x = sum(A).
    # So we just need to find all possible values of x such that there exists a subset A with sum x,
    # and there exists a subset B disjoint from A with sum k - x.
    # This is equivalent to: can we form sum x and sum k-x simultaneously using disjoint subsets?
    # Which is exactly: can we form sum k using a subset, and within that subset can we pick a sub-subset with sum x?
    # 
    # Standard DP approach for this problem:
    # Let dp[i][j] be a boolean indicating if it's possible to pick a subset of coins with sum j,
    # such that within this subset we can form sum i.
    # However, n and k are up to 500. O(n*k^2) might be too slow if not careful (500^3 = 125,000,000).
    # But notice the constraint: sum of chosen coins is exactly k.
    # We can iterate through coins and update a 2D array.
    # Let reachable[i][j] = True if we can form a subset with total sum j, and within it form sum i.
    # But we don't need to track all j. We only care about j=k eventually.
    # 
    # Alternative perspective:
    # We want to find x such that there exists a subset A with sum x and a subset B with sum k-x,
    # where A and B are disjoint.
    # This is equivalent to: there exists a subset of coins with sum k, say S, such that x is a subset sum of S.
    # 
    # Let's use a DP state: dp[j] = set of all x such that we can form a subset with total sum j,
    # and x is a subset sum of that subset.
    # Initialize dp[0] = {0}. All other dp[j] = empty.
    # For each coin c:
    #   Create new_dp as copy of dp.
    #   For each sum j from k down to c:
    #     For each x in dp[j-c]:
    #       new_dp[j].add(x)
    #       new_dp[j].add(x + c)
    #     # Also, we can just add c to the existing sums in dp[j-c] to form new sums in dp[j]
    #     # But wait, the definition is: x is a subset sum of the subset that sums to j.
    #     # If we have a subset S' that sums to j-c and can form x inside it,
    #     # then S = S' U {c} sums to j.
    #     # The subset sums of S are (subset sums of S') U {subset sums of S' + c}.
    #     # So for each x in dp[j-c], we add x and x+c to dp[j].
    #     # Also, we need to preserve the old dp[j] values? 
    #     # Yes, because we can choose NOT to include the current coin c in the subset that sums to j.
    #     # So dp[j] = dp[j] U {x, x+c for x in dp[j-c]}.
    # 
    # Complexity: 
    # Outer loop n times.
    # Inner loop j from k down to c (k times).
    # Innermost loop over dp[j-c]. How big can dp[j-c] be? At most j-c+1.
    # Total complexity roughly O(n * k * k) in worst case. With n, k <= 500, 500^3 = 125e6.
    # In Python, this might be tight (1-2 seconds). We need to be efficient.
    # Using sets is good.
    # Optimization: We only care about the final answer for j=k.
    # But intermediate states are needed.
    
    # Let's refine the DP state and transitions.
    # dp[j] is a set of achievable subset-sums x for a subset of coins with total sum j.
    # Initially dp = [set() for _ in range(k+1)]
    # dp[0].add(0)
    
    # To optimize, we can use a list of sets.
    # Since we iterate coins one by one, we update in reverse order of j to avoid using the same coin multiple times for the same sum level in one step?
    # Actually, since we are building sets, we need to be careful not to use the updated dp[j-c] of the current coin iteration.
    # So we iterate j from k down to c.
    # However, since dp[j] depends on dp[j-c], and we go downwards, when we are at j, dp[j-c] is from the previous coin iteration (since j-c < j, and we haven't updated j-c yet in this pass? No, we go downwards, so j-c hasn't been updated in this pass).
    # Wait, if we go downwards: j=k, then j=k-1...
    # When we are at j, we look at j-c. Since j-c < j, and we are going downwards, we have NOT processed j-c yet in this coin iteration. So dp[j-c] contains only values from previous coins. This is correct.
    
    # One optimization: The maximum possible sum is k. So j goes up to k.
    # Also, x cannot exceed j. And x cannot exceed k.
    
    dp = [set() for _ in range(k + 1)]
    dp[0].add(0)
    
    for coin in coins:
        # We iterate j from k down to coin
        for j in range(k, coin - 1, -1):
            prev = j - coin
            if not dp[prev]:
                continue
            
            current_set = dp[j]
            prev_set = dp[prev]
            
            # For every x in dp[prev], we can form x and x+coin in dp[j]
            # Also, we keep the existing values in dp[j] (subsets that don't include this coin)
            
            # We can perform the update.
            # To avoid creating too many intermediate objects, we can collect new values.
            new_values = set()
            for x in prev_set:
                new_values.add(x)
                if x + coin <= k:
                    new_values.add(x + coin)
            
            if new_values:
                current_set.update(new_values)
    
    # The answer is all x in dp[k]
    result = sorted(dp[k])
    print(len(result))
    print(*(result))

if __name__ == '__main__':
    solve()