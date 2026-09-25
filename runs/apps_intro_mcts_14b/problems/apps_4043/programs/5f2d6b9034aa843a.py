import sys

def construct_tree(n, d, k):
    if d == 1:
        if n > 2:
            return "NO"
        else:
            return "YES\n1 2"
    
    if d == 2:
        if n > 3:
            return "NO"
        else:
            return "YES\n1 2\n2 3"
    
    if k < 3:
        return "NO"
    
    if d >= n - 1:
        return "NO"
    
    # Construct the main path of length d
    edges = []
    for i in range(1, d + 1):
        edges.append((i, i + 1))
    
    # Attach the remaining vertices to the path
    remaining_vertices = n - d - 1
    current_vertex = 1
    for _ in range(remaining_vertices):
        edges.append((current_vertex, d + 2))
        current_vertex += 1
        if current_vertex > d:
            current_vertex = 1
    
    return "YES\n" + "\n".join(f"{u} {v}" for u, v in edges)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    result = construct_tree(n, d, k)
    print(result)

if __name__ == "__main__":
    main()