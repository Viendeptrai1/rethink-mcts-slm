import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
    except StopIteration:
        return

    # Build adjacency list and store edge indices
    adj = [[] for _ in range(n + 1)]
    edges = []
    
    for i in range(n - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append((v, i))
        adj[v].append((u, i))
        edges.append((u, v))

    # We need to find the minimal r such that we can color edges with r colors
    # where at most k nodes have >= 2 edges of the same color.
    #
    # Strategy:
    # 1. Binary search for r in range [1, n-1].
    # 2. Check function:
    #    - Perform a DFS (post-order traversal logic implicitly via recursion).
    #    - For each node, we need to assign colors to its incident edges.
    #    - The constraint is local: a node is "bad" if it has >= 2 edges of the same color.
    #    - To minimize bad nodes, we want to avoid reusing colors at the same node.
    #    - However, the global constraint is that we can have at most k bad nodes.
    #    - Actually, the problem allows us to choose WHICH nodes are bad.
    #    - The optimal strategy for a fixed r is:
    #      Traverse the tree. For each node, look at the colors used by edges to its children.
    #      Also consider the edge to its parent.
    #      We need to assign a color to the parent edge (if exists) and child edges.
    #      Wait, the standard greedy approach for this specific problem (Codeforces 1043D / similar) is:
    #      We can designate at most k nodes to be "bad". At a bad node, we can reuse colors freely.
    #      At a good node, all incident edges must have distinct colors.
    #      To minimize r, we should try to make nodes good whenever possible.
    #      But making a node good requires r >= degree(node).
    #      If r < degree(node), the node MUST be bad.
    #      So, if we fix r, the set of nodes that MUST be bad is {v | degree(v) > r}.
    #      Let count_bad_mandatory = number of nodes with degree > r.
    #      If count_bad_mandatory <= k, is it always possible?
    #      Not necessarily. Even if degree <= r, we might be forced to reuse a color if the parent edge uses a color that conflicts with a child edge, AND we don't want to make the parent bad.
    #      Actually, the condition is simpler:
    #      In a tree, we can root it arbitrarily (say at node 1).
    #      For any node u, let d(u) be its degree.
    #      If we decide u is a "good" node, then all edges incident to u must have distinct colors. This requires r >= d(u).
    #      If we decide u is a "bad" node, we can reuse colors.
    #      The constraint is: number of bad nodes <= k.
    #      So, we must select a set S of nodes with |S| <= k to be bad.
    #      For all v not in S, degree(v) <= r.
    #      Is that sufficient?
    #      Consider the edge coloring. If we root the tree, for a node u not in S, the edge to parent and edges to children must all be distinct.
    #      The colors used by children edges are determined by the children's constraints.
    #      Actually, there is a known result for this problem:
    #      The minimum r is max(1, max_degree - k + 1) ? No.
    #      Let's re-evaluate.
    #      If we have r colors.
    #      At a node u, if we want it to be good, we need d(u) distinct colors. So r >= d(u).
    #      If r < d(u), u MUST be bad.
    #      So, any node with d(u) > r is automatically bad.
    #      Let mandatory_bad = count of nodes with d(u) > r.
    #      If mandatory_bad > k, then r is too small.
    #      Is it true that if mandatory_bad <= k, then r is sufficient?
    #      Yes. Because we can simply declare all nodes with d(u) > r as bad (there are <= k of them).
    #      For all other nodes (good nodes), d(u) <= r.
    #      Can we always color the tree such that good nodes have distinct incident colors?
    #      Yes, using a greedy DFS.
    #      Root the tree at node 1.
    #      DFS(u, parent_color):
    #        Used colors at u = {parent_color} (if parent exists).
    #        For each child v:
    #          If u is bad: assign any color (e.g., 1) to edge (u,v).
    #          If u is good: assign the smallest color in [1, r] not in Used colors.
    #          Recurse DFS(v, assigned_color).
    #      Since for good nodes, d(u) <= r, and we only need to avoid at most d(u)-1 colors (parent + other children already assigned), we will always find a free color.
    #      Wait, the order matters. When processing children, we assign colors one by one.
    #      At node u (good), we have parent_color. We need to assign colors to child edges.
    #      We have d(u)-1 children. We need d(u) distinct colors total.
    #      We have r colors available. Since d(u) <= r, we can pick d(u) distinct colors including parent_color.
    #      So the greedy strategy works.
    #
    #      Therefore, the condition is simply: count of nodes with degree > r must be <= k.
    #      We need the smallest r such that count(deg > r) <= k.
    #      This is equivalent to: r >= max_degree_of_nodes_that_are_not_bad.
    #      Actually, we can just sort degrees.
    #      Let degrees be sorted in descending order: d1 >= d2 >= ... >= dn.
    #      We need to pick r such that the number of di > r is <= k.
    #      This means we can allow the top k degrees to be > r, but the (k+1)-th largest degree must be <= r.
    #      So, if we sort degrees descending, let the (k+1)-th degree be D (if k < n, else 0).
    #      Then r must be at least D.
    #      Also r must be at least 1.
    #      So r = max(1, D).
    #      Wait, let's verify.
    #      If we set r = D, then any node with degree > D will be in the top k (since D is the (k+1)-th largest).
    #      So there are at most k nodes with degree > r.
    #      And for any node with degree <= r, we can make it good.
    #      So the answer is simply the (k+1)-th largest degree (or 1 if k >= n-1, but k <= n-1).
    #      Wait, if k = n-1, then we can have all nodes bad. Then r=1 is enough?
    #      If r=1, then any node with degree > 1 is bad.
    #      If we have a star graph with center degree n-1.
    #      If k = n-1, we can make the center bad. Then r=1 works.
    #      Formula: Sort degrees descending. Take the element at index k (0-based).
    #      If k >= n, then index out of bounds, but k <= n-1.
    #      Indices: 0 to n-1.
    #      We want the (k+1)-th largest. That is index k in 0-based sorted list.
    #      Example 1: n=6, k=2.
    #      Edges: (1,4), (4,3), (3,5), (3,6), (5,2).
    #      Degrees:
    #      1: 1
    #      2: 1
    #      3: 3 (connected to 4,5,6)
    #      4: 2 (connected to 1,3)
    #      5: 2 (connected to 3,2)
    #      6: 1
    #      Degrees: [1, 1, 3, 2, 2, 1]
    #      Sorted desc: [3, 2, 2, 1, 1, 1]
    #      k=2. We look at index 2 (0-based). Value is 2.
    #      So r = 2. Correct.
    #
    #      Example 2: n=4, k=2.
    #      Edges: (3,1), (1,4), (1,2).
    #      Degrees:
    #      1: 3
    #      2: 1
    #      3: 1
    #      4: 1
    #      Sorted desc: [3, 1, 1, 1]
    #      k=2. Index 2 is 1.
    #      r = 1. Correct.
    #
    #      Example 3: n=10, k=2.
    #      Degrees calculation...
    #      Let's trust the logic.
    #      r = sorted_degrees[k] (descending sort).
    #      If k >= n, r=1? But k <= n-1.
    #      Wait, if k = n-1, index is n-1. The smallest degree.
    #      If all degrees are 1 (line graph), sorted: [1, 1, ...]. Index n-1 is 1. r=1. Correct.
    #      If star graph, center n-1, leaves 1. Sorted: [n-1, 1, 1, ...].
    #      If k = n-1, index n-1 is 1. r=1. Correct (center is bad).
    #      If k = 0, index 0 is n-1. r = n-1. Correct (no bad nodes allowed, so r must be max degree).
    #
    #      So the algorithm is:
    #      1. Calculate degrees.
    #      2. Sort degrees descending.
    #      3. r = degrees[k].
    #      4. Construct the coloring using DFS with r colors.
    #         - Identify bad nodes: those with degree > r.
    #         - DFS(u, p_color):
    #             used = {p_color} if p_color != -1 else set()
    #             for v, idx in adj[u]:
    #                 if v == p: continue
    #                 if u is bad:
    #                     color = 1
    #                 else:
    #                     # find smallest color in 1..r not in used
    #                     color = 1
    #                     while color in used:
    #                         color += 1
    #                 assign color to edge idx
    #                 DFS(v, color)
    #
    #      Wait, one edge case: if r=1, and we have a node with degree > 1, it is bad.
    #      The logic holds.
    
    degrees = [0] * (n + 1)
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    
    # Sort degrees descending, ignoring index 0
    deg_list = sorted(degrees[1:], reverse=True)
    
    # Determine r
    # We need the (k+1)-th largest degree.
    # In 0-indexed sorted list, this is index k.
    r = deg_list[k]
    if r < 1:
        r = 1
        
    # Now construct the solution
    # Identify bad nodes
    bad_nodes = set()
    for i in range(1, n + 1):
        if degrees[i] > r:
            bad_nodes.add(i)
            
    # Result array for edge colors
    # edges list is 0-indexed corresponding to input order
    result_colors = [0] * (n - 1)
    
    # We need a DFS. Since recursion limit is set, we can use recursive function.
    # But to avoid recursion depth issues on some platforms or for clarity, iterative DFS is safer?
    # Given n=200,000, recursion limit set to 300,000 should be fine in Python.
    
    # We need to map edge index to color.
    # adj stores (neighbor, edge_index)
    
    # To handle the "parent color" logic, we pass it in DFS.
    
    def dfs(u, p, p_color):
        # p_color is the color of the edge (p, u). If p is -1, p_color is None.
        used_colors = set()
        if p != -1:
            used_colors.add(p_color)
        
        # Determine if u is bad
        is_bad = (u in bad_nodes)
        
        for v, idx in adj[u]:
            if v == p:
                continue
            
            if is_bad:
                # Can reuse any color, pick 1
                c = 1
            else:
                # Must pick a color not in used_colors
                c = 1
                while c in used_colors:
                    c += 1
                # Since degree(u) <= r and we have at most (degree(u)-1) other edges + parent,
                # and we are picking sequentially, we will find a color <= r.
                # Actually, we need to ensure we don't exceed r.
                # The number of used colors so far is at most (degree(u) - 1).
                # Since degree(u) <= r, and we start from 1, the next available is at most degree(u) <= r.
                # So c will be <= r.
            
            result_colors[idx] = c
            dfs(v, u, c)

    # Start DFS from node 1, parent -1, parent_color 0 (or None)
    # Using 0 as dummy color since colors are 1-based.
    dfs(1, -1, 0)
    
    # Output
    print(r)
    print(*(result_colors))

if __name__ == '__main__':
    solve()