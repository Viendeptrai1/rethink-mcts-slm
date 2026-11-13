def can_distribute_candies(a, b, c):
    total = a + b + c
    if total % 2 != 0:
        return "No"
    target = total // 2
    if a <= target and b <= target and c <= target:
        return "Yes"
    if a <= target and b + c <= target:
        return "Yes"
    if a + b <= target and c <= target:
        return "Yes"
    if a + c <= target and b <= target:
        return "Yes"
    return "No"

# Read input
import sys
input = sys.stdin.read
data = input().split()
a = int(data[0])
b = int(data[1])
c = int(data[2])

# Print result
print(can_distribute_candies(a, b, c))