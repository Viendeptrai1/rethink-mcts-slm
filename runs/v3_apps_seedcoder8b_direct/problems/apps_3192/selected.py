def find_shortest_cycle():
    import sys
    from collections import defaultdict, deque

    input = sys.stdin.read
    data = input().splitlines()

    n = int(data[0])
    files = data[1].split()
    file_index = {file: i for i, file in enumerate(files)}

    adj_list = defaultdict(list)
    for i in range(n):
        file_name = data[2 + i * (n + 1)]
        k = int(data[3 + i * (n + 1)])
        for j in range(k):
            dependencies = data[4 + i * (n + 1) + j].split(', ')
            for dep in dependencies:
                adj_list[file_index[file_name]].append(file_index[dep])

    def bfs_cycle_detection(start):
        queue = deque([(start, [start])])
        visited = set()
        visited.add(start)

        while queue:
            current, path = queue.popleft()
            for neighbor in adj_list[current]:
                if neighbor in path:
                    cycle_start_index = path.index(neighbor)
                    return path[cycle_start_index:]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    shortest_cycle = None
    for i in range(n):
        cycle = bfs_cycle_detection(i)
        if cycle:
            if shortest_cycle is None or len(cycle) < len(shortest_cycle):
                shortest_cycle = cycle

    if shortest_cycle:
        print(' '.join(files[i] for i in shortest_cycle))
    else:
        print("SHIP IT")