import heapq

def min_cost(n, k, a, b):
    pq = []
    for i in range(k):
        heapq.heappush(pq, (a[i], b[i]))
    
    for i in range(k, n):
        if pq[0][0] <= pq[0][1]:
            _, b_min = heapq.heappop(pq)
            heapq.heappush(pq, (a[i], b_min))
        else:
            a_min, _ = heapq.heappop(pq)
            heapq.heappush(pq, (a_min, b[i]))
    
    return sum(x[0] for x in pq)

# Example usage
n = 8
k = 4
a = [3, 8, 7, 9, 9, 4, 6, 8]
b = [2, 5, 9, 4, 3, 8, 9, 1]
print(min_cost(n, k, a, b))  # Output: 32