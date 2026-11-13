import sys

def calculate_minimum_days(n, p, q, projects):
    # Sort projects by the ratio of experience gained to money earned
    projects.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    total_experience = 0
    total_money = 0
    days = 0
    
    for a_i, b_i in projects:
        if total_experience >= p and total_money >= q:
            break
        
        days += 1
        total_experience += a_i
        total_money += b_i
    
    return days if total_experience >= p and total_money >= q else float('inf')

def main():
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
    
    result = calculate_minimum_days(n, p, q, projects)
    
    if result == float('inf'):
        print("No solution")
    else:
        print(f"{result:.6f}")

if __name__ == "__main__":
    main()