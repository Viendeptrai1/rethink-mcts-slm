def slavko_wins(N, sequence):
    # Initialize variables
    slavko_word = []
    turn = 0  # 0 for Mirko, 1 for Slavko
    
    # Convert sequence to a list for easy manipulation
    letters = list(sequence)
    
    # Simulate the game
    while letters:
        if turn == 1:  # Slavko's turn
            # Slavko always takes the rightmost letter
            slavko_word.append(letters.pop())
        turn = 1 - turn  # Switch turns
    
    # Sort Slavko's word to find the most beautiful one
    slavko_word.sort()
    
    # Check if Slavko can win
    # Mirko's word will be the remaining letters sorted alphabetically
    mirko_word = sorted(letters)
    
    if slavko_word > mirko_word:
        return "DA", ''.join(slavko_word)
    else:
        return "NE", ''.join(slavko_word)


def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    sequence = data[1]
    
    result, slavko_word = slavko_wins(N, sequence)
    print(result)
    print(slavko_word)

if __name__ == "__main__":
    main()