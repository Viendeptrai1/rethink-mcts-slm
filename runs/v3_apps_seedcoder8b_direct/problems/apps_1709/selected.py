def min_paint_for_beauty(n, m, k, colors, paint_costs):
    from functools import lru_cache
    import sys

    sys.setrecursionlimit(10**6)

    # Helper function to calculate the beauty of a given coloring
    def calculate_beauty(coloring):
        beauty = 1
        for i in range(1, n):
            if coloring[i] != coloring[i - 1]:
                beauty += 1
        return beauty

    # Helper function to calculate the minimum paint required for a given coloring
    def calculate_paint(coloring):
        total_paint = 0
        for i in range(n):
            if coloring[i] != 0:
                total_paint += paint_costs[i][coloring[i] - 1]
        return total_paint

    # Recursive function with memoization to find the minimum paint for a given beauty
    @lru_cache(None)
    def dp(index, current_beauty, last_color):
        if index == n:
            return 0 if current_beauty == k else float('inf')

        if colors[index] != 0:
            # Tree is already colored
            if colors[index] != last_color:
                current_beauty += 1
            return dp(index + 1, current_beauty, colors[index])

        min_paint = float('inf')
        for color in range(1, m + 1):
            if color != last_color:
                current_beauty += 1
            if current_beauty > k:
                break
            paint = paint_costs[index][color - 1] + dp(index + 1, current_beauty, color)
            min_paint = min(min_paint, paint)
            if color != last_color:
                current_beauty -= 1

        return min_paint

    # Start the recursive search
    result = dp(0, 0, 0)
    return result if result != float('inf') else -1

# Example usage:
# n, m, k = 3, 2, 2
# colors = [0, 0, 0]
# paint_costs = [
#     [1, 2],
#     [3, 4],
#     [5, 6]
# ]
# print(min_paint_for_beauty(n, m, k, colors, paint_costs))  # Output: 10