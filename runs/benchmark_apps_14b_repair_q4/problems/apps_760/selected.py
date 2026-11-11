def max_tandem_repeat_length(s, k):
    n = len(s)
    max_length = 0
    
    # Function to check if a substring is a tandem repeat
    def is_tandem(sub):
        half = len(sub) // 2
        return sub[:half] == sub[half:]
    
    # Find the longest tandem repeat in the original string
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]
            if is_tandem(sub):
                max_length = max(max_length, 2 * (j - i))
    
    # Check if appending k characters can extend the tandem repeat
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]
            if is_tandem(sub):
                # Calculate the maximum length after appending k characters
                max_length = max(max_length, 2 * (j - i) + min(k, (j - i)))
    
    return max_length

# Read input
import sys
input = sys.stdin.read
data = input().split()
s = data[0]
k = int(data[1])

# Output the result
print(max_tandem_repeat_length(s, k))