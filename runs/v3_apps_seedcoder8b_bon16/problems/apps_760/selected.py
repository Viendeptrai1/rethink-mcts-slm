def max_tandem_repeat_length(s, k):
    n = len(s)
    
    # Function to check if a string is a tandem repeat
    def is_tandem_repeat(t):
        length = len(t)
        if length % 2 != 0:
            return False
        half = length // 2
        return all(t[i] == t[i + half] for i in range(half))
    
    # The maximum possible length of the tandem repeat
    max_length = 0
    
    # Check all possible tandem repeats
    for i in range(n):
        for j in range(i + 1, n + k + 1):
            if is_tandem_repeat(s[i:j]):
                max_length = max(max_length, j - i)
    
    return max_length

# Reading input from standard input
import sys
input = sys.stdin.read
data = input().split()
s = data[0]
k = int(data[1])

# Calculating the maximum tandem repeat length and printing the result
result = max_tandem_repeat_length(s, k)
print(result)