from typing import List

class Solution:
    def below_zero(self, operations: List[int]) -> bool:
        balance = 0
        for operation in operations:
            balance += operation
            if balance < 0:
                return True
        return False

# For call-based execution
def below_zero(operations: List[int]) -> bool:
    solution = Solution()
    return solution.below_zero(operations)