import sys
from collections import defaultdict, deque

def minimal_road_companies(n, k, roads):
    # Create adjacency list for the tree
    tree = defaultdict(list)
    for i, (u, v) in enumerate(roads):
        tree[u].append((v, i))
        tree[v].append((u, i))
    
    # BFS to find the farthest node and its distance
    def bfs(start_node):
        visited = [-1] * (n + 1)
        queue = deque([(start_node, 0)])
        visited[start_node] = 0
        farthest_node = start_node
        max_distance = 0
        
        while queue:
            node, dist = queue.popleft()
            if dist > max_distance:
                max_distance = dist
                farthest_node = node
            for neighbor, _ in tree[node]:
                if visited[neighbor] == -1:
                    visited[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
        
        return farthest_node, max_distance

    # Find one end of the longest path
    end1, _ = bfs(1)
    # Find the other end of the longest path
    end2, _ = bfs(end1)

    # Function to determine path from end1 to end2
    def find_path(u, v):
        visited = [-1] * (n + 1)
        queue = deque([u])
        visited[u] = u
        
        while queue:
            node = queue.popleft()
            if node == v:
                break
            for neighbor, _ in tree[node]:
                if visited[neighbor] == -1:
                    visited[neighbor] = node
                    queue.append(neighbor)
        
        path = []
        while v != u:
            path.append(v)
            v = visited[v]
        path.append(u)
        return path[::-1]

    # Get the path from end1 to end2
    path = find_path(end1, end2)
    path_length = len(path)

    # Determine r and coloring
    r = (path_length + k) // (k + 1)
    coloring = [0] * (n - 1)
    
    for i in range(n - 1):
        u, v = roads[i]
        if u in path and v in path:
            # Determine the position in the path
            pos_u = path.index(u)
            pos_v = path.index(v)
            if pos_u > pos_v:
                pos_u, pos_v = pos_v, pos_u
            company = (pos_u + 1) % r + 1
        else:
            # Can be assigned to any company as it's not on the path
            company = 1
        coloring[i] = company

    return r, coloring

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    roads = [(int(data[2 * i]), int(data[2 * i + 1])) for i in range(n - 1)]
    
    r, coloring = minimal_road_companies(n, k, roads)
    
    print(r)
    print(" ".join(map(str, coloring)))

if __name__ == "__main__":
    main()