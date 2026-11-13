import sys
from typing import List

def min_paint_to_color(n: int, m: int, k: int, colors: List[int], paints: List[List[int]]) -> int:
    def get_beauty(coloring):
        beauty = 0
        current_color = None
        for color in coloring:
            if color != current_color:
                beauty += 1
                current_color = color
        return beauty

    def dfs(index, current_coloring, current_cost):
        nonlocal best_cost
        if index == n:
            if get_beauty(current_coloring) == k:
                best_cost = min(best_cost, current_cost)
            return
        
        if colors[index] != 0:
            dfs(index + 1, current_coloring[:index] + [colors[index]] + current_coloring[index+1:], current_cost)
        else:
            for color in range(1, m + 1):
                dfs(index + 1, current_coloring[:index] + [color] + current_coloring[index+1:], current_cost + paints[index][color-1])

    best_cost = float('inf')
    dfs(0, [0] * n, 0)
    
    return best_cost if best_cost != float('inf') else -1

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    colors = list(map(int, data[3:3+n]))
    
    paints = []
    for i in range(n):
        paints.append(list(map(int, data[3+n+i*m:3+n+(i+1)*m])))
    
    result = min_paint_to_color(n, m, k, colors, paints)
    print(result)