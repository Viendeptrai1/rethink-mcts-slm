def solve_game(N, sequence):
    # Since Mirko always takes the rightmost letter, we need to consider the sequence in reverse
    reversed_sequence = sequence[::-1]
    
    # Slavko will take the leftmost letter each time, so we need to find the lexicographically smallest prefix
    min_prefix = ""
    for i in range(len(reversed_sequence)):
        if not min_prefix or reversed_sequence[i] <= min_prefix[0]:
            min_prefix += reversed_sequence[i]
        else:
            break
    
    # If the length of the minimum prefix is less than half of N, Slavko cannot win
    if len(min_prefix) < N // 2:
        return "NE", min_prefix[::-1]
    else:
        return "DA", min_prefix[::-1]

# Read input
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
sequence = data[1]

# Solve the problem
result, word = solve_game(N, sequence)

# Print the result
print(result)
print(word)