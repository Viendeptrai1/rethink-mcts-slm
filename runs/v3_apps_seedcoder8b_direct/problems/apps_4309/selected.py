def find_earliest_abc(N):
    # Convert N to a string to easily check if all digits are the same
    str_N = str(N)
    
    # Check if all characters in the string are the same
    if all(char == str_N[0] for char in str_N):
        return N
    
    # If not, find the next number where all digits are the same
    current = N + 1
    while True:
        str_current = str(current)
        if all(char == str_current[0] for char in str_current):
            return current
        current += 1

# Read input
N = int(input().strip())

# Find and print the earliest ABC
result = find_earliest_abc(N)
print(result)