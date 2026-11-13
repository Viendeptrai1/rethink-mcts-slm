def solve_equal_teams(scores):
    total_score = sum(scores)
    if total_score % 2 != 0:
        return "NO"
    
    target_score = total_score // 2
    for i in range(6):
        for j in range(i+1, 6):
            for k in range(j+1, 6):
                team1_score = scores[i] + scores[j] + scores[k]
                if team1_score == target_score:
                    return "YES"
    return "NO"

if __name__ == "__main__":
    scores = list(map(int, input().split()))
    print(solve_equal_teams(scores))