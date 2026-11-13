def find_possible_message(t):
    n = len(t)
    
    # Check for each possible length of the first message
    for i in range(1, n // 2 + 1):
        s = t[:i]
        # Check if repeating s can form the string t
        if s * (n // i) == t[:n - (n % i)]:
            # Check if the remaining part is a valid continuation of s
            if t[n - (n % i):] == s[:n % i]:
                return "YES\n" + s
    
    return "NO"

# Read input
t = input().strip()

# Get the result
result = find_possible_message(t)

# Print the result
print(result)