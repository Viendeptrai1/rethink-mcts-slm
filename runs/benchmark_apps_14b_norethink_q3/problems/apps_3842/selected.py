import sys
import math

def main():
    import sys
    import math
    
    def can_achieve(target_days, projects, p, q):
        total_experience = 0
        total_money = 0
        for a, b in projects:
            total_experience += a * target_days
            total_money += b * target_days
            if total_experience >= p and total_money >= q:
                return True
        return False
    
    def find_min_days(n, p, q, projects):
        low = 0.0
        high = max(max(p / a, q / b) for a, b in projects)
        while high - low > 1e-6:
            mid = (low + high) / 2.0
            if can_achieve(mid, projects, p, q):
                high = mid
            else:
                low = mid
        return low
    
    # Read input
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = int(data[1])
    q = int(data[2])
    
    projects = []
    index = 3
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        projects.append((a, b))
        index += 2
    
    # Find and print the result
    result = find_min_days(n, p, q, projects)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()