import sys
import heapq

def smallest_partition_sum(n, c, a):
    # This function computes the smallest possible sum of the values
    # of contiguous subarrays of 'a' when partitioned as described.

    # Initialize a prefix sum array
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]

    # Initialize dp array where dp[i] represents the smallest sum of the
    # values of contiguous subarrays for the first 'i' elements of 'a'
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    # Process each element as the end of a partition
    for i in range(1, n + 1):
        # We need to consider all possible starting points of a subarray
        # ending at position i, we need at least one element in the subarray
        for j in range(i):
            # Calculate the number of elements in this subarray
            k = i - j
            # Determine the number of elements we should exclude
            exclude_count = k // c
            # Calculate the sum of the subarray starting at j and ending at i-1
            total_sum = prefix_sum[i] - prefix_sum[j]
            # If we exclude 'exclude_count' elements, the smallest 'exclude_count'
            # elements will be removed (as they are smallest in this subarray)
            # Sort this subarray to find these smallest elements and exclude them
            subarray = a[j:i]
            subarray.sort()
            excluded_sum = sum(subarray[:exclude_count])
            subarray_value = total_sum - excluded_sum
            # Update dp[i] by considering this subarray
            dp[i] = min(dp[i], dp[j] + subarray_value)

    # The answer is the smallest sum for the entire array
    return dp[n]

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:2 + n]))
    
    result = smallest_partition_sum(n, c, a)
    print(result)

if __name__ == "__main__":
    main()