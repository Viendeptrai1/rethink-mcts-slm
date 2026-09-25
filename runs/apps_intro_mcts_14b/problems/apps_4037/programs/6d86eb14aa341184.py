import sys
from typing import List, Tuple

def max_project_subset(n: int, r: int, projects: List[Tuple[int, int]]) -> int:
    # Initialize DP table
    dp = [[False] * (r + 1) for _ in range(n + 1)]
    dp[0][r] = True
    
    # Fill DP table
    for i in range(1, n + 1):
        a, b = projects[i - 1]
        for j in range(r + 1):
            if dp[i - 1][j]:
                if j >= a:
                    dp[i][j + b] = True
                if j + b >= 0:
                    dp[i][j] = True
    
    # Find the maximum size of the subset
    for i in range(n, -1, -1):
        for j in range(r + 1):
            if dp[i][j]:
                return i
    return 0

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
    
    result = max_project_subset(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()