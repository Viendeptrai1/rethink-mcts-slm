import sys

# Increase recursion depth just in case, though we will use an iterative approach for search
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    # We need to store node info. 
    # The input gives v, l, r for each node. 
    # The problem statement implies the lines correspond to nodes 1 to n.
    # However, the example note says "root of the tree in vertex 2", implying the input order 
    # defines the nodes, but the root is identified by who has no parent.
    # Let's store nodes in a list where index i corresponds to node i+1 (0-based index in list).
    
    # To handle 1-based indexing from input easily, we can make our arrays size n+1.
    # But since we read n lines, let's just store them in a list of size n, 
    # and map input index i (1-based) to list index i-1.
    
    values = [0] * n
    left = [-1] * n
    right = [-1] * n
    
    # Track parents to find the root
    has_parent = [False] * n
    
    for i in range(n):
        v = int(next(iterator))
        l = int(next(iterator))
        r = int(next(iterator))
        
        values[i] = v
        
        # Adjust 1-based indices to 0-based
        if l != -1:
            l_idx = l - 1
            left[i] = l_idx
            has_parent[l_idx] = True
        else:
            left[i] = -1
            
        if r != -1:
            r_idx = r - 1
            right[i] = r_idx
            has_parent[r_idx] = True
        else:
            right[i] = -1
            
    # Find root
    root = -1
    for i in range(n):
        if not has_parent[i]:
            root = i
            break
            
    if root == -1:
        # Should not happen based on problem constraints
        print(0)
        return

    # Count frequencies of each value
    from collections import Counter
    val_counts = Counter(values)
    
    # Get unique values to search
    unique_values = sorted(val_counts.keys())
    
    total_failures = 0
    
    # For each unique value, run the search algorithm once
    for x in unique_values:
        # Iterative search to avoid recursion depth issues and overhead
        curr = root
        found = False
        
        while curr != -1:
            if values[curr] == x:
                found = True
                break
            elif x < values[curr]:
                curr = left[curr]
            else:
                curr = right[curr]
        
        if not found:
            # The search failed for this value
            total_failures += val_counts[x]
            
    print(total_failures)

if __name__ == '__main__':
    solve()