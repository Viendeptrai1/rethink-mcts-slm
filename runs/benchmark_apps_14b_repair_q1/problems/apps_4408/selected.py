import sys
from collections import Counter

def max_total_joy(n, k, cards, favorites, joys):
    # Count the occurrences of each favorite number in the cards
    favorite_counts = Counter(cards)
    
    # Calculate the maximum possible joy for each player
    max_joy = 0
    for i in range(n):
        favorite = favorites[i]
        count = favorite_counts[favorite]
        # Find the maximum joy level we can get for this player
        max_joy_for_player = 0
        for j in range(k, 0, -1):
            if count >= j:
                max_joy_for_player = joys[j-1]
                break
        max_joy += max_joy_for_player
    
    return max_joy

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2+n*k]))
favorites = list(map(int, data[2+n*k:2+n*k+n]))
joys = list(map(int, data[2+n*k+n:2+n*k+n+k]))

# Calculate and print the result
result = max_total_joy(n, k, cards, favorites, joys)
print(result)