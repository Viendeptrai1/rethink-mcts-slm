import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, c = read_ints()
    a = read_ints()
    
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    min_heap = []
    
    for i in range(1, n + 1):
        heapq.heappush(min_heap, a[i - 1])
        if len(min_heap) > i // c:
            dp[i] = dp[i - 1] + a[i - 1]
        else:
            dp[i] = dp[i - 1] + a[i - 1] - heapq.heappop(min_heap)
    
    print(dp[n])

if __name__ == "__main__":
    main()