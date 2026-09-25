import sys

def max_project_subset(n, r, projects):
    # Initialize dp array with -1 (indicating impossible states)
    dp = [-1] * (r + 1)
    dp[r] = 0  # Starting with initial rating r, we can do 0 projects initially

    for a, b in projects:
        # Create a temporary dp array to store updates for this iteration
        new_dp = dp[:]
        for j in range(r, -1, -1):
            if dp[j] != -1 and j >= a:
                new_dp[j + b] = max(new_dp[j + b], dp[j] + 1)
        dp = new_dp

    # Find the maximum value in dp array, which represents the maximum subset size
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