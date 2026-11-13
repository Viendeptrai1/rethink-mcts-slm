def minimize_debts(n, debts):
    from collections import defaultdict

    # Calculate net debts for each person
    net_debts = defaultdict(int)
    for a, b, c in debts:
        net_debts[a] -= c
        net_debts[b] += c

    # Separate people into two groups: those who owe money and those who are owed money
    debtors = []
    creditors = []
    for person, debt in net_debts.items():
        if debt < 0:
            debtors.append((person, -debt))
        elif debt > 0:
            creditors.append((person, debt))

    # Sort debtors and creditors by the amount of debt/credit
    debtors.sort(key=lambda x: x[1])
    creditors.sort(key=lambda x: x[1])

    # Minimize the total debt by settling debts between debtors and creditors
    i, j = 0, 0
    total_debt = 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]

        # Determine the amount to settle
        settle_amount = min(debt_amount, credit_amount)
        total_debt += settle_amount

        # Update the remaining debt/credit
        debtors[i] = (debtor, debt_amount - settle_amount)
        creditors[j] = (creditor, credit_amount - settle_amount)

        # Move to the next debtor or creditor if their debt/credit is settled
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return total_debt

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
debts = []
index = 2
for _ in range(m):
    a = int(data[index])
    b = int(data[index + 1])
    c = int(data[index + 2])
    debts.append((a, b, c))
    index += 3

# Output the result
print(minimize_debts(n, debts))