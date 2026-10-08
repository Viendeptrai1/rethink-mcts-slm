import sys

def min_cost(c1, c2, c3, c4, n, m, a, b):
    # Calculate the cost of buying individual tickets for each bus and trolley
    cost_individual_buses = sum(a[i] * c1 for i in range(n))
    cost_individual_trolleys = sum(b[i] * c1 for i in range(m))
    
    # Calculate the cost of buying unlimited tickets for each bus and trolley
    cost_unlimited_buses = min(sum(a), n) * c2
    cost_unlimited_trolleys = min(sum(b), m) * c2
    
    # Calculate the cost of buying unlimited tickets for all buses or all trolleys
    cost_all_buses = c3
    cost_all_trolleys = c3
    
    # Calculate the cost of buying the all-inclusive ticket
    cost_all_inclusive = c4
    
    # Calculate the minimum cost for buses
    min_cost_buses = min(cost_individual_buses, cost_unlimited_buses, cost_all_buses)
    
    # Calculate the minimum cost for trolleys
    min_cost_trolleys = min(cost_individual_trolleys, cost_unlimited_trolleys, cost_all_trolleys)
    
    # Calculate the total minimum cost
    total_min_cost = min(min_cost_buses + min_cost_trolleys, cost_all_inclusive)
    
    return total_min_cost

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    c1 = int(data[0])
    c2 = int(data[1])
    c3 = int(data[2])
    c4 = int(data[3])
    
    n = int(data[4])
    m = int(data[5])
    
    a = list(map(int, data[6:6+n]))
    b = list(map(int, data[6+n:6+n+m]))
    
    result = min_cost(c1, c2, c3, c4, n, m, a, b)
    print(result)

if __name__ == "__main__":
    main()