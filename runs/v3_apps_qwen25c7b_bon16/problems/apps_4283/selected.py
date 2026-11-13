def max_balanced_team_size(n, skills):
    skills.sort()
    left = 0
    max_size = 0
    
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_size = max(max_size, right - left + 1)
    
    return max_size

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
skills = list(map(int, data[1:]))

# Output the result
print(max_balanced_team_size(n, skills))