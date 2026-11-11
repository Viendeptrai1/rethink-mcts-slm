import sys
from collections import defaultdict, deque

def find_shortest_cycle(n, files, dependencies):
    # Create adjacency list for the graph
    graph = defaultdict(list)
    for i in range(n):
        file_name = files[i]
        k = dependencies[i][1]
        for j in range(k):
            imported_file = dependencies[i][2 + j].split()[1]
            graph[file_name].append(imported_file)
    
    # Function to perform BFS and detect cycles
    def bfs(start):
        queue = deque([(start, -1)])
        visited = {start: 0}
        parent = {start: None}
        
        while queue:
            node, distance = queue.popleft()
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited[neighbor] = distance + 1
                    parent[neighbor] = node
                    queue.append((neighbor, distance + 1))
                elif parent[node] != neighbor:
                    # Cycle detected
                    cycle = []
                    current = node
                    while current != neighbor:
                        cycle.append(current)
                        current = parent[current]
                    cycle.append(neighbor)
                    cycle.append(node)
                    return cycle[::-1]
        
        return None
    
    # Check for cycles starting from each file
    for file_name in files:
        cycle = bfs(file_name)
        if cycle:
            return cycle
    
    return ["SHIP IT"]

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    files = data[1].split()
    dependencies = [data[i].split(", ") for i in range(2, 2 + n)]
    
    result = find_shortest_cycle(n, files, dependencies)
    print(" ".join(result))

if __name__ == "__main__":
    main()