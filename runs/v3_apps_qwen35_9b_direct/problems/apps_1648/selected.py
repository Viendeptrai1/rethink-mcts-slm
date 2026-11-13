import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    MOD = 10**9 + 7

    # Precompute factorials and inverse factorials for combinations
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # dp[i][j] = number of ways to arrange j blue balls into i groups (moves)
    # such that no two groups are adjacent (at least one red between them).
    # We will compute this for j from 1 to K.
    # However, we need to consider the total number of red balls as well.
    # Let's reframe:
    # We have K blue balls and R = N - K red balls.
    # We want to form exactly i groups of blue balls.
    # This means we place i groups of blue balls into the sequence, separated by at least one red ball.
    # Also, the sequence can start or end with blue balls.
    #
    # Model:
    # We have i groups of blue balls. Let the sizes be b1, b2, ..., bi where each bj >= 1 and sum(bj) = K.
    # We need to place these i groups into the sequence of N balls such that no two groups are adjacent.
    # This is equivalent to placing i items (the groups) into the "gaps" created by the red balls, 
    # but we must ensure that if we place two groups in the same gap, they are separated by at least one red ball? 
    # Actually, the standard way is:
    # Consider the R red balls. They create R+1 gaps (including ends).
    # We need to place i groups of blue balls into these R+1 gaps such that no two groups are in the same gap? 
    # No, if we put multiple groups in the same gap, they would be adjacent unless separated by red balls, 
    # but there are no red balls inside a gap. So each gap can hold at most one group of blue balls.
    # Therefore, we must choose i distinct gaps out of R+1 gaps to place the i groups.
    # The number of ways to choose the gaps is C(R+1, i).
    # Then, we need to distribute the K blue balls into these i groups, where each group has at least 1 ball.
    # The number of ways to partition K identical items into i non-empty ordered groups is C(K-1, i-1).
    #
    # So the total ways for a fixed i is: C(R+1, i) * C(K-1, i-1).
    #
    # Let's verify with sample: N=5, K=3 => R=2.
    # i=1: C(3,1)*C(2,0) = 3*1 = 3. Correct.
    # i=2: C(3,2)*C(2,1) = 3*2 = 6. Correct.
    # i=3: C(3,3)*C(2,2) = 1*1 = 1. Correct.
    #
    # Constraints: 1 <= i <= K. Also we need i <= R+1, otherwise C(R+1, i) = 0.
    # R = N - K.
    # So for each i from 1 to K:
    #   ans[i] = C(N-K+1, i) * C(K-1, i-1) % MOD

    R = N - K
    results = []
    for i in range(1, K + 1):
        if i > R + 1:
            results.append(0)
        else:
            term1 = nCr(R + 1, i)
            term2 = nCr(K - 1, i - 1)
            ans = (term1 * term2) % MOD
            results.append(ans)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()