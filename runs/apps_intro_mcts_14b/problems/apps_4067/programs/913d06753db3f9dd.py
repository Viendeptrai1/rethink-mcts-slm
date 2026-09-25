import sys

def balance_ternary_string(s):
    # Count occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character in a balanced string
    target_count = len(s) // 3
    
    # Determine the number of replacements needed for each character
    replace_0 = max(0, target_count - count_0)
    replace_1 = max(0, target_count - count_1)
    replace_2 = max(0, target_count - count_2)
    
    # Create a list from the string to allow modifications
    result = list(s)
    
    # Priority replacements: '2' -> '1' -> '0'
    i = 0
    while replace_2 > 0:
        if result[i] == '2':
            result[i] = '1'
            replace_2 -= 1
        i += 1
    
    while replace_1 > 0:
        if result[i] == '1':
            result[i] = '0'
            replace_1 -= 1
        i += 1
    
    while replace_0 > 0:
        if result[i] == '0':
            result[i] = '2'
            replace_0 -= 1
        i += 1
    
    # Join the list back into a string and return
    return ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Output the result
print(balance_ternary_string(s))