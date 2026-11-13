def can_form_equal_teams(scores):
    from itertools import combinations

    # Generate all possible combinations of 3 participants
    all_combinations = list(combinations(scores, 3))
    
    # Check all pairs of combinations to see if they can form two teams with equal scores
    for i in range(len(all_combinations)):
        for j in range(i + 1, len(all_combinations)):
            team1 = all_combinations[i]
            team2 = all_combinations[j]
            
            # Calculate the scores of the two teams
            score1 = sum(team1)
            score2 = sum(team2)
            
            # Check if the scores are equal
            if score1 == score2:
                return "YES"
    
    return "NO"

# Read input
scores = list(map(int, input().split()))

# Output the result
print(can_form_equal_teams(scores))