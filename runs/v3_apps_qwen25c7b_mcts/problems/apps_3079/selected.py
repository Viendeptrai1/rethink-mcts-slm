def solve_game(N, sequence):
    # Initialize pointers for the left and right parts of the sequence
    left = 0
    right = N - 1
    
    # Find the longest prefix that is lexicographically smaller than its corresponding suffix
    while left < right:
        if sequence[left] < sequence[right]:
            break
        elif sequence[left] > sequence[right]:
            return "NE", sequence[:right]
        left += 1
        right -= 1
    
    # If no such prefix exists, Slavko cannot win
    if left >= right:
        return "NE", sequence[0]
    
    # Slavko can win by focusing on maintaining the identified property
    return "DA", sequence[left:right+1]

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