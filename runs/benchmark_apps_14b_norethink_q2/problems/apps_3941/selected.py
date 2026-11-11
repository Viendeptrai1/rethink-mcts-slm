import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    room_status = list(map(int, data[index:index + n]))
    index += n
    
    switches = defaultdict(list)
    for _ in range(m):
        x = int(data[index])
        index += 1
        for _ in range(x):
            room = int(data[index]) - 1
            switches[room].append(_)
            index += 1
    
    # Create a graph where each node is a switch and edges represent shared rooms
    graph = [[] for _ in range(m)]
    for room in range(n):
        if len(switches[room]) == 2:
            s1, s2 = switches[room]
            graph[s1].append(s2)
            graph[s2].append(s1)
    
    # Find all connected components in the graph
    visited = [False] * m
    components = []
    for i in range(m):
        if not visited[i]:
            component = []
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    component.append(node)
                    for neighbor in graph[node]:
                        stack.append(neighbor)
            components.append(component)
    
    # For each component, determine if we can toggle switches to unlock all doors
    for component in components:
        # Count the number of locked and unlocked doors controlled by this component
        locked_count = 0
        unlocked_count = 0
        for switch in component:
            for room in switches[room]:
                if room_status[room] == 0:
                    locked_count += 1
                else:
                    unlocked_count += 1
        
        # If the number of locked doors is odd, it's impossible to unlock all doors
        if locked_count % 2 != 0:
            print("NO")
            return
    
    print("YES")

if __name__ == "__main__":
    main()