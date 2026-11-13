def count_good_permutations(n, sequence):
    MOD = 998244353

    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def is_good_sequence(seq):
        first_elements = [x[0] for x in seq]
        second_elements = [x[1] for x in seq]
        return not (is_sorted(first_elements) or is_sorted(second_elements))

    from itertools import permutations

    count = 0
    for perm in permutations(range(n)):
        permuted_sequence = [sequence[i] for i in perm]
        if is_good_sequence(permuted_sequence):
            count += 1

    return count % MOD

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
sequence = [(int(data[i * 2 + 1]), int(data[i * 2 + 2])) for i in range(n)]

print(count_good_permutations(n, sequence))