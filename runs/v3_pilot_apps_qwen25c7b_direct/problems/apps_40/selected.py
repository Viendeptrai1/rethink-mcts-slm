def check_round_status(n, ratings):
    sorted_ratings = sorted(ratings, key=lambda x: (-x[1], x[0]))
    original_positions = {rating[0]: i for i, rating in enumerate(ratings)}
    new_positions = {sorted_rating[0]: i for i, sorted_rating in enumerate(sorted_ratings)}

    if len(set(new_positions.values())) == n:
        return "rated"
    
    if all(original_positions[rating[0]] <= new_positions[rating[0]] for rating in ratings):
        return "unrated"

    return "maybe"

# Input reading
n = int(input())
ratings = [tuple(map(int, input().split())) for _ in range(n)]

# Output result
print(check_round_status(n, ratings))