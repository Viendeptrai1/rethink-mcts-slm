import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    MOD = 10**9 + 7

    # Precompute factorials and inverse factorials for combinations
    MAX = N + 1
    fact = [1] * MAX
    inv = [1] * MAX
    for i in range(2, MAX):
        fact[i] = (fact[i-1] * i) % MOD
    inv[MAX-1] = pow(fact[MAX-1], MOD - 2, MOD)
    for i in range(MAX-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    results = []
    for i in range(1, K + 1):
        # We need exactly i groups of blue balls.
        # This means we place i groups of blue balls into the sequence.
        # There are i+1 gaps (before first, between groups, after last) for red balls.
        # Let x_0, x_1, ..., x_i be the number of red balls in each gap.
        # Sum(x_j) = N - K, with x_j >= 0.
        # Number of ways to distribute red balls = C((N-K) + (i+1) - 1, (i+1) - 1) = C(N-K+i, i)
        # However, we must ensure that no two blue groups are adjacent.
        # Actually, the standard stars and bars approach for "exactly i groups" works as follows:
        # We treat each group of blue balls as a single item. But the size of the group matters?
        # No, the problem says "collect any number of consecutive blue balls".
        # So if we have B B R B, the groups are (BB) and (B). That's 2 moves.
        # The internal arrangement of blue balls within a group doesn't matter (indistinguishable).
        # The key is: we need to form exactly i contiguous blocks of blue balls.
        # This is equivalent to choosing i positions for the "starts" of the blue blocks such that
        # no two starts are adjacent (if we consider single balls) but here blocks can be larger.
        #
        # Correct combinatorial model:
        # We have K blue balls and N-K red balls.
        # We want exactly i groups of blue balls.
        # This implies there are i-1 "gaps" between blue groups that MUST contain at least one red ball.
        # The other gaps (before first group, after last group, and between groups where we don't force a red)
        # can have zero or more red balls.
        #
        # Let's reframe:
        # We are placing i groups of blue balls. Let the sizes of these groups be b_1, b_2, ..., b_i.
        # Sum(b_j) = K, with b_j >= 1.
        # The number of ways to partition K into i positive integers is C(K-1, i-1).
        # Now we have i blocks of blue balls and (N-K) red balls.
        # We need to arrange these such that the i blue blocks are separated by at least one red ball.
        # Consider the i blue blocks as items. We need to place them into a sequence with red balls.
        # To ensure exactly i groups, we must have at least one red ball between any two blue blocks.
        # So we reserve (i-1) red balls to separate the i blue blocks.
        # Remaining red balls = (N-K) - (i-1).
        # If (N-K) < (i-1), then it's impossible (0 ways).
        # Now we have (N-K) - (i-1) red balls to distribute freely into the (i+1) gaps (before, between, after).
        # Wait, the "between" gaps already have 1 reserved red ball. We can add more.
        # So effectively, we have (i+1) bins for the remaining red balls.
        # Number of ways to distribute R' = (N-K) - (i-1) red balls into (i+1) bins is C(R' + (i+1) - 1, (i+1) - 1) = C(N-K-i+1 + i, i) = C(N-K+1, i).
        #
        # Total ways = (Ways to partition K into i groups) * (Ways to arrange groups with red balls)
        #            = C(K-1, i-1) * C(N-K+1, i)
        #
        # Let's verify with sample: N=5, K=3.
        # i=1: C(2,0)*C(3,1) = 1*3 = 3. Correct.
        # i=2: C(2,1)*C(3,2) = 2*3 = 6. Correct.
        # i=3: C(2,2)*C(3,3) = 1*1 = 1. Correct.
        #
        # Constraints: 1 <= i <= K. Also need N-K >= i-1.
        # If N-K < i-1, then C(N-K+1, i) will be 0 because N-K+1 < i (since N-K < i-1 => N-K+1 <= i-1 < i).
        # So the formula holds naturally if we handle nCr correctly for n < r.

        term1 = nCr(K - 1, i - 1)
        term2 = nCr(N - K + 1, i)
        ans = (term1 * term2) % MOD
        results.append(ans)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()