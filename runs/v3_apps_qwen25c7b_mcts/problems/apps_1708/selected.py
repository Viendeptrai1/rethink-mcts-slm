import heapq
from sys import stdin, stdout

def main():
    input = stdin.read
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
            heapq.heappush(heap, (c[i], i, a[i]))
    
    results = []
    for t, d in orders:
        cost = 0
        while d > 0 and heap:
            price, kind, count = heapq.heappop(heap)
            if count >= d:
                cost += d * price
                count -= d
                d = 0
            else:
                cost += count * price
                d -= count
        
        if d == 0:
            results.append(cost)
        else:
            results.append(0)
        
        if count > 0:
            heapq.heappush(heap, (price, kind, count))
    
    for result in results:
        stdout.write(f"{result}\n")

if __name__ == "__main__":
    main()