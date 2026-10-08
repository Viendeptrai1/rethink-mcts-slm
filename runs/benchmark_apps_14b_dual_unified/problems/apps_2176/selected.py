import sys
from itertools import permutations

def is_good_sequence(seq):
    first_elements = [x[0] for x in seq]
    second_elements = [x[1] for x in seq]
    
    return not (first_elements == sorted(first_elements) or second_elements == sorted(second_elements))

def count_good_permutations(n, seq):
    MOD = 998244353
    count = 0
    
    for perm in permutations(range(n)):
        permuted_seq = [seq[i] for i in perm]
        if is_good_sequence(permuted_seq):
            count += 1
            count %= MOD
    
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    seq = []
    index = 1
    for i in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        seq.append((a, b))
        index += 2
    
    result = count_good_permutations(n, seq)
    print(result)

if __name__ == "__main__":
    main()