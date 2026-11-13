from collections import defaultdict
import sys

input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

debts = defaultdict(int)
for i in range(m):
    a = int(data[3 * i + 2]) - 1
    b = int(data[3 * i + 3]) - 1
    c = int(data[3 * i + 4])
    debts[a] += c
    debts[b] -= c

total_debt = sum(abs(d) for d in debts.values())

print(total_debt // 2)