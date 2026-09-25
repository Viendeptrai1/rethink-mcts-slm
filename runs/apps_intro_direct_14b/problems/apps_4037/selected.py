import sys
from typing import List, Tuple

def max_projects(n: int, r: int, projects: List[Tuple[int, int]]) -> int:
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize variables
    current_rating = r
    max_subset_size = 0
    
    # Iterate over each project
    for a, b in projects:
        # Check if Polycarp can start the project
        if current_rating >= a:
            # Update the current rating after completing the project
            current_rating += b
            # Ensure the rating does not fall below zero
            if current_rating < 0:
                current_rating = 0
            # Increment the size of the subset
            max_subset_size += 1
    
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