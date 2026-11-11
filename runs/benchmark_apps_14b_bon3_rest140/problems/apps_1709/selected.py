import sys
from collections import deque

def min_paint(n, m, k, colors, paint):
    def bfs():
        queue = deque([(tuple(colors), 0)])
        visited = set()
        visited.add(tuple(colors))
        
        while queue:
            current_colors, current_cost = queue.popleft()
            
            if current_colors.count(0) == 0:
                if count_groups(current_colors) == k:
                    return current_cost
                continue
            
            for i in range(n):
                if current_colors[i] != 0:
                    continue
                
                for j in range(1, m + 1):
                    new_colors = list(current_colors)
                    new_colors[i] = j
                    new_cost = current_cost + paint[i][j - 1]
                    
                    if tuple(new_colors) not in visited:
                        visited.add(tuple(new_colors))
                        queue.append((tuple(new_colors), new_cost))
        
        return -1
    
    def count_groups(colors):
        groups = 0
        current_color = None
        
        for color in colors:
            if color != current_color:
                groups += 1
                current_color = color
        
        return groups
    
    return bfs()

# Reading input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])

colors = list(map(int, data[3:3 + n]))

paint = []
index = 3 + n
for _ in range(n):
    row = list(map(int, data[index:index + m]))
    paint.append(row)
    index += m

# Output the result
print(min_paint(n, m, k, colors, paint))