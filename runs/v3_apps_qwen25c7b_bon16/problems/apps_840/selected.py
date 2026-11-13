import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])

a = list(map(int, data[2:2+n]))
b = list(map(int, data[2+n:]))

max_cookies = 0

for i in range(n):
    if a[i] <= b[i]:
        max_cookies += b[i] // a[i]

print(max_cookies + k // min(a))