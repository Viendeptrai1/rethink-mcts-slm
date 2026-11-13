def find_median_string(k, s, t):
    median = []
    for i in range(k):
        min_char = ord(s[i])
        max_char = ord(t[i])
        if min_char == max_char:
            median.append(chr(min_char))
        else:
            mid_char = chr((min_char + max_char) // 2)
            median.append(mid_char)
    return ''.join(median)

# Input reading
import sys
input = sys.stdin.read
data = input().split()
k = int(data[0])
s = data[1]
t = data[2]

# Output the result
print(find_median_string(k, s, t))