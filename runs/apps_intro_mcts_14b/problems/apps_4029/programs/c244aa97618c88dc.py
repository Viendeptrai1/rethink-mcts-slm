import sys

def min_swaps_to_divisible_by_25(n):
    n_str = str(n)
    length = len(n_str)
    
    # Check for patterns ending in '00', '25', '50', '75'
    for i in range(length - 1, -1, -1):
        if n_str[i] == '0':
            for j in range(i - 1, -1, -1):
                if n_str[j] == '0':
                    return length - 2 - j  # Move '00' to the end
                elif n_str[j] in ['2', '5', '7']:
                    return length - 1 - j  # Move '25', '50', '75' to the end
        elif n_str[i] == '5':
            for j in range(i - 1, -1, -1):
                if n_str[j] in ['2', '5', '7']:
                    return length - 1 - j  # Move '25', '50', '75' to the end
    
    return -1

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = min_swaps_to_divisible_by_25(n)
    print(result)