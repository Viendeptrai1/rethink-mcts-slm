from collections import defaultdict, deque
import sys

def find_cycle():
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    files = data[1].split()
    
    dependencies = defaultdict(list)
    indegree = {file: 0 for file in files}
    
    index = 2
    for file in files:
        line = data[index].split()
        num_deps = int(line[1])
        index += 1
        for _ in range(num_deps):
            import_line = data[index].split(maxsplit=1)[1].strip()
            imports = import_line.split(', ')
            for dep in imports:
                dependencies[dep].append(file)
                indegree[file] += 1
            index += 1
    
    # Kahn's algorithm for topological sorting with cycle detection
    queue = deque([file for file in files if indegree[file] == 0])
    topo_sort = []
    
    while queue:
        current = queue.popleft()
        topo_sort.append(current)
        for neighbor in dependencies[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_sort) != n:
        # There is a cycle in the graph
        # Let's find the shortest cycle
        visited = {file: False for file in files}
        rec_stack = {file: False for file in files}
        
        def dfs(v, path):
            visited[v] = True
            rec_stack[v] = True
            path.append(v)
            
            for neighbor in dependencies[v]:
                if not visited[neighbor]:
                    cycle = dfs(neighbor, path)
                    if cycle:
                        return cycle
                elif rec_stack[neighbor]:
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:]
            
            rec_stack[v] = False
            path.pop()
            return None
        
        for file in files:
            if not visited[file]:
                cycle = dfs(file, [])
                if cycle:
                    return cycle
    
    return ["SHIP IT"]

if __name__ == "__main__":
    result = find_cycle()
    if result[0] == "SHIP IT":
        print(result[0])
    else:
        print(" -> ".join(result))