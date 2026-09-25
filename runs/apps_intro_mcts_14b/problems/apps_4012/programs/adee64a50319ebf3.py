import sys

def min_operations(a, b, c):
    # Initialize the result to a large number
    res = float('inf')
    best_A, best_B, best_C = a, b, c
    
    # Iterate over possible values for A
    for A in range(1, b + 1):
        if b % A == 0:
            # Calculate the minimum B that is divisible by A and greater than or equal to b
            B = b // A * A
            if B < b:
                B += A
            # Calculate the minimum C that is divisible by B and greater than or equal to c
            C = c // B * B
            if C < c:
                C += B
            # Calculate the number of operations needed
            operations = (B - b) + (C - c)
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
        res, A, B, C = min_operations(a, b, c)
        results.append((res, A, B, C))
    
    for res, A, B, C in results:
        print(res)
        print(A, B, C)

if __name__ == "__main__":
    main()