import sys

def balance_ternary_string(n, s):
    count = [0, 0, 0]
    for char in s:
        count[int(char)] += 1
    
    target_count = n // 3
    replacements = []
    
    # Calculate excess counts
    excess_0 = count[0] - target_count
    excess_1 = count[1] - target_count
    excess_2 = count[2] - target_count
    
    # Determine replacements needed
    for char in s:
        if excess_0 > 0 and char == '0':
            replacements.append('1')
            excess_0 -= 1
            excess_1 += 1
        elif excess_1 > 0 and char == '1':
            replacements.append('2')
            excess_1 -= 1
            excess_2 += 1
        elif excess_2 > 0 and char == '2':
            replacements.append('0')
            excess_2 -= 1
            excess_0 += 1
        else:
            replacements.append(char)
    
    return ''.join(replacements)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    
    result = balance_ternary_string(n, s)
    print(result)

if __name__ == "__main__":
    main()