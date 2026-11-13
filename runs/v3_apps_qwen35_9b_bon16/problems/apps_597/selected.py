import sys
import sys
from sys import stdin

# Increase recursion depth just in case, though iterative BFS is used.
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list for the tree
    adj = [[] for _ in range(n + 1)]
    
    # Read n-1 edges
    for _ in range(n - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
    
    # Read m attacked cities
    attacked = []
    for _ in range(m):
        attacked.append(int(next(iterator)))
    
    # If only one city to visit, the optimal start is that city itself.
    if m == 1:
        print(attacked[0])
        print(0)
        return

    # To find the optimal starting point, we need to determine the diameter of the set of attacked nodes.
    # The optimal path will start at one endpoint of this diameter, traverse to the other, 
    # and cover all necessary nodes on the way (since the set of attacked nodes forms a subtree).
    # The minimum time required is the length of the diameter of the attacked subgraph.
    # The starting city should be the endpoint of the diameter with the smallest index if there are ties.

    # Step 1: Run BFS from an arbitrary attacked node to find the farthest attacked node.
    # Let's pick attacked[0] as the start.
    start_node = attacked[0]
    
    # BFS to find distances and the farthest node
    def bfs_farthest(start):
        # Queue stores (node, distance)
        queue = [(start, 0)]
        visited = {start}
        farthest_node = start
        max_dist = 0
        
        # Using a list as a queue for BFS
        q_idx = 0
        while q_idx < len(queue):
            u, dist = queue[q_idx]
            q_idx += 1
            
            if dist > max_dist:
                max_dist = dist
                farthest_node = u
            
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append((v, dist + 1))
        
        return farthest_node, max_dist

    # First BFS
    node_u, dist_u = bfs_farthest(start_node)
    
    # Step 2: Run BFS from node_u to find the farthest attacked node (which will be the other end of the diameter)
    node_v, dist_v = bfs_farthest(node_u)
    
    # Step 3: Run BFS from node_v to find the farthest attacked node.
    # The diameter is between node_v and some node_w. We need to check which one gives the max distance.
    # Actually, the standard 2-BFS works for trees to find the diameter endpoints.
    # However, we are only interested in the "diameter of the subset of attacked nodes".
    # Since the attacked nodes form a connected component (a subtree) within the original tree,
    # the diameter of the subset is the same as the diameter of the minimal subtree spanning them.
    # The 2-BFS approach on the tree restricted to the subset works if we run BFS that only visits attacked nodes?
    # No, because BFS must traverse through non-attacked nodes to reach other attacked nodes.
    # But the distance between two attacked nodes in the tree is unique.
    # The "farthest attacked node" from any node X is well-defined.
    
    # Let's refine:
    # 1. Farthest attacked node from attacked[0] is A.
    # 2. Farthest attacked node from A is B.
    # The distance between A and B is the diameter of the set of attacked nodes.
    # Why? Because in a tree, the farthest node from any node is one of the endpoints of the diameter.
    # This property holds for the metric space defined by the tree restricted to the subset of nodes we care about,
    # provided we consider the unique path in the original tree.
    
    # So, node_u is one endpoint. node_v is the other endpoint.
    # The diameter length is dist_v.
    # We need to verify if node_v is indeed an attacked node.
    # The logic: 
    # Let S be the set of attacked nodes.
    # Pick x in S. Find y in S such that dist(x, y) is maximized. This y is an endpoint of the diameter of S.
    # Then find z in S such that dist(y, z) is maximized. This z is the other endpoint, and dist(y, z) is the diameter.
    
    # We need to ensure our BFS "finds the farthest attacked node".
    # Standard BFS finds the farthest node in the whole tree. We need to filter to ensure we pick an attacked node.
    # However, if the farthest node from x in the whole tree is not attacked, it might not be the correct endpoint for S.
    # Example: A -- B -- C -- D. Attacked: A, D. 
    # Start A. Farthest in tree is D (attacked). Correct.
    # Example: A -- B -- C -- D -- E. Attacked: A, D.
    # Start A. Farthest in tree is E (not attacked). Next is D.
    # So we must modify BFS to only consider attacked nodes as candidates for the "farthest" update,
    # but still traverse the whole tree to calculate distances.
    
    def bfs_farthest_attacked(start):
        queue = [(start, 0)]
        visited = {start}
        farthest_node = start
        max_dist = 0
        
        q_idx = 0
        while q_idx < len(queue):
            u, dist = queue[q_idx]
            q_idx += 1
            
            # Check if current node is attacked to update candidate
            # Note: start is guaranteed to be attacked (from the list)
            if u in attacked_set:
                if dist > max_dist:
                    max_dist = dist
                    farthest_node = u
                elif dist == max_dist and u < farthest_node:
                    farthest_node = u
            
            for v in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append((v, dist + 1))
        
        return farthest_node, max_dist

    # Precompute set of attacked nodes for O(1) lookup
    attacked_set = set(attacked)
    
    # Ensure start_node is in attacked_set (it is, by definition)
    node_a, _ = bfs_farthest_attacked(start_node)
    
    # Second BFS from node_a
    node_b, diameter = bfs_farthest_attacked(node_a)
    
    # Now node_a and node_b are the endpoints of the diameter of the attacked set.
    # The minimum time required is diameter.
    # We need to output the starting city. The problem asks for the lowest city number if there are multiple optimal starts.
    # In a tree, the diameter path is unique. The starting point can be either endpoint.
    # If both endpoints give the same time (which they do, the time is the distance), we pick the one with the smaller index.
    
    start_city = min(node_a, node_b)
    
    print(start_city)
    print(diameter)

if __name__ == '__main__':
    solve()