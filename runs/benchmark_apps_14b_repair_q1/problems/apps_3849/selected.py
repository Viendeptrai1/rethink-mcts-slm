def determine_winner(n, k, cards):
    if k == 1:
        return "once again"
    
    if n % k == 0:
        return "tokitsukaze"
    else:
        return "quailty"

# Read input
n, k = map(int, input().split())
cards = input().strip()

# Determine and print the winner
print(determine_winner(n, k, cards))