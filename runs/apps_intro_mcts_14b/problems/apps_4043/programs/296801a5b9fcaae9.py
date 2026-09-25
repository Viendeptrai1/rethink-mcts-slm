import sys

def construct_tree(n, d, k):
    if d == 1:
        if n > 2:
            return "NO"
        else:
            return "YES\n1 2"
    
    if k < 2:
        return "NO"
    
    if d % 2 == 0:
        half_d = d // 2
        if n < 2 * half_d + 1:
            return "NO"
        
        # Construct the tree
        edges = []
        for i in range(1, half_d + 1):
            edges.append((1, i + 1))
            edges.append((1, n - half_d + i))
        
        for i in range(half_d + 1, n - half_d):
            edges.append((i, i + 1))
        
        return "YES\n" + "\n".join(f"{u} {v}" for u, v in edges)
    else:
        half_d = d // 2
        if n < 2 * half_d + 2:
            return "NO"
        
        # Construct the tree
        edges = []
        for i in range(1, half_d + 1):
            edges.append((1, i + 1))
            edges.append((1, n - half_d + i))
        
        for i in range(half_d + 1, n - half_d - 1):
            edges.append((i, i + 1))
        
        edges.append((n - half_d - 1, n))
        
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