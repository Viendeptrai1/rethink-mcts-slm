def find_possible_message(t):
    n = len(t)
    
    # Check if there's any overlap of at least one character between consecutive segments
    for i in range(2, n + 1):
        prefix = t[:i]
        suffix = t[-i:]
        
        if prefix == suffix:
            return "YES", t[:-i]
    
    return "NO"

# Example usage:
t = input().strip()
result, possible_s = find_possible_message(t)
print(result)
if result == "YES":
    print(possible_s)