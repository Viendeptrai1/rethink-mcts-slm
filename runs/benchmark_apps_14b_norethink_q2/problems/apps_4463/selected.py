from collections import Counter

def can_rearrange_to_be_less(s, t):
    count_s = Counter(s)
    count_t = Counter(t)
    
    # Check if s can be made lexicographically smaller than t
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if count_s[char] < count_t[char]:
            return "Yes"
        elif count_s[char] > count_t[char]:
            return "No"
    
    # If all characters are equal in count, check lengths
    if len(s) < len(t):
        return "Yes"
    else:
        return "No"

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()
s = data[0]
t = data[1]

# Print the result
print(can_rearrange_to_be_less(s, t))