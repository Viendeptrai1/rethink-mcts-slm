def min_rolls_to_get_points(t, queries):
    dice_faces = [2, 3, 4, 5, 6, 7]
    results = []
    
    for x in queries:
        # Start with the maximum possible rolls, which is x (rolling a 2 each time)
        min_rolls = x
        
        # Try to reduce the number of rolls by using larger dice faces
        for face in sorted(dice_faces, reverse=True):
            if x >= face:
                rolls = x // face
                remaining = x % face
                if remaining == 0:
                    min_rolls = min(min_rolls, rolls)
                else:
                    # Try to fit the remaining points with smaller dice faces
                    additional_rolls = min_rolls_to_get_points(1, [remaining])[0]
                    min_rolls = min(min_rolls, rolls + additional_rolls)
        
        results.append(min_rolls)
    
    return results

# Read input
t = int(input())
queries = [int(input()) for _ in range(t)]

# Solve and print output
results = min_rolls_to_get_points(t, queries)
for result in results:
    print(result)