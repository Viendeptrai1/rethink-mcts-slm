def distribute_ratings(n, a):
    # Create a list to store the result
    b = [0] * n
    
    # Initialize a set to keep track of used ratings
    used_ratings = set()
    
    # Iterate over each user's requirement
    for i in range(n):
        # Start with the user's requirement
        current_rating = a[i]
        
        # Increment the rating until it is unique
        while current_rating in used_ratings:
            current_rating += 1
        
        # Assign the unique rating to the user
        b[i] = current_rating
        
        # Add the assigned rating to the set of used ratings
        used_ratings.add(current_rating)
    
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