def find_kth_sequence(n, k):
    def is_valid_sequence(seq):
        prefix_sum = 0
        for num in seq:
            prefix_sum += num
            if prefix_sum % n == 0:
                return False
        return True

    def generate_sequences():
        from itertools import product
        for seq in product(range(1, n), repeat=n-1):
            if is_valid_sequence(seq):
                yield seq

    count = 0
    for seq in generate_sequences():
        count += 1
        if count == k:
            return seq

n, k = map(int, input().split())
result = find_kth_sequence(n, k)
print(' '.join(map(str, result)))