def max_balanced_team(n, skills):
    skills.sort()
    left = 0
    result = 0
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        result = max(result, right - left + 1)
    return result

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
skills = list(map(int, data[1:]))

print(max_balanced_team(n, skills))