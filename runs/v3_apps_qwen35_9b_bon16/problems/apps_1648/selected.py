import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    K = int(data[1])
    MOD = 10**9 + 7

    # Precompute factorials and inverse factorials for combinations
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i - 1] * i) % MOD
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i + 1] * (i + 1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n - r]) % MOD
        return (num * den) % MOD

    # dp[i] will store the number of ways to arrange balls such that Takahashi needs exactly i moves
    # We build this by considering the positions of the K blue balls among the N positions.
    # The key insight is:
    # - The K blue balls form some number of contiguous segments.
    # - Each contiguous segment of blue balls corresponds to one move.
    # - So we need exactly i contiguous segments of blue balls.
    #
    # To form exactly i segments of blue balls using K balls:
    # We must split the K blue balls into i non-empty groups. The number of ways to do this is C(K-1, i-1).
    # Then, we have (K - i) "gaps" between these groups (since each group is a block, and there are i blocks).
    # Actually, a better way to think:
    # We have i segments of blue balls. Let the lengths of these segments be x1, x2, ..., xi where each xj >= 1 and sum(xj) = K.
    # The number of such compositions is C(K-1, i-1).
    # Now, we need to place these i segments into the row of N balls along with (N-K) red balls.
    # Think of the arrangement as: we have i blocks of blue balls and (N-K) red balls.
    # But the red balls can be anywhere, and they break the blue segments.
    #
    # Alternative approach (standard combinatorial solution for this problem):
    # To have exactly i segments of blue balls:
    # 1. We need to choose i segments of blue balls. This is equivalent to choosing i groups from K balls: C(K-1, i-1).
    # 2. Now we have i blocks of blue balls and (N-K) red balls. Total items to arrange: i + (N-K).
    #    However, the blocks of blue balls are distinct in position but identical in content? No, the problem says balls of same color are indistinguishable, but the arrangement is a sequence.
    #    Actually, once we decide the lengths of the blue segments and their positions relative to red balls, the arrangement is fixed.
    #
    # Correct model:
    # We are arranging K blue balls and N-K red balls.
    # We want exactly i contiguous segments of blue balls.
    # This is equivalent to:
    # - Distribute the K blue balls into i non-empty contiguous segments. (Number of ways: C(K-1, i-1))
    # - Place these i segments and the (N-K) red balls in a row such that no two blue segments are adjacent (otherwise they would merge into one).
    #   Actually, if we treat each blue segment as a single "super-ball", then we have i super-blue balls and (N-K) red balls.
    #   We need to arrange these (i + N - K) items such that no two super-blue balls are adjacent? 
    #   Wait, if we have i super-blue balls and we place them among red balls, we just need to ensure that between any two super-blue balls there is at least one red ball.
    #   But that's automatically satisfied if we consider the "gaps" method properly.
    #
    # Standard stars and bars with separation:
    # We have (N-K) red balls. These create (N-K + 1) possible slots (including ends) where we can place blue segments.
    # We need to place i blue segments into these slots, with at most one segment per slot (to keep them separate).
    # Number of ways to choose which slots get a segment: C(N-K+1, i).
    # Then, for each chosen slot, we must place a non-empty sequence of blue balls.
    # We have K blue balls to distribute into these i segments, each segment having at least 1 ball.
    # Number of ways to distribute K balls into i non-empty ordered segments: C(K-1, i-1).
    #
    # Therefore, total ways for a fixed i is: C(N-K+1, i) * C(K-1, i-1).
    #
    # Constraints: 1 <= i <= K.
    # Also, we must have i <= N-K+1, otherwise C(N-K+1, i) is 0.
    
    ans = []
    for i in range(1, K + 1):
        ways = (nCr(N - K + 1, i) * nCr(K - 1, i - 1)) % MOD
        ans.append(ways)
    
    for x in ans:
        print(x)

if __name__ == '__main__':
    solve()