import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
a = list(map(int, data[1:]))

operations = 0

for num in a:
    while num % 2 == 0:
        num //= 2
        operations += 1
    while num % 3 == 0:
        num //= 3
        operations += 1

print(operations)