import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    K = int(data[index + 1])
    jumps = [int(data[index + 2 + i]) for i in range(K)]
    Q = int(data[index + 2 + K])
    queries = [(int(data[index + 2 + K + 2 * i]), int(data[index + 2 + K + 2 * i + 1])) for i in range(Q)]
    
    # Initialize the array
    seq = [0] * N
    
    # Apply the jumps
    for jump in jumps:
        i = 0
        while i < N:
            seq[i] += 1
            i += jump
    
    # Calculate the results for each query
    results = []
    for L, R in queries:
        result = sum(seq[L:R + 1])
        results.append(result)
    
    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()