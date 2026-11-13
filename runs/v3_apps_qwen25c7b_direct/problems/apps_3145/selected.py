def count_multiples(X, A, B, allowed_digits):
    def is_valid_number(num_str, allowed_digits):
        return all(digit in allowed_digits for digit in num_str)
    
    count = 0
    for i in range(A, B + 1):
        if i % X == 0 and is_valid_number(str(i), allowed_digits):
            count += 1
    return count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
X = int(data[0])
A = int(data[1])
B = int(data[2])
allowed_digits = data[3]

result = count_multiples(X, A, B, allowed_digits)
print(result)