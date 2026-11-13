import sys
from functools import lru_cache

def solve():
    n, m, k = map(int, input().split())
    colors = list(map(int, input().split()))
    paint_costs = [list(map(int, input().split())) for _ in range(n)]

    @lru_cache(maxsize=None)
    def dp(i, prev_color, groups):
        if i == n:
            return 0 if groups == k else float('inf')
        
        if colors[i] != 0:
            return dp(i + 1, colors[i], groups + (1 if colors[i] != prev_color else 0))
        
        min_cost = float('inf')
        for color in range(1, m + 1):
            cost = paint_costs[i][color - 1] + dp(i + 1, color, groups + (1 if color != prev_color else 0))
            min_cost = min(min_cost, cost)
        
        return min_cost

    result = dp(0, 0, 0)
    print(-1 if result == float('inf') else result)

solve()