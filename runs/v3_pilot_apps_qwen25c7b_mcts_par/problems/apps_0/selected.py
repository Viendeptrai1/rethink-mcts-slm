def max_accordion_length(s):
    n = len(s)
    max_len = -1
    i = 0
    
    while i < n:
        if s[i] == '[':
            j = i + 1
            count_colon = 0
            count_pipe = 0
            
            while j < n and s[j] != ']':
                if s[j] == ':':
                    count_colon += 1
                elif s[j] == '|':
                    count_pipe += 1
                j += 1
            
            if j < n and s[j] == ']' and count_colon == 2:
                max_len = max(max_len, j - i + 1)
                i = j + 1
            else:
                i = j + 1
        else:
            i += 1
    
    return max_len

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
print(max_accordion_length(data[0]))