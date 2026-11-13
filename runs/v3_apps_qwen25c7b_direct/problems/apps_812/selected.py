def find_arithmetic_progression_index(n, b):
    def is_arithmetic(seq):
        if len(seq) < 2:
            return True
        diff = seq[1] - seq[0]
        return all(seq[i] - seq[i - 1] == diff for i in range(2, len(seq)))

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