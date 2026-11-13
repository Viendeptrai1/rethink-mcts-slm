from typing import List
import heapq

def min_day_to_play(n: int, m: int, k: List[int], offers: List[List[int]]) -> int:
    # Initialize variables
    days = [float('inf')] * (n + 1)
    pq = []
    
    # Parse offers and store them in a dictionary
    offer_dict = [[] for _ in range(n + 1)]
    for d, t in offers:
        offer_dict[t].append(d)
    
    # Initialize the priority queue with the initial state
    heapq.heappush(pq, (0, 0))
    
    while pq:
        current_cost, current_day = heapq.heappop(pq)
        
        # Check if we have already found a better day for this state
        if current_day >= days[k.index(current_cost)]:
            continue
        
        # Update the day for this state
        days[k.index(current_cost)] = current_day
        
        # Try to buy more microtransactions
        for i in range(1, n + 1):
            if k[i - 1] > current_cost:
                new_cost = current_cost + 2
                if i in offer_dict:
                    new_cost -= 1
                heapq.heappush(pq, (new_cost, current_day + 1))
    
    # Find the minimum day to start playing
    return max(days)

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = list(map(int, data[2:2+n]))
    offers = [[int(data[2+n+2*i]), int(data[2+n+2*i+1])] for i in range(m)]
    
    result = min_day_to_play(n, m, k, offers)
    print(result)