import sys

def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    blocked_set = set(blocked_positions)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(n + 1):
        if i in blocked_set:
            continue
        
        for j in range(1, k + 1):
            if i + j <= n:
                dp[i + j] = min(dp[i + j], dp[i] + lamp_costs[j - 1])
    
    return dp[n] if dp[n] != float('inf') else -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    blocked_positions = list(map(int, data[3:m+3]))
    lamp_costs = list(map(int, data[m+3:m+k+3]))
    
    result = min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)
    print(result)