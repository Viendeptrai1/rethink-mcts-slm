import sys
from collections import deque, defaultdict

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Read attacked cities
    attacked = []
    for _ in range(m):
        attacked.append(int(next(iterator)))

    # If only one city is attacked, start there, time is 0
    if m == 1:
        print(attacked[0])
        print(0)
        return

    # Helper function to perform BFS and return distances and parents
    def bfs(start_node):
        dist = [-1] * (n + 1)
        parent = [0] * (n + 1)
        queue = deque([start_node])
        dist[start_node] = 0
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)
        return dist, parent

    # Step 1: Find the farthest attacked node from an arbitrary attacked node (e.g., attacked[0])
    dist0, _ = bfs(attacked[0])
    node_a = attacked[0]
    max_dist = -1
    for node in attacked:
        if dist0[node] > max_dist:
            max_dist = dist0[node]
            node_a = node

    # Step 2: Find the farthest attacked node from node_a. This is one endpoint of the diameter.
    dist_a, parent_a = bfs(node_a)
    node_b = node_a
    max_dist = -1
    for node in attacked:
        if dist_a[node] > max_dist:
            max_dist = dist_a[node]
            node_b = node

    # Step 3: Find the farthest attacked node from node_b. This is the other endpoint of the diameter.
    dist_b, parent_b = bfs(node_b)
    node_c = node_b
    max_dist = -1
    for node in attacked:
        if dist_b[node] > max_dist:
            max_dist = dist_b[node]
            node_c = node

    # The diameter of the minimal subtree is the distance between node_b and node_c
    diameter = dist_b[node_c]

    # Step 4: Calculate the number of edges in the minimal subtree.
    # The minimal subtree consists of all nodes and edges on the paths between any pair of attacked nodes.
    # A known property: The number of edges in the minimal subtree connecting a set of nodes S
    # is equal to (sum of distances from an arbitrary root in the subtree to all nodes in S) - (something)?
    # Actually, a simpler way: The minimal subtree is the union of paths from a "virtual root" (e.g., node_b) to all attacked nodes? No.
    # Correct approach: The minimal subtree is the union of paths between all pairs.
    # We can count the number of edges by marking nodes that are part of the minimal subtree.
    # A node is in the minimal subtree if it lies on the path between some pair of attacked nodes.
    # Alternatively, we can use the property: 
    # Size of minimal subtree (edges) = (Sum of degrees in the minimal subtree) / 2.
    # But we don't have the degrees yet.
    # Another property: The number of edges in the minimal subtree connecting a set of nodes is:
    # (Sum of distances from an arbitrary node X in the subtree to all attacked nodes) - (m-1) * something? No.
    # Let's use the standard technique: 
    # 1. Root the tree at node_b (one endpoint of diameter).
    # 2. For each attacked node, find its depth.
    # 3. The minimal subtree edges count can be derived by counting how many nodes are in the minimal subtree.
    #    Let K be the number of nodes in the minimal subtree. Then edges = K - 1.
    #    How to find K? A node is in the minimal subtree if and only if it is an ancestor of at least two attacked nodes (in the tree rooted at node_b) OR it is an attacked node itself.
    #    Wait, if we root at node_b, then the minimal subtree is formed by the union of paths from node_b to all attacked nodes? 
    #    NO. The minimal subtree connecting a set of nodes is NOT necessarily connected to a specific root unless that root is in the set.
    #    However, node_b IS in the set (attacked). So if we root the tree at node_b, the minimal subtree connecting all attacked nodes is exactly the union of paths from node_b to every attacked node.
    #    Why? Because node_b is one of the endpoints of the diameter. Any path between two attacked nodes u and v must pass through the "virtual" structure. 
    #    Actually, if we root at node_b, the path between any two attacked nodes u and v goes u -> LCA(u,v) -> v. Since node_b is an ancestor of everyone (if we consider the whole tree rooted at node_b), the LCA of any two attacked nodes is also an ancestor of both.
    #    The union of paths from node_b to all attacked nodes covers all edges in the minimal subtree.
    #    Proof: The minimal subtree is the smallest connected subgraph containing all attacked nodes. Since node_b is in the set, any path from node_b to any other attacked node must be in the minimal subtree. Conversely, any edge in the minimal subtree must lie on a path between some pair of attacked nodes. Since node_b is an endpoint of the diameter, it is "extremal". 
    #    Actually, is it true that the minimal subtree is the union of paths from node_b to all attacked nodes?
    #    Consider attacked nodes {2, 4, 5, 6} in the example. Tree: 1-2, 2-3, 2-4, 4-5, 4-6.
    #    Diameter endpoints: 2 and 5 (dist 2) or 2 and 6 (dist 2) or 5 and 6 (dist 2). 
    #    Let's say we picked node_b = 2.
    #    Paths from 2 to attacked:
    #    2->2 (len 0)
    #    2->4 (len 1)
    #    2->5 (len 2: 2-4-5)
    #    2->6 (len 2: 2-4-6)
    #    Union of edges: (2,4), (4,5), (4,6). Total 3 edges.
    #    Is this the minimal subtree? Yes. It connects 2, 4, 5, 6.
    #    So yes, if we root at one endpoint of the diameter (node_b), the minimal subtree is the union of paths from node_b to all attacked nodes.
    #    Therefore, the number of edges in the minimal subtree is simply the sum of distances from node_b to all attacked nodes?
    #    NO. Sum of distances counts edges multiple times.
    #    We need the number of UNIQUE edges in the union of these paths.
    #    Since the tree is rooted at node_b, the union of paths from root to a set of nodes is simply the set of all ancestors of those nodes (including the nodes themselves).
    #    The number of edges is (Number of nodes in the union) - 1.
    #    How to count the number of nodes in the union of paths from root to a set of nodes?
    #    A node is in the union if it is an ancestor of at least one attacked node.
    #    We can mark all attacked nodes, then propagate "is_attacked" up the tree. If a node has any child marked, it is marked.
    #    Then count the marked nodes.
    
    # Let's implement this counting.
    # We need the parent pointers rooted at node_b. We already have parent_b from the BFS starting at node_b.
    # But parent_b gives the parent in the BFS tree (which is the same as the tree rooted at node_b since it's a tree).
    
    # Mark attacked nodes
    is_attacked = [False] * (n + 1)
    for node in attacked:
        is_attacked[node] = True

    # Propagate up to find all nodes in the minimal subtree
    # We can do this by processing nodes in decreasing order of depth (from leaves up to root)
    # Or simply: for each attacked node, walk up to root and mark. But that's O(N*M) worst case.
    # Better: Use the parent array. We can compute the "has_attacked_descendant" flag.
    # Initialize has_attacked = is_attacked.
    # Then iterate from deepest nodes up to root.
    # But we don't have depths sorted. We can get depths from dist_b.
    
    # Get depths from dist_b (distance from node_b)
    # Sort nodes by depth descending
    nodes_by_depth = sorted(range(1, n + 1), key=lambda x: dist_b[x], reverse=True)
    
    has_attacked_descendant = list(is_attacked) # Copy
    
    for u in nodes_by_depth:
        if has_attacked_descendant[u]:
            p = parent_b[u]
            if p != 0:
                has_attacked_descendant[p] = True

    # Count nodes in minimal subtree
    subtree_nodes_count = sum(has_attacked_descendant)
    subtree_edges = subtree_nodes_count - 1

    # Calculate time
    # Time = 2 * subtree_edges - diameter
    time_needed = 2 * subtree_edges - diameter

    # Determine start city
    # The start city should be one of the diameter endpoints (node_b or node_c)
    # We need the lexicographically smallest one.
    start_city = min(node_b, node_c)

    print(start_city)
    print(time_needed)

if __name__ == '__main__':
    solve()