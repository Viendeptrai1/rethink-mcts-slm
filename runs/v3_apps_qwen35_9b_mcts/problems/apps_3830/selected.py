import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    t = int(next(iterator))
    results = []
    
    for _ in range(t):
        n = int(next(iterator))
        s = next(iterator)
        
        # Convert string to a list of integers for easier processing
        # '>' : 1 (clockwise)
        # '<' : -1 (anticlockwise)
        # '-' : 0 (off)
        # We will simulate movement to find connected components and check for cycles.
        
        # Since the graph is a collection of disjoint cycles (or paths that form cycles if we consider the circular nature),
        # a room is returnable if it belongs to a cycle.
        # In this specific circular arrangement with directed/undirected edges:
        # 1. If there is a continuous path of edges going clockwise that wraps around the circle, all nodes in that path are part of a cycle.
        # 2. Similarly for anticlockwise.
        # 3. If a node has an outgoing edge but cannot reach itself (e.g., a dead end in a linear segment that doesn't wrap), it's not returnable.
        # However, because the structure is a single circle of nodes, any connected component that allows movement in a consistent direction around the loop is a cycle.
        # If a component is a "line" segment (e.g., > > < <) that doesn't wrap around fully, the endpoints are not returnable.
        
        # Strategy:
        # Identify connected components. For each component, check if it forms a cycle.
        # A component forms a cycle if every node in the component has exactly 2 edges connecting to other nodes in the component (one incoming, one outgoing in the cycle sense).
        # Actually, simpler: In a functional graph where each node has out-degree 1 (if we resolve '-' arbitrarily or check reachability), a node is part of a cycle if it can reach itself.
        # But here, nodes can have out-degree 0, 1, or 2.
        
        # Let's use a visited array and try to traverse from each unvisited node.
        # If we can return to the start node, all nodes in that traversal path are returnable.
        # Since the graph is small enough (sum of N <= 300,000), O(N) per test case is fine.
        
        # We can model this as: from each node, try to go clockwise as much as possible, then anticlockwise? No, direction is fixed per edge.
        # Correct approach:
        # Build adjacency list.
        # For each node i:
        #   adj[i] = []
        #   if s[i] == '>': adj[i].append((i+1)%n)
        #   if s[i] == '<': adj[(i+1)%n].append(i)  # Wait, '<' at index i means edge from (i+1) to i. So add i to adj[i+1]
        #   if s[i] == '-': adj[i].append((i+1)%n); adj[(i+1)%n].append(i)
        
        # Then run DFS/BFS to find cycles.
        # A node is returnable if it is part of a cycle.
        # Since the graph is a set of disjoint components, and each component is either a simple cycle or a set of paths leading to a cycle or dead ends.
        # Actually, in this specific topology (circle of nodes), a component is a cycle if and only if every node in the component has degree 2 (considering only edges within the component).
        # Wait, degree in the component:
        # If a component is a simple cycle, every node has exactly 2 neighbors in the component.
        # If a component is a path (not wrapping), the endpoints have degree 1, internal nodes degree 2.
        # So, a node is returnable iff it belongs to a component where every node has degree 2.
        # This is equivalent to: the component is a simple cycle.
        
        # Algorithm:
        # 1. Build adjacency list.
        # 2. Find connected components.
        # 3. For each component, count the number of nodes and the sum of degrees (within the component).
        #    If sum of degrees == 2 * num_nodes, then it's a collection of cycles. Since it's connected, it's a single cycle.
        #    All nodes in such a component are returnable.
        #    Otherwise, no node in this component is returnable (it's a path or tree-like structure, but here only paths).
        
        adj = [[] for _ in range(n)]
        for i in range(n):
            char = s[i]
            u = i
            v = (i + 1) % n
            if char == '>':
                adj[u].append(v)
            elif char == '<':
                adj[v].append(u)
            elif char == '-':
                adj[u].append(v)
                adj[v].append(u)
        
        visited = [False] * n
        returnable_count = 0
        
        for i in range(n):
            if not visited[i]:
                # BFS/DFS to find component
                component_nodes = []
                stack = [i]
                visited[i] = True
                while stack:
                    u = stack.pop()
                    component_nodes.append(u)
                    for v in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            stack.append(v)
                
                # Check if this component is a simple cycle
                # In a simple cycle, every node must have exactly 2 neighbors in the component.
                # Note: The adjacency list contains all neighbors. Since the component is connected and we extracted all reachable nodes,
                # we just need to check the degree of each node in the original graph restricted to this component.
                # But since the graph is undirected for connectivity purposes (we treat '-' as undirected for component finding, and '>'/'<' as directed but we traverse both ways for connectivity? 
                # Wait, the problem says "snakes can travel". So connectivity is based on directed edges?
                # "A room is returnable if the snake there can leave the room, and later come back to it".
                # This implies reachability in the directed graph.
                # My previous logic about "component degree 2" assumed undirected connectivity.
                # Let's re-evaluate.
                
                # The graph is directed.
                # A node is returnable if it is part of a directed cycle.
                # In this specific graph (circle of nodes), a directed cycle must go either fully clockwise or fully anticlockwise around the circle.
                # Why? Because to go from i to j and back to i, you must traverse the whole circle in one direction.
                # If you go clockwise from i to j, you can only go back to i if there is a path from j to i.
                # If the path from i to j is clockwise, the path from j to i must be anticlockwise.
                # But the edges are fixed.
                # Case 1: All edges in a segment are '>'. Then you can go i -> i+1 -> ... -> j. To come back, you need '<' or '-' edges going backwards.
                # If there is a mix, say > > < <, you can go 0->1->2, but from 2 you can go to 1 (via <) and 0 (via <). So 0,1,2,3 form a cycle?
                # Let's trace: 0->1 (>), 1->2 (>), 2->1 (<), 1->0 (<).
                # Cycle: 0->1->0. Yes. 1->2->1. Yes.
                # So 0, 1, 2 are returnable. What about 3?
                # If s = ">>><", edges: 0->1, 1->2, 2->3, 3->2.
                # 0->1->2->3 (stuck, 3 only goes to 2). 3->2->1->0->1... no way back to 3.
                # So 3 is not returnable.
                # 0, 1, 2: 0->1->2->1->0. Yes.
                # So it seems a node is returnable if it is part of a "strongly connected component" that is non-trivial (size > 1) or a self-loop (not possible here as n>=2 and no self edges).
                # Actually, in this graph, any non-trivial SCC is a cycle.
                # And since the graph is a circle, SCCs are either single nodes (if no cycle) or the whole circle (if fully connected in one direction) or segments?
                # Let's reconsider the ">>><" example.
                # Edges: 0->1, 1->2, 2->3, 3->2.
                # SCCs: {0}, {1, 2}, {3}.
                # {1, 2} is a cycle (1->2->1). So 1 and 2 are returnable.
                # 0 can reach 1, but 1 cannot reach 0. So 0 is not returnable.
                # 3 can reach 2, but 2 cannot reach 3. So 3 is not returnable.
                # So the answer is 2.
                
                # How to count efficiently?
                # We can find SCCs using Tarjan's or Kosaraju's algorithm.
                # Since N is up to 300,000, O(N) is required.
                # Tarjan's is O(V+E). Here V=N, E <= 2N. So it's efficient.
                
                # Implementation of Tarjan's:
                # ids, low, stack, on_stack
                pass
        
        # Let's implement Tarjan's inside the loop.
        
        ids = [-1] * n
        low = [0] * n
        on_stack = [False] * n
        stack = []
        id_counter = 0
        scc_count = 0
        scc_sizes = []
        
        def dfs(at):
            nonlocal id_counter, scc_count
            stack.append(at)
            on_stack[at] = True
            ids[at] = low[at] = id_counter
            id_counter += 1
            
            for to in adj[at]:
                if ids[to] == -1:
                    dfs(to)
                    low[at] = min(low[at], low[to])
                elif on_stack[to]:
                    low[at] = min(low[at], ids[to])
            
            if ids[at] == low[at]:
                scc_count += 1
                size = 0
                while True:
                    node = stack.pop()
                    on_stack[node] = False
                    size += 1
                    if node == at:
                        break
                scc_sizes.append(size)
        
        for i in range(n):
            if ids[i] == -1:
                dfs(i)
        
        # Count returnable rooms: sum of sizes of SCCs with size > 1
        # Note: In this problem, a self-loop (size 1) is not possible because edges are between i and (i+1)%n, and n>=2.
        # So any SCC of size 1 is not a cycle.
        # Any SCC of size > 1 is a cycle.
        
        ans = 0
        for size in scc_sizes:
            if size > 1:
                ans += size
        
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()