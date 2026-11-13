def duel(n, k, cards):
    # Calculate the number of moves required to make all color sides face up or down
    moves_to_uniform = 0
    current_state = cards[0]
    
    for i in range(n):
        if cards[i] != current_state:
            moves_to_uniform += 1
            current_state = cards[i]
    
    # Calculate the total number of moves
    total_moves = moves_to_uniform
    
    # Check if the total number of moves exceeds 10^9
    if total_moves > 10**9:
        return "once again"
    
    # Determine the winner based on the parity of total moves
    if total_moves % 2 == 0:
        return "quailty"
    else:
        return "tokitsukaze"

# Read input
n, k = map(int, input().split())
cards = input().strip()

# Call the function and print the result
print(duel(n, k, cards))