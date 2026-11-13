from collections import defaultdict, deque

def find_shortest_cycle(file_names, dependencies):
    graph = defaultdict(list)
    in_degree = {file_name: 0 for file_name in file_names}
    
    for file_name, k, *imports in dependencies:
        for imp in imports:
            graph[file_name].append(imp)
            in_degree[imp] += 1
    
    queue = deque([file_name for file_name in file_names if in_degree[file_name] == 0])
    visited = set()
    parent = {file_name: None for file_name in file_names}
    path = []
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            path.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    parent[neighbor] = node
                    queue.append(neighbor)
    
    for file_name in file_names:
        if file_name not in visited:
            cycle = [file_name]
            current = parent[cycle[-1]]
            while current != file_name:
                cycle.append(current)
                current = parent[current]
            cycle.reverse()
            return ' '.join(cycle)
    
    return "SHIP IT"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    file_names = data[1].split()
    dependencies = []
    
    index = 2
    for _ in range(n):
        file_name = data[index]
        k = int(data[index + 1])
        imports = data[index + 2:index + 2 + k]
        dependencies.append((file_name, k) + tuple(imports))
        index += 2 + k
    
    result = find_shortest_cycle(file_names, dependencies)
    print(result)