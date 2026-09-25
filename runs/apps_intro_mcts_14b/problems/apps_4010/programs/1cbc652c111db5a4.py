import sys

def has_palindromic_subsequence(n, a):
    # Create a 2D DP table initialized to 0
    dp = [[0] * n for _ in range(n)]
    
    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = 1
    
    # Check for palindromes of length 2
    for i in range(n - 1):
        if a[i] == a[i + 1]:
            dp[i][i + 1] = 2
    
    # Check for palindromes of length greater than 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if a[i] == a[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    # If there is any palindromic subsequence of length at least 3
    for i in range(n):
        for j in range(i, n):
            if dp[i][j] >= 3:
                return "YES"
    
    return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        a = list(map(int, data[index:index + n]))
        index += n
        result = has_palindromic_subsequence(n, a)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()