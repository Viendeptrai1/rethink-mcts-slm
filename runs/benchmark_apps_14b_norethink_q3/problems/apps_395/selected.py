from itertools import combinations

def can_form_equal_teams(scores):
    total_sum = sum(scores)
    if total_sum % 2 != 0:
        return "NO"
    
    target = total_sum // 2
    n = len(scores)
    
    for combo in combinations(range(n), 3):
        if sum(scores[i] for i in combo) == target:
            remaining_scores = [scores[i] for i in range(n) if i not in combo]
            for other_combo in combinations(range(3), 3):
                if sum(remaining_scores[i] for i in other_combo) == target:
                    return "YES"
    
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()
scores = list(map(int, data))

# Output result
print(can_form_equal_teams(scores))