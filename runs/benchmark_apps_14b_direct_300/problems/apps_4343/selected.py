def find_median_string(k, s, t):
    # Calculate the number of strings between s and t
    total_strings = sum(1 for _ in range(ord(s[0]), ord(t[0]) + 1)) * (26 ** (k - 1))
    
    # Find the median position
    median_position = total_strings // 2
    
    # Function to get the next string lexicographically
    def next_string(current):
        current = list(current)
        for i in range(k - 1, -1, -1):
            if current[i] < 'z':
                current[i] = chr(ord(current[i]) + 1)
                for j in range(i + 1, k):
                    current[j] = 'a'
                return ''.join(current)
        return None
    
    # Start from s and move forward to find the median string
    current = s
    for _ in range(median_position):
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