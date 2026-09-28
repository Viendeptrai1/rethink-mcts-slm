import sys

def max_digit_sum(x):
    x_str = str(x)
    n = len(x_str)
    
    # Start with the highest possible digit sum
    max_sum = sum(int(digit) for digit in x_str)
    best_number = x
    
    # Try to reduce the number while maintaining the maximum digit sum
    for i in range(n):
        if x_str[i] != '0':
            # Try to replace the current digit with a smaller one
            for new_digit in range(int(x_str[i]) - 1, -1, -1):
                new_number_str = x_str[:i] + str(new_digit) + '9' * (n - i - 1)
                new_number = int(new_number_str)
                if new_number <= x:
                    new_sum = sum(int(digit) for digit in new_number_str)
                    if new_sum > max_sum or (new_sum == max_sum and new_number > best_number):
                        max_sum = new_sum
                        best_number = new_number
                        break
    
    return best_number

if __name__ == "__main__":
    import sys
    x = int(sys.stdin.read().strip())
    print(max_digit_sum(x))