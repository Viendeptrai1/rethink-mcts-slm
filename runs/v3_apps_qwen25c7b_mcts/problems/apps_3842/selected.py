import sys

def can_meet_requirements(days, p, q, projects):
    total_experience = 0
    total_money = 0
    for a_i, b_i in projects:
        total_experience += a_i * days
        total_money += b_i * days
    return total_experience >= p and total_money >= q

def min_days_to_reach_goal(n, p, q, projects):
    left, right = 0, max(p / max(a_i for a_i, _ in projects), q / max(b_i for _, b_i in projects))
    while right - left > 1e-9:
        mid = (left + right) / 2
        if can_meet_requirements(mid, p, q, projects):
            right = mid
        else:
            left = mid
    return right

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    p = int(data[index + 1])
    q = int(data[index + 2])
    index += 3
    
    projects = []
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        projects.append((a_i, b_i))
        index += 2
    
    result = min_days_to_reach_goal(n, p, q, projects)
    print(f"{result:.10f}")