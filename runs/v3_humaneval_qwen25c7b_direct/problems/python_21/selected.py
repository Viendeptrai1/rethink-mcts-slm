from typing import List

class Solution:
    @staticmethod
    def rescale_to_unit(numbers: List[float]) -> List[float]:
        min_val = min(numbers)
        max_val = max(numbers)
        range_val = max_val - min_val
        return [(x - min_val) / range_val for x in numbers]

# Example usage:
solution = Solution()
print(solution.rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]))  # Output: [0.0, 0.25, 0.5, 0.75, 1.0]