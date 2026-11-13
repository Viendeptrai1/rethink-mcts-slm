def find_kth_sequence(n, k):
    def is_valid_sequence(seq):
        for i in range(len(seq)):
            if sum(seq[i:]) % n == 0:
                return False
        return True

    def generate_sequences(seq, length):
        if length == n - 1:
            if is_valid_sequence(seq):
                yield seq[:]
            return
        for i in range(1, n):
            seq.append(i)
            yield from generate_sequences(seq, length + 1)
            seq.pop()

    sequence = []
    for valid_sequence in generate_sequences(sequence, 0):
        k -= 1
        if k == 0:
            return valid_sequence

# Read input
n, k = map(int, input().split())

# Find and print the k-th sequence
result = find_kth_sequence(n, k)
print(' '.join(map(str, result)))