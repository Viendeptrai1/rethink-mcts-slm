from typing import List

class Solution:
    def remove_duplicates(self, numbers: List[int]) -> List[int]:
        seen = set()
        result = []
        for number in numbers:
            if number not in seen:
                seen.add(number)
                result.append(number)
        return result