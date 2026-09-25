import sys

def construct_tree(n, d, k):
    if d == 1:
        if n > 1:
            return "NO"
        else:
            return "YES", []
    
    if d % 2 == 0:
        if k < 3:
            return "NO"
        half_d = d // 2
        edges = []
        for i in range(1, half_d + 1):
            edges.append((1, i + 1))
        for i in range(half_d + 1, d + 1):
            edges.append((1, n - (i - half_d)))
        return "YES", edges
    
    if d % 2 == 1:
        if k < 4:
            return "NO"
        half_d = d // 2
        edges = []
        for i in range(1, half_d + 1):
            edges.append((1, i + 1))
        for i in range(half_d + 1, d + 1):
            edges.append((1, n - (i - half_d)))
        edges.append((1, n))
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