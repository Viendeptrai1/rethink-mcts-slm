def max_juice_drunk(n, actions):
    # Initialize the count of juice glasses drunk by Vasya
    juice_count = 0
    
    # Iterate over each turn in the game
    for i in range(len(actions)):
        # Check if the current turn is at least the 4th turn
        if i >= 3:
            # Check if the last three moves were the same as the current move
            if actions[i] == actions[i-1] == actions[i-2] == actions[i-3]:
                # Vasya drinks a glass of juice
                juice_count += 1
                # Skip the next move as Vasya would have skipped it
                i += 1
    
    return juice_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
actions = data[1]

# Calculate and print the result
print(max_juice_drunk(n, actions))