import sys

def balance_ternary_string(n, s):
    # Count the occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character
    target_count = n // 3
    
    # Initialize the result list
    result = []
    
    # Track the current counts of '0', '1', and '2' in the result
    current_0 = 0
    current_1 = 0
    current_2 = 0
    
    # Iterate over the string and build the result
    for char in s:
        if current_0 < target_count:
            result.append('0')
            current_0 += 1
        elif current_1 < target_count:
            result.append('1')
            current_1 += 1
        else:
            result.append('2')
            current_2 += 1
    
    # Convert the result list to a string and return
    return ''.join(result)

# Read input
input = sys.stdin.read().split()
n = int(input[0])
s = input[1]

# Get the balanced ternary string
balanced_string = balance_ternary_string(n, s)

# Print the result
print(balanced_string)