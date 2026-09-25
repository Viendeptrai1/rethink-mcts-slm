import sys
from itertools import permutations

def can_complete_projects(n, r, projects):
    for perm in permutations(projects):
        current_rating = r
        valid = True
        for a, b in perm:
            if current_rating < a:
                valid = False
                break
            current_rating += b
            if current_rating < 0:
                valid = False
                break
        if valid:
            return "YES"
    return "NO"

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
    
    result = can_complete_projects(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()