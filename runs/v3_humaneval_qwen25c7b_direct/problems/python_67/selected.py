import re

class Solution:
    def fruit_distribution(self, s, n):
        numbers = map(int, re.findall(r'\d+', s))
        return n - sum(numbers)