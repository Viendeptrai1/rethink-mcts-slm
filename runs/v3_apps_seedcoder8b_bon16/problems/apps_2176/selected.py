import sys
from itertools import permutations
from bisect import bisect_left, bisect_right

MOD = 998244353

def is_good_sequence(seq):
    # Check if the sequence of first elements is sorted
    if all(seq[i][0] <= seq[i + 1][0] for i in range(len(seq) - 1)):
        return False
    
    # Check if the sequence of second elements is sorted
    if all(seq[i][1] <= seq[i + 1][1] for i in range(len(seq) - 1)):
        return False
    
    return True

def count_good_permutations(n, sequence):
    count = 0
    for perm in permutations(range(n)):
        permuted_sequence = [sequence[i] for i in perm]
        if is_good_sequence(permuted_sequence):
            count += 1
    return count % MOD

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n)]
    
    result = count_good_permutations(n, sequence)
    print(result)

if __name__ == "__main__":
    main()