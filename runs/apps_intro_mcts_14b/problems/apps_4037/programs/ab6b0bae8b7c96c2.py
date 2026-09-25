import sys

def max_projects(n, r, projects):
    # Initialize the DP array with -1, indicating that initially no projects are done
    dp = [-1] * (r + 1)
    dp[r] = 0  # Starting with initial rating r, 0 projects are done

    for i in range(n):
        a, b = projects[i]
        new_dp = dp[:]
        for j in range(r, -1, -1):
            if dp[j] != -1 and j >= a:
                new_rating = j + b
                if 0 <= new_rating <= r:
                    new_dp[new_rating] = max(new_dp[new_rating], dp[j] + 1)
        dp = new_dp

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
    
    result = max_projects(n, r, projects)
    print(result)

if __name__ == "__main__":
    main()