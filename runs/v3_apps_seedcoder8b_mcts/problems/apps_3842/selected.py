def min_days_to_dream(n, p, q, projects):
    def can_achieve_goals(days):
        total_experience = 0
        total_money = 0
        for a, b in projects:
            total_experience += a * days
            total_money += b * days
        return total_experience >= p and total_money >= q

    left, right = 0, 1e10
    epsilon = 1e-7

    while right - left > epsilon:
        mid = (left + right) / 2
        if can_achieve_goals(mid):
            right = mid
        else:
            left = mid

    return left

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = int(data[1])
    q = int(data[2])
    
    projects = []
    index = 3
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        projects.append((a_i, b_i))
        index += 2
    
    result = min_days_to_dream(n, p, q, projects)
    print(f"{result:.12f}")