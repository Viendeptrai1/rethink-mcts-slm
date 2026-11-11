def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    
    # Initialize scores
    scores = [K] * N
    
    # Process each correct answer
    index = 3
    for _ in range(Q):
        A_i = int(data[index]) - 1  # Convert to zero-based index
        for j in range(N):
            if j != A_i:
                scores[j] -= 1
        index += 1
    
    # Determine survivors
    results = []
    for score in scores:
        if score > 0:
            results.append("Yes")
        else:
            results.append("No")
    
    # Print results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()