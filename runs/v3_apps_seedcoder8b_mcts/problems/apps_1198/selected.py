import sys
import heapq

def min_partition_sum(n, c, a):
    # Function to calculate the value of a subarray
    def subarray_value(subarray):
        k = len(subarray)
        remove_count = k // c
        return sum(heapq.nlargest(k - remove_count, subarray))
    
    # Initialize the dp array where dp[i] represents the minimum sum of values
    # for partitioning the first i elements of the array
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: no elements, no cost
    
    # Iterate over each possible end of a subarray
    for i in range(1, n + 1):
        # Consider all possible start points for the subarray ending at i
        for j in range(i):
            # Calculate the value of the subarray a[j:i]
            current_value = subarray_value(a[j:i])
            # Update the dp array
            dp[i] = min(dp[i], dp[j] + current_value)
    
    # The answer is the minimum sum of values for partitioning the entire array
    return dp[n]

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:2 + n]))
    
    result = min_partition_sum(n, c, a)
    print(result)

if __name__ == "__main__":
    main()