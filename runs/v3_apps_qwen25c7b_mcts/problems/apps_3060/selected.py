from itertools import product

def find_kth_sequence(n, k):
    def is_valid(seq):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq) + 1):
                if sum(seq[i:j]) % n == 0:
                    return False
        return True

    count = 0
    for seq in product(range(1, n), repeat=n - 1):
        if is_valid(seq):
            count += 1
            if count == k:
                return seq

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    k = int(data[1])
    result = find_kth_sequence(n, k)
    print(" ".join(map(str, result)))