def find_kth_sequence(n, k):
    def is_valid(seq):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq) + 1):
                if sum(seq[i:j]) % n == 0:
                    return False
        return True

    def generate_sequences(n, k):
        count = 0
        seq = [0] * (n - 1)
        while True:
            seq[0] += 1
            for i in range(n - 1):
                if seq[i] >= n:
                    seq[i] = 1
                    seq[i + 1] += 1
            if is_valid(seq):
                count += 1
                if count == k:
                    return seq

    result = generate_sequences(n, k)
    return ' '.join(map(str, result))

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Find and print the k-th sequence
print(find_kth_sequence(n, k))