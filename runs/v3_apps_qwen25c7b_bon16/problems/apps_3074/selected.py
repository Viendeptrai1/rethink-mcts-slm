def count_valid_subsets(N, S):
    mod = 10**9 + 7
    dp = [0] * 3
    dp[0] = 1
    total = 0
    
    for char in S:
        next_dp = [0] * 3
        for i in range(3):
            next_dp[(int(char) + i) % 3] += dp[i]
        total += sum(next_dp)
        total %= mod
        dp = next_dp[:]
    
    return total

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    S = data[1]
    result = count_valid_subsets(N, S)
    print(result)