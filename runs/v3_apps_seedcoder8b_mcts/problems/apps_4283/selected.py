def max_balanced_team(n, skills):
    skills.sort()
    max_team_size = 0
    left = 0

    for right in range(n):
        while skills[right] - skills[left] > 5:
            left += 1
        max_team_size = max(max_team_size, right - left + 1)

    return max_team_size

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    skills = list(map(int, data[1:n+1]))
    
    result = max_balanced_team(n, skills)
    print(result)