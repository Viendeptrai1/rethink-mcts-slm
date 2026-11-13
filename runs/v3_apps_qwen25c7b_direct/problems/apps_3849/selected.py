def determine_winner(n, k, cards):
    count_ones = cards.count('1')
    
    if count_ones % 2 == 0:
        return "tokitsukaze"
    else:
        if k == 1:
            return "once again"
        else:
            return "quailty"

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
cards = data[2]

# Determine and print the winner
print(determine_winner(n, k, cards))