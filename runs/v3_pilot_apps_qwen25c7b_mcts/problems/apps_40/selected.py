def determine_round_status(n, standings):
    # Check if any rating has changed
    ratings_changed = any(a != b for a, b in standings)
    
    # Check if the standings are sorted in decreasing order of ratings
    sorted_by_rating = all(standings[i][0] >= standings[i + 1][0] for i in range(n - 1))
    
    # Check if the standings are sorted in increasing order of indices
    sorted_by_index = all(i == j for i, (_, _) in enumerate(standings) for j, (_, _) in enumerate(sorted(standings)))
    
    if ratings_changed:
        return "rated"
    elif sorted_by_rating and sorted_by_index:
        return "unrated"
    else:
        return "maybe"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
standings = [(int(data[2 * i + 1]), int(data[2 * i + 2])) for i in range(n)]

# Output the result
print(determine_round_status(n, standings))