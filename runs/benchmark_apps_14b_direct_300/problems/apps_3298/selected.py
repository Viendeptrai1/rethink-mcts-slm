import sys
from collections import Counter
from math import factorial

MOD = 10**9 + 9

def count_entirely_unsorted_permutations(n, a):
    def is_sorted(i):
        left = all(a[j] <= a[i] for j in range(i))
        right = all(a[j] >= a[i] for j in range(i + 1, n))
        return left and right

    sorted_indices = [i for i in range(n) if is_sorted(i)]
    unsorted_count = n - len(sorted_indices)

    if unsorted_count == 0:
        return 0

    freq = Counter(a)
    total_permutations = factorial(n) % MOD

    for count in freq.values():
        total_permutations = total_permutations * pow(factorial(count), MOD - 2, MOD) % MOD

    sorted_permutations = 1
    for count in Counter(a[sorted_indices]).values():
        sorted_permutations = sorted_permutations * pow(factorial(count), MOD - 2, MOD) % MOD

    return (total_permutations - sorted_permutations) % MOD

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = count_entirely_unsorted_permutations(n, a)
    print(result)

if __name__ == "__main__":
    main()