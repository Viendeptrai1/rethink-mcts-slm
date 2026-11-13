def solve_birthday_party():
    import sys
    from collections import defaultdict

    sys.setrecursionlimit(15000)
    
    def dfs(node, parent, visited, dp, graph, jokes):
        visited[node] = True
        dp[node][0] = 1  # Not including this person
        dp[node][1] = 1  # Including this person
        
        for child in graph[node]:
            if not visited[child]:
                dfs(child, node, visited, dp, graph, jokes)
        
        # Calculate dp values
        for child in graph[node]:
            if child != parent:
                # Not taking this node
                dp[node][0] *= sum(dp[child])
                
                # Taking this node
                if jokes[child] != jokes[node] - 1 and jokes[child] != jokes[node] + 1:
                    dp[node][1] *= dp[child][0]
        
        # Check for the consecutive rule
        if parent != -1 and jokes[node] != jokes[parent] - 1 and jokes[node] != jokes[parent] + 1:
            dp[node][1] = 0

    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    jokes = [0] * (N + 1)
    for i in range(1, N + 1):
        jokes[i] = int(data[i])
    
    graph = defaultdict(list)
    for i in range(N - 1):
        A = int(data[N + i * 2 + 1])
        B = int(data[N + i * 2 + 2])
        graph[A].append(B)
        graph[B].append(A)
    
    visited = [False] * (N + 1)
    dp = [[0, 0] for _ in range(N + 1)]
    
    dfs(1, -1, visited, dp, graph, jokes)
    
    print(dp[1][0] + dp[1][1])