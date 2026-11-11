import sys
from collections import Counter

def max_total_joy(n, k, cards, favorites, joys):
    # Count the occurrences of each favorite number in the cards
    favorite_counts = Counter(cards)
    
    # Calculate the maximum possible joy for each player
    max_joy = 0
    for favorite in favorites:
        count = favorite_counts[favorite]
        # Determine the best way to distribute the cards to maximize joy
        joy = 0
        for t in range(k, 0, -1):
            if count >= t:
                joy += joys[t-1]
                count -= t
        max_joy += joy
    
    return max_joy

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2 + n * k]))
favorites = list(map(int, data[2 + n * k:2 + n * k + n]))
joys = list(map(int, data[2 + n * k + n:]))

# Calculate and print the result
result = max_total_joy(n, k, cards, favorites, joys)
print(result)