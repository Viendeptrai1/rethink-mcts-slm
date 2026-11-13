import re

class Solution:
    def is_bored(self, S):
        sentences = re.split(r'[.?!]\s*', S)
        return sum(1 for sentence in sentences if sentence.startswith('I '))

# Example usage:
solution = Solution()
print(solution.is_bored("Hello world"))  # Output: 0
print(solution.is_bored("The sky is blue. The sun is shining. I love this weather"))  # Output: 1