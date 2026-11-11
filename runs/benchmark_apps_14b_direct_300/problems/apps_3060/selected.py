def find_kth_sequence(n, k):
    def is_valid_sequence(seq):
        prefix_sums = [0]
        for num in seq:
            prefix_sums.append((prefix_sums[-1] + num) % n)
        for i in range(1, len(prefix_sums)):
            for j in range(i + 1, len(prefix_sums)):
                if prefix_sums[j] == prefix_sums[i]:
                    return False
        return True

    def next_sequence(seq):
        for i in range(len(seq) - 1, -1, -1):
            if seq[i] < n - 1:
                seq[i] += 1
                for j in range(i + 1, len(seq)):
                    seq[j] = 1
                return seq
        return None

    seq = [1] * (n - 1)
    count = 0
    while True:
        if is_valid_sequence(seq):
            count += 1
            if count == k:
                return seq
        seq = next_sequence(seq)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
result = find_kth_sequence(n, k)
print(' '.join(map(str, result)))