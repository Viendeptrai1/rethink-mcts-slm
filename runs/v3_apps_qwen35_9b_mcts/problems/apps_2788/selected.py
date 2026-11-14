import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        groups = []
        for _ in range(n):
            groups.append(int(next(iterator)))
        
        k = int(next(iterator))
        x = int(next(iterator))
        a = int(next(iterator))
        b = int(next(iterator))
    except StopIteration:
        return

    max_lunches = k * x
    
    # We need to find a subset sum S such that:
    # 1. S is a multiple of x (so S = m * x)
    # 2. m <= k (which is covered by S <= max_lunches)
    # 3. a <= S <= b
    # 4. S is achievable by summing some subset of groups
    
    # Use a boolean array for DP to track reachable sums
    # Since max_lunches can be up to 100 * 100000 = 10,000,000, a boolean array is feasible in Python
    # However, we only care about sums that are multiples of x.
    # To optimize space and time, we can track reachable indices where index = sum // x.
    # Max index = k (up to 100). This is extremely small!
    
    # Let's re-evaluate:
    # We need sum(S) = m * x, where 1 <= m <= k.
    # So we only care if a subset sum equals m*x for some m in [1, k].
    # The maximum possible sum we care about is k*x.
    # But the groups can sum up to much larger than k*x. We should cap our DP at k*x.
    # If a group size is larger than k*x, we can ignore it because including it would exceed the max allowed lunches.
    
    limit = k * x
    
    # dp[i] will be True if sum 'i' is achievable
    # We only need to go up to 'limit'
    dp = [False] * (limit + 1)
    dp[0] = True
    
    for g in groups:
        if g > limit:
            continue
        # Iterate backwards to avoid using the same group multiple times for the same sum
        for s in range(limit, g - 1, -1):
            if dp[s - g]:
                dp[s] = True
    
    # Now find the maximum S such that:
    # a <= S <= b
    # S is a multiple of x
    # dp[S] is True
    
    ans = -1
    # Check from b down to a
    for s in range(b, a - 1, -1):
        if s % x == 0 and dp[s]:
            ans = s
            break
    
    if ans == -1:
        print("impossible")
    else:
        print(ans)

if __name__ == "__main__":
    solve()