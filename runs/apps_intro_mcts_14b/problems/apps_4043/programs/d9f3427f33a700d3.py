import sys

def construct_tree(n, d, k):
    if d < 2 or d > n - 1:
        return "NO"
    if k < 2 or k > n - 1:
        return "NO"
    if n == 1:
        return "YES\n"
    if d == 1:
        if n > 2:
            return "NO"
        else:
            return "YES\n1 2"
    
    # Check if it's possible to construct the tree
    if d * k < n - 1:
        return "NO"
    
    # Construct the tree
    edges = []
    # Create a path of length d
    for i in range(1, d):
        edges.append((i, i + 1))
    
    # Attach remaining vertices
    remaining_vertices = n - d
    current_vertex = 1
    while remaining_vertices > 0:
        for _ in range(min(k - 2, remaining_vertices)):
            edges.append((current_vertex, n - remaining_vertices + 1))
            remaining_vertices -= 1
        current_vertex += 1
    
    return "YES\n" + "\n".join(f"{u} {v}" for u, v in edges)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
d = int(data[1])
k = int(data[2])

# Output result
result = construct_tree(n, d, k)
print(result)