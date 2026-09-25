import sys
from collections import defaultdict, deque

def find_centroid(tree, n):
    def dfs(node, parent):
        size[node] = 1
        max_subtree = 0
        for neighbor in tree[node]:
            if neighbor != parent:
                dfs(neighbor, node)
                size[node] += size[neighbor]
                max_subtree = max(max_subtree, size[neighbor])
        max_subtree = max(max_subtree, n - size[node])
        if max_subtree < min_size[0]:
            min_size[0] = max_subtree
            centroid[0] = node

    size = [0] * n
    min_size = [float('inf')]
    centroid = [None]
    dfs(0, -1)
    return centroid[0]

def bfs_distance(tree, start):
    distance = [-1] * len(tree)
    queue = deque([start])
    distance[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in tree[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    tree = defaultdict(list)
    index = 1
    for _ in range(n - 1):
        a = int(data[index]) - 1
        b = int(data[index + 1]) - 1
        tree[a].append(b)
        tree[b].append(a)
        index += 2
    
    # Find the centroid of the tree
    centroid = find_centroid(tree, n)
    
    # Perform BFS from the centroid to find the farthest nodes
    distances = bfs_distance(tree, centroid)
    farthest_node_1 = distances.index(max(distances))
    distances = bfs_distance(tree, farthest_node_1)
    farthest_node_2 = distances.index(max(distances))
    distances = bfs_distance(tree, farthest_node_2)
    farthest_node_3 = distances.index(max(distances))
    
    # Calculate the number of edges covered by the paths between the three farthest nodes
    res = sum(distances) // 2
    
    # Print the result
    print(res)
    print(farthest_node_1 + 1, farthest_node_2 + 1, farthest_node_3 + 1)

if __name__ == "__main__":
    main()