def can_form_equal_teams(scores):
    total_score = sum(scores)
    
    # If the total score is odd, it's impossible to split into two equal parts
    if total_score % 2 != 0:
        return "NO"
    
    target_score = total_score // 2
    
    # Use dynamic programming to check if we can form two teams with equal scores
    dp = [False] * (target_score + 1)
    dp[0] = True
    
    for score in scores:
        for j in range(target_score, score - 1, -1):
            dp[j] = dp[j] or dp[j - score]
    
    return "YES" if dp[target_score] else "NO"

# Read input
scores = list(map(int, input().split()))

# Print the result
print(can_form_equal_teams(scores))