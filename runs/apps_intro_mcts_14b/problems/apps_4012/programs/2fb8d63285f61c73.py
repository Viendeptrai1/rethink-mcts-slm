import sys

def min_operations(a, b, c):
    # Initialize the result and the best triple
    res = float('inf')
    best_A, best_B, best_C = a, b, c
    
    # Iterate over possible values of A
    for A in range(1, b + 1):
        if b % A == 0:
            # Find the smallest multiple of B that is >= A
            B = (b // A) * A
            if B > c:
                continue
            # Find the smallest multiple of C that is >= B
            C = (c // B) * B
            if C < B:
                continue
            # Calculate the number of operations needed
            operations = (A - a) + (B - b) + (C - c)
            if operations < res:
                res = operations
                best_A, best_B, best_C = A, B, C
    
    return res, best_A, best_B, best_C

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