import sys

def can_form_equal_teams(scores):
    scores.sort()
    total_sum = sum(scores)
    
    # If the total sum is not even, we cannot split it into two equal parts
    if total_sum % 2 != 0:
        return "NO"
    
    target = total_sum // 2
    
    # Try to find two subsets with sum equal to target
    def find_subset_with_sum(index, current_sum, used):
        if current_sum == target:
            return True
        if index == 6 or current_sum > target:
            return False
        
        # Include the current score in the subset
        if not used[index]:
            used[index] = True
            if find_subset_with_sum(index + 1, current_sum + scores[index], used):
                return True
            used[index] = False
        
        # Exclude the current score from the subset
        return find_subset_with_sum(index + 1, current_sum, used)
    
    used = [False] * 6
    if find_subset_with_sum(0, 0, used):
        return "YES"
    else:
        return "NO"

# Read input
input_scores = list(map(int, sys.stdin.readline().split()))

# Output the result
print(can_form_equal_teams(input_scores))