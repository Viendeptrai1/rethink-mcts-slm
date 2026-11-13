def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    K = int(data[index])
    index += 1
    
    X = [0] * K
    for i in range(K):
        X[i] = int(data[index])
        index += 1
    
    Q = int(data[index])
    index += 1
    
    queries = []
    for i in range(Q):
        L = int(data[index])
        R = int(data[index + 1])
        queries.append((L, R))
        index += 2
    
    # Calculate the effect of each jump on the array
    # We use a list to keep track of the number of times each index is incremented
    increment_count = [0] * N
    
    for jump in X:
        for i in range(jump):
            current_index = i
            while current_index < N:
                increment_count[current_index] += 1
                current_index += jump
    
    # Calculate the prefix sum of the increment_count array
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i + 1] = prefix_sum[i] + increment_count[i]
    
    # Answer each query using the prefix sum
    results = []
    for L, R in queries:
        result = prefix_sum[R + 1] - prefix_sum[L]
        results.append(result)
    
    # Print the results
    for result in results:
        print(result)