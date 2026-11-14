import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    c1 = int(next(iterator))
    c2 = int(next(iterator))
    c3 = int(next(iterator))
    c4 = int(next(iterator))
    
    n = int(next(iterator))
    m = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
        
    b = []
    for _ in range(m):
        b.append(int(next(iterator)))
        
    # Calculate minimum cost for buses
    # Option 1: Pay per ride or unlimited per bus for each bus, then sum up
    # For each bus i, cost is min(a[i] * c1, c2)
    bus_cost_individual = 0
    for rides in a:
        bus_cost_individual += min(rides * c1, c2)
        
    # Option 2: Unlimited for all buses (c3)
    bus_cost_all = c3
    
    # Minimum cost for buses is the minimum of these two options
    min_bus_cost = min(bus_cost_individual, bus_cost_all)
    
    # Calculate minimum cost for trolleys
    # Option 1: Pay per ride or unlimited per trolley for each trolley, then sum up
    trolley_cost_individual = 0
    for rides in b:
        trolley_cost_individual += min(rides * c1, c2)
        
    # Option 2: Unlimited for all trolleys (c3)
    trolley_cost_all = c3
    
    # Minimum cost for trolleys is the minimum of these two options
    min_trolley_cost = min(trolley_cost_individual, trolley_cost_all)
    
    # Total cost without the global unlimited ticket
    total_cost_without_global = min_bus_cost + min_trolley_cost
    
    # Option 3: Global unlimited ticket (c4)
    total_cost_with_global = c4
    
    # The answer is the minimum of the two strategies
    print(min(total_cost_without_global, total_cost_with_global))

if __name__ == "__main__":
    solve()