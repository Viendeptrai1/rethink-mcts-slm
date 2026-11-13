def solve_partition_weight_sum(n, k, weights):
    MOD = 10**9 + 7

    # Calculate the total sum of all weights
    total_weight = sum(weights)

    # We will use dynamic programming to solve this problem
    # dp[i][j] will store the number of ways to partition the first i elements into j subsets
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1  # Base case: one way to partition zero elements into zero subsets

    # Iterate over each element
    for i in range(1, n + 1):
        # Iterate over each number of subsets
        for j in range(1, k + 1):
            # Transition: We can either include the current element in one of the existing subsets
            # or start a new subset with the current element.
            dp[i][j] = (dp[i - 1][j] * j + dp[i - 1][j - 1]) % MOD

    # The final answer is the sum of weights of all partitions multiplied by the number of ways
    result = 0
    for i in range(1, n + 1):
        result = (result + dp[i][k] * total_weight) % MOD

    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    weights = list(map(int, data[2:2 + n]))

    result = solve_partition_weight_sum(n, k, weights)
    print(result)

if __name__ == "__main__":
    main()