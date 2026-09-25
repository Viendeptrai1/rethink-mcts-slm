import sys
from typing import List, Tuple

def max_projects(n: int, r: int, projects: List[Tuple[int, int]]) -> int:
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize variables
    current_rating = r
    max_subset_size = 0
    
    # Try to include each project if possible
    for a, b in projects:
        if current_rating >= a:
            # If we can do the project, update the current rating and increase the subset size
            current_rating += b
            max_subset_size += 1
        else:
            # If we cannot do the project, check if we can still maintain non-negative rating
            if current_rating + b < 0:
                # If the rating would go below zero, we cannot include any more projects
                break
    
    return max_subset_size

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