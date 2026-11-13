def get_odd_collatz(n):
    def collatz_sequence(num):
        while num != 1:
            yield num
            if num % 2 == 0:
                num //= 2
            else:
                num = 3 * num + 1
        yield num

    return sorted([x for x in collatz_sequence(n) if x % 2 != 0])