import sys
import heapq

def main():
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, c = read_ints()
    a = read_ints()
    
    # Initialize the dp array
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    # Min-heap to keep track of the smallest elements in the current subarray
    min_heap = []
    current_sum = 0
    
    for i in range(1, n + 1):
        # Add the current element to the heap and the current sum
        heapq.heappush(min_heap, a[i - 1])
        current_sum += a[i - 1]
        
        # If the heap size exceeds c, remove the smallest element
        if len(min_heap) > c:
            smallest = heapq.heappop(min_heap)
            current_sum -= smallest
        
        # Calculate the value of the current subarray
        value = current_sum - sum(min_heap[:len(min_heap) // c])
        
        # Update the dp array
        dp[i] = min(dp[i], dp[i - len(min_heap)] + value)
    
    print(dp[n])

if __name__ == "__main__":
    main()