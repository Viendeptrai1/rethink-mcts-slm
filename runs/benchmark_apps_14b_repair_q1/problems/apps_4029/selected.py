import sys

def min_moves_to_divisible_by_25(n):
    str_n = str(n)
    length = len(str_n)
    
    # Check for '00', '25', '50', '75' at the end of the string
    for i in range(length - 1, -1, -1):
        if str_n[i] == '0':
            for j in range(i - 1, -1, -1):
                if str_n[j] in ['0', '2', '5', '7']:
                    # Calculate the number of swaps needed
                    swaps = i + (length - 1 - j)
                    # Ensure no leading zeros are created
                    if all(str_n[k] != '0' for k in range(j + 1, i)):
                        return swaps
        elif str_n[i] == '5':
            for j in range(i - 1, -1, -1):
                if str_n[j] in ['2', '7']:
                    # Calculate the number of swaps needed
                    swaps = i + (length - 1 - j)
                    # Ensure no leading zeros are created
                    if all(str_n[k] != '0' for k in range(j + 1, i)):
                        return swaps
    
    return -1

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    result = min_moves_to_divisible_by_25(n)
    print(result)