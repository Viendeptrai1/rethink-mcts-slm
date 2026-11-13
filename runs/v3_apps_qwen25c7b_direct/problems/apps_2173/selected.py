def distribute_ratings(n, a):
    # Sort the array to facilitate the smallest possible sum while ensuring distinct ratings
    a.sort()
    
    # Initialize the result list
    b = []
    
    # Use a set to keep track of used ratings
    used_ratings = set()
    
    # Iterate through the sorted array
    for ai in a:
        # Start checking from the smallest possible rating greater than or equal to ai
        rating = ai
        while rating in used_ratings:
            rating += 1
        
        # Assign this rating to the current user
        b.append(rating)
        
        # Mark this rating as used
        used_ratings.add(rating)
    
    return b

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
a = list(map(int, data[1:]))

# Distribute ratings
result = distribute_ratings(n, a)

# Print result
print(' '.join(map(str, result)))