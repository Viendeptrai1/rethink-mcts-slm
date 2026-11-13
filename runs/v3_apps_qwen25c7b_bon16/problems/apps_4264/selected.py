def count_odd_digit_numbers(N):
    return sum(1 for i in range(1, N+1) if len(str(i)) % 2 != 0)

# Read input from standard input
import sys
input = sys.stdin.read
N = int(input().strip())

# Call the function and print the result
print(count_odd_digit_numbers(N))