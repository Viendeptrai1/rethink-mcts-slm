def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        
        # Check if it's possible to connect all districts
        from collections import defaultdict, deque
        
        gang_districts = defaultdict(list)
        for i in range(n):
            gang_districts[a[i]].append(i + 1)
        
        # If there's only one district in a gang, it's impossible
        for gang, districts in gang_districts.items():
            if len(districts) == 1:
                results.append("NO")
                break
        else:
            # We can connect districts of the same gang in a cycle
            # and connect different gangs by connecting their cycle representatives
            roads = []
            visited = [False] * (n + 1)
            cycle_representative = {}
            
            def bfs(start):
                queue = deque([start])
                visited[start] = True
                cycle = []
                while queue:
                    node = queue.popleft()
                    cycle.append(node)
                    for neighbor in gang_districts[a[node - 1]]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                return cycle
            
            for gang, districts in gang_districts.items():
                for district in districts:
                    if not visited[district]:
                        cycle = bfs(district)
                        if len(cycle) > 1:
                            cycle_representative[cycle[0]] = cycle[0]
                            for i in range(1, len(cycle)):
                                roads.append((cycle[i - 1], cycle[i]))
                                cycle_representative[cycle[i]] = cycle[0]
            
            # Connect different gangs
            representatives = list(cycle_representative.values())
            for i in range(1, len(representatives)):
                roads.append((representatives[i - 1], representatives[i]))
            
            results.append("YES")
            for road in roads:
                results.append(f"{road[0]} {road[1]}")
    
    sys.stdout.write("\n".join(results) + "\n")