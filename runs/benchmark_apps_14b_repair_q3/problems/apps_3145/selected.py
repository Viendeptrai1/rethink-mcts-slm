def count_multiples(X, A, B, allowed_digits):
    def is_valid_number(num_str):
        return all(digit in allowed_digits for digit in num_str)
    
    count = 0
    for num in range(A, B + 1):
        if num % X == 0 and is_valid_number(str(num)):
            count += 1
    return count

# Reading input
import sys
input = sys.stdin.read
data = input().split()

X = int(data[0])
A = int(data[1])
B = int(data[2])
allowed_digits = data[3]

# Calculating and printing the result
result = count_multiples(X, A, B, allowed_digits)
print(result)