import sys

def construct_tree(n, d, k):
    if d % 2 == 0:
        if n < 2 * d // 2 + 1 or k < 3:
            return "NO"
    else:
        if n < d + 1 or k < 3:
            return "NO"
    
    if d % 2 == 0:
        half = d // 2
        edges = []
        for i in range(1, half + 1):
            edges.append((1, i))
            edges.append((1, i + half))
        for i in range(2, half + 1):
            edges.append((i, i + half))
        for i in range(half + 2, n + 1):
            edges.append((1, i))
    else:
        edges = []
        for i in range(2, d + 2):
            edges.append((1, i))
        for i in range(d + 3, n + 1):
            edges.append((1, i))
    
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