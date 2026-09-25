import sys
from typing import List, Tuple

def max_projects(n: int, r: int, projects: List[Tuple[int, int]]) -> int:
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize a list to keep track of the maximum rating Polycarp can have after completing i projects
    max_rating = [0] * (n + 1)
    max_rating[0] = r
    
    # Initialize a list to keep track of the maximum number of projects completed up to i projects
    max_projects_completed = [0] * (n + 1)
    
    for i in range(1, n + 1):
        a, b = projects[i - 1]
        for j in range(i, 0, -1):
            if max_rating[j - 1] >= a:
                new_rating = max_rating[j - 1] + b
                if new_rating >= 0:
                    max_rating[j] = max(max_rating[j], new_rating)
                    max_projects_completed[j] = max(max_projects_completed[j], max_projects_completed[j - 1] + 1)
    
    return max(max_projects_completed)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    projects = []
    
    index = 2
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        projects.append((a, b))
        index += 2
    
    result = max_projects(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()