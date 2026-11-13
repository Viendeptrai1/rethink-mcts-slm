import sys
from itertools import permutations
from bisect import bisect_left

MOD = 998244353

def count_good_permutations(n, sequence):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def count_inversions(arr):
        sorted_arr = []
        inv_count = 0
        for num in arr:
            pos = bisect_left(sorted_arr, num)
            inv_count += len(sorted_arr) - pos
            sorted_arr.insert(pos, num)
        return inv_count

    a_inversions = count_inversions([a for a, b in sequence])
    b_inversions = count_inversions([b for a, b in sequence])

    total_permutations = 1
    for i in range(1, n + 1):
        total_permutations = (total_permutations * i) % MOD

    bad_permutations = 0
    for p in permutations(range(n)):
        permuted_a = [sequence[i][0] for i in p]
        permuted_b = [sequence[i][1] for i in p]
        if is_sorted(permuted_a) or is_sorted(permuted_b):
            bad_permutations += 1

    good_permutations = (total_permutations - bad_permutations) % MOD
    return good_permutations

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        sequence.append((a, b))
        index += 2
    
    result = count_good_permutations(n, sequence)
    print(result)

if __name__ == "__main__":
    main()