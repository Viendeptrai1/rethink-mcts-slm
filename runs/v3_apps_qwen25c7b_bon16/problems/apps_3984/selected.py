def determine_winner(s):
    n = len(s)
    result = []

    for k in range(n):
        if s[k] == 'a':
            result.append('Mike')
        else:
            result.append('Ann')

    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Process each test case
s = data[0]

# Determine the winners
winners = determine_winner(s)

# Print results
for winner in winners:
    print(winner)