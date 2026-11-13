import sys

# Set recursion limit just in case, though we will use iterative approach where possible
sys.setrecursionlimit(200000)

MOD = 998244353

def power(a, b, mod):
    res = 1
    a %= mod
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % mod
        a = (a * a) % mod
        b //= 2
    return res

def mod_inverse(n, mod):
    return power(n, mod - 2, mod)

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
            
        w = []
        for _ in range(n):
            w.append(int(next(iterator)))
    except StopIteration:
        return

    # Separate liked and disliked pictures
    liked_w = []
    disliked_w = []
    
    for i in range(n):
        if a[i] == 1:
            liked_w.append(w[i])
        else:
            disliked_w.append(w[i])
            
    total_liked = sum(liked_w)
    total_disliked = sum(disliked_w)
    total_sum = total_liked + total_disliked
    
    # Precompute factorials and inverse factorials for combinations if needed, 
    # but since m is small (3000), we can just compute powers iteratively.
    
    # Function to compute expected final weight for a picture with initial weight w_init
    # in a group of total weight W_group, given m steps.
    # 
    # If the picture is liked:
    # E[final] = w_init + m * (total_liked / total_sum) ? No, it's more complex because total changes.
    # Actually, for a liked picture i with weight w_i:
    # The expected number of times it is picked is NOT simply m * (w_i / sum).
    # However, due to linearity and symmetry within groups:
    # For any two liked pictures i and j, the ratio of their expected final weights 
    # equals the ratio of their initial weights.
    # Let E_i be the expected final weight of liked picture i.
    # E_i / w_i = K_liked (same constant for all liked pictures).
    # Similarly, for disliked pictures: E_j / w_j = K_disliked.
    #
    # We know: Sum_{liked} E_i + Sum_{disliked} E_j = total_sum + m
    # Because each step adds 1 to liked or subtracts 1 from disliked.
    # Net change to sum: +1 if liked picked, -1 if disliked picked.
    # Total steps = m.
    # Let X be number of times a liked picture was picked.
    # Let Y be number of times a disliked picture was picked.
    # X + Y = m.
    # Final sum = (total_liked + X) + (total_disliked - Y) = total_sum + X - Y = total_sum + 2X - m.
    # Wait, the problem asks for expected weight.
    # Sum of expected weights = E[Final Sum].
    # E[Final Sum] = total_sum + E[X - Y] = total_sum + E[2X - m] = total_sum + 2*E[X] - m.
    # But we don't know E[X] directly without simulation or DP.
    #
    # Alternative approach using DP:
    # Let dp[i][j] be the probability that after i steps, the total weight of liked pictures is (total_liked + j).
    # j ranges from -i to +i, but actually since we start with total_liked, 
    # let's say we track the net change.
    # State: dp[k][delta] = probability that after k steps, the sum of liked weights has increased by delta.
    # Then sum of disliked weights has changed by -(m - k + delta)? No.
    # Let's redefine:
    # After k steps, let L be the new sum of liked weights, D be the new sum of disliked weights.
    # L = total_liked + (number of times a liked pic was picked)
    # D = total_disliked - (number of times a disliked pic was picked)
    # Let x = number of times liked was picked. Then number of disliked picked is k - x.
    # L = total_liked + x
    # D = total_disliked - (k - x) = total_disliked - k + x
    # Total sum S_k = L + D = total_sum + 2x - k.
    # 
    # Transitions:
    # From state x (after k steps):
    # Prob of picking liked next = (total_liked + x) / (total_sum + 2x - k)
    # Prob of picking disliked next = (total_disliked - (k - x)) / (total_sum + 2x - k)
    # Let S = total_liked + total_disliked.
    # Current liked sum = total_liked + x.
    # Current disliked sum = total_disliked - (k - x).
    # Current total = S + 2x - k.
    # 
    # dp[k][x] -> dp[k+1][x+1] with prob (total_liked + x) / (S + 2x - k)
    # dp[k][x] -> dp[k+1][x] with prob (total_disliked - k + x) / (S + 2x - k)
    #
    # Range of x:
    # Min x: max(0, k - total_disliked) [cannot pick disliked more than available initially? No, weights can go to 0? 
    # Problem says w_i >= 1 initially. If weight becomes 0, can it be picked?
    # "subtract 1 from its weight". If weight becomes 0, probability is 0. So it won't be picked.
    # But can it become negative? "non-negative weight". Usually implies >= 0.
    # If weight is 0, prob is 0. So it stays 0 until picked? No, if prob is 0, it can't be picked.
    # So weight can be 0.
    # However, we are guaranteed that there is at least one picture Nauuo likes.
    # Also initial sum <= MOD - m.
    # 
    # Constraints: n <= 2e5, m <= 3000.
    # The DP state space size is m * m approx 9e6, which is acceptable for Python if optimized (C++ would be easy, Python needs care).
    # We only need to compute the sum of (prob * final_weight) for each picture.
    # For a liked picture i:
    # E[final_i] = w_i + E[number of times i is picked].
    # By symmetry, E[times i picked] / E[times any other liked picked] = w_i / w_j.
    # And sum_{i in liked} E[times i picked] = E[X] = sum_x (x * dp[m][x]).
    # Let Total_Liked_Expected_Increments = E[X].
    # Then E[final_i] = w_i * (1 + E[X] / total_liked).
    # Similarly for disliked:
    # Let Total_Disliked_Expected_Decrements = E[Y] = sum_{states} (number of disliked picks).
    # Number of disliked picks = k - x.
    # So E[Y] = sum_x ( (m - x) * dp[m][x] ).
    # Then E[final_j] = w_j - E[times j picked].
    # Sum of decreases = E[Y].
    # E[final_j] = w_j * (1 - E[Y] / total_disliked).
    #
    # So the algorithm:
    # 1. Run DP to find distribution of x (net increase in liked sum) after m steps.
    #    dp[x] = probability that liked sum increased by x.
    #    We can optimize space to 1D array since we only need previous step.
    # 2. Calculate E[X] = sum (x * dp[x]).
    # 3. Calculate E[Y] = sum ((m - x) * dp[x]).
    # 4. Compute scaling factors:
    #    factor_liked = 1 + E[X] * inv(total_liked)
    #    factor_disliked = 1 - E[Y] * inv(total_disliked)
    # 5. Output w[i] * factor_liked for liked, w[i] * factor_disliked for disliked.
    
    # Implementation details:
    # Max x is m. Min x can be negative? 
    # x is count of liked picks. Since we start with 0 liked picks relative to start, x >= 0.
    # But we also have constraint on disliked picks: cannot pick disliked if its total weight is 0.
    # Actually, the formula for prob of disliked pick involves (total_disliked - (k-x)).
    # If this becomes 0 or negative, the probability is 0.
    # So we must ensure k - x <= total_disliked => x >= k - total_disliked.
    # Also x <= k and x <= total_liked + (something)? No, x can go up to m + initial_liked? 
    # x here is the INCREASE in liked sum. So x <= m.
    # Also x >= 0.
    # So x in range [max(0, k - total_disliked), min(k, m)]. But since we iterate k from 0 to m, 
    # and x is bounded by k naturally in the loop if we start from 0.
    # However, the term (total_disliked - (k-x)) must be >= 0 for the transition to exist.
    # So k - x <= total_disliked => x >= k - total_disliked.
    # If k - total_disliked > k, impossible. But k <= m, total_disliked can be large.
    # If total_disliked is large, lower bound is 0.
    # If total_disliked is small, lower bound is positive.
    # We need to handle indices carefully.
    
    # Let's use an array `dp` of size m+1.
    # dp[x] stores probability that after current step, liked sum increased by x.
    # Initialize dp[0] = 1.0 (modular inverse for division later)
    
    dp = [0] * (m + 1)
    dp[0] = 1
    
    # We need modular arithmetic for all calculations.
    # Precompute modular inverses for denominators? Denominators change each step.
    # Denominator at step k, state x: S + 2x - k.
    # We can compute inverse on the fly. m is 3000, so 3000*3000 inverses is 9e6, might be slow in Python.
    # Total operations: sum of (range of x) over k. Sum of k is m^2/2 ~ 4.5e6.
    # 4.5e6 modular inverses might be too slow (each inverse is log(MOD) ~ 30 ops => 1.35e8 ops).
    # We need to optimize.
    # Notice that in step k, we iterate x. The denominator is D = S + 2x - k.
    # We can precompute inverses for all possible values of D?
    # Range of D:
    # Min D: S + 2*max(0, k-total_disliked) - k.
    # Max D: S + 2*m - m = S + m.
    # S <= MOD - m. So D < MOD.
    # The range of D is roughly [S - m, S + m]. Size ~ 2m = 6000.
    # We can precompute inverses for all numbers in [S - m, S + m] once!
    # S - m could be negative? No, S >= 1. But if S < m, lower bound could be negative?
    # Actually, D = total_sum + 2x - k.
    # Since x >= 0, k <= m, min D = total_sum - m (if x=0, k=m).
    # Since total_sum >= 1, and problem guarantees sum <= MOD - m, and also w_i >= 1.
    # Is it possible total_sum - m <= 0? Yes, if total_sum < m.
    # But probability denominator cannot be 0.
    # Does the process ever reach a state where total sum is 0?
    # No, because there is at least one liked picture with weight >= 1.
    # Even if we subtract from disliked, liked weight increases.
    # Total sum = Sum(liked) + Sum(disliked).
    # Sum(liked) >= 1 always (since at least one liked exists and it only increases).
    # So total sum >= 1 always.
    # So D >= 1.
    # So we need inverses for integers in [1, S + m].
    # Range size ~ 3000 + 3000 = 6000. Precomputing 6000 inverses is trivial.
    
    max_val = total_sum + m
    inv = [0] * (max_val + 1)
    inv[1] = 1
    for i in range(2, max_val + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
        
    # DP transitions
    for k in range(m):
        new_dp = [0] * (m + 1)
        # Determine valid range of x
        # x must be such that:
        # 1. We reached x at step k: dp[x] > 0
        # 2. Transitions valid:
        #    Disliked pick prob: (total_disliked - (k - x)) >= 0 => x >= k - total_disliked
        #    Also x <= k (obviously)
        #    Also x <= m (array bound)
        #    Also for next step, x+1 <= m
        
        # Let's find the actual range of x where dp[x] is non-zero.
        # Initially x=0.
        # At step k, x can be at most k.
        # Also x >= max(0, k - total_disliked).
        
        # Optimization: only iterate over non-zero dp[x]
        # Since m is small, we can just iterate all x from 0 to k.
        
        for x in range(k + 1):
            if dp[x] == 0:
                continue
            
            cur_prob = dp[x]
            
            # Current total sum
            current_total = total_sum + 2 * x - k
            
            # Liked part
            liked_sum_curr = total_liked + x
            if liked_sum_curr > 0:
                prob_liked = (liked_sum_curr * inv[current_total]) % MOD
                # Transition to x+1
                if x + 1 <= m:
                    term = (cur_prob * prob_liked) % MOD
                    new_dp[x + 1] = (new_dp[x + 1] + term) % MOD
            
            # Disliked part
            disliked_sum_curr = total_disliked - (k - x)
            if disliked_sum_curr > 0:
                prob_disliked = (disliked_sum_curr * inv[current_total]) % MOD
                # Transition to x (no change in x)
                term = (cur_prob * prob_disliked) % MOD
                new_dp[x] = (new_dp[x] + term) % MOD
        
        dp = new_dp
        
    # Calculate E[X] and E[Y]
    E_X = 0
    E_Y = 0
    for x in range(m + 1):
        if dp[x] == 0:
            continue
        px = dp[x]
        E_X = (E_X + x * px) % MOD
        E_Y = (E_Y + (m - x) * px) % MOD
        
    # Calculate factors
    # factor_liked = 1 + E[X] / total_liked
    # factor_disliked = 1 - E[Y] / total_disliked
    
    inv_total_liked = mod_inverse(total_liked, MOD)
    inv_total_disliked = mod_inverse(total_disliked, MOD)
    
    term_liked = (E_X * inv_total_liked) % MOD
    factor_liked = (1 + term_liked) % MOD
    
    term_disliked = (E_Y * inv_total_disliked) % MOD
    factor_disliked = (1 - term_disliked + MOD) % MOD
    
    # Construct result
    res = []
    for i in range(n):
        if a[i] == 1:
            val = (w[i] * factor_liked) % MOD
        else:
            val = (w[i] * factor_disliked) % MOD
        res.append(val)
        
    print(*(res))

if __name__ == '__main__':
    solve()