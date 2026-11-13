def expected_maximum(m, n):
    # Initialize a list to store the expected maximum for each number of tosses
    expected = [0] * (n + 1)
    
    # For one toss, the expected maximum is the average of all possible outcomes
    expected[1] = sum(i for i in range(1, m + 1)) / m
    
    # Use dynamic programming to calculate the expected maximum for each number of tosses
    for toss in range(2, n + 1):
        # Calculate the expected maximum for the current number of tosses
        expected[toss] = expected[toss - 1] + (m - expected[toss - 1]) / m
    
    # Return the expected maximum for n tosses
    return expected[n]

# Read input
m, n = map(int, input().split())

# Calculate and print the result
result = expected_maximum(m, n)
print(f"{result:.12f}")