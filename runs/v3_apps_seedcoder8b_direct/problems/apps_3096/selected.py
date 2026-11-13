import sys
from collections import defaultdict, deque

def count_valid_joke_sets(N, V, subordinates):
    # Build the tree structure
    tree = defaultdict(list)
    for a, b in subordinates:
        tree[b].append(a)
    
    # Dynamic programming table
    dp = [[0] * (N + 1) for _ in range(N + 1)]
    
    # DFS to calculate dp values
    def dfs(node):
        dp[node][V[node - 1]] = 1
        for child in tree[node]:
            dfs(child)
            new_dp = [0] * (N + 1)
            for i in range(1, N + 1):
                if dp[node][i] > 0:
                    for j in range(1, N + 1):
                        if dp[child][j] > 0 and abs(i - j) > 1:
                            new_dp[j] = (new_dp[j] + dp[node][i] * dp[child][j]) % (10**9 + 7)
            for i in range(1, N + 1):
                dp[node][i] = (dp[node][i] + new_dp[i]) % (10**9 + 7)
    
    # Start DFS from the CEO (node 1)
    dfs(1)
    
    # Sum up all valid sets
    return sum(dp[1]) % (10**9 + 7)

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    V = [0] + list(map(int, data[1:N+1]))
    subordinates = [(int(data[i]), int(data[i+1])) for i in range(N, len(data), 2)]
    
    result = count_valid_joke_sets(N, V, subordinates)
    print(result)

if __name__ == "__main__":
    main()