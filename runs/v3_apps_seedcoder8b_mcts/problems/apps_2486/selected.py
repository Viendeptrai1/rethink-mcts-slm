def count_unnecessary_cards():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    K = int(data[1])
    a = list(map(int, data[2:]))
    
    # Calculate the total sum of all cards
    total_sum = sum(a)
    
    # Sort the cards in descending order
    a.sort(reverse=True)
    
    # Initialize a set to keep track of achievable sums
    achievable_sums = {0}
    
    # Iterate over each card
    for card in a:
        # Update the set of achievable sums
        new_sums = set()
        for s in achievable_sums:
            new_sums.add(s + card)
        achievable_sums.update(new_sums)
    
    # Count unnecessary cards
    unnecessary_count = 0
    for i in range(N):
        # Check if removing the i-th card makes any subset sum less than K
        if total_sum - a[i] < K:
            unnecessary_count += 1
    
    # Print the result
    print(unnecessary_count)