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

    # dp[i][j][k] = number of ways to assign exactly i lines of code
    #              with exactly j bugs in total, using a subset of programmers.
    # However, we can optimize space by iterating over programmers and updating
    # a 2D DP table: dp[j][k] = number of ways to have j lines and k bugs.
    # We need to be careful with the order of updates to avoid using the same programmer multiple times for the same line count in one step.
    # Actually, the standard knapsack-like approach works here:
    # Let dp[j][k] be the number of ways to write exactly j lines with exactly k bugs using a subset of the first p programmers.
    # When considering the (p+1)-th programmer who writes x lines (contributing x*a[p] bugs),
    # we update: new_dp[j+x][k + x*a[p]] += dp[j][k]
    # Since we can choose any non-negative integer x for each programmer, this is equivalent to:
    # For each programmer, we can add 0, 1, 2, ... lines.
    # This is similar to the unbounded knapsack problem but with two constraints (lines and bugs).
    # However, note that the order of programmers matters in the sense that we are assigning specific counts to specific programmers.
    # But the problem asks for the number of sequences (v_1, v_2, ..., v_n) such that sum(v_i)=m and sum(v_i * a_i) <= b.
    # This is exactly equivalent to: for each programmer i, choose v_i >= 0, such that sum(v_i) = m and sum(v_i * a_i) <= b.
    # We can use dynamic programming where we process programmers one by one.
    # Let dp[j][k] = number of ways to assign lines to the first p programmers such that total lines = j and total bugs = k.
    # Transition: dp_new[j + x][k + x * a[p]] += dp_old[j][k] for all x >= 0.
    # Since m and b are up to 500, we can iterate x from 0 to m (or until j+x > m).
    # But note: iterating x for each state might be O(m^2 * b) per programmer, leading to O(n * m^2 * b) which is 500^4 = 6.25e10, too slow.
    # We need a better transition.
    # Notice that the transition for a fixed programmer p with bug rate a_p is:
    # dp[j][k] = sum_{x>=0} dp_old[j-x][k - x*a_p]
    # This looks like a convolution, but we can optimize by noticing that for a fixed j and k, we are summing over x.
    # Alternatively, we can reverse the thinking: instead of iterating x, we can update the DP table in a way similar to the unbounded knapsack.
    # In the unbounded knapsack, for an item with weight w and value v, we do:
    #   for j from w to M: dp[j] = (dp[j] + dp[j-w]) % mod
    # Here, we have two dimensions: lines (j) and bugs (k).
    # The "weight" in terms of lines is x, and the "weight" in terms of bugs is x * a_p.
    # But x can be any non-negative integer. So if we consider adding one line by programmer p, it adds 1 to the line count and a_p to the bug count.
    # We can do this repeatedly. So for programmer p, we can update the DP table by:
    #   for j from 1 to m:
    #       for k from a_p to b:
    #           dp[j][k] = (dp[j][k] + dp[j-1][k-a_p]) % mod
    # Why? Because if we have a way to form (j-1, k-a_p) using the first p-1 programmers, then adding one line by programmer p gives (j, k).
    # And since we can add multiple lines by programmer p, we can do this in increasing order of j and k, effectively allowing multiple lines from the same programmer.
    # This is exactly the unbounded knapsack update in 2D.
    # The complexity will be O(n * m * b), which is 500^3 = 125e6, acceptable in Python if implemented efficiently (using PyPy or careful optimization).
    # Given the constraints and typical time limits, we should try to optimize the inner loops.

    # Initialize dp table: dp[j][k] = number of ways to have j lines and k bugs using a subset of programmers processed so far.
    # Initially, with 0 programmers, we have 1 way to have 0 lines and 0 bugs, and 0 ways otherwise.
    dp = [[0] * (b + 1) for _ in range(m + 1)]
    dp[0][0] = 1

    for i in range(n):
        cost = a[i]
        # Update dp table for the current programmer
        # We iterate j from 1 to m, and k from cost to b.
        # dp[j][k] += dp[j-1][k-cost]
        # We do this in increasing order of j and k to allow multiple lines from the same programmer.
        for j in range(1, m + 1):
            for k in range(cost, b + 1):
                dp[j][k] = (dp[j][k] + dp[j-1][k-cost]) % mod

    # The answer is the sum of dp[m][k] for all k from 0 to b.
    ans = 0
    for k in range(b + 1):
        ans = (ans + dp[m][k]) % mod

    print(ans)

if __name__ == '__main__':
    solve()