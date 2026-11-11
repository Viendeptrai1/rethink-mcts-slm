def min_cost(c1, c2, c3, c4, n, m, a, b):
    # Calculate the cost if Vasya buys individual tickets for each bus and trolley
    cost_individual = sum(a[i] * c1 for i in range(n)) + sum(b[i] * c1 for i in range(m))
    
    # Calculate the cost if Vasya buys unlimited tickets for each bus and trolley
    cost_unlimited_per_transport = min(sum(a[i] for i in range(n)) * c2, c3) + min(sum(b[i] for i in range(m)) * c2, c3)
    
    # Calculate the cost if Vasya buys unlimited tickets for all buses and all trolleys
    cost_unlimited_all = c4
    
    # The minimum cost is the smallest of the three calculated costs
    return min(cost_individual, cost_unlimited_per_transport, cost_unlimited_all)

# Read input
c1, c2, c3, c4 = map(int, input().split())
n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Calculate and print the minimum cost
print(min_cost(c1, c2, c3, c4, n, m, a, b))