def optimize_debts(n, debts):
    from collections import defaultdict

    balance = defaultdict(int)

    for a, b, c in debts:
        balance[a] -= c
        balance[b] += c

    # Filter out people with zero balance
    balances = [amount for amount in balance.values() if amount != 0]

    def settle(start):
        if start == len(balances):
            return 0
        if balances[start] == 0:
            return settle(start + 1)
        
        min_debt = float('inf')
        for i in range(start + 1, len(balances)):
            if balances[start] * balances[i] < 0:  # Opposite signs can settle
                balances[i] += balances[start]
                min_debt = min(min_debt, balances[start] * -1 + settle(start + 1))
                balances[i] -= balances[start]
        
        return min_debt
    
    return settle(0)

# Reading input
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

print(optimize_debts(n, debts))