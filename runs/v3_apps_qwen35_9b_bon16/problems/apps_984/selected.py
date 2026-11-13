import sys

# Increase recursion depth for deep trees up to 10^5
sys.setrecursionlimit(200000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    # Arrays to store tree properties
    # Values, left child index, right child index
    # Indices are 0-based in our implementation, but input is 1-based for children
    values = [0] * n
    left = [-1] * n
    right = [-1] * n

    # Root is unknown initially. We need to find it.
    # Input gives n lines. The first line of input after n corresponds to some node.
    # The problem statement says "First line contains... Each of the next n lines...".
    # It does not explicitly state the order of vertices. However, usually in such problems,
    # the vertices are given in an arbitrary order, and we must deduce the root.
    # We can track which nodes have a parent. The one without a parent is the root.
    has_parent = [False] * n

    for i in range(n):
        val = int(next(iterator))
        l = int(next(iterator))
        r = int(next(iterator))
        
        values[i] = val
        
        # Store children. If child index is -1, it means no child.
        # Otherwise, adjust to 0-based index.
        if l != -1:
            left[i] = l - 1
            has_parent[l - 1] = True
        if r != -1:
            right[i] = r - 1
            has_parent[r - 1] = True

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

    # Count how many times search fails for every value in the tree.
    # We need to simulate the search for each unique value present in the tree nodes.
    # Actually, the problem says: "run algorithm on every value from the tree T".
    # "If the tree has multiple vertices with the same values on them then you should run algorithm on every one of them separately."
    # This implies we iterate over all nodes, extract their value, run the search for that value,
    # and count failures. Since multiple nodes can have the same value, we count each node's search attempt.
    
    total_failures = 0
    
    # To optimize, we can group values by their occurrence, but since n is up to 10^5,
    # and we might have duplicates, we can just iterate over all nodes.
    # However, if there are many duplicate values, simulating search for each duplicate individually
    # might be O(N * N) in worst case (e.g., all values same, search goes down one path).
    # But the search path length is O(H) where H is height. Worst case H = N. So O(N^2).
    # N=10^5 -> 10^10 operations is too slow.
    # We need a smarter approach.
    
    # Observation: The search path for a value X starting at root is deterministic.
    # The path depends ONLY on X and the structure of the tree (values at nodes).
    # If multiple nodes have value X, the search result for X is the same for all of them.
    # So we only need to simulate the search for each UNIQUE value present in the tree.
    # Then, for each unique value, we count how many nodes have that value.
    # If the search for value X returns False, we add count(X) to total_failures.
    # If it returns True, we add 0.
    
    # Step 1: Identify unique values and their frequencies.
    from collections import defaultdict
    value_counts = defaultdict(int)
    for i in range(n):
        value_counts[values[i]] += 1
    
    unique_values = list(value_counts.keys())
    
    # Step 2: For each unique value, simulate the search.
    for x in unique_values:
        current = root
        found = False
        while current != -1:
            if values[current] == x:
                found = True
                break
            if x < values[current]:
                current = left[current]
            else:
                current = right[current]
        
        if not found:
            total_failures += value_counts[x]
    
    print(total_failures)

if __name__ == '__main__':
    solve()