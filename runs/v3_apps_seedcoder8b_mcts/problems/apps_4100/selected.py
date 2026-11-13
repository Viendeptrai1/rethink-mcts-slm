def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    Q = int(data[2])
    A = list(map(int, data[3:3+Q]))
    
    # Initialize scores for each player
    scores = [K] * N
    
    # Process each correct answer
    for answer in A:
        # Player who answered correctly loses 1 point
        scores[answer - 1] -= 1
        # Other players gain 1 point
        for i in range(N):
            if i != answer - 1:
                scores[i] += 1
    
    # Determine survivors
    survivors = ['No'] * N
    for i in range(N):
        if scores[i] > 0:
            survivors[i] = 'Yes'
    
    # Print results
    for result in survivors:
        print(result)

if __name__ == "__main__":
    main()