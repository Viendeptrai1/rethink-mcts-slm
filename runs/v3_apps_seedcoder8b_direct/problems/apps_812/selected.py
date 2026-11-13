def find_arithmetic_index(n, b):
    if n == 2:
        return 1  # Any removal of one element makes it an arithmetic progression

    b.sort()

    # Check if the whole array is already an arithmetic progression
    def is_arithmetic(seq):
        if len(seq) <= 2:
            return True
        d = seq[1] - seq[0]
        for i in range(2, len(seq)):
            if seq[i] - seq[i - 1] != d:
                return False
        return True

    if is_arithmetic(b):
        return 1  # Any removal of one element makes it an arithmetic progression

    # Check if removing one element can make it an arithmetic progression
    for i in range(n):
        # Create a new sequence without the i-th element
        new_seq = b[:i] + b[i+1:]
        if is_arithmetic(new_seq):
            return i + 1  # Convert 0-based index to 1-based

    return -1

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
b = list(map(int, data[1:n+1]))

# Find and print the result
result = find_arithmetic_index(n, b)
print(result)