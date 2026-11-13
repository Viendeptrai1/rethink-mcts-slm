import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    balance = [0] * (n + 1)

    for _ in range(m):
        a = int(next(iterator))
        b = int(next(iterator))
        c = int(next(iterator))
        balance[a] -= c
        balance[b] += c

    positive_balance = 0
    negative_balance = 0

    for i in range(1, n + 1):
        if balance[i] > 0:
            positive_balance += balance[i]
        elif balance[i] < 0:
            negative_balance += abs(balance[i])

    # In a valid debt system, total money owed (negative balance sum) must equal
    # total money to be received (positive balance sum).
    # The minimum sum of debts required to settle all accounts is simply this total amount.
    print(positive_balance)

if __name__ == "__main__":
    solve()