import sys

def min_operations(a, b, c):
    # Try to find the best A, B, C such that B is divisible by A and C is divisible by B
    min_ops = float('inf')
    best_A, best_B, best_C = a, b, c
    
    for A in range(1, a + 1):
        for B in range(A, b + 1):
            if B % A == 0:
                for C in range(B, c + 1):
                    if C % B == 0:
                        ops = (A - a) + (B - b) + (C - c)
                        if ops < min_ops:
                            min_ops = ops
                            best_A, best_B, best_C = A, B, C
    
    return min_ops, best_A, best_B, best_C

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