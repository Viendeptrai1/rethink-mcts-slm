import sys

def min_days_to_dream(n, p, q, projects):
    def can_achieve_goals(days):
        total_exp = sum(a * days for a, _ in projects)
        total_money = sum(b * days for _, b in projects)
        return total_exp >= p and total_money >= q

    left, right = 0, 1e10
    while right - left > 1e-9:
        mid = (left + right) / 2
        if can_achieve_goals(mid):
            right = mid
        else:
            left = mid

    return left

def main():
    n, p, q = map(int, input().split())
    projects = [tuple(map(int, input().split())) for _ in range(n)]
    result = min_days_to_dream(n, p, q, projects)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()