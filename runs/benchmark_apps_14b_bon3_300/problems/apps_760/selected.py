import sys

def max_tandem_repeat_length(s, k):
    n = len(s)
    max_length = 0
    
    # Check all possible lengths of the tandem repeat
    for l in range(1, n + k + 1):
        if l % 2 == 0:
            half_length = l // 2
            # Check if the first half of the repeat matches the second half
            if s[:half_length] == s[half_length:half_length + half_length]:
                max_length = l
    
    return max_length

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
k = int(data[1])

# Output the result
print(max_tandem_repeat_length(s, k))