from collections import defaultdict, deque

def find_shortest_cycle(n, files, imports):
    graph = defaultdict(list)
    indegree = [0] * n
    
    for i in range(n):
        file_name, k = files[i], imports[i]
        for j in range(k):
            dep_file = imports[i][j + 1]
            graph[file_name].append(dep_file)
            indegree[files.index(dep_file)] += 1
    
    queue = deque([file for file in files if indegree[files.index(file)] == 0])
    visited = set()
    
    while queue:
        node = queue.popleft()
        visited.add(node)
        
        for neighbor in graph[node]:
            indegree[files.index(neighbor)] -= 1
            if indegree[files.index(neighbor)] == 0:
                queue.append(neighbor)
    
    remaining_files = [file for file in files if file not in visited]
    
    if len(remaining_files) == 0:
        return "SHIP IT"
    
    def dfs(node, path):
        if node in path:
            return path[path.index(node):]
        for neighbor in graph[node]:
            result = dfs(neighbor, path + [node])
            if result:
                return result
        return None
    
    for file in remaining_files:
        cycle = dfs(file, [file])
        if cycle:
            return ' '.join(cycle)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    files = data[1:n+1]
    imports = []
    index = n + 1
    for _ in range(n):
        k = int(data[index])
        imports.append(data[index+1:index+k*2+1])
        index += k*2 + 1
    
    result = find_shortest_cycle(n, files, imports)
    print(result)