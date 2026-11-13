def distribute_ratings(n, a):
    # Initialize a list to store the final ratings
    b = [0] * n
    # Use a set to keep track of used ratings
    used_ratings = set()
    
    # Iterate through each user's desired rating
    for i in range(n):
        # Start with the desired rating
        current_rating = a[i]
        
        # Adjust the rating if it has already been used
        while current_rating in used_ratings:
            current_rating += 1
        
        # Assign the unique rating to the user
        b[i] = current_rating
        # Mark the rating as used
        used_ratings.add(current_rating)
    
    return b

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse the number of users
n = int(data[0])
# Parse the desired ratings
a = list(map(int, data[1:]))

# Get the optimal distribution of ratings
result = distribute_ratings(n, a)

# Print the result
print(" ".join(map(str, result)))