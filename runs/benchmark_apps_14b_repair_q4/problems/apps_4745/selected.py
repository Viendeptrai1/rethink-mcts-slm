def max_items_without_horn(n, X, prices):
    # Sort the prices in ascending order
    prices.sort()
    
    # Initialize two pointers
    left = 0
    right = n - 1
    
    # Count the number of items that cannot be included in the offer
    non_participating = 0
    
    # Use two-pointer technique to find pairs
    while left < right:
        if prices[left] + prices[right] > X:
            # If the sum of the pair is greater than X, move the right pointer inward
            non_participating += 1
            right -= 1
        else:
            # If the sum is less than or equal to X, move the left pointer inward
            left += 1
    
    # Calculate the maximum number of items that can be marked as participating
    participating = n - non_participating
    
    return participating

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
X = int(data[1])
prices = list(map(int, data[2:]))

# Print the result
print(max_items_without_horn(n, X, prices))