import sys

def can_form_equal_teams(scores):
    total_score = sum(scores)
    if total_score % 2 != 0:
        return "NO"
    
    target_score = total_score // 2
    
    def find_teams(index, current_score, count):
        if count == 2:
            return current_score == target_score
        if index == 6 or current_score > target_score:
            return False
        
        # Include the current student in a team
        include_current = find_teams(index + 1, current_score + scores[index], count + 1)
        # Exclude the current student from a team
        exclude_current = find_teams(index + 1, current_score, count)
        
        return include_current or exclude_current
    
    return "YES" if find_teams(0, 0, 0) else "NO"

if __name__ == "__main__":
    input_scores = list(map(int, sys.stdin.readline().split()))
    print(can_form_equal_teams(input_scores))