def find_sequences(n, a):
    if n == 0:
        print("YES")
        print("0")
        print("")
        print("0")
        print("")
        return

    from itertools import permutations

    def is_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))

    def is_decreasing(seq):
        return all(x > y for x, y in zip(seq, seq[1:]))

    def is_valid_partition(seq, inc, dec):
        if len(inc) + len(dec) != len(seq):
            return False

        if inc and not is_increasing(inc):
            return False

        if dec and not is_decreasing(dec):
            return False

        combined = inc + dec
        return sorted(combined) == sorted(seq) and set(combined) == set(seq)

    a_set = set(a)
    
    for inc_size in range(n + 1):
        for dec_size in range(n + 1 - inc_size):
            for inc_perm in permutations(a, inc_size):
                for dec_perm in permutations(a, dec_size):
                    inc = list(inc_perm)
                    dec = list(dec_perm)
                    if is_valid_partition(a, inc, dec):
                        print("YES")
                        print(inc_size)
                        print(" ".join(map(str, sorted(inc))))
                        print(dec_size)
                        print(" ".join(map(str, sorted(dec, reverse=True))))
                        return

    print("NO")

# Reading input
import sys
input = sys.stdin.read
data = input().strip().split()
n = int(data[0])
a = list(map(int, data[1:n+1]))

find_sequences(n, a)