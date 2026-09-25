import sys

def main():
    import sys
    import bisect

    def read_ints():
        return list(map(int, sys.stdin.read().split()))

    data = read_ints()
    n = data[0]
    a = data[1:]

    # Initialize two arrays to store the best increasing sequence ending at each position
    left_to_right = [1] * n
    right_to_left = [1] * n

    # Fill left_to_right array
    for i in range(1, n):
        if a[i] > a[i - 1]:
            left_to_right[i] = left_to_right[i - 1] + 1

    # Fill right_to_left array
    for i in range(n - 2, -1, -1):
        if a[i] < a[i + 1]:
            right_to_left[i] = right_to_left[i + 1] + 1

    # Find the maximum length of the increasing sequence
    max_length = 0
    best_sequence = []

    for i in range(n):
        # Consider the sequence starting from the left
        left_length = left_to_right[i]
        # Consider the sequence starting from the right
        right_length = right_to_left[i]

        # The total length considering both directions
        total_length = left_length + right_length - 1

        if total_length > max_length:
            max_length = total_length
            best_sequence = ['L'] * left_length + ['R'] * (right_length - 1)

    # Print the result
    print(max_length)
    print(''.join(best_sequence))

if __name__ == "__main__":
    main()