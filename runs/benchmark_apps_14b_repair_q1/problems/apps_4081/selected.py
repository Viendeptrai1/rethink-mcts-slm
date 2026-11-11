import sys

def longest_increasing_subsequence(n, a):
    # Create a list of tuples (value, index)
    indexed_a = [(a[i], i) for i in range(n)]
    
    # Sort the list by value
    indexed_a.sort()
    
    # Initialize variables
    result = []
    moves = []
    
    # Use two pointers to track the leftmost and rightmost elements
    left = 0
    right = n - 1
    
    # Iterate through the sorted list
    for value, original_index in indexed_a:
        if original_index <= left:
            # Take from the left
            result.append(value)
            moves.append('L')
            left += 1
        elif original_index >= right:
            # Take from the right
            result.append(value)
            moves.append('R')
            right -= 1
    
    return len(result), ''.join(moves)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
k, s = longest_increasing_subsequence(n, a)

# Print the result
sys.stdout.write(f"{k}\n{s}\n")