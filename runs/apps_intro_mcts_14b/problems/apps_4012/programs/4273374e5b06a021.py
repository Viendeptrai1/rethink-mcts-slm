import sys

def solve(a, b, c):
    # Initialize the result to a large number
    res = float('inf')
    best_A, best_B, best_C = a, b, c
    
    # Iterate over possible values of A
    for A in range(1, b + 1):
        if b % A == 0:
            # Find the smallest B that is a multiple of A and >= b
            B = b
            # Find the smallest C that is a multiple of B and >= c
            C = c
            if C % B != 0:
                C += B - C % B
            
            # Calculate the number of operations needed
            operations = (B - b) + (C - c)
            
            # Update the result if this is a better solution
            if operations < res:
                res = operations
                best_A, best_B, best_C = A, B, C
    
    return res, best_A, best_B, best_C

def main():
    import sys
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
        res, A, B, C = solve(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()