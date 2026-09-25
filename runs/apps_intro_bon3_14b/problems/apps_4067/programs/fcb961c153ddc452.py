import sys

def balance_ternary_string(n, s):
    count = [0, 0, 0]
    for char in s:
        count[int(char)] += 1
    
    target_count = n // 3
    changes = []
    
    for i in range(n):
        if count[0] > target_count:
            changes.append('0')
            count[0] -= 1
            count[2] += 1
        elif count[1] > target_count:
            changes.append('1')
            count[1] -= 1
            count[0] += 1
        elif count[2] > target_count:
            changes.append('2')
            count[2] -= 1
            count[1] += 1
        else:
            changes.append(s[i])
            count[int(s[i])] -= 1
    
    return ''.join(changes)

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