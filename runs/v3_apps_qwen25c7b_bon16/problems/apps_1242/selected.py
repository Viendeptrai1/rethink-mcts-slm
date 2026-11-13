def find_prefix_reversals(s):
    n = len(s)
    reversed_indices = [0] * n
    min_word = s[:]
    
    for i in range(1, n + 1):
        current_word = s[:i][::-1] + s[i:]
        if current_word < min_word:
            min_word = current_word
            for j in range(i):
                reversed_indices[j] = 1 - reversed_indices[j]
    
    return reversed_indices

# Input handling
import sys
input = sys.stdin.read
data = input().split()
s = data[0]

# Output handling
reversed_indices = find_prefix_reversals(s)
print(' '.join(map(str, reversed_indices)))