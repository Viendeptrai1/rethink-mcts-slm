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
    
    # Create a graph where each switch is a node and edges exist between switches controlling the same room
    graph = defaultdict(set)
    for room, switch_list in switches.items():
        for i in range(len(switch_list)):
            for j in range(i + 1, len(switch_list)):
                u, v = switch_list[i], switch_list[j]
                graph[u].add(v)
                graph[v].add(u)
    
    # Function to find the number of connected components in the graph
    def find_connected_components(graph, n):
        visited = [False] * n
        count = 0
        
        def dfs(node):
            stack = [node]
            while stack:
                current = stack.pop()
                if not visited[current]:
                    visited[current] = True
                    for neighbor in graph[current]:
                        stack.append(neighbor)
        
        for node in range(n):
            if not visited[node]:
                dfs(node)
                count += 1
        
        return count
    
    # Number of connected components in the graph
    num_components = find_connected_components(graph, m)
    
    # Check if the number of locked rooms is even and less than or equal to the number of connected components
    locked_count = sum(1 for status in room_status if status == 0)
    
    if locked_count % 2 == 0 and locked_count <= num_components:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()