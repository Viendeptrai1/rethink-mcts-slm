def determine_winner(n, sequence):
    # Calculate the nim-sum of the sequence
    nim_sum = 0
    for number in sequence:
        nim_sum ^= number
    
    # Determine the winner based on the nim-sum
    if nim_sum == 0:
        return "BitAryo"
    else:
        return "BitLGM"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = list(map(int, data[1:n+1]))
    
    winner = determine_winner(n, sequence)
    print(winner)

if __name__ == "__main__":
    main()