def min_replacements_to_lucky_ticket(ticket):
    dp = [[float('inf')] * 10 for _ in range(7)]
    dp[0][0] = 0
    
    for i in range(1, 7):
        d = int(ticket[i-1])
        for j in range(10):
            dp[i][(j + d) % 10] = min(dp[i][(j + d) % 10], dp[i-1][j])
            for k in range(10):
                dp[i][(j + d - k) % 10] = min(dp[i][(j + d - k) % 10], dp[i-1][k] + 1)
    
    return dp[6][0]

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    ticket = data[0]
    result = min_replacements_to_lucky_ticket(ticket)
    print(result)