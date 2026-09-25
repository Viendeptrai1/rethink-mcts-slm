import sys
from typing import List, Tuple

def max_projects(n: int, r: int, projects: List[Tuple[int, int]]) -> int:
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Initialize variables
    max_size = 0
    current_rating = r
    
    # Iterate over all possible subsets of projects
    for i in range(1 << n):
        subset_size = 0
        valid = True
        temp_rating = current_rating
        
        for j in range(n):
            if i & (1 << j):
                # Check if the current rating is sufficient to start the project
                if temp_rating < projects[j][0]:
                    valid = False
                    break
                # Update the rating after completing the project
                temp_rating += projects[j][1]
                # Ensure the rating does not fall below zero
                if temp_rating < 0:
                    valid = False
                    break
                subset_size += 1
        
        if valid:
            max_size = max(max_size, subset_size)
    
    return max_size

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