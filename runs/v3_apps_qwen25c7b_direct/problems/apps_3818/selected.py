import sys
from collections import defaultdict, deque

MOD = 10**9 + 7

def dfs(node, parent):
    max_dist_white = [0] * 2
    max_dist_black = [0] * 2
    for neighbor in adj[node]:
        if neighbor != parent:
            dists_w, dists_b = dfs(neighbor, node)
            max_dist_white[0] = max(max_dist_white[0], max(dists_w))
            max_dist_black[0] = max(max_dist_black[0], max(dists_b))
            max_dist_white[1] += max(dists_w) + 1
            max_dist_black[1] += max(dists_b) + 1
    return max_dist_white, max_dist_black

def solve():
    n = int(input())
    adj = defaultdict(list)
    for _ in range(n-1):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)
    
    total_niceness = 0
    
    def add_niceness(color_count):
        nonlocal total_niceness
        white_count, black_count = color_count
        total_niceness = (total_niceness + max(white_count, black_count)) % MOD
    
    def count_colors(node, parent, color):
        color_count = [0, 0]
        color_count[color] += 1
        for neighbor in adj[node]:
            if neighbor != parent:
                sub_color_count = count_colors(neighbor, node, 1-color)
                color_count[0] += sub_color_count[0]
                color_count[1] += sub_color_count[1]
        add_niceness(color_count)
        return color_count
    
    count_colors(1, -1, 0)
    
    print(total_niceness)

if __name__ == "__main__":
    solve()