import sys

def balance_ternary_string(n, s):
    # Count occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character in a balanced string
    target_count = n // 3
    
    # Initialize the result list
    result = []
    
    # Iterate through the string and make replacements
    for char in s:
        if count_0 > target_count:
            result.append('0')
            count_0 -= 1
        elif count_1 > target_count:
            result.append('1')
            count_1 -= 1
        else:
            result.append('2')
            count_2 -= 1
    
    # Join the result list into a string and return
    return ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Get the balanced ternary string
balanced_string = balance_ternary_string(n, s)

# Print the result
print(balanced_string)