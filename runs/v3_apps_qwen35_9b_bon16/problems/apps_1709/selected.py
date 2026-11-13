import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
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
    except StopIteration:
        return

    # dp[i][j][last_color] = minimum cost to color first i trees such that:
    # we have exactly j contiguous groups, and the i-th tree has color 'last_color'
    # last_color ranges from 1 to m. We'll use 1-based indexing for colors.
    # If a state is unreachable, we store infinity.

    INF = float('inf')

    # Initialize DP table
    # Dimensions: (n+1) x (k+1) x (m+1)
    # We'll use 1-based indexing for trees (1 to n) and colors (1 to m)
    dp = [[[INF] * (m + 1) for _ in range(k + 1)] for _ in range(n + 1)]

    # Base case: First tree (index 0 in c, but index 1 in dp)
    first_tree = 0  # index in c
    first_tree_cost = 0

    for color in range(1, m + 1):
        if c[first_tree] != 0 and c[first_tree] != color:
            continue  # Already colored with different color, skip
        cost = 0
        if c[first_tree] == 0:
            cost = p[first_tree][color - 1]
        dp[1][1][color] = cost

    # Fill DP table
    for i in range(1, n):  # current tree index (0-based in c), corresponding to dp[i+1]
        for j in range(1, k + 1):  # number of groups
            for last_color in range(1, m + 1):
                if dp[i+1][j][last_color] == INF:
                    continue
                
                current_tree_idx = i + 1  # 1-based index for current tree
                prev_tree_idx = i         # 0-based index for previous tree (which is current-1)
                
                # Try all possible colors for the next tree (tree at index i in 0-based, i.e., current_tree_idx in 1-based)
                # Actually, we are moving from tree i (0-based) to tree i+1 (0-based)
                # So in loop: we are at tree `i` (0-based), and we look at `next_tree = i+1` (0-based)
                # But my dp state is defined as: dp[i][j][color] = min cost for first i trees (1 to i)
                # So when we are at loop i (representing we just finished tree i-1 0-based), we want to compute for tree i 0-based.
                
                # Let's re-align:
                # Outer loop: current tree index `curr` from 0 to n-2 (0-based)
                # We are transitioning from state `dp[curr+1][...][...]` to `dp[curr+2][...][...]`
                pass

    # Let's restart the loop logic clearly
    # dp[i][j][color] -> min cost for prefix of length i (trees 0 to i-1), with j groups, ending with color `color`
    
    # Re-initialize
    dp = [[[INF] * (m + 1) for _ in range(k + 1)] for _ in range(n + 1)]
    
    # Base case: Tree 0
    for color in range(1, m + 1):
        if c[0] != 0 and c[0] != color:
            continue
        cost = 0
        if c[0] == 0:
            cost = p[0][color - 1]
        dp[1][1][color] = cost

    # Iterate for each subsequent tree
    for i in range(1, n):  # i is the 0-based index of the tree we are processing now
        for j in range(1, k + 1):  # number of groups so far
            for prev_color in range(1, m + 1):  # color of tree i-1
                if dp[i][j][prev_color] == INF:
                    continue
                
                # Try all colors for tree i
                for curr_color in range(1, m + 1):
                    # Check if valid color choice
                    if c[i] != 0 and c[i] != curr_color:
                        continue
                    
                    cost_add = 0
                    if c[i] == 0:
                        cost_add = p[i][curr_color - 1]
                    
                    # Determine new number of groups
                    if curr_color == prev_color:
                        new_groups = j
                    else:
                        new_groups = j + 1
                    
                    if new_groups > k:
                        continue
                    
                    new_cost = dp[i][j][prev_color] + cost_add
                    if new_cost < dp[i+1][new_groups][curr_color]:
                        dp[i+1][new_groups][curr_color] = new_cost

    # Find the answer
    ans = INF
    for color in range(1, m + 1):
        if dp[n][k][color] < ans:
            ans = dp[n][k][color]

    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == '__main__':
    solve()