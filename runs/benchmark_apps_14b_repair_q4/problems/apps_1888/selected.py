import sys

def min_debt_sum(n, m, debts):
    balances = [0] * (n + 1)
    
    for a, b, c in debts:
        balances[a] -= c
        balances[b] += c
    
    positive_balances = [balance for balance in balances if balance > 0]
    negative_balances = [-balance for balance in balances if balance < 0]
    
    positive_balances.sort()
    negative_balances.sort()
    
    total_debt = 0
    i, j = 0, 0
    
    while i < len(positive_balances) and j < len(negative_balances):
        if positive_balances[i] < negative_balances[j]:
            total_debt += positive_balances[i]
            i += 1
        elif positive_balances[i] > negative_balances[j]:
            total_debt += negative_balances[j]
            j += 1
        else:
            total_debt += positive_balances[i]
            i += 1
            j += 1
    
    return total_debt

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    debts = []
    for _ in range(m):
        a = int(data[index])
        b = int(data[index + 1])
        c = int(data[index + 2])
        debts.append((a, b, c))
        index += 3
    
    result = min_debt_sum(n, m, debts)
    print(result)

if __name__ == "__main__":
    main()