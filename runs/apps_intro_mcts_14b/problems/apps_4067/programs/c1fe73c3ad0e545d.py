import sys

def balance_ternary_string(n, s):
    # Count occurrences of '0', '1', and '2'
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character
    target_count = n // 3
    
    # Calculate excess counts
    excess_0 = count_0 - target_count
    excess_1 = count_1 - target_count
    excess_2 = count_2 - target_count
    
    # Initialize the result list
    result = list(s)
    
    # Replace characters to balance the counts
    for i in range(n):
        if excess_1 > 0 and result[i] == '1':
            result[i] = '0'
            excess_1 -= 1
            excess_0 += 1
        elif excess_2 > 0 and result[i] == '2':
            result[i] = '0'
            excess_2 -= 1
            excess_0 += 1
        elif excess_0 < 0 and result[i] == '0':
            result[i] = '1'
            excess_0 += 1
            excess_1 -= 1
        elif excess_2 < 0 and result[i] == '2':
            result[i] = '1'
            excess_2 += 1
            excess_1 -= 1
        elif excess_0 > 0 and result[i] == '0':
            result[i] = '2'
            excess_0 -= 1
            excess_2 += 1
        elif excess_1 < 0 and result[i] == '1':
            result[i] = '2'
            excess_1 += 1
            excess_2 -= 1
    
    return ''.join(result)

# Read input
n = int(sys.stdin.readline().strip())
s = sys.stdin.readline().strip()

# Output the result
print(balance_ternary_string(n, s))