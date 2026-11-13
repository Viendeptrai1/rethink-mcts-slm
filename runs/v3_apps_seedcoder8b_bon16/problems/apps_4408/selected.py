def maximize_joy_levels(n, k, cards, favorite_numbers, joy_levels):
    from itertools import permutations

    # Calculate the joy level for a single player based on their cards
    def player_joy(player_fav, player_cards):
        count = player_cards.count(player_fav)
        return joy_levels[count - 1] if count > 0 else 0

    # Initialize the maximum total joy
    max_joy = 0

    # Generate all permutations of the cards
    card_permutations = permutations(cards)

    # Iterate over all permutations
    for perm in card_permutations:
        total_joy = 0
        # Assign permuted cards to players
        for i in range(n):
            player_cards = perm[i * k:(i + 1) * k]
            total_joy += player_joy(favorite_numbers[i], player_cards)
        max_joy = max(max_joy, total_joy)

    return max_joy

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:2 + k * n]))
favorite_numbers = list(map(int, data[2 + k * n:2 + k * n + n]))
joy_levels = list(map(int, data[2 + k * n + n:2 + k * n + n + k]))

# Calculate and print the result
print(maximize_joy_levels(n, k, cards, favorite_numbers, joy_levels))