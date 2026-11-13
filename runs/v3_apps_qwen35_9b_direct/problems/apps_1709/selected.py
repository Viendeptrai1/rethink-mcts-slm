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
    
    # dp[i][j][beauty] = minimum cost to color first i trees such that the i-th tree has color j+1 and there are 'beauty' groups
    # Colors are 1-indexed in problem, 0-indexed in our logic (0 to m-1)
    # Initialize with infinity
    INF = float('inf')
    
    # dp[j][b] will store the min cost for current tree i having color j with b groups
    # We use two rows to save space: prev and curr
    prev = [[INF] * (k + 1) for _ in range(m)]
    
    # Base case: first tree (index 0)
    color_val = c[0]
    cost_val = p[0][color_val] if color_val != 0 else 0
    
    for j in range(m):
        if j == color_val:
            # If the tree is already colored with this color, cost is 0
            # But wait, if it's already colored, we cannot change it.
            # So if c[0] != 0, then only j == c[0] is valid with cost 0.
            # If c[0] == 0, then any j is valid with cost p[0][j].
            if color_val != 0:
                if j == color_val:
                    prev[j][1] = 0
            else:
                prev[j][1] = cost_val
        else:
            if color_val == 0:
                prev[j][1] = cost_val
    
    # Process remaining trees
    for i in range(1, n):
        curr = [[INF] * (k + 1) for _ in range(m)]
        color_val = c[i]
        
        for j in range(m):
            # Cost to color tree i with color j
            if color_val != 0 and j != color_val:
                continue # Cannot change pre-colored tree
            
            current_paint_cost = 0
            if color_val == 0:
                current_paint_cost = p[i][j]
            
            # Try all previous colors 'last_j' and previous beauty counts 'b'
            for last_j in range(m):
                for b in range(1, k + 1):
                    if prev[last_j][b] == INF:
                        continue
                    
                    new_b = b
                    if last_j != j:
                        new_b += 1
                    
                    if new_b > k:
                        continue
                    
                    new_cost = prev[last_j][b] + current_paint_cost
                    if new_cost < curr[j][new_b]:
                        curr[j][new_b] = new_cost
        
        prev = curr
    
    # Find the minimum cost among all colors for the last tree with exactly k groups
    ans = INF
    for j in range(m):
        if prev[j][k] < ans:
            ans = prev[j][k]
    
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()