def get_odd_collatz(n):
    def collatz_sequence(num):
        while num != 1:
            yield num
            if num % 2 == 0:
                num //= 2
            else:
                num = 3 * num + 1
        yield 1

    return sorted([num for num in collatz_sequence(n) if num % 2 != 0])