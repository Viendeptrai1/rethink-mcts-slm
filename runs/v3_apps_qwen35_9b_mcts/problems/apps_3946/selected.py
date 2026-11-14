import sys

# Increase recursion depth just in case, though we will use iterative DP
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
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

    MOD = 998244353

    # Separate weights into liked (1) and disliked (0)
    liked_weights = []
    disliked_weights = []
    
    for i in range(n):
        if a[i] == 1:
            liked_weights.append(w[i])
        else:
            disliked_weights.append(w[i])
            
    sum_liked = sum(liked_weights)
    sum_disliked = sum(disliked_weights)
    
    # Precompute modular inverse for numbers up to m + max_initial_weight?
    # Actually, we only need inverses for the total sums which change.
    # The total sum of liked group goes from sum_liked to sum_liked + m.
    # The total sum of disliked group goes from sum_disliked to sum_disliked + m (if all picked) or sum_disliked (if none picked).
    # Wait, the total sum of ALL pictures changes.
    # If a liked picture is picked, total sum increases by 1.
    # If a disliked picture is picked, total sum decreases by 1.
    # However, the probability of picking a specific group depends on the sum of that group vs the total sum.
    # P(liked) = sum_liked_current / total_sum_current
    # P(disliked) = sum_disliked_current / total_sum_current
    
    # Let's re-evaluate the DP state.
    # dp[i][j] = probability that after i steps, the liked group has been selected j times.
    # i ranges from 0 to m.
    # j ranges from 0 to i.
    
    # Initial state:
    # dp[0][0] = 1.0 (modular 1)
    
    # Transitions:
    # At step i (having done i steps), if we have selected liked group j times:
    # Current sum_liked = sum_liked_initial + j
    # Current sum_disliked = sum_disliked_initial + (i - j) * (-1) = sum_disliked_initial - (i - j)
    # Wait, if disliked is picked, weight decreases by 1. So sum_disliked decreases.
    # Correct: sum_disliked_current = sum_disliked_initial - (i - j)
    
    # Total sum = sum_liked_current + sum_disliked_current
    # = (sum_liked_initial + j) + (sum_disliked_initial - (i - j))
    # = sum_liked_initial + sum_disliked_initial + j - i + j
    # = Total_Initial + 2*j - i
    
    # Probability of picking liked next: P_L = sum_liked_current / Total_current
    # Probability of picking disliked next: P_D = sum_disliked_current / Total_current
    
    # We need modular inverse for Total_current.
    # Total_current = Total_Initial + 2*j - i.
    # Since m <= 3000, the range of Total_current is within [Total_Initial - m, Total_Initial + m].
    # We can precompute inverses for these values.
    
    total_initial = sum_liked + sum_disliked
    
    # Determine the range of possible total sums
    min_total = total_initial - m
    max_total = total_initial + m
    
    # Precompute inverses
    inv = [0] * (max_total - min_total + 1)
    offset = -min_total
    
    # Function to compute modular inverse
    def power(a, b, m):
        res = 1
        a %= m
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % m
            a = (a * a) % m
            b //= 2
        return res

    # Compute inverses for the range
    # Since the range size is at most 2*m + 1 = 6001, we can compute each in O(log MOD)
    # Or use linear precomputation. Given constraints, O(m log MOD) is fine (3000 * 30 ops).
    
    for k in range(min_total, max_total + 1):
        inv[k + offset] = power(k, MOD - 2, MOD)
        
    # DP initialization
    # dp[j] will store the probability that after current step, liked group was picked j times.
    # We can use two rows or update in place carefully. Let's use a list of size m+1.
    
    dp = [0] * (m + 1)
    dp[0] = 1
    
    # We also need to track the expected number of times the liked group is picked?
    # No, we need the full distribution to compute the final expected weights correctly?
    # Actually, the formula for expected final weight of a specific liked picture i is:
    # E[W_i_final] = w_i + w_i * (E[K] / sum_liked_initial)
    # where K is the random variable for number of times liked group is picked.
    # Is this correct?
    # Let's verify.
    # Consider Polya's Urn. If we have a group with total weight S, and we pick an item from this group,
    # the weight of that item increases by 1.
    # The expected increase in weight of item i given that the group was picked k times is w_i * k / S.
    # This is because each time the group is picked, the probability that item i is the specific one picked is w_i / S_current.
    # But S_current changes.
    # However, there is a known result for this specific problem (Codeforces 1172B / Nauuo and Pictures):
    # The expected final weight of picture i (if liked) is w_i * (1 + E[K] / S_L_initial).
    # Wait, let's derive it properly.
    # Let X_t be the indicator that picture i is picked at step t.
    # W_i_final = w_i + sum(X_t).
    # E[W_i_final] = w_i + sum(E[X_t]).
    # E[X_t] = P(picture i is picked at step t).
    # P(picture i is picked at step t) = P(group liked is picked at step t) * P(picture i | group liked picked at step t).
    # Given the group liked is picked, the probability it is picture i is w_i / S_L_current.
    # This looks complicated because S_L_current depends on previous picks.
    # BUT, there is a symmetry argument.
    # Consider the process restricted to the liked group. It behaves like a Polya Urn where every time ANY member of the group is picked, the total weight of the group increases by 1.
    # In a standard Polya Urn with initial weights w_1, ..., w_k and adding 1 to the chosen ball:
    # The probability that ball i is chosen at any step t (given the process hasn't stopped) is w_i / S_initial.
    # This is a property of Polya Urn: the probability of picking a specific ball is constant throughout the process!
    # Proof sketch: By symmetry or martingale properties.
    # If this property holds, then E[X_t] = w_i / S_L_initial * P(group liked is picked at step t).
    # Then E[W_i_final] = w_i + sum_{t=1 to m} (w_i / S_L_initial * P(group liked picked at step t))
    # = w_i + (w_i / S_L_initial) * sum_{t=1 to m} P(group liked picked at step t)
    # = w_i + (w_i / S_L_initial) * E[K]
    # where K is the total number of times the liked group is picked.
    # Yes! This simplifies the problem immensely. We just need E[K].
    # Similarly for disliked pictures:
    # When a disliked picture is picked, its weight decreases by 1.
    # The process for the disliked group is similar but with -1.
    # The probability that a specific disliked picture j is picked at step t, given the disliked group is picked, is w_j / S_D_current.
    # Does the constant probability property hold for the "decreasing" urn?
    # Yes, by similar symmetry arguments (or linearity of expectation on the martingale).
    # The probability that picture j is picked at step t is (w_j / S_D_initial) * P(group disliked picked at step t).
    # So E[W_j_final] = w_j - sum_{t=1 to m} (w_j / S_D_initial * P(group disliked picked at step t))
    # = w_j - (w_j / S_D_initial) * E[m - K]
    # = w_j - (w_j / S_D_initial) * (m - E[K])
    
    # So the algorithm is:
    # 1. Compute E[K] using DP.
    # 2. Compute E[m-K] = m - E[K].
    # 3. For each liked picture i: ans = w_i * (1 + E[K] / S_L_initial)
    # 4. For each disliked picture i: ans = w_i * (1 - (m - E[K]) / S_D_initial)
    
    # DP to compute E[K]:
    # dp[j] = probability that after current step, liked group was picked j times.
    # Initially dp[0] = 1.
    # Iterate step t from 1 to m:
    #   new_dp = [0]*(m+1)
    #   For j from 0 to t-1:
    #     current_prob_liked = (sum_liked + j) * inv[total_initial + 2*j - (t-1)]
    #     current_prob_disliked = (sum_disliked - (t-1 - j)) * inv[total_initial + 2*j - (t-1)]
    #     # Transition from state j at step t-1 to j at step t (disliked picked)
    #     # Transition from state j at step t-1 to j+1 at step t (liked picked)
    #     # Note: inv array index: total = total_initial + 2*j - (t-1)
    #     # Let's be careful with indices.
    #     # At start of step t (0-indexed steps 0..m-1), we have done t steps? No.
    #     # Let's say we are computing step t (1-based), meaning we go from t-1 to t.
    #     # Current state is after t-1 steps. Liked picked j times.
    #     # Total sum at this moment: S = total_initial + 2*j - (t-1)
    #     # P(liked) = (sum_liked + j) / S
    #     # P(disliked) = (sum_disliked - (t-1 - j)) / S
    #     # Update new_dp[j] += dp[j] * P(disliked)
    #     # Update new_dp[j+1] += dp[j] * P(liked)
    
    # Optimization: We only need E[K] = sum(j * dp[j]).
    # But we need the full distribution to compute E[K] iteratively?
    # Yes, because the probabilities change.
    # However, m is small (3000), so O(m^2) is 9*10^6, which is acceptable in Python if optimized.
    
    # Let's implement the DP.
    
    # dp[j] stores probability after 'step' iterations
    dp = [0.0] * (m + 1) # Using floats for logic, but we need modular arithmetic.
    # Actually, we must do everything in modular arithmetic.
    dp = [0] * (m + 1)
    dp[0] = 1
    
    # We will maintain the current expected value of K? No, we need the distribution to update probabilities.
    # But wait, do we need the full distribution?
    # To compute E[K], we can just maintain the expected value?
    # E[K_t] = E[K_{t-1}] + P(liked picked at step t).
    # P(liked picked at step t) = sum_j P(state j at t-1) * P(liked | state j).
    # P(liked | state j) = (sum_liked + j) / S_j.
    # This depends on j. So we cannot just use E[K_{t-1}]. We need the distribution or at least the sum of (j * P(state j)).
    # Let E_t = sum_j (j * dp[j]). This is E[K] after t steps.
    # But to compute P(liked at t+1), we need sum_j (dp[j] * (sum_liked + j) / S_j).
    # This term is not linear in j because of the denominator S_j.
    # So we DO need the full distribution dp[j].
    
    # Given m=3000, O(m^2) is fine.
    
    current_dp = [0] * (m + 1)
    current_dp[0] = 1
    
    # We can optimize space by using two arrays.
    prev_dp = [0] * (m + 1)
    prev_dp[0] = 1
    
    for t in range(1, m + 1):
        curr_dp = [0] * (m + 1)
        # We iterate j from 0 to t-1 (max possible liked picks so far)
        # At step t (1-based), we are transitioning from t-1 steps.
        # Max j is t-1.
        
        # Precompute denominators?
        # S = total_initial + 2*j - (t-1)
        # We need inv[S].
        
        for j in range(t):
            if prev_dp[j] == 0:
                continue
            
            # Current total sum
            S = total_initial + 2*j - (t - 1)
            inv_S = inv[S + offset]
            
            w_liked_curr = sum_liked + j
            w_disliked_curr = sum_disliked - (t - 1 - j)
            
            prob_liked = (w_liked_curr * inv_S) % MOD
            prob_disliked = (w_disliked_curr * inv_S) % MOD
            
            # Transition to j (disliked picked)
            term = (prev_dp[j] * prob_disliked) % MOD
            curr_dp[j] = (curr_dp[j] + term) % MOD
            
            # Transition to j+1 (liked picked)
            term = (prev_dp[j] * prob_liked) % MOD
            curr_dp[j+1] = (curr_dp[j+1] + term) % MOD
            
        prev_dp = curr_dp
        
    # Calculate E[K]
    E_K = 0
    for j in range(m + 1):
        E_K = (E_K + j * prev_dp[j]) % MOD
        
    # Calculate answers
    # For liked: w_i * (1 + E_K / sum_liked)
    # For disliked: w_i * (1 - (m - E_K) / sum_disliked)
    
    # Precompute modular inverses for sum_liked and sum_disliked
    inv_sum_liked = power(sum_liked, MOD - 2, MOD)
    inv_sum_disliked = power(sum_disliked, MOD - 2, MOD)
    
    # Term for liked: 1 + E_K * inv_sum_liked
    term_liked = (1 + E_K * inv_sum_liked) % MOD
    
    # Term for disliked: 1 - (m - E_K) * inv_sum_disliked
    # Note: m - E_K is the expected number of times disliked group was picked.
    # Let E_D = (m - E_K) % MOD
    E_D = (m - E_K) % MOD
    term_disliked = (1 - E_D * inv_sum_disliked) % MOD
    
    results = []
    for i in range(n):
        if a[i] == 1:
            ans = (w[i] * term_liked) % MOD
        else:
            ans = (w[i] * term_disliked) % MOD
        results.append(str(ans))
        
    print(" ".join(results))

if __name__ == '__main__':
    solve()