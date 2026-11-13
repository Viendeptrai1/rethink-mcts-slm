from typing import List

class Solution:
    def median(self, l: List[int]) -> float:
        sorted_l = sorted(l)
        n = len(sorted_l)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_l[mid - 1] + sorted_l[mid]) / 2.0
        else:
            return sorted_l[mid]

# Example usage:
# sol = Solution()
# print(sol.median([3, 1, 2, 4, 5]))  # Output: 3
# print(sol.median([-10, 4, 6, 1000, 10, 20]))  # Output: 15.0