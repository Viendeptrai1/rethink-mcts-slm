def count_unique_numbers(N, A):
    unique_numbers = set()
    for number in A:
        if number in unique_numbers:
            unique_numbers.remove(number)
        else:
            unique_numbers.add(number)
    return len(unique_numbers)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:]))

print(count_unique_numbers(N, A))