import sys

def max_tandem_repeat_length(s, k):
    def is_tandem_repeat(sub):
        n = len(sub)
        return n % 2 == 0 and sub[:n//2] == sub[n//2:]

    max_length = 0
    n = len(s)

    # Check all possible tandem repeats in the original string
    for i in range(1, n // 2 + 1):
        if is_tandem_repeat(s[:i * 2]):
            max_length = max(max_length, i * 2)

    # Check potential tandem repeats after adding k characters
    for i in range(1, n // 2 + 1):
        if is_tandem_repeat(s[-i * 2:]):
            max_length = max(max_length, i * 2 + min(k, i))

    # Check if the entire string plus k characters can form a tandem repeat
    if is_tandem_repeat(s):
        max_length = max(max_length, n + k)

    return max_length

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
k = int(data[1])

# Output the result
print(max_tandem_repeat_length(s, k))