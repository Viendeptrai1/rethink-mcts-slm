def orient_edges(n, m, edges):
    # Check if the graph is a tree
    if m != n - 1:
        return "NO"
    
    # Choose a root node (node 1)
    root = 1
    
    # Create a dictionary to store the direction of each edge
    directions = {}
    
    # Direct all edges away from the root
    for u, v in edges:
        if u == root:
            directions[(u, v)] = '0'
        elif v == root:
            directions[(u, v)] = '1'
        else:
            return "NO"
    
    # Return the result
    return "YES\n" + ''.join(directions.values())

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    edges = [(int(data[2 + 2 * i]) - 1, int(data[3 + 2 * i]) - 1) for i in range(m)]
    
    result = orient_edges(n, m, edges)
    print(result)