def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    edges = []
    index = 2
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        edges.append((u, v))
        index += 2
    
    # Check if the graph is a tree
    if m != n - 1:
        print("NO")
        return
    
    # Since the graph is a tree, we can orient it in a way that no path of length 2 exists
    # A simple way to do this is to orient all edges in one direction (e.g., u -> v)
    # and then output a binary string of 0s.
    
    print("YES")
    print("0" * m)