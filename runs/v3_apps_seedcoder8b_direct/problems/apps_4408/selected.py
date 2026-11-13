def max_joy_levels(n, k, cards, favorites, joy_levels):
    from itertools import permutations

    # Calculate the joy level for a single player
    def calculate_joy(fav_number, player_cards, joy_levels):
        count_fav = player_cards.count(fav_number)
        return joy_levels[count_fav - 1] if count_fav > 0 else 0

    # Generate all possible distributions of cards to players
    max_joy = 0
    for perm in permutations(cards, n * k):
        total_joy = 0
        for i in range(n):
            player_cards = perm[i * k:(i + 1) * k]
            total_joy += calculate_joy(favorites[i], player_cards, joy_levels)
        max_joy = max(max_joy, total_joy)

    return max_joy

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = list(map(int, data[2:n * k + 2]))
favorites = list(map(int, data[n * k + 2:n * k + 2 + n]))
joy_levels = list(map(int, data[n * k + 2 + n:]))

# Output the result
print(max_joy_levels(n, k, cards, favorites, joy_levels))