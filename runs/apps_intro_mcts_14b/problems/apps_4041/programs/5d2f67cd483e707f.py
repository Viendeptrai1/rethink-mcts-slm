import sys

def max_removable_substring(s, t):
    n, m = len(s), len(t)
    i, j = 0, 0
    prev_match = -1
    max_length = 0
    
    while i < n:
        if j < m and s[i] == t[j]:
            if prev_match != -1:
                max_length = max(max_length, i - prev_match - 1)
            prev_match = i
            j += 1
        i += 1
    
    if prev_match != -1:
        max_length = max(max_length, n - prev_match - 1)
    
    return max_length

if __name__ == "__main__":
    import sys
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()
    result = max_removable_substring(s, t)
    print(result)