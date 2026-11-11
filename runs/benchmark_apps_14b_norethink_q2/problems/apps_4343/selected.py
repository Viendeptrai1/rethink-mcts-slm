def find_median_string(k, s, t):
    def char_to_index(c):
        return ord(c) - ord('a')
    
    def index_to_char(i):
        return chr(i + ord('a'))
    
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
    
    # Calculate the number of strings between s and t
    count = 0
    current = s
    while current <= t:
        count += 1
        current = next_string(current)
    
    # Find the median position
    median_pos = count // 2
    
    # Generate the median string
    current = s
    for _ in range(median_pos):
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
print(find_median_string(k, s, t))