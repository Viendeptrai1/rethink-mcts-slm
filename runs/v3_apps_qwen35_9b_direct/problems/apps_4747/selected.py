import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    # dp[i] will store the maximum expected score with i rolls remaining
    # We start from 0 rolls remaining (base case) and build up to k rolls.
    # With 0 rolls remaining, the expected score is 0 (though in the game logic,
    # we would have already taken the previous roll, so this is the value we compare against).
    
    # Actually, let's define dp[r] as the expected score if we have r rolls LEFT to use.
    # If we have 0 rolls left, we cannot roll anymore, so the value is 0.
    # However, the decision is made BEFORE rolling. If we have r rolls left, we roll once.
    # After rolling, we see the value x. We can either:
    #   1. Stop and take x.
    #   2. Continue if we have rolls left (r-1 remaining after this roll) and x is less than the expected value of continuing.
    
    # Let E[r] be the maximum expected score given that we have r rolls remaining to use.
    # Base case: E[0] = 0 (no rolls left, so we get 0 from future rolls, but in the context of the decision,
    # if we are at a state with 0 rolls left, we must have stopped already or the game ends. 
    # But the recurrence is: when we have r rolls, we roll. We get a value v in [1, n].
    # Then we choose max(v, E[r-1]).
    # So E[r] = average over v of max(v, E[r-1]).
    
    # E[0] = 0.
    
    current_expected = 0.0  # This represents E[0]
    
    for r in range(1, k + 1):
        # Calculate E[r] based on E[r-1] (which is current_expected)
        # We roll the die. The outcome v is uniform in [1, n].
        # If v >= current_expected, we take v.
        # If v < current_expected, we take current_expected (by rolling again, since we have r-1 rolls left).
        
        # Find the threshold: we take v if v >= current_expected.
        # Since v is integer, the smallest integer >= current_expected is ceil(current_expected).
        # Let threshold = ceil(current_expected).
        # Values v in [1, n].
        # If threshold > n, then for all v in [1, n], v < current_expected, so we always take current_expected.
        # If threshold <= 1, then for all v in [1, n], v >= current_expected, so we always take v.
        
        import math
        threshold = math.ceil(current_expected)
        
        # Sum of max(v, current_expected) for v from 1 to n
        total_sum = 0.0
        
        # Case 1: v < threshold. We take current_expected.
        # v ranges from 1 to min(n, threshold - 1)
        limit_low = min(n, threshold - 1)
        if limit_low >= 1:
            count_low = limit_low
            total_sum += count_low * current_expected
            
        # Case 2: v >= threshold. We take v.
        # v ranges from max(1, threshold) to n
        start_high = max(1, threshold)
        if start_high <= n:
            count_high = n - start_high + 1
            # Sum of integers from start_high to n
            sum_high = (start_high + n) * count_high // 2
            total_sum += sum_high
            
        current_expected = total_sum / n
        
    print(f"{current_expected:.10f}")

if __name__ == "__main__":
    solve()