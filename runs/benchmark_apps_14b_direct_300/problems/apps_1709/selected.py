import sys
from collections import deque

def min_paint_to_color_trees(n, m, k, colors, paint_costs):
    def bfs():
        queue = deque([(tuple(colors), 0)])
        visited = set()
        visited.add(tuple(colors))
        
        while queue:
            current_colors, current_cost = queue.popleft()
            
            # Count the number of contiguous groups of the same color
            groups = 1
            for i in range(1, n):
                if current_colors[i] != current_colors[i - 1]:
                    groups += 1
            
            if groups == k:
                return current_cost
            
            for i in range(n):
                if current_colors[i] == 0:
                    for j in range(1, m + 1):
                        new_colors = list(current_colors)
                        new_colors[i] = j
                        new_state = tuple(new_colors)
                        
                        if new_state not in visited:
                            visited.add(new_state)
                            new_cost = current_cost + paint_costs[i][j - 1]
                            queue.append((new_state, new_cost))
        
        return -1
    
    return bfs()

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

colors = list(map(int, data[3:3 + n]))

paint_costs = []
index = 3 + n
for _ in range(n):
    row = list(map(int, data[index:index + m]))
    paint_costs.append(row)
    index += m

# Output the result
print(min_paint_to_color_trees(n, m, k, colors, paint_costs))