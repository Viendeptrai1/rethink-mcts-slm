def find_median_string(k, s, t):
    def next_string(s):
        s = list(s)
        for i in range(k-1, -1, -1):
            if s[i] < 'z':
                s[i] = chr(ord(s[i]) + 1)
                for j in range(i+1, k):
                    s[j] = 'a'
                return ''.join(s)
        return None

    def prev_string(s):
        s = list(s)
        for i in range(k-1, -1, -1):
            if s[i] > 'a':
                s[i] = chr(ord(s[i]) - 1)
                for j in range(i+1, k):
                    s[j] = 'z'
                return ''.join(s)
        return None

    total_count = sum(1 for _ in range(k))
    current = s
    count = 0

    while True:
        if current == t:
            break
        current = next_string(current)
        count += 1

    median_index = count // 2
    current = s
    for _ in range(median_index):
        current = next_string(current)

    return current

# Read input
import sys
input = sys.stdin.read
data = input().split()

k = int(data[0])
s = data[1]
t = data[2]

# Find and print the median string
median_string = find_median_string(k, s, t)
print(median_string)