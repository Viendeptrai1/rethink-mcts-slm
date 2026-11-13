def can_form_equal_teams(scores):
    total_sum = sum(scores)
    if total_sum % 2 != 0:
        return "NO"
    
    target = total_sum // 2
    n = len(scores)
    dp = [False] * (target + 1)
    dp[0] = True
    
    for score in scores:
        for j in range(target, score - 1, -1):
            dp[j] = dp[j] or dp[j - score]
    
    return "YES" if dp[target] else "NO"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
scores = list(map(int, data))
print(can_form_equal_teams(scores))