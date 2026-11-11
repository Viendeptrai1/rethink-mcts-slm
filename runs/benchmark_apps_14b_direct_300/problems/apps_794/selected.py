import sys
from itertools import permutations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    total_sum = sum(a)
    if total_sum % 2 != 0:
        print("-1")
        return
    
    target_sum = total_sum // 2
    
    def can_partition(arr, n, target):
        dp = [False] * (target + 1)
        dp[0] = True
        
        for num in arr:
            for j in range(target, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        
        return dp[target]
    
    if not can_partition(a, n, target_sum):
        print("-1")
        return
    
    def find_partition(arr, n, target):
        dp = [[False] * (target + 1) for _ in range(n + 1)]
        dp[0][0] = True
        
        for i in range(1, n + 1):
            for j in range(target + 1):
                dp[i][j] = dp[i - 1][j]
                if j >= arr[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j - arr[i - 1]]
        
        partition = []
        j = target
        for i in range(n, 0, -1):
            if dp[i][j] and not dp[i - 1][j]:
                partition.append(arr[i - 1])
                j -= arr[i - 1]
        
        return partition
    
    partition1 = find_partition(a, 2 * n, target_sum)
    partition2 = [x for x in a if x not in partition1]
    
    print(" ".join(map(str, partition1 + partition2)))

if __name__ == "__main__":
    main()