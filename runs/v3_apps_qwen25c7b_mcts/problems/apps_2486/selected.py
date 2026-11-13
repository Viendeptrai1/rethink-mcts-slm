import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
cards = list(map(int, data[2:]))

# Sort the cards in ascending order
cards.sort()

# Initialize variables
total_sum = sum(cards)
unnecessary_count = 0

# Iterate through the sorted cards
for i in range(N):
    # Calculate the sum if we exclude the current card
    remaining_sum = total_sum - cards[i]
    
    # Check if the remaining sum is still >= K
    if remaining_sum >= K:
        unnecessary_count += 1
    else:
        break

print(unnecessary_count)