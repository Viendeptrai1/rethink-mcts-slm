from collections import Counter

def max_joy_levels(n, k, cards, favorites, joy_levels):
    # Count the frequency of each card number
    card_count = Counter(cards)
    
    # Initialize the total joy level
    total_joy = 0
    
    # Iterate over each player's favorite number
    for favorite in favorites:
        # Count how many times the favorite number appears
        count_favorite = card_count[favorite]
        
        # Calculate the joy level for this player
        player_joy = min(count_favorite, k) * joy_levels[min(count_favorite, k)]
        
        # Add the player's joy level to the total
        total_joy += player_joy
        
        # Decrease the count of the favorite number by k
        card_count[favorite] -= k
    
    return total_joy

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2*n+2]))
favorites = list(map(int, data[2*n+2:3*n+2]))
joy_levels = list(map(int, data[3*n+2:]))

# Calculate and print the result
print(max_joy_levels(n, k, cards, favorites, joy_levels))