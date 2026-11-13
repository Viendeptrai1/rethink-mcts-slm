import sys
from collections import defaultdict, deque

def max_importance(n, m, k, castles, portals):
    # Create a graph for portals
    portal_graph = defaultdict(list)
    for u, v in portals:
        portal_graph[u].append(v)
    
    # Sort portals by destination to ensure we can use them optimally
    for u in portal_graph:
        portal_graph[u].sort()

    # Dynamic programming table
    dp = [[-1] * (k + 1) for _ in range(n + 1)]
    dp[0][k] = 0  # Start with 0 castles captured and k warriors

    for i in range(1, n + 1):
        a_i, b_i, c_i = castles[i - 1]
        for w in range(k + 1):
            # Try to capture the i-th castle
            if w >= a_i and dp[i - 1][w - a_i] != -1:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - a_i] + c_i)
            
            # Try to use portals to capture the i-th castle
            if w >= a_i:
                for v in portal_graph[i]:
                    if dp[v][w - a_i] != -1:
                        dp[i][w] = max(dp[i][w], dp[v][w - a_i] + c_i)

            # Try to hire warriors in the i-th castle
            if w + b_i <= k and dp[i - 1][w] != -1:
                dp[i][w + b_i] = max(dp[i][w + b_i], dp[i - 1][w])

    # Find the maximum score possible
    max_score = -1
    for w in range(k + 1):
        max_score = max(max_score, dp[n][w])

    return max_score

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    castles = []
    index = 3
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        c_i = int(data[index + 2])
        castles.append((a_i, b_i, c_i))
        index += 3
    
    portals = []
    for _ in range(m):
        u_i = int(data[index])
        v_i = int(data[index + 1])
        portals.append((u_i, v_i))
        index += 2
    
    result = max_importance(n, m, k, castles, portals)
    print(result)

if __name__ == "__main__":
    main()