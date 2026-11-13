def unnecessary_cards():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:]))
    
    # Sort the array in descending order
    a.sort(reverse=True)
    
    # Calculate the prefix sum of the sorted array
    prefix_sum = [0] * (N + 1)
    for i in range(N):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]
    
    unnecessary_count = 0
    
    # Check each card
    for i in range(N):
        # If the sum of all cards except the current one is less than K,
        # then the current card is unnecessary
        if prefix_sum[N] - prefix_sum[i + 1] < K:
            unnecessary_count += 1
    
    print(unnecessary_count)