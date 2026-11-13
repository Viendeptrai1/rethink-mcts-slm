import sys

# Increase recursion depth just in case, though we will use iterative DFS for safety
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        q = int(next(iterator))
    except StopIteration:
        return

    # Build adjacency list for the tree
    # Officers are 1-indexed. We'll use a list of lists.
    # p_i is the parent of officer i+2 (since p_2 is for officer 2, etc.)
    # The input gives n-1 integers: p_2, p_3, ..., p_n
    # p_i < i constraint ensures no cycles and 1 is root.
    
    adj = [[] for _ in range(n + 1)]
    
    for i in range(2, n + 1):
        parent = int(next(iterator))
        adj[parent].append(i)
    
    # Sort children for each node to ensure minimal index is chosen first
    # This is crucial for the DFS order
    for i in range(1, n + 1):
        adj[i].sort()
    
    # Precompute the DFS traversal order starting from root (1)
    # This gives us the entry time (tin) and the full traversal sequence.
    # However, the problem asks for traversal starting from ANY node u.
    # The traversal from u is simply the subtree of u in the global DFS order,
    # but we need to be careful: the global DFS order is fixed based on sorting children.
    # If we start DFS from u, we visit u, then its first child, etc.
    # This is exactly the segment of the global DFS traversal that corresponds to u's subtree.
    
    # Let's compute the global DFS traversal order (entry times)
    # tin[u] = time when we first visit u
    # We also need to know the size of the subtree to check bounds.
    
    tin = [0] * (n + 1)
    # We can store the global traversal order in a list `order` where order[tin[u]] = u
    order = [0] * (n + 1)
    
    timer = 0
    
    # Iterative DFS to avoid recursion limit issues and to build the order
    stack = [1]
    
    # To simulate the exact DFS behavior (visit node, then children in sorted order),
    # we can just push children in reverse sorted order onto the stack.
    # But wait, standard stack DFS (LIFO) processes the last pushed child first.
    # We want to process the smallest index child first.
    # So if children are [2, 3, 5], we want to visit 2, then 3, then 5.
    # If we push 5, then 3, then 2, the stack top is 2. We pop 2, process it.
    # Then we push 5, 3 (in reverse of remaining).
    # Actually, simpler: just iterate children in sorted order and push them.
    # But since it's a stack, the last pushed is visited first.
    # So we need to push children in REVERSE sorted order.
    
    # Let's refine the iterative DFS:
    # We need to record the time when we ENTER a node.
    # The sequence of entry times defines the order.
    
    # Re-initialize stack for the global traversal from root 1
    stack = [1]
    
    # We need to handle the "enter" event.
    # Standard iterative DFS for preorder traversal:
    # Push root. While stack not empty:
    #   u = pop()
    #   record u
    #   push children in reverse order
    
    # Let's do this carefully.
    # We want the order: u, then child1, then child1's subtree, then child2...
    # If we push child_k, child_{k-1}, ..., child_1 (where child_1 is smallest),
    # then we pop child_1 first. Correct.
    
    # However, we also need to know the subtree size to answer queries efficiently.
    # And we need to map (u, k) to the k-th node in u's subtree traversal.
    
    # Let's compute:
    # 1. Global DFS order (preorder) starting from 1.
    # 2. Subtree size for each node.
    # 3. Entry time (tin) for each node.
    
    # Since the tree structure is static and the traversal rule (sort children by index) is static,
    # the relative order of nodes in any subtree is fixed.
    # The sequence starting from u is simply the nodes in u's subtree appearing in the global preorder traversal.
    # Why? Because the global DFS starts at 1, goes down to u, and then explores u's subtree completely before backtracking.
    # Within u's subtree, the traversal follows the same rules (smallest child first).
    # So the k-th node in the traversal starting from u is the node that appears at offset (k-1) in the list of nodes in u's subtree (in global preorder).
    
    # Algorithm:
    # 1. Compute global preorder traversal list `preorder`.
    # 2. Compute `tin[u]` (index in `preorder` where u appears).
    # 3. Compute `subtree_size[u]`.
    # 4. For a query (u, k):
    #    - If k > subtree_size[u], return -1.
    #    - The node is at index `tin[u] + k - 1` in the `preorder` list.
    #    - Return `preorder[tin[u] + k - 1]`.
    
    # Let's implement the iterative DFS to build `preorder`, `tin`, and `subtree_size`.
    
    preorder = []
    tin = [0] * (n + 1)
    
    # Stack for DFS: stores nodes to visit
    # We also need to compute subtree sizes. 
    # Subtree size = 1 + sum(subtree sizes of children).
    # We can compute this in a post-order traversal or by processing nodes in reverse preorder.
    
    # Step 1: Generate preorder and tin
    stack = [1]
    # To ensure we visit smallest child first, we push children in reverse sorted order.
    # But we already sorted adj[i]. So we slice [::-1].
    
    while stack:
        u = stack.pop()
        preorder.append(u)
        tin[u] = len(preorder) - 1
        
        # Push children in reverse order so smallest is popped first
        # adj[u] is sorted ascending. Reverse it.
        for v in reversed(adj[u]):
            stack.append(v)
            
    # Step 2: Compute subtree sizes
    # We can do this by iterating the preorder list in reverse.
    # The last node in preorder is a leaf (or end of a branch).
    # Its subtree size is 1.
    # When we encounter a node, its size is 1 + sum of sizes of its children.
    # But we don't have children pointers easily in reverse order without looking up.
    # Alternative: Initialize sizes to 1. Iterate preorder in reverse.
    # For each node u (except root), add its size to its parent's size.
    # We need the parent array. We can reconstruct it or store it during input reading.
    
    subtree_size = [1] * (n + 1)
    parent = [0] * (n + 1)
    
    # Reconstruct parent array from input logic or during DFS?
    # We didn't store parents during DFS. Let's reconstruct from the input loop logic or just re-scan.
    # Actually, we have the `adj` list. We can build `parent` array easily.
    # But we already read the input. Let's just rebuild parent array now.
    # Wait, we can just use the fact that we know the tree structure.
    # Let's rebuild parent array from the input data we read earlier? 
    # No, we consumed the iterator. Let's rebuild from adj.
    
    # Actually, simpler: during the initial input reading, we stored `adj`.
    # We can build `parent` array now.
    for i in range(2, n + 1):
        # Find parent of i in adj? No, adj is children list.
        # We need to know who is the parent of i.
        # We can iterate 1..n and for each child in adj[u], set parent[child] = u.
        for v in adj[i]:
            parent[v] = i
            
    # Now compute subtree sizes in reverse preorder
    for i in range(n - 1, -1, -1):
        u = preorder[i]
        if u != 1:
            p = parent[u]
            subtree_size[p] += subtree_size[u]
            
    # Process queries
    results = []
    for _ in range(q):
        u = int(next(iterator))
        k = int(next(iterator))
        
        if k > subtree_size[u]:
            results.append("-1")
        else:
            # The k-th node in u's subtree traversal
            # In global preorder, u is at index tin[u]
            # The nodes in u's subtree form a contiguous segment starting at tin[u]
            # of length subtree_size[u]
            # So the k-th node (1-based) is at index tin[u] + k - 1
            idx = tin[u] + k - 1
            results.append(str(preorder[idx]))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()