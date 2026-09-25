import sys

def can_complete_projects(n, r, projects):
    # Sort projects by the required rating in ascending order
    projects.sort(key=lambda x: x[0])
    
    # Try to complete each project in the sorted order
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
    
    n = int(data[0])
    r = int(data[1])
    
    projects = []
    index = 2
    for i in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        projects.append((a, b))
        index += 2
    
    result = can_complete_projects(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()