def determine_winner(n, sequence):
    def nim_sum(sequence):
        return reduce(lambda x, y: x ^ y, sequence, 0)
    
    if n == 1:
        return "BitLGM" if sequence[0] > 0 else "BitAryo"
    
    if n == 2:
        return "BitLGM" if (sequence[0] > 0) and (sequence[1] > 0) else "BitAryo"
    
    if n == 3:
        if sequence[0] > 0 and sequence[1] > 0 and sequence[2] > 0:
            return "BitLGM" if nim_sum(sequence) > 0 else "BitAryo"
        else:
            return "BitAryo"

import sys
from functools import reduce

def main():
    input_data = sys.stdin.read().strip()
    n = int(input_data.split()[0])
    sequence = list(map(int, input_data.split()[1:n+1]))
    winner = determine_winner(n, sequence)
    print(winner)

if __name__ == "__main__":
    main()