def find_kth_sequence(n, k):
    def is_valid_sequence(seq):
        total = 0
        for x in seq:
            total += x
            if total % n == 0:
                return False
        return True

    def generate_sequences(prefix, length):
        if length == 0:
            if is_valid_sequence(prefix):
                return [prefix]
            return []
        sequences = []
        for i in range(1, n):
            sequences.extend(generate_sequences(prefix + [i], length - 1))
        return sequences

    def count_valid_sequences(prefix):
        if len(prefix) == n - 1:
            return 1 if is_valid_sequence(prefix) else 0
        count = 0
        for i in range(1, n):
            if not (sum(prefix) + i) % n == 0:
                count += count_valid_sequences(prefix + [i])
        return count

    def find_kth(prefix, k):
        if len(prefix) == n - 1:
            return prefix
        for i in range(1, n):
            if not (sum(prefix) + i) % n == 0:
                count = count_valid_sequences(prefix + [i])
                if k <= count:
                    return find_kth(prefix + [i], k)
                k -= count
        return None

    return find_kth([], k)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    n, k = map(int, data.split())
    result = find_kth_sequence(n, k)
    print(" ".join(map(str, result)))