def find_arithmetic_progression_index(n, b):
    def is_arithmetic(lst):
        if len(lst) < 2:
            return True
        diff = lst[1] - lst[0]
        for i in range(2, len(lst)):
            if lst[i] - lst[i - 1] != diff:
                return False
        return True

    for j in range(n):
        remaining = sorted(b[:j] + b[j+1:])
        if is_arithmetic(remaining):
            return j + 1
    return -1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
b = list(map(int, data[1:]))

result = find_arithmetic_progression_index(n, b)
print(result)