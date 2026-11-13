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

    # Calculate total capacity of all bins
    total_capacity = k * x

    # We need to select a subset of groups such that:
    # 1. The sum of selected groups (S) is a multiple of x (to avoid waste)
    # 2. a <= S <= b
    # 3. S <= total_capacity (cannot take more lunches than available)
    # We want to maximize S.

    # Since n is up to 1000 and group sizes are up to 100, the maximum possible sum is 100,000.
    # We can use dynamic programming (knapsack-like) to find all reachable sums.
    
    max_sum = sum(groups)
    # dp[s] will be True if sum 's' is achievable
    dp = [False] * (max_sum + 1)
    dp[0] = True

    for size in groups:
        # Iterate backwards to avoid using the same item multiple times for the same sum in one iteration
        for s in range(max_sum, size - 1, -1):
            if dp[s - size]:
                dp[s] = True

    # Find the maximum valid sum
    ans = -1
    # We check from the largest possible value down to 'a'
    # The upper bound for our search is min(b, total_capacity, max_sum)
    search_limit = min(b, total_capacity, max_sum)
    
    for s in range(search_limit, a - 1, -1):
        if s % x == 0 and dp[s]:
            ans = s
            break

    if ans != -1:
        print(ans)
    else:
        print("impossible")

if __name__ == "__main__":
    solve()