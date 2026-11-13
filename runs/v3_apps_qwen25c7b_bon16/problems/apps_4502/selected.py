import sys

def reverse_and_append(sequence):
    reversed_sequence = []
    for num in sequence:
        reversed_sequence.append(num)
        reversed_sequence.reverse()
    return reversed_sequence

# Read input from stdin
input = sys.stdin.read
data = input().split()

n = int(data[0])
sequence = list(map(int, data[1:]))

result = reverse_and_append(sequence)

# Print the result
print(' '.join(map(str, result)))