import sys

def construct_string(n, k, t):
    # If k is 1, the string s is just t itself
    if k == 1:
        return t
    
    # If k is greater than 1, we need to overlap t in such a way
    # that it appears exactly k times.
    # The optimal way to do this is to repeat t (k-1) times and then
    # append the first (n-1) characters of t to the end.
    # This ensures that the last (n-1) characters of the repeated part
    # overlap with the first (n-1) characters of the appended part,
    # creating exactly k occurrences of t.
    
    # Construct the string s
    s = t * (k - 1) + t[:n-1]
    
    return s

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
t = data[2]

# Construct and print the result
result = construct_string(n, k, t)
print(result)