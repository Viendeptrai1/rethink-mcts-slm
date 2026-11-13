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

    positive_balance = []
    negative_balance = []

    for i in range(1, n + 1):
        if balance[i] > 0:
            positive_balance.append(balance[i])
        elif balance[i] < 0:
            negative_balance.append(balance[i])

    if not positive_balance and not negative_balance:
        print(0)
        return

    # We need to match positive balances (creditors) with negative balances (debtors)
    # to minimize the total sum of transactions.
    # This is equivalent to finding a minimum cost flow or can be solved greedily.
    # Since the total sum of positives equals the absolute sum of negatives,
    # we can simulate the process: take the largest creditor and largest debtor
    # and settle as much as possible between them.

    pos_idx = 0
    neg_idx = 0
    total_debt = 0

    while pos_idx < len(positive_balance) and neg_idx < len(negative_balance):
        p = positive_balance[pos_idx]
        n_val = negative_balance[neg_idx]  # This is negative

        transfer = min(p, abs(n_val))
        total_debt += transfer

        positive_balance[pos_idx] -= transfer
        negative_balance[neg_idx] += transfer

        if positive_balance[pos_idx] == 0:
            pos_idx += 1
        if negative_balance[neg_idx] == 0:
            neg_idx += 1

    print(total_debt)

if __name__ == "__main__":
    solve()