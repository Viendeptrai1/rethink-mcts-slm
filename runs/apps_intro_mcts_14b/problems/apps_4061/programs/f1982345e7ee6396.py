import sys

def max_removable_substring(s, t):
    n, m = len(s), len(t)
    
    # Find the longest prefix of t that matches a prefix of s
    prefix_match = 0
    for i in range(m):
        if prefix_match < n and s[prefix_match] == t[i]:
            prefix_match += 1
    
    # Find the longest suffix of t that matches a suffix of s
    suffix_match = 0
    for i in range(m - 1, -1, -1):
        if suffix_match < n and s[n - 1 - suffix_match] == t[i]:
            suffix_match += 1
    
    # If the entire t matches a prefix and suffix of s, we need to find the minimal window
    if prefix_match + suffix_match >= m:
        # Find the minimal window that contains all characters of t
        left, right = 0, n - 1
        j = 0
        
        # Move left pointer to find the start of the window
        while j < m and left < n:
            if s[left] == t[j]:
                j += 1
            left += 1
        
        # Move right pointer to find the end of the window
        j = m - 1
        while j >= 0 and right >= 0:
            if s[right] == t[j]:
                j -= 1
            right -= 1
        
        # Calculate the length of the substring to remove
        return n - (left - right - 1)
    
    # If t does not match the entire prefix and suffix, we can remove the non-matching parts
    return n - prefix_match - suffix_match

# Read input
input = sys.stdin.read
data = input().split()
s = data[0]
t = data[1]

# Output the result
print(max_removable_substring(s, t))