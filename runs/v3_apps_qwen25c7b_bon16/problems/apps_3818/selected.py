MOD = 10**9 + 7

def dfs(graph, node, parent):
    dp_white = [0] * 3
    dp_black = [0] * 3
    
    for neighbor in graph[node]:
        if neighbor == parent:
            continue
        dp_white[1], dp_white[2] = max(dp_white[1], dp_white[2]), max(dp_white[1], dp_white[2]) + 1
        dp_black[1], dp_black[2] = max(dp_black[1], dp_black[2]), max(dp_black[1], dp_black[2]) + 1
        
        white_child_max, black_child_max = dfs(graph, neighbor, node)
        
        dp_white[0] += white_child_max
        dp_black[0] += black_child_max
        
        dp_white[1] = max(dp_white[1], dp_white[0] + 1)
        dp_black[1] = max(dp_black[1], dp_black[0] + 1)
    
    return max(dp_white), max(dp_black)

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    edges = [(int(data[i*2+1])-1, int(data[i*2+2])-1) for i in range(n-1)]
    
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    total_niceness = 0
    
    for start in range(n):
        white_niceness, black_niceness = dfs(graph, start, -1)
        total_niceness = (total_niceness + max(white_niceness, black_niceness)) % MOD
    
    print(total_niceness)

if __name__ == "__main__":
    solve()