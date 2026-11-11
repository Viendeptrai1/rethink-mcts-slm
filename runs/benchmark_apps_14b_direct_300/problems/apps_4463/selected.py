import sys

def can_form_lexicographically_smaller(s, t):
    # Sort both strings
    sorted_s = sorted(s)
    sorted_t = sorted(t)
    
    # Compare the sorted strings lexicographically
    if sorted_s < sorted_t:
        return "Yes"
    else:
        return "No"

# Read input from standard input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Print the result
print(can_form_lexicographically_smaller(s, t))