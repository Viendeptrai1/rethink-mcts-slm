import sys
import heapq

def min_partition_value(n, c, a):
    total_sum = sum(a)
    min_heap = []
    current_sum = 0
    result = 0
    
    for i in range(n):
        current_sum += a[i]
        heapq.heappush(min_heap, a[i])
        
        if len(min_heap) > c:
            smallest = heapq.heappop(min_heap)
            current_sum -= smallest
        
        if len(min_heap) == c:
            result += current_sum
    
    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:]))
    
    print(min_partition_value(n, c, a))