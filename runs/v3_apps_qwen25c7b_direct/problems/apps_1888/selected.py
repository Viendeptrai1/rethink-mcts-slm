from collections import defaultdict

def min_debts(n, m, debts):
    balance = defaultdict(int)
    
    for a, b, c in debts:
        balance[a] += c
        balance[b] -= c
    
    positive_balances = [bal for bal in balance.values() if bal > 0]
    negative_balances = [-bal for bal in balance.values() if bal < 0]
    
    return sum(sorted(positive_balances + negative_balances)[:len(positive_balances)])

# Example usage:
n, m = map(int, input().split())
debts = [tuple(map(int, input().split())) for _ in range(m)]
print(min_debts(n, m, debts))