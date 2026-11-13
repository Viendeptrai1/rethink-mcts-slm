def find_reversal_indices(cards):
    n = len(cards)
    left = -1
    right = -1
    min_val = float('inf')
    max_val = float('-inf')

    for i in range(1, n):
        if cards[i] < cards[i - 1]:
            if left == -1:
                left = i - 1
                min_val = cards[i]
            else:
                right = i
                max_val = max(max_val, cards[i])

    if left == -1 or right == -1:
        return "impossible"

    if left > 0 and cards[left - 1] > min_val:
        return "impossible"

    if right < n - 1 and cards[right + 1] < max_val:
        return "impossible"

    return f"{left + 1} {right + 1}"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
cards = list(map(int, data[1:]))

result = find_reversal_indices(cards)
print(result)