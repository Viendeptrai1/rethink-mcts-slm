import sys
from collections import defaultdict

def max_balanced_team(n, skills):
    # Sort the skills array
    skills.sort()
    
    # Initialize variables
    max_size = 0
    left = 0
    
    # Use a sliding window approach
    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_size = max(max_size, right - left + 1)
    
    return max_size

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
skills = list(map(int, data[1:]))

# Output the result
print(max_balanced_team(n, skills))