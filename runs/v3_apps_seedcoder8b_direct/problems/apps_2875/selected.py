def find_reverse_subsequence(n, cards):
    # Step 1: Find the first part that is sorted
    start = 0
    while start < n - 1 and cards[start] <= cards[start + 1]:
        start += 1

    # If the entire array is already sorted
    if start == n - 1:
        print("impossible")
        return

    # Step 2: Find the last part that is sorted
    end = n - 1
    while end > 0 and cards[end] >= cards[end - 1]:
        end -= 1

    # Step 3: Reverse the identified subarray
    cards[start:end + 1] = reversed(cards[start:end + 1])

    # Step 4: Check if the entire array is now sorted
    if cards == sorted(cards):
        print(start + 1, end + 1)
    else:
        print("impossible")

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
cards = list(map(int, data[1:n + 1]))

find_reverse_subsequence(n, cards)