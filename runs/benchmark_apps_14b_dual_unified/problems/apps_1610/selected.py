import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    
    permutation = []
    
    # Fill the first k+1 elements in decreasing order
    for i in range(k, -1, -1):
        permutation.append(i + 1)
    
    # Fill the remaining elements in increasing order starting from k+2
    for i in range(k + 2, n + 1):
        permutation.append(i)
    
    print(" ".join(map(str, permutation)))

if __name__ == "__main__":
    main()