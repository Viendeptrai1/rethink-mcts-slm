def solve_dice_rolls(t, queries):
    # Define the possible outcomes of the dice
    dice_faces = [2, 3, 4, 5, 6, 7]
    
    # Function to determine the minimum number of rolls needed to achieve exactly x points
    def min_rolls_to_target(x):
        # Check if x can be achieved with a single roll
        if x in dice_faces:
            return 1
        
        # Try to find the minimum number of rolls
        for rolls in range(2, x + 1):
            # Generate all possible sums with the current number of rolls
            possible_sums = set()
            for i in range(rolls):
                if i == 0:
                    possible_sums.update(dice_faces)
                else:
                    new_sums = set()
                    for s in possible_sums:
                        for face in dice_faces:
                            new_sums.add(s + face)
                    possible_sums = new_sums
            
            # Check if x is in the possible sums
            if x in possible_sums:
                return rolls
    
    # Process each query
    results = []
    for x in queries:
        results.append(min_rolls_to_target(x))
    
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
queries = list(map(int, data[1:]))

# Solve the problem
results = solve_dice_rolls(t, queries)

# Print the results
for result in results:
    print(result)