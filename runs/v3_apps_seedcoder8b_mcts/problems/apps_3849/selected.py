def duel(n, k, cards):
    # Count the number of segments where the color side changes direction
    segments = 1
    for i in range(1, n):
        if cards[i] != cards[i - 1]:
            segments += 1

    # Calculate the total number of moves required
    total_moves = (segments + 1) // 2

    # Check if the total number of moves exceeds 10^9
    if total_moves > 10**9:
        return "once again"

    # Determine the winner based on the parity of total_moves
    if total_moves % 2 == 1:
        return "tokitsukaze"
    else:
        return "quailty"

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
cards = data[2]

# Output the result
print(duel(n, k, cards))