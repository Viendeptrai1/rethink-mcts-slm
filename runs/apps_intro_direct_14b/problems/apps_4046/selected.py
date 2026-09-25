import sys

def restore_permutation(n, q):
    # Initialize the permutation with None
    p = [None] * n
    
    # Try to place the smallest possible number in the first position
    for start in range(1, n + 1):
        # Assume the permutation starts with 'start'
        p[0] = start
        valid = True
        
        # Fill the rest of the permutation based on the differences
        for i in range(1, n):
            p[i] = p[i - 1] + q[i - 1]
            # Check if the current value is within the valid range and not repeated
            if p[i] < 1 or p[i] > n or p[i] in p[:i]:
                valid = False
                break
        
        # If we found a valid permutation, return it
        if valid:
            return p
    
    # If no valid permutation was found, return -1
    return [-1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = list(map(int, data[1:]))
    
    result = restore_permutation(n, q)
    
    if result == [-1]:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()