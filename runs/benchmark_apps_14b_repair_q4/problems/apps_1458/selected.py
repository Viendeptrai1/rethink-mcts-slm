def find_smaller_string(n, s):
    # Convert the string to a list for easier manipulation
    s = list(s)
    
    # Find the first position where the string can be improved
    for i in range(n - 1):
        if s[i] > s[i + 1]:
            # Find the longest suffix that is in descending order starting from i
            j = n - 1
            while j > i and s[j] <= s[j - 1]:
                j -= 1
            
            # Reverse the substring from i to j
            s[i:j+1] = reversed(s[i:j+1])
            
            # Check if the resulting string is lexicographically smaller
            if s < list(s[::-1]):
                return "YES", i + 1, j + 1
    
    return "NO"

# Read input
n = int(input().strip())
s = input().strip()

# Get the result
result = find_smaller_string(n, s)

# Print the result
if result == "NO":
    print("NO")
else:
    print("YES")
    print(result[1], result[2])