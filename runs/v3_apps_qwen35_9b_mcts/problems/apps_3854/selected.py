import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    c = []
    for _ in range(n):
        c.append(int(next(iterator)))

    # dp[j] will be a set of all possible sub-subset sums x achievable 
    # using a subset of coins that sums exactly to j.
    # Initialize: with 0 coins, sum is 0, and sub-subset sum is 0.
    dp = [set() for _ in range(k + 1)]
    dp[0].add(0)

    for coin in c:
        # Iterate backwards to avoid using the same coin multiple times for the same sum j
        for j in range(k, coin - 1, -1):
            prev_j = j - coin
            if not dp[prev_j]:
                continue
            
            # For every sub-subset sum x achievable with sum prev_j:
            # 1. We can keep the sub-subset as is (sum x) for the new sum j.
            # 2. We can add the current coin to the sub-subset (sum x + coin) for the new sum j.
            
            current_sums = dp[prev_j]
            for x in current_sums:
                dp[j].add(x)
                if x + coin <= k:
                    dp[j].add(x + coin)

    # Collect all x such that dp[k] contains x
    result = sorted(list(dp[k]))
    
    print(len(result))
    print(*(result))

if __name__ == "__main__":
    solve()