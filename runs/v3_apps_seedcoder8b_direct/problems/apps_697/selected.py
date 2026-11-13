def maximal_prefix_sum_sum(n, m):
    MOD = 998244853
    
    # If n or m is zero, the only possible maximal prefix sum is 0
    if n == 0 or m == 0:
        return 0
    
    # Calculate the number of arrays with exactly n 1's and m -1's
    # This is given by the binomial coefficient C(n + m, n)
    def binomial_coefficient(x, y):
        if y > x:
            return 0
        if y == 0 or y == x:
            return 1
        y = min(y, x - y)
        num = 1
        den = 1
        for i in range(y):
            num = (num * (x - i)) % MOD
            den = (den * (i + 1)) % MOD
        return (num * pow(den, MOD - 2, MOD)) % MOD
    
    total_arrays = binomial_coefficient(n + m, n)
    
    # Calculate the sum of maximal prefix sums
    # For each array, the maximal prefix sum is the sum of the first n elements
    # Since each of these elements is 1, the maximal prefix sum is n
    # There are total_arrays such arrays
    sum_max_prefix_sums = (total_arrays * n) % MOD
    
    return sum_max_prefix_sums

# Read input
import sys
input = sys.stdin.read
data = input().strip()
n, m = map(int, data.split())

# Output the result
print(maximal_prefix_sum_sum(n, m))