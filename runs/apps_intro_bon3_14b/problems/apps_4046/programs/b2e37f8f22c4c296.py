import sys

def restore_permutation(n, q):
    # Initialize the permutation with None
    p = [None] * n
    
    # Start with the smallest possible value for p[0]
    p[0] = 1
    
    # Fill the permutation based on the differences q
    for i in range(1, n):
        p[i] = p[i-1] + q[i-1]
    
    # Check if the permutation is valid
    if min(p) != 1 or max(p) != n or len(set(p)) != n:
        return [-1]
    
    return p

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