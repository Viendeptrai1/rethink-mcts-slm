import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))
    b = int(next(iterator))
    mod = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
    
    # dp[j][k] = number of ways to assign j lines of code with exactly k bugs
    # We can optimize space to use a 1D array for the number of lines, but we need two states: lines and bugs.
    # Actually, we need dp[lines][bugs]. Since m and b are up to 500, a 2D array of size (m+1) x (b+1) is feasible.
    # However, we iterate over programmers. For each programmer, we update the dp table.
    # Let dp[i][j] be the number of ways to have j bugs after considering some programmers and some total lines?
    # No, the constraint is on total lines = m and total bugs <= b.
    # We need to track both total lines and total bugs.
    # Let dp[j][k] = number of ways to write exactly j lines with exactly k bugs using a subset of programmers considered so far.
    # Dimensions: j from 0 to m, k from 0 to b.
    # Initialize dp[0][0] = 1, others 0.
    # For each programmer with bug rate 'val':
    #   new_dp[j][k] = sum(dp[j-x][k - x*val]) for x from 0 to j
    # This is a knapsack-like problem where each item (programmer) can be chosen multiple times (0 to m times) 
    # but the "weight" is the number of lines (1 per line) and "cost" is bugs (val per line).
    # Actually, it's unbounded knapsack in terms of lines, but bounded by m lines total.
    # Order of iteration:
    # Iterate programmers p from 1 to n.
    #   For each programmer, we can choose to write v lines (0 <= v <= m).
    #   Cost in bugs = v * a[p].
    #   We update dp[j][k] by adding dp[j-v][k - v*a[p]].
    # To optimize, we can iterate j from m down to 0? No, because we can use the same programmer multiple times.
    # Wait, the problem says "sequence v_1, ..., v_n". The order of programmers is fixed.
    # Programmer 1 writes v_1 lines, Programmer 2 writes v_2 lines, etc.
    # This means for each programmer, we decide how many lines they write.
    # So it is exactly: for each programmer, we can add v lines (0 <= v <= remaining lines).
    # This is equivalent to: dp[j][k] = sum over v of dp[j-v][k - v*a[i]] where v is lines assigned to current programmer.
    # Since the programmers are processed in a fixed order, we update the table sequentially.
    # For a specific programmer with bug rate 'val':
    #   new_dp[j][k] = sum_{v=0 to j} dp[j-v][k - v*val]
    # This looks like O(m^2 * b) per programmer, total O(n * m^2 * b) which is 500^4 ~ 6.25e10, too slow.
    # We need a better transition.
    # Notice that dp[j][k] for the current step depends on dp[j-v][k - v*val].
    # Let's fix the number of lines j and iterate v.
    # Actually, we can rephrase: 
    # dp[j][k] = number of ways to have j lines and k bugs after processing current programmer.
    # Transition: dp[j][k] = sum_{v=0}^{j} (ways from previous programmers with j-v lines and k - v*val bugs)
    # This is a convolution. But notice the structure:
    # dp_new[j][k] = dp_old[j][k] + dp_new[j-1][k-val] ???
    # Let's check:
    # If we assign v lines to current programmer, then we take a state from previous programmers with j-v lines and k - v*val bugs.
    # Let's try to optimize the transition for a fixed programmer with cost 'val' per line.
    # Let f[j][k] be the number of ways after current programmer.
    # f[j][k] = sum_{v=0}^{j} g[j-v][k - v*val] where g is the table from previous programmers.
    # Notice that f[j][k] = g[j][k] + f[j-1][k-val] ?
    # Let's verify:
    # f[j][k] = g[j][k] (v=0) + g[j-1][k-val] (v=1) + g[j-2][k-2*val] (v=2) + ... + g[0][k-j*val] (v=j)
    # f[j-1][k-val] = g[j-1][k-val] (v=0) + g[j-2][k-2*val] (v=1) + ... + g[0][k-(j-1)*val] (v=j-1)
    # So f[j][k] = g[j][k] + f[j-1][k-val].
    # Yes! This holds.
    # Base case: f[0][k] = g[0][k] for all k (since v must be 0 if j=0).
    # And for j > 0, f[j][k] = (g[j][k] if k >= 0 else 0) + (f[j-1][k-val] if k >= val else 0).
    # Wait, we need to be careful with indices.
    # f[j][k] depends on f[j-1][k-val].
    # We can compute this in place if we iterate j from 1 to m, and for each j, iterate k from val to b.
    # But we need the values from the previous iteration (g) for the term g[j][k].
    # So we need two tables or careful iteration order.
    # Since f[j][k] depends on f[j-1], we can iterate j from 1 to m.
    # For a fixed j, f[j][k] = g[j][k] + f[j-1][k-val].
    # We can maintain a single table `dp` where dp[j][k] stores the current values.
    # When updating for a new programmer, we need to update dp[j][k] using the old dp[j][k] (which is g[j][k]) and the newly computed dp[j-1][k-val].
    # If we iterate j from 1 to m, then when we are at j, dp[j-1] has already been updated to f[j-1].
    # And dp[j] currently holds g[j].
    # So the update rule:
    #   for j from 1 to m:
    #       for k from val to b:
    #           dp[j][k] = (dp[j][k] + dp[j-1][k-val]) % mod
    # But wait, what about k < val?
    # If k < val, then v*val <= k implies v=0 only.
    # So f[j][k] = g[j][k]. The loop for k from val to b covers the v>=1 cases. The v=0 case is implicitly kept in dp[j][k] before update?
    # No, dp[j][k] initially is g[j][k]. We add the contributions from v>=1.
    # The contribution from v=1 is g[j-1][k-val].
    # The contribution from v=2 is g[j-2][k-2*val] which is part of f[j-1][k-2*val]?
    # Let's re-verify the recurrence: f[j][k] = g[j][k] + f[j-1][k-val].
    # f[j-1][k-val] = g[j-1][k-val] + f[j-2][k-2*val] = g[j-1][k-val] + g[j-2][k-2*val] + ...
    # So yes, f[j][k] = g[j][k] + g[j-1][k-val] + g[j-2][k-2*val] + ...
    # This matches the sum over v.
    # So the algorithm is:
    # Initialize dp[0][0] = 1, all others 0.
    # For each programmer with bug rate 'val':
    #   For j from 1 to m:
    #     For k from val to b:
    #       dp[j][k] = (dp[j][k] + dp[j-1][k-val]) % mod
    #   Note: dp[0][k] remains unchanged because if j=0, we must assign 0 lines to current programmer.
    #   Also, we need to handle the case where val=0. If val=0, then k-val = k.
    #   If val=0, then f[j][k] = g[j][k] + f[j-1][k].
    #   This means if a programmer makes 0 bugs, any number of lines they write doesn't increase bug count.
    #   The recurrence still holds: f[j][k] = g[j][k] + f[j-1][k].
    #   However, if val=0, we must be careful not to use the updated f[j-1][k] which might include the current programmer's contribution for j-1 lines?
    #   Yes, that's the point. f[j-1][k] already includes the case where the current programmer wrote (j-1) lines.
    #   So adding f[j-1][k] to g[j][k] correctly adds the cases where current programmer wrote 1 line (g[j-1][k]) plus cases where they wrote >1 lines (via f[j-1][k]).
    #   So the same loop works for val=0 as well.
    #   One caveat: if val=0, the inner loop runs from 0 to b.
    #   Order of j: 1 to m.
    #   Order of k: 0 to b (if val=0) or val to b (if val>0).
    #   Is it possible that updating dp[j][k] affects dp[j][k] later in the same j loop? No, k is independent for fixed j.
    #   Does updating dp[j][k] affect dp[j+1][...]? No, j increases.
    #   Does updating dp[j][k] affect dp[j][k']? No.
    #   The only dependency is dp[j-1][...]. Since we iterate j from 1 to m, dp[j-1] is already fully updated for the current programmer.
    #   So this is correct.

    # Dimensions: (m+1) x (b+1)
    dp = [[0] * (b + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    
    for val in a:
        # We need to update dp table in place.
        # Iterate j from 1 to m
        # Iterate k from val to b (if val > 0), else 0 to b
        # Optimization: if val == 0, range is 0 to b.
        start_k = 0 if val == 0 else val
        for j in range(1, m + 1):
            for k in range(start_k, b + 1):
                # dp[j][k] currently holds g[j][k]
                # We add f[j-1][k-val] which is stored in dp[j-1][k-val]
                if k >= val:
                    dp[j][k] = (dp[j][k] + dp[j-1][k - val]) % mod
                # else: k < val, then v*val <= k implies v=0 only, so no addition needed.
    
    # The answer is the sum of dp[m][k] for all k from 0 to b.
    ans = 0
    for k in range(b + 1):
        ans = (ans + dp[m][k]) % mod
    
    print(ans)

if __name__ == '__main__':
    solve()