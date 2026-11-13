def min_paint_to_achieve_beauty(n, m, k, colors, paint_costs):
    import sys
    from functools import lru_cache

    # Initialize the DP table with a large number
    INF = sys.maxsize

    # Memoization for the recursive function
    @lru_cache(None)
    def dp(index, last_color, groups):
        # If we've processed all trees
        if index == n:
            # Check if the number of groups matches the desired beauty
            return 0 if groups == k else INF

        # If the current tree is already colored
        if colors[index] != 0:
            # Continue to the next tree
            return dp(index + 1, colors[index], groups + (1 if colors[index] != last_color else 0))

        # Try coloring the current tree with each color
        min_cost = INF
        for color in range(1, m + 1):
            cost = paint_costs[index][color - 1]
            new_groups = groups + (1 if color != last_color else 0)
            min_cost = min(min_cost, cost + dp(index + 1, color, new_groups))

        return min_cost

    # Start the DP from the first tree, with no last color and no groups
    result = dp(0, 0, 0)

    # If the result is still INF, it means no valid coloring was found
    return result if result != INF else -1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
k = int(data[2])
colors = list(map(int, data[3:n + 3]))
paint_costs = []

index = n + 3
for i in range(n):
    paint_costs.append(list(map(int, data[index:index + m])))
    index += m

# Get the result
result = min_paint_to_achieve_beauty(n, m, k, colors, paint_costs)

# Print the result
print(result)