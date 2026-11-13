def determine_winner(n, k, cards):
    count_ones = cards.count('1')
    
    if count_ones % 2 == 1:
        return "tokitsukaze"
    else:
        if n >= k:
            return "tokitsukaze"
        else:
            return "once again"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = data[2]

# Output result
print(determine_winner(n, k, cards))