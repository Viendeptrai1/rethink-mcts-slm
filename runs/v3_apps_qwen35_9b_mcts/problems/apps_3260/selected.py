import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])
    p = int(input_data[2])

    if k >= n:
        print(n % p)
        return

    # dp[j][d] will store the number of valid permutations of the current length
    # ending with a run of length j in direction d.
    # d = 0 for increasing, d = 1 for decreasing.
    # We process lengths from 1 to n.
    
    # Initialize for length 1
    # A single element has a run of length 1. Direction doesn't strictly matter yet,
    # but we can consider it as starting an increasing run or decreasing run.
    # However, the transition logic requires knowing the direction of the last added element relative to the previous.
    # Let's define state after placing i elements:
    # dp[j][0]: ends with a run of length j, and the last step was increasing (current > previous)
    # dp[j][1]: ends with a run of length j, and the last step was decreasing (current < previous)
    
    # For i=1:
    # We have 1 permutation [1]. Run length 1.
    # We can conceptually say it's the start of an increasing run or decreasing run.
    # But to make transitions work, let's say for i=1, we have 1 way in state (1, 0) and 1 way in state (1, 1)?
    # No, that would double count.
    # Actually, for the first element, there is no "previous".
    # Let's handle i=1 separately or set up the base case carefully.
    # If we consider the sequence of differences:
    # For n=1, answer is 1.
    # Let's say at i=1, we have dp[1][0] = 1 (imagining it could go up next) and dp[1][1] = 1 (imagining it could go down next)?
    # If we do that, then for i=2:
    # From dp[1][0] (last was up, run len 1): we can go down. New run len 1, dir down. Count += 1.
    # From dp[1][1] (last was down, run len 1): we can go up. New run len 1, dir up. Count += 1.
    # Total for i=2 would be 2. Correct ([1,2], [2,1]).
    # But wait, if we start with dp[1][0]=1 and dp[1][1]=1, we are effectively saying there are 2 states for length 1.
    # The actual number of permutations of length 1 is 1.
    # The issue is that the "direction" is undefined for the first element.
    # However, the transitions only care about the direction of the *last step*.
    # So for i=1, we can arbitrarily assign it to both states with weight 0.5? No, integers.
    # Let's redefine:
    # dp[j][0]: number of perms of length i ending with run length j, last step was UP.
    # dp[j][1]: number of perms of length i ending with run length j, last step was DOWN.
    # Base case i=1:
    # There is 1 permutation. It has no last step.
    # We can treat it as if it ended with a run of length 1, and we can choose the next direction freely.
    # So effectively, for the purpose of generating i=2, we need to be able to start an UP run or a DOWN run.
    # Let's set dp[1][0] = 1 and dp[1][1] = 1. This implies we have 2 "virtual" permutations of length 1?
    # If we do this, then for i=2:
    # From dp[1][0] (UP): must go DOWN. New state: run len 1, DOWN. Add 1.
    # From dp[1][1] (DOWN): must go UP. New state: run len 1, UP. Add 1.
    # Total for i=2: 2. Correct.
    # For i=3:
    # From i=2 states:
    # State (1, DOWN) count=1: can go UP (new run 1, UP) or DOWN (new run 2, DOWN).
    # State (1, UP) count=1: can go DOWN (new run 1, DOWN) or UP (new run 2, UP).
    # Total for i=3:
    # UP, len 1: from (1, DOWN) -> 1
    # DOWN, len 1: from (1, UP) -> 1
    # UP, len 2: from (1, UP) -> 1
    # DOWN, len 2: from (1, DOWN) -> 1
    # Total = 4. Correct.
    # So the base case dp[1][0] = 1, dp[1][1] = 1 works perfectly for generating n >= 2.
    # For n=1, we just output 1.
    
    # Initialize DP table
    # dp[j][d]
    dp = [[0] * 2 for _ in range(k + 1)]
    dp[1][0] = 1
    dp[1][1] = 1
    
    for length in range(2, n + 1):
        new_dp = [[0] * 2 for _ in range(k + 1)]
        
        # Iterate over previous run lengths and directions
        for prev_len in range(1, k + 1):
            for d in range(2):
                count = dp[prev_len][d]
                if count == 0:
                    continue
                
                # If previous direction was UP (d=0), we can:
                # 1. Continue UP if prev_len < k. New run length = prev_len + 1.
                # 2. Switch to DOWN. New run length = 1.
                
                if d == 0: # Previous was UP
                    # Continue UP
                    if prev_len < k:
                        new_len = prev_len + 1
                        new_dp[new_len][0] = (new_dp[new_len][0] + count) % p
                    
                    # Switch to DOWN
                    new_dp[1][1] = (new_dp[1][1] + count) % p
                    
                else: # Previous was DOWN (d=1)
                    # Continue DOWN
                    if prev_len < k:
                        new_len = prev_len + 1
                        new_dp[new_len][1] = (new_dp[new_len][1] + count) % p
                    
                    # Switch to UP
                    new_dp[1][0] = (new_dp[1][0] + count) % p
        
        dp = new_dp

    # Sum all valid states
    total = 0
    for j in range(1, k + 1):
        total = (total + dp[j][0] + dp[j][1]) % p
        
    print(total)

if __name__ == "__main__":
    solve()