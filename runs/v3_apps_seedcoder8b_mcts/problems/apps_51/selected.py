def find_possible_message(t):
    n = len(t)
    
    # Function to check if a given overlap is valid
    def is_valid_overlap(overlap_len):
        if overlap_len == 0:
            return False
        # Check if the string can be divided into two parts with the given overlap
        for i in range(overlap_len, n):
            if t[i] != t[i - overlap_len]:
                return False
        return True
    
    # Try to find the longest valid overlap
    for overlap_len in range(1, n // 2 + 1):
        if is_valid_overlap(overlap_len):
            # If a valid overlap is found, return the result
            return "YES\n" + t[:n - overlap_len]
    
    # If no valid overlap is found, return "NO"
    return "NO"

# Read input
t = input().strip()

# Get the result
result = find_possible_message(t)

# Print the result
print(result)