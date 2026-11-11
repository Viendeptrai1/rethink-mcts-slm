import sys
import heapq

def min_partition_value(n, c, a):
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    heap = []
    
    for i in range(1, n + 1):
        heapq.heappush(heap, (a[i - 1], i))
        if len(heap) > c:
            heapq.heappop(heap)
        dp[i] = dp[i - 1] + a[i - 1]
        if len(heap) == c:
            dp[i] -= heap[0][0]
    
    return dp[n]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:]))
    
    result = min_partition_value(n, c, a)
    print(result)

if __name__ == "__main__":
    main()