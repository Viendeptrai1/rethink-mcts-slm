import sys

def max_project_subset(n, r, projects):
    # Initialize a DP array where dp[i] represents the maximum subset size achievable with rating i
    dp = [0] * (r + 1)
    
    # Iterate over each project
    for a, b in projects:
        # Traverse the DP array backwards to avoid overwriting results from the current iteration
        for i in range(r, a - 1, -1):
            if dp[i - a] > 0 or i >= a:
                dp[i] = max(dp[i], dp[i - a] + 1)
    
    # The answer is the maximum value in the DP array
    return max(dp)

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
    
    result = max_project_subset(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()