def takahashi_multiplication(A, B):
    if 1 <= A <= 9 and 1 <= B <= 9:
        return A * B
    else:
        return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
A = int(data[0])
B = int(data[1])

result = takahashi_multiplication(A, B)
print(result)