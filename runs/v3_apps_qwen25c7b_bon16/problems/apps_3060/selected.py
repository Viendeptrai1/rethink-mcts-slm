from sys import stdin, stdout

def find_kth_sequence(n, k):
    def is_valid(seq):
        for i in range(len(seq)):
            for j in range(i + 1, len(seq) + 1):
                if sum(seq[i:j]) % n == 0:
                    return False
        return True

    def generate_sequences(current):
        if len(current) == n - 1:
            if is_valid(current):
                return [current]
            else:
                return []
        result = []
        for i in range(1, n):
            result.extend(generate_sequences(current + [i]))
        return result

    sequences = generate_sequences([])
    return sequences[k - 1]

def main():
    n, k = map(int, stdin.readline().split())
    result = find_kth_sequence(n, k)
    stdout.write(' '.join(map(str, result)) + '\n')

if __name__ == "__main__":
    main()