def max_score():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    # Calculate prefix sums for the first and second halves
    prefix_sum_first_half = [0] * (3 * N + 1)
    prefix_sum_second_half = [0] * (3 * N + 1)
    
    for i in range(1, 3 * N + 1):
        prefix_sum_first_half[i] = prefix_sum_first_half[i - 1] + a[i - 1] if i <= N else prefix_sum_first_half[i - 1]
        prefix_sum_second_half[i] = prefix_sum_second_half[i - 1] + a[i - 1] if i > N else prefix_sum_second_half[i - 1]
    
    max_score = float('-inf')
    
    # Try removing each possible set of N elements from the second half
    for i in range(N + 1):
        for j in range(i, N + 1):
            # Calculate the score by removing elements from i to j in the second half
            score = (prefix_sum_first_half[N] - prefix_sum_first_half[0]) - (prefix_sum_second_half[3 * N] - prefix_sum_second_half[j] - prefix_sum_second_half[i])
            max_score = max(max_score, score)
    
    print(max_score)