def game_outcome(sequence):
    mirko_word = ""
    slavko_word = ""
    
    # Simulate the game
    while sequence:
        # Mirko's turn: pick the rightmost letter
        mirko_word += sequence[-1]
        sequence = sequence[:-1]
        
        # Check if there are any letters left for Slavko
        if sequence:
            # Slavko's turn: pick the rightmost letter
            slavko_word += sequence[-1]
            sequence = sequence[:-1]
    
    # Determine the winner
    if slavko_word < mirko_word:
        return "DA", slavko_word
    else:
        return "NE", slavko_word

# Read input
N = int(input().strip())
sequence = input().strip()

# Get the outcome
result, slavko_word = game_outcome(sequence)

# Print the result
print(result)
print(slavko_word)