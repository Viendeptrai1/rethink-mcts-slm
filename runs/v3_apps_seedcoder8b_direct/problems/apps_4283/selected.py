def max_balanced_team(n, skills):
    skills.sort()
    max_team_size = 1
    current_team_size = 1

    for i in range(1, n):
        if skills[i] - skills[i - 1] <= 5:
            current_team_size += 1
        else:
            max_team_size = max(max_team_size, current_team_size)
            current_team_size = 1

    max_team_size = max(max_team_size, current_team_size)
    return max_team_size

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    skills = list(map(int, data[1:n+1]))
    
    result = max_balanced_team(n, skills)
    print(result)