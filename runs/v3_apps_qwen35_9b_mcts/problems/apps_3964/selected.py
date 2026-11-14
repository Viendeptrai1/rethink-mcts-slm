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

    # dp[i][j][k] = number of ways to assign lines to first i programmers
    # such that total lines = j and total bugs = k
    # We can optimize space to 2D: dp[j][k]
    # dp[j][k] = number of ways to have exactly j lines and k bugs using some subset of programmers processed so far

    # Initialize dp table
    # dp[j][k] will store the count
    # Dimensions: (m+1) x (b+1)
    dp = [[0] * (b + 1) for _ in range(m + 1)]
    dp[0][0] = 1

    for x in a:
        # We iterate backwards to avoid using the same programmer multiple times for the same state in one step
        # However, since we are adding a new programmer who can write any number of lines (0 to remaining),
        # we need to update the dp table carefully.
        # Actually, the standard knapsack-like approach for "unbounded" items (here, a programmer can write multiple lines)
        # but with a constraint on total lines m.
        # Let's rethink:
        # We process programmers one by one. For the current programmer with bug rate x,
        # we can choose to have them write k lines (0 <= k <= m).
        # If they write k lines, they contribute k*x bugs.
        # So, new_dp[j][k] = sum(dp[j - i][k - i*x]) for all i from 0 to j, such that k - i*x >= 0.
        # This is O(n * m^2 * b) which is too slow (500^4 is huge).
        # We need a better approach.

        # Alternative DP state:
        # dp[i][j] = number of ways to assign lines to first i programmers such that total lines = j.
        # But we also need to track bugs.
        # Let dp[j][k] be the number of ways to have j lines and k bugs using a subset of programmers.
        # When considering a new programmer with bug rate x:
        # We can transition from any state (j_prev, k_prev) to (j_prev + i, k_prev + i*x) for i >= 0.
        # This looks like a convolution.
        # Notice that the bug contribution is linear with lines: if a programmer writes i lines, bugs = i*x.
        # So total bugs = sum(i_p * x_p) for each programmer p writing i_p lines.
        # Total lines = sum(i_p) = m.
        # We need to find the number of non-negative integer solutions to:
        # i_1 + i_2 + ... + i_n = m
        # such that sum(i_p * a_p) <= b.

        # This is equivalent to finding the coefficient of x^m * y^k (where k <= b) in the expansion of:
        # Product_{p=1 to n} (1 + y^{a_p} x + y^{2*a_p} x^2 + ... )
        # = Product_{p=1 to n} (1 / (1 - x * y^{a_p}))
        # We only care about terms where the power of x is m and power of y is <= b.

        # Let's use DP where dp[i][j] = number of ways to have total lines = i and total bugs = j.
        # Initialize dp[0][0] = 1, others 0.
        # For each programmer with bug rate x:
        #   new_dp[i][j] = sum(dp[i - k][j - k*x]) for k >= 0
        # This is still O(m^2 * b) per programmer -> O(n * m^2 * b) ~ 500^4 = 6.25e10, too slow.

        # Optimization:
        # Notice that for a fixed programmer with rate x, the transition is:
        # new_dp[i][j] = dp[i][j] + new_dp[i-1][j-x]
        # Why?
        # Consider the contribution of the current programmer. They can write 0 lines, 1 line, 2 lines, ...
        # If they write k lines, we add k*x bugs.
        # Let dp[i][j] be the number of ways using a subset of programmers to get i lines and j bugs.
        # When adding a new programmer with rate x:
        # Let new_dp[i][j] be the updated value.
        # new_dp[i][j] = sum_{k=0 to i} dp[i-k][j - k*x]
        # Let's see the recurrence:
        # new_dp[i][j] = dp[i][j] + new_dp[i-1][j-x]
        # Proof:
        # new_dp[i][j] = dp[i][j] + dp[i-1][j-x] + dp[i-2][j-2x] + ... + dp[0][j-i*x]
        # new_dp[i-1][j-x] = dp[i-1][j-x] + dp[i-2][j-2x] + ... + dp[0][j-(i-1)x - x] = dp[i-1][j-x] + ... + dp[0][j-i*x]
        # So new_dp[i][j] = dp[i][j] + new_dp[i-1][j-x]
        # This reduces the complexity to O(n * m * b).
        # 500 * 500 * 500 = 125,000,000, which is acceptable for Python if implemented efficiently.

        # We can do this in-place if we iterate carefully.
        # We need to update dp[i][j] using values from the previous iteration (before this programmer).
        # But the recurrence new_dp[i][j] = dp[i][j] + new_dp[i-1][j-x] suggests we can compute row by row.
        # However, since new_dp depends on new_dp[i-1], we can update in place if we iterate i from 1 to m.
        # But we must be careful not to use the updated value of the current programmer for the same programmer again incorrectly?
        # Actually, the recurrence new_dp[i][j] = dp[i][j] + new_dp[i-1][j-x] is correct for the cumulative sum.
        # Let's verify:
        # Suppose we have processed k programmers. dp[i][j] is the count.
        # Now we process programmer k+1 with rate x.
        # Let f[i][j] be the new count.
        # f[i][j] = sum_{p=0}^{i} dp[i-p][j - p*x]
        # f[i-1][j-x] = sum_{p=0}^{i-1} dp[i-1-p][j-x - p*x] = sum_{q=1}^{i} dp[i-q][j - q*x] (let q = p+1)
        # So f[i][j] = dp[i][j] + f[i-1][j-x].
        # This holds.
        # So we can update the dp table in place.
        # We need to iterate i from 1 to m, and for each i, iterate j from x to b.
        # dp[i][j] = (dp[i][j] + dp[i-1][j-x]) % mod
        # But wait, dp[i][j] on the RHS is the old value (from previous programmers), and dp[i-1][j-x] is the NEW value (already updated for current programmer).
        # Yes, that's exactly what we want.
        # So the algorithm:
        # Initialize dp[0][0] = 1, others 0.
        # For each programmer with bug rate x:
        #   For i from 1 to m:
        #     For j from x to b:
        #       dp[i][j] = (dp[i][j] + dp[i-1][j-x]) % mod
        # Finally, sum dp[m][j] for j from 0 to b.

        # Let's trace with an example.
        # n=1, m=1, b=1, a=[1]
        # dp[0][0]=1, others 0.
        # x=1.
        # i=1:
        #   j=1: dp[1][1] = dp[1][1] + dp[0][0] = 0 + 1 = 1.
        # Result: sum(dp[1][0..1]) = dp[1][0] + dp[1][1] = 0 + 1 = 1. Correct.

        # Example 2: n=2, m=1, b=1, a=[1, 1]
        # Init: dp[0][0]=1.
        # Programmer 1 (x=1):
        #   i=1, j=1: dp[1][1] += dp[0][0] -> 1.
        # Programmer 2 (x=1):
        #   i=1, j=1: dp[1][1] += dp[0][0] -> 1 + 1 = 2.
        # Result: 2. Correct (programmer 1 writes 1 line, or programmer 2 writes 1 line).

        # Example 3: n=2, m=2, b=1, a=[1, 1]
        # Init: dp[0][0]=1.
        # Prog 1 (x=1):
        #   i=1, j=1: dp[1][1] += dp[0][0] -> 1.
        #   i=2, j=2: out of bounds for b=1? No, j goes up to b. So j=2 is skipped.
        #   Wait, if m=2, b=1, then we can't have 2 bugs.
        #   So for i=2, j must be <= 1. But j-x = 2-1=1, so j=1?
        #   Let's re-run carefully.
        #   i=1: j=1 -> dp[1][1] = 1.
        #   i=2: j=1 -> dp[2][1] = dp[2][1] + dp[1][0]. dp[1][0] is 0. So dp[2][1]=0.
        # Prog 2 (x=1):
        #   i=1: j=1 -> dp[1][1] += dp[0][0] = 1+1=2.
        #   i=2: j=1 -> dp[2][1] += dp[1][0] = 0+0=0.
        # Result: dp[2][0]+dp[2][1] = 0+0=0. Correct (min bugs for 2 lines with 2 programmers of rate 1 is 2).

        # The logic seems sound.

        for i in range(1, m + 1):
            for j in range(x, b + 1):
                dp[i][j] = (dp[i][j] + dp[i-1][j-x]) % mod

    ans = sum(dp[m]) % mod
    print(ans)

if __name__ == '__main__':
    solve()