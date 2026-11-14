import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    n = int(next(iterator))
    m = int(next(iterator))
    k = int(next(iterator))
    
    c = []
    for _ in range(n):
        c.append(int(next(iterator)))
    
    p = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(int(next(iterator)))
        p.append(row)
    
    INF = float('inf')
    
    # dp[i][j][g] = minimum cost to color first i trees (0 to i-1)
    # such that the i-th tree (index i-1) has color j (1-based) and there are exactly g groups.
    # Dimensions: (n+1) x (m+1) x (k+1)
    # We use 1-based indexing for colors in DP for convenience (1 to m).
    
    dp = [[[INF] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    
    # Base case: first tree (index 0)
    first_tree_color = c[0]
    first_tree_cost_row = p[0]
    
    for color in range(1, m + 1):
        if first_tree_color != 0 and first_tree_color != color:
            continue
        cost = 0
        if first_tree_color == 0:
            cost = first_tree_cost_row[color - 1]
        dp[1][color][1] = cost
    
    # Iterate through trees from 2 to n
    for i in range(2, n + 1):
        current_tree_color = c[i-1]
        current_tree_cost_row = p[i-1]
        
        for g in range(1, k + 1):
            for new_color in range(1, m + 1):
                # If current tree is pre-colored and doesn't match new_color, skip
                if current_tree_color != 0 and current_tree_color != new_color:
                    continue
                
                cost_add = 0
                if current_tree_color == 0:
                    cost_add = current_tree_cost_row[new_color - 1]
                
                # Try transitioning from previous tree (i-1)
                # Option 1: Same color as previous tree (extends the group)
                # Previous tree must have been colored with new_color
                prev_same = dp[i-1][new_color][g]
                if prev_same != INF:
                    dp[i][new_color][g] = min(dp[i][new_color][g], prev_same + cost_add)
                
                # Option 2: Different color from previous tree (starts a new group)
                # Previous tree must have been colored with some color != new_color
                # and we must have had g-1 groups before.
                if g > 1:
                    for prev_color in range(1, m + 1):
                        if prev_color == new_color:
                            continue
                        prev_diff = dp[i-1][prev_color][g-1]
                        if prev_diff != INF:
                            dp[i][new_color][g] = min(dp[i][new_color][g], prev_diff + cost_add)
    
    # Find the minimum cost for exactly k groups at the last tree (index n)
    ans = INF
    for color in range(1, m + 1):
        ans = min(ans, dp[n][color][k])
    
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == '__main__':
    solve()