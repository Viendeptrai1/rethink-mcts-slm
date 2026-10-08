import sys
from collections import defaultdict, Counter

def max_joy_level(n, k, cards, favorites, joys):
    # Count the occurrences of each favorite number in the cards
    favorite_count = defaultdict(int)
    for card in cards:
        favorite_count[card] += 1
    
    # Sort the favorites by their count in descending order
    sorted_favorites = sorted(favorites, key=lambda x: favorite_count[x], reverse=True)
    
    # Initialize the total joy level
    total_joy = 0
    
    # Assign cards to players
    for favorite in sorted_favorites:
        # Get the number of cards with this favorite number
        count = favorite_count[favorite]
        
        # Calculate the maximum number of players that can get at least one card with this favorite number
        max_players = min(count // k, n)
        
        # Assign cards to these players
        for i in range(max_players):
            # Calculate the joy level for this player
            joy = sum(joys[:min(k, count)])
            total_joy += joy
            
            # Decrease the count of cards with this favorite number
            count -= k
        
        # Decrease the number of players
        n -= max_players
    
    return total_joy

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2 + k * n]))
favorites = list(map(int, data[2 + k * n:2 + k * n + n]))
joys = list(map(int, data[2 + k * n + n:]))

# Calculate and print the maximum possible total joy level
print(max_joy_level(n, k, cards, favorites, joys))