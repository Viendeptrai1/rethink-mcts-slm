import sys
from collections import defaultdict

def max_students_in_teams(n, k, skills):
    # Group students by their skill levels
    skill_groups = defaultdict(list)
    for skill in skills:
        skill_groups[skill].append(skill)
    
    # Sort the unique skill levels
    unique_skills = sorted(skill_groups.keys())
    
    # Initialize DP table
    dp = [[0] * (k + 1) for _ in range(len(unique_skills) + 1)]
    
    # Fill the DP table
    for i in range(1, len(unique_skills) + 1):
        for j in range(1, k + 1):
            # Option 1: Do not include the current skill group
            dp[i][j] = dp[i - 1][j]
            
            # Option 2: Include the current skill group
            count = 0
            for l in range(i, 0, -1):
                if unique_skills[i - 1] - unique_skills[l - 1] > 5:
                    break
                count += len(skill_groups[unique_skills[l - 1]])
                if j - 1 >= 0:
                    dp[i][j] = max(dp[i][j], dp[l - 1][j - 1] + count)
    
    return dp[len(unique_skills)][k]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    skills = list(map(int, data[2:]))
    
    result = max_students_in_teams(n, k, skills)
    print(result)

if __name__ == "__main__":
    main()