def max_profit_distribution(n, k, difficulties):
    # Initialize the profit and the distribution list
    max_profit = 0
    best_distribution = []
    
    # Helper function to calculate the profit for a given distribution
    def calculate_profit(distribution):
        profit = 0
        start = 0
        for segment in distribution:
            end = start + segment
            profit += max(difficulties[start:end])
            start = end
        return profit
    
    # Generate all possible distributions of n problems into k segments
    from itertools import combinations
    
    # We need to find k-1 split points in the list of n problems
    for splits in combinations(range(1, n), k-1):
        distribution = [splits[0]] + [splits[i] - splits[i-1] for i in range(1, k-1)] + [n - splits[-1]]
        current_profit = calculate_profit(distribution)
        if current_profit > max_profit:
            max_profit = current_profit
            best_distribution = distribution
    
    return max_profit, best_distribution

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
difficulties = list(map(int, data[2:]))

# Get the result
max_profit, best_distribution = max_profit_distribution(n, k, difficulties)

# Print the result
print(max_profit)
print(' '.join(map(str, best_distribution)))