def is_real_puzzle(n, sequence):
    for _ in range(n):
        if sequence == list(range(n)):
            return "Yes"
        next_sequence = []
        for i in range(n):
            if i % 2 == 0:
                next_sequence.append((sequence[i] + 1) % n)
            else:
                next_sequence.append((sequence[i] - 1) % n)
        sequence = next_sequence
    return "No"

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    sequence = list(map(int, data[1:]))
    result = is_real_puzzle(n, sequence)
    print(result)