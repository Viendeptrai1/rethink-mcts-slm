def min_hours_to_build_houses(n, heights):
    import math

    def can_build(k):
        # Count the number of hills that can be used to build k houses
        count = 0
        i = 0
        while i < n:
            if (i == 0 or heights[i] > heights[i - 1]) and (i == n - 1 or heights[i] > heights[i + 1]):
                count += 1
                i += 1  # Skip the next hill as it can't be used
            i += 1
        return count >= k

    max_k = math.ceil(n / 2)
    results = []

    for k in range(1, max_k + 1):
        left, right = 0, 10**9
        while left < right:
            mid = (left + right) // 2
            # Create a copy of heights to simulate the excavator's work
            temp_heights = heights[:]
            for i in range(n):
                if (i == 0 or temp_heights[i] > temp_heights[i - 1]) and (i == n - 1 or temp_heights[i] > temp_heights[i + 1]):
                    continue
                # Decrease the height of the hill to make it suitable
                if temp_heights[i] > 0:
                    temp_heights[i] = max(0, temp_heights[i] - mid)
            if can_build(k):
                right = mid
            else:
                left = mid + 1
        results.append(left)

    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
heights = list(map(int, data[1:n+1]))

# Get the result and print it
result = min_hours_to_build_houses(n, heights)
print(" ".join(map(str, result)))