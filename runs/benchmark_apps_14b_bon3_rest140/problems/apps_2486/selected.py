def count_unnecessary_cards(N, K, cards):
    def is_good_subset(subset_sum):
        return subset_sum >= K

    unnecessary_count = 0

    for i in range(N):
        current_sum = sum(cards)
        if current_sum < K:
            break

        # Check if removing the i-th card makes the subset still good
        remaining_sum = current_sum - cards[i]
        if is_good_subset(remaining_sum):
            unnecessary_count += 1

    return unnecessary_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
cards = list(map(int, data[2:]))

# Calculate and print the result
result = count_unnecessary_cards(N, K, cards)
print(result)