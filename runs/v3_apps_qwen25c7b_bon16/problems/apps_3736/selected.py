def is_mirror_word(name):
    mirror = {'A': 'A', 'H': 'H', 'I': 'I', 'M': 'M', 'O': 'O', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y'}
    return name == ''.join(mirror.get(char, '') for char in reversed(name))

# Input handling
import sys
input = sys.stdin.read
data = input().split()
name = data[0]

# Output result
result = 'YES' if is_mirror_word(name) else 'NO'
print(result)