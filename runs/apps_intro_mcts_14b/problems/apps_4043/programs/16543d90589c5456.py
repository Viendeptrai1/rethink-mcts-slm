import sys

def construct_tree(n, d, k):
    if d == 1:
        if n > k:
            return "NO"
        else:
            return "YES\n" + "\n".join(f"{i} {i+1}" for i in range(1, n))
    
    if n < d + 1:
        return "NO"
    
    if k < 3:
        return "NO"
    
    # Create a linear chain of d+1 vertices
    edges = []
    for i in range(1, d):
        edges.append((i, i + 1))
    
    # Attach remaining vertices
    current_vertex = d + 1
    for i in range(d + 1, n + 1):
        edges.append((1, i))
        current_vertex += 1
    
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