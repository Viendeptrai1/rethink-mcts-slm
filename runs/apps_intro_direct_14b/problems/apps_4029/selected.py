import sys

def min_moves_to_divisible_by_25(n):
    str_n = str(n)
    length = len(str_n)
    
    # Check for '00', '25', '50', '75' at the end
    for i in range(length - 1, -1, -1):
        if str_n[i] == '0':
            for j in range(i - 1, -1, -1):
                if str_n[j] == '0' or str_n[j] == '5':
                    return length - 1 - j
        elif str_n[i] == '5':
            for j in range(i - 1, -1, -1):
                if str_n[j] == '2' or str_n[j] == '7':
                    return length - 1 - j
    
    return -1

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = min_moves_to_divisible_by_25(n)
    print(result)