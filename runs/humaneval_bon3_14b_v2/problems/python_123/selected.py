def get_odd_collatz(n):
    def collatz_sequence(x):
        sequence = []
        while x != 1:
            sequence.append(x)
            if x % 2 == 0:
                x = x // 2
            else:
                x = 3 * x + 1
        sequence.append(1)
        return sequence

    sequence = collatz_sequence(n)
    odd_numbers = [num for num in sequence if num % 2 != 0]
    return sorted(odd_numbers)

# Example usage:
# print(get_odd_collatz(5))  # Output: [1, 5]