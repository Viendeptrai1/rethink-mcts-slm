def get_odd_collatz(n):
    """
    Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence.
    """
    odds = []
    while n != 1:
        if n % 2 == 1:
            odds.append(n)
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    odds.append(1)
    return sorted(odds)