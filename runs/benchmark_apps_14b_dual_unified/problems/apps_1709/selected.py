def min_paint(n, m, k, colors, paint):
    def backtrack(index, current_color, groups, current_cost):
        nonlocal min_cost
        if index == n:
            if groups == k:
                min_cost = min(min_cost, current_cost)
            return
        
        if colors[index] != 0:
            backtrack(index + 1, colors[index], groups + (colors[index] != current_color), current_cost)
        else:
            for color in range(1, m + 1):
                backtrack(index + 1, color, groups + (color != current_color), current_cost + paint[index][color - 1])
    
    min_cost = float('inf')
    backtrack(0, 0, 0, 0)
    return min_cost if min_cost != float('inf') else -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

colors = list(map(int, data[3:3+n]))

paint = []
index = 3 + n
for _ in range(n):
    row = list(map(int, data[index:index+m]))
    paint.append(row)
    index += m

# Output the result
result = min_paint(n, m, k, colors, paint)
print(result)