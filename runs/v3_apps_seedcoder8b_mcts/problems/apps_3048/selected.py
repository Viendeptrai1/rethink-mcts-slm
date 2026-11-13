import sys
from collections import defaultdict, deque

def count_optimal_paths_of_length_two(n, roads):
    # Create an adjacency list for the graph
    graph = defaultdict(list)
    for u, v in roads:
        graph[u].append(v)
        graph[v].append(u)
    
    # Function to perform BFS and count paths of length 2
    def bfs_count_paths_of_length_two(start):
        queue = deque([(start, 0)])
        visited = set([start])
        count = 0
        
        while queue:
            node, dist = queue.popleft()
            
            if dist == 2:
                continue
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
                    if dist == 1:
                        count += 1
        
        return count
    
    total_paths = 0
    for node in range(1, n + 1):
        total_paths += bfs_count_paths_of_length_two(node)
    
    return total_paths

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    roads = []
    index = 1
    for _ in range(n - 1):
        u = int(data[index])
        v = int(data[index + 1])
        roads.append((u, v))
        index += 2
    
    result = count_optimal_paths_of_length_two(n, roads)
    print(result)

if __name__ == "__main__":
    main()