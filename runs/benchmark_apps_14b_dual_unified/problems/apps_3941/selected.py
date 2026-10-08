import sys
from collections import defaultdict, deque

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
    
    switches = []
    for _ in range(m):
        x = int(data[index])
        index += 1
        switch_rooms = list(map(int, data[index:index + x]))
        index += x
        switches.append(switch_rooms)
    
    # Create a graph where each room is a node and each switch is an edge
    graph = defaultdict(list)
    for i in range(m):
        for j in range(len(switches[i])):
            for k in range(j + 1, len(switches[i])):
                u = switches[i][j]
                v = switches[i][k]
                graph[u].append(v)
                graph[v].append(u)
    
    # Check if the graph is bipartite
    def is_bipartite(graph, n):
        color = [-1] * (n + 1)
        for start in range(1, n + 1):
            if color[start] == -1:
                queue = deque([start])
                color[start] = 0
                while queue:
                    node = queue.popleft()
                    for neighbor in graph[node]:
                        if color[neighbor] == -1:
                            color[neighbor] = 1 - color[node]
                            queue.append(neighbor)
                        elif color[neighbor] == color[node]:
                            return False
        return True
    
    if not is_bipartite(graph, n):
        print("NO")
        return
    
    # If the graph is bipartite, check if we can make all doors unlocked
    # We need to count the number of locked and unlocked rooms in each partition
    locked_count = sum(room_status)
    unlocked_count = n - locked_count
    
    # If the number of locked rooms is even, we can always make all doors unlocked
    if locked_count % 2 == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()