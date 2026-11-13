def min_ticket_cost(c1, c2, c3, c4, n, m, a, b):
    # Calculate the total number of rides
    total_rides = sum(a) + sum(b)
    
    # Calculate the number of buses and trolleys used
    buses_used = sum(1 for rides in a if rides > 0)
    trolleys_used = sum(1 for rides in b if rides > 0)
    
    # Calculate the cost for each strategy
    cost1 = total_rides * c1
    cost2 = (sum(a) * c1 + sum(b) * c1) - min(sum(a), sum(b)) * c2
    cost3 = (sum(a) * c1 + sum(b) * c1) - (buses_used * c2 + trolleys_used * c2) + c3
    cost4 = c4
    
    # Return the minimum cost among all strategies
    return min(cost1, cost2, cost3, cost4)

# Read input
c1, c2, c3, c4 = map(int, input().split())
n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Calculate and print the result
result = min_ticket_cost(c1, c2, c3, c4, n, m, a, b)
print(result)