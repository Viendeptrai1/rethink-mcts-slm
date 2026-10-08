def can_form_lexicographically_smaller(s, t):
    from collections import Counter
    
    # Count the frequency of each character in s and t
    count_s = Counter(s)
    count_t = Counter(t)
    
    # Compare the cumulative frequencies of characters
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if count_s[char] < count_t[char]:
            return "Yes"
        elif count_s[char] > count_t[char]:
            return "No"
    
    # If all characters have the same frequency, check the lengths
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
print(can_form_lexicographically_smaller(s, t))