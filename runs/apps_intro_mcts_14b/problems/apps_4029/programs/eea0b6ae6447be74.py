import sys

def min_moves_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for '00'
    if '00' in n_str:
        return n_str.index('00')
    
    # Check for '25', '50', '75'
    positions = []
    for i in range(length):
        if n_str[i] == '2' or n_str[i] == '5' or n_str[i] == '7':
            for j in range(i + 1, length):
                if n_str[j] == '5' and n_str[i] == '2':
                    positions.append(j - i + 1)
                elif n_str[j] == '0' and (n_str[i] == '5' or n_str[i] == '7'):
                    positions.append(j - i + 1)
    
    if not positions:
        return -1
    
    return min(positions)

# Read input
input_line = sys.stdin.read().strip()
result = min_moves_to_divisible_by_25(input_line)

# Print result
print(result)