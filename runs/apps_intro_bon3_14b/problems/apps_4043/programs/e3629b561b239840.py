import sys

def construct_tree(n, d, k):
    if d % 2 == 0:
        if n < d + 1 or k < 3:
            return "NO"
    else:
        if n < 2 * d or k < 3:
            return "NO"
    
    if d % 2 == 0:
        # Construct a tree with diameter d
        edges = []
        center = d // 2 + 1
        for i in range(1, d // 2 + 1):
            edges.append((center, i))
            edges.append((center, d // 2 + 1 + i))
        
        remaining_vertices = n - (d + 1)
        for i in range(d + 2, n + 1):
            edges.append((center, i))
            if len(edges) >= n - 1:
                break
        
        return "YES", edges
    else:
        # Construct a tree with diameter d
        edges = []
        center = d // 2 + 1
        for i in range(1, d // 2 + 1):
            edges.append((center, i))
            edges.append((center, d // 2 + 2 + i))
        
        remaining_vertices = n - (2 * d + 1)
        for i in range(d // 2 + 3, n + 1):
            edges.append((center, i))
            if len(edges) >= n - 1:
                break
        
        return "YES", edges

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    d = int(data[1])
    k = int(data[2])
    
    result, edges = construct_tree(n, d, k)
    print(result)
    if result == "YES":
        for u, v in edges:
            print(u, v)

if __name__ == "__main__":
    main()