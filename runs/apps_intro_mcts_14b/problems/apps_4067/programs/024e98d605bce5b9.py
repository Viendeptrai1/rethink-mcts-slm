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
    
    # Replace characters to balance the counts
    i = 0
    while count_0 < target_count or count_1 < target_count or count_2 < target_count:
        if count_2 > target_count and result[i] == '2':
            result[i] = '1'
            count_2 -= 1
            count_1 += 1
        elif count_1 > target_count and result[i] == '1':
            result[i] = '0'
            count_1 -= 1
            count_0 += 1
        i += 1
    
    return ''.join(result)

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
s = data[1]

# Output the result
print(balance_ternary_string(s))