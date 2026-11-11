import sys
from collections import Counter

def max_total_joy(n, k, cards, favorites, joys):
    # Count occurrences of each card number
    card_count = Counter(cards)
    
    # Sort cards by their frequency in descending order
    sorted_cards = sorted(card_count.items(), key=lambda x: x[1], reverse=True)
    
    # Initialize total joy level
    total_joy = 0
    
    # Process each player's favorite number
    for favorite in favorites:
        # Find the number of times the favorite card appears
        favorite_count = card_count[favorite]
        
        # Calculate the maximum joy level for this player
        joy_level = 0
        for i in range(k):
            if favorite_count > 0:
                joy_level += joys[i]
                favorite_count -= 1
        
        # Add the player's joy level to the total
        total_joy += joy_level
    
    return total_joy

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2 + k * n]))
favorites = list(map(int, data[2 + k * n:2 + k * n + n]))
joys = list(map(int, data[2 + k * n + n:]))

# Calculate and print the result
result = max_total_joy(n, k, cards, favorites, joys)
print(result)