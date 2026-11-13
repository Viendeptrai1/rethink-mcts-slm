def is_real_puzzle(n, sequence):
    current_sequence = sequence[:]
    for _ in range(n):
        next_sequence = []
        for i in range(n):
            if i % 2 == 0:
                next_sequence.append((current_sequence[i] + 1) % n)
            else:
                next_sequence.append((current_sequence[i] - 1) % n)
        if next_sequence == list(range(n)):
            return "Yes"
        current_sequence = next_sequence
    return "No"

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
sequence = list(map(int, data[1:]))

result = is_real_puzzle(n, sequence)
print(result)