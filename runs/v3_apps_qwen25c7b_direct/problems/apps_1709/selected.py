import sys
from typing import List

def min_paint_to_color_trees(n: int, m: int, k: int, colors: List[int], paints: List[List[int]]) -> int:
    def dfs(index: int, current_color: int, current_beauty: int, total_paint: int) -> int:
        if index == n:
            return total_paint if current_beauty == k else float('inf')
        
        if colors[index] != 0:
            return dfs(index + 1, current_color, current_beauty, total_paint)
        
        min_paint = float('inf')
        for color in range(1, m + 1):
            new_beauty = current_beauty + 1 if color != current_color else current_beauty
            min_paint = min(min_paint, dfs(index + 1, color, new_beauty, total_paint + paints[index][color - 1]))
        
        return min_paint
    
    result = dfs(0, 0, 0, 0)
    return result if result != float('inf') else -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    colors = [int(data[i]) for i in range(3, 3 + n)]
    
    paints = []
    for i in range(3 + n, len(data)):
        paints.append([int(data[i + j * m]) for j in range(m)])
    
    result = min_paint_to_color_trees(n, m, k, colors, paints)
    print(result)