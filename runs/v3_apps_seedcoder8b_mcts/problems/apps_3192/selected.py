from collections import defaultdict, deque
import sys

def find_shortest_cycle(n, files, dependencies):
    graph = defaultdict(list)
    indegree = {file: 0 for file in files}

    for file, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(file)
            indegree[file] += 1

    queue = deque([file for file in files if indegree[file] == 0])
    visited = set(queue)

    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                visited.add(neighbor)

    unvisited = set(files) - visited
    if not unvisited:
        return "SHIP IT"

    def bfs_cycle(start):
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor in path:
                    return path[path.index(neighbor):]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    shortest_cycle = None
    for file in unvisited:
        cycle = bfs_cycle(file)
        if cycle and (not shortest_cycle or len(cycle) < len(shortest_cycle)):
            shortest_cycle = cycle

    return ' '.join(shortest_cycle) if shortest_cycle else "SHIP IT"

def main():
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    files = data[1].split()
    dependencies = {}

    index = 2
    for _ in range(n):
        line = data[index].split()
        file = line[0]
        k = int(line[1])
        index += 1
        deps = []
        for _ in range(k):
            deps_line = data[index].strip().split('import ')[1].split(', ')
            deps.extend(deps_line)
            index += 1
        dependencies[file] = deps

    result = find_shortest_cycle(n, files, dependencies)
    print(result)

if __name__ == "__main__":
    main()