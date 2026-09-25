import sys

def min_operations(a, b, c):
    # Initialize the result with a large number
    res = float('inf')
    best_A, best_B, best_C = a, b, c
    
    # Iterate over possible values for A
    for A in range(1, a + 1):
        # Iterate over possible values for B that are divisible by A
        for B in range(A, b + 1):
            if B % A == 0:
                # Calculate the target value for C that is divisible by B
                C = (c // B) * B
                if C >= B:
                    # Calculate the number of operations needed
                    operations = abs(A - a) + abs(B - b) + abs(C - c)
                    # Update the result if a better solution is found
                    if operations < res:
                        res = operations
                        best_A, best_B, best_C = A, B, C
                else:
                    # If C is less than B, try the next possible B
                    continue
    
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