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

    # Precompute optimal cost for a single vehicle given its usage count
    # For a vehicle with k rides:
    # Option 1: k * c1
    # Option 2: c2
    # Best single vehicle cost = min(k * c1, c2)
    
    def get_single_vehicle_cost(rides):
        return min(rides * c1, c2)

    # Calculate total cost for all buses if we treat them individually
    # Then compare with buying a global bus pass (c3)
    bus_individual_total = sum(get_single_vehicle_cost(rides) for rides in a)
    bus_pass_cost = min(bus_individual_total, c3)

    # Calculate total cost for all trolleys if we treat them individually
    # Then compare with buying a global trolley pass (c3)
    trolley_individual_total = sum(get_single_vehicle_cost(rides) for rides in b)
    trolley_pass_cost = min(trolley_individual_total, c3)

    # Now we have two main strategies for the whole set:
    # 1. Pay for buses and trolleys separately (using the best mix of individual and c3)
    #    Total = bus_pass_cost + trolley_pass_cost
    # 2. Buy the global pass for everything (c4)
    #    Total = c4
    
    ans = min(bus_pass_cost + trolley_pass_cost, c4)

    print(ans)

if __name__ == "__main__":
    solve()