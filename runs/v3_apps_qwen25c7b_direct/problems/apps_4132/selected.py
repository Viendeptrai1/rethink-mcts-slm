import sys
from heapq import heappop, heappush

def min_final_health(N, A):
    heap = [-a for a in A]
    while len(heap) > 1:
        a = -heappop(heap)
        b = -heappop(heap)
        if a > b:
            heappush(heap, -(a - b))
    return -heap[0]

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    A = list(map(int, data[1:]))
    print(min_final_health(N, A))