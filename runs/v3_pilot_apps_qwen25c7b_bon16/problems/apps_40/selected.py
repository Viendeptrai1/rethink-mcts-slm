def check_round_type(n, ratings):
    # Check if any rating has changed
    any_changed = any(before != after for before, after in ratings)
    
    # Check if there is any change in ranking while rating stays the same
    sorted_ratings = sorted(ratings, key=lambda x: (-x[1], x[0]))
    is_rated = any(ratings[i][1] != sorted_ratings[i][1] for i in range(n))
    
    if any_changed:
        return "rated"
    elif is_rated:
        return "unrated"
    else:
        return "maybe"

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
ratings = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
result = check_round_type(n, ratings)
print(result)