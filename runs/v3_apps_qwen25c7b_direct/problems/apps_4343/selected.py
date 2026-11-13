def find_median_string(k, s, t):
    # Calculate the median index
    median_index = (ord(t) - ord(s)) // 2 + ord(s)
    
    # Convert the median index back to a character
    median_char = chr(median_index)
    
    # Create the median string
    median_string = s[:-1] + median_char
    
    return median_string

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
k = int(data[0])
s = data[1]
t = data[2]

# Find and print the median string
print(find_median_string(k, s, t))