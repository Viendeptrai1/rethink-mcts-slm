import sys

# Increase recursion depth just in case, though we will use iterative DFS for the traversal order calculation
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin at once
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        q = int(next(iterator))
    except StopIteration:
        return

    # Read parents for officers 2 to n
    # p_i is the parent of officer i+2 (since we start from index 0 in the list but officers are 1-indexed)
    # Actually, the input gives p_2, p_3, ..., p_n.
    # We need to build an adjacency list where adj[u] contains children of u.
    # Since p_i < i, we can process in order or just build directly.
    
    adj = [[] for _ in range(n + 1)]
    
    # The loop runs for i from 2 to n
    # The values are given in order: p_2, p_3, ..., p_n
    for i in range(2, n + 1):
        p = int(next(iterator))
        adj[p].append(i)
    
    # Precompute the DFS traversal order for the entire tree starting from root (1)
    # Since the problem states: "If there are many such direct subordinates, then a chooses the one having minimal index."
    # We need to sort children by index before traversing to ensure the correct order.
    for u in range(1, n + 1):
        adj[u].sort()
    
    # Perform DFS to generate the global traversal order
    # We use an iterative approach to avoid recursion limit issues and to be efficient
    # Stack stores (node, index_in_children_list)
    # However, a simpler way for generating the visit order (pre-order) is:
    # Push root, while stack not empty: pop node, add to list, push children in reverse order (so smallest index is popped first)
    
    dfs_order = []
    stack = [1]
    
    while stack:
        u = stack.pop()
        dfs_order.append(u)
        
        # To ensure we visit children in increasing order of index,
        # we push them in decreasing order.
        # Since adj[u] is sorted ascending, we reverse it or slice with step -1
        for child in reversed(adj[u]):
            stack.append(child)
            
    # Now we have the full DFS order for the whole tree starting at 1.
    # The query is (u, k): simulate command spreading starting from u.
    # The command spreading logic is identical to the DFS described, but starting from u.
    # This effectively means we take the segment of the global DFS order that belongs to the subtree of u.
    # Why? Because the relative order of visiting nodes in a subtree depends only on the structure of the subtree and the sorting rule (min index child first).
    # The global DFS traversal visits the subtree of u completely before moving to other branches of u's ancestors or other branches of u.
    # And within the subtree of u, the visit order is exactly the same as if we ran DFS starting from u on that subtree.
    
    # So, we need to find the start index of u in the dfs_order list.
    # Then the sequence for query (u, k) is dfs_order[start_index : start_index + size_of_subtree(u)]
    # The k-th element (1-based) corresponds to index start_index + k - 1.
    
    # We need to quickly find the start index and the size of the subtree.
    # Let's build these arrays.
    
    # Map node -> start index in dfs_order
    start_index = {}
    # Map node -> subtree size
    subtree_size = {}
    
    # We can compute subtree sizes and start indices during a post-order traversal or by using the dfs_order array properties.
    # Actually, since we have dfs_order, we can compute subtree sizes by looking at ranges if we know where each subtree ends.
    # Alternatively, standard DFS to compute size and entry time.
    
    # Let's do a quick DFS to compute sizes and entry times.
    # Since n is up to 2*10^5, recursion might hit limits, so iterative DFS is safer.
    
    # Iterative DFS for entry times and subtree sizes
    # We need to process a node after its children to get the size.
    # Stack will store (node, child_index)
    
    entry_time = [0] * (n + 1)
    # We already have dfs_order, so entry_time[u] is simply the index of u in dfs_order
    for idx, u in enumerate(dfs_order):
        entry_time[u] = idx
        
    # Compute subtree sizes
    # Initialize with 1 (the node itself)
    subtree_size = [1] * (n + 1)
    
    # Process nodes in reverse DFS order (bottom-up)
    # In reverse dfs_order, children appear before parents.
    for u in reversed(dfs_order):
        # Add the size of this subtree to its parent
        p = adj[0][0] # dummy, we need to find parent. Wait, we didn't store parent array explicitly in a way to access quickly?
        # Actually, we can reconstruct parent or store it.
        # But wait, we have the tree structure. When we are at u, we want to add subtree_size[u] to subtree_size[parent[u]].
        # We need the parent array. Let's build it.
        pass

    # Re-building parent array
    parent = [0] * (n + 1)
    # We have adj, but adj is children list. We can build parent from the input loop we did earlier.
    # Let's re-do that part cleanly.
    
    # Reset adj and parent to be sure
    adj = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    
    # Re-read input logic for parents
    # We already consumed n, q, and the first n-1 integers in the iterator.
    # Let's re-parse carefully.
    # The iterator is currently pointing after the first n-1 integers.
    # Actually, let's just reconstruct the parent array from the input we read.
    # The input format: p_2, p_3, ..., p_n.
    # We can just rebuild adj and parent from scratch by re-reading or if we stored them.
    # Since we are inside solve(), and we used `next(iterator)` to build adj, we can just store parent there.
    
    # Let's restart the input parsing logic inside the function to be clean and self-contained.
    pass

# Re-writing the entire logic cleanly in one block to avoid confusion

def run_solution():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        q = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    
    # Read p_2 ... p_n
    for i in range(2, n + 1):
        p = int(next(iterator))
        adj[p].append(i)
        parent[i] = p
        
    # Sort adjacency lists to satisfy "minimal index" condition
    for i in range(1, n + 1):
        adj[i].sort()
        
    # Generate global DFS order (pre-order)
    dfs_order = []
    stack = [1]
    while stack:
        u = stack.pop()
        dfs_order.append(u)
        # Push children in reverse order so smallest is popped first
        for child in reversed(adj[u]):
            stack.append(child)
            
    # Map node to its entry time (index in dfs_order)
    entry_time = [0] * (n + 1)
    for idx, u in enumerate(dfs_order):
        entry_time[u] = idx
        
    # Compute subtree sizes using reverse dfs_order
    subtree_size = [1] * (n + 1)
    for u in reversed(dfs_order):
        p = parent[u]
        if p != 0:
            subtree_size[p] += subtree_size[u]
            
    # Process queries
    results = []
    for _ in range(q):
        u = int(next(iterator))
        k = int(next(iterator))
        
        start_idx = entry_time[u]
        end_idx = start_idx + subtree_size[u] - 1
        
        if k > subtree_size[u]:
            results.append("-1")
        else:
            # k is 1-based, so index is start_idx + k - 1
            results.append(str(dfs_order[start_idx + k - 1]))
            
    print('\n'.join(results))

if __name__ == '__main__':
    run_solution()