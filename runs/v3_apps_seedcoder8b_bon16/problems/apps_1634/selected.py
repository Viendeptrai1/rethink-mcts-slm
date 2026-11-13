def solve():
    c1, c2, c3, c4 = map(int, input().split())
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    total_rides = sum(a) + sum(b)
    
    # Case 1: Buy individual tickets
    cost1 = sum(min(ride * c1, c2) for ride in a + b)

    # Case 2: Buy tickets for buses or trolleys
    cost2 = min(c3, c2 * n) + min(c3, c2 * m)

    # Case 3: Buy combined ticket
    cost3 = c4

    return min(cost1, cost2, cost3)

print(solve())