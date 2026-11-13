def min_hours_to_build_houses(n, heights):
    from math import ceil

    def can_build(k):
        # Count the number of hills that can be used to build houses
        count = 0
        i = 0
        while i < n:
            if (i == 0 or heights[i] > heights[i - 1]) and (i == n - 1 or heights[i] > heights[i + 1]):
                count += 1
                i += 1  # Skip the next hill as it can't be used
            i += 1
        return count >= k

    def min_hours_for_k(k):
        # Binary search to find the minimum hours required to build k houses
        low, high = 0, max(heights)
        while low < high:
            mid = (low + high) // 2
            if can_build_with_hours(k, mid):
                high = mid
            else:
                low = mid + 1
        return low

    def can_build_with_hours(k, hours):
        # Check if it's possible to build k houses with the given number of hours
        count = 0
        i = 0
        while i < n:
            if (i == 0 or heights[i] > heights[i - 1]) and (i == n - 1 or heights[i] > heights[i + 1]):
                count += 1
                i += 1  # Skip the next hill as it can't be used
            else:
                # Calculate the minimum height needed to make this hill suitable
                if i == 0:
                    needed = heights[i + 1] + 1
                elif i == n - 1:
                    needed = heights[i - 1] + 1
                else:
                    needed = max(heights[i - 1], heights[i + 1]) + 1
                if needed <= heights[i] + hours:
                    count += 1
                    i += 1  # Skip the next hill as it can't be used
            i += 1
        return count >= k

    max_k = ceil(n / 2)
    results = []
    for k in range(1, max_k + 1):
        results.append(min_hours_for_k(k))
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
heights = list(map(int, data[1:n+1]))

# Get results
results = min_hours_to_build_houses(n, heights)

# Print results
print(" ".join(map(str, results)))