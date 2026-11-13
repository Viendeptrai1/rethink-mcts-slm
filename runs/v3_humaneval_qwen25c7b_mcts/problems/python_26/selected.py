from typing import List

class Solution:
    def remove_duplicates(self, numbers: List[int]) -> List[int]:
        occurrence = {}
        for num in numbers:
            if num in occurrence:
                occurrence[num] += 1
            else:
                occurrence[num] = 1
        
        return [num for num in numbers if occurrence[num] == 1]

# Example usage:
# solution = Solution()
# print(solution.remove_duplicates([1, 2, 3, 2, 4]))  # Output: [1, 3, 4]