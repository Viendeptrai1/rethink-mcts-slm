import sys
from heapq import heappop, heappush

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    c = list(map(int, data[index:index + n]))
    index += n
    
    orders = []
    for _ in range(m):
        t = int(data[index]) - 1
        d = int(data[index + 1])
        index += 2
        orders.append((t, d))
    
    heap = []
    for i in range(n):
        if a[i] > 0:
            heappush(heap, (c[i], i))
    
    results = []
    for t, d in orders:
        cost = 0
        while d > 0:
            if heap:
                cost += heap[0][0]
                _, i = heappop(heap)
                a[i] -= 1
                if a[i] > 0:
                    heappush(heap, (c[i], i))
                d -= 1
            else:
                break
        results.append(cost)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()