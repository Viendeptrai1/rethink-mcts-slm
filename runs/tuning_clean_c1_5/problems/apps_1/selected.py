import sys

def max_digit_sum(x):
    x_str = str(x)
    max_sum = 0
    best_number = 0
    
    # Try to form numbers by replacing digits with 9s
    for i in range(len(x_str)):
        for digit in range(9, -1, -1):
            new_number_str = x_str[:i] + str(digit) + '9' * (len(x_str) - i - 1)
            if int(new_number_str) <= x:
                digit_sum = sum(int(d) for d in new_number_str)
                if digit_sum > max_sum or (digit_sum == max_sum and int(new_number_str) > best_number):
                    max_sum = digit_sum
                    best_number = int(new_number_str)
    
    return best_number

if __name__ == "__main__":
    import sys
    x = int(sys.stdin.read().strip())
    print(max_digit_sum(x))