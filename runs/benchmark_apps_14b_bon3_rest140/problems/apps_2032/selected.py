import sys
from typing import List, Tuple

def max_defended_castles_score(n: int, m: int, k: int, castles: List[Tuple[int, int, int]], portals: List[Tuple[int, int]]) -> int:
    # Initialize the DP table
    dp = [[-float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][k] = 0

    # Process each castle in order
    for i in range(1, n + 1):
        a, b, c = castles[i - 1]
        for j in range(k + 1):
            if dp[i - 1][j] == -float('inf'):
                continue
            # Option 1: Do not capture the i-th castle
            dp[i][j] = max(dp[i][j], dp[i - 1][j])
            # Option 2: Capture the i-th castle if possible
            if j >= a:
                new_army = j - a + b
                dp[i][new_army] = max(dp[i][new_army], dp[i - 1][j] + c)
                # Defend the i-th castle
                dp[i][new_army - 1] = max(dp[i][new_army - 1], dp[i - 1][j] + c)
                # Use portals to defend other castles
                for u, v in portals:
                    if u == i:
                        dp[v][new_army - 1] = max(dp[v][new_army - 1], dp[i - 1][j] + c)

    # Find the maximum score
    max_score = max(dp[n])
    return max_score if max_score != -float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    
    castles = []
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        castles.append((a, b, c))
        index += 3
    
    portals = []
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        portals.append((u, v))
        index += 2
    
    result = max_defended_castles_score(n, m, k, castles, portals)
    print(result)

if __name__ == "__main__":
    main()