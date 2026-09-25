import sys

def min_operations(a, b, c):
    # Initialize the result with a large number
    res = float('inf')
    best_a, best_b, best_c = a, b, c
    
    # Iterate over possible values for A
    for A in range(1, a + 1):
        # Iterate over possible values for B that are multiples of A
        for B in range(A, b + 1, A):
            # Iterate over possible values for C that are multiples of B
            for C in range(B, c + 1, B):
                # Calculate the number of operations needed
                operations = (A - a) + (B - b) + (C - c)
                # Update the result if fewer operations are found
                if operations < res:
                    res = operations
                    best_a, best_b, best_c = A, B, C
    
    return res, best_a, best_b, best_c

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
        res, A, B, C = min_operations(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()