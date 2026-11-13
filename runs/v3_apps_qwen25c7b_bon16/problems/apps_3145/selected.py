def count_valid_multiples(X, A, B, allowed_digits):
    count = 0
    for num in range(A, B + 1):
        if all(digit in allowed_digits for digit in str(num)) and num % X == 0:
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

result = count_valid_multiples(X, A, B, allowed_digits)
print(result)