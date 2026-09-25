import sys

def solve(a, b, c):
    # Initialize the result to a large number
    res = float('inf')
    best_A, best_B, best_C = a, b, c
    
    # Iterate over possible values for B
    for B in range(b, c + 1):
        # Find the closest multiple of B that is >= a
        A = (a + B - 1) // B * B
        if A > c:
            continue
        # Find the closest multiple of B that is <= c
        C = B * (c // B)
        if C < a:
            continue
        # Calculate the number of operations needed
        operations = (A - a) + (b - B) + (C - c)
        # Update the result if this is a better solution
        if operations < res:
            res = operations
            best_A, best_B, best_C = A, B, C
    
    return res, best_A, best_B, best_C

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
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