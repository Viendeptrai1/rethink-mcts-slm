import sys

def max_tandem_repeat(s, k):
    n = len(s)
    ans = 0
    for i in range(1, n//2 + 1):
        if n % i == 0 and s[:i] * (n // i) == s:
            ans = max(ans, 2 * i)
    return ans + 2 * k

# Reading input from standard input
input_data = sys.stdin.read().splitlines()
s = input_data[0]
k = int(input_data[1])

# Calculating and printing the result
print(max_tandem_repeat(s, k))