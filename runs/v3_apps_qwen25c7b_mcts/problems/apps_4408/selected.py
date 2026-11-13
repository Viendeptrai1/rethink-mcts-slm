import heapq
from collections import defaultdict

def max_joy_levels(n, k, cards, favorites, joy_levels):
    # Count the frequency of each card
    card_count = defaultdict(int)
    for card in cards:
        card_count[card] += 1
    
    # Create a min heap based on the negative count of cards
    card_heap = []
    for card, count in card_count.items():
        heapq.heappush(card_heap, (-count, card))
    
    # Sort the favorite numbers
    favorites.sort()
    
    # Initialize the total joy level
    total_joy = 0
    
    # Distribute the cards to maximize joy levels
    for i in range(n):
        player_fav = favorites[i]
        player_joy = 0
        
        for _ in range(k):
            if card_heap:
                count, card = heapq.heappop(card_heap)
                if card == player_fav:
                    player_joy += joy_levels[-(count // -1)]
        
        total_joy += player_joy
    
    return total_joy

# Read input
n, k = map(int, input().split())
cards = list(map(int, input().split()))
favorites = list(map(int, input().split()))
joy_levels = list(map(int, input().split()))

# Calculate and print the result
print(max_joy_levels(n, k, cards, favorites, joy_levels))