import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    ptr = 0
    c1 = int(data[ptr]); ptr += 1
    c2 = int(data[ptr]); ptr += 1
    c3 = int(data[ptr]); ptr += 1
    c4 = int(data[ptr]); ptr += 1
    
    n = int(data[ptr]); ptr += 1
    m = int(data[ptr]); ptr += 1
    
    a = []
    for _ in range(n):
        a.append(int(data[ptr])); ptr += 1
        
    b = []
    for _ in range(m):
        b.append(int(data[ptr])); ptr += 1
        
    # Cost to cover all rides on a specific vehicle using type 1 or type 2
    def cost_vehicle(rides, c1, c2):
        if rides == 0:
            return 0
        return min(rides * c1, c2)
    
    # Cost to cover all buses using type 1, type 2, or type 3
    # Type 3 covers all buses (and optionally all trolleys if we consider the combined option later, but here we calculate isolated bus cost for the "all buses" ticket)
    # Actually, type 3 is "unlimited rides on all buses OR all trolleys".
    # So for the bus side, the options are:
    # 1. Pay for each bus individually (sum of cost_vehicle for each bus)
    # 2. Pay c3 for the "all buses" ticket.
    
    bus_costs = [cost_vehicle(a[i], c1, c2) for i in range(n)]
    min_bus_individual = sum(bus_costs)
    min_bus_ticket = c3
    
    # Similarly for trolleys
    trolley_costs = [cost_vehicle(b[i], c1, c2) for i in range(m)]
    min_trolley_individual = sum(trolley_costs)
    min_trolley_ticket = c3
    
    # Now combine options for buses and trolleys
    # Option 1: Buy tickets for buses individually and trolleys individually
    option1 = min_bus_individual + min_trolley_individual
    
    # Option 2: Buy "all buses" ticket and trolleys individually
    option2 = min_bus_ticket + min_trolley_individual
    
    # Option 3: Buy buses individually and "all trolleys" ticket
    option3 = min_bus_individual + min_trolley_ticket
    
    # Option 4: Buy "all buses" and "all trolleys" tickets
    option4 = min_bus_ticket + min_trolley_ticket
    
    # Option 5: Buy the "all buses and all trolleys" ticket (type 4)
    option5 = c4
    
    print(min(option1, option2, option3, option4, option5))

if __name__ == "__main__":
    solve()