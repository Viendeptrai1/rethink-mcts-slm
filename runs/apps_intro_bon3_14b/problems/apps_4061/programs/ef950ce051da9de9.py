import sys

def max_substring_to_remove(s, t):
    n, m = len(s), len(t)
    # Create a list to store the indices of each character in s
    idx = [[] for _ in range(26)]
    for i, c in enumerate(s):
        idx[ord(c) - ord('a')].append(i)
    
    # Initialize pointers for s and t
    i, j = 0, 0
    # This will store the maximum length of the substring we can remove
    max_remove = 0
    
    while j < m:
        c = t[j]
        # Find the smallest index in s that is greater than or equal to the current position in s
        pos = -1
        for k in idx[ord(c) - ord('a')]:
            if k >= i:
                pos = k
                break
        
        # If no such index exists, it means we cannot form the subsequence t
        if pos == -1:
            break
        
        # Update the maximum length of the substring we can remove
        max_remove = max(max_remove, pos - i)
        # Move the pointer in s to the next character
        i = pos + 1
        # Move the pointer in t to the next character
        j += 1
    
    # The remaining part of s after forming the subsequence t
    max_remove = max(max_remove, n - i)
    
    return max_remove

# Read input
s = sys.stdin.readline().strip()
t = sys.stdin.readline().strip()

# Print the result
print(max_substring_to_remove(s, t))