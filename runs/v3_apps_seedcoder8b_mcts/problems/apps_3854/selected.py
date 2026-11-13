def find_arya_sums(n, k, coins):
    # Initialize a set to store all possible sums that can be made with the subset of coins
    possible_sums = set()
    
    # Initialize a list to store the current subset of coins
    current_subset = []
    
    # Helper function to perform backtracking
    def backtrack(start, current_sum):
        # If the current sum is equal to k, add all possible sums of the current subset to the set
        if current_sum == k:
            for i in range(len(current_subset) + 1):
                for subset in combinations(current_subset, i):
                    possible_sums.add(sum(subset))
            return
        
        # Iterate over the remaining coins
        for i in range(start, n):
            # Include the current coin in the subset
            current_subset.append(coins[i])
            # Recursively call backtrack with the updated sum and next index
            backtrack(i + 1, current_sum + coins[i])
            # Exclude the current coin from the subset (backtrack)
            current_subset.pop()
    
    # Import combinations from itertools
    from itertools import combinations
    
    # Start backtracking from the first coin with an initial sum of 0
    backtrack(0, 0)
    
    # Convert the set to a sorted list and return it
    return sorted(possible_sums)

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
k = int(data[1])
coins = list(map(int, data[2:2 + n]))

# Find and print the result
result = find_arya_sums(n, k, coins)
print(len(result))
print(" ".join(map(str, result)))