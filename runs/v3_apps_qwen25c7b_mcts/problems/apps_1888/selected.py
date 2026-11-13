from collections import defaultdict
import heapq

def min_debt_sum(n, m, debts):
    # Create dictionaries to store the net balance for each person
    balance = defaultdict(int)
    
    # Calculate the net balance for each person
    for a, b, c in debts:
        balance[a] += c
        balance[b] -= c
    
    # Separate positive and negative balances into heaps
    pos_heap = []
    neg_heap = []
    for bal in balance.values():
        if bal > 0:
            heapq.heappush(pos_heap, -bal)
        elif bal < 0:
            heapq.heappush(neg_heap, bal)
    
    # Calculate the minimum sum of debts
    total_debt = 0
    while pos_heap and neg_heap:
        pos = -heapq.heappop(pos_heap)
        neg = heapq.heappop(neg_heap)
        transfer = min(pos, -neg)
        total_debt += transfer
        if pos > transfer:
            heapq.heappush(pos_heap, -(pos - transfer))
        if neg < transfer:
            heapq.heappush(neg_heap, neg + transfer)
    
    return total_debt

# Example usage:
n, m = map(int, input().split())
debts = [tuple(map(int, input().split())) for _ in range(m)]
print(min_debt_sum(n, m, debts))