import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    if k == 0:
        # If k is 0, we need an increasing permutation
        print(' '.join(map(str, range(1, n + 1))))
    elif k == n - 1:
        # If k is n-1, we need a decreasing permutation
        print(' '.join(map(str, range(n, 0, -1))))
    else:
        # Create a permutation with k decreasing elements
        result = list(range(1, n - k + 1)) + list(range(n, n - k - 1, -1))
        print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()