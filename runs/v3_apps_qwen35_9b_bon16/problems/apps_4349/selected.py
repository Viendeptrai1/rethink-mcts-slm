import sys
from collections import deque, defaultdict

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
        
        k = []
        for _ in range(n):
            k.append(int(next(iterator)))
        
        offers = []
        for _ in range(m):
            d = int(next(iterator))
            t = int(next(iterator))
            offers.append((d, t))
    except StopIteration:
        return

    # Group offers by item type
    # best_offer[t] = list of days when item t is on sale, sorted ascending
    best_offer = defaultdict(list)
    for d, t in offers:
        best_offer[t].append(d)

    # For each item, if there are any offers, we only care about the earliest offer day
    # because if we can buy on an earlier sale day, we prefer that to save money or time.
    # Actually, we need to check: for a fixed deadline D, can we buy everything?
    # But we are binary searching on the answer (day).
    
    # Precompute: for each item i, what is the latest day <= D when it is on sale?
    # If no sale day <= D, then we must buy at full price (2 burles) anytime after day D is not possible for sale,
    # so we must have bought it by day D at full price or on a sale day <= D.
    
    # Let's define:
    # count_cheap[i] = number of items of type i we want to buy on sale.
    # If we decide that the deadline is D, then for each item type i:
    #   If there exists a sale day d_i <= D, we should buy as many as possible on that day (or any sale day <= D).
    #   However, we can only buy one item per day? No, we can buy any number of items as long as we have money.
    #   Money accumulates: 1 burle per day starting day 1.
    #   On day D, total money = D.
    #   Cost = 2 * (items bought at full price) + 1 * (items bought on sale).
    #   Constraint: We must buy all items by day D.
    #   For an item of type i:
    #     If we buy it on sale, it must be on a day d <= D where type i is on sale.
    #     If we don't buy it on sale (either no sale day <= D or we chose not to), we pay 2.
    #   To minimize cost, we want to maximize items bought on sale.
    #   However, there is a constraint on timing: we cannot spend money before we earn it.
    #   But since we can buy any number of items on a single day if we have enough accumulated money, 
    #   the only constraint is that the total cost must be <= D (total money earned by day D).
    #   Wait, is that true? 
    #   Example: Day 1: earn 1. Can we buy a 2-burle item? No.
    #   So we can only buy items on day D if we have accumulated enough money by day D.
    #   Total cost <= D is necessary and sufficient? 
    #   Yes, because we can defer all purchases to day D (the last day). 
    #   On day D, we have D burles. If total cost <= D, we can buy everything on day D.
    #   BUT, we can only buy an item on sale on its specific sale days.
    #   If an item has a sale day d <= D, we can buy it on day d (on sale) or on any day <= D (full price).
    #   If the cheapest way to buy item i is on sale day d_i (which is <= D), we pay 1.
    #   Otherwise, we pay 2.
    #   So for a fixed D, the minimum cost is:
    #     sum over all items of (1 if (item i has sale day <= D) else 2)
    #     = 2 * (total items) - sum over all items (1 if (item i has sale day <= D))
    #   Let S_D be the count of items that have at least one sale day <= D.
    #   Total cost = 2 * total_items - S_D.
    #   Condition: 2 * total_items - S_D <= D.
    
    # Is this correct?
    # Let's re-read carefully: "Ivan can order any (possibly zero) number of microtransactions of any types during any day".
    # "If the microtransaction he wants to order is on sale then he can buy it for 1 burle".
    # This implies if on day d, type t is on sale, we can buy type t for 1.
    # If we buy type t on a day when it is NOT on sale, we pay 2.
    # We need to buy k_i copies of type i.
    # For each copy of type i, we can choose to buy it on a sale day (if available <= D) for 1, or full price for 2.
    # To minimize cost, for each copy, if there is a sale day <= D, we buy it for 1.
    # If there is no sale day <= D, we must buy it for 2.
    # So yes, the logic holds.
    
    # Algorithm:
    # Binary search for D in range [1, 200000 + 200000] (max day could be large if no sales and many items? 
    # Max items = 2e5, cost = 2 * 2e5 = 4e5. So D up to 4e5 is enough.
    # Max offer day is 2e5. Max k sum is 2e5.
    # Upper bound: 2 * 200000 = 400000. Let's use 400005.
    
    total_items = sum(k)
    
    # Precompute for each item type, the earliest sale day
    # Actually, we need to know if there is ANY sale day <= D.
    # Since offers are given, for each item type i, let min_sale_day[i] be the minimum d_j where t_j = i.
    # If no offers for type i, min_sale_day[i] = infinity.
    
    min_sale_day = {}
    for t in range(1, n+1):
        if t in best_offer and best_offer[t]:
            min_sale_day[t] = best_offer[t][0]  # already sorted
        else:
            min_sale_day[t] = float('inf')
    
    # Now binary search
    low = 1
    high = 400005 # Sufficiently large
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        
        # Calculate min cost for deadline mid
        # Items with sale day <= mid cost 1, others cost 2.
        # Count items with sale day <= mid.
        # We can iterate over all types. n is up to 2e5. Doing this inside binary search (log(4e5) ~ 19) is 2e5*19 ~ 3.8e6 ops. Acceptable.
        
        count_sale = 0
        for t in range(1, n+1):
            if k[t-1] > 0:
                sd = min_sale_day[t]
                if sd <= mid:
                    count_sale += k[t-1]
        
        needed_money = 2 * total_items - count_sale
        if needed_money <= mid:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    print(ans)

if __name__ == '__main__':
    solve()