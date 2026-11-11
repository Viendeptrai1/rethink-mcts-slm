import sys
from collections import defaultdict

MOD = 998244353

def count_good_permutations(n, pairs):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    first_elements = [pair[0] for pair in pairs]
    second_elements = [pair[1] for pair in pairs]

    if is_sorted(first_elements) or is_sorted(second_elements):
        return 0

    # Count the frequency of each element in first and second elements
    first_count = defaultdict(int)
    second_count = defaultdict(int)
    for a, b in pairs:
        first_count[a] += 1
        second_count[b] += 1

    # Calculate the number of permutations
    total_permutations = 1
    for count in first_count.values():
        total_permutations = total_permutations * count % MOD
    for count in second_count.values():
        total_permutations = total_permutations * count % MOD

    return total_permutations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    pairs = [(int(data[2 * i + 1]), int(data[2 * i + 2])) for i in range(n)]

    result = count_good_permutations(n, pairs)
    print(result)

if __name__ == "__main__":
    main()