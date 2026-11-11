import sys
from collections import defaultdict

def min_debt_sum(n, m, debts):
    balance = [0] * (n + 1)
    for a, b, c in debts:
        balance[a] -= c
        balance[b] += c
    
    positive_balance = [b for b in balance if b > 0]
    negative_balance = [-b for b in balance if b < 0]
    
    positive_balance.sort()
    negative_balance.sort()
    
    total_debt = 0
    i, j = 0, 0
    while i < len(positive_balance) and j < len(negative_balance):
        if positive_balance[i] < negative_balance[j]:
            total_debt += positive_balance[i]
            negative_balance[j] -= positive_balance[i]
            i += 1
        elif positive_balance[i] > negative_balance[j]:
            total_debt += negative_balance[j]
            positive_balance[i] -= negative_balance[j]
            j += 1
        else:
            total_debt += positive_balance[i]
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