import sys
from functools import lru_cache

def min_paint(n, m, k, colors, paint):
    @lru_cache(None)
    def dp(i, prev_color, groups):
        if i == n:
            return 0 if groups == k else float('inf')
        
        if colors[i] != 0:
            return dp(i + 1, colors[i], groups + (colors[i] != prev_color))
        
        min_paint_used = float('inf')
        for color in range(1, m + 1):
            paint_used = paint[i][color - 1]
            new_groups = groups + (color != prev_color)
            min_paint_used = min(min_paint_used, paint_used + dp(i + 1, color, new_groups))
        
        return min_paint_used
    
    result = dp(0, 0, 0)
    return result if result != float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    k = int(data[index + 2])
    index += 3
    
    colors = list(map(int, data[index:index + n]))
    index += n
    
    paint = []
    for _ in range(n):
        row = list(map(int, data[index:index + m]))
        paint.append(row)
        index += m
    
    result = min_paint(n, m, k, tuple(colors), tuple(map(tuple, paint)))
    print(result)

if __name__ == "__main__":
    main()