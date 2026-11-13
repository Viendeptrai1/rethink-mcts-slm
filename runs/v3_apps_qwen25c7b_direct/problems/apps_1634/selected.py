def min_transport_cost(c1, c2, c3, c4, n, m, a, b):
    total_rides_buses = sum(a)
    total_rides_trolleys = sum(b)
    
    # Calculate the cost if buying individual tickets
    individual_cost = total_rides_buses * c1 + total_rides_trolleys * c1
    
    # Calculate the cost if buying unlimited tickets for buses and trolleys separately
    unlimited_bus_cost = c2 * n
    unlimited_trolley_cost = c2 * m
    combined_unlimited_cost = min(unlimited_bus_cost + unlimited_trolley_cost, c3)
    
    # Calculate the cost if buying unlimited tickets for all buses and trolleys together
    unlimited_all_cost = c4
    
    # Return the minimum cost among the above options
    return min(individual_cost, combined_unlimited_cost, unlimited_all_cost)

# Example usage:
if __name__ == "__main__":
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
    b = list(map(int, data[6+n:]))
    
    result = min_transport_cost(c1, c2, c3, c4, n, m, a, b)
    print(result)