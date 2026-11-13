def can_form_equal_teams(scores):
    total_score = sum(scores)
    if total_score % 2 != 0:
        return "NO"
    
    target_score = total_score // 2
    from itertools import combinations
    
    for combo in combinations(scores, 3):
        if sum(combo) == target_score:
            return "YES"
    
    return "NO"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
scores = list(map(int, data))
print(can_form_equal_teams(scores))