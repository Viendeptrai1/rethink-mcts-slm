from typing import List

class Solution:
    @staticmethod
    def separate_paren_groups(paren_string: str) -> List[str]:
        paren_string = paren_string.replace(" ", "")
        stack = []
        result = []
        current_group = []

        for char in paren_string:
            if char == '(':
                stack.append(char)
                current_group.append(char)
            elif char == ')':
                stack.pop()
                current_group.append(char)
                if not stack:
                    result.append(''.join(current_group))
                    current_group = []

        return result

# Example usage:
solution = Solution()
print(solution.separate_paren_groups('( ) (( )) (( )( ))'))  # Output: ['()', '(())', '(()())']