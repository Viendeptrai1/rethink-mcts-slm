def find_median_string(k, s, t):
    # Convert strings to lists for easier manipulation
    s_list = list(s)
    t_list = list(t)
    
    # Find the first position where s and t differ
    median_list = s_list[:]
    for i in range(k):
        if s_list[i] != t_list[i]:
            # Calculate the median character for this position
            median_char = chr((ord(s_list[i]) + ord(t_list[i])) // 2)
            median_list[i] = median_char
            break
    
    # Fill the rest of the string with the median character
    for i in range(i + 1, k):
        median_list[i] = median_char
    
    return ''.join(median_list)

# Read input
k = int(input())
s = input().strip()
t = input().strip()

# Find and print the median string
result = find_median_string(k, s, t)
print(result)