def find_arithmetic_sequence(n, a, d):
    from itertools import count

    def fibonacci():
        f0, f1 = 0, 1
        while True:
            yield f0
            f0, f1 = f1, f0 + f1

    def last_18_digits(num):
        return str(num)[-18:]

    def check_sequence(b, e):
        fib_gen = fibonacci()
        for i in range(n):
            fib_value = next(fib_gen)
            while fib_value < a + i * d:
                fib_value = next(fib_gen)
            fib_str = last_18_digits(fib_value)
            if str(a + i * d) not in fib_str:
                return False
        return True

    for b in range(1, int(2**64)):
        for e in range(1, int(2**64)):
            if check_sequence(b, e):
                print(b, e)
                return

    print(-1)