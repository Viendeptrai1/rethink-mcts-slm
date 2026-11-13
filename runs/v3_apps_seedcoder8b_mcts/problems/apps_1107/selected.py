def max_juice_drunk(n, actions):
    # Initialize the count of juice glasses drunk by Vasya
    juice_count = 0
    
    # Iterate over each turn in the game
    for j in range(len(actions)):
        # Determine the current player's index
        current_player = j % n
        
        # Check if the current player is Vasya (index 0)
        if current_player == 0:
            # Check if the last 4 turns (if available) have the same action
            if j >= 3:
                if actions[j] == actions[j-1] == actions[j-2] == actions[j-3]:
                    # Vasya drinks a glass of juice
                    juice_count += 1
                    # Skip the next turn as Vasya would have moved
                    j += 1
    
    return juice_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
actions = data[1]

# Get the result and print it
result = max_juice_drunk(n, actions)
print(result)