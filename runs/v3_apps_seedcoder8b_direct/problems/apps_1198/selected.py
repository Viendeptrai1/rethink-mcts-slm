import sys
import heapq

def min_partition_sum(n, c, a):
    # Function to calculate the value of an array b of length k
    def calculate_value(subarray):
        k = len(subarray)
        # Find the floor(k/c) smallest elements
        smallest_k = heapq.nsmallest(k // c, subarray)
        # Sum the rest of the elements
        return sum(subarray) - sum(smallest_k)
    
    # Initialize the dp array where dp[i] represents the minimum sum of values
    # for partitioning the first i elements of the array
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: no elements, no cost
    
    # Iterate over each possible end of a subarray
    for i in range(1, n + 1):
        # Try every possible start of a subarray ending at i
        for j in range(i):
            # Calculate the value of the subarray a[j:i]
            subarray_value = calculate_value(a[j:i])
            # Update the dp table
            dp[i] = min(dp[i], dp[j] + subarray_value)
    
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