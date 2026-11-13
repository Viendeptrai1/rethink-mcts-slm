def min_absolute_difference():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    weights = list(map(int, data[1:]))
    
    min_diff = float('inf')
    
    # Calculate the total sum of all weights
    total_sum = sum(weights)
    
    # Iterate over possible T values
    for T in range(1, N):
        # Calculate the sum of the first group
        S_1 = sum(weights[:T])
        # Calculate the sum of the second group
        S_2 = total_sum - S_1
        # Calculate the absolute difference
        diff = abs(S_1 - S_2)
        # Update the minimum difference found
        if diff < min_diff:
            min_diff = diff
    
    print(min_diff)