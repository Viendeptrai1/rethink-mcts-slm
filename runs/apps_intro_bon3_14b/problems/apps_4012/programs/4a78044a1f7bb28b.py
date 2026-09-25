import sys

def min_operations(a, b, c):
    # Function to find the minimum operations to make b divisible by a and c divisible by b
    def find_operations(x, y, z):
        ops = 0
        if x > y:
            ops += x - y
            y = x
        if y > z:
            ops += y - z
            z = y
        if x > y:
            ops += x - y
            y = x
        return ops, x, y, z

    # Try different combinations of a, b, c
    ops1, a1, b1, c1 = find_operations(a, b, c)
    ops2, a2, b2, c2 = find_operations(b, a, c)
    ops3, a3, b3, c3 = find_operations(c, b, a)
    
    # Find the best combination
    min_ops = min(ops1, ops2, ops3)
    if min_ops == ops1:
        return min_ops, a1, b1, c1
    elif min_ops == ops2:
        return min_ops, a2, b2, c2
    else:
        return min_ops, a3, b3, c3

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        index += 3
        res, A, B, C = min_operations(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()