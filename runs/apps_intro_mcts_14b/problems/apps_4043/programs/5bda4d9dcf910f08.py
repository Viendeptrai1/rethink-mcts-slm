import sys

def construct_tree(n, d, k):
    if d >= n - 1:
        return "NO"
    if k < 2:
        return "NO"
    
    # Create a path of length d
    edges = []
    for i in range(1, d + 1):
        edges.append((i, i + 1))
    
    # Attach remaining vertices
    remaining_vertices = n - (d + 1)
    current_vertex = d + 1
    
    # Try to attach remaining vertices to the path
    for _ in range(remaining_vertices):
        if len(edges) >= n - 1:
            break
        # Find a vertex with degree less than k
        for i in range(1, d + 2):
            if sum(1 for u, v in edges if u == i or v == i) < k:
                edges.append((i, current_vertex))
                current_vertex += 1
                break
        else:
            return "NO"
    
    if len(edges) < n - 1:
        return "NO"
    
    return "YES", edges

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    result = construct_tree(n, d, k)
    
    if result == "NO":
        print("NO")
    else:
        print("YES")
        for u, v in result[1]:
            print(u, v)

if __name__ == "__main__":
    main()