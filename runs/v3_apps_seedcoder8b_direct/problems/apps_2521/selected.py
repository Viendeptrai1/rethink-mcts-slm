def max_score():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    # Calculate prefix sums for the first 3N elements
    prefix_sum = [0] * (3 * N + 1)
    for i in range(1, 3 * N + 1):
        prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    
    # Initialize the maximum score
    max_score = float('-inf')
    
    # Try removing N elements such that the first half and second half are contiguous
    for i in range(N + 1):
        for j in range(i + N, 2 * N + 1):
            # Calculate the sum of the first half and the second half
            first_half_sum = prefix_sum[i + N] - prefix_sum[i]
            second_half_sum = prefix_sum[2 * N] - prefix_sum[j]
            # Calculate the score
            score = first_half_sum - second_half_sum
            # Update the maximum score
            max_score = max(max_score, score)
    
    print(max_score)