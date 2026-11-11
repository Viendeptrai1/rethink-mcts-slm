import sys
from collections import Counter

def max_total_joy(n, k, cards, favorites, joys):
    # Count occurrences of each favorite number in the cards
    favorite_counts = Counter(cards)
    
    # Calculate the maximum possible joy for each player
    max_joy = 0
    for i in range(n):
        favorite = favorites[i]
        count = favorite_counts[favorite]
        # Find the best joy level we can get for this player
        for j in range(k, 0, -1):
            if count >= j:
                max_joy += joys[j-1]
                break
    
    return max_joy

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2 + k * n]))
favorites = list(map(int, data[2 + k * n:2 + k * n + n]))
joys = list(map(int, data[2 + k * n + n:]))

# Output the result
print(max_total_joy(n, k, cards, favorites, joys))