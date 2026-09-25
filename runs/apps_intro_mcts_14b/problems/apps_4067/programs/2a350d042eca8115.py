import sys

def balance_ternary_string(n, s):
    # Count occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Target count for each character in a balanced ternary string
    target_count = n // 3
    
    # Calculate excess counts
    excess_0 = count_0 - target_count
    excess_1 = count_1 - target_count
    excess_2 = count_2 - target_count
    
    # Initialize the result list
    result = []
    
    # Iterate through the string and make replacements
    for char in s:
        if char == '0':
            if excess_0 > 0:
                result.append('0')
                excess_0 -= 1
            elif excess_1 < 0:
                result.append('1')
                excess_1 += 1
            else:
                result.append('2')
                excess_2 -= 1
        elif char == '1':
            if excess_1 > 0:
                result.append('1')
                excess_1 -= 1
            elif excess_2 < 0:
                result.append('2')
                excess_2 += 1
            else:
                result.append('0')
                excess_0 += 1
        else:  # char == '2'
            if excess_2 > 0:
                result.append('2')
                excess_2 -= 1
            elif excess_0 < 0:
                result.append('0')
                excess_0 += 1
            else:
                result.append('1')
                excess_1 += 1
    
    # Join the result list into a string and return
    return ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Get the balanced ternary string
balanced_string = balance_ternary_string(n, s)

# Print the result
print(balanced_string)