import heapq

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    a = list(map(int, data[2:2+n]))
    c = list(map(int, data[2+n:2+2*n]))
    
    orders = []
    for i in range(m):
        t = int(data[2+2*n+i*2]) - 1
        d = int(data[2+2*n+i*2+1])
        orders.append((t, d))
    
    # Priority queue to store available dishes by cost
    pq = []
    for i in range(n):
        if a[i] > 0:
            heapq.heappush(pq, (c[i], i, a[i]))
    
    results = []
    for t, d in orders:
        cost = 0
        while d > 0:
            if pq and pq[0][1] == t and pq[0][2] > 0:
                # Serve from the ordered type if available
                cost_c, idx, count = heapq.heappop(pq)
                serve_count = min(d, count)
                cost += serve_count * cost_c
                d -= serve_count
                if count - serve_count > 0:
                    heapq.heappush(pq, (cost_c, idx, count - serve_count))
            elif pq:
                # Serve from the cheapest available type
                cost_c, idx, count = heapq.heappop(pq)
                serve_count = min(d, count)
                cost += serve_count * cost_c
                d -= serve_count
                if count - serve_count > 0:
                    heapq.heappush(pq, (cost_c, idx, count - serve_count))
            else:
                # No dishes left to serve
                break
        results.append(cost)
    
    for result in results:
        print(result)

# Uncomment the following line to run the function when the script is executed
# solve()