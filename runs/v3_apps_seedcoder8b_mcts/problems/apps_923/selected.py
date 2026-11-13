def is_real_puzzle(n, active_tooth_sequence):
    def rotate_clockwise(x):
        return (x + 1) % n

    def rotate_counterclockwise(x):
        return (x - 1 + n) % n

    def simulate_rotation(initial_sequence):
        current_sequence = initial_sequence[:]
        for i in range(n):
            if i % 2 == 0:
                current_sequence[i] = rotate_clockwise(current_sequence[i])
            else:
                current_sequence[i] = rotate_counterclockwise(current_sequence[i])
        return current_sequence

    target_sequence = list(range(n))
    current_sequence = active_tooth_sequence[:]

    for _ in range(n):
        if current_sequence == target_sequence:
            return "Yes"
        current_sequence = simulate_rotation(current_sequence)

    return "No"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    active_tooth_sequence = list(map(int, data[1:]))
    print(is_real_puzzle(n, active_tooth_sequence))