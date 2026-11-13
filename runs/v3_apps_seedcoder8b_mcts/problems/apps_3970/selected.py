def largest_k_multiple_free_subset(n, k, arr):
    arr.sort()
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[i] % arr[j] != 0 or arr[i] // arr[j] != k:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    arr = list(map(int, data[2:2+n]))
    
    result = largest_k_multiple_free_subset(n, k, arr)
    print(result)