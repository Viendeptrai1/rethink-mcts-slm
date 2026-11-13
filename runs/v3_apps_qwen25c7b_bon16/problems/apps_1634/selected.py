def min_transport_cost(c1, c2, c3, c4, n, m, a, b):
    total_cost = 0
    
    # Calculate cost for buses
    if c3 <= c2 + sum(a):
        total_cost += c3 * n
    else:
        for ai in a:
            if c1 * ai < c2:
                total_cost += c1 * ai
            else:
                total_cost += c2
    
    # Calculate cost for trolleys
    if c4 <= c2 + sum(b):
        total_cost += c4 * m
    else:
        for bi in b:
            if c1 * bi < c2:
                total_cost += c1 * bi
            else:
                total_cost += c2
    
    return total_cost

# Input reading
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

# Output the result
print(min_transport_cost(c1, c2, c3, c4, n, m, a, b))