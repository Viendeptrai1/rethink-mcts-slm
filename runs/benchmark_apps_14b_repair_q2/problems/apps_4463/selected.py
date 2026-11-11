import sys

def can_form_lexicographically_smaller(s, t):
    # Count the frequency of each character in both strings
    from collections import Counter
    count_s = Counter(s)
    count_t = Counter(t)
    
    # Check if s' can be made lexicographically smaller than t'
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if count_s[char] < count_t[char]:
            return "Yes"
        elif count_s[char] > count_t[char]:
            return "No"
    
    # If all characters are equal in count, compare lengths
    if len(s) < len(t):
        return "Yes"
    else:
        return "No"

# Read input from standard input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Print the result
print(can_form_lexicographically_smaller(s, t))