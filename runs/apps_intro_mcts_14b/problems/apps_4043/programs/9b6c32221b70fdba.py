import sys

def construct_tree(n, d, k):
    if d % 2 == 0:
        if n < d + 1 or k < 3:
            return "NO"
    else:
        if n < 2 * d or k < 3:
            return "NO"
    
    edges = []
    
    if d % 2 == 0:
        # Construct a tree with even diameter
        center = d // 2 + 1
        for i in range(1, center):
            edges.append((center, i))
        for i in range(center + 1, d + 2):
            edges.append((center, i))
        for i in range(d + 3, n + 1):
            edges.append((edges[-1][1], i))
    else:
        # Construct a tree with odd diameter
        left_center = d // 2 + 1
        right_center = d // 2 + 2
        for i in range(1, left_center):
            edges.append((left_center, i))
        for i in range(right_center + 1, d + 3):
            edges.append((right_center, i))
        edges.append((left_center, right_center))
        for i in range(d + 4, n + 1):
            edges.append((edges[-1][1], i))
    
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