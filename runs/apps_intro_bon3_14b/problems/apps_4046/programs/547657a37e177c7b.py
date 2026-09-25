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
    min_p = min(p)
    max_p = max(p)
    
    # If the permutation contains all numbers from 1 to n, it's valid
    if min_p == 1 and max_p == n and len(set(p)) == n:
        return p
    else:
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