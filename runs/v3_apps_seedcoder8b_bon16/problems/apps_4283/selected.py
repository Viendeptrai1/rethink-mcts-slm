def max_balanced_team(n, skills):
    skills.sort()
    max_team = 0
    left = 0
    
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_team = max(max_team, right - left + 1)
    
    return max_team

# Read input
n = int(input())
skills = list(map(int, input().split()))

# Compute and print result
result = max_balanced_team(n, skills)
print(result)