from typing import List

class Solution:
    @staticmethod
    def factorize(n: int) -> List[int]:
        factors = []
        # Start with the smallest prime number
        divisor = 2
        while n >= divisor * divisor:
            if n % divisor == 0:
                factors.append(divisor)
                n //= divisor
            else:
                divisor += 1
        if n > 1:
            factors.append(n)
        return factors

# Example usage:
# print(Solution.factorize(8))   # Output: [2, 2, 2]
# print(Solution.factorize(25))  # Output: [5, 5]
# print(Solution.factorize(70))  # Output: [2, 5, 7]