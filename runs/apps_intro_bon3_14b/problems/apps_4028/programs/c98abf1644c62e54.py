import sys
from collections import defaultdict

MOD = 10**9 + 7

def count_regular_sequences(n, s):
    # Function to calculate binomial coefficient C(n, k)
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)  # Take advantage of symmetry
        c = 1
        for i in range(k):
            c = c * (n - i) // (i + 1)
        return c

    # Calculate the number of ways to balance the remaining brackets
    def count_ways_to_balance(open_count, close_count):
        if open_count < 0 or close_count < 0 or open_count > close_count:
            return 0
        return binomial_coefficient(open_count + close_count, open_count)

    # Precompute the number of ways to balance the remaining brackets
    balance_ways = defaultdict(int)
    for open_count in range(n + 1):
        for close_count in range(n + 1):
            balance_ways[(open_count, close_count)] = count_ways_to_balance(open_count, close_count)

    # Count the number of valid sequences
    result = 0
    open_count = 0
    close_count = 0

    for char in s:
        if char == '(':
            open_count += 1
        else:
            close_count += 1

        # If at any point close_count exceeds open_count, it's invalid
        if close_count > open_count:
            return 0

    # Calculate the number of ways to place the remaining brackets
    remaining_open = n - open_count
    remaining_close = n - close_count

    # The number of valid sequences is the product of the number of ways to balance the remaining brackets
    result = balance_ways[(remaining_open, remaining_close)]

    return result % MOD

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Calculate and print the result
print(count_regular_sequences(n, s))