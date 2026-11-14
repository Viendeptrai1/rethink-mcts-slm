import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(data[i+1]) for i in range(n)]
    
    # Maximum possible houses is ceil(n/2)
    max_k = (n + 1) // 2
    
    # Precompute costs to make index i a peak
    # cost[i] = cost to make a[i] > a[i-1] and a[i] > a[i+1]
    # We can reduce neighbors, but not increase a[i].
    # Cost for left neighbor: max(0, a[i] - a[i-1]) -> we need a[i] > a[i-1], so if a[i] <= a[i-1], we must reduce a[i-1] to a[i]-1. Cost = a[i-1] - (a[i]-1) = a[i-1] - a[i] + 1. If a[i-1] < a[i], cost is 0.
    # Similarly for right neighbor.
    
    # However, the problem allows reducing hills to negative values.
    # To make a[i] a peak:
    # 1. If i > 0: we need new_a[i] > new_a[i-1]. Since we can only decrease, the best strategy is to keep new_a[i] = a[i] (since increasing is impossible) and reduce new_a[i-1] to a[i]-1. Cost = max(0, a[i-1] - (a[i]-1)).
    # 2. If i < n-1: we need new_a[i] > new_a[i+1]. Reduce new_a[i+1] to a[i]-1. Cost = max(0, a[i+1] - (a[i]-1)).
    
    # Let's define base_cost[i] as the cost to make index i a peak assuming no other constraints on neighbors (i.e., we just fix immediate neighbors).
    base_cost = [0] * n
    for i in range(n):
        c = 0
        if i > 0:
            # Need a[i] > a[i-1] -> a[i-1] <= a[i] - 1
            # If a[i-1] >= a[i], we reduce a[i-1] to a[i]-1. Cost = a[i-1] - (a[i]-1)
            # If a[i-1] < a[i], cost is 0.
            if a[i-1] >= a[i]:
                c += a[i-1] - a[i] + 1
        if i < n - 1:
            # Need a[i] > a[i+1] -> a[i+1] <= a[i] - 1
            if a[i+1] >= a[i]:
                c += a[i+1] - a[i] + 1
        base_cost[i] = c

    # Now we need to select k indices such that they are peaks and the total cost is minimized.
    # Constraints: If we pick index i, we cannot pick i-1 or i+1 because they would be neighbors of a peak, and a peak must be strictly higher than neighbors.
    # Actually, if i is a peak, then i-1 and i+1 cannot be peaks because a peak must be strictly higher than its neighbors. If i-1 were a peak, it would need to be > i, but i is > i-1 (since i is a peak). Contradiction.
    # So selected indices must be non-adjacent.
    
    # We need to compute min_cost[k] for k from 1 to max_k.
    # This is a DP problem: select k non-adjacent indices to minimize sum of base_cost.
    # Let dp[i][j] be the min cost to select j peaks using a subset of first i hills (indices 0 to i-1).
    # Transitions:
    # dp[i][j] = min(
    #   dp[i-1][j],  // don't pick hill i-1
    #   dp[i-2][j-1] + base_cost[i-1]  // pick hill i-1 (requires i-2 to be the last picked or none)
    # )
    # Base cases:
    # dp[0][0] = 0, all others infinity.
    # dp[1][0] = 0, dp[1][1] = base_cost[0].
    
    # Since n is up to 5000, O(n^2) is acceptable (25e6 operations).
    
    INF = float('inf')
    # dp[j] will store the min cost to have j peaks considering hills processed so far.
    # We need to keep track of the state where the last hill was picked or not.
    # Let's use two arrays: dp[j] = min cost for j peaks ending with NOT picking current hill
    #                dp_prev[j] = min cost for j peaks ending with picking current hill?
    # Better: dp[i][j] where i is number of hills considered.
    # To save space, we can iterate i from 1 to n.
    # Let dp[j] be the min cost to have j peaks using a subset of the first i hills, where the i-th hill is NOT picked.
    # Let dp_pick[j] be the min cost to have j peaks using a subset of the first i hills, where the i-th hill IS picked.
    
    # Initialize for i=0 (0 hills)
    # dp[j] = 0 if j=0 else INF
    # dp_pick[j] = INF
    
    # We will iterate i from 0 to n-1 (hill index)
    # Let current_dp[j] = min cost for j peaks considering hills 0..i, where hill i is NOT picked.
    # Let current_pick[j] = min cost for j peaks considering hills 0..i, where hill i IS picked.
    
    # Initial state (before processing any hill):
    # current_dp[0] = 0, others INF
    # current_pick[0..max_k] = INF
    
    current_dp = [INF] * (max_k + 1)
    current_pick = [INF] * (max_k + 1)
    current_dp[0] = 0
    
    results = [INF] * (max_k + 1)
    
    for i in range(n):
        # Compute next states based on hill i
        next_dp = [INF] * (max_k + 1)
        next_pick = [INF] * (max_k + 1)
        
        # Option 1: Don't pick hill i
        # We can transition from any state of previous hills (whether i-1 was picked or not)
        # So next_dp[j] = min(current_dp[j], current_pick[j])
        for j in range(max_k + 1):
            val = min(current_dp[j], current_pick[j])
            if val < next_dp[j]:
                next_dp[j] = val
        
        # Option 2: Pick hill i
        # We can only pick hill i if we didn't pick hill i-1.
        # So we transition from current_dp (where i-1 was not picked)
        # next_pick[j] = current_dp[j-1] + base_cost[i]
        cost = base_cost[i]
        for j in range(1, max_k + 1):
            if current_dp[j-1] != INF:
                val = current_dp[j-1] + cost
                if val < next_pick[j]:
                    next_pick[j] = val
        
        # Update for next iteration
        current_dp = next_dp
        current_pick = next_pick
        
        # After processing hill i, the answer for k peaks is min(current_dp[k], current_pick[k])
        if k_val := 0:
            pass
        # We need to store the min cost for each k after processing all hills.
        # But we can just update a global min array at the end or track it.
        # Actually, the final answer for k is min(current_dp[k], current_pick[k]) after the loop.
    
    # Final answers
    final_ans = []
    for k in range(1, max_k + 1):
        ans = min(current_dp[k], current_pick[k])
        final_ans.append(ans)
    
    print(*(final_ans))

if __name__ == '__main__':
    solve()