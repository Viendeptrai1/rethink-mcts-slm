def tri(n):
    def tribonacci(n):
        if n == 1:
            return 3
        elif n % 2 == 0:
            return 1 + n / 2
        else:
            return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n + 1)

    return [tribonacci(i) for i in range(1, n + 2)]