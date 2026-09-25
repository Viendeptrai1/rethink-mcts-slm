import sys

def balance_ternary_string(n, s):
    count = {'0': 0, '1': 0, '2': 0}
    
    # Count the occurrences of '0', '1', and '2'
    for char in s:
        count[char] += 1
    
    # Calculate the target count for each character in a balanced string
    target_count = n // 3
    
    # Determine how many replacements are needed
    replacements = {
        '0': max(0, target_count - count['0']),
        '1': max(0, target_count - count['1']),
        '2': max(0, target_count - count['2'])
    }
    
    # Create the result string
    result = []
    for char in s:
        if replacements[char] > 0:
            # Replace the character if we still need to replace some of this type
            if char == '0':
                result.append('1')
                replacements['1'] -= 1
            elif char == '1':
                result.append('2')
                replacements['2'] -= 1
            else:
                result.append('0')
                replacements['0'] -= 1
        else:
            result.append(char)
    
    return ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Output the result
print(balance_ternary_string(n, s))