import sys
input = sys.stdin.read
data = input().split()

def min_paint_needed(n, m, k, c, p):
    def is_valid_coloring(coloring, k):
        groups = 0
        current_group_size = 0
        previous_color = None
        for color in coloring:
            if color != previous_color:
                if previous_color is not None:
                    groups += 1
                previous_color = color
                current_group_size = 1
            else:
                current_group_size += 1
        groups += 1
        return groups == k

    def dfs(index, current_coloring, cost):
        if index == n:
            if is_valid_coloring(current_coloring, k):
                return cost
            return float('inf')
        
        if c[index] > 0:
            return dfs(index + 1, current_coloring[:], cost)
        
        min_cost = float('inf')
        for new_color in range(1, m + 1):
            min_cost = min(min_cost, dfs(index + 1, current_coloring[:index] + [new_color] + current_coloring[index + 1:], cost + p[index][new_color - 1]))
        return min_cost

    min_cost = dfs(0, [0] * n, 0)
    if min_cost == float('inf'):
        return -1
    return min_cost

# Parsing input
n = int(data[0])
m = int(data[1])
k = int(data[2])
c = list(map(int, data[3:(3 + n)]))
p = []
for i in range(n):
    row = list(map(int, data[(3 + n) + (i * m):(3 + n) + ((i + 1) * m)]))
    p.append(row)

print(min_paint_needed(n, m, k, c, p))