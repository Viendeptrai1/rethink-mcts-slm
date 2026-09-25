import sys

def balance_ternary_string(s):
    n = len(s)
    count_0 = s.count('0')
    count_1 = s.count('1')
    count_2 = s.count('2')
    
    # Calculate the target count for each character
    target_count = n // 3
    
    # Initialize the result list
    result = list(s)
    
    # Calculate excess counts
    excess_0 = count_0 - target_count
    excess_1 = count_1 - target_count
    excess_2 = count_2 - target_count
    
    # Adjust the string to make it balanced
    for i in range(n):
        if excess_0 > 0 and result[i] == '0':
            result[i] = '1'
            excess_0 -= 1
            excess_1 += 1
        elif excess_1 > 0 and result[i] == '1':
            result[i] = '2'
            excess_1 -= 1
            excess_2 += 1
        elif excess_2 > 0 and result[i] == '2':
            result[i] = '0'
            excess_2 -= 1
            excess_0 += 1
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(balance_ternary_string(s))