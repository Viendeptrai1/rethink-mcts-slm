import sys

def max_problems_in_contest(n, difficulties):
    dp = [1] * n
    max_problems = 1
    
    for i in range(1, n):
        for j in range(i):
            if difficulties[i] <= difficulties[j] * 2:
                dp[i] = max(dp[i], dp[j] + 1)
        max_problems = max(max_problems, dp[i])
    
    return max_problems

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    result = max_problems_in_contest(n, difficulties)
    print(result)

if __name__ == "__main__":
    main()