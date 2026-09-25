import sys

def max_projects(n, r, projects):
    # Initialize the dp array where dp[i] represents the maximum number of projects
    # Polycarp can complete with rating i.
    dp = [0] * (r + 1)
    
    # Iterate over each project
    for a, b in projects:
        # Update the dp array from right to left to avoid using the same project multiple times
        for i in range(r, a - 1, -1):
            if dp[i - a] > 0 or i >= a:
                dp[i] = max(dp[i], dp[i - a] + 1)
    
    return max(dp)

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