import sys
from collections import defaultdict, deque

def find_farthest_node(tree, start):
    visited = [False] * len(tree)
    queue = deque([(start, 0)])
    farthest_node = start
    max_distance = 0
    
    while queue:
        node, distance = queue.popleft()
        if distance > max_distance:
            max_distance = distance
            farthest_node = node
        visited[node] = True
        for neighbor in tree[node]:
            if not visited[neighbor]:
                queue.append((neighbor, distance + 1))
    
    return farthest_node, max_distance

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
    
    # Find the farthest node from an arbitrary starting node (0)
    node1, _ = find_farthest_node(tree, 0)
    
    # Find the farthest node from node1
    node2, _ = find_farthest_node(tree, node1)
    
    # Find the farthest node from node2
    node3, _ = find_farthest_node(tree, node2)
    
    # The path from node1 to node3 will include the longest path in the tree
    # We need to find two more nodes on this path to maximize the number of edges covered
    # The optimal choice is to take the two endpoints of the longest path
    path = []
    visited = [False] * n
    queue = deque([(node1, 0)])
    
    while queue:
        node, distance = queue.popleft()
        if node == node3:
            break
        visited[node] = True
        for neighbor in tree[node]:
            if not visited[neighbor]:
                queue.append((neighbor, distance + 1))
                path.append(neighbor)
    
    # The path from node1 to node3 includes all nodes in the path list
    # We need to choose two more nodes from this path to maximize the number of edges covered
    # The optimal choice is to take the two endpoints of the longest path
    a = node1 + 1
    b = node3 + 1
    c = path[-1] + 1
    
    res = len(path) + 1  # +1 for the edge between node1 and node3
    print(res)
    print(a, b, c)

if __name__ == "__main__":
    main()