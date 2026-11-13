def can_form_equal_teams(scores):
    total_score = sum(scores)
    if total_score % 2 != 0:
        return "NO"
    
    target_score = total_score // 2
    
    def dfs(start, current_sum, count):
        if count == 3 and current_sum == target_score:
            return True
        if count == 3 or start >= len(scores) or current_sum > target_score:
            return False
        
        # Choose the current student
        choose_current = dfs(start + 1, current_sum + scores[start], count + 1)
        
        # Skip the current student
        skip_current = dfs(start + 1, current_sum, count)
        
        return choose_current or skip_current
    
    scores.sort(reverse=True)
    return "YES" if dfs(0, 0, 0) else "NO"

# Read input
import sys
input = sys.stdin.read
data = list(map(int, input().split()))

# Call the function and print the result
print(can_form_equal_teams(data))