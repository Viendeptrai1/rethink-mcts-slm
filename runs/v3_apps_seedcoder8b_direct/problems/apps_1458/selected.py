def find_substring_to_reverse(n, s):
    for i in range(n):
        for j in range(i + 1, n):
            # Reverse the substring s[i:j+1]
            reversed_substring = s[i:j+1][::-1]
            # Form the new string by replacing the original substring with its reverse
            new_string = s[:i] + reversed_substring + s[j+1:]
            # Check if the new string is lexicographically smaller
            if new_string < s:
                return "YES", i + 1, j + 1
    return "NO"

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Get the result
result = find_substring_to_reverse(n, s)

# Print the result
if result == "NO":
    print(result)
else:
    print(result[0])
    print(result[1], result[2])