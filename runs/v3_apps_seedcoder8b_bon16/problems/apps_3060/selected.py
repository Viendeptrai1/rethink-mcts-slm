def find_kth_sequence(n, k):
    def is_valid_sequence(seq):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq) + 1):
                if sum(seq[i:j]) % n == 0:
                    return False
        return True

    def next_valid_sequence(seq):
        for i in range(len(seq) - 1, -1, -1):
            if seq[i] < n - 1:
                seq[i] += 1
                for j in range(i + 1, len(seq)):
                    seq[j] = 1
                return seq
        return None

    sequence = [1] * (n - 1)
    count = 0

    while count < k:
        if is_valid_sequence(sequence):
            count += 1
        if count == k:
            return sequence
        sequence = next_valid_sequence(sequence)
        if sequence is None:
            break

# Read input
n, k = map(int, input().split())

# Find and print the k-th sequence
result = find_kth_sequence(n, k)
print(*result)