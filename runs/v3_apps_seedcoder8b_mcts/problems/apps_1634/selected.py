def min_ticket_cost(c1, c2, c3, c4, n, m, a, b):
    # Calculate the total number of rides
    total_rides = sum(a) + sum(b)
    
    # Calculate the cost for individual tickets
    cost_individual = sum(min(ride * c1, c2) for ride in a) + sum(min(ride * c1, c2) for ride in b)
    
    # Calculate the cost for unlimited tickets on buses and trolleys separately
    cost_unlimited_buses = min(sum(a) * c1, c3)
    cost_unlimited_trolleys = min(sum(b) * c1, c3)
    
    # Calculate the cost for unlimited tickets on all buses and trolleys
    cost_unlimited_all = min(total_rides * c1, c4)
    
    # Return the minimum of all calculated costs
    return min(cost_individual, cost_unlimited_buses + cost_unlimited_trolleys, cost_unlimited_all)

# Read input
c1, c2, c3, c4 = map(int, input().split())
n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Calculate and print the result
result = min_ticket_cost(c1, c2, c3, c4, n, m, a, b)
print(result)