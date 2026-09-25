import sys

def can_complete_projects(n, r, projects):
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Try to complete the projects in the sorted order
    for a, b in projects:
        if r < a:
            return "NO"
        r += b
        if r < 0:
            return "NO"
    
    return "YES"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    r = int(data[index + 1])
    index += 2
    
    projects = []
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        projects.append((a, b))
        index += 2
    
    result = can_complete_projects(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()