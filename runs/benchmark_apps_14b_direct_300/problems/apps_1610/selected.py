import sys

def find_permutation(n, k):
    # Initialize the permutation array
    p = list(range(1, n + 1))
    
    # To achieve the decreasing coefficient k, we need to swap elements
    # such that there are exactly k positions where p[i] > p[i+1]
    for i in range(k):
        p[i], p[i + 1] = p[i + 1], p[i]
    
    return p

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    
    result = find_permutation(n, k)
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()