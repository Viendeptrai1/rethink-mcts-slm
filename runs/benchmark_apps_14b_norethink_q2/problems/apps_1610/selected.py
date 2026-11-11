import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    # Start with the identity permutation
    permutation = list(range(1, n + 1))
    
    # Swap elements to create decreasing pairs
    for i in range(k):
        permutation[i], permutation[i + 1] = permutation[i + 1], permutation[i]
    
    # Print the resulting permutation
    print(" ".join(map(str, permutation)))

if __name__ == "__main__":
    main()