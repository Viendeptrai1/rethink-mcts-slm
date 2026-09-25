import sys

def balance_ternary_string(n, s):
    # Count occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character in a balanced string
    target_count = n // 3
    
    # Determine how many replacements are needed for each character
    replace_0 = max(0, target_count - count_0)
    replace_1 = max(0, target_count - count_1)
    replace_2 = max(0, target_count - count_2)
    
    # Create a list from the string for easier manipulation
    s_list = list(s)
    
    # Replace characters to achieve the target counts
    # Prioritize replacing '2' with '1', then '1' with '0' to maintain lexicographical order
    index = 0
    while replace_2 > 0:
        if s_list[index] == '2':
            s_list[index] = '1'
            replace_2 -= 1
        index += 1
    
    while replace_1 > 0:
        if s_list[index] == '1':
            s_list[index] = '0'
            replace_1 -= 1
        index += 1
    
    # Join the list back into a string and return
    return ''.join(s_list)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Get the result
result = balance_ternary_string(n, s)

# Print the result
print(result)