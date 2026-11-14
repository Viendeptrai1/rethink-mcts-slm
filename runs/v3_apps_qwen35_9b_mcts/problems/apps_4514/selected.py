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
        q = int(next(iterator))
    except StopIteration:
        return

    # Build adjacency list
    # p_i is the parent of node i (for i from 2 to n)
    # We need children lists. Since p_i < i, we can just append.
    children = [[] for _ in range(n + 1)]
    
    for i in range(2, n + 1):
        parent = int(next(iterator))
        children[parent].append(i)
    
    # The problem states: "If there are many such direct subordinates, then a chooses the one having minimal index."
    # So we must sort children lists in ascending order.
    for i in range(1, n + 1):
        children[i].sort()
    
    # Precompute DFS order (pre-order traversal) and subtree sizes for each node
    # dfs_order[u] will store the index in the global DFS sequence where u appears
    # subtree_size[u] will store the size of the subtree rooted at u
    # We also need to map the global DFS index back to the node index.
    
    dfs_order = [0] * (n + 1)
    subtree_size = [0] * (n + 1)
    node_at_dfs_idx = [0] * (n + 1)  # node_at_dfs_idx[t] = node that is at position t in the DFS sequence (1-based)
    
    # Iterative DFS to avoid recursion limit issues and ensure correct order
    # We need to simulate: visit node, then visit first child, then second child, etc.
    # Standard iterative DFS with a stack of (node, child_index)
    
    stack = [(1, 0)]  # (current_node, next_child_index_to_visit)
    timer = 0
    
    # We will build the sequence of nodes visited
    # Actually, we just need to record the order.
    
    while stack:
        u, idx = stack[-1]
        
        if idx == 0:
            # First time visiting u (pre-order)
            timer += 1
            dfs_order[u] = timer
            node_at_dfs_idx[timer] = u
        
        if idx < len(children[u]):
            v = children[u][idx]
            # Push child to stack, reset its child index to 0
            stack.append((v, 0))
            # Increment current node's child index to process next time we return
            stack[-2] = (u, idx + 1)
        else:
            # All children visited, pop
            stack.pop()
            # Calculate subtree size
            # Subtree size = 1 (self) + sum of subtree sizes of children
            # Since we process children before returning, we can accumulate.
            # However, in this iterative approach, we don't have a direct way to sum up children sizes easily 
            # unless we do a post-order pass or accumulate during the process.
            # Let's do a separate pass or accumulate here.
            # Actually, we can accumulate subtree_size during the post-order phase.
            # But wait, the logic above pops u. At that point, all children have been processed.
            # We can sum up children's sizes.
            s = 1
            for v in children[u]:
                s += subtree_size[v]
            subtree_size[u] = s

    # Now process queries
    results = []
    
    for _ in range(q):
        u = int(next(iterator))
        k = int(next(iterator))
        
        # The command starts at u.
        # The sequence of officers receiving the command is the pre-order traversal of the subtree rooted at u.
        # The length of this sequence is subtree_size[u].
        
        if k > subtree_size[u]:
            results.append("-1")
        else:
            # The k-th element in the subtree's pre-order traversal corresponds to:
            # The node that appears at global DFS index: (dfs_order[u] + k - 1)
            global_idx = dfs_order[u] + k - 1
            node = node_at_dfs_idx[global_idx]
            results.append(str(node))
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()