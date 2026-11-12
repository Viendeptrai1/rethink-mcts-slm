def check_rating_status(n, standings):
    # Check if any rating has changed
    rating_changed = any(a != b for a, b in standings)
    
    # Check if the standings are in non-increasing order of ratings
    sorted_ratings = sorted(standings, key=lambda x: x[1], reverse=True)
    standings_sorted = sorted(standings, key=lambda x: x[1])
    
    # Determine if the standings are consistent with an unrated round
    unrated_possible = all(sorted_ratings[i][1] == standings_sorted[i][1] for i in range(n))
    
    if rating_changed:
        return "rated"
    elif unrated_possible:
        return "unrated"
    else:
        return "maybe"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
standings = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]

# Output the result
print(check_rating_status(n, standings))